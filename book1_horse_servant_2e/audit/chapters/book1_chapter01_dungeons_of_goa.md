# Chapter 1 Audit: Dungeons of Goa

Source: `book1_horse_servant/book1_chapter01_dungeons_of_goa.md` (first edition, frozen; 113 lines, 1,941 words of prose). Line numbers refer to that file.

Adjudicated from two independent reports: a pattern auditor (67 line flags) and a holistic reader (27 suspect passages, 14 protected passages). Duplicates are merged into single rows. Every flag was checked against a full read of the chapter and against the project's own references: `STYLE_SHEET.md`, `VOICE_BIBLE.md` (touchstones T1 and T2 and section 6b quote this chapter), `OPENINGS_ENDINGS_MOTIFS.md`, `REGISTER_AND_ANACHRONISM.md` and `REVIEW_BACKLOG.md`. I also checked the later chapters that quote this one back (ch2, ch3, ch6, ch9, ch24, ch25) and the parallel Chapter 2 audit in this folder. Where a fix would have broken a callback, I rewrote it so the words that are called back survive.

## Verdict

| | |
|:-|:-|
| Severity | **3 of 5.** A noticeable pattern throughout, but not spread evenly. The dialogue core (lines 21 to 37 and 49 to 87) is mostly sound. The first page (5 to 11) stacks four hook shapes. The last page (91 to 113) reads at 5: eleven paragraphs, eight of them one sentence long, and nearly every one closes the chapter again. |
| Recommended intensity | **Medium.** Most fixes are cuts. Line-level re-voicing is needed only in the opening paragraph (7), four interior paragraphs (39, 63, 71, 73) and the ending. |
| Estimated word cut | **About 22 percent.** A scratch pass that applies every confirmed fix, the leaned borderline choices and the proposed ending takes the chapter from 1,941 to 1,521 words (see the appendix). That figure includes about 40 words of optional additions; without them the cut is about 24 percent. |

This is well above `PLAN.md`'s 5 to 10 percent, for two reasons. The cut falls almost entirely on narration: the exchanges between Duarte, João and Nagoji lose only tags and one speech clause each. And about a fifth of the removed words are commentary that restates something the scene has just shown (19, 45, 55, 57, 63, 89, 95 to 101, 109 to 111). Outside the blocks listed under Flab, the edit is word swaps.

Scanner counts (`scan_slop.py`), first edition, then after the fixes:

| Marker | 1e | After | Ration |
|:-|:-|:-|:-|
| "not X, but Y" in narration | 2 | 0 | 1 per chapter, dialogue only |
| Correction openers ("Not with...", "Not for...") | 3 (2 in speech) | 2 (both in speech) | |
| "as if" | 2 | 1 | 1 |
| "like a" similes | 1 | 0 | 2 |
| slowly / softly / quietly | 3 (+ "carefully") | 0 | 2 |
| Fragment triads | 2 | 1 (the tool inventory, defended) | 3 |
| Paragraphs ending in a short kicker | 3 | 0 | |
| One-sentence paragraphs | 13 | 7 | |
| Rhetorical questions in narration | 1 | 0 | 1 |
| "for the first time" / "something" | 1 / 1 | 0 / 0 | |

Adjudication tally: **43 confirmed**, **10 borderline**, **16 defended**.

## Confirmed issues

Fixes replace the quoted text unless marked "cut". All are in Nagoji's voice and keep every phrase a later chapter quotes back (see Chapter-specific notes, item 1).

| Line | Quote | Category | Suggested fix |
|:-|:-|:-|:-|
| 7 | "Not with ceremony or proclamation, just a shrug and an entry in a book." | correction | "A clerk took it with a shrug and a line in his book, and did not lift his head to do it." (The head the clerk does not lift sets up the Chapter 21 ending proposed in OPENINGS_ENDINGS_MOTIFS, where Ramayyan lifts his.) |
| 7 | "To the men who ruled this cellar I was no longer Nagoji Sawant. I was no longer *huzurat* cavalry ... No longer the rider of the black horse Kanka, nor the son of a landlocked village" | tricolon (anaphora) | One inventory sentence: "I had been Nagoji Sawant, *huzurat* cavalry in the service of Chimaji Appa and the Peshwa, rider of the black horse Kanka, son of a village near Nashik where the farthest water anyone feared was a swollen river in the rains." (Drops "landlocked", which the river clause already says in a villager's terms.) |
| 7 | "In the quiet of Maratha tents that word *huzurat* carried weight, the household horse that rode closest to command, picked out by sardars when bravery and impatience had been proved in more than one fight." | abstract_depth | Cut. He does not gloss his own regiment to himself. The term is in `glossary.md`, Duarte glosses it at 49 and Nagoji glosses it again at ch5:145 (REVIEW_BACKLOG C10-02). See Borderline for saving "impatience". |
| 7 | "Here I was a number the clerk scratched beside the words *prisioneiro marata*." | balanced_antithesis | "The clerk scratched a number beside the words *prisioneiro marata* and called the next man." (The Here/There frame goes. The number stays, because ch9:122 quotes it.) |
| 9 | "Above, somewhere beyond the sweating ceiling, ... Down here, the rhythm that governed us was the scrape of the gaoler's boots ... Water dripped somewhere in the darkness," | abstract_depth | "Faint through the stone came the bells of Goa's churches, ringing for evening prayers. Down here we had the scrape of the gaoler's boots, the splash of the bucket that carried away blood and filth, and water dripping in the dark, steady as..." (Simile: see Borderline.) |
| 11 | "old enough to have seen men I admired die foolishly, young enough to believe I could still choose the shape of my own death." | balanced_antithesis | End the sentence at "Konkan." Then: "I had seen men I admired die foolishly, and I still expected to die in the saddle." (Four lines later he is tied to a stool with his horse dead, and nobody needs to say so.) |
| 15 | "The padre walked carefully between the lines of prisoners, his black cassock held slightly above the slime on the floor." | soft_adverb | "The padre walked between the lines of prisoners with his black cassock held above the slime on the floor." (The cassock shows the care. ch24:311 quotes it back, so keep it.) |
| 15 | "the sort of holy man who looked built for argument, not battle. Yet the calluses on his right hand told me he had once held something heavier than a quill." | stock_phrase | "the sort of holy man who looked built for argument. Yet his right palm had the calluses a sword grip leaves." (Keeps the reversal and the calluses, which the fishermen mirror at ch4:43, and saves "quill" for Duarte's line at 85.) |
| 15 | "Here he was, deep under the Portuguese fortress at Goa, eyes moving from one ruined body to the next." | filler | "His eyes went from one ruined body to the next." |
| 17 | "My gaze stayed on him without seeming to. That habit predated the Portuguese by years." | modern_register | "I watched him without seeming to." Cut the second sentence ("predated" is an essayist's word). Optionally "As a boy in the Deccan" becomes "As a boy". |
| 17 | "Here in this cellar I turned the same skill on other men." | kicker | Cut. The paragraph ends on the sardar's hand on his hilt. |
| 19 | "He was a broad man whose belly strained his leather belt, a man who had learned to wrap cruelty in jokes." | explained_subtext | "He was a broad man whose belly strained his leather belt, and he smelled of garlic sausage and chapel incense." (Merges with the next sentence. João's jokes at 21, 35 and 53 show the cruelty.) |
| 39 | "My joints protested after so long curled under me. I bit back the groan. A Maratha horseman does not whimper in front of an enemy. We bleed, we fall, we curse the gods and get back up. On the black soil of the Deccan that had been simple enough. Here in the Portuguese darkness it took more effort." | balanced_antithesis (creed, tricolon, Here/There kicker) | "My knees had been folded under me so long that they would not straighten, and I bit down on the groan before João could hear it." (Pride aimed at one man, not a poster creed. Also removes the stock "joints protested", which ch2:15 repeats.) |
| 41 | "The interrogation chamber lay twenty paces away and felt like another world entirely." | stock_phrase | "The interrogation chamber lay twenty paces away." (The phrase is on the style sheet's kill list. The number shows he counted.) |
| 41 | "something sharp that stung the nose, a sour mixture of wine and old fear." | abstract_depth | "...to lamp oil, sweat, spilled wine and the vinegar they used to wash the floor." (The vinegar is a new detail. Any plain cleaning smell will do, and "wash the floor" implies what gets washed off it.) |
| 43 | "A brazier glowed on the far side of the room, its coals sending up a thin trail of heat that shimmered in the dim light." | filler | "A brazier glowed on the far side of the room with two irons resting in the coals." (Makes the glance at 61, "hot iron" at 65 and João's reach at 83 concrete. It can also plant the brand; see Notes, item 5.) |
| 45 | "This was where the Portuguese forged information." | kicker | Cut. "tools that had never worked metal" already made the point without the pun. |
| 49 | "The Viceroy's spies insist you were *huzurat* cavalry under Chimaji Appa himself, chosen by your sardars for your initiative." | modern_register | "The Viceroy's spies say you rode huzurat, in Chimaji Appa's own household horse." (Drops "initiative", a late-century appraisal word, per REGISTER_AND_ANACHRONISM. The gloss moves into Duarte's reason for asking. Roman type after the word's first use.) |
| 51 | "You draw lines on paper and call them borders." | modern_register | Cut. "You have maps and books. My horse does not read." The joke lands harder with one setup line, and the answer gets shorter than the question, which is how he talks (VOICE_BIBLE 3.4). |
| 55 | "They wanted to see grief; they wanted to use it as a lever." | explained_subtext | Cut, or give the reader the lever as an object: "João had the tongs in his hand and his eyes on my face." (VOICE_BIBLE C1.) |
| 57 | "“Then he died better than I will,” I said, hearing the flatness in my own voice." | explained_subtext | "“Then he died better than I will,” I said." (ch3:227 calls this line back. Protect the words, drop the tag.) |
| 59 | "You know your position. The Viceroy needs names. He needs to know if the army that devoured his northern strongholds is turning its hunger south. He needs to know if Chimaji Appa intends to bring his siege guns to Goa next. If you cooperate, your suffering can end." | tricolon (anaphora, ornamental metaphor, police register) | "“You are not a fool,” he said. “The Viceroy needs names. He needs to know whether Chimaji Appa means to bring his siege guns to Goa. Tell us, and this ends. I can speak for you, perhaps find you work on a plantation, a life in chains that is still a life. If you do not...”" |
| 61 | "His gaze flickered briefly toward the brazier." | soft_adverb | "He glanced at the brazier." (Keep the beat. It finishes the threat.) |
| 63 | "Those northern forts rose in my mind ... each fall ringing like a bell across the Konkan. Chimaji Appa followed, and with him the fear I smelled on these priests. They knew what we knew: the war was not over." | explained_subtext | "So the Viceroy was afraid for Goa itself. Any day now, I told myself, the ground above this cellar would shake under Maratha guns." (The campaign is already told at 11 and 59. "I told myself" marks it as a prisoner's hope, which is also the historical truth: see Notes, item 11. This also fixes "these priests" when only one is present.) |
| 65 | "You will try to make me scream something that fits the shapes you already have in your mind." | modern_register | "“If I do not,” I said, “you will do what you have already done to others. You will pull me apart on your ropes and put your irons to my skin until I scream whatever names you have already written down.”" (Paper and names, the chapter's own objects, in place of modern psychology. Still long enough for João's "He talks too much.") |
| 69 | "“He is a soldier,” Father Duarte said softly." | soft_adverb | "“He is a soldier,” Father Duarte said." (See Borderline for "He knows the game".) |
| 71 | "The question surprised me more than any threat could have. For an instant the dungeon vanished ... feeling that familiar tightness in my chest that was not quite fear and not quite joy." | hedged_emotion | "For a moment I was on a ridge above the Godavari again, looking down at the dust of a marching column, my chest tight the way it always was before we rode." (Keeps the ridge. The feeling gets one body beat and a job, with no double negative.) |
| 73 | "“I fight because I was born into a world where men who do not fight are trampled,” I said slowly. “I fight because if my people do not learn to meet guns with courage, someone else's flag will fly over our forts." | tricolon (speech anaphora, modern national framing) | "“I fight because men who do not fight are trampled,” I said. “As for God, Father, I leave Him to the Brahmins and to you. He seems to favour whoever has the better powder.”" (ch24:327 quotes exactly these two ideas. The flag idea returns at ch9:122, and "learn to meet guns with courage" is wrong for men who have just broken a string of Portuguese forts.) |
| 75 | "The priest's mouth twitched, a shadow of something that might almost have been a smile." | hedged_emotion | "The priest almost smiled." (One hedge instead of three. Twitching mouths are a book-wide tic: OPENINGS_ENDINGS_MOTIFS 5.2 counts 13.) |
| 79 | "For a heartbeat Father Duarte did not answer. His jaw worked, as if he chewed on words he could not swallow. Then he inclined his head, a small, weary nod," | stock_phrase | "Father Duarte was a long moment answering. Then he nodded, and João reached for the tools." (Keeps the hesitation and the nod that ch24:311 recalls, "hesitated, and nodded anyway". Removes the chapter's second "as if".) |
| 81 | "The next hours stretched and blurred." ... "Once you have felt your fingers crushed in iron and your joints forced against the way they were meant to bend, the mind floats above the body and watches priests and gaolers ply their trade." | stock_phrase | Cut the first sentence. Replace the last with "They used the ropes on my shoulders and the tongs on my fingers, and through all of it the priest stood back and watched." (ch25:248 remembers Duarte "standing just far enough back" and watching, so the watching stays. The out-of-body cliché and the plural "priests" go.) |
| 89 | "Somewhere in that haze Father Duarte said, “Enough.” ... The tired priest insisted that a dead prisoner could not testify and that the Viceroy preferred confessions on paper, not corpses." | balanced_antithesis | "At last Father Duarte said, “Enough.” João complained that the marata had still given no names, but he cut me loose." (The quill line at 85 already gave the reason. Ends on an act.) |
| 93 | "How often they changed shifts." | modern_register | "How often the watch changed." ("Shift" for a spell of work is 19th-century factory usage.) |
| 95 | "Horses, men, paces, opportunities." | fragment_list | Cut. It restates 93 and ends on an abstraction. Move "I counted, as I always had." to close paragraph 91 (see Borderline, line 91). |
| 97 | "The priest's question lingered like smoke in my mind." | simile_stack | Cut. |
| 99 | "Did I believe in anything beyond survival and the honour of my people?" | rhetorical_question | Cut. He answered it aloud at 73 (REVIEW_BACKLOG C10-01). |
| 101 | "I decided that belief did not matter in this place. Numbers did. Chains did. Ships did." | fragment_list | Cut the paragraph. It answers the question a third time and names ships before the rumour of a ship has reached him. Optional replacement that plants Keshavrao: Notes, item 3. |
| 103 | "Rumour moved through the dungeon the next day, low and cautious, like water seeping through a crack." | simile_stack | "The next day a rumour came down the wall from man to man, too low for the gaoler to hear." |
| 105 | "Not for the stake, not for the scaffold, but for transport. Somewhere far to the south the Portuguese needed labour. Somewhere beyond the horizon they were building something that required bodies that did not ask questions." | correction | "The Portuguese were gathering prisoners for a ship, and the ship was going south, where they needed men to work their land." (Matches Duarte's plantation offer at 59 and the rumours at ch2:55 and ch2:87, and leaves the destination to Chapter 2: see Notes, item 10.) |
| 107 | "for the first time since they dragged me into this fortress a thin thread of hope tugged at me." | stock_phrase | Cut. The Ending shows the hope as an act. |
| 109 | "Ships meant movement. Movement meant chances." | kicker | Cut. ch2:89 to 93 makes the same point in dialogue ("As long as we move, there is a chance." / "The sahib still counts chances."), and the Chapter 2 audit keeps it there. |
| 111 | "The Portuguese had taken my name and tried to break my body. They had forgotten the simplest lesson of the Deccan monsoon." | summary_ending | Cut. It closes the name bookend with a slogan. The proposed Ending closes it with the clerk's book instead. |
| 113 | "Storms do not ask permission." | summary_ending | Cut. It is a motto with no referent, it recurs at ch7:225, and the style sheet saves the storm for ch13:321. See Ending. |

## Borderline

The original is not wrong in these places. Each row gives the case both ways and my lean, and the author decides.

| Line | Quote | For keeping | Against | Lean |
|:-|:-|:-|:-|:-|
| 7 | "picked out by sardars when bravery and impatience had been proved in more than one fight" | "Impatience" is his dry self-portrait (VOICE_BIBLE 3.3, no. 7). | It sits inside a gloss that stalls the opening. | Cut with the gloss. If the author misses it, fold a short form into the inventory: "*huzurat* cavalry, picked for bravery and, I suspect, impatience". |
| 9 | "steady as monsoon rain on a Deccan roof" | VOICE_BIBLE 3.2 cites it as a model Deccan simile. | The physics is wrong: a drip is intermittent, while monsoon rain on a roof is a roar. | Keep the Deccan house and fix the physics: "steady as the eaves of a Deccan house in the rains." |
| 19 | "an unholy combination" | VOICE_BIBLE T1 counts it as the joke that closes the smell. | Both auditors flagged it. It is a stock idiom, and it explains a joke the pairing already makes (VOICE_BIBLE 3.3: he never explains his joke). | Cut. End the sentence at "incense". |
| 33 | "Enough to know when I am being lied to, Father," | It is dialogue and defiance, and it sets up João's "he understands". | It is a stock screen retort. | "“Enough for his jokes,” I said in my own Marathi, and tipped my head at João." This makes the language joke work and shows João's cruelty-by-joke, which confirmed row 19 removes from the narration. |
| 41 | "stone thick enough to swallow most screams before they reached the street." | "Most" is the chilling word: some screams did reach the street. | "Walls that swallow screams" is a stock torture-room image. | Keep. |
| 53 | "he said conversationally" | Tongs in hand and a chatty tone is João. Once "wrap cruelty in jokes" is cut, this one word does the showing. | It is an adverb tag, and the lines carry the tone on their own. | Keep. |
| 59 | "a life in chains that is still a life." | A Jesuit is trained to turn a phrase, and this is the offer the chapter's ending fulfils. | It is a tidy chiasmus of the kind the Voice Bible warns about in dialogue. | Keep. It is Duarte's one turned phrase before the quill line (VOICE_BIBLE rule 13: one epigram a scene). |
| 65 | "You will pull at my body ... You will hold hot iron ... You will try..." | João's "He talks too much" needs a speech long enough to earn it. | Three "You will" clauses are an orator's rhythm from a man with no fingernails. | Two clauses (confirmed row 65). |
| 69 | "He knows the game." / "for some higher good" | Both idioms are period-possible. | "Knows the game" is stock, and "some higher good" is a modern abstraction set beside the concrete "plunder". | Cut both: "Do you believe you fight for God, or is it simply for plunder and the honour of your people?" |
| 91 | "I closed my eyes, not in prayer, but in calculation." | VOICE_BIBLE T2 and 6b defend it: the Y is paid out at once in five concrete questions, and "not in prayer" answers Duarte's God question in action. The Chapter 2 audit leans on the prayer contrast (its merged ch2:97 to 99). | STYLE_SHEET section 1 allows this construction only in dialogue. Both auditors flagged it at top severity, and the chapter already keeps its one spoken correction at 69. | Re-voice, keeping both halves and the Chapter 2 echo: "I closed my eyes. Along the wall men were praying, some to the priest's God and some to their own. I counted, as I always had." If the author keeps the original, it is the one narration correction to spare, and 105's still goes. |

## Defended (flagged, but keep)

| Line | Quote | Flagged by | Reason to keep |
|:-|:-|:-|:-|
| 5 | "The first thing they took was my name." | both (2) | This is the book's spine motif (OPENINGS_ENDINGS_MOTIFS 4.1 calls it "the best line in the book"), paid off in ch9, ch17, ch19, ch21 and ch25. "Taken" pairs with the nails at 13: name, then body. The real weakness was the bookend at 111, which goes. The chapter does not disprove the line: the register takes the name, and Duarte uses it at 49 as bait. |
| 7 | "a number the clerk scratched beside the words *prisioneiro marata*" | pattern (2) | The "Here I was" frame goes (confirmed row 7). The number stays, because ch9:122 says "they tried to erase my name and replace it with a number in their books". *Marata* is the period Portuguese form. |
| 9 | the bells above against the bucket below | both (2) | The contrast is physically real in a cellar, and the evening bells pair with the morning bells that open ch2:3. Only "the rhythm that governed us" and the two "somewhere"s go. |
| 11 | "I was twenty-five that year, 1738" | holistic (flagged the paragraph) | This is the chapter's one memoir anchor, added on purpose (REVIEW_BACKLOG C12-06, F13-05). Only the antithesis goes. |
| 13 | "They had already taken my fingernails by the time Father Duarte came." | pattern (1) | The strongest sentence in the opening: flat, unexplained, the horror already in the past tense. Keep it as its own paragraph. |
| 23 | "Stubborn is better than broken in any language." | pattern (3), holistic (1) | He coins it on the spot from João's own word, and "in any language" is a language joke (the word came to him in Portuguese). It passes the drill-ground test, it is his only proverb in the scene after the cuts, and the Voice Bible names it as a keeper (T1, 6b). |
| 39 | "curled under me" | holistic (contradicts "backs pressed to damp stone" at 9) | There is no contradiction: a man chained with his back to a wall sits with his legs folded under him. The fix keeps "folded under me". |
| 43 | "Pliers. Hammers. Wooden wedges." | both (3) | This is a count of things he could touch, which VOICE_BIBLE rule 11 and 6b allow, and the wedge pays off at 81. Once 45 is cut, the list is no longer the setup for a pun. |
| 49 | "using my name as if it still belonged to me" | pattern (2) | It adds meaning rather than restating: the priest hands back the taken name as bait. Once 111 goes, it is the only touch of the spine motif mid-chapter, and it becomes the chapter's one "as if". |
| 49 | "You have already told us ... You have admitted..." | both (2) | Interrogators read back the confession so far. That is method, not "as you know" exposition. Only the rank gloss is trimmed (confirmed row 49). |
| 55 | "My throat closed. Kanka's black mane ... near Chaul. I forced the memory down." | pattern (2) | This is the Voice Bible's model for feeling (3.5): one beat in the body, a memory in nouns, then an act. Chaul pays off at ch6:151. Only the sentence after it goes. |
| 69 | "Not for the Viceroy, for me." | pattern (2) | It is natural speech and the chapter's one allowed spoken correction (STYLE_SHEET section 1). It makes the question personal, which ch24:325 picks up ("Whether you found what you were fighting for"). |
| 73 | "He seems to favour whoever has the better powder." | pattern (1, as a Voltaire echo) | Theology as a trade dispute, the register the whole chapter should be tuned to (holistic reader). ch24:327 quotes it. The idea is a soldier's commonplace older than Voltaire: Bussy-Rabutin's letter of 1677 says God is usually on the side of the big squadrons. So it is period-plausible, not borrowed from 1770. |
| 81 | "what remained of my left thumbnail" | pattern (continuity check against 13) | It is consistent: the nails were torn, not gone, and ch19:179's ridged regrown nails follow from it. |
| 93 | "How many guards at the door. ... How many steps from the stair to the courtyard above." | pattern (accepted), holistic (protected) | The engine of the voice (VOICE_BIBLE T2). The Chapter 2 audit pays off the last question with its step count. |
| 95 | "I counted, as I always had." | pattern (3) | Keep the sentence and move it ahead of the inventory, so that it introduces the count instead of restating it. VOICE_BIBLE C8 proposes a last line for the book that answers it ("as I always had"). |

## Opening

Current (5 to 13): four hook shapes in the first seven lines (5, the kicker at the end of 7, 11, 13) and a glossary sentence, in about 260 words. The raw material is the best in the chapter: the clerk's shrug, the book, the Nashik river that quietly plants his fear of the sea, *prisioneiro marata*, the fingernails. It is buried under a "Not X, just Y" opener, a triple "no longer", a gloss and an "old enough / young enough" antithesis.

Verdict: **keep 5 and 13**, which bracket the page (name, then nails). **Rewrite 7 and 11, trim 9.** Do not open on the clerk instead of line 5. Line 5 is the spine of the book, and it only looked decorative because 111 mirrored it.

Proposed opening (about 205 words):

> The first thing they took was my name.
>
> A clerk took it with a shrug and a line in his book, and did not lift his head to do it. I had been Nagoji Sawant, *huzurat* cavalry in the service of Chimaji Appa and the Peshwa, rider of the black horse Kanka, son of a village near Nashik where the farthest water anyone feared was a swollen river in the rains. The clerk scratched a number beside the words *prisioneiro marata* and called the next man.
>
> They chained us in rows along the curved wall, backs to the damp stone, ankles linked by rusty iron. Faint through the stone came the bells of Goa's churches, ringing for evening prayers. Down here we had the scrape of the gaoler's boots, the splash of the bucket that carried away blood and filth, and water dripping in the dark, steady as the eaves of a Deccan house in the rains.
>
> I was twenty-five that year, 1738, in the seasons after we broke a string of Portuguese forts along the Konkan. I had seen men I admired die foolishly, and I still expected to die in the saddle.
>
> They had already taken my fingernails by the time Father Duarte came.

What each change buys: the correction opener goes, and it was the first of eight in the book (OPENINGS_ENDINGS_MOTIFS 2.1). The "no longer" litany becomes one inventory sentence of things he was. The clerk now acts twice, in a shrug and in calling the next man, so no line is needed to say he was indifferent. The bucket stays for 93. "Die in the saddle" replaces an abstraction with the object the chapter is about to take from him.

## Ending

Current last lines (107 to 113):

> Back pressed to cold stone, I listened, and for the first time since they dragged me into this fortress a thin thread of hope tugged at me.
>
> Ships meant movement. Movement meant chances.
>
> The Portuguese had taken my name and tried to break my body. They had forgotten the simplest lesson of the Deccan monsoon.
>
> Storms do not ask permission.

Verdict: **rewrite.** This is the chapter's heaviest block. It has four closing beats in a row (a labelled hope, a chain-link maxim, a bookend summary and a motto), and the motto has no referent: what did the Portuguese forget, and how would a storm matter to them? The storm line recurs at ch7:225 and gives away Chapter 3's title, and the style sheet reserves the storm for ch13:321, with the old woman at ch5:105 as its plant. The one earned idea on the page, that a ship means a chance, belongs to Chapter 2's dialogue.

Proposed ending (replaces 103 to 113, after the cut of 95 to 101):

> The next day a rumour came down the wall from man to man, too low for the gaoler to hear. The Portuguese were gathering prisoners for a ship, and the ship was going south, where they needed men to work their land.
>
> That evening the clerk came down with his book and a stick of chalk and walked the wall behind João. Wherever João stopped, the clerk turned his pages, found the man's number and chalked a stroke on the stone above his head. When they reached my place I sat up as straight as my shoulders would let me, and João stopped.

Why this ending:

- It ends on an action with a small hook: he has been chosen, and he wanted to be.
- The hope is shown, not named. A tortured man sits up straight to look fit for labour, which carries everything "a thin thread of hope" and "Ships meant movement" said.
- It closes the name thread through an object, not a moral. The same clerk, the same book and the same number from the first page come back, and nothing has to say "they had taken my name".
- It gives Chapter 2 a source. "Those marked go to the docks" (ch2:7) and "the marks on my cell wall" (ch2:11) now point at something the reader has seen, so ch2:11 can stand as written, and the Chapter 2 audit's fallback ("his strip") is no longer needed.
- It leaves Chapter 2 its own devices. Chapter 2 opens on bells and on counting strokes, the Chapter 2 audit gives the stair count to ch2:25 ("nineteen, in two turns"), and it gives the scratched tally to the ship's plank. An ending on chalk made by the Portuguese does not spend any of these. Nagoji's own marks begin in the hold, which makes a quiet pair: first they mark him, then he marks the days.

This supersedes the draft Chapter 1 ending in OPENINGS_ENDINGS_MOTIFS 3.4, in which Nagoji scratches a mark with his ankle iron and counts the stairs ("Nineteen, up to the light"). That draft ends on a count that Chapter 2 now opens with and uses at line 25, and on a self-made mark that Chapter 2 now places in the hold.

Cut-only fallback: delete 107 to 113 and end on the rumour sentence ("...where they needed men to work their land."). It is plain and hands over cleanly to Chapter 2, but it loses the object bookend.

## Flab

| Lines | Issue | Action |
|:-|:-|:-|
| 7 | A 40-word glossary sentence stops the lament in its first paragraph. | Cut (confirmed row). |
| 15 to 17 | Three framing sentences ("Here he was", "That habit predated...", "Here in this cellar...") wrap two good details. | Cut the frames and keep the calluses, the saddle strap and the sardar's hand. |
| 7, 15, 17, 39 | The Here/There pivot four times, three of them as a "Deccan then, cellar now" tag. | All four go under confirmed rows. "Deccan" drops from four uses to one, the eaves at 9. |
| 29, 49, 59 | What the Portuguese want is listed three times ("No names, no forts, no routes"; "who ordered ... how many ... which forts"; "The Viceroy needs names. He needs ... He needs ..."). | Keep João's (29) and Duarte's question (49). Cut 59 to one sentence, the siege guns. |
| 11, 59, 63 | The fall of the northern forts is told three times. | Keep 11's clause and Duarte's siege-guns line. 63 shrinks to one line of hope. |
| 25 to 89 | Duarte's conscience is signalled about nine times: wince and twitching fingers (25), "fingers worrying at the cloth" (47), "softly" (69), mouth twitch (75), working jaw and "small, weary nod" (79), wrist grab (83), "voice rough" (85), "The tired priest" (89). | Keep 25 (ch24:302 calls back the sleeves and the grey eyes), the hesitation and nod at 79 (ch24:311), and 83 to 85 (ch24:355). Cut "fingers worrying at the cloth" at 47, and the rest under confirmed rows. The glance at 61 stays: it is a threat, not conscience. He is more interesting when the reader has to infer him. |
| 15, 17, 25, 31, 61 | "Gaze" and "eyes" do the blocking five times in about forty lines. | Let an action carry it. For example, at 25: "Father Duarte looked where the boot had touched." |
| 39 | A creed and a Here/There contrast pad a man being hauled to his feet. | Confirmed row 39. |
| 65, 73 | Two speeches in balanced oratory from a man whose fingernails are gone. | Trim to what ch24 quotes back and what João's "He talks too much" needs. |
| 81 | Generalising in the second person ("Once you have felt...") after two exact sentences. | Confirmed row 81. |
| 89 | Duarte's reason for stopping repeats the quill line at 85. | Confirmed row 89. |
| 91 to 113 | The closing cascade: eleven paragraphs, eight of them one sentence, seven ending on a fragment, a kicker or a motto. The prose resolves the chapter again at 91, 95, 97, 99, 101, 107, 109, 111 and 113. | Keep 91 (re-voiced), 93 and the rumour. Cut 95 (except its first sentence, moved), 97 to 101 and 107 to 113. Add the chalk ending. |

## Passages to protect

These are marked with the later chapters that depend on them. An edit that changes the words breaks the callback.

- **5** "The first thing they took was my name." The spine motif of the book.
- **7** "a shrug and an entry in a book"; the Nashik river line (it plants his fear of the sea for Chapters 2 and 3); "*prisioneiro marata*"; the number (ch9:122).
- **9** The evening bells (they pair with ch2:3's morning bells) and the bucket (it pays off at 93).
- **13** "They had already taken my fingernails by the time Father Duarte came."
- **15** The cassock held above the slime (ch24:311), the scholar's stoop and ink-stained fingers (ch24:302), the calluses (ch4:43 mirrors them on Nagoji).
- **17** "from the loosened strap on a trooper's saddle to the way a sardar's hand tightened on his sword hilt at the mention of a rival."
- **19** "garlic sausage and chapel incense" (chouriço and the Church, exactly Goa); the boot tap, "almost companionable".
- **21 to 23** "Este ... this one is stubborn." / "Stubborn is better than broken in any language."
- **25** The grey, tired eyes, the wince, the fingers twitching inside his sleeves (ch24:302 repeats all three).
- **33** "My mouth tasted of rust and old water." / "I have heard most of them already."
- **43** "tools that had never worked metal. Pliers. Hammers. Wooden wedges."
- **51** "My horse does not read."
- **53** "Your horse is dead ... We shot it when we brought you in. A pity. Fine animal."
- **55** "My throat closed. Kanka's black mane against my cheek on winter mornings, his easy stride, the way he had carried me through musket fire near Chaul. I forced the memory down." (ch6:151 recalls Chaul.)
- **57** "Then he died better than I will" (ch3:227, "the horse who died better than I would").
- **67** "He talks too much."
- **69** Duarte's question, including "Not for the Viceroy, for me." (ch24:311 and ch24:325).
- **73** "men who do not fight are trampled" and "I leave Him to the Brahmins and to you. He seems to favour whoever has the better powder." (ch24:327 quotes both.)
- **79** The hesitation and the nod (ch24:311, "hesitated, and nodded anyway").
- **81** "The first wedge went under what remained of my left thumbnail. After that, pain lost its degrees." (REVIEW_BACKLOG C10-05 already removed the repeat in Chapter 3, so this is the one home of the line.)
- **83 to 87** The wrist grab, "The Viceroy needs a hand that can still hold a quill.", and "The gaoler grumbled, but he chose another tool." (ch24:355.)
- **93** The five questions.

## Chapter-specific notes

1. **Callbacks that constrain the edit.** Later chapters quote this one at: ch3:227 (57); ch4:43 (15, the calluses mirrored); ch6:151 (55, Chaul); ch9:122 (7, the number); ch24:302 (15, 25); ch24:311 (15, 69, 79); ch24:325 and 327 (69, 73); ch24:355 (83); ch25:248 (81, and Duarte watching from a distance). Every fix above keeps the words that are called back. The ch25:248 memory ("fingers bend at angles they were never meant to bend") echoes the first edition's line 81, which the fix removes. It still reads as his memory of the chamber, but if the author wants the exact echo, keep "the way they were meant to bend" in the new sentence: "They used the ropes on my shoulders and bent my fingers the way they were never meant to bend..."
2. **Language logic (31 to 49).** Duarte asks in Portuguese, Nagoji answers in Marathi, and the interrogation goes on with no word about how the priest understands him. One clause settles it, at the end of 47: "He questioned me in Marathi, a priest's Marathi learned from books." This is sound for the period: Goa's Jesuits preached and wrote in Marathi and Konkani (Thomas Stephens's *Kristapurana*, 1616). It also gives Nagoji a foreigner's ear on his own language. Do not put it on "Bring him" at 37, which is spoken to João.
3. **Keshavrao is never planted.** ch2:17 has him "familiar", ch2:75 has Nagoji surprised he is alive, and ch3:227 calls him "the boy I promised not to leave", but he is not in this chapter. The anonymous "someone sobbed quietly in the darkness" (101) is the slot. Optional replacement: "That night a man wept further along the wall. It might have been Keshavrao, the youngest rider in my troop, if the Portuguese had let him live. I did not call out." Not calling out is itself the chapter's subject: a name said aloud in that cellar is a name for João, and the interrogation has just failed to get one. ch2:21 then shows him risking it ("Rao," I said softly). This is compatible with the Chapter 2 audit's line 17 fix, which gives Keshavrao's age at first sight. It is an author decision because it adds a fact: that Nagoji knew Keshavrao had been taken.
4. **Kanka (REVIEW_BACKLOG BL-01).** This chapter's version (he, shot at capture) is the one to keep. The fixes belong in prequel:23 and ch7:145 and 179, not here.
5. **The brand (REVIEW_BACKLOG N-21).** The brand is never applied on the page, and it moves around the body in later chapters. The irons now resting in the brazier (confirmed row 43) and Duarte's "Not yet" at 85 give it a home. If the author wants it shown here, the place is the end of the torture scene, where the irons already are, as one sentence after "Enough" at 89: "Before they cut me down, João took an iron from the coals and put it to my left forearm, and this time the priest did not stop him." That pays off "Not yet", fixes the brand on the forearm (as the backlog recommends), and leaves ch24:355 true, since Duarte stopped him once. The Chapter 2 audit offers ch2:7 as the alternative place. Choose one.
6. **The officer with the cuffs (REVIEW_BACKLOG N-41).** ch24:223 remembers an officer who came "to the cell each morning", checked his cuffs and gave orders. He is not in this chapter. If the author wants him planted, the natural place is paragraph 9, as one plain sentence ("Each morning an officer in a white coat came to the foot of the stair, looked us over, straightened his cuffs and went up again."), not in the ending.
7. **Dhanaji (REVIEW_BACKLOG N-01).** ch13:221 says he "survived Goa's dungeons alongside me", and this chapter has no Dhanaji. Fix it in ch13, per the backlog. Do not add him here.
8. **"these priests" (63) and "priests and gaolers" (81).** There is only one priest in the room. Both are fixed by confirmed rows 63 and 81.
9. **The stool (47).** "My wrists bound to its legs" folds him double and leaves no hands for the wedges. The ceiling ropes (43) and "joints forced" (81) point to the strappado. Suggested: "They sat me on a stool and tied my ankles to its legs."
10. **Where the ship is going (history).** By 1738 Portugal held nothing on the Indian coast south of Goa: the Dutch took Quilon (1661), Cranganore (1662), and Cochin and Cannanore (1663), and Ceylon was lost by 1658. A ship leaving Goa southward must be bound round Cape Comorin for the East, which fits ch2:55 ("beyond Lanka") and the Chapter 2 audit's "round Comorim" at ch2:103. The first edition's "Somewhere beyond the horizon" was hiding this. The fix keeps the rumour to "south, where they needed men to work their land" and leaves the destination to Chapter 2's prisoners, whose rumours may disagree.
11. **"Chimaji was coming for Goa" (63, history).** Maratha forces did overrun Goa's outer provinces of Bardez and Salcete in early 1739, but under other commanders, and the city itself was never taken. As a prisoner's hope in 1738 the line is plausible. The fix frames it as hope ("I told myself") rather than as fact.
12. **The Viceroy.** In 1738 the viceroy was Pedro Mascarenhas, Conde de Sandomil (1732 to 1741). He is unnamed here, which is fine. If a later chapter names the viceroy of this period, use him.
13. **Huzurat is glossed three times** (ch1:7, ch1:49, ch5:145). After the fixes it is glossed once here (by Duarte) and once in Chapter 5. Following VOICE_BIBLE 3.7, italicise it at 7 and set it in roman at 49.
14. **Seam with Chapter 2.** Chapter 2 opens on bells and on counting. The ending must not close on either, and the chalk ending does not.
15. **One shared cellar.** The chapter consistently has one cellar with prisoners in rows ("this cellar", 7 and 17), and the fixes keep that word. The Chapter 2 audit corrects "cells" at ch2:3 to match.
16. **Retrospect.** The memoir frame is announced once ("I was twenty-five that year, 1738") and never used again. The confirmed fixes add none, deliberately. If the author wants one line of hindsight, the natural place is after the hope at 63 ("Any day now, I told myself..."), where a reader who knows 1739 feels the irony without being told.

## Appendix: the chapter with the fixes applied

This is for reading, to check that the voice survives the cut. It is not for pasting. It applies every confirmed fix, the leaned borderline choices and the proposed ending. It also includes three optional additions, which the author may drop: the Marathi clause (Notes, item 2), the Keshavrao plant (Notes, item 3) and the two irons in the brazier (confirmed row 43). The vinegar at 41 is a placeholder detail. 1,521 words, against 1,941.

> The first thing they took was my name.
>
> A clerk took it with a shrug and a line in his book, and did not lift his head to do it. I had been Nagoji Sawant, *huzurat* cavalry in the service of Chimaji Appa and the Peshwa, rider of the black horse Kanka, son of a village near Nashik where the farthest water anyone feared was a swollen river in the rains. The clerk scratched a number beside the words *prisioneiro marata* and called the next man.
>
> They chained us in rows along the curved wall, backs to the damp stone, ankles linked by rusty iron. Faint through the stone came the bells of Goa's churches, ringing for evening prayers. Down here we had the scrape of the gaoler's boots, the splash of the bucket that carried away blood and filth, and water dripping in the dark, steady as the eaves of a Deccan house in the rains.
>
> I was twenty-five that year, 1738, in the seasons after we broke a string of Portuguese forts along the Konkan. I had seen men I admired die foolishly, and I still expected to die in the saddle.
>
> They had already taken my fingernails by the time Father Duarte came.
>
> The padre walked between the lines of prisoners with his black cassock held above the slime on the floor. He was a thin man with a scholar's stoop and ink-stained fingers, the sort of holy man who looked built for argument. Yet his right palm had the calluses a sword grip leaves. His eyes went from one ruined body to the next.
>
> I watched him without seeming to. As a boy I had learned to sit in the corner of a fort courtyard and see everything, from the loosened strap on a trooper's saddle to the way a sardar's hand tightened on his sword hilt at the mention of a rival.
>
> The gaoler, João, moved beside the priest. He was a broad man whose belly strained his leather belt, and he smelled of garlic sausage and chapel incense. When he passed my place he tapped my shoulder with his boot, almost companionable.
>
> “Este,” he said in Portuguese, “this one is stubborn.”
>
> I kept my face blank. Stubborn is better than broken in any language.
>
> Father Duarte looked where the boot had touched. His eyes were grey and tired, with the faint redness of a man who slept badly. When he saw my hands, wrapped in dirty cloth, he winced and his fingers twitched inside his sleeves.
>
> “How long since the last questioning?” he asked in that same tongue.
>
> “Two days,” João replied. “He still insists he is only a horseman. No names, no forts, no routes. He knows we have others who talk, but still he holds on.”
>
> The priest's eyes came back to my face. “You understand our language, senhor marata?”
>
> “Enough for his jokes,” I said in my own Marathi, and tipped my head at João. My mouth tasted of rust and old water. “But you can speak your questions. I have heard most of them already.”
>
> João laughed. “You see, he understands.”
>
> “Bring him,” Father Duarte said.
>
> They unshackled my legs and hauled me upright. My knees had been folded under me so long that they would not straighten, and I bit down on the groan before João could hear it.
>
> The interrogation chamber lay twenty paces away. The smell changed as we went, from rotting straw and human waste to lamp oil, sweat, spilled wine and the vinegar they used to wash the floor. They had built the room under a vaulted arch, stone thick enough to swallow most screams before they reached the street.
>
> Ropes hung from an iron ring bolted into the ceiling. A table sat to one side, laid out neatly with tools that had never worked metal. Pliers. Hammers. Wooden wedges. A brazier glowed on the far side of the room with two irons resting in the coals.
>
> They sat me on a stool and tied my ankles to its legs. João checked the knot, then moved to the table. The priest remained standing, hands tucked into his sleeves. He questioned me in Marathi, a priest's Marathi learned from books.
>
> “Nagoji Sawant,” Father Duarte said, using my name as if it still belonged to me. “You have already told us that you rode with a Maratha force against our allies. You have admitted that you attacked Portuguese caravans and outposts. The Viceroy's spies say you rode huzurat, in Chimaji Appa's own household horse. Such men see more than dust and hooves. What we do not yet know is who ordered those attacks, how many men you had, and which forts or roads you meant to strike next.”
>
> “You know more than I do then,” I said. “We raided where we could, when we could, against whoever traded with our enemies. That is the way of the ghats and passes. You have maps and books. My horse does not read.”
>
> João picked up a pair of iron tongs. “Your horse is dead,” he said conversationally. “We shot it when we brought you in. A pity. Fine animal.”
>
> My throat closed. Kanka's black mane against my cheek on winter mornings, his easy stride, the way he had carried me through musket fire near Chaul. I forced the memory down. João had the tongs in his hand and his eyes on my face.
>
> “Then he died better than I will,” I said.
>
> Father Duarte studied me. “You are not a fool,” he said. “The Viceroy needs names. He needs to know whether Chimaji Appa means to bring his siege guns to Goa. Tell us, and this ends. I can speak for you, perhaps find you work on a plantation, a life in chains that is still a life. If you do not...”
>
> He glanced at the brazier.
>
> So the Viceroy was afraid for Goa itself. Any day now, I told myself, the ground above this cellar would shake under Maratha guns.
>
> “If I do not,” I said, “you will do what you have already done to others. You will pull me apart on your ropes and put your irons to my skin until I scream whatever names you have already written down.”
>
> João snorted. “He talks too much.”
>
> “He is a soldier,” Father Duarte said. He stepped closer. “Tell me this at least, Nagoji. Not for the Viceroy, for me. Do you believe you fight for God, or is it simply for plunder and the honour of your people?”
>
> For a moment I was on a ridge above the Godavari again, looking down at the dust of a marching column, my chest tight the way it always was before we rode.
>
> “I fight because men who do not fight are trampled,” I said. “As for God, Father, I leave Him to the Brahmins and to you. He seems to favour whoever has the better powder.”
>
> The priest almost smiled.
>
> “You see,” João said, “he gives you nothing. Let me loosen his tongue.”
>
> Father Duarte was a long moment answering. Then he nodded, and João reached for the tools.
>
> The first wedge went under what remained of my left thumbnail. After that, pain lost its degrees. They used the ropes on my shoulders and the tongs on my fingers, and through all of it the priest stood back and watched.
>
> Once, when João reached for the brazier, Father Duarte's hand shot out and closed over his wrist.
>
> “Not yet,” he said, voice rough. “The Viceroy needs a hand that can still hold a quill.”
>
> The gaoler grumbled, but he chose another tool.
>
> At last Father Duarte said, “Enough.” João complained that the marata had still given no names, but he cut me loose.
>
> When they dragged me back to the cellar and chained me in my place against the wall, my hands were raw meat and my shoulders throbbed with each breath. I closed my eyes. Along the wall men were praying, some to the priest's God and some to their own. I counted, as I always had.
>
> How many guards at the door. How often the watch changed. Which men wore keys at their belts and which only carried cudgels. Where the buckets were stored. How many steps from the stair to the courtyard above.
>
> That night a man wept further along the wall. It might have been Keshavrao, the youngest rider in my troop, if the Portuguese had let him live. I did not call out.
>
> The next day a rumour came down the wall from man to man, too low for the gaoler to hear. The Portuguese were gathering prisoners for a ship, and the ship was going south, where they needed men to work their land.
>
> That evening the clerk came down with his book and a stick of chalk and walked the wall behind João. Wherever João stopped, the clerk turned his pages, found the man's number and chalked a stroke on the stone above his head. When they reached my place I sat up as straight as my shoulders would let me, and João stopped.
