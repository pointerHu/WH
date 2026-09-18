"""Download only the official CLIP checkpoint, with its official SHA256 check."""
import argparse
import shutil
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import load_config, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wavcaps-local", type=Path, help="Optional trusted matching WavCaps checkpoint already downloaded by the user")
    args = parser.parse_args()
    import clip.clip as clip_impl
    config = load_config()
    output = Path(config["clip_weights"])
    output.parent.mkdir(parents=True, exist_ok=True)
    url = clip_impl._MODELS["ViT-B/32"]
    expected = url.split("/")[-2]
    downloaded = Path(clip_impl._download(url, str(output.parent)))
    if downloaded != output:
        shutil.copy2(downloaded, output)
    if sha256(output) != expected:
        raise ValueError("Official CLIP checksum mismatch")
    print("CLIP_READY", output, expected)
    if args.wavcaps_local:
        source = args.wavcaps_local.resolve()
        if not source.is_file():
            raise FileNotFoundError(str(source))
        destination = Path(config["wavcaps_weights"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source != destination.resolve():
            shutil.copy2(source, destination)
        print("WAVCAPS_INSTALLED", destination, sha256(destination))
        print("Strict audio-encoder key/shape validation happens when inference loads the checkpoint.")
    else:
        print("WavCaps must be the matching HTSAT_BERT_zero_shot.pt from the official project.")
        print("No substitute CLAP checkpoint is automatically downloaded.")


if __name__ == "__main__":
    main()
