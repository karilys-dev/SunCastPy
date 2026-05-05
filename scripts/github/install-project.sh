#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip

DIR="$( realpath $(dirname "${BASH_SOURCE[0]}")/../../ )"

pip install ${DIR}/SunCastPy${1:-}