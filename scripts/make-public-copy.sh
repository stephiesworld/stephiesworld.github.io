#!/usr/bin/env bash
# Build a standalone, publishable copy of deployment-doctor/ with a fresh history.
#
# Why a fresh history rather than a subtree push: the commit messages and
# trailers in this repository reference a private context, and git history is
# permanent and public once pushed. Rewriting after the fact does not help —
# the old objects stay reachable through forks, caches, and the API. So the
# public copy starts from one clean commit.
#
# Usage:
#   ./scripts/make-public-copy.sh [output-dir]
#
# Then:
#   cd <output-dir>
#   git remote add origin git@github.com:<you>/deployment-doctor.git
#   git push -u origin main

set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL="$SRC_DIR/deployment-doctor"
OUT="${1:-$SRC_DIR/../deployment-doctor-public}"

[ -d "$TOOL" ] || { echo "error: $TOOL not found" >&2; exit 1; }

rm -rf "$OUT"
mkdir -p "$OUT"

# Only tracked files. Anything gitignored — .env above all — must not travel.
( cd "$TOOL" && git ls-files . ) | while read -r f; do
  mkdir -p "$OUT/$(dirname "$f")"
  cp "$TOOL/$f" "$OUT/$f"
done

# CI moves from a path-scoped job in a larger repo to the whole of this one.
mkdir -p "$OUT/.github/workflows"
sed -e 's/^name: deployment-doctor$/name: ci/' \
    -e '/paths: \["deployment-doctor/d' \
    -e '/working-directory: deployment-doctor/d' \
    -e '/^    defaults:$/d' \
    -e '/^      run:$/d' \
    -e "/^# Scoped to the tool's own directory/d" \
    -e '/^# has nothing to run\.$/d' \
    "$SRC_DIR/.github/workflows/deployment-doctor.yml" > "$OUT/.github/workflows/ci.yml"

# The study guide is prep material for a private purpose, not part of the tool.
rm -f "$OUT/docs/study-guide.html"

# Neutral section headings in place of the ones written for that purpose.
if [ -f "$OUT/docs/retrieval.md" ]; then
  sed -i.bak 's/^## What to say in an interview$/## The short version/' "$OUT/docs/retrieval.md"
fi
if [ -f "$OUT/docs/the-loop.md" ]; then
  sed -i.bak \
    -e 's/^## What to say in the interview$/## The short version/' \
    -e 's/which makes it a usable interview example:/which makes the contrast concrete:/' \
    "$OUT/docs/the-loop.md"
fi
find "$OUT" -name '*.bak' -delete

# Fail loudly rather than publish something that should have stayed private.
if grep -rniE "interview|delpaggio|@gmail\.com|claude\.ai/code/session" "$OUT" >/dev/null 2>&1; then
  echo "error: private references survived the scrub:" >&2
  grep -rniE "interview|delpaggio|@gmail\.com|claude\.ai/code/session" "$OUT" >&2
  exit 1
fi
if [ -e "$OUT/.env" ]; then
  echo "error: .env was copied — refusing to continue" >&2
  exit 1
fi

cd "$OUT"
git init -q -b main
git add -A
git -c user.name="Stephanie Del Paggio" -c user.email="stephiesworld@users.noreply.github.com" \
    commit -q -m "Deployment Doctor: audit a codebase's Claude API integration

Point it at a repository that calls the Claude API and get back a prioritised
scorecard: what will break, what is silently costing money, what is untested.

Roughly thirty deterministic checks run over parsed source with no model and no
tokens — retired model IDs, parameters that now return a 400, cache-control
placement below the model's silent minimum, tool version pairs, unhandled
refusals. Anything requiring judgement rather than a rule goes to a separate
pass, which runs either as a single call or as a real agent loop with grep and
read_file tools.

That judgement pass is itself graded, against a set of findings written down in
advance, so \"would a cheaper model do?\" is a measurement rather than an
argument.

Includes a browser UI, so the audit and the eval can be run without a terminal."

echo
echo "Built $OUT ($(git ls-files | wc -l | tr -d ' ') files, 1 commit)"
echo
echo "Next:"
echo "  cd $OUT"
echo "  git remote add origin git@github.com:stephiesworld/deployment-doctor.git"
echo "  git push -u origin main"
