# Second-Edition Audit: Chapter 9, Princess of Velinadu

- Source (frozen first edition): `book1_horse_servant/book2_chapter09_princess_of_velinadu.md`, 254 lines, 3,062 words by `wc` (3,056 by the scanner).
- Line numbers are physical lines in that file, blank lines included. `manuscript/` does not yet hold a copy of this chapter. A fresh copy will match these numbers until its first edit, so apply the fixes from the bottom up.
- Method: I read the chapter in full and ruled on every flag from the pattern auditor (83 flags) and the holistic reader (27 passages, 13 flab notes), merging duplicates. I checked the end of Ch 8, the openings of Chs 10 and 11, the Revathi and brand passages in Chs 1, 4, 16, 17 and 20, the Author's Historical Note, and the book-level audits (`REGISTER_AND_ANACHRONISM.md`, `OPENINGS_ENDINGS_MOTIFS.md`, `VOICE_BIBLE.md`, `REVIEW_BACKLOG.md`). To test the cut estimate, I applied every confirmed fix and every borderline "take" to a scratch copy outside the repo and ran `audit/tools/scan_slop.py` on it against the original.
- Source tags: **P** = pattern auditor, **H** = holistic reader, **R** = an earlier book-level audit already flagged it, **N** = new in this pass.

## Verdict

| Measure | Call |
|:-|:-|
| Severity | **4 of 5** |
| Recommended intensity | **Medium** (tics plus tightening). Rewrite four places: the road opening (4 to 12), the wait and entrance (56 to 66), the Savitri beat (144 to 152) and the back fifth (206 to 254). |
| Estimated word cut | **About 20%** for the confirmed fixes. The scratch pass with the confirmed fixes plus the borderline takes went from 3,062 to 2,388 words (22%). About 40% of the cut comes from lines 206 to 254. |
| Scanner, before and after the scratch pass | Style-sheet excess 17 to 2. Not-but family 6 to 3 (the 3 are on two dialogue lines, 138 and 184). "as if" 5 to 1. Slowly/quietly/softly/carefully 9 to 2. "the weight of" 2 to 0. "For now" closers 2 to 0. One-sentence paragraphs 35 to 21. No marker went up. |
| Rulings | 59 confirmed, 17 borderline, 21 defended |

The chapter has a sound skeleton and some of the best dialogue in Part II: the gate exchange (28 to 38), "What letters do you carry on your skin" (106 to 110), "Horses also." (118), the burned pepper fields question (160), the companies buying coasts (170), "Padmini warms your feet at her hearth so your loyalty tastes local" (176), "Not from mine." (184), and the night exchange "Sea or fort?" / "Dungeon" (240 to 242). Almost none of that needs re-voicing.

The slop is in the connective tissue and at the back:

1. **Nearly every narration beat between speeches is stock.** A reaction tag, a correction or a sentence explaining a tone follows almost every good line of dialogue. Examples: "It was not a question." (92), "Her mouth twitched, not quite a smile." (82), "There was no shrillness in her tone. Only..." (102), "She smiled then, but it was a smile with an edge." (158), "Her bluntness stung because it was true." (168), "The words were light. The tone was not." (186). Most fixes are plain deletions.
2. **The back fifth ends three times.** First Padmini's verdict, spoiled by the meta line "Her place in this story" (206). Then a reflective run that is the most machine-sounding block in the book so far (208 to 218): mirrored Goa/Velinadu sentences, "precarious", "a strange comfort", "If storms had taught me anything", "had made her position clear". Then a night coda with good material inside a lesson quiz ("what did you learn about yourself?"), closed by an announced open question and "For now... words sharper than blades" (252 to 254).
3. **Continuity seams that read as patched text:** the plantain is picked up twice (112, 128), Revathi's speech is split across two tagged paragraphs (114, 116), Padmini comes back to a verandah she never left (200), and a new "long white scar" appears (238).

Why medium and not deep: the dialogue carries the chapter and should mostly be left alone. About half the confirmed fixes are straight cuts, and most of the rest are shorter than the lines they replace.

## Confirmed issues

| Line | Quote | Category | Suggested fix | Src |
|:-|:-|:-|:-|:-|
| 4 | "and the air still clung to the night's cool" | stock_phrase | "We left Padmini Amma's estate before sunrise, when the sky was the colour of old iron and the grass on the bunds was still wet enough to darken the horses' fetlocks." Or just cut the clause. | P |
| 6 | "low hills quilted with rubbery green" | anachronism | "We rode through low hills of jack and areca". Para rubber was not planted in Kerala until the 1870s, and the estates date from 1902. | P H R |
| 6 | "oil lamps clung to the trunks of ancient trees ... revealed more of the land's body" | abstract_depth | "...and on past lotus ponds and small shrines, where cloth was tied to old trees and oil lamps burned at their roots. As the light grew, the mist lifted off the paddy." This also removes the second "clung". | P H |
| 10 | "moved with the confidence of one who knew every stone on the path" | stock_phrase | "sitting sideways on a short-legged country horse that picked its own way over the stones" | P H |
| 24 | "was not the city my Deccan mind had expected. There were no towering walls, no massive bastions. Instead," | correction | "Velinadu Kovilakam sat inside a ring of red laterite and packed earth, with tiled roofs and trees behind it." Leave the Deccan fort comparison to Ch 10, which opens on it (ch10:3). | P H N |
| 24 | "seemed more focused on who entered than what" | modern_register | "The gates were wide enough for carts and elephants, and the guards cared more about who came through them than what." | P R |
| 26 | "They watched Padmini Amma approach with a mixture of respect and calculation." | stock_phrase | Cut. The bow at 28 shows the respect and "And this?" at 34 shows the calculation. | P H |
| 40 | "Banners hung from poles, heavy with the morning's stillness." | stock_phrase | "Banners hung limp from their poles." Or cut. | P H |
| 42 | "their weapons, their writing tablets, their anxious glances toward doorways where no one had yet appeared" | anachronism | "There were fewer men, most of them carrying a sword or a bundle of palm leaves and an iron stylus, and all of them watching a doorway no one had yet come out of." A Kerala scribe wrote on ola with an iron stylus, and the chapter itself has palm leaves at 114. | P H |
| 44 | "Padmini Amma said quietly ... waiting for a husband to give her meaning" | modern_register | "“Remember,” Padmini Amma said as we dismounted ... Do not speak to her as you would to a sardar's daughter waiting to be married off.”" This also removes one "as if" and one soft adverb. | P H |
| 52 | "somewhere deeper within the complex" | anachronism | "Drums and bells sounded from somewhere behind the main hall." | P R |
| 56 | "letting it wash away the dust of the road ... learn the patterns of this land. Rice instead of bhakri. Coconut instead of groundnut. Fish where once there had been mutton." | fragment_list | "I drank the cool water. My stomach had fought this coast's food for months and was only now giving in: rice where there had been bhakri, coconut oil where there had been sesame, fish in place of mutton." Groundnut was not a Deccan staple in the 1730s. | P H R |
| 58 | "Waiting is familiar to any soldier ... as the minutes stretched ... This was not the tense quiet before a battle ... It was the waiting men endure when summoned before someone who can change their fate with a word." | correction | "I had waited like this once before, outside a sardar's tent, to learn whether I would ride with the huzurat or go home. I caught myself picking at the linen on my fingers and made my hands lie still." At ch1:7 sardars pick the huzurat, and at ch8:75 his fingers are still wrapped in linen. | P H R |
| 60 | "Not the heavy tread of armoured guards, but the light, quick rhythm of someone accustomed to moving through these spaces without being questioned." | correction | "Bare feet came quickly over the stone, and nobody stopped them." Nair guards wore no armour, so the negation brings in the wrong picture. | P H |
| 64 | "though the way she held herself made guessing her exact years difficult ... skin the colour of polished teak" | stock_phrase | "She was a little younger than I." ... "At her throat lay a necklace of flat gold coins." Keep the coins, which are her signature (224, ch20:63). | P H |
| 66 | "When they met mine there was no flutter, no demure dip of lashes." | correction | Cut. "Her eyes were dark and level" already says it. If a beat is wanted: "She held my eyes until I was the one who looked away." | P H |
| 82 | "Her mouth twitched, not quite a smile." | stock_phrase | Cut. Keep the guard's twitch at 32 as the chapter's only one. | P R |
| 90 | "She sat with liquid ease ... A servant appeared as if summoned by thought" | stock_phrase | "She sat and folded her legs under her. A servant set a brass plate of food beside her without being called, and she let it lie, her eyes still on me." | P H |
| 92 | "It was not a question." | stock_phrase | Cut. | P H R |
| 96 | "tasting the words as if they were unfamiliar" | stock_phrase | "“My king,” she repeated." Keep the rest of the speech. | P H |
| 100 | "the Maharaja's reforms" | modern_register | "Now everyone speaks of the Maharaja as if the world began when he took the throne." This becomes the chapter's one "as if". | P H |
| 102 | "There was no shrillness in her tone. Only a steady, simmering annoyance that reminded me of the way..." | correction | "She spoke of him the way old captains speak of young sardars who think themselves clever." | P H |
| 104 | "She leaned back slightly, studying me." | filler_beat | Cut. | P |
| 116 | "“You think you can teach our men ... on your hills?” she asked." (Revathi again, in a new tagged paragraph) | continuity | Merge into 114: "...Ramayyan filled a grove of palm leaves about it. Do you think you can teach our men to kill Dutch as easily as you killed Portuguese on your hills?”" | P H R |
| 122 | "their flag will cast a shadow over every fort ... they tried to erase my name and replace it with a number in their books. I have seen their hunger." | stock_phrase | "“Because if we do not, the Europeans will fly their flags over every fort from Nashik to this coast,” I said. “Because in Goa they took my name and scratched a number in its place. Give them an inch of riverbank..." (the rest as is). "Scratched" echoes ch1:7. | P H |
| 124 | "Her eyes narrowed slightly." | filler_beat | Cut. | P H |
| 128 | "She picked up a piece of plantain from her plate and ate it slowly, chewing as if the act helped her think." | continuity | "Now she ate the plantain." She already picked it up at 112. | P H R |
| 130 | "gesturing vaguely toward the hall behind her, the trees, the earth under us" | filler_beat | "“You know what this place is?” she asked." She points at the earth at 136, so this gesture doubles it. | P |
| 138 | "Not to my husband, if I take one ... To my sisters. To their daughters. To the name we carry ... the very wind. They were wrong." | fragment_list | "“This land belongs to my line,” she said. “Not to any husband I take, not to any son I bear. It goes to my sisters and their daughters, under the name we carry. The company men did not understand that. They thought that if they pleased the right man and signed the right paper, the pepper was theirs. Now they send different men with different papers.”" This also fixes the clash with her widowhood (see notes). | P H R |
| 140 | "where I knew, beyond the curve of the land, Dutch ships rode at anchor somewhere beyond sight" | filler_beat | "She looked south, toward the anchorage where the Dutch ships lay." | P H |
| 142 | "He builds a state that answers to the crown, not to the old lines." | dialogue_exposition | "He wants every house to answer to Padmanabhapuram and none to its own mothers." Keep the rest of the speech. | P H R |
| 144 | "She paused, and something shifted in her face. A shadow, there and gone." | abstract_depth | "She wiped her fingers on the cloth beside her plate." A plain beat is needed; without one, 142 and 146 read as one speech spliced in two. | P H |
| 146 | "her tone carefully flat" | explained_subtext | Cut the tag: "“My mother's cousin sits in Kottarakkara,” she said." | P H |
| 148 | "She did not elaborate. The silence stretched a heartbeat longer than it should have." | signposting | "I made her say the name of the house twice before I had it." Then 150 as is, with "Revathi said" in place of "Revathi added". | P H |
| 152 | "I did not know the name. I did not know the house. The weight of what she was not saying settled into the air between us like monsoon humidity." | explained_subtext | Cut. The dog and wounded bird at 150 do the foreshadowing, and 148 now shows that the name was new to him. | P H R |
| 158 | "She smiled then, but it was a smile with an edge." | stock_phrase | Cut, and run 160 on from 156 with no new tag: "...Harder for them to say no. Will you say no, Nagoji Sawant, when he points you at a house that will not bow as deeply as he likes? If he tells you my pepper fields shelter Dutch spies, will you burn them for him?”" | P H |
| 162 | "The question was hypothetical, but it landed like a thrown dagger." | stock_phrase | Cut the sentence and trim the rest: "I thought of Padmini's estate, of the boys in the kalari pit and the women sorting pepper under her eye. I thought of my father's fields near Nashik burning on the orders of a king who called himself our protector." | P H R |
| 164 | "I said slowly ... That choice is not made lightly." | stock_phrase | "“I ride for the orders I am given,” I said. “But I choose which king gives them.”" | P H |
| 166 | "Do not pretend you stand at a crossroads when your feet are already on the path." | stock_phrase | "“You have already chosen,” she said. ... Do not tell me you are still choosing.”" Also change "when the sea spat you out" to "when the sea gave you back", because Padmini owns "spits" (ch8:77). | P H R |
| 168 | "Her bluntness stung because it was true." | explained_subtext | Cut. His retort at 170 shows the sting. | P H |
| 176 | "They groom you" | modern_register | "“They are breaking you to the saddle,” she said. “I can see it.”" This is a metaphor from his own trade, turned on him. | P H |
| 180 | "Land. Honour. A place in their tales. Perhaps even a wife from some house that can make you feel rooted here." | fragment_list | "“They will offer you land and honours,” she said. “Perhaps even a wife from some house that will tie you to this coast.”" | P H |
| 186 | "The words were light. The tone was not." | kicker | Cut. | P H |
| 188 | "Men like you rarely have to ask ... The world falls over itself to give them offers. I state my position early." | modern_register | Cut the paragraph. "Not from mine." stands on its own. | P H R |
| 192 | "listen to old women argue about dowries" | anachronism | "listen to old women argue over boundary stones and young men boast about boats". A marumakkathayam house pays no dowry, and this chapter is about exactly that law. | P H |
| 198 | "Then she was gone, swallowed by the shade of the inner hall, jasmine leaving a faint trail in the air." | stock_phrase | "Then she went in. A jasmine flower from her hair lay on the mat where she had sat." | P H |
| 200 | "Padmini Amma stepped back onto the verandah from the direction of the inner rooms and let out a slow breath." | continuity | Plant her exit after 70: "Padmini Amma went in to greet the elders." (see 72 in the notes). Then 200: "Padmini Amma came back along the verandah, her stick tapping on the stone." | P H |
| 206 | "Her place in this story is not to approve. It is to remind men like you and the Maharaja that the land remembers longer than crowns do." | explained_subtext | End the speech at "“She does not have to,” Padmini said." "Land remembers" belongs to Revathi at ch18:193. | P H R |
| 208 | "a steady heartbeat rhythm. As we rose to follow, the ground under my bare feet took on new weight." | abstract_depth | "Inside, the drums started again. Padmini went in toward them, and I followed." | P H |
| 210 to 218 | "In Goa, I had fought men who believed God and gunpowder gave them the right to rule ... my own place felt precarious. / Yet there was a strange comfort in that. / If storms had taught me anything ... / Revathi Bayi had made her position clear." | summary_ending | Cut all five paragraphs. They are a mirrored antithesis, a mood kicker, a stock reversal, the storm motif (reserved for ch13:321) and a summary in office language. He was also taken in the Konkan, not in a fight at Goa. | P H R |
| 220 | "Padmini was talking quietly with house elders" | soft_adverb | "That night, when the hall had emptied and Padmini sat with the house elders, a servant found me by the outer steps." | P |
| 226 | "“You heard many words today,” she said without preamble. “Tell me one thing you learned.”" | explained_subtext | "“Well,” she said. “What will you tell your king about us?”" This picks up her own instruction at 192 and gives her something she wants from him. | P H |
| 230 | "The corner of her mouth twitched." / "“Not bad,” she said." | stock_phrase | "“Tell him exactly that.”" | P H R |
| 232 to 236 | "“And what did you learn about yourself?” ... “That I am still a man the sea has not decided to keep,” ... “land that can throw me off if I forget whose it is.”" | modern_register | Cut 232 to 236. The question is therapy language, and the answer restates 74 and 196. | P H |
| 238 | "the long white scar on my forearm, a souvenir of Goa" | continuity | "Her gaze went to the linen still wound round my fingers." At 240: "“That?” she asked. “Sea or fort?”" She has already seen the brand (108), the scar is new to the book, and the nails taken in Goa (ch1:13) are still bandaged at ch8:75. | P H R |
| 244 | "Her hand lifted, almost of its own accord" | stock_phrase | "She put out her hand and stopped it a finger's breadth from the linen." | P H |
| 246 | "“Travancore has its own tools,” she said softly. “Do not give us reason to use them.”" | continuity | "“Your king keeps men with tools too,” she said. “Do not let him make you one of them.”" Revathi has spent the scene setting her house against the crown, so she cannot speak for Travancore as "us". The new line turns his "time and tools" into her real warning from 160. | P H |
| 252 | "The question of where I would stand when the king's wishes scraped against the houses of this coast remained unanswered." | summary_ending | Cut. | P H R |
| 254 | "For now, I followed Padmini into the hall, where incense curled, drums spoke, and old Velinadu women weighed the future in words sharper than blades." | summary_ending | Cut, and end on 250. This paragraph also breaks the timeline: the hall emptied at 220, and he already followed Padmini in at 208. | P H R |

## Borderline

These are real tics, but each line also does some work. Take the fix if the paragraph still reads flat after the confirmed cuts; otherwise leave it.

| Line | Quote | Why borderline | Option |
|:-|:-|:-|:-|
| 6 | "lotus leaves floated like idle coins" | Coins belong to his world (pay, the companies' coins at 170, Revathi's necklace), so the image is not foreign. "Idle" is the decorative word. | The line 6 rewrite drops it. If the author wants it, keep "floated like coins". |
| 8 | "Women with baskets ... talking and laughing ... Men led bullocks ... Children chased each other" | A postcard triad, but the bunds that "would have sent me tumbling" are his honest clumsiness. | "Women with baskets on their hips were already on their way to the pepper gardens, and men were leading bullocks out to plough. Children ran along the bunds on ridges that would have tipped me into the channel in three steps." |
| 10 | "the colours drawn from the earth rather than court paintings" | A mild correction; court paintings are not his frame of reference. | "but in the colours of turmeric and red earth" |
| 12 | "close enough to hear her speak ..., far enough that ..." / "their eyes scanning the road" | The etiquette point is real; the mirrored frame is the tell. | "I rode half a length behind her on the left, the place a huzurat keeps behind his sardar. Ibrahim and two of Padmini's male relatives came after." |
| 40 | "some in plain cotton, some in brighter silk, all with their heads uncovered" | The uncovered heads are the point: a Maratha would notice them. The some/some/all frame is reflexive. | "Women moved along the verandahs with their heads uncovered, their hair oiled and coiled or braided as they pleased." |
| 44 | "land, not men, is the first thing named ... the weight of many fields behind her" | A dialogue X-not-Y and a weight tic, but it is Padmini's briefing. Spend the chapter's one allowed X-not-Y at 138. | "you stand in a place where the land is named before the men. The woman who carries that name speaks for every field that goes with it." |
| 48 to 50 | "She smiled, a flash of white teeth." / "“That can be arranged.”" | P would keep it and H calls it a stock film comeback. The kick exchange is Padmini's threat register and should stay; the reply is the stock part, and the teeth smile repeats ch8:173. | Cut 48 and make 50: "“I will not need to,” she said. “Revathi kicks harder.”" |
| 64, 190 | "Her sari ... leaving one shoulder bare" / "smoothing her sari" | Period dress, not slop (see notes). | "Her mundu and upper cloth were deep indigo edged with gold." Check this with a costume source. |
| 80 | "I said carefully" | "Carefully" describes a learner choosing his words, but the spoken "Slowly." doubles it. | Cut the adverb. |
| 84 | "normally insist theirs is the only one that matters. Those men bore me." | It gives her an edge early, but "normally" and the sass read modern. Earlier review C10-17 also flagged it. | "Good. A man who will not learn our tongue thinks God speaks only his. I do not waste my mornings on such men." |
| 114 | "They also love patterns" | "Patterns" leans modern, and the line is the hinge from scars to the sand drill. | "They love a new trick too" |
| 172 | "to stand on the other side of some doors when they close" | A good threat, but figurative doors are rationed to the cellar door (OPENINGS_ENDINGS_MOTIFS). Gates are literal in this chapter (16, 24). | "Understand that you also chose which side of some gates you will stand on when they shut." |
| 174 | "She looked away briefly" | A filler adverb. | "She looked toward the inner hall." |
| 176 | "Men like you look good in stories when the scribes write of brave charges." | The fifth "men like you" in the chapter; otherwise it is a dry, good line. | "You will look well in the scribes' stories of brave charges." |
| 182 | "She shrugged slightly." | The third "slightly". | "She shrugged." |
| 192 | "Tell him also that we are still watching." | Stock menace, though it is a real message. "Tell him Velinadu smiled at you" already carries the threat. | Cut. |
| 194 to 196 | "She turned to go, then paused and looked over her shoulder ... Every hoofprint has a name beneath it. Learn those names." | A TV "one more thing" exit and a three-step epigram, but the hoofprint is the only version of her theme built from his trade. Keep it as her one epigram of the exit. | "At the door of the inner hall she turned. / “And Nagoji. When you run your horses on that wet sand, remember that every hoofprint falls on somebody's name. Learn the names.”" |

## Defended (flagged, keep)

| Line | Quote | Flagged by | Why it stays |
|:-|:-|:-|:-|
| 18 to 22 | "Stories travel badly ... She carries those bones in her tongue." | H (mixed metaphor) | It is not mixed. It turns the proverb "the tongue has no bones" (common across Indian languages, Malayalam included) inside out: Revathi's words have bones. Padmini is extending her own image from 18. |
| 32 | "The guard's mouth twitched." | P (tic count) | The tic is the problem, not this instance. The guard's twitch answers Padmini's joke and makes the gate human. Keep this one and cut 82 and 230. |
| 54 | "That is part of the weighing." | P (weight motif) | This is the chapter's one earned "weigh". It frames the whole visit. Cut the others (44, 152, 208, 254). |
| 74 | "The one the Portuguese could not quite break and the sea could not quite keep." | P, H | Mirrored, but it is dialogue and it is how she introduces him. The problem is Nagoji's echo at 236, which is cut. |
| 100 | "We bled when those pacts were broken. We killed when they thought our hands too soft to hold swords." | H | This is history, not decoration: the 1721 killing of the English Company men at Attingal, which Velinadu borrows (16, 132). |
| 100 | "long before your Maratha court ever saw a European" | P, H (history) | It stands as a jab: Kerala's houses dealt with the Portuguese from 1500, and the Chhatrapati's court dates from the 1670s. Tighten to "long before there was a Maratha court to see one," which is accurate and more insulting. |
| 118 | "The ground does not care whose blood it drinks." | P | It sets up "Yet you keep pouring" at 120. Cutting it breaks her comeback. |
| 122 | "a number in their books" | P (called it a 19th or 20th-century prison image) | This is the book's spine motif, planted at ch1:7 ("a number the clerk scratched beside the words *prisioneiro marata*"). Only "erase ... replace" and "I have seen their hunger" go. |
| 122 | "Give them an inch of riverbank, and they will swallow the whole valley before you have finished signing their treaty." | P, H | The proverb is sixteenth-century in shape, and he puts it in his own terrain. The tail about the treaty sets up "treaties are nets" at 228. |
| 134 | "They did not forget to listen ... They never thought they had to. That is worse." | P | One character correcting another is argument, not the narrator's reflex, and it moves the scene forward. |
| 138 | "This land belongs to my line ..." (core) | P, H (flab) | Keep it, trimmed, as the chapter's one full statement of the law of the mothers. Cut the restatements at 44 (softened), 196 (trimmed) and 206. |
| 142 | "That is good for facing Europeans. It is less good for those of us whose names are older than his." | H | Dry understatement in her voice. "Before his uncles did" in the same speech is a precise matrilineal touch, since Marthanda Varma succeeded his uncle. |
| 156 | "Fear is for people who have no knives ... Easier to shift such men when the time comes. Harder for them to say no." | P | This is the political core of the scene, and the "say no" now carries straight into her question at 160. |
| 162 | "I thought of Padmini's estate, of the boys in the kalari pit, of women sorting pepper" | P | Every item is concrete and comes from Ch 8. The Nashik fields foreshadow Ch 26. Only the dagger sentence goes. |
| 166 | "You could have run north ... You drilled horses on sand. You accepted the Maharaja's gaze on your neck." | P (exposition) | Her recital is her argument that he has already chosen, and "the Maharaja's gaze on your neck" is hers alone. Only the crossroads line goes. |
| 176 | "Ramayyan marks your uses. The Maharaja tests your judgment. Padmini warms your feet at her hearth so your loyalty tastes local." | P (tricolon) | Each clause names a real person and that person's method. No template produces "tastes local". |
| 184 | "“Not from mine.”" | H (romance move) | This is dramatic irony: he marries into Velinadu in Ch 20. Cutting 186 and 188 lets it land. |
| 192 | "young men boast about boats" | P (jingle) | Lively and local. Only "dowries" is wrong. |
| 222 | "The Velinadu lady asks if your feet remember her verandah" | H (the "remember" count) | An indirect, courtly summons, and a callback to a verandah that pays off at ch20:63. |
| 228 | "That treaties are nets ... Velinadu does not let anyone else hold the rope." | H (grouped with the quiz) | Not a restatement. It is a new image from the fishing coast that saved him (Ch 4), and it answers her reframed question at 226. |
| 250 | "Padmini will think I am trying to steal her new toy." | R (C10-17 asked to replace "toy") | "Toy" in the sense of plaything is sixteenth-century English, and the line pays off "The Maharaja plays with him" (36). It is the natural last line. |

## Opening

Current first lines (4 to 8): "We left Padmini Amma's estate before sunrise, when the sky was the colour of old iron and the air still clung to the night's cool." This is followed by a "through ... past ... past" road list, lotus leaves "like idle coins", "the land's body", and a women/men/children village.

**Verdict: revise (light).** "The colour of old iron" is his: iron is the cellar and the chains of Ch 1. The rest of the approach could open any chapter of any novel. Ch 9 is also one of four chapters that open on sky or weather (9, 13, 19, 25, per OPENINGS_ENDINGS_MOTIFS).

Option A, the minimum, keeps the road and makes it a rider's road (confirmed and borderline fixes at 4 to 12):

> We left Padmini Amma's estate before sunrise, when the sky was the colour of old iron and the grass on the bunds was still wet enough to darken the horses' fetlocks.
>
> The road to Velinadu wound inland at first, away from the sea. We rode through low hills of jack and areca and on past lotus ponds and small shrines, where cloth was tied to old trees and oil lamps burned at their roots. As the light grew, the mist lifted off the paddy.
>
> Women with baskets on their hips were already on their way to the pepper gardens, and men were leading bullocks out to plough. Children ran along the bunds on ridges that would have tipped me into the channel in three steps.

Option B, if the author wants to cut down the book's weather openings, starts on Padmini's question. It follows straight on from Ch 8's last line ("Two days to learn how not to offend a princess."):

> “You have heard of Velinadu,” Padmini Amma said. “What did your hills tell you?”
>
> We had left her estate before sunrise, when the sky was the colour of old iron, and the road had carried us inland through low hills of jack and areca, past lotus ponds and shrines where cloth was tied to old trees.

Then 16 ("Stories," I said...), with the description of Padmini on horseback (10) moved to after 22. Either way, the first living exchange ("Stories travel badly", 18) arrives within a hundred words.

## Ending

Current last lines (250 to 254):

> “Go,” she added. “Padmini will think I am trying to steal her new toy.”
>
> The question of where I would stand when the king's wishes scraped against the houses of this coast remained unanswered.
>
> For now, I followed Padmini into the hall, where incense curled, drums spoke, and old Velinadu women weighed the future in words sharper than blades.

**Verdict: revise.** Cut 252 and 254 and end on 250, which is already in the text. The final paragraph fails four ways. It is a "For now" closer, which the style sheet bans. It ends on a tricolon capped by "sharper than blades", which ch14:185 repeats. It weighs the future (the fifth "weigh"). And it breaks the timeline: the hall emptied at 220, and he already went in at 208. The line before it announces the chapter's open question outright.

The voice bible's alternative ("I followed Padmini into the hall.") would still carry the timeline error, so end on Revathi. The night coda then keeps its best material and loses the quiz. Proposed 220 to 250:

> That night, when the hall had emptied and Padmini sat with the house elders, a servant found me by the outer steps.
>
> “The Velinadu lady asks if your feet remember her verandah,” he said.
>
> She was waiting where I had first seen her, coins at her throat dimmer in the lamplight, the night air cooler on the stone.
>
> “Well,” she said. “What will you tell your king about us?”
>
> “That treaties are nets,” I said. “And that Velinadu does not let anyone else hold the rope.”
>
> “Tell him exactly that.”
>
> Her gaze went to the linen still wound round my fingers.
>
> “That?” she asked. “Sea or fort?”
>
> “Dungeon,” I said. “A Portuguese man with time and tools.”
>
> She put out her hand and stopped it a finger's breadth from the linen.
>
> “Your king keeps men with tools too,” she said. “Do not let him make you one of them.”
>
> She let her hand drop.
>
> “Go,” she added. “Padmini will think I am trying to steal her new toy.”

The chapter now closes on a touch that stops short, a warning that fits her politics, and a joke that puts him back in his place. That hands the unanswered question to the reader without naming it. An optional variant for the last word is "steal her new horse", which rhymes with "breaking you to the saddle" (176). "Toy" pays off line 36 more directly, so I would keep "toy".

The verandah scene's own close (198 to 208) also needs trimming so that it does not compete with this ending. End Padmini's speech at "She does not have to" (206), keep the drums as a plain action (208), and cut 210 to 218 entirely.

## Flab (passages to tighten)

| Lines | Issue | Tighten to |
|:-|:-|:-|
| 4 to 12 | A scenic road approach with a postcard village; Padmini's horse and the escort position are described in stock terms. | Option A above. The aim here is voice, not length: 4 to 8 stay about the same (131 words to 125), and 10 to 12 lose about 20. |
| 24 to 26 | A place defined by what it lacks, then the guards' attitude named. | One sentence of laterite and roofs, one of the gates. Cut 26. |
| 40 to 44 | A generic arrival panorama, then a briefing that restates 16 to 22. | Keep the uncovered heads, palm leaves and stylus, and a shorter briefing without "give her meaning". |
| 56 to 66 | A diet list, a meditation on waiting, a corrected footstep and a head-to-toe portrait of Revathi: 246 words before she speaks. | About 170 words: the meal in one sentence, the sardar's tent and his hands, bare feet, then coins, jasmine and level eyes. |
| 112 to 130 | The plantain is picked up twice, one speech is split in two (114/116), and there are two filler beats (124, 130). | One plantain, one merged speech, no gestures. |
| 138 to 142 | Revathi lectures on matriliny, then on state-building. | Keep both speeches, trimmed as in the table. The look south (140) is the breather between them. |
| 144 to 152 | Four foreshadowing signals in nine lines. | One plain beat (144), one line of him struggling with the name (148), and the dog simile (150). |
| 158 to 168 | After the burn question: an explained impact, a filler answer, a crossroads rebuttal, then "stung because it was true". | The question, his thoughts, one short answer and her rebuttal. |
| 176 to 188 | Offers, fragments, "The words were light", and office language. | "Breaking you to the saddle" ... "Not from mine." Cut 186 and 188. |
| 194 to 208 | A TV exit, a stock vanishing, Padmini re-entering, a meta line and new weight underfoot. | Five short paragraphs: the turn, the hoofprint, the jasmine on the mat, Padmini's verdict, the drums. |
| 208 to 218 | A reflective coda after the scene has ended, including the false ending "made her position clear". | Cut. |
| 226 to 236 | A lesson quiz that recites 74 and 196 back. | The one question she would really ask (226) and his net and rope answer. |
| 252 to 254 | An announced question and a "For now" closer that contradicts the timeline. | Cut. |
| Throughout | One-line action paragraphs (35 in the source) that stand apart from the speech they belong to. | Where the beat belongs to a speech, fold it in: 20 into 22, 136 into 138, 178 into 180, 182 into 184. |

## Passages to protect

- 16 to 22: "Stories travel badly ... the bones of that one are not wrong." / "She pointed ahead with her chin." / "She carries those bones in her tongue."
- 28 to 38: the gate exchange, word for word, including "When tongues are still loose from sleep, they forget to lie as well." and "The Maharaja plays with him. I thought Velinadu should have its share."
- 54: "Ceremony ... They will make you wait. That is part of the weighing."
- 70: "I brought him before the salt left his skin."
- 74: "each syllable placed slowly enough that even a northerner could not pretend to misunderstand."
- 80: "Like a horse finding its footing on new ground."
- 88: "If you crane your neck the whole time, you will despise me before we have even argued."
- 94 to 96: "I ride where I am told ... At present, that is for your king." / "He takes heads when he must and lands when he can."
- 106 to 110: "What letters do you carry on your skin, Sawant?" / "Joints that ache in the rain. Nothing a scribe would waste ink on." / "They love scars."
- 114: "Made them move like the fish I watch at low tide. Ramayyan filled a grove of palm leaves about it."
- 118 to 120: "We lost men every time. Horses also." / "Yet you keep pouring."
- 134: "They never thought they had to. That is worse."
- 150: "Your king circles that house the way a dog circles a wounded bird."
- 156 to 160: "Fear is for people who have no knives" through "will you burn them for him?"
- 170: "the companies buy whole coasts with a handful of coins and a barrel of powder."
- 176: "Padmini warms your feet at her hearth so your loyalty tastes local. They will make you a general of horse if you do not die first."
- 184: "Not from mine."
- 192: "tell him Velinadu smiled at you."
- 202 to 204: "You did not disgrace yourself." / "I am not sure she agrees."
- 222 to 224: the summons and "coins at her throat dimmer in the lamplight".
- 240 to 242: "Sea or fort?" / "Dungeon ... A Portuguese man with time and tools."
- 250: "Padmini will think I am trying to steal her new toy."

## Chapter-specific notes (continuity and history)

1. **Revathi's widowhood.** At ch16:77 she "lost a husband ... five years before you washed up on this coast", so she is a widow here. At 138, "Not to my husband, if I take one" reads as never married (REVIEW_BACKLOG FM-07). The fix in the table ("Not to any husband I take") fits both chapters and gives nothing away.
2. **Padmini is on the verandah until 70, then vanishes from the scene and "steps back" at 200.** Add her exit after 70 ("Padmini Amma went in to greet the elders."). This mends 200 and explains why no one translates for him (see 5).
3. **Padmini's stick.** It is her signature prop in Ch 8 (about 30 mentions in the book) and is missing here, where she rides with a sword "at her right side". A right-handed woman wears a blade on the left. Put the stick behind the saddle (as in the Option A text) so it can tap the stone at 200, and drop "right".
4. **Ibrahim rides in at 12 and never appears again.** Either drop him from 12 or give him one beat, for example staying with the horses at the gate.
5. **Language.** Revathi speaks slow Malayalam "so even a northerner" can follow (74), he says "I learn it ... Slowly" (80), and then he follows twenty lines of politics without a slip. VOICE_BIBLE 3.8 rule 10: he does not "understand every language in the room". The new line at 148 ("I made her say the name of the house twice before I had it") gives him one honest stumble on the hardest word in the chapter. With Padmini gone, no one else can help him.
6. **Seated or standing.** He is seated on a mat at 52, yet Revathi says "Sit" at 88. Add "I got to my feet." after 62. Change 60 to "over the stone" so that "verandah" does not appear in two lines running.
7. **The brand moves across the book:** his shoulder or arm (ch4:19, 45), his left wrist with ridged letters (ch17:119, ch20:242), and here a "long white scar on my forearm" (238). The fix at 238 moves Revathi's attention to his bandaged fingers (ch1:13, ch8:75), which leaves the brand free to settle on the wrist book-wide. Ch20:372 says she "had traced" the brand before; the near touch at 244 is a good plant for that, whichever mark it is.
8. **Timeline in the coda.** At 220 it is night and the hall has emptied; at 254 drums and old women fill it, and he enters a second time. Cutting 254 resolves it.
9. **Groundnut (56).** Groundnut was not a Deccan staple in the 1730s (REGISTER_AND_ANACHRONISM ch9:56). VOICE_BIBLE's Deccan word list (the "The Deccan at home" row) also cites groundnut from this line. Drop it there too when the voice bible is next revised.
10. **Period dress (64, 190).** A sari worn with "one shoulder bare" reads as modern costume. A Nair court lady of 1740 would wear the mundu and an upper cloth (melmundu or neriyathu). Check with a costume source before changing "sari" book-wide.
11. **Side saddle (10).** "Side saddle" names a European saddle. Horses were scarce on this coast, which is why his cavalry matters, and a Nair noblewoman would more often travel by manchal or palanquin. If Padmini rides, "sitting sideways" avoids the European term. Her riding is itself worth a line of surprise from a Maratha horseman.
12. **Writing tablets (42) and dowries (192)** are fixed in the table. Kerala scribes used palm leaf and an iron stylus, and a marumakkathayam house pays no dowry.
13. **Velinadu's history.** Lines 16, 100 and 132 borrow the Attingal killings of April 1721, when the queen's people killed a party of English Company men from Anjengo. The glossary lists Attingal separately as a real house, and the Author's Historical Note calls Velinadu invented and "inspired by" coastal matrilineal houses. Consider naming Attingal and 1721 in the note, so that informed readers see the borrowing is deliberate.
14. **"South" at 140.** Whether the Dutch lie south depends on where Velinadu sits. Their strongholds at Kochi and Quilon lie north of Travancore's heartland, while their post at Thengapattanam and the 1741 landing at Colachel lie south. Check against the book's map.
15. **Duplication with neighbouring chapters.** Ch10:3 opens on "In the Deccan, a kingdom revealed itself in its forts", the same contrast as ch9:24. The fix at 24 leaves that idea to Ch 10. Ch11:267 ("I filed the name away. Kottarakkara. Elayadathu.") reads as a first hearing. After this chapter he has heard both names from Revathi, so Ch 11 should say he had heard them once already, on a verandah in Velinadu.
16. **Motifs this chapter should give up.** "The land remembers" (206) belongs to Revathi at ch18:193 ("Paper burns. Land remembers."). The storm aphorism (216) is reserved for ch13:321. Blade similes (254) repeat at ch14:185. The "In Goa ... Here" contrast (210) is kept only in Ch 21.
17. **Optional.** At 222, a Velinadu servant would hardly call his own mistress "the Velinadu lady". "The Thampuratti asks if your feet remember her verandah" keeps the line and makes the servant local. This is a small change; take it only if the author wants the term.
18. **Ration check after the fixes** (scratch pass): "as if" 1 (100); slowly/quietly/softly 2 (74 in narration, "Slowly" at 80 in speech); "mouth twitched" 1 (32); "slightly" 0; weight or weigh 1 (54); "men like you/me" 2 (154, 156); "It was not a question" 0; Not-X constructions on two lines, both in dialogue (138, 184).
