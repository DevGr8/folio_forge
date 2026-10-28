#!/usr/bin/env bash
# ============================================================================
# One-Command GitHub Upload Script
# Usage:
#   chmod +x push_to_github.sh
#   ./push_to_github.sh https://github.com/<your-username>/<your-repo-name>.git
# ============================================================================
set -e

if [ -z "$1" ]; then
  echo "Usage: ./push_to_github.sh https://github.com/<your-username>/<your-repo-name>.git"
  exit 1
fi

REPO_URL="$1"

if [ ! -d ".git" ]; then
  git init
  git branch -M main
fi

git add .
git commit -m "Feat: AI-Powered Portfolio Database & Dynamic Resume Generator (Gemini API + Google Sheets + PDF/DOCX)" || true
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
git push -u origin main

echo "✅ Successfully pushed repository to $REPO_URL"
