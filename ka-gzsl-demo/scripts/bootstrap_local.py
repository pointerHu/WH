"""Create project-local environments and a read-only snapshot of existing code.
Run with system Python >=3.10. Does not install into the original environment.
"""
import argparse
import json
import subprocess
import sys
import tarfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import ROOT, UPSTREAM_COMMIT, read_json, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--python38", type=Path, required=True)
    parser.add_argument("--legacy-site-packages", type=Path, required=True)
    parser.add_argument("--ffmpeg-bin", type=Path, required=True)
    args = parser.parse_args()
    for path in (args.source_repo / "src/clipclap_model.py", args.python38,
                 args.ffmpeg_bin / "ffmpeg", args.ffmpeg_bin / "ffprobe"):
        if not path.is_file():
            raise FileNotFoundError(str(path))
    destination = ROOT / ".vendor/KA-GZSL"
    if not destination.exists():
        destination.mkdir(parents=True)
        archive = ROOT / ".vendor/upstream-source.tar"
        with archive.open("wb") as handle:
            subprocess.run(["git", "-C", str(args.source_repo), "archive", "HEAD", "src", "WavCaps",
                            "config", "clip_feature_extraction", "clip_embeddings_extraction", "LICENSE", "README.md"],
                           stdout=handle, check=True)
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                if member.issym() or member.islnk() or not (member.isfile() or member.isdir()):
                    raise ValueError("Unsupported archive member")
                target = (destination / member.name).resolve()
                if destination.resolve() not in target.parents:
                    raise ValueError("Unsafe archive path")
            tar.extractall(destination)
        archive.unlink()
    web_python = ROOT / ".venv-web/bin/python"
    if not web_python.exists():
        subprocess.run([sys.executable, "-m", "venv", str(ROOT / ".venv-web")], check=True)
    model_python = ROOT / ".venv-model/bin/python"
    if not model_python.exists():
        subprocess.run([str(args.python38), "-m", "venv", "--system-site-packages", str(ROOT / ".venv-model")], check=True)
    site = ROOT / ".venv-model/lib/python3.8/site-packages"
    site.mkdir(parents=True, exist_ok=True)
    (site / "legacy_training_dependencies.pth").write_text(str(args.legacy_site_packages.resolve()) + "\n")
    local = read_json(ROOT / "config.example.json")
    local.update({"ffmpeg": str(args.ffmpeg_bin / "ffmpeg"), "ffprobe": str(args.ffmpeg_bin / "ffprobe")})
    if not (ROOT / "config.local.json").exists():
        write_json(ROOT / "config.local.json", local)
    write_json(ROOT / "assets/bootstrap_provenance.json", {
        "expected_upstream_commit": UPSTREAM_COMMIT,
        "source_snapshot_head": subprocess.check_output(["git", "-C", str(args.source_repo), "rev-parse", "HEAD"], text=True).strip(),
        "environment_strategy": "isolated Python 3.8 venv with read-only inherited training packages",
        "source_repository_modified": False})
    print("BOOTSTRAP_OK", ROOT)
    print("Next: .venv-web/bin/python -m pip install -r requirements-web.txt")
    print("Next: .venv-model/bin/python -m pip install -r requirements-model-extra.txt")


if __name__ == "__main__":
    main()
