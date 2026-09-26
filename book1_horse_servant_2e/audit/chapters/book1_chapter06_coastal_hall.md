# Chapter 6 Audit: The Coastal Hall

Second-edition slop audit, adjudicated. Source: `book1_horse_servant/book1_chapter06_coastal_hall.md` (first edition, frozen; 193 lines, about 2,700 words). Line numbers are the physical lines of that file, blank lines included. Apply fixes from the bottom of the chapter upward so the numbers hold.

How this was judged:
- The chapter was read in full, together with the end of Chapter 5 (lines 120 to 177) and the opening of Chapter 7 (lines 1 to 30), because this chapter answers the first and hands off to the second.
- Two auditor reports (a pattern auditor with 70 flags and a holistic reader with 24 passages) were merged and ruled on flag by flag. The existing 2e audits (`STYLE_SHEET.md`, `VOICE_BIBLE.md`, `OPENINGS_ENDINGS_MOTIFS.md`, `REGISTER_AND_ANACHRONISM.md`, `REVIEW_BACKLOG.md`) were checked for earlier rulings. Where this report disagrees with one of them, it says so.
- Every confirmed fix below was applied to a scratch copy outside the repository to test the result. The draft ran from 2,703 to 2,174 words (minus 19.6 percent). `scan_slop.py` core hits fell from 41 to 28, and no marker went up. The one-sentence paragraph count fell from 27 to 25 once three small merges were made (noted in the table).

## Verdict

| Measure | Ruling |
|:-|:-|
| Severity | **3 of 5.** There is a noticeable pattern throughout, but it is not pervasive. The dialogue is mostly clean and often very good (lines 57 to 77, 97 to 115, 125 to 131, 157 to 171). The slop sits in the narration *between* the lines of speech, in the approach (lines 3 to 33), in one set piece (lines 139 to 155) and in the ending (lines 185 to 193). |
| Edit intensity | **Medium**: cut the tics and tighten. Two places need a structural fix: the pitch sequence (139 to 155) and the ending (185 to 193). Neither needs new material. About a dozen single lines are re-voiced; the rest are cuts. |
| Estimated word cut | **About 19 percent** (roughly 530 words). This is well above the plan's 5 to 10 percent, and the reason is specific. The pitch sequence and the ending together account for about 250 of those words. Both auditors and the book-level endings audit agree on both. Without those two, the chapter would lose about 10 percent. If the author keeps the approach paragraphs as they are, the cut falls to about 15 percent. |

The chapter's fingerprint, in order of damage:
1. **Reaction shots in place of reactions.** Across 14 "eyes" or "gaze" beats and a loop of stock micro-expressions (flicker, twitch, twitch "again" with no earlier twitch, unreadable eyes, thin smile, dry chuckle, studied in silence), the king and Ramayyan are described rather than shown. The chapter already has better tells (fingers on the spear shaft, the spear butt, "Ram", the map), and they are enough.
2. **The correction habit in narration** ("not X, but Y" and its cousins) at lines 9, 21, 25, 39, 47, 123 and 191, plus balanced symmetry at 35 and 53.
3. **Explaining the translation device.** The scene's best idea is that the king understands more than he lets on, and that Nagoji hears Malayalam as noise. The chapter shows this at 79 and 103 and then explains it at 107, 115, 119 to 123 and 143.
4. **Stacked closing beats.** The ending lands five times (185, 187, 189, 191, 193) and closes on a forge-and-blade summary.

## Confirmed issues

Fixes are written in Nagoji's voice and follow the house rules (no em dashes, no new plot). "Cut" means delete the quoted text and close up.

| Line | Quote | Category | Suggested fix |
|:-|:-|:-|:-|
| 5 | "high halls thick with incense, with carpets to muffle footsteps and paintings on the walls to remind visitors who held power. Here, on this coast, the hall where my fate shifted stood within sight of the sea." | stock phrase; portentous signposting | "In the Deccan, kings and sardars received men in high halls, on carpets, under painted walls. The king of this coast kept his hall within sight of the sea." |
| 7 | "The air carried a constant tang of salt and something metallic, as if the very wind had tasted blood." | melodramatic simile; vague "something" | "The wind off the sea left salt on my lips." |
| 9 | "This time I rode, though not as I had once ridden." | coy negation | "The bulls were gone. This time I rode." |
| 11 | "Still, the feel of a moving back under me, the sway of a neck, the rhythm of hooves on packed earth, did something to straighten my spine." | reflex tricolon; vague verb ("did something") | "Still, a horse was moving under me again, and my back straightened before I had thought to straighten it." |
| 13 | "his clothes different from the day I had first seen him in the fisher village. Now he wore a short coat over his vest, its pockets bulging with something that clinked softly when he moved." | throat-clearing; soft adverb; "vest" (register audit P3) | "Ibrahim rode a sturdy pony at my side. He had put on a short coat for the occasion, and its pockets clinked when he moved." |
| 15 | "Information costs, *bhau*. So do favours. When we reach the hall, remember that." | modern register ("information"); set-up that is never paid off | "News costs, *bhau*. So do favours." (See 43 for the pay-off.) |
| 19 | "a structure of wood and stone looked down on everything" | vague noun; personification (missed by both auditors) | "On a rise beyond the inlet stood a small fort of stone and timber." |
| 21 | "It was not large, not compared to the great forts of the north, but there was purpose in every line." / "curling motifs of vines and tigers" | correction; stock phrase; art-history word ("motifs"); third north-versus-here comparison | Cut the first sentence and begin "The outer wall was of rough red stone blocks, topped with a parapet..." Change the pillars to "carved with tigers among vines". Keep the tigers, which plant the Tiger motif. |
| 23 | "Ibrahim said softly" | soft adverb | "Ibrahim said." |
| 25 | "their posture alert but not nervous" | "X but not Y" correction | Cut. The guard's wave shows the ease. |
| 29 | "The words sent a little shock through me. In most kingdoms I had known, days would pass between a stranger's arrival and an audience with the ruler. Messages would be sent. Names would be checked." | named emotion; stacked passive sentences | "At Pune a stranger could wait a week at the door while his name went from clerk to clerk. Here I had crossed a few hills from a minor compound, and the king was already waiting." |
| 31 | "They took our horses. As I dismounted, the coastal animal tossed its head and snorted. I patted its neck ... My bandaged fingers ached with the remembered absence of Kanka. This horse did not know me." | abstract grief label; repeats line 11; the horse is "he" at 11 and "it" here; the horses are taken before he dismounts | "I dismounted, and a groom took the horses. The coastal horse tossed his head and snorted. I patted his neck without thinking, feeling the warm hide, smelling sweat and salt. My bandaged fingers ached. Kanka would have nudged my shoulder." |
| 35 | "The roof was high enough to let smoke and heat rise, yet low enough that one could still hear the sea beyond when the hall fell quiet." | "high enough... yet low enough" template; faulty logic | "The roof was high and open under the eaves, and when the talk dropped I could hear the sea." (This keeps the plant that pays off at 155.) |
| 37 | "on a slightly raised wooden platform" / "a rolled map on the mat before him" | repeats ch5:125 word for word; a rolled map cannot be read (51, 95) | "on a low wooden platform" / "a map weighted open on the mat before him" |
| 39 | "the simple lines of a Vaishnavite devotee" / "its hilt polished by use, not ornament" | scholar's label; "by X, not Y" correction | "the upright lines of a Vishnu worshipper" / "its hilt worn smooth by his hand" |
| 41 | "His eyes moved constantly, taking in everything, even when the king's attention seemed fixed on the map. Men near us whispered that this was his diwan" | stock phrase; point-of-view slip (Nagoji has no Malayalam, so whispers tell him nothing) | "His eyes kept moving, even when the king's were on the map. Ibrahim had told me on the road who this must be: the diwan Ramayyan, who spoke Persian and Dutch and the trade tongues of this coast." |
| 43 | "And his diwan. Remember what I said about gifts." | the identification is repeated, and the gift reminder is dropped | Cut both sentences, leaving "“Marthanda Varma,” Ibrahim murmured." Optional one-line pay-off at 25: "One recognised Ibrahim and raised a hand in greeting, and something passed from Ibrahim's pocket into his." |
| 45 | "as it always did when I walked alone into a space where everyone else already knew their place" | modern "a space"; "alone" contradicts Ibrahim at his side | "as it did whenever I walked into a room where every other man knew his place." |
| 47 | "I bowed. Not as deeply as a subject would, but enough to acknowledge the man on the platform as something other than a fellow soldier." | verbless correction fragment; repeats the Chapter 5 closing bow ("Not as a subject, not yet") | "I bowed as I would have bowed to Chimaji Appa, and not an inch lower." Join it to the end of the paragraph at 45. |
| 49 | "Your Majesty" | European form of address (register audit P2) | "“Maharaja,” Ibrahim said, his voice smooth." |
| 53 | "in the glare of men who held small forts against impossible odds. There was nothing soft in them, but there was nothing careless either." | cliché; mirrored "nothing X, but nothing Y" kicker | "I had seen such eyes in generals' tents, and once on the *killedar* of a hill fort we sat below for a month and never took." Keep the first sentence (see Defended). |
| 55 | "His gaze did not leave my face." | third gaze beat in five lines (missed by both auditors) | Cut. |
| 79 | "Something like amusement flickered in Marthanda Varma's gaze, gone as quickly as it came." | hedged emotion; cliché | Cut. Keep the second sentence (see Defended). |
| 85 | "The diwan's eyes stayed on me, unblinking." | stock gaze beat | Cut, leaving "I sat. The diwan's hand hovered over his stylus..." |
| 87 | "For the next while, time lost its edges." | abstract time image; modern idiom | "I talked until the shadows of the pillars had crossed two mats." |
| 91 | "that the Portuguese wrapped promises in palm leaves and made them tighter than ropes" / "they had invited a hungry wolf into their courtyards" | metaphor with a simile stacked on it, and the wrong writing material (the Portuguese used paper); stock fable image | "that a raja who put his mark to a Portuguese paper found it held him tighter than a hobble" / "and found they had let a wolf into the fold to keep off the jackals." (A Deccan shepherd's image, and it carries the argument.) |
| 93 | "Only occasionally did his fingers move on the spear shaft, a small adjustment, a tiny tap." | appositive filler | "Now and then his fingers shifted on the spear shaft." |
| 103 | "the king looked up, eyes narrowing" | stock beat | "the king looked up." The action carries the point. |
| 107 | "“You mistrust pilots?” Ramayyan translated, but I had the prickling sense that the Maharaja already understood more than he chose to show." | explained subtext (103 has just shown it); "prickling" echoes 45 | "“You mistrust pilots?” Ramayyan said." |
| 111 | "The corner of his mouth twitched again." | continuity: nothing has twitched before | "The corner of his mouth twitched. “Ram,” he said, without looking at the diwan." (This merges 111 and 113 and keeps the chapter's only twitch.) |
| 115 | "His voice was soft, almost gentle. It did not match the sharpness of his gaze." | explained contrast; repeats 41; blunts "Already marked" | Cut. |
| 117 | "When I had finished, the hall felt oddly still, as if it were waiting for something." | stock personification; "finished" is unclear after the pilot exchange | Cut, and open 119 with: "When I had told him all I knew, Marthanda Varma spoke at length in Malayalam, his tone even." |
| 119 | "I caught none of the words, only the weight." | aphoristic kicker built on a vague noun | "I caught nothing but my own name, and a word close enough to our *firangi* that I knew he meant the Portuguese." (Malayalam *parangi*; partial hearing is the book's best device, per `VOICE_BIBLE.md`.) |
| 121 | "Ramayyan's translation carried the edge." | mirrors "weight" at 119 | "Ramayyan did not soften it." |
| 123 | "The words were not meant as an insult. They were simple fact. Still, they stung." | "Not X. Y." correction; named emotion; kicker | Cut. The reply at 125 shows the sting. |
| 125 | "That does not make my other calculations less true." | modern register ("calculations") | "That does not make the rest of my counting wrong." (This picks up "counted men and ships" at 121.) |
| 127 | "The diwan turned the answer into Malayalam with a few quick phrases. The king listened, eyes unreadable. Then he spoke again, this time more briefly." | stock "eyes unreadable" | "The diwan turned the answer into Malayalam. The king heard it out, then spoke again, more briefly." |
| 133 | "a dry sound that needed no translation" | stock tag; repeats ch5:133 ("needed no translation") | "The king chuckled once, then spoke again in Malayalam, gesturing toward the inlet and the wall behind him." (This merges 133 and 139.) |
| 135 | "Ramayyan murmured something in Malayalam that made Marthanda Varma's mouth twitch." | second twitch | Cut. |
| 141 | "They have Dutch fortifications in their minds, thanks to other Europeans who have chosen to be practical rather than loyal." | modern register; unclear "they" | "He says we already have horse from Madurai... We have our own Nair warriors... We know how the Dutch build, because the English at Anjengo will sell us that as readily as powder." (The glossary already names Anjengo as an arms source.) |
| 143 | "only sharpened by the fact that this time it came from the mouth of a man who could, with a word, have me thrown back to the Portuguese or consigned to some pepper estate as expendable labour" | essay syntax; stakes the reader already feels; "expendable" is a 20th-century word (register audit P2) | "It was the question the man in the compound had asked. This time I had slept on the answer." |
| 145 | "Men moved like ants along the shore, unloading sacks, checking nets, shouting to one another in Malayalam." | the most generic crowd simile; reflex tricolon | "I looked past him, out through the open side of the hall, to the inlet and the strip of sand below the wall." Then move the first two sentences of 151 here (see Flab). |
| 147 | "Above them all the sea lay, flat and deceptive. Somewhere beyond that horizon sat Goa..." | panorama pause; pathetic fallacy; "pepper and souls" gives the Dutch a Portuguese motive | Cut the paragraph. |
| 149 | "I said slowly" / "as they know their own pulse" / "Someone who has watched their neat formations falter not from fear of God, but because a hoof struck at the right moment in the right place." | soft adverb; generic body simile; the last sentence restates "felt it break" with a "right moment, right place" doublet | "I said"; "who know every path of this land in the dark"; cut the "Someone who..." sentence. |
| 151 | "and the weight I now carried" | abstraction attached to a concrete memory | Cut, leaving "I thought of Keshavrao's eyes in the storm." Move the paragraph ahead of the speech. |
| 153 | "“You have men who can build ships and forts,” I said. “I can help you turn speed into a weapon against men who think their guns make them untouchable. I can help you teach your riders..." | the speech restarts and restates 149; pitch register ("turn speed into a weapon", "untouchable") | Fold into the end of 149: "Give me your riders and I will teach them to stand a volley. I will show them where to strike and when to pull away, until men who drilled on flat European fields die confused on this coast." |
| 155 | "The hall remained quiet. Somewhere outside a bird called. The waves hissed on the sand." | cinematic silence beat; third "Somewhere" | "The diwan turned my words into Malayalam. The hall was so quiet I could hear the waves on the sand." |
| 165 | "The king smiled thinly at his minister's summary." | stock micro-expression (Ramayyan is "amused" two lines later) | "The king said something brief in Malayalam, his gaze returning to me." |
| 167 | "For now, you are not a guest. You are not yet a servant either. You are an experiment." | "Not X. Not Y. Z." crescendo; "experiment" reads as laboratory talk | "For now you are not a guest, and not yet a servant. You are a horse on trial." (Plainer alternative: "You are on trial.") |
| 181 | "He does not throw them away lightly, not even when the gods demand it." | softening add-on after the chapter's hardest line | Cut. |
| 185 | "Let us see what a storm can do when given horse instead of chains." | the narrator's storm motif put in the minister's mouth; tagline symmetry | "“Come,” he said. “You will want to see that sand before the tide takes it.”" |
| 187 | "For the first time since Goa, my blood beat in my veins with something other than pain and stubbornness." | named emotion; vague "something other than" | Cut. Keep the first sentence ("As I followed him out of the hall, the roar of the sea grew louder."). |
| 189 | "Storms had tried to kill me. Now I would learn whether I could become one." | reversal aphorism; storm motif (reserved for ch13:321) | Cut. |
| 191 | "Not in threat, but in promise." / "I will harden his riders and break his enemies." / "stone by bloody stone" | correction fragment; triple "I will" vow; stock vengeance cadence | See Ending. Keep the vow in plain form and the hand on the hip. |
| 193 | "For now, Travancore was the forge. But the blade was meant for another war." | summary ending; breaks the style sheet's rule on last paragraphs beginning "For now" or "But" | Cut. |

## Borderline

The author decides these. My leaning is given for each.

- **3** "They did not take me to a palace." This is a negation opener, but it is plain, and the expectation is Nagoji's own: Chapter 5 ends with "Tomorrow we take you to the king's war hall", and a Maratha who has seen Pune expects a palace. Once 9, 21, 25 and 47 are fixed, this is the only negation on the first page. **Keep** (in agreement with `OPENINGS_ENDINGS_MOTIFS.md`).
- **17** "its water dark and still": a default pair in an otherwise concrete paragraph. Harmless. Cut only when tightening.
- **23** "The kingdom itself is the beast." With tigers on the pillars, "This is only one claw" already carries the image, and the second sentence explains it. The endings audit treats the pair as the Tiger plant, so this is the author's choice. My leaning is to cut the second sentence.
- **57** "Ramayyan's Konkani followed a heartbeat later." The phrase is common but harmless, and it sets the pace of the translation device. Keep, or use "Ramayyan put it into Konkani."
- **99** "replacement ships": "relief ships" is the period military word. It is a one-word swap. The sentence itself is defended.
- **137** "For a few breaths the Maharaja studied me in silence." "Breaths" is the register audit's own period measure of time, so that part is fine; "studied me in silence" is stock. Once 135 is cut and 133 is merged, the pause is not needed. Leaning: cut.
- **141** "He asks what you add that he does not already have." "What you bring" sounds less like a job interview. It is minor, and the question has to stay close to ch5:157 either way.
- **157** "tapped the butt of his spear against the mat once, twice": keep the tap, which is the king's best tell. "Twice" does the counting on its own.
- **163** "You could help shape that." "Shape" is mildly modern and managerial. Try "You could teach them that."

## Defended (flagged, but keep)

- **5 and 29, the Deccan-versus-coast comparisons.** The auditors wanted one of the three comparisons cut. Two of them compare different things: the décor at 5 and the speed of an audience at 29. Each shows the Travancore court by its habits (`VOICE_BIBLE.md`, rule 8). Keep both in the trimmed forms above, and cut the vague one at 21.
- **11** "He did not know my hand, and I did not yet know his language." The line is balanced, but it is a horseman's idea (every horse has its own language), and it quietly sets up the chapter's real subject, a man walking into a hall whose language he does not know. Keep it here and cut the repeat at 31.
- **39** "He wore no crown." The endings audit keeps this instance, where the king is introduced, and cuts the copy at ch5:127.
- **39** "in the style I would come to know as a *Konda*". Memoir retrospect is allowed once a chapter (`VOICE_BIBLE.md` 6b), and this is the chapter's only use.
- **45** "The back of my neck prickled". The voice bible cites it as Nagoji's single beat in the body. Only the end of the sentence needs fixing.
- **53** "the kind that measure before they strike". "Measure" is a swordsman's word for judging distance, so the image comes from his trade. It is also cited in the voice bible. Keep it and cut only the two clichés after it.
- **67** "Another question, another soft roll of Malayalam." This is the only fragment left in the chapter, and it copies the clipped rhythm of the exchange around it. It is well inside the style sheet's limit of three.
- **79**, second sentence: "If he understood my answers without his minister's help, he gave no sign beyond the speed with which his eyes moved." *This overrules `REVIEW_BACKLOG.md` C10-13*, which proposed keeping 107 and cutting this sentence. Line 79 is the plant, 103 is the payoff shown in action, and 107 explains the payoff. Keep the plant and the action, and cut the explanation.
- **99** "I thought of wind, of the usual routes, of how many days it had taken". This is not a reflex triple. Those are the three things a scout reckons with before giving an estimate, and the voice bible protects hedged estimates "even when they slow a scene".
- **149** "You have... You have... You have... What you do not yet have is..." The anaphora is not decoration. It answers the king's own list at 141 point by point (Madurai horse, Nair warriors, European know-how) and then names the missing piece. This is one of his two audition speeches, which the voice bible protects. Cut only the restatements (the end of 149 and the start of 153).
- **167** "not a guest, and not yet a servant". This is the one correction construction the style sheet allows per chapter, spent in dialogue on the king's verdict. It is also the first time the book's title word is applied to Nagoji. Merge it into one sentence; only "experiment" goes.
- **173** "The way Ramayyan relayed it made it clear that his king had imagined a great deal." *This overrules the pattern auditor and C10-13.* The line is not about whether the king understands Konkani. It is a dry joke on "imagined" from 171 (the king has already imagined what he will do if Nagoji fails), and it makes the threat smaller in Nagoji's way. Keep it. An optional trim: "His king, I gathered, had imagined a great deal."
- **191**, first sentence: "my hand went to my hip, to the empty place where a sword should hang." This is the best image in the ending, and it becomes the last line.

## Opening

Current lines 3 to 11: a negation hook ("They did not take me to a palace."), a generic paragraph about Deccan halls ending in "the hall where my fate shifted", the blood-tasting wind, "though not as I had once ridden", and a triple of riding sensations.

**Verdict: keep the first line and revise the paragraphs after it.** Both auditors are right that the first page stacks up machine moves. The holistic reader's suggestion to open on the horse is attractive, but not needed. The first line is plain, and it is Nagoji's own expectation. Once its companions are gone, it reads as dry understatement rather than as a pattern. The first page becomes:

> They did not take me to a palace.
>
> In the Deccan, kings and sardars received men in high halls, on carpets, under painted walls. The king of this coast kept his hall within sight of the sea.
>
> We travelled south along a road that clung to the edge of the land. On one side, palm groves and pepper gardens climbed gentle slopes. On the other, low cliffs dropped toward a strip of sand and the grey plane of the ocean beyond. The wind off the sea left salt on my lips.
>
> The bulls were gone. This time I rode.
>
> The horse beneath me was a coastal animal, smaller than the Deccan mares I knew, with a rougher coat and a suspicious eye. He did not know my hand, and I did not yet know his language. Still, a horse was moving under me again, and my back straightened before I had thought to straighten it.

That is 155 words against 196, with no loss of fact. "The bulls were gone" still links back to the Chapter 5 cart.

## Ending

Current last lines (183 to 193):

> The diwan stood, gathering his palm leaves.
>
> “Come,” he said. “Let us see what a storm can do when given horse instead of chains.”
>
> As I followed him out of the hall, the roar of the sea grew louder. For the first time since Goa, my blood beat in my veins with something other than pain and stubbornness.
>
> Storms had tried to kill me. Now I would learn whether I could become one.
>
> As I walked, my hand went to my hip, to the empty place where a sword should hang. Not in threat, but in promise. *I will serve this king,* I told myself. *I will harden his riders and break his enemies. When that debt is paid, I will turn north again, find Chimaji, and burn the Portuguese out of Goa, stone by bloody stone.*
>
> For now, Travancore was the forge. But the blade was meant for another war.

**Verdict: rewrite, almost entirely by cutting.** There are five closing beats, and each one explains what the reader already knows. The storm line comes out of Ramayyan's mouth, the storm motif is spent twice more (it is reserved for ch13:321), and the last paragraph opens with "For now" and turns on "But", both banned by the style sheet. Chapter 5 already ends with a stacked cascade ("Horses. Guns. Storms."), so a reader will hear the same close twice in a row.

Proposed:

> The diwan stood, gathering his palm leaves.
>
> “Come,” he said. “You will want to see that sand before the tide takes it.”
>
> As I followed him out of the hall, the roar of the sea grew louder. *I will serve this king,* I told myself. *When that debt is paid, I will go north again, find Chimaji, and burn the Portuguese out of Goa.*
>
> My hand went to my hip, to the empty place where a sword should hang.

Why this ending:
- The chapter ends on an image. When the gesture follows the vow, it says "promise" without the words "Not in threat, but in promise".
- The vow stays, in plain words. Later chapters depend on it (see `REVIEW_BACKLOG.md` C12-05 and the sparing of Duarte at ch24:351). Chimaji also gets his plant, and line 47 now names him too.
- Ramayyan talks in his own practical register, not in the narrator's motif. His line hands off directly to Chapter 7, which opens on that strip of sand and its tides ("At high tide the waves gnawed at it").
- It adds no new plot facts.

Alternative, if the author wants the chapter to end on dialogue: the endings audit proposed ending with Ramayyan saying "You will have a sword by morning." That line adds a small fact (a sword is issued), and later chapters would then need to agree with it.

## Flab

- **Lines 3 to 33, the approach (580 words, down to about 455).** It takes thirty lines to reach the hall. The time goes on three north-versus-here comparisons (5, 21, 29), throat-clearing about Ibrahim's clothes (13), the blood simile (7), and a grief label for Kanka (31). The fixes above keep every fact and every good beat: the horse, the clinking coat, the inlet boats, the tigers, the guard's wave, Kanka's nudge.
- **Lines 35 to 47, the hall entry, which repeats Chapter 5's compound hall.** Compare ch5:125 to 127 ("wooden pillars carved with curling designs", "Men sat cross-legged around a central space", "on a slightly raised platform", "He wore no crown") and the ch5 closing bow. The fixes at 21, 37 and 47 make this hall read differently. The better fix is in Chapter 5, the lesser hall: cut "He wore no crown" at ch5:127 and the carving detail at ch5:125. Ramayyan is also introduced twice (41, 43). The fix at 41 and 43 introduces him once.
- **Lines 51 to 55, three gaze beats in a row** (eyes leave the map, the eyes paragraph, "His gaze did not leave my face"). Keep the first two and cut the third.
- **Lines 103 to 137, the explanation layer and the reaction stall.** About twenty lines of reaction sit between two real exchanges: 107, 115, 117, 123, 127, 133, 135 and 137. After the fixes, the stretch keeps its best beats ("Ram" / "Already marked, Maharaja", the charge about the dungeons, "trust is for priests") and loses about 50 words.
- **The king's tells, a budget for lines 51 to 169.** Keep: eyes leave the map (51), the eyes paragraph (53), the hand flick (73), the speed of his eyes (79), fingers on the spear shaft (93), the tap on the map (95), looking up before the translation (103), one mouth twitch (111), "Ram" (113, 159), one chuckle (133), the spear butt (157), the glance at the open hall (169). Cut: the flicker (79), narrowing (103), "again" (111), unreadable (127), the second twitch (135), silent study (137), the thin smile (165). Ramayyan keeps his moving eyes (41), the stylus (85, 93) and "amused" (167). Cut "unblinking" (85) and the soft voice (115).
- **Lines 139 to 155, the pitch: the one structural fix inside the scene (440 words, down to about 260).** The problems: the question repeats ch5:157 and line 143 says so in essay syntax; a panorama (145 to 147) delays the answer by two paragraphs; the speech starts over at 153 and says it all again; and the best thing in the passage, the Chaul memory at 151, is hidden in the middle. The fix is to reorder and cut, with no new material. Nagoji looks out at the sand, the sand brings back Chaul, and the memory becomes the speech. The king then hands him that same sand at 171. Worked text:

> It was the question the man in the compound had asked. This time I had slept on the answer.
>
> I looked past him, out through the open side of the hall, to the inlet and the strip of sand below the wall. I thought of Kanka then, of wet sand beneath his hooves near Chaul, of Portuguese musketeers flinching when our horses came at an angle they had not drilled for. I thought of Keshavrao's eyes in the storm.
>
> “You have horse from Madurai,” I said. “You have Nair warriors who know every path of this land in the dark. You have guns and forts and men from across the sea who teach you how Europeans think. What you do not yet have is someone who has ridden into a European line and felt it break. Give me your riders and I will teach them to stand a volley. I will show them where to strike and when to pull away, until men who drilled on flat European fields die confused on this coast.”
>
> The diwan turned my words into Malayalam. The hall was so quiet I could hear the waves on the sand.

  To keep the dig at Portuguese piety from 149 ("not from fear of God"), it would have to go into the speech as "and seen it break, and not from fear of God". That would spend the chapter's one correction construction, which this report assigns to 167.
- **Lines 179 to 193, the ending.** See Ending: about 70 words cut.

## Passages to protect

These must survive the edit word for word, or as close as the fixes allow.

- **31** "Kanka would have nudged my shoulder." (voice bible touchstone T4)
- **57 to 77**, the clipped exchange: "I did." / "I did." / "They tried." And "came the diwan's version" (69), which quietly shows Ramayyan turning questions into statements.
- **83**, Ramayyan's brief ("Tell him how their forts stand, how their captains think, how quickly they can bring ships..."). It sets up the order of 89, 91 and 97.
- **89**, the bastions "built thick and low so cannonballs skipped off instead of biting deep", and the half-sick garrisons at the lonely outposts.
- **91** "talking of one God while the men behind them counted how many guns a king could spare"
- **93** "The diwan wrote nothing at first. Then, as I began to speak of cavalry... his hand moved, scratching quick notes."
- **99 to 101**, the burned warehouse and "three days. Four if they are unlucky. Longer if someone whispers wrong directions into the ear of a pilot."
- **109** "I mistrust everyone who touches a coin... men who steer ships can be made to see profit in many directions."
- **113 to 115** "Ram," / "Already marked, Maharaja," with nothing after it.
- **121**, the king's charge about the dungeons, and **125** "I misjudged a patrol near the coast. I paid the price."
- **129 to 131** "He says, perhaps," and Ibrahim's "Beyond that, trust is for priests."
- **151** "wet sand beneath his hooves near Chaul... an angle they had not drilled for"
- **149 and 153** "felt it break" and "die confused on this coast"
- **163**, Ramayyan's diagnosis: "They do not know the feint and vanish the way Deccan riders do."
- **167** "He says I always see the two faces of the coin"
- **171**, the strip of land "too wet for most cavalry work, too narrow for big batteries" and "show him something there he has not already imagined". Chapter 7 quotes this at ch7:21, so keep the wording.
- **181** "He has spent too many lives to sit on that mat."
- **191** "the empty place where a sword should hang"

## Chapter-specific notes

Continuity and history points noticed during the audit. They are not slop, but they are cheap to fix in the same pass.

1. **Diwan or Dalawa.** "Diwan" appears 13 times in this chapter. `REGISTER_AND_ANACHRONISM.md` rates it P1 (Travancore's minister was the Dalawa in 1738) and `REVIEW_BACKLOG.md` N-42 and FM-14 ask for a house decision. If the author chooses Dalawa, this chapter is where Nagoji should learn the word. The new line 41 can carry it: "the Dalawa Ramayyan (a diwan, we would say)". After that, use Dalawa.
2. **"Your Majesty" (49)** appears nowhere else in the book. Use "Maharaja", as the rest of this chapter does.
3. **The Nayak of Madurai (141).** Nayak rule in Madurai ended in 1736. The fix at 141 already drops "the Nayak". Chapter 7:13 ("The Nayak of Madurai sends his horse") needs the matching change (`REVIEW_BACKLOG.md` N-26).
4. **Kanka.** Lines 31 and 151 ("his hooves") agree with Chapter 1: a male horse, shot at the capture. "The Deccan mares I knew" (11) is fine, since a huzurat rider knew many horses. The conflict is in ch7:145 and the prequel (BL-01), not here. The coastal horse at 31 must be "he", as at 11.
5. **Cross-chapter echoes with Chapter 5.** These are "needed no translation" (ch5:133, ch6:133), the hall description (ch5:125 to 127), "He wore no crown" (ch5:127), the half-bow (end of Ch 5, ch6:47), and the repeated question (ch5:157, ch6:141). The fixes here remove the first and fourth. For the others, trim Chapter 5 and let this chapter keep them. For the question, shorten Nagoji's answer at ch5:161 (C10-12) so the full answer belongs to this chapter.
6. **Line 29 and Chapter 5.** The holistic reader called the "shock" a contradiction of "Tomorrow we take you to the king's war hall". Strictly it is not one: being taken to a hall is not the same as being seen by the king the same day. The fix keeps the real point, the speed of this court, and drops the shock.
7. **The inland rampart (21).** Make sure it cannot be read as the Travancore Lines (Nedumkotta), which were built in the north from the 1760s. "A short earth wall" or "a stockade" would be safer for 1738.
8. **Palm-leaf promises (91)** have been moved to Portuguese paper. **"Pepper and souls" (147)** goes with the panorama. If the author keeps any of that paragraph, give the Dutch a motive of contract and ledger rather than one about souls.
9. **"Other Europeans" (141)** now means the English at Anjengo, as the glossary and character guide already say. This also stops the line from seeming to point ahead to de Lannoy, who is only captured at Colachel in 1741.
10. **Maravar riders (163, 171; also Ch 7).** Maravar troops in Travancore service were mostly foot soldiers. The book treats them as cavalry consistently, so this is only a flag for the author to check.
11. **The storm motif.** After the fixes, the only storm in this chapter is literal: "storm water" (49) and "Keshavrao's eyes in the storm" (151), both about the wreck. That leaves the figurative storm free for ch13:321, as `OPENINGS_ENDINGS_MOTIFS.md` proposes.
12. **New terms introduced by the fixes.** *Killedar* (53) and *firangi* (119) are Marathi words Nagoji would use without a gloss, in keeping with voice bible rule 9. Italicise them on first use. *Konda* (39) and diwan or Dalawa still need glossary entries (FM-10).
13. **Chapter 7 hand-off.** Chapter 7 opens on the beach strip and quotes the king's challenge (ch7:21). With the proposed ending, Ramayyan's "see that sand before the tide takes it" leads straight into it.
