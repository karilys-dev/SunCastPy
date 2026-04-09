#!/usr/bin/env bash
set -e

echo 'export PATH=$HOME/.venv/bin:$HOME/.local/bin:$PATH' >> ~/.bashrc

python -m venv "$HOME/.venv"

"$HOME/.venv/bin/pip" install --upgrade pip
"$HOME/.venv/bin/pip" install -e SunCastPy[tests,dev]