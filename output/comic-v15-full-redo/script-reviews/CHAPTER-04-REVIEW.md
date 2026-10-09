# Chapter 4 script review, reviser's disposition

Script: `scripts/CHAPTER-04-SCRIPT.md` (pre-review draft kept as `script-reviews/CHAPTER-04-SCRIPT-r1.md`).
Checked against `book1_horse_servant/book1_chapter04_fishermen_of_the_pepper_coast.md`, `CONTINUITY.md`, the novel's later brand passages (ch5, ch8, ch9, ch17, ch20), the ch2, ch3, ch5 and ch6 V15 scripts, the V13 Nagoji concept sheet, and the pipeline parser and compositor.

Result: 6 pages, 29 panels. 31 findings: 30 APPLIED, 1 REJECTED. The revised script parses cleanly with `parse_script` and contains no em or en dashes.

## Fidelity

1. **4.2, "may be useful" cut.** APPLIED. The novel gives this line in the Konkani Nagoji can follow, and it is the only offer of a future he understands. It is restored verbatim as the third balloon; "Teeth" and "Dutch" stay, so the 4.3 hook still pays off.
2. **4.5 vs 5.3, carriers reversed.** APPLIED. The novel's rebuke comes from "the man at my feet", so the Fisherman now takes the shoulders and the Young Fisherman the legs.
3. **3.1 balloons should be Malayalam.** APPLIED. The novel follows these remarks with "Malayalam ... a language I could not follow". They are now in brackets, and the last balloon of 3.5 marks the switch to Konkani.
4. **3.4, "one marata" cut.** APPLIED. The line is restored verbatim as the middle balloon, and the Wary Fisherman's reply moves to the top of 3.5 to make room.
5. **6.4, resolve line cut.** APPLIED, with a change. Both sentences are kept verbatim, because "more than that" has no referent without "chance and stubbornness". The storms caption moves to 6.3, and 6.4 becomes a full-width tier, so neither panel is overloaded.
6. **1.2, 2.4 and 6.4 reworded.** APPLIED. "Each time I drew in air", "I recognised" and "They did not roar and crash;" are restored exactly as the novel has them.
7. **6.3, ambiguous "his shoulder".** APPLIED. It now reads "on his own left shoulder (the one established in 2.1)", which matches the novel.

## Craft

8. **Brand reveal cannot be staged on a sleeveless tunic.** APPLIED. The forearm is sand-caked or turned down in 1.2 through 2.4. In 3.1 the Fisherman scrapes the sand off with his thumb, and the 3.2 insert is the first readable view.
9. **4.5 vs 5.3 carriers.** APPLIED. Same fix as finding 2.
10. **2.5, either/or eye reflection.** APPLIED. It is now an empty-surf POV strip with foam, planks and a scrap of sail, no human figure, and at most a sliver of his cheek.
11. **5.1, contradictory camera.** APPLIED, with a change. The panel is a high wide shot, but the camera sits up among the palms looking back down the slope. A camera behind the party looking inland could not see the beach.
12. **4.4, "flat on the sand" and horse metaphor.** APPLIED. He stays propped on one elbow with his chin lifted and shoulders squared.
13. **The rope is never removed.** APPLIED. In 2.4 the Young Fisherman is putting away his knife, with the cut rope beside Nagoji, and every later panel reads "no rope".
14. **5.4 is a sequence, not a moment.** APPLIED. It is frozen to a half-smile with her gaze on the brand, the Fisherman mid-gesture; "is gone" and the three-step eye path are cut.
15. **Ten panels on one patch of beach.** APPLIED. 4.1 now opens wide on all four men at full scale, with the wreck behind them.
16. **6.5 caption 1 repeats the shot text.** REJECTED. The duplication is fixed from the art side instead: the horse-trader clause is removed from the shot description (finding 25). The caption is a verbatim novel line that carries Nagoji's horseman reading of the look, which is interiority, not a description of the art.
17. **2.1 cannot show costume in a supine POV.** APPLIED. 2.1 establishes faces, hair, beards and head-level identifiers only; the full costume is established in 2.4.

## Continuity

18. **Brand invented as a cross on the left upper arm (blocker).** APPLIED in the script. The brand is now on the left inner forearm, a hand's width above the wrist, drawn as raised ridges blurred past reading, with no letters and no cross. This matches the bible's ch7-16 row and the novel's ch17 ("my left wrist ... ridged letters"). It is inner rather than outer because Padmini "turned it upward". NOT DONE HERE: CONTINUITY.md's ch4 row still says "upper arm", and the pipeline copies that row into every ch4 Nagoji prompt. That row and ch5 script 1.1 must be amended before generation, and both are flagged in the script notes.
19. **Three fishermen indistinguishable.** APPLIED, with a change. Each man has a fixed tag carried into every panel he appears in, and the cast inside the house on page 6 is stated. The lungis are plain dyed colours (madder red, indigo, off-white) rather than the suggested checks, to avoid a later-period kaili look.
20. **4.5 vs 5.3 carriers.** APPLIED. Same fix as finding 2; 5.1 and 5.3 name the Fisherman at the shoulders.
21. **Beards bleeding onto Nagoji.** APPLIED. A clean-chin tag is added to every panel that shows his face, and 1.3 now reads "faint stubble shadow at most, no beard".
22. **Irons vanish unexplained.** APPLIED, with a correction. "No irons, manacles, chain or collar" appears in every full-figure panel, the chafe rings are at the ankles only, and the wrist bandages are slipping. The V13 captivity sheet does not actually show ankle irons; the risk comes from the bible's ch1-3 row and the ch3 art. The optional snapped-cuff bridge is not adopted, because it risks the model drawing irons on him; it is left to the author.
23. **Rope never removed; burns hidden by the tunic.** APPLIED. The rope is cut in 2.4, the loops sit under the armpits well clear of the neck, and the tunic is torn open down the front from 1.2.
24. **6.5 scar unreadable.** APPLIED. The camera is low from the mat, with his anatomical left cheek toward camera and warm hearth light on it. Daylight only rims his shoulders, the Young Fisherman stands behind him for scale, and there is no coat.
25. **"Horse" in shot text (4.4, 6.5).** APPLIED. Both shot descriptions are now horse-free; 6.5 reads "a slow, appraising look".
26. **Turban and beard not in the bible.** APPLIED as a flag. The ch4 script keeps the look and asks for the bible's Ibrahim entry and the ch5 and ch6 scripts to carry it. Those files are outside this reviser's scope and were not edited.
27. **Healer reads as Padmini; anachronistic blouse.** APPLIED. She is heavier-set, with a low grey knot, betel-stained lips, no gold, no stick and undyed cotton with no fitted blouse, and the village women are modestly draped. Padmini is deliberately not named in panel text, because the parser would then attach her bible look; the warning sits in the notes.
28. **Wreck position and ship identity.** APPLIED. 2.4 shows the black, high-sided ch2-3 ship with its carved stern castle and snapped mainmast, heeled on an offshore reef. 5.1 shows it far off on its reef, with the ship's boat on the sand.
29. **3.1 sides and palms undefined.** APPLIED. The Young Fisherman is at his RIGHT, turning up the right hand (only the fingers are bandaged; the heel of the palm is calloused and rope-burned). The Fisherman is at his LEFT, handling the left forearm.
30. **6.3 cloth ambiguity.** APPLIED. Same fix as finding 7.
31. **Frames below 300 PPI after crop.** APPLIED, with a correction. The print note now requires the strips and the 3.2 insert to be generated at their final ratio, with 3.2 as its own close-up. Every frame goes through `dpi_gate`, frames below 150 PPI are regenerated rather than upscaled twice, and `verify_pdf` must pass at 300 PPI or more. The full-bleed width is 6.125 in (the 441 pt media box), so a full-width panel needs about 1,840 px, not 1,875.

## Reviser's own fix

- The draft did not parse: the 6.2 letterer note came after the panel copy, and `parse_script` raised "Unattached prose after panel copy". The note now sits in the page 6 introduction, where the parser ignores it and it stays out of the image prompt.
- The parser will infer Ibrahim into 5.4, 6.1, 6.2 and 6.3, because "kapitan" appears in their copy. The script notes ask for cast overrides so that he appears only in 6.5.
