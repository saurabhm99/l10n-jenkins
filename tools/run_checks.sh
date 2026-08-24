#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v python >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
  echo "python not found on PATH" >&2
  exit 127
fi
PYTHON=$(command -v python3 || command -v python)

mkdir -p reports

"$PYTHON" -c 'import json; print("en.json keys:", len(json.load(open("locales/en.json", encoding="utf-8"))))'
echo "locale files: $(ls locales/*.json | wc -l)"

set +e
\\"$PYTHON" tools/check_locales.py | tee reports/locale-report.txt
"$PYTHON" tools/check_locales.py "$@" | tee reports/locale-report.txt
status=${PIPESTATUS[0]}
set -e
exit "$status"