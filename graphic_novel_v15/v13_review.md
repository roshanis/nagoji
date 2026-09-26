# Review of V13 (Horse of the Servant, Reference Redesign r1)

Source: `output/pdf/Horse-of-the-Servant-V13-Reference-Redesign-r1.pdf`, 161 PDF pages
(front matter, 151 story pages, character pages). Page numbers below are the printed
numbers at the foot of each page.

## 1. Characters do not stay the same person

The largest problem with the art. The image model drew each panel from scratch, so
designs drift.

| Character | What happens in V13 | Effect |
|---|---|---|
| Nagoji | Three unrelated looks: curly hair and a tunic (Ch 1 to 5), red turban and white shawl (Ch 7 to 16), bare-chested topknot (Ch 17 to 28). Page 96 shows him twice in one panel, once with each hair style. | The narrator is hard to find on the page. |
| Revathi | Purple and green silk (Ch 9, 20); blue silk with a different face (Ch 16, pages 79 and 80). | The Chapter 16 love scene reads as Nagoji with an unnamed woman. |
| Marthanda Varma | Peacock-feather turban on every appearance. | Krishna iconography, not Travancore royal dress. |
| Many men | Bodybuilder torsos and film-star faces. | Reads as a modern film poster, not 1738. |

## 2. Page mechanics that are visibly broken

- Page 136: the chapter title prints over the art; three balloons overflow their text;
  one balloon is empty; the last caption runs out of its box.
- About six different chapter header styles. Chapter 6 alone uses three (pages 22, 25,
  26), and headers appear on second and third pages of chapters.
- Page 54 is titled "The Nawab of Arcot's Raids", which is not a chapter; its raiders are
  drawn with green turbans and a crescent flag, a stereotype.
- The Chapter 1 map repeats its title cartouche and draws Chinese-style dragons.

## 3. It reads as an illustrated summary, not a comic

- Captions are mostly lifted from the novel's prose ("The sea was only one artery",
  "The cost had only changed its address"). Pictures illustrate the words rather than
  tell the story.
- Many panels are people seated or standing and talking. "Dutch on the Horizon" runs
  8 pages of council; the shipwreck gets 1 page (14); Colachel gets 7.
- Emotional beats have no setup. Kanka dies in one speech balloon (page 2) before we
  see him ridden. Keshavrao is only "Rao" until he drowns (page 14). Megha is introduced
  and dies on page 78.
- The romance is hard to follow: page 41 says the wife will "not be from my house",
  then pages 79 and 80 put Nagoji and Revathi together with no scenes between them in
  the comic, and she is in a different costume.
- The temple attack on the heir (pages 111 to 113) and the king taking a blade for the
  heir (page 123) are too alike; readers will take them for the same event or an error.
- Ramayyan's Test (pages 132 to 136) references "Ram", a shelf, and a priest "in my pay
  for eleven years" without setup in the comic.

## 4. What works

Colachel (pages 69 to 71) and the sand training in Horses in Wet Sand (pages 27 to 31):
clear action, panels that move, short captions. V15 holds every chapter to that standard.

## V15 response

| V13 problem | V15 fix | Where |
|---|---|---|
| Character drift | Locked designs with anchors and dated costume phases; character model sheets generated first and passed to every panel as references | `characters.yaml`, `tools/generate_qwen.py refs` |
| Broken lettering | Lettering is set in code, never by the image model; any overflow stops the build | `tools/build.py pages` |
| Header chaos | One header, chapter openers only | `tools/build.py`, `style_guide.md` |
| Summary storytelling | Rewritten script: cold open, setups for Kanka and Keshavrao, caption budget, silent panels | `script_ch01-05.yaml` |
| Period errors | Negative prompts for known errors; `verify` flags for the historian agent | `characters.yaml` |
