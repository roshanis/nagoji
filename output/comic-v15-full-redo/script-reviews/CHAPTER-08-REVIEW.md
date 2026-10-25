# Chapter 8 script review: reviser's disposition

Script: `scripts/CHAPTER-08-SCRIPT.md` (r2). Pre-review draft: `script-reviews/CHAPTER-08-SCRIPT-r1.md`.
Checked against `book1_horse_servant/book2_chapter08_padmini_ammas_estate.md`, `CONTINUITY.md`, the neighbouring chapter scripts and `pipeline/script_pipeline.py`.

Result: 12 pages, 57 panels (was 11 pages, 55 panels). 33 findings: 33 applied (5 of them modified or in part), 0 rejected outright. The parts not taken are listed under findings 6, 15, 16, 25 and 27.

## Fidelity

1. **Page 11, 11.1: Padmini's reasons and Nagoji's motive cut (major). APPLIED.** Checked against the novel: the lines are there, and "older than his throne" feeds Chapter 9's Revathi line. They are now in 11.1 and 11.2, verbatim ("The Velinadu line is old. Older than his throne"). The overflow moved the close to a new page 12.
2. **Page 10, 10.4: Revathi reduced to a joke (major). APPLIED.** "Listen to her as carefully as you listen to Ramayyan" is added to 10.4, and the caption, with "sharp-tongued" restored, now opens 10.5.
3. **Page 11, 11.4: thesis line and "power had been simple" cut (major). APPLIED.** Both are restored in 12.2 and 12.3, so "A house that remembered..." has its subject again.
4. **Page 5, 5.4: "understanding an estate... a charge" cut (minor). APPLIED.** It is restored verbatim in its own balloon. Nagoji's reply moved to 5.5 to spread the words.
5. **Page 2, 2.3 and 2.4: caste stake and misquote (minor). APPLIED.** "They are... particular about who sleeps under their roof" is restored, and the caption now reads "questions of blood and birth".
6. **Page 7, 7.2: novel's shadows image paraphrased (minor). APPLIED.** Both of the novel's sentences are used. "Here they flowed through the centre" states a habit of the house, not the moment drawn, so it no longer clashes with the women being gone in 7.3.
7. **Page 7, 7.5: "heavier than jackfruit" cut (minor). APPLIED.** The beat is now 7.4, split as "Yes." / caption / the family line.

## Craft

8. **Page 8: five static faces (major). APPLIED.** 8.2 has the Maratha column bleed behind his head. 8.4 is wide and high, with crows and a watching woman. 8.3 gets the jackfruit seed, and 8.1 the tumbler stopped halfway.
9. **Page 10: second talking-heads page (major). APPLIED.** 10.1 shows the horses led out to graze, 10.2 the girl with the water pot, 10.3 Ibrahim and Nagoji's riders at the baggage cart, and 10.5 the stick laid across her knees.
10. **Page 6, 6.1: caption repeats the drawn smile (major). APPLIED.** The panel is restaged from behind his shoulder, so only the caption carries the smile. Padmini's sideways look stays.
11. **Page 7: six frames and about 130 words (major). APPLIED.** 7.3 and 7.4 are merged and her follow-up is trimmed to "He is honest, then. Good." The page is now four panels and an inset.
12. **Page 10, 10.4: 45 words (minor). APPLIED.** The caption moved to 10.5 and "You will meet one of those tongues soon" moved to 10.3. 10.4 is now 35 words.
13. **Page 4, 4.3: caption restates the bow (minor). APPLIED.** Only the Patil comparison is kept, and the art shows the depth of the bow.
14. **Page 3, 3.3: caption states what the art stages (minor). APPLIED.** 3.3 now runs silent, and 3.1 already carries "everything about it said power".
15. **Page 7, 7.2: "Here they stayed to listen" describes the art (minor). APPLIED, modified.** The line is replaced by the novel's habitual sentence (finding 6) rather than cut. The shot note "neither leaves at once" was removed, so the caption no longer describes the drawn action.
16. **Page 8, 8.5: page ends on a definition (minor). APPLIED, modified.** Page 8 now ends on "*Sambandham.*" and the definition opens 9.1. The suggested cut of "Her *tharavadu*" was not taken, because Chapters 13 and 17 to 19 use the word and it is introduced here. 9.1 is instead a tall panel.
17. **Page 11, 11.5: "Two days to learn..." is redundant (minor). APPLIED.** It is cut. The chapter ends on the novel's closing lines alone.
18. **Page 1, 1.5 into 2.1: whom Ramayyan addresses, and the location jump (minor). APPLIED.** Nagoji is reined in at the verandah beside Ramayyan, and 2.1's "Then the king's ola came" marks the time jump.

## Continuity

19. **Principals missing from panel lines, so the pipeline casts them empty or wrong (blocker). APPLIED.** Every on-panel principal is now named in the panel line, and page 9's staging note has moved into its panels. Every panel was re-checked with `infer_cast`, and all 57 final casts match the intended staging.
20. **Names in the lettering pull absent characters into panels (major). APPLIED.** Cast overrides are listed in the adaptation notes for 2.2, 2.5, 3.1, 4.5, 6.2, 9.4, 10.4, 11.1, 11.2 and 12.3. The 4.2 and 10.4 descriptions no longer name Nagoji or Revathi. The reviewer's 4.2 override is unnecessary after the rewording, and 4.2 now infers Padmini alone.
21. **Page 5, 5.1: cross-chapter reference the model cannot see (major). APPLIED.** The framing is written out with the clean-shaven chin. The Chapter 1 echo stays in the notes only, with a warning not to attach Chapter 1 frames before the pilot fix.
22. **Horse colours unset (major). APPLIED.** Nagoji rides a plain grey gelding in every mounted panel and in 5.3 and 10.1, and Ibrahim a sturdy brown pony. Kayal (bay mare) is not the novel's gelding.
23. **Ibrahim's head and face will drift (major). APPLIED.** The white turban and short grey-flecked beard from Chapter 4, 6.5 are in every Ibrahim panel. The CONTINUITY.md edit is flagged for the author: that file is shared and hash-locked, and Ibrahim's entry is currently parsed into Keshavrao's block.
24. **Page 4, 4.4: brand shape and place (major). APPLIED.** The brand is a crude burned cross with no letters or numerals, on the left forearm above the wrist, matching Chapters 7, 9 and 10. The chapter 4 "upper arm" row is flagged for the author.
25. **Lettering too heavy in 10.4, 11.1 and 4.3 (major). APPLIED, in part.** 10.4 is lightened as in finding 12, 11.1 is split and enlarged to a third of the page, and 4.3 is trimmed as in finding 13. Two parts were not taken. Moving "He allows her to speak against him?" to 10.5 was rejected, because the question belongs with the Varma memory that motivates it and page 10 already ends on a turn. The alternative 4.3 trim was superseded by finding 13.
26. **Page 6, 6.5: vertical composition in a horizontal strip (major). APPLIED.** It is now a low angle, with the stick strike in the left foreground and her face in the right third.
27. **Pages 1.3 and 1.4: chavers, the official and the column undefined (major). APPLIED, modified.** The chavers, the kneeling official and the bandaged riders with no blood are all defined. The chavers carry ash rather than a red brow cloth, to match Chapter 22's chaver. The script's invented "Nair riders" were replaced by Chapter 7's Madurai and Maravar riders, who are this column.
28. **Page 11, 11.1: Varma look (minor). APPLIED.** It now uses the Chapter 6, 2.2 coastal-hall description, and the parenthetical is dropped.
29. **Household women and Padmini default to modern dress or Revathi's markers (minor). APPLIED.** The women wear off-white mundu and an upper cloth, with no stitched blouse, no blue, no coins and no armlets. Padmini's sari is the old Kerala drape with no stitched blouse. Adding this to her CONTINUITY.md entry is flagged.
30. **Boots indoors (minor). APPLIED.** He leaves his boots at the pavilion step (2.1) and the verandah step (5.4) and is barefoot inside the house, matching Chapter 9. His bare feet in 11.4 also sit under the "Deccan boot" line.
31. **Page 2, 2.1: Ramayyan could render as a temple priest (minor). APPLIED.** His tag is restated, with "a minister at his accounts, not a priest" and no ritual implements.
32. **Pages 3.1 and 1.1: Mangalore tiles and European boats (minor). APPLIED.** 3.1 has curved hand-made country tiles, and 1.1 has plank-sewn canoes and log catamarans.
33. **Page 1, 1.2: "eyes streaming" reads as weeping (minor). APPLIED.** He now has eyes watering from the chilli, is fanning his tongue and grinning, and the fisherman is laughing.
