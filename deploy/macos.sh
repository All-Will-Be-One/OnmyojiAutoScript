#!/bin/bash
set -eo pipefail
cd "$(dirname "$0")/.."
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
export PYTHONUTF8=1
case "${1:-check}" in
  install)
    uv venv --python 3.10 .venv
    uv pip install --python .venv/bin/python -r requirements.txt
    ;;
  serve)
    shift
    exec .venv/bin/python server.py --host 127.0.0.1 --port 22267 "$@"
    ;;
  check)
    shift || true
    exec .venv/bin/python -m deploy.macos_check "${@}"
    ;;
  python)
    shift
    exec .venv/bin/python "$@"
    ;;
  *) echo 'Usage: macos.sh {install|serve|check [config]|python ...}' >&2; exit 2 ;;
esac
