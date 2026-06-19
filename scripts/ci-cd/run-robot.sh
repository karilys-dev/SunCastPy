#!/usr/bin/env bash
set -euo pipefail

ARTIFACTS=${OUTPUT_DIR}/robot
if [ -d "${ARTIFACTS}" ]; then
  rm -rf ${ARTIFACTS}
fi

if command -v robot &> /dev/null; then
    echo "Success: robot is installed and ready."
else
    echo "Installing: robot-framework."
    DIR="$( realpath $(dirname "${BASH_SOURCE[0]}")/../../ )"
    pip install ${DIR}/SunCastPy[test-robot]
fi

robot \
    --outputdir=${ARTIFACTS} \
    --loglevel=TRACE \
    . 