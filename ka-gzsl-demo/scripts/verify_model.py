"""Validate exported model inference against original model code on real features."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import ROOT, load_config, write_json


def main():
    import numpy as np
    import torch
    from model_adapter import KAClassifier
    config = load_config()
    classifier = KAClassifier(config)
    with np.load(str(Path(config["bundle_dir"]) / "example_features.npz"), allow_pickle=False) as data:
        audio, video, target = data["audio"], data["video"], int(data["target"].item())
    result, logits, class_ids = classifier.predict(audio, video, "gzsl")
    with torch.no_grad():
        a = torch.as_tensor(audio, dtype=torch.float32, device=classifier.device).reshape(1, -1)
        v = torch.as_tensor(video, dtype=torch.float32, device=classifier.device).reshape(1, -1)
        _, visual_latent, text_latent = classifier.model.get_embeddings(a, v, classifier.text, None, None)
        distances = torch.cdist(visual_latent.float(), text_latent.float())[0]
        direct = -(distances + torch.as_tensor(classifier.seen.astype(np.float32), device=classifier.device) * classifier.beta)
        reference = direct.cpu().numpy()
    delta = float(np.max(np.abs(reference - logits)))
    assert delta <= 1e-5, delta
    assert np.isfinite(logits).all()
    assert result["prediction"]["class_id"] == int(class_ids[np.argmax(reference)])
    zsl_result, zsl_logits, zsl_ids = classifier.predict(audio, video, "zsl")
    assert all(not p["seen"] for p in zsl_result["top5"])
    assert len(zsl_ids) == classifier.manifest["unseen_count"]
    # Reject dimensions that would otherwise hide an incompatible audio encoder.
    rejected = False
    try:
        classifier.predict(np.zeros(512, dtype=np.float32), video)
    except ValueError:
        rejected = True
    assert rejected
    report = {"status": "passed", "test_kind": "real_feature_classifier_adapter_not_raw_video",
              "max_absolute_logit_difference": delta,
              "reference_class_id": target, "prediction": result["prediction"],
              "candidate_count": len(class_ids), "zsl_candidate_count": len(zsl_ids),
              "wrong_audio_dimension_rejected": rejected, "checkpoint_sha256": result["checkpoint_sha256"],
              "probability_calibrated": False, "raw_video_end_to_end_verified": False}
    write_json(ROOT / "artifacts/model_verification.json", report)
    write_json(ROOT / "artifacts/feature_example_result.json", result)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
