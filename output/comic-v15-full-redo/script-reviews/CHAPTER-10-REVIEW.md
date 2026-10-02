# Chapter 10 script review, round 1

Pre-review draft: `script-reviews/CHAPTER-10-SCRIPT-r1.md`. Revised script: `scripts/CHAPTER-10-SCRIPT.md` (9 pages, 45 panels; unchanged count).

Each finding was checked against the novel (`book1_horse_servant/book2_chapter10_lessons_in_travancore.md`), CONTINUITY.md and the V15 pipeline (`pipeline/script_pipeline.py`, `pipeline/compositor.py`).

Result: 38 findings. 38 applied (7 of them in part, with the rejected part explained), 0 rejected outright.

## Fidelity

| # | Where | Verdict | Reason |
| --- | --- | --- | --- |
| 1 | 6.3 thesis line | APPLIED (in part) | The thesis is the chapter's argument and Nagoji's reply depends on it, so it is restored. Its setup line was folded in ("For the Maharaja, conquest...") so the panel stays at 42 words and does not reach 58. |
| 2 | 7.4, 7.5 hinge | APPLIED | Checked against the novel. The "borrowed eyes" payoff now carries 7.4, and "A campaign in Travancore did not always mean a pitched battle." plus the verbatim lancers line carry 7.5. |
| 3 | 9.1 sullen silence | APPLIED | This is the only moment Nagoji acknowledges the losing side. It replaces the Malayalam line, which the art already shows. |
| 4 | 4.2, 4.3 order | APPLIED | The novel runs scowl, then retort, then order, then volley. The retort moves to 4.2, and 4.3 has no balloon. |
| 5 | 4.1 market, "here" | APPLIED | The novel has this exchange at the market. 4.1 is staged at the market's edge and "here" is restored. |
| 6 | 2.3 misquote | APPLIED | "Carries him" did read as the priest. "Temple roof" and "carries the idol" are restored. |
| 7 | 1.2 teaching line | APPLIED | It is cheap and sets up "That was the first lesson" in 7.3. The panel has room. |
| 8 | 9.3 to 9.5, 3.4 threads | APPLIED | The 9.3 time captions are merged, the compressed Velinadu itinerary is added, 9.5 gains the palace and a distant lit hall, and 3.4 gains "Not much older than Revathi Bayi." |

## Craft

| # | Where | Verdict | Reason |
| --- | --- | --- | --- |
| 9 | 6.1 overload | APPLIED (in part) | 6.1 is cut to the quartet (33 words). "If you ride only on the training field..." was cut rather than moved, because 6.3 now carries the restored thesis. Its point returns verbatim at 7.1. |
| 10 | 6.4 overload | APPLIED (in part) | The family and chieftains sentence is cut. "He has been at war since before he took the throne" opens 6.4 (35 words) and does not close 6.3, which is already full. |
| 11 | Page 6 static | APPLIED | 6.3 adds Nagoji stopping to look back while Ramayyan turns. 6.5 adds Ramayyan tapping and tucking away the palm-leaf bundle. The page drops from about 220 to 184 words. |
| 12 | 4.1 overload | APPLIED | Nagoji's question and "As often as I can" are cut. 41 words. |
| 13 | 8.4, 8.5 outcome shown early | APPLIED | The chief's sword stays belted, with his hand on the buckle, so the 8.5 caption now carries the outcome. |
| 14 | 3.5 double eyeline | APPLIED | One eyeline, to the Dutch factor. Ramayyan and Nagoji are in the foreground and the scribe's pen inset is kept. |
| 15 | 4.3 retort in the volley | APPLIED | Resolved together with #4. |
| 16 | 4.5 flat ending | APPLIED | The page ends on the Dutch drums. 6.1 carries the "many rhythms" idea. |
| 17 | 6.2 caption repeats art | APPLIED | The trim is taken as proposed. 38 words. |
| 18 | 7.5 broken fragment | APPLIED (in part) | The fragment is replaced, via #2. The lancers clause is kept because the "fifty Maravar" number and the menace are information the art cannot give, and the line is verbatim. The levy is shown by an empty cart instead. |
| 19 | 8.1 "We took his walls at dawn." | APPLIED | 8.2 and 8.3 show it, and the charge now lands unannounced. |
| 20 | 2.5 list duplicates art | APPLIED | The balloon is trimmed to its first sentence. The houses it listed are drawn, with the #26 staging. |
| 21 | 3.1 glossary weight | APPLIED | The "five hundred pounds a sack" aside is cut. 37 words. |

## Continuity

| # | Where | Verdict | Reason |
| --- | --- | --- | --- |
| 22 | 300 PPI print rule (blocker) | APPLIED (in part) | A Print bullet is added, as the user asked. It states the 300 PPI minimum, the 369 pt art column and the 1538 px need, the 2x upscale path, the panels at risk, and a DPI-REPORT check. Rejected part: the compositor places every panel inside the 369 pt art column, not 441 pt full bleed, so the 1875 px figure does not apply. The pipeline also takes one frame per panel, so insets are drawn inside their panel's frame, not generated as separate frames. |
| 23 | Nagoji facial lock | APPLIED | The pipeline already injects CLEAN-SHAVEN CHIN whenever Nagoji is cast. It is still spelled out in 1.2, 2.2, 4.4, 7.2 and 9.1 and in the Art bullet, because Chapter 1 drifted to a beard. |
| 24 | 1.5 temple-priest sheet | APPLIED | The sheet is dropped for the whole chapter. The officiant is set small, deep in the sanctum, with a lamp tray, and Ramayyan is described apart from him in the same panel. |
| 25 | Boots and sword in the temple | APPLIED | Boots and talwar are left at the steps in 1.4, and he is barefoot through 2.5 and on the 9.1 mat, following the Chapter 9 precedent. |
| 26 | 2.5 caste staging | APPLIED | Correct for 1740s Travancore, where temple entry came only in 1936. Nair-house worshippers stand inside, and the fisherman and labourer hand oil across the outer gateway. |
| 27 | Yusuf's look | APPLIED | His look now matches Chapters 18 and 23: white skullcap, trimmed dark beard, no scar. The negative clause is removed. Ibrahim gets his Chapter 4 white turban and grey-flecked beard. |
| 28 | Ibrahim scar, Ramayyan identifiers | APPLIED (in part) | The anatomical-left scar is now turned to camera in 5.2, 5.3 and 5.5. Rejected part: the pipeline already injects each named character's CONTINUITY block, including Ibrahim's scar and Ramayyan's look, so a separate cast header is not needed. Instead, every panel now names the characters it shows. |
| 29 | Scribe unanchored | APPLIED | The scribe's desk is set beside Yusuf's stall in 3.1, he is placed at the end of Yusuf's table in 3.3, and his look is specified. The inset is drawn inside the 3.5 frame. |
| 30 | 3.5 two eyelines | APPLIED | Same fix as #14. |
| 31 | 4.3 line of fire | APPLIED | The rank is side-on, firing to off-panel right. The drill master is at the flank, clear of the muzzles, and Ramayyan and Nagoji are behind the line. |
| 32 | 6.2 fort below versus above | APPLIED | The novel has the fort above them. 6.2 now shows only the edge of its wall at the top of the frame. |
| 33 | 9.4 brand and scar | APPLIED | Chapter 9 (5.2, 11.3, 11.4) draws both marks. 9.4 now shows the Chapter 4 crude cross with no lettering, plus the long white scar, and the adaptation note is corrected. |
| 34 | Period coats | APPLIED | The factor and the drill master are both in 1740s dress. The drill master has grizzled dark hair so he cannot read as De Lannoy. |
| 35 | Gopuram | APPLIED | Rewritten as a Kerala gateway with a laterite base, a two-tiered sloping roof and no stone tower. |
| 36 | The two forts | APPLIED | The coastal fort is laterite with no European flag. The far-bank fort is a whitewashed Dutch bastion with a plain banded flag, no monogram, matching Chapter 11. |
| 37 | Stallholder costume | APPLIED | Plain undyed cotton, no gold, no jasmine, simple knot. The Cast overrides bullet also stops the pipeline from attaching Revathi's look, since 3.4 now names her. |
| 38 | Chieftains and lancers | APPLIED (in part) | The chieftains are distinct: heavy-set in red-bordered cloth at 7.5, lean and grey in white at 8.4. The lancers follow Chapter 7. Rejected part: red shoulder cloths for every lancer, because that is Ponnan's personal identifier. |

## Found while verifying (not raised by reviewers)

- The pipeline infers cast from any name or first-person pronoun in a panel's description or copy. That would have attached absent characters' looks: Padmini in 2.2 and 9.3, Ibrahim in 3.3, Revathi in 3.4, De Lannoy in 4.2, Ramayyan in 7.4, the Senior Rani in 8.1 (via "Attingal"), and Nagoji in 3.3, 3.4, 9.2 and 9.5. A "Cast overrides for `prepare`" bullet now lists them. The phrase "our right as he faces us" was removed from the Ibrahim descriptions, because "us" was adding Nagoji to 5.1 and 5.3.
- The revised script parses cleanly with `parse_script`: 9 pages, 45 panels, no em or en dashes. The heaviest panel is 9.3 at 45 words.
