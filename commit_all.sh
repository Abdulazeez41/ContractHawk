#!/bin/bash

# Ensure we're on the main branch
git checkout main

# Capture all modified + untracked files (excluding deleted)
FILES=$(git ls-files --others --exclude-standard; git diff --name-only)

echo "📦 Total files to commit: $(echo "$FILES" | wc -l)"
echo "⚙️  Starting individual commits..."

for FILE in $FILES; do
  if [ ! -f "$FILE" ]; then
    echo "⚠️  Skipping (not a regular file): $FILE"
    continue
  fi

  git add "$FILE"

  # Get directory and filename
  DIR=$(dirname "$FILE")
  NAME=$(basename "$FILE")

  # Infer commit message based on location
  case "$FILE" in
    README.md)
      MSG="docs: update main README with current project status"
      ;;
    .solhint.json)
      MSG="chore: add Solidity linting config (.solhint.json)"
      ;;
    Dockerfile)
      MSG="chore: add Dockerfile for containerized setup"
      ;;
    docker-compose.yml)
      MSG="chore: add docker-compose file for multi-service orchestration"
      ;;
    package.json)
      MSG="chore: add Node.js project manifest"
      ;;
    package-lock.json)
      MSG="chore: add lockfile for npm dependencies"
      ;;
    requirements.txt)
      MSG="chore: add Python requirements.txt for dependencies"
      ;;
    main.py)
      MSG="feat: add main orchestrator script"
      ;;
    solc-static-linux)
      MSG="chore: add static Solidity compiler binary"
      ;;
    agents/*)
      MSG="feat(agents): added agent structure and files - $NAME"
      ;;
    core/*)
      MSG="feat(core): add core logic structure and files - $NAME"
      ;;
    scripts/*)
      MSG="feat(scripts): add script - $NAME"
      ;;
    tools/*)
      MSG="feat(tools): integrated agent tools - $NAME"
      ;;
    utils/*)
      MSG="feat(utils): add utility module - $NAME"
      ;;
  esac

  echo "✅ Committing $FILE → $MSG"
  git commit -m "$MSG"
done

# Final push
echo "🚀 Pushing all commits to origin/main..."
git push origin main
