"""Isolated model worker; invoked by the web server with server-owned job paths."""
from __future__ import annotations
import argparse
import os
import time
import traceback
from pathlib import Path
from runtime import load_config, read_json, write_json


def run(job_dir, config):
    import numpy as np
    import torch
    from model_adapter import KAClassifier, VideoBackbones
    from media import decode_media
    job_dir = Path(job_dir).resolve()
    request = read_json(job_dir / "request.json")
    started = time.monotonic()
    def progress(stage, percent, message):
        write_json(job_dir / "progress.json", {"stage": stage, "progress": percent, "message": message})
    torch.set_num_threads(4)
    metadata, timings, warnings = {}, {}, []
    kind = request["input_kind"]
    if kind == "raw_video":
        progress("decoding", 12, "正在分离音轨并读取中间帧")
        t = time.monotonic()
        image, waveform, metadata = decode_media(job_dir / request["stored_filename"], job_dir, config)
        timings["decode_seconds"] = time.monotonic() - t
        write_json(job_dir / "metadata.json", metadata)
        progress("encoding", 35, "CLIP / WavCaps 正在提取双模态特征")
        t = time.monotonic()
        backbones = VideoBackbones(config)
        audio, video = backbones.encode(image, waveform)
        metadata["clip_sha256"] = backbones.clip_sha256
        metadata["wavcaps_sha256"] = backbones.wavcaps_sha256
        timings["backbone_seconds"] = time.monotonic() - t
        del backbones
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        if metadata.get("silent_audio"):
            warnings.append("检测到近乎静音的音轨，结果可能不可靠。")
        warnings.append("原始视频提取与已有数据包的逐样本数值一致性尚需配对视频验证。")
        if config["preprocess_profile"] == "rgb":
            warnings.append("RGB 是修正预处理实验模式，不能宣称与旧训练特征一致。")
    elif kind == "cached_feature_validation":
        progress("features", 40, "正在读取真实 UCF 特征；此操作不测试视频编码器")
        sample_path = Path(config["bundle_dir"]) / "example_features.npz"
        with np.load(str(sample_path), allow_pickle=False) as sample:
            audio, video = sample["audio"], sample["video"]
            metadata["reference_class_id"] = int(sample["target"].item())
        warnings.append("本次输入为已有 UCF 特征，不是新上传视频；不能用于证明视频提取链路已跑通。")
    else:
        raise ValueError("Invalid input kind")
    np.savez_compressed(str(job_dir / "features.npz"), audio=audio, video=video)
    progress("classifying", 72, "KA-GZSL 正在匹配类别语义原型")
    t = time.monotonic()
    classifier = KAClassifier(config)
    result, logits, ids = classifier.predict(audio, video, request.get("mode", "gzsl"))
    timings["classifier_seconds"] = time.monotonic() - t
    np.savez_compressed(str(job_dir / "scores.npz"), logits=logits, class_ids=ids)
    warnings.extend([
        "置信分数是当前候选类别内的 softmax 相对分数，不等于准确率或经校准的正确概率。",
        "候选类别之外的事件仍会被分配给某个候选类别；本系统不声称具备开放世界拒识能力。"
    ])
    result.update({"input_kind": kind, "metadata": metadata, "timings": timings,
                   "elapsed_seconds": time.monotonic() - started,
                   "feature_dimensions": {"audio": 1024, "video": 512, "text": 1536},
                   "warnings": warnings})
    write_json(job_dir / "result.json", result)
    progress("complete", 100, "推理完成")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-dir", required=True)
    parser.add_argument("--config")
    args = parser.parse_args()
    os.environ.setdefault("MPLBACKEND", "Agg")
    try:
        run(args.job_dir, load_config(args.config))
    except Exception as exc:
        write_json(Path(args.job_dir) / "error.json", {"error": str(exc), "type": type(exc).__name__})
        traceback.print_exc()
        raise SystemExit(1)
