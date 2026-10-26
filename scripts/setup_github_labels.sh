#!/usr/bin/env bash
set -euo pipefail
# Run from repository root after installing gh and running `gh auth login`.
gh label create "user-story" --color "1D76DB" --description "Пользовательская история" --force
gh label create "mvp" --color "0E8A16" --description "Входит в MVP" --force
gh label create "backlog" --color "FBCA04" --description "После MVP" --force
echo "Labels are ready. Now run: python scripts/create_github_issues.py"
