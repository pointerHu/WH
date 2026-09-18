"""Shared, dependency-free configuration and atomic job records."""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UPSTREAM_COMMIT = "085eae46195728fef3ad86b7a046528913f9bc39"


def read_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                    allow_nan=False), encoding="utf-8")
    os.replace(str(temporary), str(path))


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_config(path=None):
    config = read_json(ROOT / "config.example.json")
    local = Path(path or os.environ.get("KA_DEMO_CONFIG", ROOT / "config.local.json"))
    if local.exists():
        config.update(read_json(local))
    for key in ("model_python", "ka_repo", "bundle_dir", "clip_weights", "wavcaps_weights"):
        p = Path(config[key]).expanduser()
        config[key] = str(p if p.is_absolute() else ROOT / p)
    for key in ("ffmpeg", "ffprobe"):
        config[key] = shutil.which(config[key]) or config[key]
    if config["preprocess_profile"] not in ("legacy", "rgb"):
        raise ValueError("preprocess_profile must be legacy or rgb")
    if not 0 < float(config["temperature"]) < 100:
        raise ValueError("temperature must be finite and in (0, 100)")
    for key in ("max_upload_mb", "max_duration_seconds", "job_timeout_seconds", "retention_hours", "max_jobs"):
        if not 0 < float(config[key]) < 100000:
            raise ValueError("Invalid positive limit: " + key)
    return config


def readiness(config):
    bundle = Path(config["bundle_dir"])
    required = {
        "推理解释器": Path(config["model_python"]),
        "KA-GZSL 模型代码": Path(config["ka_repo"]) / "src/clipclap_model.py",
        "KA-GZSL 已训练权重": bundle / "model.pt",
        "类别语义向量": bundle / "class_bank.npz",
        "模型清单": bundle / "manifest.json",
    }
    missing_model = [name for name, path in required.items() if not path.is_file()]
    missing_video = list(missing_model)
    for name, key in (("CLIP ViT-B/32 权重", "clip_weights"), ("WavCaps HTSAT-BERT 权重", "wavcaps_weights")):
        if not Path(config[key]).is_file():
            missing_video.append(name)
    for name in ("ffmpeg", "ffprobe"):
        if not shutil.which(config[name]) and not Path(config[name]).is_file():
            missing_video.append(name)
    manifest = read_json(bundle / "manifest.json") if (bundle / "manifest.json").is_file() else {}
    return {
        "model_ready": not missing_model,
        "video_files_ready": not missing_video,
        "sample_ready": not missing_model and (bundle / "example_features.npz").is_file(),
        "missing": missing_video,
        "dataset": manifest.get("dataset", "UCF"),
        "classes": manifest.get("classes", []),
        "seen_count": manifest.get("seen_count", 0),
        "unseen_count": manifest.get("unseen_count", 0),
        "upstream_commit": UPSTREAM_COMMIT,
        "preprocess_profile": config["preprocess_profile"],
        "confidence_kind": "relative_softmax_uncalibrated",
        "temperature": float(config["temperature"]),
        "note": "文件就绪不等于完整视频链路已验证；请参阅验证报告。"
    }
