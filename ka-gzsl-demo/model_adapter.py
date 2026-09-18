"""Thin adapters around the pinned KA-GZSL and WavCaps implementations."""
from __future__ import annotations
import copy
import sys
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from runtime import read_json, sha256


def add_upstream(path):
    path = Path(path).resolve()
    if not (path / "src/clipclap_model.py").is_file():
        raise FileNotFoundError("Missing pinned KA-GZSL source snapshot")
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


def trusted_torch_load(path):
    # Only load administrator-installed local model files; never user-uploaded .pt.
    # PyTorch 1.7 has no weights_only argument. See docs/security.md.
    return torch.load(str(path), map_location="cpu")


class KAClassifier:
    def __init__(self, config):
        add_upstream(config["ka_repo"])
        from src.clipclap_model import ClipClap_model
        folder = Path(config["bundle_dir"])
        self.manifest = read_json(folder / "manifest.json")
        for name, expected in self.manifest["sha256"].items():
            if sha256(folder / name) != expected:
                raise ValueError("Model bundle checksum mismatch: " + name)
        code_hash = self.manifest.get("model_source_sha256")
        if code_hash and sha256(Path(config["ka_repo"]) / "src/clipclap_model.py") != code_hash:
            raise ValueError("Model source differs from exported checkpoint's source")
        self.device = torch.device(config["device"])
        if self.device.type == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA 不可用，请检查 WSL GPU 或将 device 显式设为 cpu。")
        self.model = ClipClap_model(self.manifest["model_params"],
                                   self.manifest["input_size_audio"], self.manifest["input_size_video"])
        checkpoint = trusted_torch_load(folder / "model.pt")
        self.model.load_state_dict(checkpoint["model"], strict=True)
        self.model.to(self.device).eval()
        for parameter in self.model.parameters():
            parameter.requires_grad_(False)
        with np.load(str(folder / "class_bank.npz"), allow_pickle=False) as bank:
            self.class_ids = bank["class_ids"].astype(np.int64)
            self.seen = bank["seen"].astype(bool)
            self.text = torch.as_tensor(bank["text"], dtype=torch.float32, device=self.device)
        self.classes = self.manifest["classes"]
        if self.text.shape != (len(self.classes), 1536):
            raise ValueError("Expected a matching [classes, 1536] CLIP+WavCaps text bank")
        self.beta = float(self.manifest["seen_bias"]["value"])
        self.temperature = float(config["temperature"])

    def predict(self, audio, video, mode="gzsl"):
        if mode not in ("gzsl", "zsl"):
            raise ValueError("Unsupported classification mode")
        audio = torch.as_tensor(audio, dtype=torch.float32, device=self.device).reshape(1, -1)
        video = torch.as_tensor(video, dtype=torch.float32, device=self.device).reshape(1, -1)
        if audio.shape[1] != 1024 or video.shape[1] != 512:
            raise ValueError("KA-GZSL expects 1024-D audio and 512-D video features")
        if not torch.isfinite(audio).all() or not torch.isfinite(video).all():
            raise ValueError("Non-finite input features")
        with torch.no_grad():
            _, latent, prototypes = self.model.get_embeddings(audio, video, self.text, None, None)
            distances = torch.cdist(latent.float(), prototypes.float())[0]
            if self.manifest.get("distance_fn") == "SquaredL2Loss":
                distances = distances.pow(2)
            selected = np.ones(len(self.classes), dtype=bool) if mode == "gzsl" else ~self.seen
            positions = np.flatnonzero(selected)
            if positions.size < 1:
                raise ValueError("No candidate classes in the requested mode")
            penalty = torch.as_tensor(self.seen.astype(np.float32), device=self.device) * self.beta
            logits = -(distances + penalty)
            logits = logits[torch.as_tensor(positions, dtype=torch.long, device=self.device)]
            probabilities = torch.softmax(logits / self.temperature, dim=0).cpu().numpy()
            distances = distances.cpu().numpy()[positions]
        if not np.isfinite(probabilities).all():
            raise ValueError("Non-finite prediction scores")
        ranked = np.argsort(-probabilities, kind="stable")
        predictions = [{"class_id": int(self.class_ids[positions[i]]),
                        "label": self.classes[positions[i]], "seen": bool(self.seen[positions[i]]),
                        "confidence": float(probabilities[i]), "distance": float(distances[i])}
                       for i in ranked[:5]]
        result = {"prediction": predictions[0], "top5": predictions,
                  "candidate_count": int(len(positions)), "mode": mode,
                  "remaining_probability": max(0.0, 1.0 - sum(x["confidence"] for x in predictions)),
                  "confidence_kind": "relative_softmax_uncalibrated",
                  "temperature": self.temperature, "seen_bias": self.beta,
                  "seen_bias_source": self.manifest["seen_bias"]["source"],
                  "latent_dimension": int(latent.shape[-1]), "dataset": self.manifest["dataset"],
                  "checkpoint_sha256": self.manifest["sha256"]["model.pt"]}
        return result, logits.cpu().numpy(), self.class_ids[positions]


class VideoBackbones:
    def __init__(self, config):
        import clip
        import yaml
        add_upstream(config["ka_repo"])
        from WavCaps.retrieval.models.audio_encoder import AudioEncoder
        self.device = torch.device(config["device"])
        if not Path(config["clip_weights"]).is_file() or not Path(config["wavcaps_weights"]).is_file():
            raise FileNotFoundError("需要同款 CLIP 与 WavCaps 权重；不会替换成随机权重或其他 CLAP。")
        self.clip, self.preprocess = clip.load(config["clip_weights"], device=self.device, jit=False)
        with (Path(config["ka_repo"]) / "WavCaps/retrieval/settings/inference.yaml").open() as f:
            wav_config = yaml.safe_load(f)
        wav_config = copy.deepcopy(wav_config)
        # The full ASE checkpoint contains this encoder; loading HTSAT.ckpt first
        # would be redundant and triggers a hard-coded author path in upstream.
        wav_config["audio_encoder_args"]["pretrained"] = False
        class AudioOnlyASE(nn.Module):
            def __init__(self):
                super().__init__()
                self.audio_encoder = AudioEncoder(wav_config)
                dim = int(wav_config["embed_size"])
                self.audio_proj = nn.Sequential(nn.Linear(self.audio_encoder.audio_width, dim),
                                                nn.ReLU(), nn.Linear(dim, dim))
            def forward(self, waveform):
                return F.normalize(self.audio_proj(self.audio_encoder(waveform)), dim=-1)
        self.audio = AudioOnlyASE()
        loaded = trusted_torch_load(config["wavcaps_weights"])
        if not isinstance(loaded, dict) or "model" not in loaded:
            raise ValueError("Expected WavCaps HTSAT_BERT_zero_shot.pt with a 'model' state dict")
        selected = {k: v for k, v in loaded["model"].items()
                    if k.startswith("audio_encoder.") or k.startswith("audio_proj.")}
        self.audio.load_state_dict(selected, strict=True)
        self.audio.to(self.device).eval()
        self.clip.eval()
        self.clip_sha256 = sha256(config["clip_weights"])
        self.wavcaps_sha256 = sha256(config["wavcaps_weights"])

    def encode(self, image, waveform):
        with torch.no_grad():
            visual = self.clip.encode_image(self.preprocess(image).unsqueeze(0).to(self.device))
            visual = F.normalize(visual, dim=-1).float()
            audio = self.audio(waveform.to(self.device)).float()
        if tuple(visual.shape) != (1, 512) or tuple(audio.shape) != (1, 1024):
            raise ValueError("Backbone output dimensions do not match this KA-GZSL checkpoint")
        return audio.cpu().numpy(), visual.cpu().numpy()
