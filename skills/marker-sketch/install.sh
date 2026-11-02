#!/usr/bin/env bash
# Installe marker-sketch pour Claude Code (niveau utilisateur par défaut).
#   bash install.sh              -> ~/.claude/skills/marker-sketch
#   bash install.sh --project    -> ./.claude/skills/marker-sketch
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HOME/.claude/skills"
[ "${1:-}" = "--project" ] && DEST="$PWD/.claude/skills"
mkdir -p "$DEST"
if [ "$SRC" != "$DEST/marker-sketch" ]; then
  rm -rf "$DEST/marker-sketch"
  cp -R "$SRC" "$DEST/marker-sketch"
fi
echo "Skill installée dans $DEST/marker-sketch"
if command -v python3 >/dev/null 2>&1; then
  python3 -m pip install --quiet --user fonttools playwright 2>/dev/null || python3 -m pip install --quiet --break-system-packages fonttools playwright 2>/dev/null || echo "Dépendances non installées (fonttools, playwright): voir README.md"
  python3 -m playwright install chromium >/dev/null 2>&1 || echo "Chromium non installé: les PNG de contrôle seront indisponibles."
else
  echo "python3 introuvable: installer Python 3 pour les scripts."
fi
echo "Dans Claude Code: /reload-skills puis /skills pour vérifier."
