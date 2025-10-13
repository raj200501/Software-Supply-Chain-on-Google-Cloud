#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "usage: $0 --bucket <bucket> --prefix <prefix> --path <path>" >&2
  exit 1
fi

BUCKET=""
PREFIX=""
PATH_TO_ARTIFACTS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bucket)
      BUCKET="$2"
      shift 2
      ;;
    --prefix)
      PREFIX="$2"
      shift 2
      ;;
    --path)
      PATH_TO_ARTIFACTS="$2"
      shift 2
      ;;
    *)
      echo "unknown flag $1" >&2
      exit 1
      ;;
  esac
done

if [[ ! -d "${PATH_TO_ARTIFACTS}" ]]; then
  echo "path ${PATH_TO_ARTIFACTS} does not exist" >&2
  exit 1
fi

gsutil -m cp -r "${PATH_TO_ARTIFACTS}" "gs://${BUCKET}/${PREFIX}/"
