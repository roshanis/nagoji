#!/bin/bash

set -euo pipefail

OUTPUT_FILE="Tigers_Heir.epub"
MANUSCRIPT_FILE="manuscript_book3.md"

TITLE="Tiger's Heir"
AUTHOR="RV Menon"
COVER_IMAGE="images/cover.jpg"

echo "Building $OUTPUT_FILE..."

awk 'FNR==1 && NR!=1 {print ""} {print}' \
  book3_tigers_heir/title_page.md \
  book3_tigers_heir/b3_chapter01_the_knife_in_the_dark.md \
  book3_tigers_heir/b3_chapter02_the_hunters.md \
  book3_tigers_heir/b3_chapter03_the_road_south.md \
  book3_tigers_heir/b3_chapter04_arcot.md \
  book3_tigers_heir/b3_chapter05_the_ghats.md \
  book3_tigers_heir/b3_chapter06_the_gate.md \
  book3_tigers_heir/b3_chapter07_revathis_gambit.md \
  book3_tigers_heir/b3_chapter08_the_lowest_rung.md \
  book3_tigers_heir/b3_chapter09_the_old_dutchman.md \
  book3_tigers_heir/b3_chapter10_earning_the_saddle.md \
  book3_tigers_heir/b3_chapter11_lessons.md \
  book3_tigers_heir/b3_chapter12_the_kings_eye.md \
  book3_tigers_heir/b3_chapter13_brothers.md \
  book3_tigers_heir/b3_chapter14_the_knifes_weight.md \
  book3_tigers_heir/b3_chapter15_the_house_of_velinadu.md \
  book3_tigers_heir/b3_chapter16_the_north_smells_of_smoke.md \
  book3_tigers_heir/b3_chapter17_refugees.md \
  book3_tigers_heir/b3_chapter18_mariam.md \
  book3_tigers_heir/b3_chapter19_father_thomas.md \
  book3_tigers_heir/b3_chapter20_a_house_of_their_own.md \
  book3_tigers_heir/b3_chapter21_the_lines.md \
  book3_tigers_heir/b3_chapter22_breach.md \
  book3_tigers_heir/b3_chapter23_fire_and_flight.md \
  book3_tigers_heir/b3_chapter24_the_tiger_at_alleppey.md \
  book3_tigers_heir/b3_chapter25_the_flag.md \
  book3_tigers_heir/b3_chapter26_the_treaty.md \
  book3_tigers_heir/b3_chapter27_new_masters.md \
  book3_tigers_heir/b3_chapter28_the_fourth_war.md \
  book3_tigers_heir/b3_chapter29_the_breach.md \
  book3_tigers_heir/b3_chapter30_the_frenchman.md \
  book3_tigers_heir/b3_chapter31_the_reckoning.md \
  book3_tigers_heir/b3_chapter32_what_we_carry.md \
  book3_tigers_heir/b3_epilogue_monsoon.md \
  glossary.md \
  front_matter_about_author.md \
  > "$MANUSCRIPT_FILE"

echo "Created concatenated manuscript: $MANUSCRIPT_FILE"

pandoc "$MANUSCRIPT_FILE" \
  -o "$OUTPUT_FILE" \
  --metadata title="$TITLE" \
  --metadata author="$AUTHOR" \
  --epub-cover-image="$COVER_IMAGE" \
  --css=epub.css \
  --split-level=1 \
  --toc \
  --toc-depth=2

echo "Successfully created $OUTPUT_FILE"
