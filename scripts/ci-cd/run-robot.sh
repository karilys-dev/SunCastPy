#!/usr/bin/env bash
set -euo pipefail

install(){
  if command -v robot &> /dev/null; then
      robot --version || true
      echo "Success: robot is installed and ready."
  else
      echo "Installing: robot-framework."
      DIR="$( realpath $(dirname "${BASH_SOURCE[0]}")/../../ )"
      pip install ${DIR}/SunCastPy[test-robot]
  fi
}

run(){
  ARTIFACTS=${OUTPUT_DIR}/robot
  if [ -d "${ARTIFACTS}" ]; then
    rm -rf ${ARTIFACTS}
  fi


  robot \
      --outputdir=${ARTIFACTS} \
      --loglevel=TRACE \
      --xunit=xunit.xml \
      . 
}


usage() {
    echo "Usage: $(basename "$0") [-h help] [-r robot] [-i install]" >&2
}

while getopts ":irh" opt; do
    case $opt in
        i) install ;;
        r) run ;;
        h) usage ;;
        \?)
          echo "Invalid option: -$OPTARG" >&2
          exit 1
          ;;
    esac
done
shift $((OPTIND - 1))
