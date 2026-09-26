# Second-Edition Audit: Prequel ("The Vow and the Tiger")

- Source (frozen first edition): `book1_horse_servant/front_matter_prequel.md`, 51 lines, 25 paragraphs, 1,295 words of body text. Line numbers below refer to that file.
- Method: I read the whole file and ruled on every flag from the pattern auditor (63 flags) and the holistic reader (16 suspect passages, 9 human passages, 11 flab notes), merging duplicates. I cross-checked against Chs 1, 2, 3, 6, 7, 10, 11 and 12, the Foreword, the character guide, the glossary, `STYLE_SHEET.md`, `VOICE_BIBLE.md`, `OPENINGS_ENDINGS_MOTIFS.md`, `REVIEW_BACKLOG.md` and `SOURCE_OF_TRUTH.md`. I also ran `audit/tools/scan_slop.py` on the file (output kept in scratch, not in the repo).
- Voice note: unlike the Foreword, this piece is Nagoji's. From line 13 on he says "I", so every fix below is written in his voice: a Maratha rider writing in the 1740s and 1750s, looking back.

## Verdict

| Measure | Call |
|:-|:-|
| Severity | **4 of 5** |
| Recommended intensity | **Deep** (line-level re-voicing, plus paragraph merges; paragraph order can stay) |
| Estimated word cut | **About 28%** (1,295 to about 935 words; measured on a scratch assembly of the fixes below) |

Adjudication totals: **44 confirmed, 8 borderline, 22 defended.**

Most of the prequel reads as machine-written history. The narrator is absent from lines 3 to 11 and fades out again from 31 to 47. The template tics are dense for 1,300 words:

- About eight correction constructions in narration. The limit is one, and only in dialogue, and the prequel has no dialogue. They are at L5, L9 (two), L13, L17, L31, L43 and L45. The scanner catches only four, because it misses the "was not X. It was Y." sentence pair.
- Nine one-sentence paragraphs: L7, 11, 21, 27, 33, 37, 41, 49, 51.
- Ten "like" similes and three "as if" uses, against a ration of two and one.
- Mirrored pairs built for symmetry: tighten/tightening (L29), broke bodies/broke forts (L19 to 21), sharpened/sharpened (L47), and time/time (L9 to 11).

It is not a 5, because four paragraphs carry the real voice: the vow camp (L13), the horse-and-ground lessons (L17), the siege dirty work (L19) and the Vasai wall (L23). The Travancore half also holds sound, needed history. The job is to cut the verdicts and keep the facts. Nothing in the plot, the history or the cast needs to go.

Where the two auditors split, I rule as follows. The Siddis stay, in one clause (L5). The glosses stay for first mentions: "Kochi (Cochin)" is load-bearing, and the other two are borderline. "We broke forts instead" is borderline, not confirmed. The Travancore half stays as a structure, compressed and framed as what Nagoji learned later in the king's service. I overrule the pattern auditor's "he could not know this in 1738": he is writing years afterwards, and L29 says so. I have also rejected one of the holistic reader's suggestions, the "fire my head into the fort" vow, on dating grounds (see Chapter-specific notes).

## Confirmed issues

| Line | Quote | Category | Suggested fix |
|:-|:-|:-|:-|
| 3 | "In the late 1730s, the western coast of India smelled of wet gunpowder and pepper." | modern_register (documentary opener, outsider's map, smell opener) | Replace the paragraph with: "When I rode for Chimaji Appa, the Portuguese and the Marathas had been leaning on each other between the surf and the hills for as long as my father could remember, like wrestlers in the pit, each sure the other would tire first." (This keeps the wrestlers and puts "I" in the first line.) |
| 3 | "Salt wind carried the tang of the Arabian Sea into every camp and every fort." | stock_phrase | Cut. |
| 5 | "On one coast," | geography (sets up the false "two coasts" of L47) | Cut. Start: "The Portuguese still rang their church bells over Goa..." |
| 5 | "stone walls that had learned to swallow screams" | stock_phrase (gothic personification; duplicates ch1:45 "stone thick enough to swallow most screams", the literal use Ch 1 earns) | "...and flew their flags over its walls." |
| 5 | "their caravels and galleys" | modern_register (anachronism: caravels had long gone out of service by the 1730s) | "their galleys" |
| 5 | "The Siddis of Janjira were not priests and merchants like the Portuguese. They were sea fighters, a kingdom of sailors with African blood and Indian shores, hired and hated and feared in the same breath." | correction (straw man, mirrored noun pair, "in the same breath") | Join it to the sentence before: "...by the dark-hulled ships of the Siddis, Habshi sea fighters who had held their island fort at Janjira against every fleet we sent at it." (Janjira never fell to the Marathas. Add *Habshi* to the glossary.) |
| 5 | "Between them, they made the coast feel fenced." | kicker | Cut. |
| 7 | "Then the Maratha hand closed." | kicker (first of nine one-line paragraphs) | Replace with a fact and make it the first sentence of L9: "In 1737 our army came down the ghats into Salsette." (Verify the year; otherwise cut the line.) |
| 9 | "In Pune, Baji Rao, the Peshwa, sent orders like arrows. His younger brother Chimaji Appa carried those orders to the coast and made them personal." | simile (workshop image; introduces the Peshwa as if to strangers; "made them personal" is modern) | "The Peshwa sent the orders from his camp, and his younger brother Chimaji Appa brought them down to the coast himself." |
| 9 | "Chimaji was not a man who loved speeches. He loved tallies of powder" | correction (template repeated for Ramayyan at L45) | "He loved tallies of powder and lists of captured guns, the slow certainty of siege lines tightening." |
| 9 | "But he understood something about the Portuguese that many inland men missed. They were not unbeatable because they were white or Christian. They were dangerous because they had fort walls, cannon, and the patience of men who believed time itself worked for them." | correction (vague "something" reveal; two corrections whose logic does not meet, "not unbeatable" against "dangerous"; abstract third item) | "He knew what made the Portuguese hard to beat: stone walls, good cannon, and ships that brought them powder and rice all through the rains, when our army had to go home." |
| 11 | "So Chimaji vowed that time would not save them." | kicker (announces the vow that L13 then shows) | Cut. |
| 13 | "his face hard in the flicker" | stock_phrase | Cut. "a lamp smoking beside him" already lights him. |
| 13 | "He did not promise easy victory. He promised" | correction | "He promised that no foreign flag would sit on Konkan soil unchallenged, not the Portuguese cross, not the Siddi banner painted on a prow." |
| 13 | "to make the coast remember who it had always belonged to" | stock_phrase (speech-writer rhetoric; the title's vow holds nothing a rider would carry away) | "He promised to take their forts one by one, and he swore to the goddess Vajreshwari that on the day Vasai fell he would build her a temple of stone." (Verify; see notes. If in doubt, stop at "one by one.") |
| 15 | "Wars are made of such vows. They are also made of trenches, and blood, and the stubborn labour of men who drag cannon through mud." | summary (present-tense aphorism, polysyndeton; L17 shows it anyway) | Cut. If the author wants the cannon image, add "and guns dragged through mud" after "weeks of hunger" at L17. |
| 17 | "The Konkan campaign was not a single battle. It was a grinding season" | correction | "The Konkan campaign was a grinding season of sieges and raids, ..." |
| 17 | "We learned to cut supply lines, to watch for the glint of a musket barrel in coconut groves, to move like a flood and vanish like smoke." | simile (infinitive triad, two stacked stock similes, later staff term) | "We learned to watch for the glint of a musket barrel in the coconut groves." (The night attacks on carts in the sentence before already cover the supply raids.) |
| 19 | "They broke bodies in cells under Goa and called it justice." | stock_phrase | "When that failed, they sent iron and rope, and broke bodies in the cells under Goa." |
| 23 | "the Portuguese fortress that watched the sea like an old predator" | simile (generic, over the ration) | Cut the clause: "At Vasai (Bassein) I saw a wall tremble under our guns." |
| 23 | "I saw my black mare Kanka take a ball through the chest and fold as if the ground had suddenly gone soft beneath her." | continuity (Ch 1 has Kanka a stallion shot at the capture, ch1:53 to 55; REVIEW_BACKLOG BL-01 and FM-15), plus filler "suddenly" | "A ball from the bastion took the grey mare beside me through the chest, and she folded as if the ground had gone soft beneath her. I got down and held Kanka's head until he stood quiet again." (Option: make her Keshavrao's grey, which plants the comrade of ch2:89 and ch3:177.) |
| 23 | "In the roar and confusion, in the stink of powder and blood, I understood that campaigns turn into legends because the men who live through them need something to hold onto when the dead begin to outnumber the living." | explained_subtext (an epiphany in place of grief; breaks style sheet 4) | Cut. |
| 25 to 27 | "In those months, we spoke as if Konkan was the whole world. We spoke as if Chimaji Appa’s war was the only war that mattered. / It was not." | kicker (mirrored setup, three-word reversal paragraph, two "as if" over the ration) | "In those months the Konkan was the whole world to us, and Chimaji Appa’s war the only war." Make it the first sentence of the L29 paragraph and cut "It was not." |
| 29 | "Far south, beyond the passes and the Deccan plateau, beyond the long curve of the Malabar coast where pepper vines climbed trees like hungry fingers, another king was shaping a kingdom with the same ruthless patience." | simile ("beyond, beyond" atlas view; "hungry" again after L13; "ruthless patience" repeats L9's "patience") | "Far down the same coast, at the end of the pepper country, another king was taking his land back from the men who ruled it in his name." |
| 29 | "But later, in Travancore, I learned that while Chimaji tightened his siege lines against Portuguese stone, Marthanda Varma of Venad was tightening his grip on men and land." | balanced_antithesis (tighten/tightening mirror, stock "tightening his grip") | Keep the frame and drop the mirror: "He was Marthanda Varma, and his country was Venad, which the Europeans called Travancore. The rest I learned later, in his service." (This also links Venad and Travancore, which the first edition never does.) |
| 31 | "Venad was not supposed to frighten anyone. It was a wet strip of country" | correction | "To a Deccan man Venad was hardly a country at all: a wet strip between the mountains and the sea, broken into quarrelling houses and temple lands, rich in pepper and coconut and river mouths." |
| 31 | "and rich, too, in the kind of small pride that makes neighbours sharpen knives" | stock_phrase ("the kind of X that Y", rhetorical doubling) | Cut. |
| 31 | "many had lived too long under the shadow of Dutch treaties and European guns to imagine a future that was fully their own." | stock_phrase ("under the shadow of", modern self-determination language) | "Its neighbours were older and some were richer, but most of them sold their pepper at whatever price the Dutch set." |
| 33 | "Marthanda Varma did imagine it." | kicker (callback one-liner) | Cut. Open L35 with the borderline fix B5: "Marthanda Varma meant to set the price himself, and to say which foreign ship could anchor where." |
| 35 | "He had the ego of a man who refuses to stay small." | modern_register | Cut. |
| 35 | "Venad learned, in a short brutal span, that this king would not be managed." | kicker (verdict closer, management word) | Cut. |
| 37 to 39 | "Then he turned outward. / Small kingdoms and chiefdoms that had spent generations balancing each other suddenly found a new weight pressing on them." | kicker (one-line pivot mirroring L7; vague "new weight"; also pre-spends Ramayyan's "reach outward" at ch10:151) | "When his own house was quiet he turned on his neighbours, small kingdoms and chiefdoms that had spent generations balancing each other." |
| 39 | "Some bent. Some resisted. Some ran to older powers for protection." | tricolon (staccato fragment run) | "A few chiefs bent to him. Others fought, or wrote to the Dutch for help." |
| 39 | "It was in the interest of the Dutch that no single prince on the Malabar coast became too strong. A divided land made treaties easy. A divided land signed away pepper cheaply, prince by prince, without the Dutch needing to maintain an expensive army beyond the walls of their coastal forts." | modern_register (textbook exposition, anaphora, budget-brief phrasing) | "That suited the Dutch. A divided coast sold its pepper cheap, prince by prince, and the Company seldom had to send a soldier beyond the walls of its forts." |
| 41 | "So the Dutch played the coast like a stringed instrument." | kicker (simile one-liner restating L39) | Cut. |
| 43 | "Kochi (Cochin), long a pivot between European powers, watched with alarm." | stock_phrase | "In Kochi (Cochin), where the Dutch had held the fort since they drove out the Portuguese, the Raja took fright." (Keep the gloss; see Defended.) |
| 43 | "Principalities nursed grievances and old succession disputes like infected wounds." | stock_phrase (cliche plus simile over the ration) | Cut. |
| 43 | "Dutch agents offered arms and ammunition, offered promises, offered the thin comfort of European umbrellas." | tricolon (anaphora; the protective "umbrella" is a twentieth-century image) | "Dutch agents offered muskets and powder to any prince who would sign their pepper contracts." |
| 43 | "Alliances formed, not out of love, but out of fear." | correction (the plainest not-X-but-Y in the file, used as a kicker) | Cut. |
| 45 | "He had something most of his rivals lacked, a minister who could see past today’s feud to tomorrow’s war." | balanced_antithesis (reveal construction, mirrored slogan) | "He had Ramayyan, his Dalawa," (join to the next fix) |
| 45 | "Ramayyan Dalawa was not a man who shouted on battlefields. He was a man who counted, who read letters in multiple tongues, who understood that pepper is not just spice but power." | correction (L9 template again; "not just X but Y" nested inside; "multiple tongues") | "...who counted everything and could tell you what a candi of pepper would buy in muskets." (This plants the ledger of Ch 21.) |
| 45 | "Under his guidance, the king gathered guns, trained men, and made a state that could endure beyond one season’s victory." | modern_register (tricolon ending in political-science abstraction) | "Between them they bought guns and threw earth walls across the passes from Madurai." (Matches the Aramboli works in the Foreword and Ch 12.) |
| 47 | "By 1738, two storms were rising on two coasts. In the west, Chimaji Appa’s vow sharpened ... In the deep south, Marthanda Varma’s ambition sharpened Travancore against every neighbour, every rival house, and every European company that believed this coast could be owned." | summary (recap of both halves; sharpened/sharpened mirror; "every" triad; spends the storm reserved for ch13:321; wrong geography) | Cut the whole paragraph. |
| 49 to 51 | "I was only a cavalryman then, one more rider in Chimaji’s shadow, thinking I knew what war was. / The Portuguese taught me otherwise." | summary (stock foreshadow and moral closer; "only" undercuts the *huzurat* pride of ch1:7) | Replace; see Ending. |

## Borderline

| # | Line | Quote | Ruling and suggested treatment |
|:-|:-|:-|:-|
| B1 | 1 | "Prequel: The Vow and the Tiger" | The tiger never appears in the text. This is not slop, but the title promises an image the text never plants. Either retitle it "Prequel: The Vow", or let the merchants' rumour at L29 carry the word once: "...beyond a rumour carried by pepper merchants, of a young king in the south they called a tiger." Coordinate with `OPENINGS_ENDINGS_MOTIFS.md` 1.7, which reserves the Tiger epithet for Part IV with one earlier plant, so the book does not end up with two plants. |
| B2 | 13 | "hands touching sword hilts and prayer beads with equal familiarity" | The image is concrete; "with equal familiarity" is the writerly tag that sums it up. Trim to: "the men answered in murmurs, one hand on a sword hilt and the other on prayer beads." |
| B3 | 21 | "We broke forts instead." | This is a dry soldier's retort, and Ch 1 uses the same verb ("after we broke a string of Portuguese forts", ch1:9). As a stand-alone paragraph, though, it reads as a rhyme on "broke bodies". Keep the words, but only if "and called it justice" goes, and drop the paragraph break so it opens the Vasai paragraph. |
| B4 | 23 | "I saw a wall tremble ... I saw men climb ... I saw my black mare" | Witness anaphora, with every item concrete. Keep the first two "I saw" sentences. The continuity fix above changes the verb of the third, which breaks the triad without losing anything. |
| B5 | 35 | "He dreamed of a southern empire, a single authority that could tell the pepper coast what price it would accept and which foreign ship could anchor where." | The tail is concrete and good; "dreamed of a southern empire, a single authority" is abstract. Trim to: "Marthanda Varma meant to set the price himself, and to say which foreign ship could anchor where." |
| B6 | 35 | "the Eight Houses who had treated the crown like a decoration while they ruled the land" | Good content, but this would be the third "like" simile. Make it plain: "the Eight Houses who had let the king wear the crown while they ruled the land". |
| B7 | 43 | "The Samudri, the Zamorin of Kozhikode (Calicut), understood that a king who grew too strong in the south would eventually pull at the north as well." | This is court talk Nagoji could have heard later, so it may stay. The double title plus gloss is heavy, and the chapters say "Zamorin" (REVIEW_BACKLOG FM-09). Suggested: "The Zamorin at Kozhikode (Calicut) knew that a king who swallowed the south would come north next." |
| B8 | 23, 43 | "(Bassein)", "(Calicut)" | English glosses in first-person narration are a mild tic, but these are the book's first mentions and readers may know only the older names. Keep them, or move them to the glossary; the author decides. "Kochi (Cochin)" is defended separately. |

## Defended (flagged, keep)

| Line | Quote | Why it stays |
|:-|:-|:-|
| 3 | "Between the surf and the hills, empires pressed against each other like wrestlers, each convinced the other would tire first." | Both auditors like it. The image is a kusti pit, from Nagoji's world, and it makes a real point about attrition. It is one of the two "like" similes to keep. The opening fix carries it into a first-person sentence. |
| 5 | "long enough to believe it belonged to them by habit" | Pattern auditor, severity 1. This is a dry, ironic judgement in his voice, not a mirrored turn. |
| 5 | "Their forts along the Konkan were a chain of white teeth" | Whitewashed forts seen from the land. It is a metaphor, not a simile. Count it against the "teeth" budget in `OPENINGS_ENDINGS_MOTIFS.md` (front matter, one use). |
| 5 | The Siddis themselves | Both auditors wanted them compressed, and they are, to one clause. They should not go entirely: the vow's "Siddi banner painted on a prow" needs them, and the character guide lists them only because the prequel has them (REVIEW_BACKLOG FM-06). |
| 9 | "He loved tallies of powder and lists of captured guns, the slow certainty of siege lines tightening." | Concrete: Chimaji Appa as a siege accountant. The "tighten" echo goes once L29 is fixed. |
| 9, 11, 13, 29, 49 | Bare "Chimaji" | The holistic reader says a rider would always say "Chimaji Appa", but the chapters use both forms ("Chimaji was coming for Goa", ch1:63; "find Chimaji", ch6:191). Prefer "Chimaji Appa" at first mention in a paragraph. It is not a rule. |
| 9 | "white" (as a word) | Ramayyan says "They think white skin means heavier gold" in ch11:423, so the word is not foreign to the book. The sentence goes because it is a correction (see Confirmed), not because of the word. |
| 13 | "I heard the vow in a camp that stank of horse sweat and damp rope. The monsoon had passed, leaving the earth soft and the mosquitoes hungry." | The first witnessed moment, told through a horseman's senses. The "hungry" echo goes with the L29 fix. |
| 13 | "Brahmins chanted in a small, stubborn voice" | The pattern auditor calls it a doubled adjective. It is odd and exact, and it earns both words. The "stubborn" echo goes with L15, and the word quietly plants ch1's "this one is stubborn". |
| 13 | "not the Portuguese cross, not the Siddi banner painted on a prow" | A list of flags, not a correction. Concrete. |
| 17 | "forts that fell after weeks of hunger and sudden night attacks that left a road littered with broken carts and spilled grain" | Concrete campaign detail. |
| 17 | "We learned that Portuguese guns could kill a horse as easily as a man, and that a cavalry charge means nothing if the ground is chopped into ditches and sharpened stakes." | Trade knowledge. The present tense "means" is a horseman's rule, of a piece with ch7's "the ground lies to you". |
| 19 | "The Portuguese fought like men defending a house they had stolen and made their home." | Fresh and morally complicated. The second "like" simile to keep. |
| 19 | "They countermined our tunnels. They bribed scouts. They sent priests to promise salvation to men who could not read their prayers." | The pattern auditor calls this drumbeat anaphora. It is an inventory of real siege practice, the kind `VOICE_BIBLE.md` T2 allows, and it plants Keshavrao's "We will sweat for their salvation" (ch2:87). Optional: "our scouts". |
| 19 | "When that failed, they sent iron and rope." | Concrete, and it prepares for Ch 1. |
| 23 | "I saw a wall tremble under our guns. I saw men climb into smoke with ladders shaking in their hands." and "fold as if the ground had gone soft beneath her" | Fear shown, not named. The fold is the rider's image of a horse going down, and it is the chapter's one allowed "as if". |
| 29 | "I did not meet him then. I did not even know his name beyond a rumour carried by merchants." and the "later, in Travancore, I learned" frame | An honest limit on what he knew. The pattern auditor objects that Nagoji could not know Dutch policy in 1738, but he is writing years later, after service under Ramayyan, and this line says so. The frame licenses everything that follows. |
| 29 to 45 | The Travancore half as a structure | Keep it; do not move it to the Historical Note. It is the "Tiger" half of the title. It introduces Marthanda Varma and Ramayyan before Ch 6, and it sets up the Deccan condescension that Ch 10 then undoes. Compress it; do not remove it. |
| 31 | "a wet strip of country pressed between the mountains and the sea, broken into quarrelling houses and temple lands, rich in pepper and coconut and river mouths" | Concrete geography with a Maratha's condescension. |
| 35 | "To build it, he first crushed the threats inside his own house. The Thampi brothers who claimed power by blood and violence were hunted down." | Plain, necessary history. Trim only. |
| 43 | "Kochi (Cochin)" | Load-bearing. Ch 11 dropped its own "(Cochin)" gloss because the prequel gives it (`SOURCE_OF_TRUTH.md` 5.3). |
| 45 | "Inside Venad, Marthanda Varma prepared anyway." | Plain and in voice. Neither auditor flagged it. |

## Opening

**Current (L3):** "In the late 1730s, the western coast of India smelled of wet gunpowder and pepper. Salt wind carried the tang of the Arabian Sea into every camp and every fort. Between the surf and the hills, empires pressed against each other like wrestlers, each convinced the other would tire first."

**Verdict: revise.** This is a documentary voice-over. It gives a date, a region and a smell pair, then two paragraphs of exposition, and the narrator does not appear until L13. It also uses an outsider's map ("India", "the Arabian Sea") and opens on a smell, which `OPENINGS_ENDINGS_MOTIFS.md` 2.2 wants to reserve for Ch 13 alone. The wrestlers are the one image worth keeping.

**Proposed:** "When I rode for Chimaji Appa, the Portuguese and the Marathas had been leaning on each other between the surf and the hills for as long as my father could remember, like wrestlers in the pit, each sure the other would tire first."

This sets up the first-person contract in line one, keeps the protected simile, gives a family's sense of time in place of a date, and leaves the paragraph order intact, so the rest of the edit is cutting. The holistic reader's alternative, opening on "I heard the vow in a camp that stank of horse sweat and damp rope" (L13), also works. It would mean moving the Portuguese and Siddi context after the vow, and it opens on a smell. I prefer the smaller change.

## Ending

**Current last lines (L49 to 51):** "I was only a cavalryman then, one more rider in Chimaji’s shadow, thinking I knew what war was. / The Portuguese taught me otherwise."

**Verdict: rewrite.** The closing pair uses the stock "thought I knew / taught me otherwise" foreshadow, and it ends on a moral, which style sheet 3 forbids. The last line is also the ninth one-line paragraph. "Only a cavalryman" undercuts the *huzurat* pride that ch1:7 sets up a page later. The paragraph before it (L47) spends the storm motif and must go too.

**Proposed ending (replaces L47 to 51):**

> In the cold season our sardar took the troop down the coast toward Goa, to strike at Portuguese outposts and the carts on their roads. One morning on the north bank of the Chapora I sat Kanka and listened to the church bells of Bardez ringing across the water.

Why this ending:

- It ends on an image.
- It closes the prequel's own bells (L5) and hands straight on to Ch 1, where "the bells of Goa's churches rang for evening prayers" (ch1:9), and to Ch 2's first line, "They woke us under cover of bells."
- It keeps Kanka alive and male, so João's "Your horse is dead ... We shot it when we brought you in" (ch1:53) still lands as news.
- It matches Ch 1's account of what the Portuguese say he did ("attacked Portuguese caravans and outposts", ch1:49).
- It uses no storm and no moral.

Geography: Bardez had been Portuguese since the 1540s, while the land north of the Chapora did not become Portuguese until much later, so the river is a natural frontier. If the author places the capture somewhere else, keep the shape and drop the names: "One morning, a day's ride short of Goa, I sat Kanka on a river bank and listened to church bells ringing across the water."

## Flab (passages to tighten)

| Lines | Problem | Target |
|:-|:-|:-|
| 3 to 11 | Context is delivered three ways (smell, Portuguese and Siddi survey, Chimaji's character) before anyone says "I". The vow is announced at L11 and then told again at L13. | About 277 words down to about 190. One opening sentence, one Portuguese paragraph, one Chimaji paragraph. Cut L11. |
| 15 | An aphorism that L17 then shows. | Cut (25 words). |
| 23 | The last sentence explains away the horse's death. | End on the horse (see Confirmed). |
| 25 to 27 | A transition spread over two mirrored sentences and a three-word paragraph. | One sentence, merged into L29. |
| 29 to 47 | 571 words, about 44 percent of the prequel. Marthanda Varma's ambition is stated five times (L29 "ruthless patience", L33, L35 "ego" and "southern empire", L37, L47). Dutch divide-and-rule is explained four times running (L39 twice, L41, L43). The Thampis and the Pillamar are also told at length in the Foreword, which sits directly before the prequel in the build (`SOURCE_OF_TRUTH.md` section 3), and in scene by Ramayyan at ch10:151. | About 330 words. One statement of ambition (B5), one of Dutch policy (the L39 fix), and one sentence each for the Thampis and the Pillamar. |
| 43 | Four sentences on neighbours' fears, two of them stock. | Two sentences: Kochi, and the Zamorin (B7), plus the Dutch agents fix. |
| 45 | Ramayyan is introduced as a list of qualities. | One concrete trait (the candi of pepper in muskets) and one concrete act (walls across the passes). |
| 47 | A recap of everything just read, with wrong geography. | Cut. |

## Passages to protect

1. "I heard the vow in a camp that stank of horse sweat and damp rope. The monsoon had passed, leaving the earth soft and the mosquitoes hungry." (L13)
2. "Behind him, Brahmins chanted in a small, stubborn voice, and the men answered in murmurs" (L13)
3. "not the Portuguese cross, not the Siddi banner painted on a prow" (L13)
4. "forts that fell after weeks of hunger and sudden night attacks that left a road littered with broken carts and spilled grain" (L17)
5. "We learned that Portuguese guns could kill a horse as easily as a man, and that a cavalry charge means nothing if the ground is chopped into ditches and sharpened stakes." (L17)
6. "The Portuguese fought like men defending a house they had stolen and made their home. They countermined our tunnels. They bribed scouts. They sent priests to promise salvation to men who could not read their prayers. When that failed, they sent iron and rope." (L19)
7. "I saw a wall tremble under our guns. I saw men climb into smoke with ladders shaking in their hands." (L23) and "fold as if the ground had ... gone soft beneath her" (L23)
8. "long enough to believe it belonged to them by habit. Their forts along the Konkan were a chain of white teeth" (L5)
9. "empires pressed against each other like wrestlers, each convinced the other would tire first" (L3, to be moved into the new first sentence)
10. "He loved tallies of powder and lists of captured guns, the slow certainty of siege lines tightening." (L9)
11. "I did not meet him then. I did not even know his name beyond a rumour carried by merchants." (L29)
12. "a wet strip of country pressed between the mountains and the sea, broken into quarrelling houses and temple lands, rich in pepper and coconut and river mouths" (L31)
13. "a single authority that could tell the pepper coast what price it would accept and which foreign ship could anchor where" (L35; its content survives the B5 trim)

## Chapter-specific notes (continuity and history)

1. **Kanka (REVIEW_BACKLOG BL-01, FM-15).** The prequel's "my black mare Kanka" dying at Vasai contradicts Ch 1, where Kanka is a stallion shot at the capture. Follow the backlog ruling: keep Ch 1, and have another horse die at Vasai (Confirmed, L23). One more reason to keep Kanka off the page at the capture: ch1:53 plays his death as news João gives Nagoji, and that only works if the prequel has not shown it. The Ch 7 fixes in BL-01 (ch7:145 and 179) also remove Ch 7's walk "the last miles to Goa" from Vasai, which would be hundreds of miles.
2. **Dates.** Ch 1 fixes the capture in 1738 (ch1:9). Vasai fell in May 1739, after the long siege. The L23 wall scene therefore has to be one of the earlier Maratha attacks on Vasai in 1737 to 1738, and the text must not imply the fort fell while Nagoji was there. The fixes above do not. **Do not adopt the holistic reader's suggestion** to use Chimaji Appa's famous "fire my head into the fort from a cannon" vow: tradition ties it to the 1739 siege, when Nagoji is already in the Goa cellar. The Vajreshwari temple vow proposed at L13 is also a Vasai tradition. It is phrased as a promise about the future, so it survives the dating, but verify it before print, and if in doubt cut the clause and stop at "one by one."
3. **"In 1737 our army came down the ghats into Salsette" (L7 fix).** This is the spring 1737 Salsette campaign, when Thane fell. Verify the month if the author wants it named. Also, in 1737 to 1738 the Peshwa spent much of the season campaigning in the north, so the first edition's "In Pune ... sent orders" is loose, and the fix says "from his camp".
4. **Siddis.** Chimaji Appa had already beaten the Siddi fleet in 1736 (verify), so by the time of this vow the Siddis are a remaining enemy, not the main guard of Portuguese shipping. "Guarded, when it suited them" is vague enough to stand, but do not make it stronger.
5. **"Two coasts" (L5, L47).** Goa and Travancore are on the same western seaboard. Both uses go with the Confirmed cuts.
6. **Duplicate with Ch 1.** "stone walls that had learned to swallow screams" (L5) and "stone thick enough to swallow most screams" (ch1:45). Cut the prequel's (Confirmed).
7. **Overlap with the Foreword and Ch 10.** The Foreword, directly before the prequel, gives the Thampis and the Pillamar at length. The Foreword audit (`audit/chapters/front_matter_foreword.md`) cites the prequel as a reason to shrink the Foreword, and this audit cites the Foreword as a reason to shrink the prequel. Settle it once: the Foreword keeps the author's opinion, and the prequel keeps one plain sentence each. Ramayyan's speech at ch10:151 ("Only after those knots were cut could he afford to reach outward") is the scene version, so the prequel should not pre-spend "turned outward".
8. **Naming.** The Foreword has "the Eight Lords", the prequel "the Eight Houses", and Ch 10, the glossary and the character guide have "Lords of the Eight Houses". Align them. For "Samudri" against "Zamorin", see FM-09. Ramayyan is "Dalawa" here, but "diwan" in Chs 6 to 10 and "Dalawa" from Ch 13 (`VOICE_BIBLE.md` section 4). Ramayyan held the Dalawa office from about 1737 (verify), so "By 1738" works, but decide what Chs 6 to 10 call him.
9. **Venad and Travancore.** The first edition uses both names without ever linking them. The L29 fix does it once.
10. **New terms introduced by the fixes.** Habshi, Salsette, Vajreshwari, Chapora and Bardez would be new to the book. Add any that are kept to the glossary. The book never uses "Firangi" or "Parangi", so I have not introduced them. The Portuguese stay "the Portuguese", as in every chapter.
11. **Ch 12 conflict.** Ch 12 has Nagoji "fled the Peshwa's justice" and "in my exile" (`SOURCE_OF_TRUTH.md` section 7). The prequel, with the new ending, fixes his capture in the field on a raid. Fix Ch 12, not the prequel.
12. **Title.** See B1. If the Tiger stays in the title, plant it once at L29, or retitle.
13. **Copyedit.** Hyphenate "dark hulled" to "dark-hulled" (L5). This is a hyphen in a compound adjective, not a dash.
14. **Word-bank echoes** that survive until the cuts are made: patience (L9, 29), hungry (13, 29), tighten (9, 29 twice), sharpen (17, 31, 47 twice), shadow (31, 49), stubborn (13, 15), pressed (3, 31, 39), strip (5, 31), and broke or broken (17, 19, 21, 35). After the confirmed fixes, only "broke" (L19, 21, 35) and one each of the others remain.

## Appendix: the confirmed fixes read together (reference only)

This is a scratch assembly to check that the fixes read as one voice and to measure the cut (about 935 words). It is not a proposed final text. The author edits the 2e file, and the borderline calls are applied here only as recommended.

> When I rode for Chimaji Appa, the Portuguese and the Marathas had been leaning on each other between the surf and the hills for as long as my father could remember, like wrestlers in the pit, each sure the other would tire first.
>
> The Portuguese still rang their church bells over Goa and flew their flags over its walls. They had held that coast for generations, long enough to believe it belonged to them by habit. Their forts along the Konkan were a chain of white teeth, and their galleys prowled the sea lanes, guarded, when it suited them, by the dark-hulled ships of the Siddis, Habshi sea fighters who had held their island fort at Janjira against every fleet we sent at it.
>
> In 1737 our army came down the ghats into Salsette. The Peshwa sent the orders from his camp, and his younger brother Chimaji Appa brought them down to the coast himself. He loved tallies of powder and lists of captured guns, the slow certainty of siege lines tightening. He knew what made the Portuguese hard to beat: stone walls, good cannon, and ships that brought them powder and rice all through the rains, when our army had to go home.
>
> I heard the vow in a camp that stank of horse sweat and damp rope. The monsoon had passed, leaving the earth soft and the mosquitoes hungry. Chimaji stood in a circle of officers, a lamp smoking beside him. Behind him, Brahmins chanted in a small, stubborn voice, and the men answered in murmurs, one hand on a sword hilt and the other on prayer beads. He promised that no foreign flag would sit on Konkan soil unchallenged, not the Portuguese cross, not the Siddi banner painted on a prow. He promised to take their forts one by one, and he swore to the goddess Vajreshwari that on the day Vasai fell he would build her a temple of stone.
>
> The Konkan campaign was a grinding season of sieges and raids, forts that fell after weeks of hunger and sudden night attacks that left a road littered with broken carts and spilled grain. We learned to watch for the glint of a musket barrel in the coconut groves. We learned that Portuguese guns could kill a horse as easily as a man, and that a cavalry charge means nothing if the ground is chopped into ditches and sharpened stakes.
>
> The Portuguese fought like men defending a house they had stolen and made their home. They countermined our tunnels. They bribed our scouts. They sent priests to promise salvation to men who could not read their prayers. When that failed, they sent iron and rope, and broke bodies in the cells under Goa.
>
> We broke forts instead. At Vasai (Bassein) I saw a wall tremble under our guns. I saw men climb into smoke with ladders shaking in their hands. A ball from the bastion took the grey mare beside me through the chest, and she folded as if the ground had gone soft beneath her. I got down and held Kanka's head until he stood quiet again.
>
> In those months the Konkan was the whole world to us, and Chimaji Appa's war the only war. Far down the same coast, at the end of the pepper country, another king was taking his land back from the men who ruled it in his name. I did not meet him then. I did not even know his name beyond a rumour carried by merchants. He was Marthanda Varma, and his country was Venad, which the Europeans called Travancore. The rest I learned later, in his service.
>
> To a Deccan man Venad was hardly a country at all: a wet strip between the mountains and the sea, broken into quarrelling houses and temple lands, rich in pepper and coconut and river mouths. Its neighbours were older and some were richer, but most of them sold their pepper at whatever price the Dutch set.
>
> Marthanda Varma meant to set the price himself, and to say which foreign ship could anchor where. First he crushed the threats inside his own house. The Thampi brothers who claimed power by blood and violence were hunted down. The *Ettuveetil Pillamar*, the Eight Houses who had let the king wear the crown while they ruled the land, were broken and scattered.
>
> When his own house was quiet he turned on his neighbours, small kingdoms and chiefdoms that had spent generations balancing each other. A few chiefs bent to him. Others fought, or wrote to the Dutch for help. That suited the Dutch. A divided coast sold its pepper cheap, prince by prince, and the Company seldom had to send a soldier beyond the walls of its forts.
>
> In Kochi (Cochin), where the Dutch had held the fort since they drove out the Portuguese, the Raja took fright. The Zamorin at Kozhikode (Calicut) knew that a king who swallowed the south would come north next. Dutch agents offered muskets and powder to any prince who would sign their pepper contracts.
>
> Inside Venad, Marthanda Varma prepared anyway. He had Ramayyan, his Dalawa, who counted everything and could tell you what a candi of pepper would buy in muskets. Between them they bought guns and threw earth walls across the passes from Madurai.
>
> In the cold season our sardar took the troop down the coast toward Goa, to strike at Portuguese outposts and the carts on their roads. One morning on the north bank of the Chapora I sat Kanka and listened to the church bells of Bardez ringing across the water.

Checks on this assembly:

- Two "like" similes (the wrestlers and the house) and one "as if" (the fold). Both are within the ration.
- No correction constructions and no one-line paragraphs.
- No storm and no em dashes.
- It ends on an image.
