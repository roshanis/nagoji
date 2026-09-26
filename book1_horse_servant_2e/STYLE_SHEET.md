# Second Edition Style Sheet: Removing AI Slop

Apply these rules to every chapter. When a rule and the story disagree, the story wins, but note it in `notes/changelog.md`.

## 1. Kill on sight

- Em dashes (none allowed)
- "Not X, but Y" and "Not X. Y." correction constructions. Keep at most one per chapter, and only in dialogue where a character would really say it.
- Three-word fragment lists used for drama: "Horses. Guns. Storms." Rewrite as a sentence or cut.
- Kicker one-liners that restate the paragraph above: "This was where the Portuguese forged information."
- Explaining subtext just shown: "They wanted to see grief; they wanted to use it as a lever." Trust the reader.
- Vague depth words: "something older / deeper / else", "the weight of", "etched", "a sense of", "somehow", "in that moment", "for the first time" (unless it is literally the first time and that matters)
- "felt like another world entirely", "the air was thick with", "hung in the air", "a chill that had nothing to do with the wind"

## 2. Ration

| Item | Limit per chapter |
|---|---|
| "as if" | 1 |
| "like a ..." simile | 2, and each must use an image Nagoji would know (horses, the Deccan, forts, the sea, cooking fires) |
| slowly / quietly / softly | 2 in total |
| Rhetorical questions in narration | 1 |
| Sentence fragments for effect | 3 |

## 3. Chapter endings

- End on an action, an image, or a line of dialogue. Do not end on a summary, a moral, or "that was enough for now".
- No two chapters may share a closing idea. The recurring "storm" motif gets used once, where it matters most (Chapter 13 "The storm was here" is the best candidate).
- Cut any last paragraph that begins "But", "For now", "For the moment", "And some", "Perhaps".

## 4. Voice

- Nagoji is a Maratha cavalryman writing in the 1740s and 1750s. He is plain, practical, dry. He names things: saddle, matchlock, salt, rice, rope. He does not reach for abstractions.
- Similes come from his world, not from a writing workshop.
- He does not narrate his own emotional growth. Show it in what he does.
- Dialogue stays period-plausible. No "okay", no therapy language, no modern management words ("process", "navigate", "journey", "focus").

## 5. Rhythm

- Vary sentence length, but do not use the short punchy sentence as a reflex after every long one.
- A paragraph should not end with a short summary sentence more than once a page.
- Remove doubled adjectives when one does the work ("grey and tired" is fine; "cold, hard, unforgiving" is not).

## 6. Process per chapter

1. Run `audit/scan_slop.py` on the chapter; save the report.
2. Edit: cut first, then rewrite only what the cut breaks.
3. Re-scan; record before/after counts and word count.
4. Read aloud (or read slowly) the first and last pages to check the voice.
5. Log non-trivial changes in `notes/changelog.md`.
