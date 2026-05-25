#!/usr/bin/env bash
set -euo pipefail

robot \
    --outputdir=${OUTPUT_DIR}/robot \
    --loglevel=TRACE \
    . 