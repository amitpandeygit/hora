#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
exec .venv/bin/uvicorn hora.api.main:app --reload --port "${PORT:-8000}"
