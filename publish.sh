#!/usr/bin/env bash
# Rebuild the blog indexes from posts-data.json and publish to GitHub Pages.
# Usage: ./publish.sh
#        ./publish.sh 2026-11-12
#        ./publish.sh --no-push
#        ./publish.sh 2026-11-12 --no-push
set -euo pipefail

cd "$(dirname "$0")"

NO_PUSH=0
DATE=""
for arg in "$@"; do
  case "$arg" in
    --no-push) NO_PUSH=1 ;;
    *)
      if [[ -n "$DATE" ]]; then
        echo "Unexpected argument: $arg" >&2
        exit 1
      fi
      DATE="$arg"
      ;;
  esac
done

if [[ -z "$DATE" ]]; then
  DATE="$(date +%Y-%m-%d)"
fi

if ! [[ "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "Date must be YYYY-MM-DD, got: $DATE" >&2
  exit 1
fi

python3 scripts/generate.py

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "This folder is not a git repository yet." >&2
  exit 1
fi

git add -A

if git diff --cached --quiet; then
  echo "No changes to publish for $DATE."
  exit 0
fi

git commit -m "Daily posts $DATE"

if [[ "$NO_PUSH" -eq 1 ]]; then
  echo "Committed locally as 'Daily posts $DATE'. Skipped push (--no-push)."
  exit 0
fi

git push origin main
echo "Published 'Daily posts $DATE' to origin/main."
