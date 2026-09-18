"""Fit one temperature on an independent labelled calibration split (not test).
Input NPZ: logits [N,C], labels [N] are column indices, not arbitrary class IDs.
This writes a proposal/report only: it never silently changes the web configuration.
Validate transfer to the final stage-B model and domain before describing it as calibrated.
"""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--split-name", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if "test" in args.split_name.lower():
        raise ValueError("Do not use the final test split for calibration")
    import numpy as np
    from scipy.optimize import minimize_scalar
    from scipy.special import logsumexp
    with np.load(str(args.input), allow_pickle=False) as data:
        logits = np.asarray(data["logits"], dtype=np.float64)
        labels = np.asarray(data["labels"], dtype=np.int64)
    if logits.ndim != 2 or labels.shape != (logits.shape[0],) or len(labels) < 10:
        raise ValueError("Need [N,C] logits and N labels, with N >= 10")
    if not np.isfinite(logits).all() or labels.min() < 0 or labels.max() >= logits.shape[1]:
        raise ValueError("Invalid logits or label indices")
    def nll(log_temperature):
        scaled = logits / np.exp(log_temperature)
        return float(np.mean(logsumexp(scaled, axis=1) - scaled[np.arange(len(labels)), labels]))
    fitted = minimize_scalar(nll, bounds=(-5, 4), method="bounded")
    report = {"temperature": float(np.exp(fitted.x)), "split_name": args.split_name,
              "sample_count": len(labels), "nll_before": nll(0), "nll_after": float(fitted.fun),
              "status": "fitted_on_supplied_calibration_split; independent holdout validation still required",
              "changes_model_argmax": False, "web_configuration_changed": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
