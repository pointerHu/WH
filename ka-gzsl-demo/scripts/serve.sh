#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
exec .venv-web/bin/python -m uvicorn webapp:app --host 127.0.0.1 --port 8765 --workers 1
