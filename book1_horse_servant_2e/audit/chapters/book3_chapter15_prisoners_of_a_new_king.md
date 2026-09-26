# Second-Edition Audit: Chapter 15, Prisoners of a New King

- Source (frozen first edition): `book1_horse_servant/book3_chapter15_prisoners_of_a_new_king.md`, 331 lines, 3,957 words.
- Method: I read the whole chapter and ruled on every flag from the pattern auditor (95 flags) and the holistic reader (25 passages), merging duplicates. I ran `audit/tools/scan_slop.py` on the chapter and cross-checked Chs 9, 11, 13, 14 and 16 and STYLE_SHEET, VOICE_BIBLE, OPENINGS_ENDINGS_MOTIFS, REGISTER_AND_ANACHRONISM, REPETITION_AND_DENSITY, REVIEW_BACKLOG and SOURCE_OF_TRUTH. Line numbers refer to the first-edition file.
- Scanner counts, with the style-sheet ration in brackets: "not ... but" 6 plus 2 comma-not; "as if" 3 (1); "like a" 6 (2); slowly, quietly and softly 7 (2); "the weight of" 2 (0); fragments 7 (3); one-sentence paragraphs 36. The scanner misses the "with the [noun] of a man who" frame (L37, 73, 75, 133, 199, 297) and the two-sentence "not X. They were Y" (L65, L67), so check those two by hand.

## Verdict

| Measure | Call |
|---|---|
| Severity | **4 of 5** |
| Recommended intensity | **Deep** (line-level re-voicing of the surrender, the audience and the coat scene; cuts and tics elsewhere) |
| Estimated word cut | **About 25%** (3,957 to about 2,950 words) |

The plot is sound and much of it is good: the broken terms, the sword in the sand, the cavalry fight on wet sand, the offer in the stone room, the coat left folded on a bench. The machine layer sits on top of it in four ways.

1. **Stacked climaxes.** The surrender (L43 to 61) piles up white knuckles, a drummer boy, "something passed between them", four "He looked at" sentences, a sword ritual with a boyhood backstory, "A quiet death for a quiet surrender", a cracking voice, and a weeping tableau with a simile. Each beat explains the one before it.
2. **Explained subtext and mind-reading.** Nagoji hears a quiet Dutch aside he could neither hear nor understand (L39), knows Donnadi's boyhood (L55), knows what Lannoy "knew enough of war to know" (L191), and reads "loyalty ... warring with reality" in his eyes (L243). Three times the narrator tells the reader what a scene has just shown (L155, L173, L225).
3. **Morals at every exit.** The chapter has five sections, and every one closes on a moral or a prophecy: L67 (the sea that failed them), L111 (enemy against friend), L161 (let myself breathe), L277 ("They did not know it yet"), and L329 to 331 ("History is strange" plus a destiny). In every case the fix is a cut back to an image or a line of dialogue that is already there, or one sentence.
4. **One voice for everyone.** Varma, Ramayyan, Tharakan, Ibrahim, Dhanaji and Nagoji all speak in maxims, and the one-word correction template ("Generous." / "Practical," he corrected; "useful" / "a weapon") appears twice (L97 to 99, L263 to 265). VOICE_BIBLE 3.9 gives the swap test. Varma is best when terse and coarse (L63, L125, L247). Ramayyan is best cold and administrative (L35's first sentence, L41). Ibrahim is best sly and commercial (L91, L109). Nagoji is best blunt and horse-minded (L139 to 149, L235, L287).

The modern register clusters in the audience: "red ink", "written you off", "beachhead", "corporate master", "draw up the papers", "You start tomorrow", "isn't", "complicated". Apart from L45 and L175 the chapter never uses the Deccan as a frame of reference, and the proposed L321 fix adds one.

## Confirmed issues

| Line | Quote | Category | Suggested fix |
|---|---|---|---|
| 3 | "The end came with a lie, or perhaps just a misunderstanding of what honour meant on this coast." | signposting | Cut. See Opening. |
| 5 | "He carried terms, counter-terms, and the slow grinding of pride against reality." | tricolon | "He carried terms one way and counter-terms back." ("the slow grinding of" also appears at Ch 10 L191.) |
| 7, 9 | "Terms had been agreed upon, or so they believed." / "They marched out of their ruined camp at mid-morning." | signposting | Cut both. L5 has already dated the march-out, and "at mid-morning" folds into the opening rewrite. |
| 11 | "It was a strange sight." | stock_phrase | Cut. Begin the paragraph at "Beaten men". |
| 19 | "silent, impassive." | stock_phrase | "His Nair infantry lined the path the Dutch were taking, spears grounded." (This sets up "Spears lowered" at L25.) |
| 21 | "the trap snapped shut." | stock_phrase | "When the last Dutch soldier had stepped clear of the charred stockade, Marthanda Varma lifted his hand." Keep L23, "A conch blew." |
| 25 | "Suddenly, the Nair lines thickened." | soft_adverb | "The Nair lines thickened." |
| 27 | "Confusion rippled through their ranks." | stock_phrase | "The Dutch column halted, and the men at the back walked into the men in front." |
| 31 | "You are prisoners of the State of Travancore." | modern_register | "You are the Maharaja's prisoners." |
| 33 | "his face darkening with rage" | stock_phrase | Cut the tag. The shouted line carries the anger. |
| 35 | "Did you think we would simply wave goodbye?" | modern_register | "Did you think we would hold the road open for you?" |
| 37, 39 | "His voice was calm, carrying the weight of a man who had already calculated the odds." / "“Joseph,” he said quietly, in Dutch. “Look around you. ...”" | pov_logic | "De Lannoy stepped out of the Dutch ranks and spoke to Donnadi, low and quick, in their own tongue. I could not hear it, and I would not have understood it if I had." Nagoji is in the saddle by the dunes, cannot hear Donnadi at L47, and has no Dutch. If the words matter, frame them as later report: "Months afterwards he told me what he had said: that there was no battle left to win." This also removes an echo of Ch 14 L163 ("a man who had already decided"), a page earlier and about the same man. |
| 41 | "Ramayyan said calmly" | soft_adverb | "Ramayyan said." Keep the line. |
| 43 | "I saw Donnadi's knuckles turn white on his hilt." | stock_phrase | "Hands tightened on musket stocks, and Donnadi's hand was on his hilt." |
| 45 | "on my own in the Goan dungeon. The moment when a man realizes that every road leads to the same wall." | kicker | "I had seen that look on Keshavrao in the storm, and I had worn it myself in the Goan dungeon." Cut the last sentence. |
| 49 | "Something passed between them, permission, perhaps, or apology." | abstract_depth | Cut. "Donnadi put a hand on the boy's shoulder. The boy's face crumpled, then steadied." |
| 51 | "He looked at the thousands of fresh Nair troops ringing them. He looked at the sea behind him, where the ships had drawn back like spectators who did not want to be splashed by blood. And he looked at De Lannoy, who had spoken the truth no one else dared say." | tricolon | "Then he looked at De Lannoy." One sentence in place of four. The ships are already turning away at the end of Ch 14. |
| 55 | "the leather warm from his body ... I saw his thumb trace the Company insignia, the VOC monogram that had been his identity since he was a boy in the Low Countries dreaming of foreign shores." | pov_logic | "He did not throw it. He held it a moment, the brass of the hilt catching the sun." Cut the rest. That leaves the thumb on the insignia to Lannoy at L289, where it belongs. |
| 57 | "It landed in the sand with a soft thud, not a clatter. A quiet death for a quiet surrender." | kicker | "Then he let it fall into the sand." (This also removes the contradiction with L61's "clatter".) |
| 61 | "Others stood rigid, staring at nothing. One sergeant knelt and pressed his forehead to his fallen weapon, as if saying goodbye to an old friend." | simile_stack | "Some of the men wept. One sergeant knelt and pressed his forehead to the stock of his musket." |
| 65 | "his eyes were not on the ground. They were on the walls of Udayagiri, as if he were already measuring them for improvement." | pov_logic | Cut from L65. Udayagiri cannot be seen from the Colachel beach. The image moves to L67. |
| 67 | "We did not march them to Kanyakumari. We marched them inland, away from the sea that had failed to save them, to the granite walls of Udayagiri Fort." | summary_ending | "That afternoon we marched them inland to Udayagiri. At the gate De Lannoy stopped and looked up at the granite walls, and the guard behind him had to push him on." |
| 73 | "He came not from the inland roads but from the sea itself, his small boat sliding through the surf with the ease of a man who had spent his life reading these waters." | correction | "He came by sea, his small boat riding in on the surf, and a second boat behind it loaded with crates and bundles wrapped in oiled cloth." |
| 75 | "his bare feet finding purchase where Dutch boots had stumbled. He surveyed the wreckage of the company camp with the eye of a merchant appraising goods at auction." | simile_stack | "I watched from the dunes as he waded ashore and stood looking over the wreck of the Company camp. I could see him pricing it." |
| 93 | "It was not salvage, I realised, but supplies. Rice. Dried fish. Coconut oil. The small necessities that an army needs after a battle." | correction | "His crew had begun unloading the second boat: sacks of rice, baskets of dried fish, jars of coconut oil." |
| 97, 99 | "“Practical,” he corrected. ... He shrugged. “A man who is remembered kindly by both sides is a man who survives.”" | correction | "“Generous,” I said. / “Marthanda Varma will remember who fed his prisoners,” Ibrahim said. “And if the Dutch ever come back, they will remember who fed their countrymen.”" This drops the correction template, the maxim and one of Ibrahim's five shrugs. If the author wants Ibrahim ahead of the court, keep "his new recruits" and add: "“Recruits?” I said. He only smiled." |
| 101 to 105 | "Is that all you care about? Surviving?" / "for a moment the merchant's mask slipped." / "But the Marakkars remain. ... the sea belongs to no one. It only lends itself to those clever enough to use it." | stock_phrase | Cut all three paragraphs. Ch 11 L405 already has Ibrahim's mask slip, and Ch 11 L407 and Ch 13 L205 have his sea line. VOICE_BIBLE names L105 as the example of Ibrahim's drift into mission statements. |
| 111 | "and wondered which was more dangerous: an enemy you could see, or a friend you could never quite trust." | summary_ending | Cut. The section ends on L109, "For the usual consideration, of course." |
| 115 | "The victory did not give us the luxury of rest." | stock_phrase | Cut. Open the section on L117. |
| 117 | "Before the prisoners were fully counted ... Fresh men. Blue coats. Not a fleet, but enough to be dangerous if they reached our exhausted lines" | fragment_list | "The same morning Ramayyan's runners brought word from the south. A boat had slipped in under the headlands at Kanyakumari and put fresh men ashore, a few dozen blue coats, enough to do harm if they reached our lines while half our men were guarding captives and dragging cannon out of the wreck." |
| 121 | "I will not let the company write a second ending to this battle while my men are drinking water." | modern_register | "I will not let them take back on the road what they lost on the beach." |
| 131 | "coconut palms blurring into a green wall. The wind off the sea stung my eyes. My ribs ... protested at every stride. I clenched my jaw and rode through it. Pain was a tax you paid for staying alive." | kicker | "We went south at a gallop along the beach track. My ribs, bruised in the charge, caught at every stride." |
| 133 | "ran here like a scar, and the Dutch had found a weak stitch. ... moving with the quick confidence of men who believed the war had not yet been decided." | simile_stack | "The trenches and palm-log barricades we had thrown up for the siege ran down to the stream, and where they crossed the water there was a gap. A handful of blue coats had come through it in the early light, bayonets fixed." |
| 135 | "Far enough to taste the idea of escape." | fragment_list | Cut. These are a relief party, not men escaping. |
| 141 | "They tried to reset. They tried to lock into the comfort of drill. But drill is a luxury when hooves are already inside your breath." | modern_register | "Their sergeants bawled at them to dress their ranks, but by then our hooves were inside their breath." This keeps the live image and loses "reset", the maxim, and the second "luxury". |
| 143 | "Steel met steel. ... Another man fired point-blank and missed, the recoil turning his musket into a club. I took him with the flat of my blade, not out of mercy, but because we needed prisoners who could speak." | stock_phrase | Cut "Steel met steel." Then: "Another fired at me point-blank, missed, and came on swinging the empty musket by the barrel. I took him with the flat of my blade. We needed prisoners who could talk." (Recoil does not turn a musket into a club.) |
| 145 | "It lasted minutes. It felt like an hour." | balanced_antithesis | Cut, or "It was over in less time than it takes to water a horse." |
| 147 | "his face pale with shock at how quickly a victory can be taken away." | explained_subtext | "...leaving two dead and three wounded on the sand. Their officer went with them, limping between two of his men." |
| 155 | "I knew what Ramayyan meant. Here, on broken sand and shallow water, their discipline became a burden. Under their own stone, with clear ground and prepared fire, it would become a weapon again." | explained_subtext | Cut both sentences. See Flab on the runner. |
| 159 | "Today they learned that even the road home has teeth." | kicker | "“Let them run,” I told my men. “Let them tell Kanyakumari what they met.”" (This was the third "teeth" in the chapter.) |
| 161 | "Only when the last blue coat had vanished into the haze did I let myself breathe." | summary_ending | Cut. The section ends on L159. |
| 167 | "The air here was different, still heavy with moisture, but held close by the hills and the high walls. ... guards who never blinked." | stock_phrase | "The Dutch officers had been separated from their men and kept in the upper quarters, better fed than the common prisoners and never out of a guard's sight." |
| 173 | "He was no longer just the merchant ... breaking centuries of caste tradition ... It was a statement as loud as any cannon: in this new Travancore, power flowed to those who built the state, regardless of the god they prayed to." | explained_subtext | "And beside him sat Mathoo Tharakan, the merchant from the war council, now in the gold chains and silk of a *Sarvadhi Karyakkar*. The king had seated a Syrian Christian among the great men of his durbar." L175 then does the arguing in Nagoji's voice. (This depends on N-27; see Notes.) |
| 177 | "I stood by the door, silent witness." | stock_phrase | "I stood by the door." |
| 191 | "He knew enough of war to know that the loser does not dictate the vocabulary of the aftermath." | explained_subtext | Cut. "Lannoy fell silent." is enough. |
| 199 | "“And books with too much red ink are burned,” Tharakan interjected softly, his voice carrying the weight of a man who owned half the warehouses on the coast." | modern_register | Cut. The line repeats L37's "weight of a man who" and Varma's "their books are bleeding" (Ch 13 L93). If Tharakan needs a line, give him a price: "“A captain costs them less than a ship,” Tharakan said." |
| 201 | "“It has already written you off,” the king continued, nodding at his noble. “Do you think they will send a fleet to rescue a man who lost a beachhead?" | modern_register | "“It has already struck your name out,” the king said. “Do you think they will send a fleet for a man who lost them Colachel? They will count the cost, shake their heads, and hire a new captain.”" "Beachhead" dates from the 1940s. Neither auditor caught it. |
| 203 | "Ramayyan had already shown him damp letters ... Varma did not need enemy ink to know the truth, but he enjoyed hearing it from their own mouths." | pov_logic | Cut the paragraph from the scene. As placed, it cuts the flinch at L205 off from its trigger ("hire a new captain"), and its last sentence mixes metaphors. A letter from Kochi admitting defeat could not already be in the wrecked camp two or three days after the battle. If the letters stay, put them before the audience, after L169: "Ramayyan had already shown him letters taken from the camp: the garrison's pleas to Kochi for men and powder, and Kochi's answers, which promised both." Give the Governor's sentence to the Historical Note with its real source and date. |
| 205 | "It was a small movement, but it betrayed him." | explained_subtext | "Lannoy flinched." |
| 217 | "Not as a guest, but as a prisoner. You will rot here while the world forgets your name." | stock_phrase | "“Then you stay in Udayagiri,” Ramayyan said. “You will rot here, and die of fever or old age, wondering what you might have built.”" This keeps "rot" and "built", which throw De Lannoy's own words from Ch 14 L155 back at him. |
| 225 | "It was a staggering offer. To go from a prisoner in a dungeon to the commander of the army that had defeated him." | explained_subtext | Cut. It also contradicts the "upper quarters" of L167. |
| 243 | "The silence stretched. I could see the calculation in the Dutchman's eyes. The loyalty to a distant flag warring with the reality of the stone walls and the indifference of the corporate master he had served." | explained_subtext | "Lannoy said nothing for a long while. He picked at a scorched thread on the cuff of his coat." This plants the coat for L283. |
| 247 | "a smile touching his lips" | stock_phrase | Cut the tag. |
| 249, 317 | "Lannoy nodded slowly." / "He nodded slowly." | soft_adverb | "Lannoy nodded." Cut L317. Most of the other soft adverbs (L39, L41, L105, L199, L297) go with the fixes in their own rows. |
| 255 | "Ram will draw up the papers. You start tomorrow." | modern_register | "Ram will have it written. You begin tomorrow." Keep "Ram" (see Defended). |
| 259 | "The war isn't over just because you surrendered ... There is always work. Go. Sleep. You will need your strength." | modern_register | "“The war is not over because you have surrendered,” Varma said. “There are other factories, and other chiefs. Go and sleep.”" |
| 263, 265 | "“He will be a weapon,” Varma said. “And like any weapon, we must make sure he points away from us.”" | correction | "“He will be useful,” the Dalawa said. / “So is a cannon,” Varma said. “Mind which way it points.”" |
| 269 | "Watch him. Be his friend holding the shield." | other | "Watch him. Be his friend, and keep your shield on your arm." Neither auditor flagged this. As written the idiom does not parse. |
| 271, 273 | "Friendship with a man who walked away from his own flag is a complicated thing" / "“Life is complicated,” ... “That includes surviving it. The simple things usually end in funerals.”" | modern_register | "“It is hard to be a friend to a man who has left his own flag,” I said. / “I have managed it with a Maratha,” Marthanda Varma said, rising and reaching for his spear." |
| 275 | "The Dutch prisoners, no, the Dutch recruits, were being fed in the lower yard. They looked up as we passed, fear mixing with curiosity." | correction | "We walked out into the courtyard. The sun was high now. In the lower yard the Dutch soldiers were eating Ibrahim's rice, and they looked up as we passed." This ends the section on an image and gives the Ibrahim scene a consequence. Only Lannoy has accepted by this point (L241), so "recruits" comes too early. |
| 277 | "They did not know it yet, but they had just become the seed of the Travancore Nair Brigade." | signposting | Cut. "Nair Brigade" is the 1818 name (REVIEW_BACKLOG RV-02). |
| 295 | "He stood very still for a long moment." | stock_phrase | Cut. The same phrase appears at Ch 18 L125. |
| 297 | "Then, slowly, he unbuttoned it. The brass clicked softly in the morning quiet. He folded the coat with the care of a man folding a shroud" | simile_stack | "Then he unbuttoned it, folded it square the way a good groom folds a saddle cloth, and set it on the stone bench beside him." |
| 301 | "looked at it as if it were a map of an unknown country." | simile_stack | "He picked up the white *mundu* and turned it over in his hands, looking for a button or a string." |
| 307 | "he looked like a ghost of himself, a European skeleton wearing Indian skin." | simile_stack | "When he straightened, his shins showed below the hem, whiter than the cloth." The original image is incoherent (a mundu is cloth, not skin) and racialized. |
| 315 | "Not your old rank. Not your old flag. Something new. Competence. Fairness. The willingness to stand in the same sun and eat the same rice." | modern_register | "“You show him something he respects,” I said. “Stand in the same sun he stands in, and eat what he eats.”" |
| 319 | "is going to take some getting used to." | modern_register | "“The rice,” he said, “will be harder than the cloth.”" Keep the joke; only the idiom changes. |
| 321 | "“So is everything else,” I said. “Welcome to Travancore, Kappittan.”" | stock_phrase | "“I still dream of bhakri,” I said. “Eat the rice, Kappittan.”" (Ch 9 L56 plants "Rice instead of bhakri".) |
| 323 | "But something in his face shifted, the first crack in the wall between what he had been and what he might become." | abstract_depth | "He did not smile. He sat down on the bench beside the folded coat and pulled on the sandals." |
| 325, 327 | "He had not thrown it away. Perhaps he never would." / "But he was not wearing it." | kicker | See Ending. |
| 329 | "History is strange. It turns on a lucky shot, a broken promise, and a conversation in a stone room." | summary_ending | Cut. It repeats Ch 12 L147's closing idea, "The world turns strangely." |
| 331 | "But with Lannoy's help, I knew they would become stronger. And Travancore ... would become something no one, not even the great Companies of Europe, could swallow." | summary_ending | Cut. |

## Borderline

| Line | Quote | Ruling |
|---|---|---|
| 17 | "The King does not let tigers walk away because they promise not to bite" | Good banter from the saddle, and the holistic reader protects it. But the book reserves the tiger for the king (OPENINGS_ENDINGS_MOTIFS), and here it stands for the Dutch. Keep the shape and swap the animal for a horseman's hunt: "The King does not let a speared boar walk off because it promises not to charge." |
| 59 | "his voice cracking on the word." | A shouted order carries, so Nagoji could hear the crack. Keep it if the L45 to 57 cuts go through, since it would then be the only emotional beat left in the surrender. Cut it if the scene still feels heavy. |
| 71 | "The next morning, before the prisoners had even been sorted and counted, Ibrahim Marakkar appeared at the beach." | The prisoners went to Udayagiri at L67, and L117 reuses the "before ... counted" opener. "The next morning Ibrahim Marakkar came to the beach." |
| 79 | "“The sea moves quickly,” he replied. “I merely follow its currents.”" | A retort, not an oracle, but it adds one more sea line to Ibrahim's pile. Drier: "“The tide was with me,” he said." |
| 95 | "not starved into uselessness. This is my contribution." | Wordplay on "useful" and a modern "contribution". Trim to "“For the prisoners,” Ibrahim said, following my gaze. “The king will want them alive.”" |
| 129 | "“If you are going to ride into trouble,” he said, “I will be close enough to drag you out.”" | A stock sidekick line, but loyal and harmless. Dhanaji's own register is camp wit: "“Someone has to bring your horse back,” he said." |
| 175 | "But the Syrian houses of this coast were not meek converts huddled outside the warrior order." | This is Nagoji correcting his own Deccan assumption, which is legitimate, but the frame is the correction tic. "But the Syrian houses of this coast trained in the same kalari pits as the Nairs ..." does the same work. |
| 189 | "Dead men have no honour." | This is the middle one of three maxims. Cut it. Keep "Honour is eating well and sleeping without fear" and "That is the only term that matters", which pays off Donnadi's "We have terms!" (L33). |
| 219 | "He looked at the window, where the green hills of Travancore rose against the sky." | This is scenic filler, and it starts a second "He looked at" run after L51. "Lannoy looked at the stone floor, then at the window." |
| 223, 261 | "You keep your sword. You keep your rank. You rise as high as your skill takes you. You become the Valiya Kappittan" / "the new Great Captain" | A formal offer can take anaphora, but a title on the first day telescopes history and clashes with Ch 16 L179 ("We will see what kind"). "You keep your sword and your rank. Serve me well and you will be my Valiya Kappittan, the Great Captain of my forces." At L261: "As the guards took Lannoy out". |
| 231 | "I just found a paymaster who offers more than coin." | The line is in voice, but "just" is modern filler. "I have found a paymaster who offers more than coin." |
| 257 | "“Tomorrow?” Lannoy looked surprised." | A mild tell. "“Tomorrow?” Lannoy said." |
| 293 | "The coat cannot follow you where you are going." | The first two sentences ("Your mother is in Arras. You are in Travancore.") are blunt and in voice. The third turns them into an aphorism. Cut it. |
| 311 | "The cloth is easy. The hard part is what happens when" | The substance is concrete and good, but the cadence is self-help. "That will come. Your first order is the harder thing, when a Nair captain looks at your pale face and wonders why he should obey it." |

## Defended (flagged, keep)

| Line | Quote | Flagged by | Reason to keep |
|---|---|---|---|
| 25 | "blocked by a wall of shields" | Pattern (stock) | Literal. Nair infantry carried shields, and the phrase describes what closed the road. |
| 41 | "“You have marched out,” Ramayyan said ... “Now you will drop the arms.”" | Holistic (one of L37 to 41 could go) | This is the cold twist on the terms: they were allowed to march out with arms, and they did. Only "calmly" goes. |
| 43 | "They were surrounded, outnumbered twenty to one, starving and shocked, but they were soldiers." | Pattern (kicker) | This is a soldier's judgment and the reason Nagoji fears a fight. It explains his fear, not the image. |
| 47 | "The boy could not have been more than fourteen." | Both (stock age estimate) | Hedged estimates are how Nagoji thinks (VOICE_BIBLE, "what to keep"). The boy is what Donnadi looks at before he gives in. |
| 49 | "The boy's face crumpled, then steadied." | Holistic (paired beat) | Visible action seen through the glass, with no interpretation added. It stays once "Something passed between them" goes. |
| 61 | "sounded like a heavy rain" | Pattern (contradiction, generic) | The contradiction goes with the L57 cut. The simile comes from Nagoji's monsoon world and counts as one of the chapter's two. |
| 139 | "not elegant in this ground, but heavy enough to make Dutch shoulders flinch" | Pattern (correction) | A horseman's concessive judgment of other horsemen, not a reveal. Keep it as the chapter's one narrative "not ... but". |
| 149 | "My horse wanted to follow. So did my blood." | Pattern (kicker) | Bodily and a horseman's instinct, and the holistic reader protects it. It earns its tidiness. |
| 171 | "No throne, just a low platform and simple mats." | Pattern (correction) | It describes the room by use and lack, as VOICE_BIBLE asks. The "of course" that follows is Nagoji's own. |
| 175 | "The king was shocking some priests, yes, but he was not inventing a new world from nothing." | Pattern (antithesis) | Nagoji argues with his own Deccan eyes here. Once L173's thesis is cut, this becomes the paragraph's only verdict, and it is his. |
| 193 | "You are Eustachius De Lannoy ... You know guns. You know drill. You know how to build forts that do not burn when a lucky shot hits them." | Pattern (dialogue exposition) | A king naming a captive to his face is a display of power, not exposition, and the list ends in a barb about the magazine. |
| 197 | "“The Company is a ledger,” Varma said." | Pattern (implicit) | Terse and in Varma's register. It is the chapter's one "ledger", and REVIEW_BACKLOG C10-27 already cut the rest. |
| 209 | "not for pepper prices." | Scanner (comma-not) | Grounded in the trade, and the holistic reader protects it. Keep it as the chapter's one dialogue correction. |
| 255 | "Ram" | Pattern (modern nickname) | This is the king's established name for Ramayyan (Ch 6 L113, L159; Ch 10 L87; Ch 22 L349, L383). Only the job-offer idiom goes. |
| 289 | "running his thumb along the Company insignia." | Both (recycled gesture) | Keep it here, where the coat is the subject, and cut it from Donnadi at L55. |
| 291 | "My mother sewed the lining herself before I left Arras for the sea." | Holistic (convenient sentiment) | This was added on purpose to give De Lannoy a personal hook (REVIEW_BACKLOG C10-26), and it is what makes "Your mother is in Arras" land. |
| 319 | "“The rice,” he said, ..." | Pattern (sitcom quip) | The holistic reader protects the beat, which is a deflating joke that breaks the solemnity. Keep it and fix only the idiom (see Confirmed). |

## Opening

Current (L3 to 11):

> The end came with a lie, or perhaps just a misunderstanding of what honour meant on this coast.
>
> For two days after the explosion, De Lannoy went back and forth between our lines and the Dutch camp. He carried terms, counter-terms, and the slow grinding of pride against reality. On the twelfth of August, the capitulation was signed. On the thirteenth, the Dutch marched out.
>
> The smoke had cleared by then, but the smell lingered, ash and burnt powder mixed with the salt of the sea. They had signalled their readiness to treat. Terms had been agreed upon, or so they believed.
>
> They marched out of their ruined camp at mid-morning.
>
> It was a strange sight. ...

Verdict: **rewrite**. The first line is a hedged thesis that spoils the trap eighteen lines early. The next four paragraphs give the capitulation and the march-out three times (L5, L7, L9, L11), and "It was a strange sight" tells the reader how to react. The chapter comes alive at L13 with Nagoji in the saddle. The rewrite follows on from the Ch 14 ending that OPENINGS_ENDINGS_MOTIFS proposes ("Tomorrow, we will see what remains").

Proposed (about 105 words, replacing L3 to 11):

> For two days after the explosion, De Lannoy went back and forth between our lines and the Dutch camp, carrying terms one way and counter-terms back. On the twelfth of August the capitulation was signed. The garrison would give up what was left of the fort and march with its arms to the Dutch factory at Kanyakumari.
>
> They marched out on the thirteenth, at mid-morning. The beach still stank of the fire, ash and burnt powder under the salt. Beaten men, coats stained with soot and blood, but in ranks, with their drums beating. They carried their muskets. Their officers wore their swords.
>
> I sat on my horse near the dunes, watching them come.

If the author wants a voiced first line, make it blunt and owned, not hedged: "The terms were a lie, and my riders were part of it." That line admits Nagoji's part, since his riders wait behind the dunes at L25. It still gives the trap away, so the image opening is the stronger choice.

## Ending

Current last lines (L321 to 331):

> “So is everything else,” I said. “Welcome to Travancore, Kappittan.”
>
> He did not smile. But something in his face shifted, the first crack in the wall between what he had been and what he might become.
>
> That evening, I saw him walking the ramparts alone, the Dutch coat still folded on his bench, untouched. He had not thrown it away. Perhaps he never would.
>
> But he was not wearing it.
>
> History is strange. It turns on a lucky shot, a broken promise, and a conversation in a stone room.
>
> I looked at the walls of the fort. They were strong. But with Lannoy’s help, I knew they would become stronger. And Travancore, this slip of land between the mountains and the sea, would become something no one, not even the great Companies of Europe, could swallow.

Verdict: **revise**. The right ending is already here (a coat folded and left on a bench), but it arrives three times over. First comes the "first crack in the wall" abstraction. Then the image is wrapped in a hedge ("Perhaps he never would") and a one-line "But" kicker; STYLE_SHEET section 3 bars a closing paragraph that begins "But" or "Perhaps". Last come a recap tricolon and a destiny prophecy.

Proposed (replacing L321 to 331):

> “I still dream of bhakri,” I said. “Eat the rice, Kappittan.”
>
> He did not smile. He sat down on the bench beside the folded coat and pulled on the sandals.
>
> That evening I saw him on the ramparts in the white cloth, pacing the wall from one tower to the next and counting under his breath. The blue coat still lay folded on the stone bench where he had left it. Dew had beaded on its brass buttons.

This ends on an image. The pacing pays off the Udayagiri glance moved to L67, sets up Ch 16's walls, and gives De Lannoy the engineer's exactness that REVIEW_BACKLOG BL-04 asks for, without saying any of it. The minimal alternative is the motif audit's cut: "That evening I saw him walking the ramparts alone. The Dutch coat still lay folded on the bench outside his door. He had not thrown it away. He was not wearing it either."

## Flab (passages to tighten)

| Lines | Issue | Action |
|---|---|---|
| 3 to 11 | The surrender and march-out are stated three times, with a thesis line on top. | Replace with the Opening rewrite. |
| 37 to 61 | Nine paragraphs of stacked climaxes and POV breaks. | Keep: Ramayyan's two lines, the Keshavrao and dungeon callback, the drummer boy, "Then he looked at De Lannoy", the swear, the belt, the sword in the sand, "Down", the muskets like rain, the weeping, and the sergeant's forehead on the stock. Cut the rest as listed. About 330 words become about 190. |
| 65 to 67 | An impossible glance and a corrective restating the trap. | One tally paragraph (L65 first two sentences), then the gate image. |
| 71 to 111 | Forty lines with no consequence, ending in a mission speech and a moral. | Cut L101 to 105 and L111. Trim L73, L75, L93, L95 and L99 as listed. Keep L77 to 91 and L107 to 109. Pay it off at L275 ("Ibrahim's rice"). About 40% shorter. |
| 115 to 117 | A summary opener, and "before the prisoners were counted" is reused from L71. | Cut L115 and fix L117 as listed. |
| 131 to 135 | Three stock gallop details, a maxim, a broken scar metaphor, and "taste the idea of escape". | Two sentences for the gallop, two for the gap in the lines. |
| 151 to 161 | The halt is ordered three times: the king at L125, the runner at L153, and Nagoji's explanation at L155. | Keep the king's "But do not chase it into stone" and cut the runner (L151 to 153) and the explanation. New L155: "I stared south toward Kanyakumari, where their ships could still put cannon on any open beach, and remembered what the king had said about stone." Then L157 and the fixed L159. Cut L161. |
| 185 to 205 | The case against the Company is made four ways (treaty logic, honour, ledger and red ink, captured letters), with narrator glosses in between. | Keep L185, L189 (trimmed), L193 to 197 and L201 (fixed), then "Lannoy flinched." Cut L191, L199, L203 (or move it) and the L205 gloss. |
| 217 to 225 | The threat speech plus an explanation of the stakes. | The L217 fix, and cut L225. |
| 253 to 277 | Twenty-four lines of wrap-up after "I accept". | Keep L253 to 257, L259 (fixed), L261 to 269 (fixed), L271 to 273 (fixed) and L275 (fixed). Cut L277. If the author wants it leaner still, end the audience at L269 and go straight to the courtyard. |
| 289 to 301 | Undressing beats padded with pauses, adverbs and two similes. | Cut L295. Apply the L297 and L301 fixes. |
| 321 to 331 | The coat scene ends three times. | See Ending. |

## Passages to protect

- L13: "I sat on my horse near the dunes, watching them come."
- L15: "“They think they are going for a long walk and then a boat home.”" (Dhanaji at his best)
- L23: "A conch blew."
- L35: "“Terms change when kings have time to think,”" (the best line in the surrender)
- L45: the callback to Keshavrao in the storm and the Goan dungeon (as fixed)
- L53: "He swore, a short, sharp sound. Then he unbuckled his sword belt."
- L63 and L65: "“Take them,” Varma said." and the prisoner tally ("their muskets, their drums, and the few cannon that had not burst in the fire")
- L83 to 91: Ibrahim's salvage banter, "Things that have no flag now." and "It is healthier."
- L109: "For the usual consideration, of course."
- L125: the king's order, down to "If they can keep up" and "But do not chase it into stone."
- L139 to 143: the wet sand that "slow[s] the footman and favour[s] the rider who knew when to turn", smoke blowing into their own faces, and the sergeant under a horse's shoulder
- L149: "My horse wanted to follow. So did my blood."
- L157: the sword held across the chest, the signal to halt
- L171: "Ramayyan was there, of course, his stylus ready."
- L175: the Deccan-eyes paragraph (kalari pits, "closer to horse and musket than to plough")
- L179 to 181: "He did not bow." / "“You have a strange way of keeping treaties,”"
- L185: the king's treaty logic
- L201: "They will count the cost, shake their heads, and hire a new captain."
- L209 to 213: "not for pepper prices", "You want me to turn my coat." and "I want you to change your master,"
- L235: "when he could have let the Nair boys spear you on the beach."
- L245 to 247: "I will not fight against the Dutch" and "Or if I do, that they lose even faster."
- L283 to 287: the pile of local cloth, and "Men who lost brothers at Colachel will not take orders from a man who wears the uniform that killed them."
- L291: the mother's lining and Arras
- L299: "his shirt was sweat-stained, his chest pale where the sun had never reached."
- L303 to 305: "“Show me,”" and "He fumbled twice, cursed in Flemish, then got it right on the third attempt."

## Chapter-specific notes (continuity and history)

1. **The surrender happens twice (REVIEW_BACKLOG N-14).** Ch 14 L145 has "The survivors threw down their arms" and Ch 14 L183 "the prisoners being led away". Ch 15 L11 then has them march out armed. Fix this in Ch 14 (the backlog proposes "The survivors fell back into the ruins of their stockade"), not here.
2. **Who commands (SOURCE_OF_TRUTH 9.4).** Ch 13 L151 and Ch 14 L65 and L151 leave Lieutenant Rijtel in command. L27 here makes Donnadi "the senior surviving officer", and Rijtel never appears again. If Donnadi stays, one clause settles it: "Donnadi, the senior officer left alive since Rijtel fell in the charge".
3. **Numbers.** Ch 13 L151 gives the garrison as 250 Europeans, 50 lascars and two ensigns under a lieutenant. "Twenty-four European officers" plus "hundreds of soldiers" (L65) cannot come out of that. The figure usually cited is about 24 Europeans captured in all. Verify it, and reconcile it with Ch 16 L167 ("nearly a third asked to enter Travancore service").
4. **De Lannoy accepts twice (N-15).** He accepts here at L251, then again in Ch 16 at L165 and L175 to 177. The day-one Valiya Kappittan at L223 and L261 also conflicts with Ch 16 L179 ("You are an officer. We will see what kind") and with history, where the title came after years of service. The Borderline fix at L223 turns the title into a promise.
5. **De Lannoy's wound.** L179, "his wound bandaged", has no setup in Ch 14 or here. Either add a rag bound round his forearm at L27 or cut the clause.
6. **The Governor's letter (L203).** Its timing and provenance do not fit (see Confirmed). Verify the quotation's real source before it appears anywhere, and consider the Historical Note as its home.
7. **Mathoo Tharakan (N-27).** The historical Thachil Mathu Tharakan was born about 1741, so making him *Sarvadhi Karyakkar* at Colachel is anachronistic. The fix to L173 does not settle this. Rename him or disclose the liberty in the Author's Note, and add *Sarvadhi Karyakkar* to the glossary (FM-10).
8. **"Travancore Nair Brigade" (L277).** This is an 1818 name (RV-02). The recommended cut removes it.
9. **"Beachhead" (L201).** The word dates from the 1940s. It also appears at Ch 14 L11 and L23 and in the glossary's Colachel entry. Use "landing" or "foothold" throughout the book.
10. **Arras and Flemish (N-04).** Arras is in Artois and French-speaking, yet L305 has him curse "in Flemish", and Ch 16 L349 calls Arras "a city in Flanders". Decide this once for the whole book: curse "in French", or give the family Flemish roots on the page. "Since I was seventeen" (L291) fits a 1715 birth. Ch 16 L353 ("seventeen years") and L361 ("forty-three") do not, and should be fixed in Ch 16.
11. **The coat's logic (L291).** "The first thing I bought with my own wages" and "My mother sewed the lining ... before I left Arras" sit awkwardly with a Company coat that bears VOC insignia (L289), since he would have enlisted in the Republic. Cutting "It was the first thing I bought with my own wages" fixes it.
12. **The king's wound.** Ch 16 L154 has Varma at Tiruvattar with "the bandage on his shoulder still stiff from Colachel", but neither Ch 14 nor this chapter shows it. A clause at L273 would plant it: "reaching for his spear with his good arm".
13. **Motif budget.** Keep "teeth" once, at L125, cutting L159 and varying the L17 animal. "Rot" appears in three chapters running (Ch 14 L155, Ch 15 L217, Ch 16 L167). Keep this chapter's, which is a deliberate callback, and vary Ch 16's. Other repeats: "luxury" (L115, L141), "stained" coats (L11, L27, L179, L283), "rigid" (L47, L61). The coat scene is one half of a mirrored pair with Ch 24 (OPENINGS_ENDINGS_MOTIFS), so do not let Ch 16 L273 to 287 spend it again.
14. **Phrases repeated from other chapters (REPETITION_AND_DENSITY):** "the slow grinding of" (Ch 10 L191); "a man who had already" (Ch 14 L163, about De Lannoy a page earlier); "carrying the weight of a" (also Ch 20 L222); "very still for a long moment" (Ch 18 L125); "He nodded slowly" (Ch 7 L115); "I drove my horse straight at" (Ch 23 L223, keep one). Ibrahim's mask and sea lines repeat Ch 11 L405 and L407 and Ch 13 L205.
15. **Consistency for the 2e copy.** "De Lannoy" runs to L65 and "Lannoy" from L169 onward; pick one rule. Straight quotes appear at L31 to 59 and L121 to 159, curly elsewhere. Change "realizes" (L45) to "realises". "Company" and "company" appear 4 times each, and "King" 4 times against "king" 7. Italics: *mundu* is italic but "Valiya Kappittan" is roman (C18-04).
16. **Comic tie-in.** The unpublished graphic-novel snapshot letters "HIS EYES WERE ON UDAYAGIRI" from L65 (SOURCE_OF_TRUTH section 11). The L67 fix keeps the image but moves it to the gate. The author can decide whether the comic follows.
17. **Scanner gap.** `scan_slop.py` counts 6 "not ... but" hits, but a hand count finds 13 correction constructions (L57, 65, 67, 73, 93, 117, 139, 143, 173, 175, 217, 275, 315), because it misses the two-sentence "not X. They were Y" form and "no longer just". Hand-check this chapter again after editing.
