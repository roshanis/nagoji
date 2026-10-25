# Chapter 2 script review: reviser's disposition

Script: `output/comic-v15-full-redo/scripts/CHAPTER-02-SCRIPT.md` (pre-review draft kept as `CHAPTER-02-SCRIPT-r1.md`).
Result: 6 pages, 29 panels (target 6, range 5 to 7). 36 findings: 36 applied, 0 rejected. Five were applied in a different form, and one was applied to the script only (notes below).
Each finding was checked against `book1_chapter02_slave_ship_south.md`, `CONTINUITY.md`, the Chapter 3 script and `pipeline/script_pipeline.py`. The pipeline checks were run, not assumed.

## Fidelity

1. **5.5, the sailor's warning is cut.** APPLIED. The novel has the officer answering "They say God sends warnings". That line is restored, and the first sailor's storm-season line now sits in 5.4. The lightning clause is dropped to save space.
2. **6.5, the chapter cuts outside to the storm.** APPLIED. The novel ends in the hold, and Chapter 3 opens on "the change in the way the ship moved". 6.5 is now the hold, tilted: a swinging chain, a prayer, running feet. No lightning. The staging note is updated.
3. **6.3, the rope line is cut.** APPLIED. It is verbatim from the novel and the only place the narration calls Keshavrao a boy. All three captions fit.
4. **4.5 and 5.1, the order is wrong.** APPLIED, in a different form. It is confirmed against the novel. "Do you know where they send us?" now ends page 4 as a page-turn question, and "South" opens page 5. After that come the cane, Chaul and chances, then the days passing in 5.4.
5. **1.4, "rising in one movement".** APPLIED. The novel says "I stood slowly, every joint complaining". He is now drawn braced and mid-rise, with a held wince.
6. **2.4, "almost involuntarily" is dropped.** APPLIED. It is verbatim in the novel. The gesture now escapes him and is then completed deliberately, which is the Chapter 24 and 25 plant.
7. **2.5, "I filed his face away" is cut.** APPLIED. It is Nagoji's accounting habit in his own voice, and it is now the first caption.
8. **4.3, "old military habit" and "sons of the Deccan" are lost.** APPLIED. Without them, "sahib" reads as caste deference instead of rank.
9. **3.3, João boards the ship.** APPLIED. In the novel he tugs the chain on the wharf. He now stands at the foot of the gangplank, and a ship's hand takes the chain at the top.
10. **Nagoji's pepper aside is cut.** APPLIED, in a different form. It is placed after the officer's "silver" balloon in 5.5. The novel's verbatim "a number of cruzados" is used rather than "a price".

## Craft

11. **5.3, the caption describes the Chaul inset.** APPLIED. It broke rule 1 of the exemplar. The caption is now "Near Chaul he dared the Portuguese to shoot the song out of his mouth."
12. **3.3, two framings in one thin panel.** APPLIED. The main frame is the gangplank with João's balloon. The feet and the "Horses would hate this" captions move to a corner inset. 3.2 is reduced to two fifths of the page to make room.
13. **6.2, a face close-up loses the hand.** APPLIED. It is now a medium shot, with the hand curled round an absent hilt described as a pose, not a motion.
14. **1.5, motions that one frame cannot show.** APPLIED. The head is turned a few degrees and the shoulders are rigid. The hand is curled at his hip, with enough slack in the wrist chain to reach it.
15. **6.1, the tilt compares against an earlier panel.** APPLIED, in a different form. The vertical references are a dipper hanging off true and slopped trough water. An overhead chain was not used, because a chain above a head risks reading as a noose (finding 25).
16. **3.1, "merchants" is plural but one is drawn.** APPLIED. Two or three merchants now stand in separate doorways, and the caption uses the novel's "Their eyes told a different story."
17. **5.5, "God sends opportunity" answers nothing.** APPLIED, merged with finding 1. The lightning clause is left out for space, as finding 1 allows.
18. **3.4, the bottom strip is overloaded.** APPLIED. It is composed on one axis: Nagoji at the hatch, the town small beyond the rail, and one or two background sailors.

## Continuity

19. **Blocker: the Ibrahim line is merged into Keshavrao's look.** APPLIED to the script only. Confirmed by running `_character_look(continuity, "keshavrao", 2)`, which returns the Ibrahim scar and coat. Every Keshavrao panel now says "no scar", and the lock at 1.5 adds "no coat or vest". The CONTINUITY.md edit was NOT made and needs the author: it is a shared file, and its sha256 is locked into the prepared `chapters/ch01/IMAGEGEN-JOBS.json`, so `run_chapter.load_job` would refuse Chapter 1 after any edit. The fix is one line: `- **Ibrahim Marakkar ("kapitan")**:`. Do not prepare Chapter 2 until it is made.
20. **Keshavrao has no identity lock.** APPLIED. He has no concept sheet and only "prisoner rags" in CONTINUITY. The full lock is at 1.5, a short form is in every panel he appears in, and the two-shots fix Nagoji on the left.
21. **Cast inference attaches Nagoji to Keshavrao solo panels.** APPLIED. Verified with `infer_cast` on the revised script. The overrides `{"page-04-panel-05": [], "page-06-panel-02": ["keshavrao"]}` are recorded in the adaptation notes. 3.1 now infers an empty cast, and the Chaul panel (5.2) infers Keshavrao only.
22. **Nagoji's clean chin appears only in 1.1.** APPLIED to the script only. The premise is wrong: `_nagoji_look` already prepends the Constant identity line (clean chin, moustache, ear stud), which was checked by running it. Short face locks were still added to 2.3, 2.5, 4.3, 5.1, 5.3 and 6.3 as cheap reinforcement.
23. **The guards have no costume.** APPLIED. They are defined once at 1.1 (morion or black hat, off-white shirt, buff jerkin, nothing red or blue, matching the Chapter 3 guard), with a short form at 1.3, 1.5, 3.4 and 4.1. João is set apart as bareheaded, the biggest man, in a brown jerkin, and he has his back to the tally scratches.
24. **The irons appear and vanish between panels.** APPLIED. Chapter 3 needs ankles "chained in pairs" and one chain linking both collars to a ring. Hobble chain, wrist chain and hinged collar are set at 1.3 and 1.5, repeated in the hold panels, and shown in the 3.3 inset.
25. **Collar chains to overhead rings read as a hanging.** APPLIED. The collars are rigid, and each chain leaves the collar at the side, droops along the plank and rises to a ring off to one side. No taut vertical chain appears in 4.1, 6.1 or 6.5.
26. **The wharf official could read as Duarte.** APPLIED. He is now a stout lay clerk in a brown coat and pale grey felt hat, ledger turned away, not in black. The name "Duarte" is kept out of the description so the cast does not attach him.
27. **3.3, two framings (continuity lens).** APPLIED, in a different form. It is solved together with findings 9 and 12: a main frame plus an inset. João's boots are not put at the top edge, because the novel puts him on the wharf.
28. **The ship's flag and name.** APPLIED. There is no national flag, only plain pennants, and no name or lettering, in 3.2 and 3.4. The 6.5 ship tie is moot because 6.5 now stays in the hold.
29. **The other prisoners are cloned as Nagoji.** APPLIED. They vary in age and build, wear grey, brown and off-white, and only Nagoji wears ochre. In 1.5 Nagoji is in the foreground and Keshavrao two men ahead.
30. **1.5, the hand at the hip and the ambiguous guard.** APPLIED, in a different form. The slack wrist chain is specified. The guard walks alongside the line at the gap between the two men, but does not fully screen Keshavrao, because that would hide the hilt-hand plant.
31. **5.3, the memory costume.** APPLIED. Long uncut hair, bareheaded (as in the novel), white angarkha and sash, a sheathed sword, a bay horse rather than a black mare, and the Portuguese only as smoke. The style reference now points at Chapter 1 panel 6.5, not "the mare".
32. **3.1, Goan period detail.** APPLIED. Lime-washed laterite, tile roofs, balconies and oyster-shell panes; Catholics with a rosary and veils; merchants in turbans and angarkhas.
33. **3.4, sailors could be drawn as prisoners.** APPLIED. They are free lascars in shirts and head cloths, with no irons.
34. **Text-like marks.** APPLIED. João's strip has notches, the ledger is turned away, and the prayers are strokes, crosses and circles. No musical notes are drawn; the letterer may add them.
35. **4.1 and 4.5 light the hold inconsistently.** APPLIED. 4.1 now shows a small square of daylight at the top of the ladder.
36. **Full-width strips miss 300 PPI.** APPLIED. The math checks out: 369 pt is 5.125 in, and 1536 px gives 299.7 PPI. The print note now lists all ten full-width strips, requires at least 1538 px visible width, a 2x Real-ESRGAN pass before placement and a check after the crop. `compositor.dpi_gate` already enforces 300 PPI at build.

## Also fixed (not raised by reviewers)

- The pre-review draft failed `parse_script`, because `> *No text. Let the glare hurt.*` is not an allowed no-text line. Both such lines are now `> *No text.*`, with the direction moved into the shot. The revised script parses: 6 pages, 29 panels, no em or en dashes, and every prompt assembles.
- Out of scope for this chapter: similar no-text lines in chapters 3, 14, 17, 23 and 24 will probably fail the same parser check.
