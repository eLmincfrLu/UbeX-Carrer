#!/usr/bin/env bash
# Run from Git Bash: cd ~/projects/ubex && bash setup-github.sh

set -e
cd "$(dirname "$0")"

echo "==> Initializing git..."
git init

echo "==> First commit..."
git add .
git commit -m "Initial commit: UBEx Flask MVP"

echo ""
echo "Done locally. Next steps:"
echo "  1. Create empty repo on GitHub (no README/license)"
echo "  2. Replace YOUR_USER and YOUR_REPO below, then run:"
echo ""
echo "  git branch -M main"
echo "  git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git"
echo "  git push -u origin main"
echo ""