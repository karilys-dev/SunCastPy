#!/usr/bin/env bash
set -eEuo pipefail

echo 'export PATH=$HOME/.venv/bin:$HOME/.local/bin:$PATH' >> ~/.bashrc

python -m venv "$HOME/.venv"

"$HOME/.venv/bin/pip" install --upgrade pip
"$HOME/.venv/bin/pip" install -e SunCastPy[tests,dev,test-black]

git config --global user.email ${USER_EMAIL}
git config --global user.name ${USER_NAME}

$HOME/.venv/bin/pre-commit install