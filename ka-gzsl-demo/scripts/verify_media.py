"""Synthetic media tests cover decoding only; not classification accuracy."""
import json, sys, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import ROOT, load_config, sha256, write_json
from media import decode_media, inspect_video, MediaError
import numpy as np
import torch
config = load_config()
folder = ROOT / 'runtime/media-verification'
folder.mkdir(parents=True, exist_ok=True)
video = folder / 'synthetic-av.mp4'
command = [config['ffmpeg'], '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc=size=320x240:rate=10', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=44100', '-t', '2', '-c:v', 'mpeg4', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', str(video)]
subprocess.run(command, check=True, timeout=30)
image, waveform, metadata = decode_media(video, folder, config)
assert tuple(waveform.shape) == (1, 320000)
assert torch.isfinite(waveform).all()
assert image.size == (320, 240)
no_audio = folder / 'no-audio.mp4'
subprocess.run([config['ffmpeg'], '-nostdin', '-v', 'error', '-y', '-i', str(video), '-an', '-c:v', 'copy', str(no_audio)], check=True, timeout=20)
rejected = False
try:
    inspect_video(no_audio, config)
except MediaError:
    rejected = True
assert rejected
report = {'preprocessing': 'passed', 'input': 'synthetic test pattern + 440Hz tone', 'audio_shape': list(waveform.shape), 'image_size': list(image.size), 'missing_audio_rejected': rejected, 'metadata': metadata, 'raw_video_classification_verified': False}
clip_path = Path(config['clip_weights'])
if clip_path.exists():
    import clip
    expected = '40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af'
    assert sha256(clip_path) == expected, 'CLIP checkpoint incomplete or checksum mismatch'
    model, preprocess = clip.load(str(clip_path), device=config['device'], jit=False)
    model.eval()
    with torch.no_grad():
        feature = model.encode_image(preprocess(image).unsqueeze(0).to(config['device']))
        feature = torch.nn.functional.normalize(feature, dim=-1)
    assert tuple(feature.shape) == (1, 512) and torch.isfinite(feature).all()
    report.update({'clip_forward': 'passed', 'clip_shape': list(feature.shape), 'clip_sha256': expected, 'clip_norm': float(feature.norm().cpu())})
else:
    report['clip_forward'] = 'not_run_missing_checkpoint'
write_json(ROOT / 'artifacts/media_verification.json', report)
print(json.dumps(report, ensure_ascii=False, indent=2))
