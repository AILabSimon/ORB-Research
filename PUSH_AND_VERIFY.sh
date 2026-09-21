#!/bin/bash

set -e

cd "$(dirname "$0")"

echo "=== ORB GitHub Sync ==="

# Stage all research changes
git add -A

# Commit only if something changed
if git diff --cached --quiet; then
    echo "No uncommitted changes."
else
    MESSAGE="${1:-ORB automated research update}"
    git commit -m "$MESSAGE"
fi

LOCAL=$(git rev-parse HEAD)

echo ""
echo "Local commit: $LOCAL"
echo "Pushing to GitHub..."

git push origin master

echo ""
echo "Verifying remote..."

REMOTE=$(git ls-remote origin refs/heads/master | awk '{print $1}')

if [ "$LOCAL" = "$REMOTE" ]; then
    echo ""
    echo "================================="
    echo "GITHUB PUSH VERIFIED"
    echo "REMOTE HEAD: $REMOTE"
    echo "================================="
    exit 0
else
    echo ""
    echo "================================="
    echo "ERROR: GITHUB PUSH NOT VERIFIED"
    echo "LOCAL : $LOCAL"
    echo "REMOTE: $REMOTE"
    echo "================================="
    exit 1
fi
