#!/usr/bin/env bash
# Download the Swiss Ephemeris data files that Jagannatha Hora itself ships.
#
# Without these, pyswisseph falls back to the built-in Moshier ephemeris. That
# is accurate to a fraction of an arcsecond for the classical seven, but it is
# NOT what JHora uses, so parity work at arcsecond tolerance needs these files.
#
# Default set spans 1800-2400 CE (600 years per file), which covers all natal
# work. Pass --full for the complete 13000 BCE - 16800 CE range (~100 MB).
set -euo pipefail

DEST="${DEST:-$(cd "$(dirname "$0")/.." && pwd)/data/ephe}"
BASE="https://raw.githubusercontent.com/aloistr/swisseph/master/ephe"
mkdir -p "$DEST"

FILES=(sepl_18.se1 semo_18.se1 seas_18.se1 sefstars.txt seorbel.txt)

if [ "${1:-}" = "--full" ]; then
  FILES=(sefstars.txt seorbel.txt)
  for prefix in sepl semo seas; do
    for n in m132 m126 m120 m114 m108 m102 m96 m90 m84 m78 m72 m66 m60 m54 m48 \
             m42 m36 m30 m24 m18 m12 m06 _00 _06 _12 _18 _24 _30 _36 _42 _48 \
             _54 _60 _66 _72 _78 _84 _90 _96 _102 _108 _114 _120 _126 _132 \
             _138 _144 _150 _156 _162 _168; do
      FILES+=("${prefix}${n}.se1")
    done
  done
fi

for f in "${FILES[@]}"; do
  if [ -f "$DEST/$f" ]; then
    echo "have  $f"
  elif curl -fsSL "$BASE/$f" -o "$DEST/$f"; then
    echo "fetch $f"
  else
    rm -f "$DEST/$f"
    echo "skip  $f (not published upstream)" >&2
  fi
done

echo
echo "Ephemeris installed in $DEST"
echo "The engine picks these up automatically; override with HORA_EPHE_PATH."
