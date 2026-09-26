# Second-Edition Audit: Chapter 10, Lessons in Travancore

- Source (frozen first edition): `book1_horse_servant/book2_chapter10_lessons_in_travancore.md`, 201 lines, 2,587 words.
- Method: I read the whole chapter with line numbers and ruled on all 81 flags from the pattern auditor and all 26 suspect passages from the holistic reader, merging duplicates. I cross-checked against Ch 6 (L5, L41, L113), Ch 8 (L217, L231 to 239), Ch 9 (L24, L132), Ch 11 (L3, L7, L123), Ch 25 L198, STYLE_SHEET.md, VOICE_BIBLE.md, REGISTER_AND_ANACHRONISM.md, OPENINGS_ENDINGS_MOTIFS.md and REVIEW_BACKLOG.md. I also ran `audit/tools/scan_slop.py -k all` on this chapter (output kept out of the repo). Line numbers refer to the first-edition file.
- Quotation marks in the fixes are curly, to match this source file.

## Verdict

| Measure | Call |
|:-|:-|
| Severity | **4 of 5** |
| Recommended intensity | **Deep**, applied unevenly: medium (tics and tightening) for the walk, L15 to L135; line-level re-voicing and a rebuild for L137 to L201 |
| Estimated word cut | **About 27%** (2,587 to roughly 1,900 words, after the short additions proposed below) |

The chapter's bones are good. The walk has four stops, and at each one the people talk like people: Nagoji's "Gods and I have an understanding", the lame temple elephant, the pepper woman's "fewer worms than your honesty", Yusuf's glance at the factor, the mercenary's "First they learn left from right", Ibrahim's quay, and "Borrowed eyes... We will see how long he keeps the loan." None of that needs more than a light hand.

The slop sits in three places:

1. **Ramayyan's thesis speeches.** Nearly every stop ends with him stating the point the scene has just made (L49, L75, L103, L137, L147, L151, L157). Counting Nagoji's own versions (L7, L143, L199 to 201), the lesson is stated outright about ten times.
2. **Nagoji's reflections** (L139 to L143). A modern essayist's voice ("the weight of new connections"), then a then-and-now symmetry that contradicts Ch 8's picture of Pune.
3. **Sections two and three** (L169 to L201). Almost all summary, in twentieth-century vocabulary ("state-building", "total erasure", "years of consolidation", "internal map", "request/requirement", "supply lines", "unit"). Every section ends on an aphorism (L165, L187, L199 to 201), and the chapter ends three times.

The 27% cut is high, and it is deliberate. About 450 of the roughly 700 words come from the three restatement blocks (L137 to 143, the middle of L151, and the L191 to 201 coda). No scene, plot beat or historical fact is lost, and every passage listed under **Passages to protect** survives.

**Where I overruled the auditors or the book-level plan:**

- **Opening.** Both auditors flag the thesis opener. OPENINGS_ENDINGS_MOTIFS.md says keep it because the chapter answers it. I recommend moving it: keep the fort-reading, but make it something Nagoji does in the temple, not a thesis the chapter illustrates. Ch 6 L5 and Ch 9 L24 have already made the Deccan-walls contrast, so this would be the third in five chapters.
- **Ending image.** The holistic reader and the book-level plan both propose ending under Padmini Amma's jackfruit tree. I reject that. Ch 8 already closes there (L231: "I sat alone on the stone platform under the jackfruit tree"), and the book-level plan's proposed 2e ending for Ch 8 is also under that tree, with the kalari boys shouting. See **Ending**.
- **L71.** Both auditors keep only the pepper woman's first sentence. I keep her second as well ("Your ships carry news as well as goods"), because it is the jab that makes Yusuf look at the factor at L73.
- **L151, "Men like you... Men like him".** The pattern auditor would cut it. I keep it, as the holistic reader does, as Ramayyan's one aphorism in the chapter.
- **L187, the reload line.** The pattern auditor would cut it. VOICE_BIBLE 3.2 names it as a line that passes. I keep it, stripped of "And I learned that" and folded into a paragraph.
- **L53, "Some by...".** The pattern auditor calls it a mechanical triad. It is a man pointing at lamps one by one. I keep it.
- **L171, wet season and monsoon.** The pattern auditor says they are the same season. This coast has two rains, so that objection falls. The sentence still needs fixing, for its "not X but Y" frame, its geography and its continuity.

Tally: 51 confirmed, 13 borderline, 13 defended.

## Confirmed issues

| Line | Quote | Category | Suggested fix |
|:-|:-|:-|:-|
| 5 | "Temples and markets came later, clustering under the shadow of those choices." | abstract_depth | "Temples and markets grew up afterwards, under the walls." (If Opening option A is taken, the whole paragraph moves into the temple scene.) |
| 7 | "In Travancore, I learned, you had to listen in different places." | kicker (thesis signpost) | Cut. The walk shows it. |
| 9 | "Ramayyan taught me that, though he never called it teaching. He simply appeared one morning ... his plain white cloth as neat as if it had never seen dust" | correction (stock mentor frame), filler, "as if" | "Ramayyan came for me one morning at the quarters Padmini Amma had given me, his white cloth clean, his palm leaves under one arm." |
| 17 | "Not the great shrine at Padmanabhaswamy, which I had heard of but not yet seen, but a smaller temple on a hill" | correction | Merge with L15: "We started at a temple on a hill above a cluster of houses and pepper gardens. It was a small place. The great shrine of Padmanabhaswamy I knew only by name." (Keeps the plant for Ch 28.) |
| 17 | "Its gopuram was modest by southern standards, its stone steps worn hollow in the centre by generations of feet." | stock_phrase; POV (he has no southern standards yet) | "Its gateway was low and roofed with tile, and its stone steps were worn hollow in the middle." |
| 17 | "It was dedicated to Lord Ayyappa, the forest warrior, brother of Ganapati and patron of all who carried arms in these hills." | guidebook gloss | "The god was Sasta, the forest warrior. Men who carried arms in these hills came to him before a fight." ("Lord Ayyappa" is modern devotional English; Sasta or Ayyan is the period name.) |
| 19 | "He returned each with the same small nod, storing something behind his eyes." | abstract_depth ("something") | "He returned each with the same small nod, and more than once he looked back to see which house a man had come out of." |
| 21 | "Brahmins moved through their rituals like men repeating a song they had sung since childhood. Oil lamps flickered. Bells chimed. The smell of ghee and incense wound itself around the stone pillars." | simile_stack; fragment list; personified smell | "Inside the outer courtyard, Brahmins went through their rites without once looking at their hands, the way a groom saddles a horse he has saddled a thousand times. Oil lamps burned in rows along the walls, and the place smelled of ghee and incense." (Keep the lamps. L35 depends on them.) |
| 23 | "a Deccan non-Brahmins like me" | copyedit | "a Deccan non-Brahmin like me" |
| 29 | "He smiled faintly." | stock beat; continuity | "He let that pass." (Ch 25 L198 says Nagoji saw Ramayyan smile "for the first time in all the years I had known him". Every earlier smile spends that payoff.) |
| 49 | "A temple is not just stone. It is a ledger. Offerings in. Blessings out. The names written on both sides matter." | correction; fragment pair; kicker | "“If he wants men to believe the god favours his reign,” Ramayyan said. “A temple is a ledger, Sawant. Read it.”" (Keeps the ledger plant the book-level plan wants for Chs 21 and 25. L51 to 53 then do the reading.) |
| 57 | "There, under awnings of cloth and palm leaves, the kingdom took another shape." | abstract_depth | "The market stood under awnings of cloth and palm leaves." |
| 57 | "their eyes constantly flicking toward the path that led to the backwaters" | stock_phrase (repeats L73) | "watching the path that led down to the backwaters" (Save the flicking eyes for Yusuf.) |
| 57 | "An Arab merchant in a flowing white robe" | stock_phrase (costume) | "An Arab merchant" |
| 57 | "each sack a *candi*, I had learned, roughly five hundred pounds, the measure by which fortunes were made or lost on this coast" | modern_register; history | "while his servant counted sacks of pepper against the *candi*" (A candi is a weight, not a sack. "Pounds" is an English unit. A Pune man grew up with the *khandi* and needs no gloss.) |
| 57 | "writing contracts in a hand that flowed like water; beside him, a stack of *hundis*, bills of exchange that could turn pepper in Travancore into gold in Muscat without a single coin crossing the sea" | simile; reader-facing gloss | "Nearby a Syrian Christian scribe sat at a low desk writing contracts, with a stack of *hundis* at his elbow, the same paper the sahukars wrote in Pune, only these would be paid out in Muscat." |
| 59 | "“Do you see the pattern?” Ramayyan asked." | modern_register ("pattern"); mentor stock | "“What do you see?” Ramayyan asked." |
| 71 | "When you bring Dutch coins into our land, remember that the king counts them with his fingers, not yours." | dialogue_exposition | Cut this sentence only. Keep "My pepper has fewer worms than your honesty" and "Your ships carry news as well as goods." |
| 75 | "Too high, the Marakkar captain goes to another coast. Too low, the queen in Padmanabhapuram cannot buy Dutch guns to shoot back at Dutch ships." | balanced_antithesis; explains the glance; factual slip | End the line at "“The king's tax sits between them,” Ramayyan said." and let him walk on. If a reason must stay, use one clause: "Set it too high and the Marakkar sail for another coast." (Never "the queen". Before Ch 16, "Kalkulam", not "Padmanabhapuram".) |
| 85 | "Not De Lannoy. Not yet. This man was older, his belly soft, his eyes wary. One of the earlier European mercenaries who had sold his skill where he could." | correction; foreshadowing tic | "He was older than most soldiers I knew, soft in the belly and wary in the eye, one of those Europeans who sold his skill to whoever paid." |
| 95 | "The smell of saltpetre and burned powder wrapped itself around us." | stock_phrase (repeats L21's smell shape) | Merge with the sentence before: "Smoke rolled out in a white sheet, stinking of saltpetre and stinging my eyes even from the side." |
| 103 | "But this is only one rhythm. Yours is another. The temple has its own. The market too. A kingdom survives when these rhythms do not trip each other up." | fragment_list; kicker | Cut. End the speech at "...or they will die confused when the Dutch play their drums.”" |
| 107 | "There, in the maze of narrow channels and broad lagoons, the kingdom's veins opened." | stock_phrase ("veins" also at Ch 7 L175 and Ch 26) | Merge into L105: "We walked on, down to the backwaters, where narrow channels opened into broad lagoons." |
| 109 | "Boats moved along the water like insects ... The water's surface reflected palm fronds and sky in shards that broke and reformed with every ripple." | simile_stack | "Boats moved on them, small ones with one or two men poling, broad low ones piled with sacks until the water stood a hand's width below the side." (Sets up Ibrahim's overloaded boat at L111.) |
| 135 | "Ramayyan's eyes crinkled at the edges." | stock beat; continuity (Ch 25 L198) | "Ramayyan made a mark on one of his leaves." (It answers Ibrahim's joke about scribes' memories, and it is the chapter's one leaf-and-stylus beat.) |
| 137 | "“See,” he said to me as we left the quay. “Horses carry men to battle. Boats carry the coin ... you will know why they move.”" | explained_subtext | Cut the paragraph. Ibrahim's "Water is a road" has already made the point. |
| 139 | "My head, too, buzzed with the weight of new connections." | abstract_depth; modern | Cut. Keep the first sentence (legs aching more than after a ride). |
| 141 | "In Pune, the world had been simple. Orders came. Men rode. Villages paid. Priests blessed. Merchants complained. ..." | fragment_list; continuity | Cut. Ch 8 L233 has Pune power in "silk and pearls ... behind carved screens", so it was not simple, and a huzurat trooper knew sahukar credit and court factions. |
| 143 | "Here, everything tied to everything else with threads I had not seen at first." | explained_subtext; thread motif | Cut. (For the list sentence that follows, see Borderline.) |
| 147 | "For him, conquest is not only taking land. It is knitting these pieces together so that when a Dutch cannon fires at one place, the rest does not unravel." | correction; knit/unravel | Cut. Keep the first sentence (Borderline) so Nagoji can answer it at L149. |
| 151 | "In the early years he turned his sword inward, against the Lords of the Eight Houses ... Only after those knots were cut could he afford to reach outward, toward Kayamkulam and the other neighbours, and then toward Dutch cannon." | dialogue_exposition (history briefing, two back-to-back triads, "the weight of", "knots") | Cut the middle run. Keep: "“He has been at war since before he took the throne,” Ramayyan said. “First with his own family. Then with the chieftains who thought him a boy.” He glanced toward the fort above us. “Men like you feel war when the drums beat. Men like him feel it when the accounts do not balance.”" (The Eight Houses repeat Ch 8 L217. The list of attempts repeats Ch 21 L189 and Ch 22 L335, and the book-level plan keeps Ch 21's.) |
| 157 | "When the time comes, the Maharaja will expect you to ride in ways that suit them. Not only your own." | correction; foreshadowing tag; unclear "them" | "“You have a sharp eye, Sawant,” he said. “You see angles on a battlefield. Learn to see these. One day the Maharaja will send you to ride for a grain levy, not a battle.”" (Plants the levy scene at L175.) |
| 161 | "He regarded me for a moment, as if tasting the shape of my answer." | simile_stack ("as if", "shape") | "He looked at me a moment longer than I liked." |
| 165 | "That conversation was the first lesson. The application came soon after." | summary_ending | Cut. Section one ends on "“We will see how long he keeps the loan.”" |
| 169 | "The months blurred into seasons, the seasons into years." | stock_phrase; timeline | "Through the rest of that year and into the next, I rode wherever Ramayyan's leaves sent me." |
| 171 | "I marked time not by calendars but by campaigns: the wet season when we rode against the Kayamkulam chiefs, the dry season when we fortified the northern passes, the monsoon when even horses learned to pray for solid ground." | correction; padded triad; geography; continuity | "That dry season we dug earthworks in the passes under the eastern hills. The monsoon we spent in the mud, when even the horses learned to pray for solid ground." (Travancore's passes lie south and east. Kayamkulam belongs to Part IV.) |
| 171 | "Each year the kingdom grew a little larger, a little tighter, a little more certain of its shape." | tricolon | Cut. |
| 173 | "In those years before the Dutch clouds fully gathered, the King turned his “borrowed eyes” inward as Ramayyan had promised." | stock_phrase; continuity | Cut. Ramayyan promised nothing, the eyes were Nagoji's, and the loan line at L163 is stronger left unexplained. |
| 175 | "We rode not against foreign armies, but against the stubborn knots of the internal map. I learned that a “campaign” in Travancore did not always mean a pitched battle." | correction; explained_subtext; modern | Cut. Open the paragraph at "Some days I rode with Padmini Amma to a chieftain's estate..." |
| 175 | "My presence, and the fifty Maravar lancers behind me, turned a “request” into a “requirement.”" | modern_register (office wordplay in scare quotes) | "She asked. He paid. The fifty Maravar lancers sitting their ponies behind me, in plain sight of his granary, may have helped him with his sums." |
| 177 | "Other times, it was sharper." | kicker | Cut. |
| 179 | "a raid on a recalcitrant *madampi* ... a young King's decrees. He did not know that Ramayyan had mapped his supply lines, or that I had trained a unit of Maravar horsemen to cut through bamboo dampness as if it were dry grass." | modern_register | "The raid I remember best was on a *madampi* near Attingal who would not send his men to the new drills. He trusted his walls and his bamboo to keep out a king he still thought of as a boy. Ramayyan had counted every cart that fed that house for a month, and my Maravar had spent the rains learning to take their ponies through bamboo." |
| 181 | "There was no glory in it, only the brutal efficiency of state-building. ... a choice: total submission or total erasure." | modern_register; correction | "We took his walls at dawn. In the smoking courtyard of a house that had been noble for three hundred years, the King gave the old chief his choice: kneel, or watch the house pulled down to its plinth. He knelt." |
| 185 | "It was during these “years of consolidation” that I stopped being a guest and became a limb of this growing beast." | modern_register; narrated growth (STYLE_SHEET 4) | Cut. |
| 185 | "I learned to distinguish the sullen silence of a conquered village from the quiet respect of a protected one." | balanced_antithesis | "I came to know which villages hid their grain when our horses came and which brought out water for them." |
| 191 | "Seasons passed in this way. Dust and rain and the slow grinding of old orders into new shapes." | fragment_list; abstract | Cut. |
| 191 | "By the time the Dutch began to show their teeth more openly, ... and forgotten what the Deccan hills looked like except in dreams." | stock_phrase; continuity | "By the time the rains ended I had ridden every road in the kingdom at least twice." Move it into section two. (Teeth are reserved for Part IV and Ch 11 L87. Chs 19, 22 and 25 depend on the Deccan still pulling at him, so he has not forgotten it.) |
| 193 | "One night, back at Padmini Amma's estate, as I sat under the jackfruit tree ... I thought of those early lessons." | summary_ending | Cut. It labels the lessons, and the jackfruit tree with kalari shouts is Ch 8's closing image. |
| 195 | "Temple to market. Market to training ground. ... Houses to Velinadu's halls." | fragment_list | Cut. It recaps the walk and adds a fort and a palace that the walk never visited. |
| 197 | "In Goa, chains had held me still in one place. Here, invisible cords tied me to many." | balanced_antithesis | Cut. The book-level plan keeps only Ch 21's Goa contrast, and Ch 8 L233 has already used Goa/Pune/Here. |
| 199 to 201 | "Travancore was already at war, even in its quiet moments. It had just learned to fight with more than swords. / If I wished to survive, I would have to learn the same." | summary_ending | Cut. The third "already at war", and the same survive-and-learn close as Ch 4 L123 and Ch 8 L239. See **Ending**. |

## Borderline

| Line | Quote | Why it is borderline | Recommendation |
|:-|:-|:-|:-|
| 3 | "In the Deccan, a kingdom revealed itself in its forts." | Plain, and the chapter does answer it, but it is the third Deccan-walls contrast in five chapters (Ch 6 L5, Ch 9 L24). | Prefer Opening option A, where the fort-reading becomes an action. If kept, merge with L5: "In the Deccan I read a kingdom from its forts." |
| 13 | "When the diwan of a kingdom tells you to walk, you do not ask where." | Dry, and it does not restate anything, but it is a second-person maxim in a chapter full of maxims. | "I did not ask where." keeps the joke in his own voice. |
| 19 | "women and men stepped aside" | The order may be deliberate in a matrilineal district (Ch 8 L233), but it reads as modern. | Name them: "the women at the well and the men on the pepper mats stepped aside". |
| 45 | "the elephant that carries the idol in procession" | "Idol" is a missionary's word. A Brahmin official would not use it for his own god. | "the elephant that carries the god in procession" |
| 63 | "“Look closer,” he murmured." | The pivot is needed. The tag is soft, and it is the third of four murmurs. | "“Look again,” he said." |
| 65 | "not Ibrahim but his cousin Yusuf" | Functional, but it adds to a heavy "not X but Y" count. | "a Marakkar captain, Ibrahim's cousin Yusuf, leaned across..." |
| 79 | "knows half a kingdom. The other half lives here, in the way people say 'our pepper' and 'the king's pepper' as if they are the same, or as if they are not." | The observation is good, heard with the ear. The double "as if" is a hedge. | "“A diwan who hears only petitions knows half a kingdom,” he said. “The other half is here, in whether a man says ‘our pepper’ or ‘the king's pepper’, and which one he says when he thinks I cannot hear.”" |
| 89 | "Ramayyan said mildly." | The tone is already in the line. | Drop "mildly". |
| 95 | "On the next word the line fired as one." | Stock, and a perfect volley undercuts the mercenary's "First they learn left from right." | "On the next word the line fired, the left end a breath behind the right." |
| 143 | "A temple roof and a musket barrel and a boat's cargo and a pepper vine and a boy in a kalari and a woman on a mat counting coins all tugged on the same knot." | Both auditors would keep it for its concrete nouns, but it is still a recap, and "knot" belongs to the thread family (seven uses in this chapter). | Cut with L141 to 143, or re-voice it as his own failed reckoning: "I tried to reckon the day as I would reckon a march, fodder against distance, and could not make the sums close." |
| 147 | "“You see now why the Maharaja thinks of war even when he sits in a temple courtyard,” Ramayyan said." | "You see now" explains, but it gives Nagoji a line to answer at L149. | Keep if L149 stays. Otherwise cut. |
| 153 | "The day was nearly done. Men inside already sat over palm leaves and cups of buttermilk, murmuring over plans." | The buttermilk is exact. The rest is filler. | "We reached the hall. Inside, men sat over palm leaves and cups of buttermilk, arguing figures." |
| 183 | "I do not destroy them because I hate them. I break them so they can be reset into a stronger bone." | The bone-setting image belongs to this coast. The not-because frame is the tell. | "“A bone that sets crooked has to be broken again,” Marthanda Varma said to me on the ride back, the smell of wet ash still on our clothes. “Ask any kalari healer.”" |

## Defended (flagged, but keep)

| Line | Quote | Reason |
|:-|:-|:-|
| 19, 99 | "murmuring greetings"; "“Praise indeed,” I murmured." | Of the four murmurs, keep these two. L99's murmur motivates "He glanced at me" at L101. Cut the tags at L63 and L153. |
| 41 | "I thought of the boys in the kalari, of women sorting pepper, of carts groaning under loads of paddy." | His thinking on the way to his answer, built from things he saw in Ch 8. Optional trim: "the paddy carts on the estate road". |
| 53 | "Some by Padmini's line. Some by fishermen. Some by men who own no land but rent their backs to others." | A man pointing at lamps one by one. "Rent their backs" and "feeds their god" are the best lines in the speech. |
| 57 | The market roll call (interior traders, Marakkar, Arab, Syrian Christian) | The communities are historically right, and the Yusuf scene grows out of the list. Trim the ornaments (rows for L57 above), not the people. |
| 71 | "Your ships carry news as well as goods." | This is the jab that sends Yusuf's eyes to the factor at L73. Without it the glance has nothing to answer. Cut only the sentence after it. |
| 73 | "Yusuf laughed, but his eyes flicked sideways" | The chapter's best subtext. Fix the duplicate at L57 instead, and do not let L75 explain it. |
| 97 to 99 | "“Adequate,” Ramayyan said. / “Praise indeed,” I murmured." | VOICE_BIBLE cites "Adequate" as Ramayyan at his best. It is understatement, not drawing-room banter. |
| 119 | "I admire anyone who rides it as if it were a road." | It sets up Ibrahim's "Water is a road". This is the one "as if" the chapter keeps (the ration is one). |
| 149 | "“He is already at war,” I said. “Even when the Dutch have not fired.”" | Nagoji draws the conclusion himself, which the holistic reader's own voice note asks for. Keep this one and cut the echoes at L199. |
| 151 | "Men like you feel war when the drums beat. Men like him feel it when the accounts do not balance." | A mirrored maxim, but it is Ramayyan's one aphorism in the chapter, in his ledger idiom and aimed at Nagoji. Characters get about one per scene. |
| 171 | "the monsoon when even horses learned to pray for solid ground" | A horseman's image. The objection that the wet season and the monsoon are the same season does not hold on a coast with two rains. It survives in the rewrite above. |
| 185 | "I learned to eat rice from a plantain leaf without spilling it, and to speak enough Malayalam to order a charge or a retreat." | Belonging shown through small skills, which is exactly what STYLE_SHEET 4 asks for. The "I learned" count is fixed by rewriting the sentences around it. |
| 187 | "And I learned that peace here was just a word for the time it took to reload." | VOICE_BIBLE 3.2 passes it: "A soldier's joke with a musket in it." Keep the joke. Drop "And I learned that" and make it the last sentence of the section-two paragraph, not a section-closing one-liner. |

## Opening

Current (L3 to L13):

> In the Deccan, a kingdom revealed itself in its forts.
> You could stand on a bastion and read a ruler's mind in stone and mortar; how high he built his walls, how thick he poured his lime, where he dug his wells, where he placed his cannon. Temples and markets came later, clustering under the shadow of those choices.
> In Travancore, I learned, you had to listen in different places.
> Ramayyan taught me that, though he never called it teaching. ...
> When the diwan of a kingdom tells you to walk, you do not ask where.

**Verdict: revise.** The first line is an aphorism, the third mirrors it, and the fourth labels the scene as a lesson. The chapter's argument is announced before a single thing happens, so every stop on the walk reads as an illustration. The one living sentence is L5's list, a cavalryman's real habit. Ch 6 L5 and Ch 9 L24 have already made the Deccan-walls contrast.

**Option A (preferred).** Open in scene. Move the fort-reading into the temple, where it becomes something he does and gets gently corrected:

> Ramayyan came for me one morning at the quarters Padmini Amma had given me, his white cloth clean, his palm leaves under one arm.
>
> “Walk with me, Sawant,” he said.
>
> I did not ask where.

Then, after the courtyard sentence at L21:

> From habit I looked the place over as I would a fort in the Deccan: how high the walls, how thick the lime, where the water was, where a gun could stand. The walls would not have stopped a goat. Ramayyan was looking at the lamps.

L35's "Who pays for the oil in those lamps?" then answers Nagoji's way of reading a kingdom with Ramayyan's, and nobody has to say so.

**Option B (lighter).** Merge L3 and L5 into one paragraph ("In the Deccan I read a kingdom from its forts. You stood on a bastion and saw a ruler's mind in stone and mortar: how high he built his walls, how thick he poured his lime, where he dug his wells, where he placed his cannon. Temples and markets grew up afterwards, under the walls."). Cut L7 and the first sentence of L9, and use "I did not ask where." for L13.

## Ending

Current last lines (L193 to L201):

> One night, back at Padmini Amma's estate, as I sat under the jackfruit tree listening to distant temple bells and nearer kalari shouts, I thought of those early lessons.
> Temple to market. Market to training ground. Training ground to backwaters. Backwaters to fort. Fort to palace. Palace to houses like Padmini's. Houses to Velinadu's halls.
> In Goa, chains had held me still in one place. Here, invisible cords tied me to many. If one snapped, I had no doubt the others would tighten.
> Travancore was already at war, even in its quiet moments. It had just learned to fight with more than swords.
> If I wished to survive, I would have to learn the same.

**Verdict: rewrite.** The chapter ends three times (L165, L187, L199 to 201), each time on a moral. The last run is a recap chain, a Goa/Here symmetry and two morals. It also repeats Ch 8's close almost move for move: the jackfruit tree and kalari shouts (Ch 8 L231), a Goa/Pune/Here contrast (Ch 8 L233), and "If I was to survive ... I would have to learn" (Ch 8 L239). That is why I reject the jackfruit-tree image that the holistic reader and the Ch 10 row of OPENINGS_ENDINGS_MOTIFS.md both propose: it would give Chs 8 and 10 the same closing image. The book-level plan's Ch 10 row should be updated to match.

**Proposed.** Cut L165 and L173 to L201. Rebuild section two from the material the chapter already has, in this order: bridge, levy, belonging, raid. End on the raid's consequence (about 300 words, replacing about 590):

> Through the rest of that year and into the next, I rode wherever Ramayyan's leaves sent me. That dry season we dug earthworks in the passes under the eastern hills. The monsoon we spent in the mud, when even the horses learned to pray for solid ground.
>
> Some days I rode with Padmini Amma to a chieftain's estate, a man who had once pledged himself to one of the Eight Houses, and stood by the gate while she settled the grain levy. She asked. He paid. The fifty Maravar lancers sitting their ponies behind me, in plain sight of his granary, may have helped him with his sums.
>
> I came to know which villages hid their grain when our horses came and which brought out water for them. I could eat rice from a plantain leaf without spilling it, and I had enough Malayalam to order a charge or a retreat. By the time the rains ended I had ridden every road in the kingdom at least twice. Peace here was just a word for the time it took to reload.
>
> The raid I remember best was on a *madampi* near Attingal who would not send his men to the new drills. He trusted his walls and his bamboo to keep out a king he still thought of as a boy. Ramayyan had counted every cart that fed that house for a month, and my Maravar had spent the rains learning to take their ponies through bamboo.
>
> We took his walls at dawn. In the smoking courtyard of a house that had been noble for three hundred years, the King gave the old chief his choice: kneel, or watch the house pulled down to its plinth. He knelt.
>
> “A bone that sets crooked has to be broken again,” Marthanda Varma said to me on the ride back, the smell of wet ash still on our clothes. “Ask any kalari healer.”
>
> His sons marched with us the next week. I rode behind them, where I could see their hands.

Why this works: the last line is an action and an image. It quietly pays off "We will see how long he keeps the loan" (L163), because Nagoji is now doing the King's watching, and nobody names it. It also shows the kingdom swallowing its enemies instead of saying so. It shares no closing idea with the planned endings for Chs 8, 9, 11 or 12 (the jackfruit and crows, Revathi's "new toy", ship smoke, the saddlers' lamp).

One echo for the author to decide on: the planned Ch 16 ending has the King's Nair guards following Nagoji and Lannoy "three paces behind". Read together, the two form a mirror: in Ch 10 Nagoji watches the newly absorbed, and in Ch 16 he is watched as one of them. Keep that on purpose, or vary one of them.

**Cut-only fallback:** move the L185 plantain sentence and the L187 reload joke above the raid, cut L173 to 177 and L185 to 201, and end on L181's own last sentence: "His sons marched with us the next week."

## Flab (passages to tighten)

| Lines | Issue | Action |
|:-|:-|:-|
| 3 to 13 | Thesis, gloss, mirror, lesson label and maxim before any action | Three short paragraphs (Opening option A). |
| 17 | Guidebook gloss: gopuram standards, generations of feet, appositive chain on the god | About 70 words down to about 55 (rows above). |
| 49, 75, 103 | Each stop ends on Ramayyan's moral | Cut the morals. Let the training ground and the backwaters end without one. |
| 57 | One 150-word catalogue sentence with two similes, two glosses and a unit conversion | Down to about 105 words. Keep every trader. |
| 107 to 109 | A lyrical establishing paragraph that copies L57's "There, ... the kingdom took another shape" | One sentence. The boat detail should set up Ibrahim's overloaded boat. |
| 137 to 143 | Recap speech, abstract reaction, then-and-now symmetry, thread metaphor | Keep one sentence (L139's legs). About 175 words down to about 20. |
| 147 to 151 | Two more thesis statements and a 150-word history briefing that repeats Ch 8 L217 and Ch 21 | About 200 words down to about 70 (rows above). |
| 157 to 165 | Foreshadowing tag, "as if" pause and a section label on top of the chapter's best exchange | Trim. End the section on the loan line. |
| 169 to 201 | Two time-skip summaries, definitions, scare quotes, three aphorism closes and a recap coda | Rebuild as in Ending (about 590 words down to about 300). |

Motif counts to bring down in the edit:

- thread, knot, cord, knit, unravel: 7 (L143 twice, L147 twice, L151, L175, L197). Target 0 here; the thread belongs to Ch 20.
- "shape": 4 (L57, L161, L171, L191). Target 0.
- body metaphors (veins, limb, beast, bone): L107, L185, L183. Keep only the King's bone.
- "I learned": 6. Target 1 or 2.
- "as if": 6. Target 1 (L119).
- "not X but Y" and "Not X." openers: 8 in narration or tags. Target 0 in narration.

## Passages to protect

- L5, the fort list: "how high he built his walls, how thick he poured his lime, where he dug his wells, where he placed his cannon". Relocate it; do not lose it.
- L25 to L27: "Gods and I have an understanding ... I try not to waste their time."
- L35 to L47: the lamp-oil catechism, the leaking roof, the lame elephant, and "“The king,” I said. “If he is wise.”"
- L53: "men who own no land but rent their backs to others" and "they remember whether he feeds their god".
- L61: "I see men arguing over coins. That is the same everywhere."
- L67 to L71: the worm-eaten pepper, the baby on her hip, "My pepper has fewer worms than your honesty."
- L73: Yusuf's sideways glance and the scribe's tiny adjustment. Never explain it.
- L85 to L93: the mercenary's soft belly, "Ram, my friend", "First they learn left from right."
- L97 to L99: "Adequate." "Praise indeed."
- L103, first sentence: "or they will die confused when the Dutch play their drums."
- L111 to L133: the whole quay scene with Ibrahim.
- L139, first sentence: legs aching more from walking than from a morning's ride.
- L149 and L151's frame: "He is already at war" and "Men like you feel war when the drums beat. Men like him feel it when the accounts do not balance."
- L153: buttermilk and palm leaves.
- L159 to L163: "He has my sword ... My eyes he can borrow when he asks." / "Borrowed eyes ... We will see how long he keeps the loan."
- L171: "even horses learned to pray for solid ground".
- L175: standing silently by the gate while Padmini Amma negotiates the grain levy.
- L181 to L183: "His sons marched with us the next week" and "the smell of wet ash still on our clothes".
- L185: the plantain leaf and enough Malayalam to order a charge or a retreat.
- L187: the reload joke.
- L191: "I had ridden every road in the kingdom at least twice".

## Chapter-specific notes (continuity and history)

1. **Timeline.** The chapter's "years" (L169, L185, L191) do not fit between the 1738 capture (Ch 1 L11) and "late in 1739" (Ch 11 L3). Backlog N-49 applies. The rebuild above covers about a year. Ch 11 L3's "ending the years of quiet consolidation" should change at the same time.
2. **Kayamkulam.** L151 and L171 have Travancore campaigning against Kayamkulam before the Dutch war, but the Kayamkulam war belongs to 1742 to 1746 and to Part IV (Ch 22 "Command of the Marches"). Ch 11 L7 also gives a different outward campaign for the same months (Kollam and Desinganadu). Keep the outward war in Ch 11 and leave Ch 10 with internal work. The earthworks in the eastern passes link to Ch 12, where Chanda Sahib's raids come through those passes.
3. **Internal contradiction.** L151 says the inward wars are over. L173 to L175 then send the King's "borrowed eyes" inward "as Ramayyan had promised". The recommended cuts remove both.
4. **L75.** "The queen in Padmanabhapuram" should be the king (backlog N-34). Before Ch 16's renaming, the fort is Kalkulam (N-28).
5. **L57.** A candi is a weight of roughly five to six hundred pounds, not a sack (backlog N-33). Drop the conversion (VOICE_BIBLE Appendix C). "Sacks of rice and oil" should be "sacks of rice and pots of oil".
6. **L83.** A European mercenary drilling Nair troops in "broken Hindustani" is unlikely. On this coast the trade tongue for Europeans was Portuguese, usually worked through an interpreter: "shouting commands in a broken Portuguese that a boy beside him turned into Malayalam". The character guide's Karl August entry (backlog FM-03) is a separate problem.
7. **Smiles.** L29 ("smiled faintly") and L135 ("eyes crinkled") spend Ch 25 L198's "for the first time ... he smiled". Both are cut above.
8. **Pune.** L141's "the world had been simple" contradicts Ch 8 L233 and Nagoji's own background. It is cut above.
9. **Closing collisions with Ch 8.** Ch 8 already closes on the jackfruit tree, the kalari boys, a Goa/Pune/Here contrast and "If I was to survive ... learn". Ch 10's current coda repeats all four. Update OPENINGS_ENDINGS_MOTIFS.md's Ch 10 row so the two chapters do not share an image.
10. **L191, "forgotten what the Deccan hills looked like".** This is premature. The pull of the north drives Chs 19, 22 and 25.
11. **L151's list of assassination attempts** repeats Ch 21 L189 and Ch 22 L335. The book-level plan keeps Ch 21's. Its Eight Houses history repeats Padmini Amma at Ch 8 L217. Cutting the middle of L151 also removes the only use of *yogakkar*, which simplifies glossary item FM-10.
12. **Dhanaji** first appears unexplained at Ch 11 L123. Backlog N-01 suggests giving him an arrival in this chapter's montage. The natural place is the end of the bridge paragraph: "That was the season Dhanaji and four of my old riders came down the coast in one of Ibrahim's boats, thinner than I remembered and asking for work." This is optional, and it is the author's decision.
13. **L179, "a young King".** Marthanda Varma was past thirty and had ruled since 1729. The fix, "a king he still thought of as a boy", turns it into the *madampi*'s contempt and echoes L151's "chieftains who thought him a boy".
14. **L17, "Lord Ayyappa".** "Sasta" or "Ayyan" is the period usage. "Brother of Ganapati" is a reader's gloss, and it is cut.
15. **L65.** Yusuf is "recognised from the coastal hall", but he is not shown there in Ch 6. "Ibrahim's cousin Yusuf" is enough.
16. **Titles, book-wide decisions.** Ramayyan's historical title from 1737 was Dalawa. The book uses "diwan" through Ch 10 and "Dalawa" from Ch 13 (VOICE_BIBLE inconsistent forms). "King", "king" and "Maharaja" are capitalised inconsistently (L47, L147, L173, L181).
17. **Copyedits.** L23 "non-Brahmins" should be "non-Brahmin". Restore the hyphens in "worm-eaten" (L67) and "pale-faced" (L73); the book already hyphenates compounds such as "ink-stained" at Ch 1 L15. Remove the trailing whitespace on L17.
18. **Scanner counts, before and after the recommended edit** (`scan_slop.py -k all`): "as if" 6 to 1; "not X but Y" 5 to 1 (dialogue only, at most); "Not X." openers 3 to 0; fragments 9 to 0; "the weight of" 2 to 0; one-sentence paragraphs 30 to about 18.
