"""Export the matching stage-B checkpoint, class bank and validation-only bias.
Run in the model environment. Only trusted local training files are accepted.
"""
import argparse
import inspect
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import ROOT, UPSTREAM_COMMIT, load_config, sha256, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage-a", type=Path, required=True)
    parser.add_argument("--stage-b", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "assets/ucf")
    args = parser.parse_args()
    import numpy as np
    import torch
    import yaml
    from types import SimpleNamespace
    config = load_config()
    sys.path.insert(0, config["ka_repo"])
    from src.dataset import UCFDataset
    from src.utils_improvements import get_model_params
    with (args.stage_b / "args.yaml").open() as handle:
        training = yaml.safe_load(handle)
    if training["dataset_name"] != "UCF" or not training["retrain_all"]:
        raise ValueError("Initial demonstrator requires a fully trained UCF stage-B run")
    if training["modality"] != "both" or training["word_embeddings"] != "both":
        raise ValueError("Expected dual audio/video and CLIP+WavCaps text model")
    if training.get("z_score_inputs") or training.get("norm_inputs"):
        raise ValueError("This adapter does not silently change input normalization")
    a_weights = args.stage_a / ("ClipClap_model_" + training["best_model_criterion"] + ".pt")
    first = torch.load(str(a_weights), map_location="cpu")
    epoch = int(first["epoch"])
    del first
    b_weights = args.stage_b / "checkpoints" / ("ClipClap_model_%s_ckpt_%d.pt" % (training["best_model_criterion"], epoch - 1))
    weights = torch.load(str(b_weights), map_location="cpu")
    if int(weights["epoch"]) != epoch:
        raise ValueError("Stage A/B epochs do not match")
    log = (args.stage_b / "eval.log").read_text()
    match = re.search(r"Validation betas:\s*Audio=([0-9.eE+-]+)\s+Video=([0-9.eE+-]+)", log)
    if not match:
        raise ValueError("Cannot find validation-selected beta; refusing to fit on test labels")
    beta = float(match.group(2))
    aliases = {"dropout_encoder": "embedding_dropout", "dropout_decoder": "decoder_dropout",
               "encoder_hidden_size": "embeddings_hidden_size"}
    params = get_model_params(**{key: training[aliases.get(key, key)] for key in inspect.signature(get_model_params).parameters})
    training["root_dir"] = args.data_root.resolve()
    training["device"] = "cpu"
    training["feature_extraction_method"] = Path(training["feature_extraction_method"])
    dataset = UCFDataset(args=SimpleNamespace(**training), dataset_split="test", zero_shot_mode=None)
    all_data = dataset.all_data
    class_ids = np.asarray(dataset.classes, dtype=np.int64)
    seen = np.isin(class_ids, dataset.seen_class_ids)
    labels = [str(dataset.all_class_names[int(i)]) for i in class_ids]
    text = np.asarray(all_data["text"], dtype=np.float32)
    if text.shape != (len(labels), 1536):
        raise ValueError("Unexpected class text dimensions: " + str(text.shape))
    output = args.output.resolve()
    if (output / "manifest.json").exists():
        raise FileExistsError("Bundle already exists; use a new --output directory")
    output.mkdir(parents=True, exist_ok=True)
    torch.save({"model": {k: v.detach().cpu() for k, v in weights["model"].items()}, "epoch": epoch}, str(output / "model.pt"))
    np.savez_compressed(str(output / "class_bank.npz"), class_ids=class_ids, seen=seen, text=text)
    # Deterministic first sample: no cherry-picking and no calibration on its label.
    np.savez_compressed(str(output / "example_features.npz"), audio=np.asarray(all_data["audio"][0], dtype=np.float32),
                        video=np.asarray(all_data["video"][0], dtype=np.float32), target=np.int64(all_data["target"][0]))
    manifest = {"schema": 1, "dataset": "UCF", "upstream_commit": UPSTREAM_COMMIT,
                "model_source_sha256": sha256(Path(config["ka_repo"]) / "src/clipclap_model.py"),
                "model_params": params, "input_size_audio": training["input_size_audio"],
                "input_size_video": training["input_size_video"],
                "actual_feature_dimensions": {"audio": 1024, "video": 512, "text": 1536},
                "distance_fn": training["distance_fn"], "stage_b_epoch": epoch,
                "stage_a_checkpoint_sha256": sha256(a_weights), "stage_b_checkpoint_sha256": sha256(b_weights),
                "classes": labels, "class_ids": class_ids.tolist(), "seen_mask": seen.tolist(),
                "seen_count": int(seen.sum()), "unseen_count": int((~seen).sum()),
                "seen_bias": {"value": beta, "source": "stage_A_validation_log; NOT fitted on test labels"},
                "confidence_calibrated": False, "example_source": "first UCF test feature; only functional verification",
                "sha256": {name: sha256(output / name) for name in ("model.pt", "class_bank.npz", "example_features.npz")}}
    write_json(output / "manifest.json", manifest)
    write_json(ROOT / "artifacts/export_manifest.json", manifest)
    print("EXPORT_OK", len(labels), "classes", epoch, "stage-B epochs", "beta", beta)
    print("MODEL_MB", (output / "model.pt").stat().st_size / 1024 / 1024)


if __name__ == "__main__":
    main()
