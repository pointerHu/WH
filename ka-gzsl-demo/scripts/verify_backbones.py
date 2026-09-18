"""Run the real, administrator-installed encoder weights; no random fallback."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import time
import numpy as np
import torch
from runtime import ROOT, load_config, write_json
from media import decode_media
from model_adapter import VideoBackbones

if __name__ == '__main__':
    torch.set_num_threads(4)
    config = load_config()
    job = ROOT / 'runtime' / 'backbone-verification'
    job.mkdir(parents=True, exist_ok=True)
    sample = ROOT / 'runtime/media-verification/synthetic-av.mp4'
    image, waveform, metadata = decode_media(sample, job, config)
    start = time.monotonic()
    model = VideoBackbones(config)
    audio, video = model.encode(image, waveform)
    assert np.isfinite(audio).all() and np.isfinite(video).all()
    assert abs(float(np.linalg.norm(audio)) - 1.0) < 0.002
    assert abs(float(np.linalg.norm(video)) - 1.0) < 0.002
    report = dict(test_input='synthetic_av_plumbing_only_not_accuracy', passed=True,
                  audio_shape=list(audio.shape), video_shape=list(video.shape),
                  audio_norm=float(np.linalg.norm(audio)), video_norm=float(np.linalg.norm(video)),
                  audio_finite=bool(np.isfinite(audio).all()), video_finite=bool(np.isfinite(video).all()),
                  clip_sha256=model.clip_sha256, wavcaps_sha256=model.wavcaps_sha256,
                  elapsed_seconds=time.monotonic()-start, metadata=metadata)
    write_json(ROOT / 'artifacts/backbone_verification.json', report)
    print(report, flush=True)
