#!/usr/bin/env bash
set -euo pipefail

echo "Creating html report"

forecast \
    --group-by date \
    --output ${OUTPUT_DIR} \
    --zone="${ZONE}" \
    ${LIMIT:+--limit $LIMIT} \
