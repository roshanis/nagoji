# Chapter 21 script review: reviser's disposition

Script: `scripts/CHAPTER-21-SCRIPT.md` (pre-review draft kept as `script-reviews/CHAPTER-21-SCRIPT-r1.md`).
Novel: `book1_horse_servant/book3_chapter21_ramayyans_ledger.md`. Checked against `CONTINUITY.md`, `pipeline/script_pipeline.py` (the revised script was re-parsed and every panel's cast checked with the overrides applied) and `pipeline/compositor.py`.

Result: 8 pages, 38 panels and 2 insets (target 7, range 6 to 8). 35 findings: 35 applied (5 of them with modifications), 0 rejected.

## Fidelity

1. **5.4 Pune: the rumour sentence dropped.** APPLIED. The novel's sentence is what "fear and jealousy filled the gaps" and Ramayyan's "less room to invent" answer. It is restored verbatim, including "in his mind" (panel renumbered 5.3).
2. **5.5: Revathi's three Dutch refusals cut.** APPLIED. Page 3 does plant suspicion of her, and the novel answers it directly. 5.1 and 5.2 are merged, and a new 5.5 carries the line verbatim, with Revathi ghosted in the 3.2 stain style.
3. **7.4: "warning in time" cut and "his life" has no antecedent.** APPLIED. The line is restored verbatim, and "his" becomes "the king's". The three lines fit in one panel, so no extra beat was needed.
4. **Page 6: Ramayyan's self-doubt ("lines on leaves") cut.** APPLIED (modified). The exchange is restored as a new 6.4. Merging 6.2 and 6.3 as proposed would have put about 60 words in one panel once finding 6 was added, so the panel was freed another way: "fools or tyrants" and "I am tired" now share 6.5, with the tired smile in an inset.
5. **3.4: the finger is not on the Velinadu line, and "Leverage: significant" is cut.** APPLIED. The novel is exact on both points. The draft's letterer note also sat inside the speaker label ("LEAF (letterer: ...)"), and the parser splits at the first colon, so the note would have been lettered into the art. The note now lives in the adaptation notes.
6. **6.2: "let you go ... same reason" cut.** APPLIED (modified). The line is verbatim in the novel and shows Ramayyan weighing both ways. It goes in 6.3, just before "one line in a very long text", as in the novel, so that 6.2 is not overloaded.
7. **7.3: no answer to "Why show me this?"** APPLIED. The novel's full sentence is restored, including "old men with styluses", and "Roots are harder to kill than branches" moves into 7.2 to rejoin its run.
8. **8.4: the prisoner number is missing.** APPLIED. `compositor.py` line 525 hardcodes "17   prisioneiro marata", so the left page now matches it exactly.
9. **Page 8: the historians/spider verdict cut.** APPLIED (modified). One compressed caption goes on the quiet 8.3 night panel. "Him" becomes "Ramayyan", because after "Of the king's own" the pronoun would have pointed at the king.

## Craft

10. **4.5 inset leaf is unletterable, and the panel is crowded.** APPLIED. The leaf is fully open with the cover board coming down at the inset's edge, and old 4.3 is merged into 4.2 so that the loyalty panel (now 4.4) gets the height.
11. **8.1 and 8.2 lack flashback treatment, and "That night" is ambiguous.** APPLIED. Both panels now share 7.5's stain-edged borders and warm palette, and 8.3 uses the novel's "after the ground had dried".
12. **7.4: "his" reads as Nagoji.** APPLIED. It now reads "the king's life" (same fix as finding 3).
13. **Page 1 is overbooked.** APPLIED. 1.4 and 1.5 are merged into one two-shot, and 1.1 is cut down to the squall, the barrels, the plan board and Nagoji.
14. **5.5 ends on a resolved statement.** APPLIED. Page 5 now ends on Ramayyan's gaze lifting and sharpening on Nagoji, after the Revathi line, which follows the novel's order. The look is removed from 6.1.
15. **7.2 staging jump, and 7.3 has no action.** APPLIED. Nagoji steps back from the door into the lamplight, and Ramayyan's eyes drop to the Goa brand.
16. **3.3 and 3.4 run the action backward.** APPLIED. 3.3 is now a still, flat leaf, so the order is read, pause, hide.
17. **1.3 "no dust" caption duplicates the art.** APPLIED. It is cut; the swept, dust-free floor and the seated man are drawn instead.
18. **7.5 caption narrates the shoulders.** APPLIED. It is trimmed to "I saw him not by his face." The upright silhouette does the rest (and matches finding 32).
19. **8.1 has two focal actions.** APPLIED. 8.1 is the knife and the clamping forearm only. The fall is shown in 8.2 as its result: the king sitting up, the oil smear and the broom in the oil.

## Continuity

20. **5.4 Pune casts Nagoji onto the kneeling captain (blocker).** APPLIED. The parse returned ['nagoji'], as the reviewer said. The description now says "the narrator", the override is [], the sardar, astrologer and captain are dressed in Maratha dress, the captain has a grey-flecked beard, and the star chart becomes a blank kundali leaf.
21. **Names in LEAF copy pull faces into inserts.** APPLIED. The claim was confirmed by parsing. Overrides are set for 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 and 8.4, and those panels are marked "hands only" or "no figure, no face".
22. **Festival flashback casts a full Nagoji.** APPLIED (modified). 7.5 and 8.2 say "the narrator is not in frame" and take the override ["varma"]. 8.1 takes [] instead of ["varma"], because the king appears there only as a sliver of bare side; with the sheet attached, the model could add his face to a tight grapple.
23. **8.3, 1.1 and 4.4 casts are wrong.** APPLIED. 8.3 is "Nagoji alone" in "the estate courtyard". Overrides are set for 1.1, 8.3 and old 4.4 (now 4.3). An override is also added for 1.3, where "my garden" would attach Nagoji's sheet to a shot from his point of view.
24. **Two-shots have no screen direction and look alike.** APPLIED. Nagoji is on frame left and Ramayyan on frame right in every two-shot, each man is tagged each time, and 6.1 puts Nagoji crouched across the table.
25. **The full ch17-27 row brings in the knife, bandages and coat.** APPLIED. Every Nagoji panel carries a ch21 tag reading "no knife, no bandages, no coat".
26. **LEAF panels conflict with outlined reserves, and foreshortened leaves.** APPLIED. Every leaf is flat and square to camera, with a counted number of empty bands and fingers in the margin. The compositor and prompt gap is flagged in the adaptation notes for the pipeline owner, since this is a script-only revision.
27. **4.5 inset has no letterable surface.** APPLIED. The leaf is fully exposed with two bands, the board and its shadow stay at the top edge, and the LEAF line is split into two chunks (same fix as finding 10).
28. **4.3 asks for village names on the tags.** APPLIED. Old 4.3 is merged away; the shelf hand now appears in 4.3 (old 4.4) with "abstract impressed marks, no script".
29. **1.2 cloth over the topknot may read as a turban.** APPLIED. It is now a loose rain hood held in one hand, with the topknot visible beneath and the cloth not wrapped.
30. **3.4 finger and underline placement.** APPLIED. The fingertip is in the margin beside the upper band, and the strokes run under the right-hand third of the lower band only (same fix as finding 5).
31. **4.1 De Lannoy's coat is under-specified.** APPLIED. It now uses the chapter 18 wording: a cotton coat over a European shirt, white mundu, not a uniform.
32. **7.5 Varma may be aged, and the assassin is unplaced.** APPLIED. Varma is drawn younger than at the dedication, with dark hair bound back. The lean assassin, with a dark shoulder cloth, stands two steps from the king in silhouette.
33. **8.2 guards undressed.** APPLIED. They are Nair palace guards with forward topknots, bare chests, hitched mundus, curved swords and round shields, and no turbans.
34. **8.1 "clamps his wrist" is ambiguous.** APPLIED. It now reads "clamping the assassin's knife wrist". The fall is moved to 8.2 (same fix as finding 19).
35. **8.4 ledger number and style.** APPLIED. The left page reads "17   prisioneiro marata" and is lettered in chapter 1's Georgia Italic ledger style, not in a DIN reserve (same fix as finding 8).
