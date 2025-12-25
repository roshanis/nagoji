#!/bin/bash

# Output filename
OUTPUT_FILE="Horse_of_the_Servant.epub"
MANUSCRIPT_FILE="manuscript_complete.md"

# Metadata
TITLE="Horse of the Servant"
AUTHOR="RV Menon"
COVER_IMAGE="images/cover.jpg"

echo "Building $OUTPUT_FILE..."

# Concatenate files in specific order with a blank line between files.
# Note: book1_horse_servant/book*_chapter*.md relies on shell expansion to sort alphabetically, which is standard.
awk 'FNR==1 && NR!=1 {print ""} {print}' \
    title_page.md \
    dedication.md \
    front_matter_publication_notes.md \
    book1_horse_servant/front_matter_foreword.md \
    book1_horse_servant/front_matter_prequel.md \
    book1_horse_servant/front_matter_character_guide.md \
    book1_horse_servant/book*_chapter*.md \
    Author_Historical_Note_nagoji.md \
    book1_horse_servant/glossary.md \
    front_matter_about_author.md \
    > "$MANUSCRIPT_FILE"

echo "Created concatenated manuscript: $MANUSCRIPT_FILE"

# Run Pandoc
pandoc "$MANUSCRIPT_FILE" \
    -o "$OUTPUT_FILE" \
    --metadata title="$TITLE" \
    --metadata author="$AUTHOR" \
    --epub-cover-image="$COVER_IMAGE" \
    --css=epub.css \
    --split-level=1 \
    --toc \
    --toc-depth=2

if [ $? -eq 0 ]; then
    echo "Successfully created $OUTPUT_FILE"
else
    echo "Error running pandoc"
    exit 1
fi
