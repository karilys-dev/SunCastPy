#!/usr/bin/env bash
set -eEuo pipefail

SCRIPTS_DIR="$( realpath $(dirname "${BASH_SOURCE[0]}") )/ci-cd"
echo "export PATH=${SCRIPTS_DIR}:"'$HOME/.venv/bin:$HOME/.local/bin:$PATH' >> ~/.bashrc

python -m venv "$HOME/.venv"

"$HOME/.venv/bin/pip" install --upgrade pip
"$HOME/.venv/bin/pip" install -e SunCastPy[tests,dev]

git config --global user.email ${USER_EMAIL}
git config --global user.name ${USER_NAME}

$HOME/.venv/bin/pre-commit install