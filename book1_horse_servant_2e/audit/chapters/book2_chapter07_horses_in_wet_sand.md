# Chapter 7 Audit: Horses in Wet Sand

Source: `book1_horse_servant/book2_chapter07_horses_in_wet_sand.md` (first edition, 225 lines, 2,868 words). Line numbers refer to that file.

- I read the whole chapter myself. I then set the reports from the pattern auditor and the holistic reader against it, and against `STYLE_SHEET.md`, `VOICE_BIBLE.md` (sections 4 to 6b, which triage this chapter's naming scene and its "Anticipation" passage), `OPENINGS_ENDINGS_MOTIFS.md`, `REGISTER_AND_ANACHRONISM.md`, `REVIEW_BACKLOG.md` and the Chapter 6 audit in this folder.
- I also checked Chapter 1 (lines 39 and 53 to 55), Chapter 6 (lines 11, 31, 107, 141, 151, 163 and 171) and Chapter 14 (line 101) for continuity.
- Where the two auditors flagged the same line, I merged the flags into one entry. When in doubt I kept the line: a line stays if it does work a cut would lose.
- The word counts and scanner figures come from a scratch copy with every confirmed fix applied, run through `audit/tools/scan_slop.py`. The scratch copy is not in the repo.

## Verdict

| Measure | Value |
| :- | :- |
| Severity | **3 of 5**, at the high end of 3. The scene work is sound, but the seams read at 4 to 5. |
| Recommended intensity | **Medium**: fix the tics and tighten. Rewrite only at the three section endings and in the horse-economics block. |
| Estimated word cut | **24%**, from 2,868 to about 2,170 words. About 9 points of that is the unpublished exposition at 149 to 157 (`SOURCE_OF_TRUTH.md` Decision 2). |

The chapter has a real spine: two proud troops of horse, ground that "drinks the hoof", and a foreign captain who has to earn the right to give orders. The best writing in it is as good as anything in the book: the laughing horses (3 to 7), "not to dance with crabs" (29), "He waits for the sand to hold him" (71), the driftwood map (83 to 89), "less foolish than they were at sunrise" (117), and Ibrahim's lamps and priests (205).

Machine connective tissue sits around that material:

- **Every section ends on a named feeling or a moral.** Section one ends on "Anticipation." (139), section two on "the strange comfort of belonging" (183), and the chapter on "Storms did not ask permission. Perhaps..." (225).
- **Every speaker talks in maxims.** Raza Khan, Ponnan, the king, Ramayyan and Ibrahim all use the same epigram register.
- **Lines 147 to 157 are an essay**, and it contradicts itself on where the Maravar ponies come from.
- **Ibrahim states the tolerance theme three times** (209, 217 and 221), and the narrator restates it once more.

Almost all of this can be fixed by cutting. Nearly everything worth keeping is already on the page.

Scanner counts before and after the confirmed fixes:

| Marker | Style-sheet ration | Before | After |
| :- | :- | :- | :- |
| "as if" | 1 | 3 (19, 157, 177) | 2; 1 if the borderline fix at 19 is taken |
| "like a / like the" similes | 2 | 4 | 1 (77, the tide, in dialogue) |
| slowly / quietly / softly | 2 | 5 | 2 (49, 167) |
| fragments for effect | 3 | 10 | 2 |
| "something X" | 0 | 2 | 0 |
| one-sentence paragraphs | none set | 34 | 29 |
| "strange" | none set | 4 | 0 |
| em dashes | 0 | 0 | 0 |

## Confirmed issues

53 entries. Fixes are drafts in Nagoji's voice for the author to accept, adjust or reject.

| Line | Quote | Category | Suggested fix |
| :- | :- | :- | :- |
| 15 | "They looked confident. Too confident." | kicker | Cut both sentences and end on something he sees: "Behind him the men sat straight in their saddles, horses tossing their heads, bits clinking. None of them looked down at the sand." |
| 17 | "They wore no uniforms, ... but each man carried himself with the easy assurance of one whose family had held swords for generations." | stock_phrase | "They wore white cloths hitched up for riding and short jackets, and sat their ponies with the reins loose in one hand." A Maratha would not expect uniforms, and the loose rein shows the ease. |
| 17 | "He said little, but his eyes missed nothing." | stock_phrase | "In all that riding he had not said twenty words to me." The original line is used again for the heir at ch17:25. |
| 23 | "the challenge had felt almost like grace ... it sat on me like a weight." | simile_stack | Cut the paragraph. Line 21 leads straight into the order at 25. |
| 31 | "you are not a soldier, you are a target." | correction | "If you charge a Dutch square and your horse stumbles on the turn, they will have time to load twice." |
| 33 | "He did not want to be seen arguing with the stranger Marthanda Varma had set over him." | explained_subtext | Cut. The whole paragraph becomes: "Raza Khan glanced up at the bluff, where the king watched." This also drops a jaw tic, the confusing "The Madurai rider" (he is their commander) and the capital K. |
| 37 | "a faint smile touched his lips as he signalled his Maravar." | stock_phrase | "Ponnan said nothing, but he was already signalling his Maravar down off the bluff." |
| 63 | "He glared at me, but the anger was cooled by the shame of the stumble." | explained_subtext | "He glared at me. Then he turned his horse back toward the water." |
| 65 | "You must ride with the sand, not against it." | correction | Cut. The speech ends on "before you ask for the turn." |
| 69 | "I stripped the pageantry from them. No formations. No lances. Just men sweating in the heat, learning that the Malabar coast did not care about their lineage." | fragment_list | "I sent their lances up the bluff and broke their ranks. I made them mix their lines, one heavy Madurai horse, one light Maravar pony, and walk and turn and walk again in the wet until the men had sweated through their jackets." |
| 73 | "The sun climbed. The heat turned the air liquid." | stock_phrase | "By the time the sun stood overhead the Madurai horses were caked to the knee." |
| 77 | "Precise. Mechanical." | fragment_list | "They load together and fire together, on one word." "Mechanical" is on the VOICE_BIBLE banned list (rule 10). |
| 79 | "To ride like the tide, one must first not drown in the sand." | dialogue_aphorism | Raza Khan wiped his face. “The tide does not break its legs.” This keeps him a mercenary deflating Nagoji's simile in his own trade, not a sage. |
| 81 | "Exactly." | modern_register | Cut. The driftwood at 83 is Nagoji's answer. |
| 89 | "We do not hit them. We bait them." | correction | “Us. We are the bait. We ride close, close enough to make them level their muskets.” |
| 89 | "we take them with the sabre." | modern_register | "we take them with the talwar." |
| 101 | "Slowly, muscle by muscle, the rhythm changed." | soft_adverb | "We went back to the work, and by the afternoon the rhythm had changed." Keep the rest of the paragraph, which is good. |
| 103 | "the subtle shift from resistance to acceptance. Men began to trust ... Horses began to trust ..." | balanced_antithesis | Cut the paragraph. If a beat is wanted, show one rider: "The Madurai rider I had shouted at in the morning took his horse through the turn at the water's edge without a slide, and rode back past me without a word, which from a Madurai man that day was praise." |
| 105 | "On the bluff, the awning's edge moved again." / "The diwan inclined his head" | staging | "On the bluff, the king rose and stretched his legs. He spoke to Ramayyan in words I could not catch. The Dalawa inclined his head..." Nothing has moved before, so "again" has nothing to refer to. For Dalawa, see the notes. |
| 111 | "he said, without preamble." | stock_phrase | "he said." |
| 113 | "If your enemies expect bulls, better to be something else." | abstract_depth | Cut. The line becomes: “Fish do not charge muskets,” I said. “But yes.” |
| 115 | "He nodded slowly." | soft_adverb | Cut. This is one of nine "nodded slowly" in the book. |
| 121-125 | "Even when their pride bucked harder than their horses." ... "Voices matter," ... "Especially when the sea is loud." | dialogue_aphorism | Replace 121 to 125 with what Ramayyan's palm leaves are for: “Four horses lame by my count,” he said. “None of them Maravar.” This pays off the stylus at 19 and puts him in his own register of accounts and understatement. |
| 127 | "The king's gaze shifted to the horizon, where a line of darker blue hinted at deeper water." | stock_phrase | "The king looked down at the tide line, where the water was already filling the holes the Madurai horses had torn in the sand." |
| 129 | "he said softly." | soft_adverb | "he said." |
| 135-139 | "a strange mixture tightened in my chest. / Fear, yes. Responsibility, sharp as any spear point. But also something I had not felt since before Goa, before the dungeon, before the storm. / Anticipation." | summary_ending | Replace all three paragraphs with one act: "Halfway down the slope I caught myself already sorting the Madurai horses in my head, the ones that had kept their feet from the ones that would get a man killed." (VOICE_BIBLE C2.) This also removes the tricolon that ch20:412 repeats. |
| 145 | "a stride that ate distance ... too stunned to mourn properly." | stock_phrase | "In the Deccan I had ridden Kanka, a black stallion with a temper like monsoon lightning. The Portuguese shot him when they took me." This follows REVIEW_BACKLOG BL-01. If the author keeps the Vasai version instead, keep the mare and Vasai, cut only the two stock phrases, and fix "the last miles to Goa" (see notes). |
| 147 | "their temperaments uncertain in this strange wet land." | stock_phrase | "...bred for show as much as war, and not yet sure of wet ground." "Strange" is the chapter's default adjective: 135, 147, 183 and 221. |
| 149 | "horses were not native to Kerala in the way they were to the Deccan or the Rajput lands." | modern_register | "On the Bhima we bred our own horses. On this coast nobody bred them at all." This removes the modern state name and gives him a Deccan anchor (the Bhimthadi horse). |
| 151 | "their desert bloodlines prized for endurance and speed." | stock_phrase | Cut. |
| 153 | "their ancestors had lived on this coast for generations, bred by families who valued survival over elegance. They knew the monsoon in their bones." | balanced_antithesis | Cut both sentences. They contradict 149 ("Every war horse on this coast was an import"), and Maravar country lies east of the ghats. Keep the hoof, coat and fodder sentences. |
| 155 | "The smart commanders mixed their cavalry. ... the shock troops, ..." | modern_register | Cut the paragraph. It restates the mixed lines already staged at 69. "Shock troops" is a First World War coinage, and "smart" is colloquial (REGISTER, rated P1). |
| 157 | "his stylus tapping each line as if the numbers pained him." | simile_stack | "Ramayyan had shown me the accounts once, tapping each line with his stylus." |
| 157 | "But without cavalry, the king was just another petty chief with spears. With cavalry, he could strike ..." | balanced_antithesis | Cut. End the paragraph on "than to paying the men who rode them." |
| 159 | "One horse caught my attention." | stock_phrase | Cut, and open 161 with "At the end of the picket line stood a bay mare, neither Madurai nor Maravar..." |
| 161-163 | "that seemed to hold the earth's heat. She stood at the edge of the picket line, watching me approach with an expression I recognized. / Wariness. Interest. The calculation of a creature deciding whether to trust." | fragment_list | "Her coat was the colour of red earth after rain. She watched me come, one ear on me and one on the Madurai horses, her weight already shifted to go." (VOICE_BIBLE section 5.) A horseman reads ears and weight, not "expressions". |
| 169 | "then, unexpectedly, pushed her nose into my chest." | soft_adverb | "then pushed her nose into my chest." |
| 171 | "hay and sweat and something else, something green and unfamiliar, the herbs" | abstract_depth | "hay and sweat and the green herbs they fed the horses here to keep them cool in the coastal heat." |
| 173 | "But it was honest." | kicker | Cut. |
| 175 | "the word coming unbidden. It was the Malayalam name for the backwaters, those brackish channels that threaded through this coast like veins." | simile_stack | “Kayal,” I said. It was the fishermen's word for the backwaters. This glosses the word by how he learned it (voice rule 9). "Veins" also repeats ch10 and ch26. |
| 179 | "The first time I had let myself care whether one particular animal lived or died." | explained_subtext | Cut. Keep the first sentence ("since Goa" if the BL-01 fix is taken). |
| 181 | "Some bonds are forged in battle. Others in the quiet after, when the sun sets and a man stands alone with a creature who asks nothing but grain and a steady hand." | kicker | Cut. |
| 183 | "But that night, all I knew was the warmth of her breath and the red-brown of her coat, and the strange comfort of belonging, even a little, to this unfamiliar land." | summary_ending | "That night she only wanted the salt off my hand." For the first sentence of 183, see Borderline. |
| 193 | "his face half-shadowed by the evening light." | stock_phrase | "He leaned against a palm trunk." |
| 195 | "It was not a question." | stock_phrase | Cut. The book uses this line six times, and Nagoji answers it as a question anyway. |
| 201 | "I pray to whatever is listening ... a cavalryman with sand in his boots." | modern_register | “I pray to Khandoba when I remember,” I said, “and to whichever god is nearest when I do not. One of them may have time for a cavalryman with sand in his ears.” "Whatever is listening" is modern agnostic phrasing, and "sand in his boots" is an English idiom. |
| 203 | "Ibrahim was quiet for a moment." | stock_phrase | Cut, and drop "finally" from 205. |
| 207-209 | "He shrugged. / On this coast, the gods mix like the waters of the backwaters, salt and fresh, never quite one thing. A man who insists on purity drowns faster than one who learns to float in both." | dialogue_aphorism | Cut both paragraphs. Line 205 already shows the mixing through the lamps and the priests, and the backwater image was just used at 175. |
| 217 | "The king does not keep men for their faith. He keeps them for what they can do. Remember that, when you wonder why a Muslim sailor and a Hindu horseman and a Christian merchant all sit in the same war hall." | correction | Cut. Keep the first two sentences: “You are useful too, Sawant. That is why you are still alive.” |
| 219 | "He walked away into the gathering dark." | stock_phrase | "He walked off toward the cook fires." |
| 221 | "thinking about gods and usefulness and the strange tolerance of a king who measured men by their hands, not their prayers." | explained_subtext | Cut. See Ending. |
| 223 | "On Deccan soil, I had thought I knew the limits ... those limits shifted." | balanced_antithesis | Cut. It also contradicts ch1:55 and ch6:151, where he has already ridden wet sand near Chaul. |
| 225 | "Storms did not ask permission. Perhaps horses, taught well, did not either." | summary_ending | Cut. See Ending. |

Count by category:

| Category | Count |
| :- | :- |
| stock phrase | 14 |
| modern register | 5 |
| explained subtext | 4 |
| correction | 4 |
| soft adverb | 4 |
| balanced antithesis | 4 |
| kicker | 3 |
| summary ending | 3 |
| fragment list | 3 |
| dialogue aphorism | 3 |
| simile stack | 3 |
| abstract depth | 2 |
| staging | 1 |

## Borderline

These are lines where the flag is fair but the line also does work. Each has a recommendation, and the choice is the author's.

| Line | Quote | Issue | Recommendation |
| :- | :- | :- | :- |
| 5 | "Not with their mouths. Horses do not waste breath on that." | correction opener | The joke is Nagoji's and must survive. The problem is at book level: eight chapters open with a statement and then a correction (OEM 1.4), and the style sheet keeps correction constructions for dialogue. If the author is clearing that template, reorder without loss: "Horses do not waste breath on laughing. They did it with every sideways step, every planted hoof that refused to drive, every rolling eye that said what the riders did not dare speak aloud." Unlike the OEM draft, this keeps the riders clause, which line 7 needs. If one correction opener survives in the book, this is the best candidate. |
| 9 | "the tug of the Arabian Sea" | register | "the tug of the sea". This is a chart name used from outside; elsewhere he says "this coast". Low priority. |
| 11 | "lances gleaming, turbans wrapped high. Their commander, a lean man with a hawk nose and a scar that puckered his left cheek" | stock arrival kit | The line works, but it describes the men before the horses, and this is a horse chapter. Try: "...when the Madurai troop arrived, big horses with heavy necks, lances upright. Their commander, a lean man with a scar that puckered his left cheek, saluted..." Keep the scar and lose the hawk nose. |
| 13 | "Raza Khan, at your service," ... "in a Hindustani that carried the singsong of the Carnatic" | register | “Raza Khan,” he said, in the Dakhni of the Carnatic camps. "At your service" is an English courtesy formula. Dakhni is the word a Maratha would use for this speech. For the Nayak half of the line, see the notes. |
| 19 | "as if he meant to take notes on horses as much as on men." | "as if" ration | This is a good line, but the ration is one per chapter and 177 is the better one. Try: "...palm leaves in his lap, stylus ready in case the horses said anything worth writing down." The new tally at 121 then pays it off. |
| 39 | "The first pass was a disaster." | signposting | This is a plain soldier's verdict in the memoir voice. The first line of the chapter has already said the horses laughed at him, so the verdict gives no suspense away. Lean keep. Alternatively, cut it and let 41 open. |
| 45 | "The earth here judges weight. It punishes force." | paired aphorism | Keep "judges weight", because Ponnan throws the word back at 49. Cut "It punishes force." |
| 51 | "Today they followed me into the bog. Tomorrow they follow you around it." | balanced antithesis | Keep the move: handing the teaching to the Maravar sets up 69 to 71. The mirrored phrasing is the tell. Try: “Then teach the Madurai men,” I said. “They will take it better from you than from me.” |
| 93-95 | "To ride into the teeth of the gun and turn away." / "It is better than riding into the teeth and staying there," | motif ration | Nagoji's reply is good soldier's wit. OEM reserves "teeth" for Part IV, with one plant earlier. Keep it once, at 95, and change 93 to: “It is a gamble,” he said. “To ride at their muskets and turn away.” |
| 97-99 | "If the horses hold," he murmured. / "Make them hold." | screenplay beat | Defensible: it puts his own horses back in Raza Khan's hands. Change "murmured" to "said". Lean keep. |
| 107-109 | "When the run ended" / "watched the riders regroup below, tiny figures against the shining strip of water." | staging | "When the last pass was done..." and "Marthanda Varma watched the riders walk their horses back along the tide line." No particular run has been described, and "regroup" is a modern military verb. |
| 183 | "Kayal would carry me through Colachel and beyond." | flash-forward | VOICE_BIBLE 6b allows one memoir retrospect per chapter, and this is the right one, but only if ch14:101 names Kayal (REVIEW_BACKLOG N-03, OEM section 7). If the author fixes Chapter 14, keep "Kayal would carry me through Colachel." and drop "and beyond". If not, cut the sentence, because the book must not promise what it does not deliver. |
| 191 | "They simply refuse, or they follow. It is simpler than men." | word echo | Cut "simply". The rest of the line stays; it answers the king's "horses can disagree" (129). |

## Defended (flagged, but keep)

| Line | Quote | Flagged by | Why keep |
| :- | :- | :- | :- |
| 5 | "every sideways step, every planted hoof that refused to drive, every rolling eye that said what the riders did not dare speak aloud" | Pattern: tricolon | This is a horseman's list of refusals. Each item is something he could see from the saddle, and the third hands the insult to the riders, which both line 7 and Ponnan at 49 depend on. |
| 7 | "You do not belong here, Deccan man." | Pattern: kicker | This is the riders' unspoken line, not a summary. Ponnan says it aloud, with an edge, at 49. That payoff is why it stays. |
| 29 | "not to dance with crabs" | Scanner: comma_not | Raza Khan's own idiom (VOICE_BIBLE T5). |
| 45, 49 | "judges weight" / "This earth has judged hooves longer than you have ridden, Deccan man" | Holistic: idea said twice | The repetition is the point. Ponnan throws Nagoji's word back at him. |
| 49 | "Ponnan said quietly" | Pattern: soft adverb | This is one of the two adverbs the ration allows. A man who barely speaks, speaking low, makes the insult sharper. |
| 53-55 | "We will see whose tricks the Dutch remember" | Holistic: flab | It sets Ponnan's pride against Nagoji's, a rivalry the book draws on later. Keep it, with the simpler 51. |
| 75 | "This is not war," ... "This is labour." | Pattern: correction | This is the chapter's one kept correction. It is dialogue, from a mercenary who would say exactly this. |
| 77 | "The Dutch carry muskets that fire in volleys" / "like the tide, fast, from the angle they do not expect, and gone before they can reload" | Pattern: dialogue exposition, tricolon | Ramayyan says at ch6:163 that the Madurai horse do not know how to face guns, so this is a briefing, not a lecture. The three beats are the drill itself, and the tide is a coast image he has earned. Fix only "Precise. Mechanical." |
| 89 | "If we slip then, we die. If we turn true, they fire at ghosts" | Pattern: balanced antithesis | It passes the drill-ground test (voice rule 6): it tells a rider what to do and what it costs. |
| 111 | "You make them move like fish," ... "Not like bulls." | Pattern: correction | This is the king's coarse wit in its short form, and Nagoji's literal reply needs "bulls". Drop only "without preamble". |
| 129 | "Show me, Nagoji Sawant, that horses can disagree." | Holistic: states the theme | A royal order with a dry twist, and the king's one set line in the scene. Drop only "softly". |
| 145 | "a temper like monsoon lightning" | Pattern: stock horse description | Deccan weather, cited in VOICE_BIBLE as one of his own similes. Only "a stride that ate distance" goes. |
| 147 | "stood barely fourteen hands" | Holistic: English measure | Voice rule 10 makes hands the house measure. |
| 153 | "They were not beautiful. No raja would ride one in a procession." | Pattern: correction | Dry and concrete, and the concession is paid off at once in hooves and fodder (VOICE_BIBLE 6b). |
| 167 | "You do not belong to any of them either," I said softly. "Do you?" | Pattern: explained subtext; Holistic: on the nose | Talking to a horse is the one place he is allowed to be sentimental (VOICE_BIBLE section 5). It lands once 183's "belonging" is cut. The theme is then said twice: as an insult (7 and 49) and as sympathy (here). This is the second allowed adverb. |
| 171 | "It was not Kanka's smell. It never would be." | Pattern: kicker | Grief carried by a smell. The finality is a fact, not a moral. |
| 177 | "She tossed her head, as if agreeing to terms she had not yet heard." | Pattern: simile | A horse dealer's joke, and the chapter's one "as if". |
| 179 | "It was the first time since Vasai that I had named a horse." | Pattern: explained subtext | A literal first, and it matters. Only the second sentence explains. |
| 197 | "The Portuguese tried to convince me otherwise. It did not take." | Holistic: modern phrasing | Understatement about the Inquisition. "Take" in the sense of a graft or a dye taking is old usage. |
| 205 | "We built mosques. We kept the faith. But we also lit lamps at Hindu shrines when our ships sailed" | Pattern: tricolon | The one place the mixing of faiths is shown in practice. Everything after it only says it again. |
| 217 | "You are useful too, Sawant. That is why you are still alive." | Holistic: cut 215 to 217 | Dry and faintly threatening, and it echoes the king's warning at ch6:171. It gives Ibrahim an exit line with an edge. |

## Opening

Current lines 3 to 9:

> The first time I tried to make Madurai horses run in Malabar sand, they laughed at me.
>
> Not with their mouths. Horses do not waste breath on that. They laughed with every sideways step, every planted hoof that refused to drive, every rolling eye that said what the riders did not dare speak aloud.
>
> You do not belong here, Deccan man.

**Verdict: keep.** These are the best lines in the chapter.

- **The conceit is specific.** The horses "laugh" with feet and eyes, as a horseman would see it.
- **The unspoken insult is planted, then paid off.** Ponnan says it aloud at 49.
- **The tide paragraph (9) is terrain-first thinking.** Only "Arabian Sea" is in question.
- **The one open decision is line 5's correction shape** (see Borderline). I would keep it unless the author is clearing the correction opener across the book.

The sag comes after, at 11 to 23:

- the stock arrival kit ("lances gleaming", the hawk nose and scar)
- "Too confident"
- "his eyes missed nothing"
- a then/now recap of the Chapter 6 challenge, "grace" balanced against "weight"

The fixes in the tables above shorten this stretch by about 60 words and put the horses and the ground in front of the reader. That is what a cavalryman looks at first.

Nagoji's authority also needs one concrete source. He has ridden wet sand before: at Chaul, against Portuguese musketeers who flinched at an angled charge (ch1:55, ch6:151). The Chapter 6 audit makes that memory the core of his pitch to the king. A single clause here would ground the whole drill, for example at 89: “Us. We did this to the Portuguese near Chaul. We are the bait.” It would also stop the chapter from contradicting itself at 223.

## Ending

Current last lines (219 to 225):

> He walked away into the gathering dark.
>
> I stayed with Kayal a while longer, thinking about gods and usefulness and the strange tolerance of a king who measured men by their hands, not their prayers.
>
> On Deccan soil, I had thought I knew the limits of what a horse could do against a gun. Here, with the sea muttering at my back and wet sand underfoot, those limits shifted.
>
> Storms did not ask permission. Perhaps horses, taught well, did not either.

**Verdict: rewrite, mostly by cutting.** The ending breaks the style sheet five times:

- It restates Ibrahim's speech (221).
- It turns back to horses with no scene behind the turn (223), and that claim contradicts Chaul.
- Its last paragraph pivots on "Perhaps".
- It spends the storm motif, which is reserved for ch13:321.
- It repeats the closing idea of Chapter 1 ("Storms do not ask permission", ch1:113).

The line also has no concrete meaning. It has the shape of wisdom without the content.

Proposed ending, from 215:

> He pushed off from the tree.
>
> “You are useful too, Sawant. That is why you are still alive.”
>
> He walked off toward the cook fires.
>
> When he had gone I ran my hand down Kayal’s near foreleg. She lifted the hoof before I asked, and I dug the sand out of it with my thumb. There was very little to dig.

Why this ending:

- **It ends on an act.** Her trust shows in what she does: she lifts the hoof before he asks.
- **It pays off the chapter's ground** without comment: the sand that "drinks the hoof" (31) and the hard, narrow hooves that shed water (153). A horse whose hoof holds almost no sand is a horse for this beach.
- **It lets Nagoji answer Ibrahim's talk of gods by going back to a horse.**
- **It shares no closing idea with any other chapter.**

A plainer fallback is to stop at "He walked off toward the cook fires." That ends on Ibrahim's line and a movement.

I prefer this ending to the OEM draft (the cook fires burning low, then Kayal pushing her nose back into his palm). That draft repeats the nose push at 169 and the hand-and-salt beat at the new 183.

The two section endings change as well:

- **Section one** ends on the new 135: Nagoji already sorting the horses in his head. This replaces "Anticipation."
- **Section two** ends on "That night she only wanted the salt off my hand."

## Flab

| Lines | Problem | Action |
| :- | :- | :- |
| 11-23 | Stock arrival kit, "Too confident", "eyes missed nothing", then a then/now recap. | Fixes at 15, 17 and 23; borderline items at 11 and 13. About 60 words saved. |
| 45-55 | Two maxims side by side and a mirrored reply. | Cut "It punishes force." and simplify 51. Keep 47 to 49 and 53 to 55. |
| 63-65 | A named emotion, then a slogan added to good advice. | See the table. |
| 73-81 | Weather filler, "Precise. Mechanical.", the tide proverb, "Exactly." | Go from 77 to the driftwood with one sour line from Raza Khan. About 35 words saved. |
| 101-109 | The change is summarised twice (101 and 103), with staging clutter at 105 to 109. | Keep 101 trimmed. Cut 103. Fix 105 and 107 to 109. |
| 111-139 | Every speaker closes on a maxim, then a gaze to the horizon, then an inventory of emotions. | Keep 111 (trimmed), 117, 129 (trimmed) and 131 to 133. Replace 121 to 125, 127, and 135 to 139. About 90 words saved. |
| 145-157 | About 465 words of essay: climate, prices, breeds and doctrine. 147 and 153 both open "were different". 149 contradicts 153. 155 restates 69. "Shock troops". This block is the unpublished post-build addition (`SOURCE_OF_TRUTH.md` Decision 2). | Compress to about 200 words, keeping the horseman's knowledge (REVIEW_BACKLOG C10-14 asked for exactly this). Worked text below. |
| 159-163 | A pivot line and a fragment catalogue. | Merge into 161 (see the table). |
| 171-183 | Kicker, dictionary gloss, explanation, life maxim, summary of the theme. | Cut 173 and 181. Trim 171, 175, 179 and 183. This keeps about two thirds of the passage, the same ratio VOICE_BIBLE section 5 found. |
| 187-203 | Stage beats: the half-shadowed face, "It was not a question", a quiet moment. | Cut the beats and keep every line of dialogue. |
| 207-225 | The theme said four times (209, 217, 221 and 223), then a return to horses with no scene behind it. | Keep 205, 211 to 213 and the first two sentences of 217, then the new ending. About 150 words saved. |

Worked text for 145 to 157. Every sentence comes from the chapter except the Bhima line; nothing else is invented.

> In the Deccan I had ridden Kanka, a black stallion with a temper like monsoon lightning. The Portuguese shot him when they took me.
>
> The horses here were smaller, most of them. The Maravar ponies stood barely fourteen hands, rough-coated and watchful. The Madurai horses were taller, bred for show as much as war, and not yet sure of wet ground.
>
> On the Bhima we bred our own horses. On this coast nobody bred them at all. The monsoon rotted hooves, and the wet bred sores and fevers that could kill a horse in a week. Every war horse here had come by ship or down through the passes, and each one cost more than a soldier earned in a year. A good Madurai charger was fifty pagodas bought young, and a proven one twice that. Arabs cost three or four times as much and did worst of all. I had seen them come off the ships sleek and proud and within a season turn dull-coated, their legs swelling from standing in mud.
>
> The Maravar ponies were not beautiful. No raja would ride one in a procession. But their hooves were hard and narrow and shed the water, their rough coats turned the rain, and they ate the coarse grass between the paddies, fodder that would give a Madurai charger colic. Ramayyan had shown me the accounts once, tapping each line with his stylus. More coin went to feeding and replacing horses than to paying the men who rode them.

This version drops "Kerala", "shock troops", "smart", the without/with antithesis, the "in their bones" cliché and the contradiction about where the Maravar ponies come from. Now they too come "down through the passes".

## Passages to protect

These should be kept word for word, apart from the small fixes noted.

- **3 to 9.** The laughing horses, the unspoken "Deccan man", and the tide strip that "looked inviting to a cavalryman who had never tried to stop a charge on such footing".
- **29 to 31.** "My men ride to break lines, not to dance with crabs." / "Here the ground lies to you. It looks firm, but it drinks the hoof." Only the "target" tag changes.
- **35.** "One pass. To show you there is no magic in sand."
- **41.** "When they tried to turn, their weight carried them deep. Hooves sucked into the slurry. Legs flailed."
- **47 to 49.** Ponnan's retort, "Deccan man".
- **57 to 61.** "It is a bog," he spat. / "If you cannot fight where they stand, why did you take the king's coin?"
- **67 and 71.** "We spent the morning in that slurry." / "He does not force the step. He waits for the sand to hold him."
- **83 to 89.** The driftwood map, and "they fire at ghosts".
- **95.** "It is better than riding into the teeth and staying there."
- **101, from "The Madurai horses stopped fighting the ground" on.** "the heavy, sucking pause of the sand".
- **117.** "But they are less foolish than they were at sunrise."
- **143.** The picket line after the horses are rubbed down.
- **151 and 153, the horseman's knowledge.** Arabs going dull-coated with swelling legs; hard, narrow hooves; coarse grass; colic.
- **157.** "More coin went to feeding and replacing horses than to paying the men who rode them."
- **165 to 171.** The salt and sweat on his palm, the nose pushed into his chest, and "It was not Kanka's smell. It never would be."
- **175 to 177.** "we will show them what a backwater horse can do" / "as if agreeing to terms she had not yet heard".
- **189.** "I have seen men talk to worse."
- **197 to 199.** "It did not take." / "touch the wall of a mosque without spitting".
- **205.** The lamps at Hindu shrines and the Christian priests blessing cargo.
- **213.** "The king cares that I bring him information and that I do not sell it to the Dutch first."

## Chapter-specific notes

These are continuity, history and copyedit points noticed during the audit. None of them is slop, but most are cheap to fix in the same pass.

**Continuity**

1. **Ponnan's name.** He is "Ponnam Pandya Deven" at 17 and 25 but "Ponnan" everywhere else in the book. Give the full name once, as "Ponnan Pandya Deven" at 17, and use "Ponnan" at 25 (REGISTER house list; REVIEW_BACKLOG N-42).
2. **Kanka.** At 145 Kanka is a black mare who died at Vasai. In Chapter 1 (ch1:53 to 55) he is a male horse shot when Nagoji was captured, and Chapter 6 (ch6:31, 151) agrees with Chapter 1. REVIEW_BACKLOG BL-01 recommends the Chapter 1 version, which also turns "since Vasai" at 179 into "since Goa". If the Vasai version is kept instead, "walked the last miles to Goa on foot" cannot stand: Vasai is several hundred miles from Goa, and any distance he gives should be in kos (REGISTER). Chaul and Goa are also Konkan, not "the Deccan".
3. **Kayal.** At 183 Kayal is promised for Colachel, but she is never named again. Chapter 8 (ch8:89) mentions a gelding, ch14:101 has an unnamed "him", and ch16:5 mourns a mount "lost in the storm" that never existed. This needs the book-level fix (REVIEW_BACKLOG N-03; OEM section 7); the Borderline entry for 183 depends on it.
4. **Chaul and the feint.** Nagoji has ridden wet sand near Chaul (ch1:55, ch6:151). Ramayyan tells the king that the Madurai horse "do not know the feint and vanish the way Deccan riders do" (ch6:163). Yet this chapter presents both the footing and the bait-and-turn as things Nagoji is working out on the spot, and 223 calls the lesson new. The one-clause Chaul reference suggested under Opening fixes this and makes the tactic Maratha (the old light-horse way) instead of improvised.
5. **The king's language.** In Chapter 6 every word the king says reaches Nagoji through Ramayyan's Konkani, and Nagoji suspects the king understands more than he lets on (ch6:107). Here the king speaks to him directly at 111, 117 and 129 with no interpreter. Either restore the interpreter once ("Ramayyan put it into Konkani"), or make the king's first direct words to Nagoji a moment Nagoji notices. Neither auditor flagged this.
6. **The hand.** His fingers are bandaged at ch6:31 and ch8:9, and Chapter 1 leaves his left thumb damaged. Chapter 7 never mentions the hand, though he handles reins, driftwood and a hoof. One touch would keep the thread: "I held out my bandaged hand" at 165, or "with my good thumb" in the proposed ending.
7. **Counting.** Chapter 6 (ch6:171) gives him "a hundred Maravar riders", but this chapter never counts anything, although counting is his voice (voice rule 4). One number, at 11 or 17, would help. The number is for the author to set.
8. **Echoes in other chapters.** ch20:412 repeats the tricolon from 137 ("since Goa, since the dungeon, since the storm"); cutting 137 here leaves Chapter 20's. ch17:25 repeats "eyes missed nothing"; the fix at 17 frees it for Chapter 17. ch11:7 speaks of "the Nairs we had drilled in the wet sand", but this chapter drills only Madurai and Maravar horse (REVIEW_BACKLOG N-51).
9. **Two lines that answer each other.** "Horses do not argue" (191) answers the king's "horses can disagree" (129). Keep both, or neither.

**History and register**

1. **The Nayak of Madurai (13).** "The Nayak of Madurai sends his horse as promised." The Nayak line ended in 1736, and in 1740 to 1741 the Carnatic was a Maratha war zone (Raghuji Bhonsle took Trichinopoly in 1741), which Nagoji would know. REVIEW_BACKLOG N-26 suggests: “We rode for Madurai's old Nayaks, and for your king before.” The matching fix at ch6:141 is in the Chapter 6 audit.
2. **Dalawa (105).** "Diwan" is a post-1809 Travancore title (REGISTER, rated P1). The Chapter 6 audit proposes that Nagoji learns the word "Dalawa" there. Use it here.
3. **Word by word.**
   - "Shock troops" and "smart" (155): both cut with the paragraph.
   - "Kerala" (149): replaced in the worked text.
   - "Sabre" (89): use talwar.
   - "Boots" (201): replaced. At 129 it is the king's word for the Dutch and can stay.
   - "Arabian Sea" (9): see Borderline.
   - "Hindustani" (13): Dakhni.
   - "They wore no uniforms" (17): a European expectation, and no Maratha army wore uniforms.
   - "Mundus" (17): a Malayalam word used for Tamil Maravar dress. Replaced by "white cloths". If it is kept, italicise it (REVIEW_BACKLOG C18-04).
4. **Maravar ponies (153).** Maravar country (Ramnad, Tirunelveli) lies east of the ghats. The worked text brings the ponies through the passes. The Chapter 6 audit also notes that Maravar in Travancore service were mostly foot soldiers. The book consistently makes them cavalry, so this is only a flag.
5. **Prices (151).** I have not verified the pagoda figures. They read as a veteran's hedged estimates, which is how the voice bible praises them, so keep them unless a source says otherwise.
6. **The "Christian merchant ... in the same war hall" (217).** This goes with the cut. Kept, it would point at Mathu Tharakan, who was born in 1741 (REGISTER).
7. **Khandoba (201).** The book never names Nagoji's god. Khandoba of Jejuri rides a horse and is a common Maratha family deity, which suits a huzurat trooper named Sawant. Tulja Bhavani is the alternative. This is the author's call.

**Copyedit**

- "King" is capitalised at 33 and 61 and lowercase everywhere else. Use lowercase.
- UK spelling: "recognized" (161) becomes "recognised" (REVIEW_BACKLOG F12-04). This is moot if 161 is rewritten as proposed.
- Apostrophes are straight at 105, 123, 127, 149, 151, 157, 161, 171 and 187, and curly elsewhere. Make them all curly.
- "the southerners' clumsiness" (43) is ambiguous, since both troops are southern. Use "the Madurai men's clumsiness".
- "The Madurai rider" (33) means Raza Khan, their commander. Use his name (handled by the fix at 33).
- "the simple release" (25) is an unclear drill term. The next three sentences already describe the drill, so "We begin with the simplest thing" would do.
- "wet earth" (83) is on a beach. Use "wet sand".
