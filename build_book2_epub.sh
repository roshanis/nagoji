#!/bin/bash

set -euo pipefail

OUTPUT_FILE="The_Dutchmans_Son.epub"
MANUSCRIPT_FILE="manuscript_book2.md"

TITLE="The Dutchman's Son"
AUTHOR="RV Menon"
COVER_IMAGE="images/cover.jpg"

echo "Building $OUTPUT_FILE..."

awk 'FNR==1 && NR!=1 {print ""} {print}' \
  book2_dutchmans_son/title_page.md \
  book2_dutchmans_son/b2_chapter01_the_kings_death.md \
  book2_dutchmans_son/b2_chapter02_smoke_at_colachel.md \
  book2_dutchmans_son/b2_chapter03_the_captive_boy.md \
  book2_dutchmans_son/b2_chapter04_lessons_in_iron.md \
  book2_dutchmans_son/b2_chapter05_lakshmi.md \
  book2_dutchmans_son/b2_chapter06_the_new_king.md \
  book2_dutchmans_son/b2_chapter07_house_by_the_backwaters.md \
  book2_dutchmans_son/b2_chapter08_the_sons_of_de_lannoy.md \
  book2_dutchmans_son/b2_chapter09_news_from_mysore.md \
  book2_dutchmans_son/b2_chapter10_the_rocket_wound.md \
  book2_dutchmans_son/b2_chapter11_english_faces.md \
  book2_dutchmans_son/b2_chapter12_the_liaison.md \
  book2_dutchmans_son/b2_chapter13_caspars_fire.md \
  book2_dutchmans_son/b2_chapter14_pepper_and_lead.md \
  book2_dutchmans_son/b2_chapter15_prisoners_of_mysore.md \
  book2_dutchmans_son/b2_chapter16_the_first_mysore_war.md \
  book2_dutchmans_son/b2_chapter17_the_old_mans_burden.md \
  book2_dutchmans_son/b2_chapter18_the_chapel.md \
  book2_dutchmans_son/b2_chapter19_the_dutch_shadow.md \
  book2_dutchmans_son/b2_chapter20_the_wall_takes_shape.md \
  book2_dutchmans_son/b2_chapter21_night_on_the_lines.md \
  book2_dutchmans_son/b2_chapter22_hendriks_command.md \
  book2_dutchmans_son/b2_chapter23_lakshmis_wisdom.md \
  book2_dutchmans_son/b2_chapter24_the_last_order.md \
  book2_dutchmans_son/b2_chapter25_the_funeral.md \
  book2_dutchmans_son/b2_chapter26_the_heir_of_udayagiri.md \
  book2_dutchmans_son/b2_chapter27_caspars_choice.md \
  book2_dutchmans_son/b2_chapter28_pollilurs_echo.md \
  book2_dutchmans_son/b2_chapter29_the_lines_tested.md \
  book2_dutchmans_son/b2_chapter30_refugees_again.md \
  book2_dutchmans_son/b2_chapter31_the_companys_price.md \
  book2_dutchmans_son/b2_chapter32_the_tiger_dies.md \
  book2_dutchmans_son/b2_epilogue_the_torch_passes.md \
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
