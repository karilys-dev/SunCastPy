#!/usr/bin/env bash
set -euo pipefail

echo "Creating html report"

forecast \
    --group-by date \
    --output ${OUTPUT_DIR} \
    ${LATITUDE:+--latitude ${LATITUDE}} \
    ${LONGITUDE:+--longitude ${LONGITUDE}} \
    ${LIMIT:+--limit $LIMIT} \
