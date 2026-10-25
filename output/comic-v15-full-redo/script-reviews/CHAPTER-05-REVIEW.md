# Chapter 5 script review: reviser's decisions

Script: `scripts/CHAPTER-05-SCRIPT.md` (r2). Pre-review draft: `script-reviews/CHAPTER-05-SCRIPT-r1.md`.
Checked against `book1_horse_servant/book1_chapter05_road_to_travancore.md`, `CONTINUITY.md`, the Chapter 4 and Chapter 6 scripts, and `pipeline/script_pipeline.py`.

Result: 8 pages, 40 panels (was 39). 31 findings: 30 applied, 1 rejected.

## Fidelity

1. **Page 4, 4.4-4.5, raiding admission and "Your masters. Not you." (major).** APPLIED. The novel has both lines, and without them "I serve" answers nothing; restored verbatim ("We have learned to ride down..."), page 4 now ends on the fort line and "Our fortresses are both" gets its own panel (5.1). One sub-claim is wrong: 7.3's "You raided them?" refers to the Portuguese, not the coast.
2. **8.4 bow caption cut in half (major).** APPLIED. The dropped half carries the meaning and Chapter 6, 3.1 echoes the bow; the full sentence is now set verbatim across two boxes.
3. **1.4, "He will want to hear what you have seen" dropped (minor).** APPLIED. Short line that motivates the road; added as a second balloon ahead of the 1.5 flicker, as in the novel.
4. **8.5, maps and "south" merged away (minor).** APPLIED. Both novel sentences are now verbatim; the maps line plants Varma's rolled map in Chapter 6 and stays inside Nagoji's imagination.
5. **4.1, 7.4, 8.1 verbatim drift (minor).** APPLIED. All three now use the novel's wording ("both eyes...", "those local chiefs who think they can hide...", "He knows these hills").
6. **8.3-8.4 missing pause before the smile (minor).** APPLIED. New wordless 8.3 (hall still, stylus lifted, smile starting); the official speaks in 8.4.

## Craft

7. **7.5 stakes caption lettered after the question (major).** APPLIED. Caption moved to the top of 7.5 and reworded as a lead-in ("Then came the question..."), so the question is the last element before the turn; kept near-verbatim rather than trimmed.
8. **8.5 too dense, cut the road caption (minor).** REJECTED. It conflicts with finding 4: once the maps sentence is restored, "toward him" has a referent and no longer repeats 8.4's war-hall line, and it is the chapter-title payoff. Density is handled instead by making 8.5 the tallest tier, with the captions in the moonlit sky.
9. **8.2 "tighter" yet showing the hall; three push-ins (minor).** APPLIED. Page 8 is now a reverse wide from behind the platform (8.1), then a close on the eyes (8.2), then a side-on silent wide (8.3).
10. **1.5 caption labels the flicker; notes misname 4.2 a silent beat (minor).** APPLIED. Cut "A calculation. A road not taken." so the art plants it wordlessly, as with Duarte. The note is corrected, and now records the Chapter 11 and 26 payoff so the artist sells the look.
11. **2.4 restages Chapter 1, 6.5 with an explanatory caption (minor).** APPLIED (option a). The mare bleed stays and there is no text; the preceding "on a horse?" balloon carries the link.
12. **Page 5 ends on a quip (minor).** APPLIED. The shrine and the storms-and-horses reply come before the climb, so the page ends on the watcher and "announced", which hands off to the gate. The reorder is logged in the notes.
13. **Page-turn markers after pages 2, 6 and 7 (minor).** APPLIED. Consecutive turns are impossible, so only the marker after page 7 is kept. The recto assumption is flagged below because current page counts contradict it.
14. **2.1 "back in the room" (minor).** APPLIED. He is now still crouched at the mat's edge and rises in 2.3.
15. **1.3 and 7.3 eyelines on several targets (minor).** APPLIED. 1.3 locks on the brand; 7.3 locks on the left sleeve over the brand, with the hands in frame.
16. **4.5 "I serve" is a non sequitur (minor).** APPLIED, through finding 1: "Your masters. Not you." is restored as the prompt.

## Continuity

17. **Ibrahim has no locked look (blocker).** APPLIED in the script. His Chapter 4, 6.5 look (white turban, short grey-flecked beard with the LEFT scar as a bare pale line, pale vest over a white mundu, no coat) is set in 1.1 and the page blocks, with a tag in every Ibrahim panel. I did not edit CONTINUITY.md; see orchestrator actions. Verified that the pipeline finds no Ibrahim block at all, so the script text is currently the only source.
18. **The official reads like Ibrahim or the temple priest (major).** APPLIED. He is now a Nair official (topknot, clean chin, greying moustache, bare torso, white mundu, plain shoulder cloth; no turban, beard, thread or marks), at screen right in 7.4 with Ibrahim at screen left. I also removed the diwan's name from 6.3's description, because the pipeline would have added that character's bible look to the panel.
19. **Brand arm and side unspecified (major).** APPLIED. It is now a crude cross, no letters, on the LEFT upper arm just below the shoulder (matching Chapter 4, 3.2): 1.1, 1.3 over the LEFT shoulder, and the LEFT sleeve in 7.3.
20. **"Simple cream shirt" will be drawn modern (major).** APPLIED. It is now a loose, collarless, pullover homespun tunic-shirt with no buttons, collar or pocket, repeated in 3.1 and the page 3 block.
21. **Guards, watcher and hall men undescribed (major).** APPLIED. All are drawn as Nair men, matching Chapter 6, 1.4 but without matchlocks; 6.2 states that Nagoji is still on the sacks.
22. **1.4 scar may be mirrored (major).** APPLIED. The bible's ANATOMICAL LEFT wording is used, with a three-quarter view, the left cheek to camera and the left thumb on the scar. 4.4 and 5.1 are also blocked so his left side faces the camera.
23. **Pages 1-2 costume vs the bible's Chapter 5-6 row; ankle chafe rings (minor).** APPLIED in the script. There is an explicit override in 1.1 and the page 1 block. Verified that the pipeline injects the 5-6 row as authoritative into every Chapter 5 prompt, so the bible or prompt fix below is needed before generation.
24. **No Nagoji character block or concept attachment (minor).** APPLIED. There are Chapter 6-format blocks at the top of pages 1, 3 and 6 (nagoji-v2.png, gold stud, curly hair loose then tied back). The parser ignores page-level prose, so key details are also repeated in the panels.
25. **Healer thinner than Chapter 4, 5.4 (minor).** APPLIED. Her Chapter 4 description (fifties, plain cotton sari, grey-streaked hair) is carried over.
26. **2.1/2.3 re-entry contradiction (minor).** APPLIED. Same fix as finding 14.
27. **No carter; cart and sacks risk modern or lettered (minor).** APPLIED with one change. The carter is added, with an open two-wheeled cart, spoked wooden wheels, no hood, and unmarked cloth and palm-leaf sacks. He wears a short plain mundu and a topknot instead of a checked lungi and head cloth: the checked lungi is a period risk, and a head cloth would put a second wrapped head beside Ibrahim's turban.
28. **Temple roof will be drawn as a gopuram or shikhara (minor).** APPLIED. 4.3 now specifies a low, tiered, gabled tiled Kerala roof with a brass lamp-post and no tower.
29. **Night panels have no light source (minor).** APPLIED. A cart lantern is the key light from 5.1 to 6.1, "heavy air" becomes low mist in 5.5, and 8.5 is moonlit with a high camera so the vines and road show over the wall.
30. **Ash on Ibrahim's forehead will flicker (minor).** APPLIED. The ash is applied in 5.3, tagged in every later Ibrahim panel, and noted in the page 6 block.
31. **7.3, 8.2, 8.4 not drawable as written (minor).** APPLIED. 7.3 is over the official's shoulder with a single eyeline; the old 8.2 becomes the 8.1 reverse wide; the official in 8.4 is mid-ground and readable, with the captions set around Nagoji's lowered head.

## Orchestrator actions (outside this reviser's files)

- **CONTINUITY.md, Nagoji table:** put the pages 1-2 exception inside the existing `5-6` row, for example "Ch5 pages 1-2 only: bare-chested, cream captivity dhoti, LEFT upper-arm cross brand, chest rope burns, ankle chafe rings, no irons, hair loose. From ch5 page 3: collarless cream homespun pullover tunic-shirt over a village cotton dhoti...". Do not add a separate row: `_nagoji_look` only reads rows whose first cell is a bare chapter number or range, so it would ignore a "5 pp1-2" row.
- **CONTINUITY.md, Ibrahim:** the bullet `- **Ibrahim Marakkar** ("kapitan"):` does not match the parser's `**Name**:` pattern, so it is folded into the Keshavrao block and Ibrahim gets no continuity text. Reformat the bullet and add his Chapter 4-5 look (white turban, short grey-flecked beard, LEFT scar, pale vest, white mundu, no coat), keeping the turban and beard under the Chapter 6 coat. The Chapter 6 script also omits the turban and beard.
- **Cast overrides for generation:** Nagoji is inferred into 1.4, 7.2 and 7.5 from narration or off-panel lines, but he is not in frame there.
- **Page parity:** Chapters 1-4 currently total 31 pages (9 + 6 + 10 + 6). With continuous pagination from a recto and no front matter, Chapter 5 would open on page 32, a verso, and the page 7 turn would become a facing spread. Settle this at assembly.
