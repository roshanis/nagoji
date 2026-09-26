# Second-Edition Audit: Chapter 5, Road to Travancore

- Source (frozen first edition): `book1_horse_servant/book1_chapter05_road_to_travancore.md`, 177 lines, 2,007 words by `wc` (2,001 in SOURCE_OF_TRUTH's count).
- Line numbers are physical lines in that file, blank lines included. `manuscript/` does not yet hold a copy of this chapter. A fresh copy will match these numbers until its first edit, so apply the fixes from the bottom up.
- Method: I read the chapter in full and ruled on every flag from the pattern auditor (56 flags) and the holistic reader (25 passages, 11 flab notes), merging duplicates. I also checked the end of Ch 4, Chs 6 and 7, and the book-level audits (`OPENINGS_ENDINGS_MOTIFS.md`, `REGISTER_AND_ANACHRONISM.md`, `VOICE_BIBLE.md`, `REVIEW_BACKLOG.md`), and ran `audit/tools/scan_slop.py` on the chapter. To test the cut estimate, I applied every confirmed fix to a scratch copy and rescanned it (not saved in the repo).
- Source tags in the tables: **P** = pattern auditor, **H** = holistic reader, **N** = new in this pass.

## Verdict

| Measure | Call |
|:-|:-|
| Severity | **3 of 5** |
| Recommended intensity | **Medium** (tics plus tightening), with a rewrite of the last nine lines |
| Estimated word cut | **About 15%** (2,007 to about 1,700 words). The scratch pass with every confirmed fix plus the "take" borderlines came to 1,668 words (17%). |
| Scanner, before and after the scratch pass | not-X-but-Y 3 to 0; "Not" openers 2 to 0; "as if" 1 to 0; soft adverbs 2 to 0; "something else" 1 to 0; fragment triad 1 to 0; short paragraph-final kickers 3 to 1; "like a" 2 to 2 (both from his world) |

The chapter has a sound skeleton: a trader collects a castaway, carts him inland and hands him to a king's man, who questions him and passes him up the line. Its best writing is its plainest. The yes/yes interrogation (13 to 19), the guarded "Some." (153), Ibrahim's inventory of teeth and eyes (69), the contemptuous bulls (75) and the cavalryman reading the wheel ruts (109) all sound like one man. The slop gathers in three places:

1. **The close (169 to 177) reads as machine-written.** The chapter ends five times: a bow explained by a present-tense maxim, a double "Somewhere" cutaway that leaves first person, a title-echo summary, "Horses. Guns. Storms." and a dream coda. Cut to one concrete beat.
2. **Ibrahim's introduction (5 to 25).** A "Not with a bow" correction opens the chapter's second paragraph, an office idiom decodes a gesture, and the stock "Something flickered behind his eyes... Then it was gone" follows.
3. **The hall (125 to 169).** It uses "He wore no crown", which belongs to the king in Ch 6. Around it are "needed no translation", "There it was.", "Silence settled" and "smiled, very slightly", plus modern race vocabulary in Nagoji's key speech.

Three habits run through the whole chapter:

- **Epigram sameness.** The healer, Ibrahim, the guard and the official all trade the same polished quip, and most exchanges end on one (41, 59, 69, 87, 101, 107, 115, 121, 135, 167). The rule here is to keep Ibrahim's best lines and flatten the rest, not to remove wit.
- **Dusk is announced four times** (53, 75, 109, 171).
- **Stock gesture beats**: twitched lips, two shrugs, a raised eyebrow, flicked eyes and a slight smile.

This is not a deep rewrite. About a third of the confirmed fixes are straight cuts, and most of the rest are no longer than the lines they replace.

## Confirmed issues

34 rows. Several merge flags from both auditors. The order follows the text.

| Line | Quote | Category | Suggested fix |
|:-|:-|:-|:-|
| 3, 5 | "The man they called *kapitan* introduced himself as Ibrahim. / Not with a bow or a flourish, only with a nod and a measuring look that told me he had decided what kind of man I was before he opened his mouth." | correction opener; explained subtext; repeats Ch 4's closing "weighed" beat and its last phrase (P, H) | Line 3: "The *kapitan* gave his name as Ibrahim." Cut line 5. |
| 11 | "He glanced at my branded arm, at the bandaged hands, at the rope burns." | repetition: Ch 4's last paragraph has already listed "the brand, the bandaged hands"; reflexive triad (P, N) | "He looked at the brand on my arm." |
| 21 | "a habit, I would learn, that meant he was filing information away." | modern register (office filing, "information"); it decodes a gesture the book never uses again (P, H) | "He nodded, and his thumb went to the scar on his jaw." |
| 23 | "“Our king fights them too,” he said. “And their cousins, the Dutch.”" | history: Travancore was not at war with the Portuguese in 1738. The line also repeats the Ch 4 fisherman almost word for word ("Our king to the south fights them too... the Dutch", ch4:63) (H, N) | "“Our king has no love for them either,” he said. “Nor for their cousins, the Dutch. He will want to hear what you have seen.”" |
| 25 | "He paused, his thumb tracing the scar again. Something flickered behind his eyes, a calculation, a road not taken. Then it was gone." | stock beat; Frost echo; "Then it was gone" kicker; the same gesture four lines later (P, H) | Cut the paragraph. The hint of Ibrahim's double dealing (REVIEW_BACKLOG F13-02, paid at ch11:401) moves to line 69, which must stay. |
| 31 | "Ibrahim's lips twitched." | stock gesture (13 twitching mouths in the book; a twitching nose follows at 55) (P, H) | Cut. His evasive answer carries the amusement. |
| 39, 41 | "Men like you never do." / "“Men like me are paid to be impatient,” he said mildly." | stock tag; mirrored setup and punchline; adverb tag (P, H) | 39: end at "but you will not wait.” 41: "“I am not paid to wait,” he said. To me he added..." |
| 43 | "At the word horse an ache went through me that had nothing to do with broken skin." | banned formula (STYLE_SHEET 1); names the feeling (P, H) | "At the word horse my knees tightened on the mat, the way they tighten on a saddle." Do not name Kanka here: ch6:31 spends that memory. |
| 49 | "wrapped in clean strips of linen" | material: linen is unlikely in a Mukkuvar fishing village (H) | "wrapped in clean strips of old cotton" |
| 51 | "Women drew water from a well. Children chased each other with shrieks of laughter. Men patched nets in the shade of leaning palms. Only the occasional glance at the path toward the sea betrayed the fact that a Portuguese ship had broken nearby." | postcard tricolon; "betrayed the fact that" (P, H) | "Outside, the men were back at their nets. Now and then one of them looked down the path toward the sea." |
| 53 | "Ibrahim led me not to the shore, but inland... reflected the darkening sky in strips... and something else, sharp and almost floral." | not-X-but-Y in narration; "something else" (kill list); the first of four dusk resets (P, H) | "Ibrahim led me inland, along a narrow track that wound between paddy fields. The water in the flooded plots held the sky in strips. Frogs chirped. The breeze smelled of wet earth, with a sharpness under it that caught at the back of my nose." |
| 57 | "On the Deccan we had fought for the routes that carried this smell north. Now I was at the source." | kicker; shaky history: Malabar pepper went north by sea, not along routes the Marathas fought over (P, H) | "I breathed it in. In our camps pepper came by the handful, and the cooks guarded it like powder." This keeps his contrast and hands straight to "And for kings". |
| 63 | "Our people are the vines that run along this coast. We carry news as well as goods. When we bring you to the king's men, they will already know more about you than you think." | ornamental metaphor (REVIEW_BACKLOG C10-10); stock menace (P, H) | "“We send word ahead,” Ibrahim said. “My people trade the length of this coast, and news travels with the pepper. The king's men will know of you before you reach them.”" |
| 67 | "He shrugged, but the gesture was a little too careful." | "a little too X"; reads the body language for us (P, H) | Cut. The sideways glance and "to whom" in 69 do the work. This also saves Ibrahim's one shrug for 105. |
| 71 | "biting back a groan as my bruised ribs protested." | two stock phrases (P, H) | "I took it and hauled myself onto the sacks, and lay there until my ribs let me breathe." |
| 75 | "Above us the sky shifted from bruised grey to the deep blue of evening. Fireflies sparked in the wet fields. Somewhere a temple bell rang, a soft, clear sound that seemed to hang in the thick air." | "hang in the air" (kill list); "bruised" twice in five lines; sensory checklist (P, H) | "When the light went, fireflies came out over the paddy, and a temple bell rang in a village I could not see." Make this the chapter's one nightfall. |
| 79 to 87 | "ride back before your masters answer." / "“Your masters,” he repeated. “Not you.”" / "“I serve, as all men serve,”... a fort built to defend a people and a fort built to protect a treasury." / "He considered that." | muddled referent (whose masters?); generic aphorism; slogan antithesis; filler beat (P, H) | 79 ends: "...and ride back before the port lords can answer.” 81: "“And you?”" 83: "“I go where I am sent,” I said. “But I have seen enough forts to know which are built to keep an enemy out and which to keep a treasury in.”" Cut 85. 87: "“Ours do both,” he said. “You will see.”" |
| 95 | "In their place rose other trees, taller and denser, their leaves a darker green. The air grew heavier, as if the forest held the day's heat in its branches." | unnamed trees; "as if" filler; the second heavy air (P, H) | "As the road climbed, the coconut palms thinned. Jackfruit and areca closed over the road, as they do in the Konkan, and the heat sat under them without a breath of wind." |
| 105 | "When I raised an eyebrow, he shrugged." | stock gesture pair (P, H) | "When I looked at him, he shrugged." Keep the woman's line (see Defended). |
| 107 | "Storms and horses can both be useful, if you know how to ride them." | motif stitching; it explains the woman's line straight away (REVIEW_BACKLOG C10-11; STYLE_SHEET 3) (P, H) | Cut this sentence. Keep "I told her you carry horses there too.” |
| 109 | "As evening deepened, we reached a larger settlement. It was not quite a town, not yet, but bigger than the fishing village... and trinkets." | hedged correction; "not yet" tic (3 in the chapter); third dusk; list ending on a filler noun (P, H) | "By the time the lamps were lit we had reached a place larger than the fishing village. Houses stood closer together. A small bazaar clustered around a crossroads, stalls offering spices, cloth, oil, and betel. The road here was better packed, the wheel ruts deeper." |
| 115 | "The sea does not consult my schedule" | anachronism (REGISTER P1) (P, H) | "“Tell the sea,” Ibrahim said." (Or REGISTER's "The sea does not keep my hours.") |
| 125 | "its wooden pillars carved with curling designs. Lamps hung from chains, casting soft light on the packed earth floor... At the far end, on a slightly raised platform, another man sat" | generic set dressing; near-verbatim duplicate of the king's hall at ch6:19 ("carved with curling motifs") and ch6:37 ("At the far end, on a slightly raised wooden platform, a man sat") (P, H, N) | "Inside the compound stood a low hall on plain wooden pillars. Brass lamps hung on chains over a floor of beaten earth. Men sat cross-legged around a mat laid in the middle. By the far wall, on a low dais, another man sat with a stack of palm leaf records and a writing stylus." Keep this hall plain so that Ch 6's carved vines and tigers read as a step up. |
| 127 | "He wore no crown, only a simple dhoti and a shawl over one shoulder. Yet the way others watched him made it clear he was the one who mattered here." | "no X, only Y"; explained subtext; "He wore no crown" is Marthanda Varma's introduction at ch6:39 (P, H, N) | "He wore a plain dhoti and a shawl over one shoulder, and the men on the mats talked with one eye on him." |
| 133 | "Ibrahim translated, but the dry amusement in the official's tone needed no translation." | worn quip; the same device returns at 167 (P, H) | "“You bring me shipwreck,” he said in Malayalam, and Ibrahim gave it to me in Konkani." Use the device once, at 167. |
| 145 | "*huzurat* cavalry," | typography: lower case at the start of a sentence (P, H) | "*Huzurat* cavalry," |
| 159 | "There it was. The question that would decide whether I was given a place in this new game or quietly dropped into some ditch." | reveal tic; states stakes already clear; "game" is modern thriller register (P, H) | Cut. The question stands on its own, and ch6:143 recalls it. |
| 161 | "which chiefs will bend and which must be broken... believe God and powder have made them superior... stopped being impressed by white skin." | modern race and status framing; stock bend or break (P, H) | Change three phrases and keep the speech: "...which chiefs have eaten his salt and which only pretend to." / "...believe God and powder have made them masters of it." / "...when the man in the saddle has stopped being afraid of them." |
| 163, 165 | "Silence settled over the hall for a moment." / "Then the man on the platform smiled, very slightly." | stock pause; stock smile with a filler qualifier (P, H) | Cut both. At 167, "the translation arriving a moment after the amusement in his eyes" already gives the pause and the smile. |
| 169 | "I bowed my head. Not as a subject, not yet, but as a man who understands that some battles begin with a lowered gaze and a measured tone." | not-X-but-Y; maxim; slip into present tense; "measured" echoes 5's "measuring" (P, H) | "I bowed my head, no lower than I had to." |
| 171 | "The air was thick and warm. Somewhere in the darkness pepper vines climbed up their supports, indifferent to the schemes of men. Somewhere to the south a king I had not yet met considered maps covered in salt stains and ink." | "the air was thick" (kill list); cosmic-indifference cliche; leaves first person; double "Somewhere" (P, H) | Cut. Ch6:37 shows the king with his map, so nothing is lost. |
| 173 | "The road that had begun in a Goan dungeon now pointed toward him." | summary that echoes the title (P, H) | Cut. |
| 175 | "Horses. Guns. Storms." | fragment triad, the style sheet's named example (P, H) | Cut. |
| 177 | "Sleep came slowly that night, but when it did, it carried no dreams of drowning. Only the steady beat of hooves on sand, and a distant roar like the sea." | mood coda; "no X. Only Y."; a weak simile that brings the sea back again (P, H) | Replace with the close under **Ending**. |

## Borderline

The author's call. Rows marked "take" are counted in the scratch pass.

| Line | Quote | Issue | Option |
|:-|:-|:-|:-|
| 7 | "in Konkani, the trade tongue one of the fishermen had used to speak with me." | Repeats the setup at ch4:57 ("a broken Konkani that bore the marks of trade"). | Take: "in Konkani, the tongue one of the fishermen had used with me." |
| 27 | "The fishermen had spoken the name Travancore, but I wanted to hear it from this man's mouth." | Explains his motive. It is also a **continuity error**: at ch4:67 Nagoji says "Travancore" himself and the fisherman answers "You know the name." (N) | Take: "I had said Travancore to the fishermen, and they had not denied it. I wanted to hear it from him." Keep the first two sentences of the paragraph (see Defended). |
| 33 | "whose boats pull the pepper your people crave" | The middle item of the triple "whose" is muddled: Travancore's boats do not carry pepper for the Marathas. ("Crave" is old enough; the problem is sense, not date.) | Take: "the man whose land you lie on, and whose patience with Europeans is thin." One flourish is enough for Ibrahim. |
| 101 | "With me you are still an uninvited guest,” he said, “but one whose arrival has been announced." | The fourth "word sent ahead" (63, 69, 101, 115) and one more epigram, but short and in character. | Leave, or: "“With me,” he said, “you are expected.”" |
| 121 | "“He disagrees,” Ibrahim said. “Our king might too.”" | "He disagrees" is dry and good. The second half is ambiguous (might the king think he should be dead, or not?). | Leave, or end at "“He disagrees,” Ibrahim said." |
| 139 and 157 | "Ibrahim translated the harsh Malayalam syllable for me." / "waiting for Ibrahim to echo the words in Konkani" | Translation is narrated at 89, 105, 133, 139, 157, 161 and 167. Each one is harmless, but together they stall the hall scene. | Keep one of the two. I would keep 157, which shows the official's patience, and trim 139 to "“Name,” he said." |
| 147 | "His eyes flicked to my bandaged hands, the brand under my sleeve." | "Flicked" is a stock verb. This is not a continuity error (see Defended). | Take: "His eyes went to my bandaged hands, then to the sleeve over the brand." |
| 157 | "Our king sharpens his sword for the Dutch now... ships that slip between the foreign hulls at night." | A third statement in two chapters that the king is readying for the Dutch (ch4:63 "He sharpens his teeth for them", then 23 here). The romantic third item overstates Travancore's boats in 1738. | Take: "“Our king will have the Dutch to fight before long,” he said... “He has horse from Madurai and musketeers of his own. What does a Maratha rider know that he does not already have?”" |

## Defended (flagged, keep)

| Line | Quote | Flag | Why it stays |
|:-|:-|:-|:-|
| 9 | "herbs that burned my throat but soothed my chest" | balanced antithesis (P); recovery recap (H) | Concrete. This is how a man describes bitter medicine, and it marks the day that has passed. VOICE_BIBLE lists "rice gruel" here as his coast vocabulary. |
| 21 | the "I would learn" device | signposting (P) | Looking back from the 1740s is legitimate in a memoir. The line is cut because of what it decodes (a tic never used again), not because of the device. |
| 23 | "their cousins, the Dutch" | odd (H) | VOICE_BIBLE gives Ibrahim a "sea, trade, cousins" register. As a trader's joke that all Europeans are one family, it works even though the Dutch threw the Portuguese out of Kochi in 1663. Only "fights them too" changes. |
| 27 | "He did not say which king. On this coast there were many rulers, small and large, each jealous of their titles." | flab (H) | Accurate for 1738 Kerala, and it explains why he asks. Only the third sentence changes (Borderline). |
| 53 | "Frogs chirped." | filler sound (H) | Two words, and concrete. Keep them to break up the landscape paragraph. |
| 55 | "It sits in the lungs. It pays for guns." | part of the epigram pile (P) | Short, mercantile and specific. One of Ibrahim's best. |
| 59 | "“And for kings,” Ibrahim added. “That too.”" | kicker (P) | It sounds spoken, as an afterthought. Once the kicker at 57 goes, it follows the pepper line directly. |
| 69 | "A man like that has value. The question is always to whom." | aphorism closer (P) | With 25 cut, this is the chapter's only seed of Ibrahim's two-sided dealing (REVIEW_BACKLOG F13-02, paid at ch11:401). It has to stay. |
| 83 to 87 | the forts exchange | balanced antithesis; filler (P, H) | Its job survives: "You will see" is paid at ch6:19 to 23 ("This is only one claw"). Only the wording changes (Confirmed 79 to 87). |
| 105 | "That one carries storms in his bones" | stock prophetic old woman (P, H) | OPENINGS_ENDINGS_MOTIFS makes this the book's single figurative storm plant, paid at ch13:321 ("The storm was here."). Once the explanation at 107 goes, she gets seven plain words and no gloss. Also keep the shrug here, Ibrahim's one shrug in this chapter. |
| 107 | "I told her you carry horses there too." | part of the motif stitch (P, H) | A dry, trader's answer that keeps the title motif in view. Only the second sentence goes. |
| 147 | "the brand under my sleeve" | continuity error, since 49 hides the brand (P, H) | Not an error. Word went ahead ("a branded Maratha officer", 69), so the official's eyes go to where he knows the brand is. That shows the message arrived. Keep the idea and change only "flicked" (Borderline). |
| 157 | "What does a Maratha rider know that he does not already have?" | part of the flagged triad (P); REVIEW_BACKLOG C10-12 wants the exchange shortened | The question must stay: ch6:143 refers back to it ("the same question that had been asked in the coastal compound"). Shorten the list before it, not the question. |
| 161 | "Your king knows... The Dutch and the Portuguese know... I know... I know" | rehearsed anaphora (P, H) | VOICE_BIBLE calls this one of his two audition speeches, the only times he orates. He has had a day in a bullock cart to rehearse it. Keep the build and fix only the modern vocabulary. The horse against musket line claim is plot-critical, and ch6:149 develops it ("felt it break"), so this does not duplicate it. |
| 167 | "the translation arriving a moment after the amusement in his eyes" | recycled device (P) | The better of the two versions, placed where the delay matters. Kept once, after 133's version is cut. |

## Opening

**Current (3 to 11):** "The man they called *kapitan* introduced himself as Ibrahim. / Not with a bow or a flourish, only with a nod and a measuring look that told me he had decided what kind of man I was before he opened his mouth." Then the Konkani explanation, the recovery recap, and "He glanced at my branded arm, at the bandaged hands, at the rope burns."

**Verdict: revise.** The first thing a reader meets is the book's commonest opening template: a statement, then a "Not with..." correction in the next line. It also sits on a seam: Ch 4 closes on "the man they called *kapitan*", on his eyes weighing the brand and bandaged hands, and on "I was being weighed". Ch 5 then repeats the phrase, the weighing and the inventory. OPENINGS_ENDINGS_MOTIFS proposes keeping "a look that told me he had already decided what kind of man I was". I would drop that clause as well: it explains what the yes/yes exchange at 13 to 19 shows better.

**Proposed:**

> The *kapitan* gave his name as Ibrahim.
>
> “You were on the Portuguese ship,” he said in Konkani, the tongue one of the fishermen had used with me. “The storm did not like her.”
>
> “The storm did not like any of us,” I said. My voice had grown stronger after a day of rest, rice gruel and herbs that burned my throat but soothed my chest. “I took the chance it gave.”
>
> He looked at the brand on my arm.
>
> “You are Maratha.”

Leave lines 13 to 19 exactly as they are.

## Ending

**Current last lines (169 to 177):**

> I bowed my head. Not as a subject, not yet, but as a man who understands that some battles begin with a lowered gaze and a measured tone.
>
> Outside, night had fallen. The air was thick and warm. Somewhere in the darkness pepper vines climbed up their supports, indifferent to the schemes of men. Somewhere to the south a king I had not yet met considered maps covered in salt stains and ink.
>
> The road that had begun in a Goan dungeon now pointed toward him.
>
> Horses. Guns. Storms.
>
> Sleep came slowly that night, but when it did, it carried no dreams of drowning. Only the steady beat of hooves on sand, and a distant roar like the sea.

**Verdict: rewrite.** After the official's good line ("He can decide whether your words are as sharp as you think"), the chapter closes five times. None of the five paragraphs is concrete except the hooves, and those are a dream.

**Proposed close (replaces 169 to 177):**

> I bowed my head, no lower than I had to.
>
> They gave me a mat in a storeroom behind the hall, among the pepper sacks. Some time in the night a horse stamped and blew beyond the wall. I lay awake a long time, waiting for it to stamp again.

Why this close:

- It ends on an action and a sound he really hears, not a dream.
- It shows the longing that line 43 used to label, without naming Kanka (ch6:31 spends that memory).
- It sets up Ch 6's "The bulls were gone. This time I rode": the compound keeps horses, and he has heard one.
- It keeps the smell of pepper that runs through the chapter.
- It leaves "storm" alone, as the ch13:321 payoff needs.

The bow keeps his pride without a maxim.

OPENINGS_ENDINGS_MOTIFS offers another version: a dream of "a horse under me whose colour I could not see", planting Kayal. It is acceptable, but it is still a dream coda. If the author prefers it, check it against the proposed Ch 7 close (Kayal's nose in his palm) so the two horse endings do not rhyme. Either way, record the choice in the ending plan (OPENINGS_ENDINGS_MOTIFS 3.4).

## Flab (passages to tighten)

| Lines | Issue | Action |
|:-|:-|:-|
| 3 to 11 | The seam echo with Ch 4, the Konkani re-explained, and the brand and hands inventory repeated from Ch 4's last paragraph. | As under Opening. |
| 21 to 27 | The scar tic twice, a gloss on it, a stock "flicker", and a motive stated for a question he asks at once. | Keep one scar gesture with no gloss. Cut 25. Trim 27. |
| 51 to 53 | A village establishing shot for a scene they are leaving, then the first dusk. | One sentence of village (Confirmed 51); no dusk at 53. |
| 53, 75, 109, 171 | Dusk is announced four times, which squeezes "a long road" behind slow bulls into one evening and resets the mood at every stop. | One nightfall, at 75 ("When the light went"). Mark time at 109 with lamps. Cut 171. |
| 63, 69, 101, 115 | "Word sent ahead" is said four times. | Keep 63 (trimmed), 69 and 115. 101 is optional (Borderline). |
| 77 to 87 | The "your masters" exchange muddles who is needling whom, and the fort slogan covers it over. | Confirmed 79 to 87. |
| 105 to 107 | The woman's line is explained in the next breath. | Cut the second sentence of 107. |
| 111 to 131 | The compound hall copies the king's hall in Ch 6, and "no crown" copies the king. | Confirmed 125, 127. Leave "red stone blocks" at 111 here (first sight) and vary ch6:19 in its own pass. |
| 133 to 167 | Translation is narrated six or seven times, and the "tone before translation" device appears twice. | Keep 89 (sets up the interpreter), 157 and 167. Trim 133 and 139. |
| 159 to 177 | Stacked reaction beats and endings: stakes explained, silence, slight smile, explained bow, cutaway, summary, triad, dream. | Confirmed rows 159 to 177 and Ending. |
| Whole chapter | Nearly every exchange ends on a quip (41, 59, 69, 87, 101, 107, 115, 121, 135, 167). | Keep 55, 59, 69, 93, 97, 135 and 167, which are the best of them. Flatten 41, 83, 107 and 115. 101 and 121 are optional. Let one or two exchanges simply stop. |

## Passages to protect

- **13 to 19**, "You are Maratha." / "Yes." / "You fought them." / "Yes." The best rhythm in the chapter. Do not touch it.
- **7 to 9**, "The storm did not like her." / "The storm did not like any of us." This is his shrinking verb (VOICE_BIBLE). "The storm" here names the wreck and is not a figure, so the storm rationing does not apply.
- **39**, "She snorted. “He should rest another week, but you will not wait.”"
- **45 to 47**, "I can sit... I can walk, if there is no better way." / "There is a better way, though you will not like it." A horseman's pride, set up for the bullock cart.
- **49**, the coconut-smoke shirt and "My branded arm was hidden now."
- **55 and 59**, "It sits in the lungs. It pays for guns." / "And for kings... That too."
- **61**, the sacks of rice and "dried, wrinkled berries that gave the air its sting."
- **69**, "more teeth than one would expect from the Viceroy's dungeons" through "The question is always to whom." The most characterful sentence in the chapter, and now the seed of Ibrahim's double dealing.
- **75**, "the slow, patient gait of creatures that had never been asked to do anything quickly."
- **89 to 93**, "asked after catches and prices"; "A man who thought he could drown, then changed his mind."
- **97**, "back at the sea with fewer coins and perhaps fewer fingers."
- **103 to 105 (first sentence)**, the shrine, the coin, the ash, "That one carries storms in his bones."
- **109 (last sentence) to 111**, "The road here was better packed, the wheel ruts deeper," and the sentries straightening. His soldier's eye.
- **119**, "He looks like he should already be dead." / "He disagrees."
- **129**, "This is one of his hands on this coast."
- **135**, "I only stopped the crabs from finishing."
- **139 to 157**, the interrogation: "Until the Portuguese netted me." / "Some." / the stylus tap / the official's closing question.
- **167**, "He can decide whether your words are as sharp as you think."

## Chapter-specific notes (continuity and history)

1. **ch5:27 contradicts ch4:67.** Nagoji says "Travancore" himself in Ch 4, and the fisherman replies "You know the name." Fix it in ch5 (Borderline 27); Ch 4 stays as it is.
2. **Travancore and the Portuguese (23; also ch4:63).** In 1738 the king's wars were with Kayamkulam, Desinganad (Kollam) and the Elayadathu branch, and the Dutch were more and more on their side. The Portuguese had been gone from the Kerala ports since the Dutch took them in the 1660s. "No love for them" is safe, and "fights them" is not. Fix ch4:63 in the Ch 4 pass as well.
3. **"King readies for the Dutch" three times** (ch4:63 "sharpens his teeth", ch5:23, ch5:157 "sharpens his sword"). Borderline 157 varies it. OPENINGS_ENDINGS_MOTIFS reserves "teeth" for Part IV, which is another reason to change ch4:63.
4. **The crabs twice.** The Ch 4 fisherman says "Before the crabs claim you" (ch4:75), and Ibrahim says "I only stopped the crabs from finishing" (135). Ibrahim's line is the better one. Drop or vary the Ch 4 line in its pass, or accept it as a joke the village has already told.
5. **Konkani (7).** A Konkani speaker on this coast is plausible: Konkani-speaking merchant families had settled at Kochi since the sixteenth century. Ch4:57 has already set this up. glossary:92 defines Konkani only for the Konkan and Goa, so add half a line if the 2e glossary is revised.
6. **"Our people" (63).** Ibrahim's community is never named in this chapter. "My people trade the length of this coast" is enough, since the name Ibrahim and ch7:213 ("whether I face Mecca or the temple") do the rest. The ash he accepts at the shrine (103) fits the pragmatism of ch7:213. Keep it.
7. **"Officer" (69).** A *huzurat* trooper is not an officer. Let it stand as Ibrahim's sales talk (he is pricing goods). Nagoji not correcting it is in character.
8. **"Horse from Madurai" (157)** is safe as a place name for hired horse. In the Ch 6 pass, check ch6:141's "the Nayak of Madurai": Chanda Sahib had overthrown the Madurai Nayak line by the late 1730s.
9. **"White skin" (161)** has a sibling at ch11:423 ("They think white skin means heavier gold"). Decide once for the whole book how characters name Europeans. This pass avoids adding "firangi", which appears nowhere in Book 1 and would need a glossary entry.
10. **Duplicated halls.** ch5:111 and ch6:19 both use "red stone blocks". ch5:125 and ch6:19 both have carved wooden pillars. ch5:125 and ch6:37 both have "At the far end, on a slightly raised platform, a man sat". The fix here makes the compound plain. In Ch 6, vary "red stone blocks" (for example, "the same red stone as the compound, but dressed and fitted"). Do not use "laterite", a word first used in 1807.
11. **"Tomorrow we take you to the king's war hall" (167)** is consistent enough with Ch 6 ("the king is in council") and with ch7:217 ("the same war hall"). No change.
12. **Kanka.** Do not bring Kanka into Ch 5. Ch6:31 has the memory, and Kanka's sex is still inconsistent between ch1:53 (he) and ch7:145 (she) until the book-level fix lands.
13. **Scar tic.** With 25 cut, the scar appears once (21). OPENINGS_ENDINGS_MOTIFS suggests bringing it back at ch11:405 or ch15:103. Leave that for those chapters.
14. **Dhoti (49, 127)** is Nagoji's own word from the north. The coast's word is *mundu*. Keep "dhoti" in his narration. Watch for it in local characters' mouths elsewhere.
15. **Timeline.** With the dusk resets gone, the day reads: the woman's house, a walk inland, the cart through the afternoon, nightfall on the road, the compound by lamplight. That fits Ch 6's "crossed a few hills from a minor compound".
