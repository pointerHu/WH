"""Raw video decoding. No fallback to synthetic/zero-valued audio features."""
from __future__ import annotations
import json
import subprocess
from pathlib import Path


class MediaError(ValueError):
    pass


def inspect_video(path, config):
    command = [config["ffprobe"], "-v", "error", "-protocol_whitelist", "file,pipe",
               "-show_format", "-show_streams", "-of", "json", str(path)]
    try:
        completed = subprocess.run(command, capture_output=True, timeout=20, check=True)
        meta = json.loads(completed.stdout)
    except (subprocess.SubprocessError, OSError, ValueError) as exc:
        raise MediaError("视频无法解码，或 FFprobe 不可用。请使用本地 MP4/AVI/MOV/MKV/WebM 文件。") from exc
    videos = [s for s in meta.get("streams", []) if s.get("codec_type") == "video"]
    audios = [s for s in meta.get("streams", []) if s.get("codec_type") == "audio"]
    if not videos:
        raise MediaError("文件不包含视频流。")
    if not audios:
        raise MediaError("视频不含音轨。当前模型按音频与视觉双模态训练，不使用零向量冒充音频。")
    try:
        duration = float(meta.get("format", {}).get("duration", videos[0].get("duration", 0)))
    except (TypeError, ValueError) as exc:
        raise MediaError("无法确定视频时长。") from exc
    if not 0 < duration <= float(config["max_duration_seconds"]):
        raise MediaError("视频时长必须在 0 到 %s 秒之间。" % config["max_duration_seconds"])
    width, height = int(videos[0].get("width", 0)), int(videos[0].get("height", 0))
    if not 0 < width <= 4096 or not 0 < height <= 4096:
        raise MediaError("视频分辨率无效或超过 4096 像素限制。")
    return {"duration_seconds": duration, "width": width, "height": height,
            "has_audio": True, "audio_sample_rate": audios[0].get("sample_rate"),
            "audio_channels": audios[0].get("channels"), "video_codec": videos[0].get("codec_name")}


def decode_media(path, job_dir, config):
    import cv2
    import librosa
    import numpy as np
    import torch
    from PIL import Image
    from torchvision.transforms import ToPILImage
    metadata = inspect_video(path, config)
    cap = cv2.VideoCapture(str(path))
    try:
        count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if count < 1:
            raise MediaError("无法读取视频帧数。")
        midpoint = count // 2
        cap.set(cv2.CAP_PROP_POS_FRAMES, midpoint)
        ok, frame_bgr = cap.read()
        if not ok or frame_bgr is None:
            raise MediaError("无法解码视频中间帧。")
    finally:
        cap.release()
    preview = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
    preview.save(str(Path(job_dir) / "preview.jpg"))
    if config["preprocess_profile"] == "legacy":
        # Match the pinned repository literally: BGR -> float32 (0..255) -> ToPILImage.
        # ToPILImage scales floating tensors by 255; this historical behavior is NOT
        # silently 'corrected'. See docs/architecture.md before using RGB instead.
        tensor = torch.from_numpy(frame_bgr).to(torch.float32).permute(2, 0, 1)
        model_image = ToPILImage()(tensor)
    else:
        model_image = preview
    model_image.save(str(Path(job_dir) / "model_input.jpg"))
    wav = Path(job_dir) / "decoded_audio.wav"
    command = [config["ffmpeg"], "-nostdin", "-v", "error", "-y",
               "-protocol_whitelist", "file,pipe", "-i", str(path),
               "-map", "0:a:0", "-vn", "-t", str(config["max_duration_seconds"]),
               "-acodec", "pcm_s16le", str(wav)]
    try:
        subprocess.run(command, capture_output=True, timeout=45, check=True)
    except (subprocess.SubprocessError, OSError) as exc:
        raise MediaError("音轨解码失败。") from exc
    audio, sr = librosa.load(str(wav), sr=32000, mono=True)
    if audio.size == 0 or not np.isfinite(audio).all():
        raise MediaError("音轨为空或包含非法采样值。")
    length = 320000
    start = max(0, audio.shape[-1] // 2 - length // 2)
    if audio.shape[-1] > length:
        audio = audio[start:start + length]
    elif audio.shape[-1] < length:
        audio = np.pad(audio, (0, length - audio.shape[-1]))
    audio = np.asarray(audio, dtype=np.float32)
    np.save(str(Path(job_dir) / "audio_32k_10s.npy"), audio, allow_pickle=False)
    metadata.update({"frame_index": midpoint, "frame_count": count,
                     "audio_start_seconds": start / 32000.0,
                     "audio_samples": length, "sample_rate": sr,
                     "preprocess_profile": config["preprocess_profile"],
                     "silent_audio": bool(np.max(np.abs(audio)) < 1e-7)})
    return model_image, torch.from_numpy(audio).unsqueeze(0), metadata
