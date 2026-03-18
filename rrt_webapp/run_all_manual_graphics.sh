#!/usr/bin/env bash
# Run the all_manual_graphics.pqi example and place JSON charts where the webapp can show them.
# Usage: from repo root: ./rrt_webapp/run_all_manual_graphics.sh
#        or: cd rrt_webapp && ./run_all_manual_graphics.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INPUT="$REPO_ROOT/manual_examples/files/all_manual_graphics.pqi"
OUT_DIR="$REPO_ROOT/manual_examples/output/all_manual_graphics"
PHREEQC=""

for exe in "$REPO_ROOT/build/phreeqc" "$REPO_ROOT/build/Release/phreeqc" /usr/local/bin/phreeqc phreeqc; do
  if command -v "$exe" >/dev/null 2>&1 || [ -x "$exe" ]; then
    PHREEQC="$exe"
    break
  fi
done
[ -n "$PHREEQC" ] || { echo "phreeqc not found. Build the project first (e.g. mkdir build && cd build && cmake .. && cmake --build .)."; exit 1; }

mkdir -p "$OUT_DIR"
# Run from OUT_DIR so JSON files are written there (and DATABASE path must be absolute)
DB="$REPO_ROOT/og/database/phreeqc.dat"
if [ ! -f "$DB" ]; then
  echo "Database not found: $DB"
  exit 1
fi
# Write input with absolute DATABASE so phreeqc finds it when cwd is OUT_DIR
(
  echo "DATABASE $DB"
  grep -v '^DATABASE' "$INPUT" || true
) > "$OUT_DIR/all_manual_graphics.pqi"

cd "$OUT_DIR"
"$PHREEQC" all_manual_graphics.pqi

echo "Done. Charts written to $OUT_DIR"
echo "Charts are under manual_examples/ so the webapp will find them. Start the webapp (flask --app app run), open http://127.0.0.1:5000, then click Refresh to view all 5 charts."
