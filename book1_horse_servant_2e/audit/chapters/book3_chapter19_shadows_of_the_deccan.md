# Second-Edition Audit: Chapter 19, Shadows of the Deccan

- Source (frozen first edition): `book1_horse_servant/book3_chapter19_shadows_of_the_deccan.md`, 275 lines, 2,882 words (2,875 by `scan_slop.py`).
- Method: I read the whole chapter with line numbers and ruled on all 80 flags from the pattern auditor and all 23 suspect passages from the holistic reader, merging duplicates. I cross-checked against Ch 1 L7 and L63, Ch 3 L137 and L185 to 211 (Keshavrao's death), Ch 8 L33 and L129, Ch 16 L151 and L319, Ch 17 L139 and L153 to 175 (the naming), Ch 18 L23, L239 to 269 (Ibrahim's news, Ramayyan's "bring it to me", the dust on the wind), Ch 22 L196 to 229 (the chaver), Ch 25 L46, L104, L130 and L186, Ch 27 L7, the glossary, STYLE_SHEET.md, VOICE_BIBLE.md (T11, C5), REGISTER_AND_ANACHRONISM.md, REPETITION_AND_DENSITY.md, OPENINGS_ENDINGS_MOTIFS.md and REVIEW_BACKLOG.md. Line numbers refer to the first-edition file.
- I checked the cut figure and the fixes by assembling a scratch version of the chapter (in `$TMPDIR`, not in the repo) with every confirmed fix and the leaned borderline choices, then running `scan_slop.py` on it against the original.
- Quotation marks in the fixes are straight. The source uses curly quotes except L131 (see Chapter notes); the 2e typography pass will settle them.

## Verdict

| Measure | Call |
|:-|:-|
| Severity | **4 of 5** |
| Recommended intensity | **Deep**, in the narration only. The dialogue needs a light touch; the brother's letter needs almost none. Line-level re-voicing is needed in the opening (L3 to 11), the king's scene narration (L95 to 117), the aftermath (L141 to 149), the night vigil (L175 to 193) and the gate scene through the end (L239 to 275). |
| Estimated word cut | **About 37%** (2,882 to about 1,805 words on the scratch assembly). `scan_slop.py` core hits fall from 83 to 31, and style-sheet excess from 29 to 1 (the 1 is a letter salutation the fragment heuristic miscounts). |

This chapter has two voices. In dialogue and in the brother's letter it is some of the best writing in Part III. The brother (sky versus Peshwa, "offended if the sea had kept you", the mispronounced name) is VOICE_BIBLE touchstone T11. Padmini reads a stranger by his gait and appetite, the king likes the joke and then threatens a "very narrow river", Revathi has an "impatient" tongue and a "root" jab, and the sowcar angles for a bigger fee. In narration, Nagoji keeps turning into a modern novelist explaining him to himself. That shows up as a storm-simile opening with a correction, fragment lists, "Not a report. Not a record. A story.", a title-drop kicker, "expiry date", "asset" and "risk", a sleepless-night nocturne, a "These hands had..." litany, "stop pretending that the man who failed him still existed", the river conceit eight times, and five endings in thirty lines. REPETITION_AND_DENSITY ranks it third densest in the book (28.9 hits per 1000 words).

The 37% cut is far above the PLAN's 5 to 10%, so I checked it for over-cutting. No scene, plot beat, historical fact or line of the brother's letter is lost. About three quarters of the cut is the same point made again. The renunciation is stated at L191, L193, L215, L221, L237, L247, L253, L259, L271 and L273. There are family catalogues at L115, L185 and L245, hands passages at L179 to 187 and L251, and "the sea took him" at L49, L215 and L259. The opening preamble (L3 to 11) and the coda (L265 to 275) make up most of the rest. If the author wants a gentler pass, the Flab table lists texture that can be restored without bringing any slop back (for example the toddy-drinking caravan guard at L7).

The chapter depends on two continuity decisions, and several fixes below assume them. First, Keshavrao's death must match Ch 3 (rope torn out through his hands, empty hatch; backlog N-39). Second, the brother's name must be settled (Ramji at L199 and Bhalerao at L213, the latter colliding with Book 3; backlog N-38).

## Confirmed issues

| Line | Quote | Category | Suggested fix |
|:-|:-|:-|:-|
| 3 to 5 | "News from the Deccan arrived the way monsoon storms do. / Not as a single, clear front, but as a series of clouds that thickened until you realised the sky had changed." | correction / modern_register / motif | Cut both paragraphs and open on L13 (see **Opening**). "Front" is a 1919 weather term, the correction is the chapter's first move, and STYLE_SHEET keeps the storm image for Ch 13. |
| 7 | "Sometimes it came in letters ... Sometimes it came as gossip ... Sometimes it came in the eyes of a man ..." | tricolon | Cut. The "bought or trusted" either/or goes with it. (The details are good; the Flab table notes where one could be restored.) |
| 9 | "Sand, horse, fort, Dutch. The Deccan had receded to the edges of my waking mind, surfacing only at night in dreams of black soil and dry wind." | fragment_list / stock_phrase | Cut. Move the paragraph's first idea, trimmed, to L55: "Since Goa I had trained myself not to look north too often; the work here had needed all of me." |
| 11, 13 | "Then a letter arrived with my village's dust still clinging to it." / "as she often did" | stock_phrase / kicker | Fold the dust into L13 as a physical fact, and drop "as she often did": "Padmini found me in the shade of the jackfruit tree and tossed a small bundle into my lap. The cloth was grey with the dust of the Deccan roads." (It keeps the bridge from Ch 18 L269, the dust on the wind "carrying the Deccan toward this coast". Road dust is also more believable than "my village's dust" on a packet that has crossed half the country.) |
| 15 | "her voice softer than usual" | stock_phrase | Cut the tag. "my son" carries the softness. |
| 17 | "My fingers trembled slightly as I unwrapped the cloth." | soft_adverb | "I unwrapped it." |
| 29 | "The world here turns as it always has and yet not." | kicker | Cut. It is the one oracle line in the brother's letter. |
| 31 | "New chiefs rise. Old ones fall." | balanced_antithesis | Cut these two sentences. The rest of the paragraph stays. (Chapter notes, item 9, has an optional historical replacement.) |
| 33 to 35 | "He wrote of local matters too. / A neighbour's death. A cousin's marriage. A new well ... the villagers now treated it like a miracle." | fragment_list | "He wrote of a neighbour's death and a cousin's marriage, and of a new well that had struck water after so many dry attempts that the village now made offerings at it." |
| 37 | "Then, near the end, a single line that made my chest tighten." | stock_phrase / signposting | "Near the end he had written:" |
| 41 | "The words blurred for a moment." | stock_phrase | Cut. |
| 43 to 45 | "We heard a tale. / Not a report. Not a record. A story. Yet stories carry their own weight." | correction / fragment_list / kicker | Cut both paragraphs. This is the chapter's worst hot spot (REPETITION_AND_DENSITY scores it 6.0). |
| 47 | "the moment the line went taut and then snapped free. Keshavrao's face, eyes wide, mouth open, vanished under a wave." | continuity / stock_phrase | "I felt the rope again, burning out through my palms and over the rail, and saw the empty hatch where his face had been." (Ch 3 L201 to 211: the rope "peeled my skin and vanished over the side" and he stared at "the absence where his face had been". The rope did not snap, and he did not see the face go under.) |
| 49 | "I had known, in my bones, that the sea had kept him. Seeing the shape of the tale written in my brother's hand pressed that knowledge into ink." | explained_subtext | Cut. The flash at L47 carries it. |
| 55 to 59 | "I sat for a long time with the letter in my hands. / ... Somewhere, a pot clanged. / Deccan names wrapped themselves around Travancore sounds ... as if two different songs were playing at once." | stock_phrase / simile | "I sat with the letter in my lap for a long time. Since Goa I had trained myself not to look north too often; the work here had needed all of me. Now the estate went on around me, women calling across the yard, boys shouting in the kalari, and I found I was putting it all into Marathi in my head." (Keeps the two-worlds idea as something he catches himself doing, not a simile about it.) |
| 61 | "When I finally folded ... Padmini was still there, watching from a respectful distance." | stock_phrase | "When I folded the letter and tucked it into my belt, Padmini was still there." |
| 67 | "It was not a question." | stock_phrase | Cut. It is a book-wide tic (backlog C18-05, six uses), and the flat line shows it is not a question. |
| 79 to 81 | "Her words should have steadied me. / Instead, I heard Ibrahim's voice from the day the Dutch came bowing ..." | other (transition formula) | "I heard Ibrahim again, from the day the Dutch came bowing: the wind blows in circles, and names travel." ("Dangerous combination" was never going to steady him, so the formula is also illogical. The callback itself is deliberate and stays.) |
| 87 to 89 | "We sat not in the crowded war hall, but in a smaller room off to the side ... / He held my brother's letter in his hand." | correction / POV | "The king received me in a small room off the war hall, its walls lined with shelves of palm leaves and a few cloth-wrapped volumes that had once been Portuguese property. He read my brother's letter through before he spoke." (This also fixes "He", which grammatically points to the runner.) Insert the Ramayyan line from Chapter notes, item 4, before it. |
| 95 | "The king smiled faintly, then let the expression fade." | stock_phrase | Cut. |
| 97 to 101 | "He tells you that your homeland has heard of me ... None of that surprises me. The Maratha confederacy is a storm with many centres." | dialogue_exposition / modern_register | Replace L97 to 101 (including Nagoji's "Yes.") with: "Your former master's court argues about me," the king said. "Your brother writes of quarrels and shifting banners. None of that surprises me. What interests me is this." ("Maratha Confederacy" is a 19th-century British label, and the storm is a second storm image. "Your former master's court" is kept because it is a small needle from the king.) |
| 107 | "I thought of the men in Pune, of their hunger for land and revenue, of their pride." | tricolon | "I thought of the revenue clerks in Pune, who could price a kingdom by its villages." |
| 113 | "The words landed like weights on the mat between us." | simile | Cut. |
| 115 | "I thought of my father, his back bent over a plough. Of my mother ... Of my brother, sitting by lamplight ... Of Deccan forts ..." | tricolon / repetition | "I thought of my brother at his lamp, tongue between his teeth as he wrote to me, and of the Deccan forts where I had first learned to count men and cannon." (The catalogue repeats at L185 and L245. The plough also contradicts Ch 8 L33; see Chapter notes, item 5.) |
| 117 | "building a new kind of state because the old kinds were crumbling under European pressure." | modern_register | Cut the paragraph. It is a historian's thesis, and it misreads the king, whose wars in these years were mainly against local lords and rival houses. |
| 119 | "I would read the letter," I said slowly. "I would weigh it. I would remember Goa. I would remember the storm. I would remember Colachel. Then I would choose." | tricolon / soft_adverb | "I would read the letter," I said. "I would remember Goa, and the storm, and Colachel. Then I would choose." (The content stays; only the six-fold drumbeat goes.) |
| 133 | "His gaze sharpened." | stock_phrase | Cut. |
| 137 | "He waved a hand, dismissing the solemnity with a flick." | explained_subtext | "He waved a hand." |
| 141 | "When I left the room, the air outside felt thicker." | stock_phrase | Cut. It belongs to the style sheet's "air was thick" family. |
| 143 | "The shadows of the Deccan had lengthened into Travancore's corridors." | kicker (title drop) | Cut. |
| 147 | "Not mistrust exactly. More calculation." | correction | Cut. |
| 149 | "my usefulness now had a clear expiry date. As long as I pointed my gaze and my horse south and west ... I was an asset ... I would become a risk." | modern_register / geography | Replace L145 to 149 with one observed incident: "In the days that followed, some men looked at me differently. The next time I rode north, the clerk at the river ferry, who had always waved me through, asked my business and wrote the answer on a leaf." (It shows the watching that Ch 21's ledger and Ch 25's test pay off. It also removes "south and west", which points into the sea.) |
| 151 | "Padmini, as always, cut through the fog with a single remark." | stock_phrase | Cut. Move the tag into L153: "... forever," Padmini said, as we watched men load supplies for a northern fort. |
| 167 | "a playful glint entering her eyes that softened the hard truth of her words." | explained_subtext | "She leaned back against the carved pillar." |
| 171 | "It was said in jest, but the wall was there, invisible and ancient." | explained_subtext / vague depth | "It was said in jest. Revathi's letters to Padmini were the same, all levies and Velinadu rights; she never named worry, but she folded it into the way she asked whether the king's new walls were worth the men they ate." (This relocates the best sentence of L265 to a place where it characterises her instead of trailing the ending.) |
| 173 | "That impatient tongue was right. I could not stand in two rivers." | kicker | Cut. It also credits Padmini's river line to Revathi. |
| 175 to 177 | "That night, I did not sleep. / ... watching the moon trace its slow arc over the coconut palms ... the rhythmic croak of frogs ... the distant bark of a village dog." | stock_phrase | "That night I sat on the verandah of my quarters until the frogs in the irrigation channels went quiet." |
| 179 | "Now I studied them as if seeing them for the first time." | stock_phrase (kill list) | Cut this sentence only. The two before it are protected. |
| 181 | "These hands had held Maratha reins ... held a dying chaver's wrist while a king drove steel through his throat." | tricolon / continuity | Cut. It is VOICE_BIBLE counter-example C5, the chaver is a Ch 22 event told before it happens (backlog RV-01), and in Ch 22 L223 to 229 Nagoji cuts the throat, not the king. "A rope that broke" contradicts Ch 3. |
| 183 | "Whose hands were they now?" | kicker (rhetorical question) | Cut. |
| 185 | "I thought of my father's hands ... Of my mother's hands ... the stone *sil-batta* ... Of my brother's hands, ink-stained ..." | repetition / register | "I thought of my mother's hands at the grinding stone before dawn, keeping time with her prayers." (The brother's lamp is used at L115. *Sil-batta* is the Hindustani word; a Marathi kitchen has the *pata-varvanta*, and "grinding stone" avoids the choice.) |
| 187 | "They did not know the man those hands had made me ... rode north to raid Portuguese forts ... That man had been simpler. He had known which rivers were his." | kicker / geography | "At home they remembered a son who had ridden down to the Konkan to take Portuguese forts and had not come back." (From Nashik the Konkan forts lie west and south, down the ghats.) |
| 189 | "Somewhere in the black water off this coast, Keshavrao's bones lay tangled in Portuguese wreckage. He had followed me. He had trusted me. And I had let go." | tricolon | "Keshavrao's bones lay in the black water off this coast, among what was left of the Portuguese ship. He had come up that ladder behind me because I told him to, and the rope had gone out through my hands." (The guilt stays; see **Defended**.) |
| 191 | "I could not bring him back. But I could stop pretending that the man who failed him still existed." | balanced_antithesis / modern_register | Cut. It is therapy language, and STYLE_SHEET 4 says he does not narrate his own growth. |
| 193 | "arrived not as a thunderclap but as a settling, like silt finding the riverbed after a flood. I had been fighting the current for years. Now I would let it carry me." | correction / motif | Cut. The night ends on Keshavrao and the rope, and "The next morning, I went to the market" shows the decision. |
| 195 | "a Gujarati *sowcar*, a money changer whose networks of trust ran deeper than any royal decree." | modern_register / stock_phrase | "to the stall of a Gujarati *sowcar* whose *hundis* were honoured as far north as Pune." |
| 197 | "It was gold, borrowed from Padmini Amma's private vault. A debt I would repay with service, or blood." | kicker / register | "It was gold, borrowed from Padmini Amma's strongroom against my pay." |
| 201 | "his eyes widening slightly at the heft" | soft_adverb | "The trader weighed the pouch in his palm." Keep the rest of the line. |
| 205 | "He nodded, a flicker of respect in his gaze." | stock_phrase | "He shrugged and wrote out the note of credit, his hand steady." (The shrug concedes the haggle.) |
| 211 | "by a dying lamp" | stock_phrase | "I had written it the night before. It was short." |
| 215 | "The sea that took Keshavrao took him too, in a different way." | explained_subtext | Cut this sentence. The letter's other lines stay. |
| 219 | "Forget his name. Remember his love." | balanced_antithesis | Cut. The letter ends on "It is the last debt he owed you.", which is plainer and harder. |
| 221 | "It was a lie. And it was the truest thing I had ever written." | kicker | Cut. |
| 227 | "I walked back to the fort feeling lighter, as if I had cut a heavy pack from my saddle." | explained_subtext / continuity | Cut. L229 becomes "When I reached the estate, Padmini was waiting by the gate ...". (He lives at the estate, L175 to 177, not the fort.) |
| 239 | "She nodded slowly, her eyes searching mine." | stock_phrase | Cut. |
| 243 | "I tasted the air, heavy with pepper and sea salt. It no longer tasted foreign." | kicker | Cut these two sentences. Keep the chain and the roof (see **Ending**). |
| 245 to 247 | "For a moment, I felt the pull of two currents, the dry wind of the Deccan ... at war in my chest for years. / Now, standing at this gate, I let one of them go." | simile (mixed) / repetition | Cut. Currents that are winds, a wind that smells of hands, and a third family catalogue. |
| 249 | "Not forgotten. Never forgotten. But released, the way you release a horse too old to ride, with gratitude and grief, with the knowledge that holding on would only make both of you suffer." | correction / modern_register | Keep the horse and drop the frame and the gloss: "In the Deccan, when a horse grew too old to ride, we turned it out to graze with thanks and did not go back to look at it." (It echoes the letter's "Do not look for him" without saying so.) |
| 251 to 253 | "I looked at my scarred hands one last time ... that had somehow found their way ... They would not change. The scars would remain. But the name attached to them could." | abstract_depth / tricolon | Cut. |
| 257 | "The name felt strange on my tongue, new and stiff like unconquered leather. But it fit. Ananthan, the endless one ... Pillai, the suffix that marked me as Padmini's son ..." | explained_subtext / repetition | Cut. Ch 17 L153 to 175 already gives the meaning of Ananthan and the name settling "strange and familiar at once". "Unconquered leather" is a misword, and "his bones" slips out of first person. |
| 259 | "The man I had been, Nagoji Sawant, died in the black water with Keshavrao. The sea had just taken longer to tell me." | kicker / continuity | Cut. This is the third death site for "Nagoji" (the letter says Colachel, L237 says the market). |
| 261 | "Padmini Amma smiled, an expression that cracked the iron mask she usually wore." | stock_phrase | "Padmini Amma turned for the house." (The iron-mask cliché, OPENINGS_ENDINGS_MOTIFS 5, also contradicts a Padmini who has called him "my son" and waited at the gate for him.) |
| 265 | "I knew its outward words would be correct and cool ... but somewhere between them there would be a line that cut deeper." | stock_phrase / structure | Move the last sentence to L171 (above) and cut the rest of the paragraph. |
| 267 | "lodged itself like a small, dangerous hope." | simile | Cut. See **Borderline** for an optional plain version. |
| 271 to 275 | "The Deccan son was gone. Another man, with two coasts in his chest, had taken his place. / The Travancore soldier had finally arrived. / For the moment, that was enough." | summary_ending | Cut all three paragraphs. End on L269 (see **Ending**). |

**Confirmed total: 65 rows**, merged from the 80 pattern flags and 23 holistic passages. The L47 and L189 rulings reverse the pattern auditor's reading of which lines contradict Ch 3. Items neither auditor raised are in **Borderline** (L53 against Ch 18) and **Chapter notes** (items 6, 9, 10 and 13).

## Borderline

These are judgment calls. My lean is given in each row. The scratch assembly took every lean.

| Line | Quote | Ruling |
|:-|:-|:-|
| 23 | "Nagoji anna," | Marathi families do use *Anna* for an elder brother, but *Dada* is the common word around Nashik, and most readers of a Travancore novel will hear "anna" as Malayalam or Tamil. Lean: "Nagoji Dada," but it is the author's call (REGISTER P3). |
| 39 | "Do you remember Keshavrao, who sat in the cell with you near the coast before they took you away?" | The clause reminds the reader rather than the brother. Lean: "Do you remember Keshavrao, who was taken with you?" Keep the rest of the paragraph intact. |
| 53 | "They argue over whether it was luck or craft." | Ch 18 L239 has Ibrahim say almost the same thing ("Some men call it luck. Some call it warning. Some say..."). Lean: cut this sentence. Keep both "Some say" sentences, because the king taps the second one at L103. |
| 65 | "Which is the only kind that travels far." | An aphorism on demand, but it is dry and Nagoji's own, and it plants "names travel" for L81. Lean: keep. If the chapter still feels epigrammatic after the cuts, drop it and let "Mixed," stand alone. |
| 77 | "Dangerous combination." | Modern clipped idiom, and it pins a label on what she has just repeated. Lean: cut. "Sharp and divided," she said. is weightier alone. |
| 81 | "from the day the Dutch came bowing" | A wink at the previous chapter's title. Lean: keep. It is Nagoji's own name for the day. |
| 123 | "Because I am not arrogant enough to think I know what the world will look like when that letter arrives," | A modern hedge. Lean: "Because I do not know what the world will look like when that letter arrives," I said. "If it arrives." |
| 139 | "There is still Dutch paper to manage" | "Manage" is on the watch list. Lean: "to answer". See Chapter notes, item 10, on "Mysore greed". |
| 161 | "Do not let that flattery blind you to the fact that neither will mourn very long if they must cut you loose." | Over-articulated for Revathi. Lean: "Do not let that flattery blind you. Neither will mourn you long if they must cut you loose." |
| 217 | "to keep the creditors from the door" | Optional: "to keep the *sowcar* from the door". It echoes the man carrying the gold and names the village moneylender a Deccan farmer would actually fear. |
| 223 | "sealing the transaction with a stamp of red wax" | A hundi was a signed note, not usually wax-sealed. Lean: "pressing his seal into the red wax on my letter". |
| 243 | "I looked at the red tiled roof of the *tharavadu* that had sheltered a king and now sheltered me." | A neat parallel, but a concrete one that carries the Ch 17 cellar story. Lean: keep, merged with the chain (see **Ending**). |
| 249 | the horse image | Lean: salvage it as in the confirmed fix. The minimal alternative is to cut L243 to 253 entirely and go straight from "Then who stands before me?" to "Ananthan Pillai," I said. Both work. |
| 267 | "The thought that my new name might one day be spoken in her halls ..." | It is Nagoji's only line of hope before the Ch 20 marriage. If the author wants it, keep it plain and after the Revathi scene, not at the gate: "I did not tell her that I had already imagined my new name spoken in her halls." Lean: cut. Revathi's own "too much hope" already plants it. |

**Borderline total: 14.**

## Defended (flagged, but keep)

| Line | Quote | Why keep |
|:-|:-|:-|
| 31 | "Some say the Maratha hand is strong. Others say each finger pulls in a different direction." | Flagged as Some/Others symmetry. It is the brother's farm-dry political sense, and the hand-and-fingers image is fresh. It stays. |
| 53 | "Some say we should send men to learn. Some say we should conquer him before he grows too strong. ... even if they mispronounce it." | The king taps the conquest line at L103, and the mispronunciation pays off in Ch 25 L130. Only the "luck or craft" sentence is borderline. |
| 119 | "I would remember Goa ... the storm ... Colachel. Then I would choose." | The content is a careful subject stalling before a king, and "You do not say which way" answers it. Only the anaphora is trimmed. ("The storm" here is the wreck's name, which OPENINGS_ENDINGS_MOTIFS allows.) |
| 135 | "we will stand on opposite sides of a very narrow river" | Understated royal menace. The river conceit is kept in dialogue twice (here and L153) and cut from narration four times (L173, L187, L193, L245). |
| 153 | "You cannot stand with one foot in each river forever ... which current to let carry you." | OPENINGS_ENDINGS_MOTIFS names this the one home of the river motif. With the narration echoes gone, it lands. |
| 157 | "Then you drown slower," she said. "But you still drown." | Flagged as epigram ping-pong. It is Padmini's blunt register and her best line in the chapter. |
| 165 | "No," she said. "I have an impatient one." | A witty correction, and a correction in dialogue is the one the style sheet allows. It is also the chapter's only one after the cuts. |
| 189 | "And I had let go." (the guilt) | The pattern auditor called this a contradiction of L47 and L181. It is the other way round. In Ch 3 L205 to 207 the rope was torn out through his hands, so his guilt at "letting go" fits Ch 3, and L47 and L181 ("snapped", "broke") are the lines that are wrong. Keep the guilt; the confirmed fix only removes the three-beat cadence. |
| 201 | "Roads have bandits. Bandits have hunger." | A merchant angling for a carrying fee, answered by a soldier who knows how a hundi works. This is trade texture, not theme. |
| 215 | "The man known as Nagoji died at Colachel. Do not look for him. He fights battles that are no longer yours." | This third-person death notice is the chapter's event and a step on the book's name spine (OPENINGS_ENDINGS_MOTIFS, summary point 6). With L259 and L271 to 275 cut, the chapter no longer contradicts where he "died". See Chapter notes, item 7, on Ch 25. |
| 223 | "My word is iron." | A generic boast, but it earns Nagoji's dry "See that it is." |
| 235 to 237 | "And the man who wrote it?" / "He stayed at the market," I said. "He is not coming back." | Flagged as staged. It is the right kind of indirection: two people who both know what the letter said and will not say it. |
| 241 | "Then who stands before me?" | Flagged as allegorical. Keep it. In Ch 17 the name was given to him by Padmini, Ramayyan and the king. This is the first time he claims it himself, and her question gives him the chance. It works once L243 to 261 stop answering it for him. |
| 255 | "Ananthan Pillai," I said. | Same reason. It is new as an act, even though the name is not new. That is why L257's "new" and the etymology have to go and this line stays. |
| 263 | "Welcome home, Ananthan Pillai," she said. "Dinner is ready. Do not make us wait." | Flagged as a stock homecoming line (REGISTER P3 offers "Come in ... The rice is served"). "Welcome home" is old English usage, and here it does the theme's work in two words before Padmini deflates it into household routine. Keep. "The rice is served" is a fine alternative if the author wants a less Western meal word. |

**Defended total: 15.** One pattern ruling covers several of these. The pattern auditor's "epigram dialogue" complaint (L65, L77, L157, L165, L201) is fixed by removing the narrator's glosses around the lines (L151, L167, L171, L173) and one weak label (L77), not by flattening the speakers. Each of Padmini, Revathi, the king and the sowcar keeps one sharp line.

## Opening

Current first lines (L3 to 11):

> News from the Deccan arrived the way monsoon storms do.
>
> Not as a single, clear front, but as a series of clouds that thickened until you realised the sky had changed.
>
> Sometimes it came in letters ... Sometimes it came as gossip ... Sometimes it came in the eyes of a man ...
>
> For a long time after Goa and the storm ... Sand, horse, fort, Dutch. ...
>
> Then a letter arrived with my village's dust still clinging to it.

**Verdict: rewrite.** Both auditors agree, and so does OPENINGS_ENDINGS_MOTIFS (row 19). It is 167 words of throat-clearing with a storm simile, a correction, a triple anaphora, a fragment list and a psychological summary, and nothing happens until L13. OPENINGS_ENDINGS_MOTIFS proposes "My brother's letter came south wrapped in cloth, with our village's dust still in the folds." That is serviceable, but it is still summary. The chapter's best observed detail is Padmini's reading of the messenger, and it should come first.

**Proposed** (in scene, about 30 words before Padmini speaks; the dust keeps the bridge from Ch 18's last line):

> Padmini found me in the shade of the jackfruit tree and tossed a small bundle into my lap. The cloth was grey with the dust of the Deccan roads.
>
> "From your hills, my son," she said. "The boy who brought it walked like a man used to stones, not sand. He eats too fast. That is how I know he comes from a place where grain is a worry."
>
> I unwrapped it.

Continue at L19 unchanged. The one idea from L9 worth keeping (he had trained himself not to look north) moves to L55, after the letter, where it explains why the letter hits him.

## Ending

Current last lines (L259 to 275):

> The man I had been, Nagoji Sawant, died in the black water with Keshavrao. The sea had just taken longer to tell me.
>
> Padmini Amma smiled, an expression that cracked the iron mask she usually wore.
>
> "Welcome home, Ananthan Pillai," she said. "Dinner is ready. Do not make us wait."
>
> As I stepped through the gate, I caught sight of Revathi's latest letter ... whether the king's new walls were worth the men they ate.
>
> The thought that my new name might one day be spoken in her halls as easily as in this courtyard lodged itself like a small, dangerous hope.
>
> I followed Padmini inside.
>
> The Deccan son was gone. Another man, with two coasts in his chest, had taken his place.
>
> The Travancore soldier had finally arrived.
>
> For the moment, that was enough.

**Verdict: revise** (cut and tighten; the right last line is already on the page). The chapter ends five times (L259, L263, L269, L271 to 273, L275). The last closer is the "For the moment ... enough" formula the style sheet bans, and it shares its closing idea with Ch 16. L271 and L273 contradict each other ("two coasts" against "the Travancore soldier"), and the Deccan is not a coast. Everyone who has looked at this chapter agrees the end is L269 (OPENINGS_ENDINGS_MOTIFS row 19, VOICE_BIBLE end table, backlog C10-35, both auditors). The run-up from L243 to L261 also needs cutting, because it answers Padmini's question four times before Nagoji answers it once.

**Proposed** (replaces L239 to 275; about 110 words; ends on an action):

> "Then who stands before me?" she asked.
>
> I touched the silver chain at my neck and looked up at the red-tiled roof of the *tharavadu* that had sheltered a king and now sheltered me. In the Deccan, when a horse grew too old to ride, we turned it out to graze with thanks and did not go back to look at it.
>
> "Ananthan Pillai," I said.
>
> Padmini Amma turned for the house.
>
> "Welcome home, Ananthan Pillai," she said over her shoulder. "Dinner is ready. Do not make us wait."
>
> I followed her inside.

The best sentence in the coda (Revathi's worry folded into "whether the king's new walls were worth the men they ate") is not lost. It moves to L171, where it replaces an explanation.

## Flab

| Lines | Issue | Action |
|:-|:-|:-|
| 3 to 11 | 167 words of preamble on how news travels before the letter appears. | Open on L13 (see **Opening**). If the author misses the texture, the one detail worth restoring is the caravan guard "who had drunk too much toddy at a wayside stall". It could go into L55 as a second channel he had stopped listening to, but only as a clause, not a "Sometimes" paragraph. |
| 37 to 49 | Keshavrao's death is re-dramatised against Ch 3 and then processed four ways (blur, echo, correction, "in my bones"). It is stated again at L181, L189, L251 and L259. | Keep the brother's paragraph (L39) and one corrected sensory flash (L47). Keshavrao comes back once more, at L189, and nowhere else. |
| 55 to 61 | A stillness beat, an ambient-sound list and an explained simile. | One paragraph (confirmed fix at L55 to 59). |
| 95 to 117 | The king recaps the letter; Nagoji gets an abstract triad, a simile, a family montage and a historian's thesis before he answers. | The confirmed fixes keep every exchange and cut about 140 words of stage business. Backlog C10-34 asks to cut L107 to 127 to two exchanges. I disagree: the exchanges themselves (L109, L111, L121 to 127) are the scene. The flab is only the narration between them. |
| 141 to 149 | Aftermath exposition that tells how men looked at him, in balance-sheet words, with a title drop. | One observed incident (the ferry clerk). |
| 151 to 173 | Two advisers deliver "you must choose", then the narrator restates it (L173) and glosses both women (L151, L167, L171). | Keep all the dialogue and cut every gloss. Revathi's scene becomes about flattery and marriage, with the relocated letters sentence. |
| 175 to 193 | The night vigil recaps the book (Goa chains, the rope, wet sand, the chaver), repeats the family catalogue, and narrates the decision in therapy language and river imagery. | Keep the nails, one image of his mother, one line about how home remembers him, and one sentence of Keshavrao. About 316 words become about 130. The market scene shows the decision. |
| 211 to 227 | Kickers around the letter: "dying lamp", the explained sea metaphor, "Forget his name. Remember his love.", "a lie ... the truest thing", "feeling lighter, as if". | Five cuts; the letter itself stays. |
| 239 to 261 | The gate scene answers "Then who stands before me?" with a sensory triad, two currents, a correction, the fourth hands passage, a gloss of the name and a third death site. | See **Ending**: the chain, the roof, the horse, the name. |
| 265 to 275 | Four closing beats after the natural end. | Relocate the L265 sentence; cut the rest. |

## Passages to protect

- L15: "The boy who brought it walked like a man used to stones, not sand. He eats too fast. That is how I know he comes from a place where grain is a worry." (the new chapter opening)
- L19 to 21: "a folded piece of paper, not palm leaf" and "My younger brother's, grown more angular since I had last seen it."
- L25 to 27, entire (VOICE_BIBLE T11): "I would have been offended if the sea had kept you. This land needs you more than salt does." ... "Father says the sky is more unreliable than the Peshwa. I am not sure which is the greater insult."
- L31: "Our forts still stand, but their banners change more often. Some say the Maratha hand is strong. Others say each finger pulls in a different direction."
- L35 (inside the merged sentence): the new well that struck water after so many failed attempts.
- L39: "There are many boys and many names. Stories change as they travel. I do not know if this is true. I only know that when I heard it, I thought of you and the sea."
- L53: "your new king's name has reached our hills, even if they mispronounce it." (paid off at Ch 25 L130)
- L69 to 73: "For now." / "They grow sharper," I said. "And more divided."
- L91 to 93: the king liking the joke, and "He does not have to face either directly ... That makes jokes easier."
- L109: Nagoji's answer about Pune ("If they think you are useful, they will keep you as you are").
- L115 (clause): "tongue between his teeth as he wrote this letter".
- L127: "I prefer honest answers to pious lies."
- L131 to 139: the king's "Understand this, Ananthan" speech, the "very narrow river", "For whatever that is worth", and "The north will have to wait its turn."
- L153 to 157: Padmini's river and "Then you drown slower ... But you still drown."
- L163 to 169: "You have a cruel tongue." / "I have an impatient one." / "Even ones who think they have found a root."
- L179 (first two sentences): the nails "grown back, but wrong, ridged and discoloured ... I had stopped noticing them months ago."
- L199 to 209: the sowcar exchange, including "Your paper is worth more than gold on the road. Do not tell me otherwise."
- L215 to 217: the letter, less its explaining sentence, ending on "It is the last debt he owed you." ("new seed" answers the parents' quarrel over seed at L27.)
- L229 to 237: "She looked at my empty hands, then at my face." through "He is not coming back."
- L263: "Dinner is ready. Do not make us wait."
- L265 (last sentence, relocated): "she folded it into the way she asked whether the king's new walls were worth the men they ate."

## Chapter-specific notes

1. **Keshavrao's death (L47, L181, L189; backlog N-39).** Ch 3 L201 to 211: the rope goes taut, "the line took the wrong kind of weight", "The rope peeled my skin and vanished over the side", and he stares at "the absence where his face had been". So in Ch 3 the rope did not snap, he did not see the face go under, and the rope went out through his own hands. The confirmed fixes bring L47 and L189 into line, and L181 is cut. Ch 16 L383, Ch 24 L621 and Ch 25 L130 ("Keshavrao's face as the rope slipped from his grasp") need the same check in their own audits.
2. **Premature callback (L181; backlog RV-01).** The chaver fight is in Ch 22, and there Nagoji cuts the throat while the king pins the man (Ch 22 L196 to 229). Cutting L181 settles it. If the author wants one line of hands in its place, VOICE_BIBLE C5 offers "I closed the left hand as if on Kanka's reins; the thumb the Portuguese had worked on still would not lie flat." That line spends the chapter's one "as if", and it depends on the Kanka continuity decision (OPENINGS_ENDINGS_MOTIFS 7).
3. **The brother's name (L199, L213; backlog N-38).** Gold goes "To the house of Ramji Sawant" and the letter is addressed "To Bhalerao Sawant". Neither is identified. Bhalerao reads as a surname, and it is the name of Book 3's narrator (Dhanaji's son). The simplest reading is that Ramji is the father, as head of the house. Suggested: L199 "To the house of Ramji Sawant, my father." and at L213 the brother's own first name, introduced once at L21 so the reader has it ("My younger brother's, [name]'s, grown more angular ..."). Author's choice of name.
4. **Ramayyan's instruction is dropped (Ch 18 L261).** Ramayyan told him, "When the first letter comes, bring it to me." Nagoji does not, and by dusk the palace knows. One added line after L85 turns this into the chapter's surveillance beat and makes L145 to 149's telling unnecessary: "Ramayyan had asked me to bring him the first letter that came from the north. I had not yet gone to him. Someone had gone for me."
5. **Does his father plough? (L27, L115, L185; backlog N-22.)** Ch 8 L33 has "My father's house has held the sword for five generations. We do not plough." L27 (fields, seed, the sky joke) is protected, so change Ch 8, as the backlog proposes ("We hold the sword and the plough both"). The confirmed fixes here drop the plough at L115 and the father's "plough and sword" hands at L185 anyway.
6. **Is this the first letter from home? (Missed by both auditors.)** Ch 16 L151 says "since my family faded into letters that grew shorter each year", which means letters were already arriving. Ch 8 L129 ("fields that do not know whether I am alive") and this chapter ("We heard from a trader that you did not drown") both say they were not. Fix Ch 16 L151, not this chapter.
7. **The three renunciations (OPENINGS_ENDINGS_MOTIFS 6.4) and Ch 25.** OPENINGS_ENDINGS_MOTIFS suggests Ch 19 for the family (private), Ch 22 for the frontier and Ch 25 for the Maratha state. Under that split the letter at L213 to 217 is fine as written, because it speaks to his family ("battles that are no longer yours"). What overreached were the narrator's claims that the whole Deccan self was gone (L259, L271, L273), and those are cut. Ch 25 L46 has a Bhonsle sardar write "you did not die in the sea as some said", and Ch 25 L186 has Ramayyan say the burned reply makes him "silent to them". Both still work, since the state never received the family letter. The holistic reader suggests softening the letter to "do not wait for me". I do not recommend it: the death notice is the stronger scene and the split already protects Ch 25.
8. **The naming was already done (L255 to 257; Ch 17 L139 to 175).** Padmini chose "Ananthan" for "the serpent on which Lord Padmanabha rests", Ramayyan added "Pillai", the king used it, and it "settled on me like a second skin, strange and familiar at once". Revathi teased it at Ch 17 L195. The king uses "Ananthan" at L131 here. L257's etymology, "strange", and "new" repeat Ch 17 and are cut. L255 stays because saying it himself is the new act. The holistic reader is right that "suffix" is a grammarian's word, and that Pillai is a conferred Nair title rather than a mark of adoption. Both points disappear with the cut.
9. **Baji Rao and Chimaji Appa (optional; also raised in the Ch 12 audit, note 13).** Baji Rao died in April 1740 and Chimaji Appa, Nagoji's own commander (Ch 1 L7), in December 1740. A letter from Nashik written after Colachel would almost certainly say so. If the author wants it, it can replace the cut "New chiefs rise. Old ones fall." at L31 with something literal: "The old Peshwa is dead, and Chimaji Appa, whom you served, died the same year. The new Peshwa is his son, and young, and the old chiefs do not like taking orders from him." Verify the dates and Balaji Baji Rao's standing with the older sardars first. This changes what Nagoji knows (Ch 6 L191 has him vowing to find Chimaji again), so it needs one line of reaction and is an author decision, not a slop fix.
10. **"Mysore greed to watch" (L139).** In 1741 to 1742 Mysore did not border Travancore. Its neighbours to the north were Kayamkulam, Chempakassery, Thekkumkur, Cochin and the Dutch, and the book itself calls Mysore "still half rumour" at Ch 27 L7. Suggest "and Kayamkulam to watch", which also sets up Ch 22's Kayamkulam frontier. Verify. The letter's "quarrels with ... men in Mysore" at L31 is fine, since the Marathas were active in Karnataka.
11. **Geography.** L149 "south and west, toward Dutch and Mysore" points into the sea; both lie north. L187 "rode north to raid Portuguese forts" is wrong from Nashik, where the Konkan forts lie west and south down the ghats. (Ch 1 L63 calls them "northern forts", which is the Portuguese view of their Província do Norte, and may be where "north" came from.) Both lines are removed by the confirmed fixes.
12. **Register and terms, collected:** "front" (L5), "Maratha confederacy" (L101; also Ch 21 L207 and Ch 25 L144), "state ... European pressure" (L117), "expiry date", "asset", "risk" (L149), "networks of trust" (L195), "private vault" (L197), "suffix" (L257), "Dangerous combination" (L77), "not arrogant enough to think" (L123), "manage" (L139), *sil-batta* (L185). All are handled above. *Sowcar* is the glossary's spelling (glossary L18), so keep it for consistency; *savkar* would be Nagoji's own word, but that is a book-wide decision. *Karyakkar* (L201) is still missing from the glossary (backlog FM-10).
13. **Hundi mechanics (L201 to 223).** Once the hundi is written, the gold stays with the sowcar and his correspondent pays out at Nashik. The letter's "Use this gold" (L217) is therefore loose; "Use this money" is exact. It is minor and optional. The wax is covered in **Borderline** (L223).
14. **Continuity with Ch 18 (L53, L81).** L53 repeats Ibrahim's "luck" and "Some say" from Ch 18 L239 (see **Borderline**). The L81 callback quotes Ch 18 L247 accurately enough. REPETITION_AND_DENSITY counts "the wind blows in circles" as a deliberate echo; keep it once here.
15. **Mechanical items.** L131 uses straight double quotes while the rest of the chapter uses curly. Apostrophes are mixed (L197 "Amma’s", L265 "Revathi’s"). The brother's letter (L23 to 53) is set in roman, while Nagoji's letter (L213 to 219) is in italics; pick one convention. The chapter has "red tiled" (L243) against "red-tiled" (L251) and "cloth wrapped" (L87). Narration alternates "Padmini" and "Padmini Amma". No em dashes are present in the source (checked).
16. **Cross-chapter tics to police.** "It was not a question." (L67; six uses book-wide), "He studied me." (L125; also Ch 8 L35, kept here as the chapter's one use), "landed like" (L113), "as if seeing them for the first time" (L179; also Ch 28 L127), "found their way to this" (L251; also Ch 28 L211), the iron mask (L261; also Ch 17 L11, Ch 17 L127, Ch 20 L103), and "For the moment, that was enough." (L275; Ch 16 L439 "That was enough for now."). All of these are cut or kept once by the fixes above.
