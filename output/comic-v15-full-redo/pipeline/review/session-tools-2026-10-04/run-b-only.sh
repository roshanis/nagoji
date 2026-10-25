set -e
P=/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python
S=/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad
export PYTHONDONTWRITEBYTECODE=1
# runb CH PACKAGE TAG(b-pass tag) LAYOUT FOLIO REV DECISIONS FACES KEEP EXTRA
runb() { ch=$1; C=$2; tag=$3; layout=$4; folio=$5; rev=$6; dec=chapters/$C/review/$7; faces=chapters/$C/review/$8; keep=chapters/$C/review/$9; extra=${10}
  pkgflag=""; [ "$C" != "ch0$ch" ] && [ "$C" != "ch$ch" ] && pkgflag="--package-dir chapters/$C"
  echo "== $C assemble $tag"
  $P $S/lean_assemble.py --chapter $ch --package chapters/$C --decisions $dec --tag $tag --draw --faces-file $faces --face-scale 1.0 --keep-file $keep $extra --layout $layout > $TMPDIR/$C-$tag.json; grep -E '"selected"|"regenerate"|failed|carried' $TMPDIR/$C-$tag.json | cut -c1-300
  echo "== $C build $rev"
  $P pipeline/run_chapter.py build --chapter $ch $pkgflag --manifest chapters/$C/SELECTION-INPUT-$tag.json --layout $layout --first-folio $folio --revision $rev 2>&1 | grep -v "OMP\|^((" | tail -8 || true
}
