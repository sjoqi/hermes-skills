#!/usr/bin/env bash
# Pre-push PII / secret screen for a staging directory.
#
# Usage:
#   ./screen_for_pii.sh <dir> [extra_regex]
#
# Exit 0 = nothing found (still eyeball the output).
# Exit 1 = potential findings; review every line before pushing.
#
# ALWAYS pass locale-specific extras for the user (their own name, email,
# employer, school, phone prefix). The generic patterns below will NOT catch
# a name they never told you about.
#   ./screen_for_pii.sh /tmp/staging 'Acme Corp|State University|\+62'

set -uo pipefail
DIR="${1:?usage: screen_for_pii.sh <dir> [extra_regex]}"
EXTRA="${2:-}"
FOUND=0

if command -v rg >/dev/null 2>&1; then GREP="rg -n --no-heading -i"; else GREP="grep -rInE"; fi

scan() { # label, regex
  local out
  out=$($GREP "$2" "$DIR" 2>/dev/null | grep -v '/\.git/' | head -40)
  if [ -n "$out" ]; then
    echo "=== $1 ==="; echo "$out"; echo
    FOUND=1
  fi
}

scan "EMAIL"            '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
scan "PHONE (intl)"     '\+[0-9]{1,3}[ -]?[0-9][0-9 ()-]{6,}[0-9]'
scan "API KEY / TOKEN"  '(sk-[A-Za-z0-9]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|xox[baprs]-[0-9A-Za-z-]{10,}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,})'
scan "PRIVATE KEY"      'BEGIN [A-Z ]*PRIVATE KEY'
scan "BEARER"           'Bearer [A-Za-z0-9._-]{20,}'
scan "USER HOME PATH"   '/(Users|home)/[a-z0-9_.-]+'
scan "SOCIAL HANDLE"    '(linkedin\.com/in/|github\.com/|t\.me/|instagram\.com/|twitter\.com/|x\.com/)[A-Za-z0-9_.-]+'
scan "DB / CONN STRING" '(postgres|postgresql|mysql|mongodb(\+srv)?|redis|amqp)://[^ "'"'"']+'
scan "LONG NUMERIC ID"  '\b[0-9]{9,}\b'

[ -n "$EXTRA" ] && scan "USER-SUPPLIED PATTERN" "$EXTRA"

# Generated OOXML artifacts hide PII inside zipped XML.
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if unzip -p "$f" '*.xml' 2>/dev/null | grep -qiE "${EXTRA:-__nomatch__}"; then
    echo "=== OOXML INNER XML MATCH: $f ==="; FOUND=1
  fi
done < <(find "$DIR" -type f \( -name '*.docx' -o -name '*.xlsx' -o -name '*.pptx' \) 2>/dev/null)

if [ "$FOUND" -eq 0 ]; then
  echo "CLEAN: no matches for the screened patterns in $DIR"
  echo "NOTE: absence of matches is not proof. Placeholders must be obviously fictional"
  echo "      (Jane Q. Example / example.com / +1 555-0100 / Anytown, USA)."
else
  echo "REVIEW REQUIRED: potential findings above. Do NOT push until each is confirmed"
  echo "                 a deliberate placeholder."
fi
exit "$FOUND"
