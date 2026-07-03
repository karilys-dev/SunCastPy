#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="$( realpath $(dirname "${BASH_SOURCE[0]}") )"
DIR="$( realpath $(dirname "${BASH_SOURCE[0]}")/../../ )"

install(){
  if command -v semgrep &> /dev/null; then
      semgrep --version || true
      echo "Success: semgrep is installed and ready."
  else
      echo "Installing: semgrep."
      pip install ${DIR}/SunCastPy[scan]
  fi
}

run(){
  ARTIFACTS=${OUTPUT_DIR}/semgrep
  if [ -d "${ARTIFACTS}" ]; then
    rm -rf ${ARTIFACTS}
  fi

  semgrep scan \
    --config=auto \
    --error \
    --matching-explanations \
    --output=${ARTIFACTS}/report.json --json \
    --junit-xml-output=${ARTIFACTS}/result.xml \
    ${DIR}/SunCastPy
    # --exclude-rule=python.flask.security.xss.audit.direct-use-of-jinja2.direct-use-of-jinja2 \
}

usage() {
    echo "Usage: $(basename "$0") [-h help] [-r run] [-i install]" >&2
}

while getopts ":irh" opt; do
    case $opt in
        i) install ;;
        r) run ;;
        h) usage ;;
        *)
          echo "Error: Option -$OPTARG requires an argument." >&2
          exit 1
          ;;
        \?)
          echo "Error: Unknown option -$OPTARG." >&2
          exit 1
          ;;
    esac
done
shift $((OPTIND - 1))
