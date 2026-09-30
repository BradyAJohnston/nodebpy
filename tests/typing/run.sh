#!/usr/bin/env bash
# Type-check nodebpy the way a downstream user sees it: build the wheel,
# install it into a clean venv and check consumer.py with every major checker.
# Runs from a temp dir so no checker can resolve `nodebpy` from the repo's src/.
set -uo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

uv build --wheel --out-dir "$work/dist" "$repo" -q || exit 1
cp "$here/consumer.py" "$here/pyproject.toml" "$work/"
cd "$work"
uv venv -q -p 3.13 .venv || exit 1
uv pip install -q -p .venv/bin/python "$work"/dist/*.whl -r "$here/requirements.txt" || exit 1
# pyright --verifytypes only finds the package through an active venv.
source "$work/.venv/bin/activate"
py="$work/.venv/bin/python"
bin="$work/.venv/bin"

failed=()
check() {
    local name="$1"
    shift
    echo "=== $name"
    if ! "$@"; then
        failed+=("$name")
    fi
}

check mypy "$bin/mypy" --strict --python-executable "$py" consumer.py
check pyright "$bin/pyright" --pythonpath "$py" consumer.py
check basedpyright "$bin/basedpyright" --pythonpath "$py" consumer.py
check pyrefly "$bin/pyrefly" check --python-interpreter-path "$py" consumer.py
check ty "$bin/ty" check --python "$work/.venv" consumer.py
check "pyright --verifytypes" "$bin/pyright" --pythonpath "$py" \
    --verifytypes nodebpy --ignoreexternal

if ((${#failed[@]})); then
    echo "FAILED: ${failed[*]}"
    exit 1
fi
echo "All type checkers passed."
