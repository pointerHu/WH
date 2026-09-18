"""Prepare a local-only public AV test sample from an official source archive."""
import argparse
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import ROOT, load_config, sha256, write_json

COMMIT = 'a5a167dff2399e2d182a60332325f9c0d4663517'
SAMPLE_SHA256 = 'cc3ebb11e80d2900071ff929633b7476a33ee1698ac9a91206e2ba64c1c28920'
SOURCE = 'https://github.com/open-mmlab/mmaction2/blob/' + COMMIT + '/tests/data/test.avi'


def prepare(archive):
    output = ROOT / 'runtime/public-samples'
    output.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as source:
        if source.comment.decode() != COMMIT:
            raise ValueError('Wrong MMAction2 commit; use the pinned official archive.')
        names = [n for n in source.namelist() if n.endswith('/tests/data/test.avi')]
        if len(names) != 1 or source.getinfo(names[0]).file_size > 10 * 1024 * 1024:
            raise ValueError('Unexpected archive contents')
        content = source.read(names[0])
    if hashlib.sha256(content).hexdigest() != SAMPLE_SHA256:
        raise ValueError('Sample SHA256 mismatch')
    original = output / 'real-av-source.avi'
    original.write_bytes(content)
    browser_video = output / 'real-av-demo.mp4'
    config = load_config()
    subprocess.run([config['ffmpeg'], '-nostdin', '-v', 'error', '-y', '-i', str(original),
                    '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                    '-movflags', '+faststart', str(browser_video)], check=True, timeout=60)
    report = dict(source_url=SOURCE, source_commit=COMMIT, source_sha256=SAMPLE_SHA256,
                  source_bytes=len(content), browser_copy_sha256=sha256(browser_video),
                  browser_copy_bytes=browser_video.stat().st_size,
                  transformation='H.264 CRF18 + AAC MP4; encoded bytes/features may differ',
                  sample_purpose='Raw-video pipeline verification, NOT an accuracy benchmark',
                  redistribution='Video bytes remain local; only provenance and result JSON are published')
    write_json(ROOT / 'artifacts/public_sample_provenance.json', report)
    print('Local browser-compatible test video:', browser_video)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True,
                        help='Official codeload archive for commit ' + COMMIT)
    prepare(parser.parse_args().archive)
