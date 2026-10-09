set -e
P=/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python
S=/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad
export PYTHONDONTWRITEBYTECODE=1
# run CH PACKAGE TAG FOLIO REVISION DECISIONS FACES KEEP EXTRA(assembler flags)
run() { ch=$1; C=$2; tag=$3; folio=$4; rev=$5; dec=chapters/$C/review/$6; faces=chapters/$C/review/$7; keep=chapters/$C/review/$8; extra=$9
  pkgflag=""; [ "$C" != "ch0$ch" ] && [ "$C" != "ch$ch" ] && pkgflag="--package-dir chapters/$C"
  echo "== $C assemble $tag-a"
  $P $S/lean_assemble.py --chapter $ch --package chapters/$C --decisions $dec --tag $tag-a --no-backup --draw --faces-file $faces --face-scale 1.0 --keep-file $keep $extra > $TMPDIR/$C-$tag-a.json; grep -E '"selected"|"regenerate"' $TMPDIR/$C-$tag-a.json
  echo "== $C fit"
  $P pipeline/run_chapter.py fit-layout --chapter $ch $pkgflag --manifest chapters/$C/SELECTION-INPUT-$tag-a.json --decisions $dec --faces-dir chapters/$C/review/geometry-$tag-a --layout ${LAYOUT_IN:-chapters/$C/LAYOUT.json} --layout-out chapters/$C/LAYOUT-fitted-$tag.json --probe --structures ${FIT_EXTRA:-} > $TMPDIR/$C-$tag-fit.json; $P $TMPDIR/check_fit.py $TMPDIR/$C-$tag-fit.json
  echo "== $C assemble $tag-b"
  $P $S/lean_assemble.py --chapter $ch --package chapters/$C --decisions $dec --tag $tag-b --draw --faces-file $faces --face-scale 1.0 --keep-file $keep $extra --layout chapters/$C/LAYOUT-fitted-$tag.json > $TMPDIR/$C-$tag-b.json; grep -E '"selected"|"regenerate"|failed|carried' $TMPDIR/$C-$tag-b.json | cut -c1-300
  echo "== $C build $rev"
  $P pipeline/run_chapter.py build --chapter $ch $pkgflag --manifest chapters/$C/SELECTION-INPUT-$tag-b.json --layout chapters/$C/LAYOUT-fitted-$tag.json --first-folio $folio --revision $rev 2>&1 | grep -v "OMP\|^((" | tail -8 || true
}
