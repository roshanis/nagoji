# Chapter 12 script review: The Shadow from Arcot

Pre-review draft: `script-reviews/CHAPTER-12-SCRIPT-r1.md`. Revised script: `scripts/CHAPTER-12-SCRIPT.md` (r2). New file: `scripts/CHAPTER-12-CAST-OVERRIDES.json`, the visible cast of all 40 panels.

Result: 8 pages, 40 panels (range 6 to 8). 34 findings: 34 applied (4 of them in part or adapted), 0 rejected outright. Every finding was checked against the novel, CONTINUITY.md and the pipeline code (`script_pipeline.infer_cast`, `compositor.fit_clip_contain`) before it was applied.

## Fidelity

1. **Page 4, 4.3, Shenkottai exchange (major).** APPLIED. The novel stages it as dialogue and "we paid in gold and blood" is Ramayyan's; now Nagoji's question and Ramayyan's verbatim answer are off-panel balloons under one caption.
2. **Page 7, 7.1, Nagoji's admission (major).** APPLIED. "I knew Raghuji Bhonsle was ambitious and that Chanda Sahib had made enemies" is restored verbatim; the Peshwa clause is cut because Varma has said "The Peshwa's war" in 6.3.
3. **Page 8, 8.3, lost key line (major).** APPLIED. "Without knowing it" and "One man's capture becomes another man's freedom" are restored verbatim; the notes only ever meant to cut "One kingdom's loss".
4. **Page 4, 4.1 and 4.2, open-ground chase (major).** APPLIED. 4.1 now holds a ravine mouth in broken ground with Nair musketmen while the riders refuse it, and in 4.2 Dhanaji gestures at that ground, so the art shows the land fighting for them.
5. **Page 3, 3.1, the Dutch line (minor).** APPLIED. The full line is in 3.2 and sets up "two fronts" in 8.4. "Every rupee" moves to 3.3 with the novel's "to Chanda Sahib" restored, because "him" would now point at the king. "Tribute buys time" moves over the Aramboli lines in 3.4 to balance the page, and "Sometimes his generals" is restored in 3.1.
6. **Page 8, 8.2, the irony caption (minor).** APPLIED, placed in 8.1 rather than 8.2. There it plays against the men watching him ("my people's victory"), and 8.2 stays at 28 words instead of 53, above the heaviest panel in any other V15 script.
7. **Page 4, 4.5, misquote (minor).** APPLIED. It is now fully verbatim ("Men might think I was a spy, or worse, a lever they could use to bargain...") and preceded by "I did not know how the war would end."

## Craft

8. **Page 4, 4.1, caption describes the panel (major).** APPLIED. The caption is now the place tag "Near Nagercoil." and "We spoke of it afterward..." stays. Dhanaji is named in 4.2 with "Dhanaji admitted it.", taken from the novel's "he admitted", rather than the invented "said it plainest".
9. **Page 4, 4.5, flat page end (major).** APPLIED, adapted. A clay oil lamp (finding 30) has no shutter, so Nagoji pinches out the wick, and the rampart goes dark above Ramayyan and Dhanaji talking in a lit doorway.
10. **Page 7, talking heads (major).** APPLIED, adapted. In 7.2 Varma lowers the ola from the lamplight; holding it over the flame would read as burning the dispatch, which the novel does not have. In 7.3 Nagoji stacks coins from a tray now planted in 5.3, which also shows what a pagoda is. In 7.4 Ramayyan tucks the ola away with the sea beyond.
11. **Page 8, 8.5, flat closing caption (major).** APPLIED. The chapter ends on the sand line, and the walk back to the fires carries "There was still work to do". The notes give the author the option of a silent narrow strip if the line must be lettered.
12. **Page 1, 1.4 and 1.5 (minor).** APPLIED. "From there he looked south" is cut, and 1.5 now carries the whole sentence, keeping the novel's colon: "He saw what every ambitious man saw: pepper, ports, and a king...".
13. **Page 4, 4.3, "where the passes met the plains" (minor).** APPLIED. The clause describes the drawn view.
14. **Page 8, 8.1, captions narrate the reactions (minor).** APPLIED in part. "Some looked at me with new respect" becomes "As if my people's victory was somehow mine." The second caption keeps "Others wondered what other secrets I kept", because the suggested "Or as if I kept other secrets" implies the suspicion is baseless, and page 4 shows he did keep one.
15. **Page 7, 7.1, "I chose my words carefully" (minor).** APPLIED. The measured performance carries it, and the close-up drops to 37 words.
16. **Adaptation notes, print (minor).** APPLIED. The note now requires 300 effective PPI or more for every placed image and lists all eight full-width panels (1.1, 1.5, 2.5, 3.4, 4.3, 4.5, 7.5, 8.5).

## Continuity

17. **Page 1, 1.3, Chanda Sahib drawn as Nagoji (blocker).** APPLIED. Confirmed by running `infer_cast`: the cast was ['nagoji']. The override is now [], and he is dressed in a beard, white jama and cream turban, "no red turban and no red sash".
18. **Page 1, 1.1, Raza and Nagoji injected (blocker).** APPLIED. Confirmed: the cast was ['nagoji', 'raza']. The costume line no longer names anyone, the override is [], and the notes are corrected: Raza's lancers serve Travancore from chapter 7, which is earlier, not later.
19. **Page 8, 8.3, Nagoji in irons (blocker).** APPLIED. Confirmed: the cast was ['nagoji']. The panel is now vision only with override [], the captive is dressed apart from Nagoji and matches the 1.3 rider, and the Maratha officers wear white angarkhas and pagdis with no red sashes.
20. **Page 4, 4.1 and 4.2, Dhanaji undressed (major).** APPLIED in part. His look is written into 4.1, 4.2 and 4.5, with "only Nagoji wears the rust-red turban". CONTINUITY.md is not edited because it is shared by all chapters and its hash is recorded by the chapter 1 pilot package; the line is proposed in the adaptation notes for the author to add.
21. **Page 4, 4.1, "the enemy horsemen from 1.1" (major).** APPLIED. Each prompt stands alone, so the riders' costume is restated in the panel.
22. **Pages 5 to 7, chiefs undressed (major).** APPLIED. Nair chieftains are bare-headed with a front topknot, white mundu and gold earrings, with no turbans, in 5.3, 6.2, 6.4, 6.5, 7.3 and 7.5. Nagoji is now the only turbaned man in the hall.
23. **Page 3, 3.4 and page 4, 4.3, landscapes gain principals (major).** APPLIED. Confirmed: the casts were ['nagoji'] and ['nagoji', 'ramayyan']. Both overrides are now [], and 3.4 has a timber palisade with firing loopholes on the earthen rampart.
24. **Page 6, 6.4, Varma's "I/my" adds Nagoji (major).** APPLIED. Confirmed: the cast was ['nagoji', 'varma']. The override is now ["varma"].
25. **Page 1, 1.4, terraced slopes (major).** APPLIED. Pepper on jackfruit and areca trees in homestead gardens, "no terraces, no plantation rows".
26. **Page 1, 1.2, European-style letter (minor).** APPLIED. It is now a rolled Persian letter in a brocade kharita with a lac seal.
27. **Page 2, 2.1, boots on temple steps (minor).** APPLIED. His boots are off and set below the bottom step, and the shrine is Kerala-style with no gopuram.
28. **Pages 2, 4 and 8, undressed Maratha riders (minor).** APPLIED. White angarkhas, white pagdis, bamboo lances and no red sashes in 2.5, 4.4 and 8.3.
29. **Page 5, 5.1 and page 8, 8.1, guards, soldiers and courier (minor).** APPLIED. The courier wears a plain cotton head cloth and a dusty cream tunic rather than a white turban and jama, which would read as Maratha white. The nodding and suspicious men in 8.1 are both Nairs, so "my people's victory" stays clear.
30. **Page 4, 4.4, lamp and rampart (minor).** APPLIED. A clay oil lamp, an open wick dish, on the laterite parapet of a Travancore fort.
31. **Page 5, 5.5 and page 7, 7.3, the king unnamed (minor).** APPLIED. In 5.5 Ramayyan turns to Varma on the dais instead of looking up; 7.3 says "toward Varma, who is off-panel".
32. **Page 6, 6.5, camera position (minor).** APPLIED. Over Varma's shoulder, with Nagoji small at the far end and the chiefs leaning out of the line.
33. **Page 7, 7.5, the spear appears from nowhere (minor).** APPLIED. It is planted in 5.3, leaning against the dais at his right hand.
34. **Adaptation notes, print pixel math (minor).** APPLIED in part. The 1536 px (299.7 PPI, fails) and about 2172 px (about 424 PPI) figures check out. The "3:1 source is height-limited above about 174 pt" claim does not: `fit_clip_contain` letterboxes a source that is wider than its slot, so height governs only when a source is narrower in aspect than its row, and the note says that.

## Checks run

- `parse_script` parses the revised script: 8 pages, 40 panels, contiguous numbering, and no em or en dashes in the script or the overrides file.
- `assemble_prompt` builds all 40 prompts with the overrides, and the override keys match the 40 panel ids exactly.
- Every copy sentence was compared with the novel. The only sentences not found verbatim are the compressions carried over from r1, the place and time tags, and "Dhanaji admitted it."
- The heaviest panel is now 44 words (8.1), within the range of other V15 scripts. Page 4 (173 words) and page 8 (159 words) are the densest pages, because the fidelity restorations landed there.
