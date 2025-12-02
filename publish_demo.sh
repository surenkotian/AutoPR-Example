#!/usr/bin/env bash
# Publish demo/demo-repo-ready to a new GitHub repository
# Usage: ./publish_demo.sh <remote-git-url> [branch]
# Example: ./publish_demo.sh git@github.com:your-user/autopr-demo.git main

set -euo pipefail
REMOTE=${1:-}
BRANCH=${2:-main}

if [ -z "$REMOTE" ]; then
  echo "Usage: $0 <remote-git-url> [branch]" >&2
  exit 2
fi

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
echo "Publishing demo repo from $ROOT_DIR to $REMOTE (branch $BRANCH)"

cd "$ROOT_DIR" || exit 1

# ensure working tree clean
git init
git add .
git commit -m "Initial AutoPR demo repo" || true
git branch -M "$BRANCH"
git remote add origin "$REMOTE" || git remote set-url origin "$REMOTE"
git push -u origin "$BRANCH"

echo "Done. Visit your repository and open a PR to trigger the demo workflow." 
