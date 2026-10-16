#!/usr/bin/env bash
# Publish an already validated build in one Git commit, retaining branch history.
set -euo pipefail

output="$(cd "${1:-build}" && pwd)"
script_dir="$(cd "$(dirname "$0")" && pwd)"
python3 "$script_dir/verify-build.py" "$output"

publish_dir="$(mktemp -d)"
rmdir "$publish_dir"
trap 'git worktree remove --force "$publish_dir" >/dev/null 2>&1 || true' EXIT

# An empty successful response means the publication branch does not exist yet.
# Network/authentication failures stop the script instead of resetting history.
existing="$(git ls-remote --heads origin refs/heads/rule-set)"
if [[ -n "$existing" ]]; then
  git fetch --depth=1 origin refs/heads/rule-set
  git worktree add --detach "$publish_dir" FETCH_HEAD
else
  git worktree add --detach "$publish_dir" HEAD
  git -C "$publish_dir" checkout --orphan rule-set
fi

git -C "$publish_dir" rm -rf --ignore-unmatch .
cp -R "$output/." "$publish_dir/"
git -C "$publish_dir" add --all
if git -C "$publish_dir" diff --cached --quiet; then
  echo "Rules unchanged; skipping publication."
  exit 0
fi
git -C "$publish_dir" -c user.name='github-actions[bot]' \
  -c user.email='41898282+github-actions[bot]@users.noreply.github.com' \
  commit -m "Update rule sets"
git -C "$publish_dir" push origin HEAD:refs/heads/rule-set
