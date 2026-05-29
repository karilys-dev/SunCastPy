#!/usr/bin/env bash
set -euo pipefail

ARTIFACTS=${OUTPUT_DIR}/robot
if [ -d "${ARTIFACTS}" ]; then
  rm -rf ${ARTIFACTS}
fi

robot \
    --outputdir=${ARTIFACTS} \
    --loglevel=TRACE \
    . 