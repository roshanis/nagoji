# Second-Edition Audit: Chapter 8, Padmini Amma's Estate

- Source (frozen first edition): `book1_horse_servant/book2_chapter08_padmini_ammas_estate.md`, 243 lines, 3,427 words by `wc`.
- Line numbers are physical lines in that file, blank lines included. A fresh copy in `manuscript/` will match them until its first edit, so apply fixes from the bottom up.
- Method: I read the chapter in full and ruled on every flag from the pattern auditor (104 flags) and the holistic reader (37 passages, 19 flab notes), merging duplicates. I checked the end of Ch 7, the opening of Ch 9, the cellar payoff in Chs 16 and 17, the "Eight Houses" in Chs 21 and 22, and the book-level audits (`OPENINGS_ENDINGS_MOTIFS.md`, `REGISTER_AND_ANACHRONISM.md`, `VOICE_BIBLE.md`, `REVIEW_BACKLOG.md`). I ran `audit/tools/scan_slop.py` on the chapter. To test the cut estimate, I applied every confirmed fix and the "take" borderlines to a scratch copy outside the repo and rescanned it.
- Source tags in the tables: **P** = pattern auditor, **H** = holistic reader, **N** = new in this pass.

## Verdict

| Measure | Call |
|:-|:-|
| Severity | **4 of 5** |
| Recommended intensity | **Medium** (tics plus tightening). Most fixes are cuts, but three blocks need line-level rebuilding: the arrival (47 to 61), the *sambandham* lecture (149 to 197) and the close (229 to 243). |
| Estimated word cut | **About 30%** (3,427 to about 2,400 words; the scratch pass came to 2,400). Two blocks account for more than half of it: the lecture (693 words down to about 320) and the close (212 words down to 20). Outside those blocks the line-level cut is about 13%. If the author wants to keep more of the *sambandham* explanation for readers new to it, a 450-word version brings the total to about 25%. |
| Scanner, before and after the scratch pass | not-X-but-Y 4 to 0; "Not" openers 4 to 0; ", not" 5 to 3 (all in dialogue: 11, 163, 223); "as if" 4 to 1; "like a" 5 to 1 (the clerk's scale, from his world); soft adverbs 4 to 1; "gently" 2 to 0; "Somehow" 1 to 0; fragments 2 to 0; one-sentence paragraphs 23 to 16; "power" 8 to 0; Padmini's stick as a gesture 7 to 4 |

The chapter is two books laid over each other. The dialogue core is often very good and sounds like one household: Ramayyan's caste check and "We do not plough" (27 to 39), the measured/insulted exchange (77 to 83), the soldier's count against the landholder's (95 to 97), the grandmother's gossip (101), the son's-wife question (107), "I own this land. Why should I not?" (147), the navel-to-feet threat (197) and "Confusion is useful" (223). None of that should be touched beyond a word.

The slop is in the narration and in three blocks, and it is dense enough there to read as machine-written:

1. **The *sambandham* lecture (149 to 197).** About 700 words of as-you-know exposition with a false Sanskrit etymology, three anaphoric triples (159, 171, 183), "Not X. Not Y." fragments, modern rights and "system" language, and lean-back, lean-forward choreography. Nagoji becomes a question-feeder. The matrilineal point is made four times (55, 101, 159 to 171, 183), and 101 does it best in five lines of gossip.
2. **The close (231 to 243).** Five closing moves in a row after the chapter's best image at 229: a Goa/Pune/Here tricolon, a vague "something less obvious and perhaps more dangerous", a fragment-pair button, a moral with a timeline error (Dutch drill manuals before Colachel) and an "I had faced X and Y; somehow this felt harder" quip.
3. **The arrival (47 to 61).** "Yet everything about it said power", then "Power in... Power in... Power in...", "like quiet promises", a signpost on the cellar panel ("That was what made it feel important"), and a fragment ladder that recaps who Nagoji is.

Two habits run through the rest:

- **The narrator explains a scene that has already landed** (11, 35, 113, 115, 137, 189, 225).
- **Padmini is choreographed like a stage figure.** Her stick taps as punctuation (7 uses), she leans back and forward, studies him, and her mouth and expression shift on cue.

The verdict is severity 4, not 5, because the cure is mostly deletion: the good lines are already on the page and simply need the explanations cleared away from them.

## Confirmed issues

67 rows. Duplicates from both auditors are merged. The order follows the text.

| Line | Quote | Category | Suggested fix |
|:-|:-|:-|:-|
| 5 | `part of the landscape` | modern_register (P, H) | "I became, in a small way, one of the sights of that beach: the foreign captain who yelled at horses." Change only the idiom. The rest of the paragraph is a Voice Bible touchstone (T6). |
| 9 | `small wars that never reached European maps` | modern_register: a historian's frame (P, H) | "small wars that no clerk in Pune would ever write down, though they decided who paid tax and who held a temple key." |
| 9 | `reins that did not care about pain` | flourish: personified tack (P, H) | "my bandaged fingers clenched on the reins." |
| 11 | `We also came back with a different kind of silence, the kind that forms when soldiers have watched you ride into danger instead of pointing at it from behind.` | stock_phrase ("a different kind of X, the kind that"); explains the men's respect (P, H) | Cut. "We came back with cuts and missing men." then Ramayyan's line, which does the same job. |
| 13 | `Not to the war hall, but to a smaller pavilion near the temple.` | correction (P) | "Then the King's ola came, calling me to a small pavilion near the temple." |
| 35 | `It was not enough to be a soldier. In this land, as in mine, questions of blood and birth could close a door faster than any bolt.` | explained_subtext; aphorism; a figurative door that competes with the one real door, the cellar panel (P, H, N) | Cut both sentences. "He studied me." can stand alone, or go too. "Which line?" and the stables line carry the test. |
| 37 | `testing the sound on his tongue` | stock_phrase (P, H) | "“Sawant,” he repeated. “Good. That will satisfy..." |
| 41 | `pepper that Arab traders from Muscat and Aden bid against the Dutch to buy, paying in silver *chuckrams* and gold *varahans* that fill the King's treasury` | dialogue_exposition; also `Pack your kit` and `pays for your salary` (P, H, register audit) | "“Go then. Gather your things. The cart is waiting. Try not to offend her. Half the pepper that pays your wages comes off her hills.”" |
| 47 | `Not one of the great stone temples I knew from the Deccan` ... `This place had no towering spires, no massive gateways.` | correction opener; stock intensifiers (P, H) | "In the Deccan a temple is stone, with a tower you can see from half a day's ride. This place sprawled low and wide beneath the palms, its tiled roofs sloping, its carved wooden beams dark with oil and age." |
| 47 | `Yet everything about it said power.` | kicker: a thesis sentence (P, H) | Cut. |
| 47 | `shifting their weight like grey boulders` ... `defend its wealth, not just display it` | simile_stack (boulders do not shift their weight); correction (P, H) | "Two tuskers swayed in the shade of the compound wall, and Kayal did not like them. From a long stable came the smell of more horses than any farmer needs." (A cavalryman counts the horses and watches his own mare; the reader draws the conclusion.) |
| 49 | `Power in the neatness of the courtyards` ... `like quiet promises` ... `where cool air and authority met` | fragment_list (anaphoric "Power in" triple); abstract simile; zeugma (P, H) | "The courtyards had been swept before dawn. The granary walls were as thick as a fort's, with paddy heaped inside to the roof. The men with spears stood back in the shade of the inner verandahs, where a visitor would not see them until he was among them." Place this after line 53 (see Chapter-specific notes on sequence). |
| 51 | `It looked like nothing. That was what made it feel important.` | kicker: a signpost on a plant (P, H) | "In the shadow near the granary was a low wooden panel that looked like nothing, except that its edges were rubbed smooth, as if fingers had found it in the dark." Keep "looked like nothing": ch16:109 echoes it ("looked like nothing more than a repair panel"). Only the signpost goes. |
| 55 | `It belongs to the name on the matrilineal line.` | modern_register: 20th-century anthropology word (REGISTER P1); pre-empts 101 (P, H) | Cut the sentence. "Here, the house does not belong to the man who sleeps in the front room. You will see." Padmini's grandmother speech at 101 then pays it off. |
| 61 | `A stranger. A Maratha. A man who had washed up from Portuguese wreckage` | fragment_list; recap; "stretcher" is a 19th-century word (P, H, register audit) | Cut the paragraph. Line 59 already has their eyes settle on him. |
| 65 | `She was not young, but no one would have called her old.` | balanced_antithesis (P, H) | "She was past forty, I guessed, and her hair was still thick and black, left unbraided and coiled at the nape of her neck." |
| 65 | `not in great heavy chains, but in simple pieces that looked as if they had been worn for work as much as for ceremony` | correction; "as if" (P, H) | "She wore gold at her ears and throat, small plain pieces a woman could work in." |
| 65 | `Her sari was cotton, not silk, hitched up around her ankles` | correction; period dress (P, H) | "Her mundu was plain cotton, tucked up at the shin the way the women in the paddy wore theirs." (See notes on dress. Ch9:9 "She wore more silk than she had at home" still holds.) |
| 67 | `could have been a staff or a cane, depending on who held it` | balanced_antithesis; restated at 225 (P, H) | "She held a long stick of dark wood, as tall as her shoulder." This sets up the fixed 225. |
| 71 | `Not a deep court bow, but more than a nod to an equal.` | correction (P) | Cut. The Patil comparison already sets how deep the bow is. |
| 81 | `One corner of her mouth curved.` | stock_phrase: a cast-wide face tic (P, H) | Cut. "Good." carries the approval. |
| 89 | `took my gelding's reins. He handled the animal with an easy calm that spoke of long familiarity.` | stock_phrase ("spoke of"); continuity: Kayal is a bay mare (ch7:161) (P, H) | "A boy of perhaps twelve ran forward and took Kayal's reins. He let her smell his palm before he turned her, and she went with him after one snort." |
| 91 | `talking quietly` ... `tapping lightly against the stone` | soft_adverb (P, H) | "already talking with one of her stewards." ... "the stick tapping on the stone." |
| 93 | `He knows that understanding an estate is as important as understanding a charge.` | explained_subtext: states the chapter's thesis (P, H) | Cut. End her speech on "Clever man." Her questions at 97 make the point better. |
| 99 | `lips moving as if reciting something` | abstract_depth: a vague "something" (P) | "an elderly man with a thin white beard traced lines on a cloth map with his finger, counting under his breath." |
| 105 | `She tapped the floor with her stick.` | prop_tic: stick as punctuation (H, N) | Cut. The stick keeps 67, 85, 91 and 225. |
| 107 | `Or her. This is our way.` | modern_register: an inclusive-language self-correction; generic (P, H) | Cut both. |
| 107 | `through more kings than I care to count` | stock_phrase (P, H) | "It has kept pepper flowing and swords sharp since before this king's grandfather was born." |
| 109 | `worn smooth by generations of use` ... `steel ringing on steel` | stock_phrase (P) | "A stone platform sat under it, its edges rounded by years of sitting. From beyond a low wall came the crack of wood on wood and the grunt of bodies in practice." |
| 113 | `There was no threat in her tone. Only a statement of fact, laid on the ground like a tool.` | explained_subtext; "No X. Only Y."; stock simile (P, H) | Cut. |
| 115 | `The ease with which they moved, the way they did not avert their eyes from me, the way Padmini Amma accepted their presence without comment, all of it was different from what I had grown up with.` | explained_subtext: a triple gathered by a summarizer (P, H) | "She gestured for us to sit on the platform. A pretty girl brought water in brass tumblers. Another followed with a plate of sliced fruit and fried snacks, and looked me in the eye as she set it down." |
| 117 | `they moved like shadows at the edge` ... `Here they flowed through the centre, talking, laughing, listening in.` | simile_stack: a stock simile, a participle triad and an odd "men in armour" (P, H) | "In my village the women worked as hard as any man, at the well and in the fields. But when the men sat in the courtyard, the women set down the food and went back inside. These girls stayed within earshot, and listened." The Deccan contrast itself is protected (see Defended). |
| 129 | `The word tasted heavier than jackfruit.` | kicker: a synesthetic callback (P, H) | Cut. "“Yes,” I said. “Parents. A younger brother...”" |
| 137 | `Here it came like another test, dropped into the space between us.` | stock_phrase ("the space between us"); labels the test (P, H) | Cut. The first sentence stands. |
| 139 | `The life I chose did not lend itself to regular hearths` | modern_register: essay phrasing (P, H) | Cut the sentence. Open on "“I rode where the Peshwa's orders sent me,” I said." |
| 149 | `She studied me for a moment, then seemed to make a decision.` | stock_phrase: the pause before an info-dump (P, H) | Cut. Run 151 on from 147: "“I own this land,” she said. “Why should I not? You will hear a word here..." |
| 151 | `From the Sanskrit, *sama*, meaning equal, and *bandham*, meaning bond or alliance.` | dialogue_exposition: a dictionary gloss, and a false one (the prefix is *sam-*, together) (P, H, REVIEW_BACKLOG N-32) | "You will hear a word here. *Sambandham*. It is what we call the tie between a man and a woman." |
| 151 | `Not ownership. Not conquest. An alliance between equals.` | correction: "Not X. Not Y. Z." (P, H) | Cut. |
| 155 | `a woman leaves her father's house and enters her husband's. She becomes his. Her children are his.` | dialogue_exposition: she tells him his own custom, then asks "Yes?" (P, H) | Give the Deccan custom to Nagoji, in his own words: "“In the Deccan,” I said, “a wife goes to her husband's house. If he dies, she lives on his brothers' mercy.”" Cut 155 and 157. |
| 159 | `But he does not own the house. He does not own the land. He does not own her.` | tricolon: anaphora, after a second triple ("He visits. He may... He may..."); also a stick tap and "call it what you will" (P, H) | "A woman stays in her own house, her *tharavadu*. When she takes a husband, he comes to her. He may sleep in her room and father her children, but he does not own the house, or the land, or her." |
| 167 | `This is their home. This is where they will fight and die if the king calls.` | dialogue_exposition: a weaker repeat of 111 (P, H) | "She pointed toward the kalari. “Some of those boys have fathers who ride for other lords entirely.”" |
| 169, 171 | `I searched for the right word. “Complicated.”` ... `A man who goes to war may not return. A man who travels for trade` ... `In your system` | tricolon; sitcom setup and correction; modern "system" (P, H) | Cut 169 and the "A man who" triple. Keep one case: "“Here, if a man goes to war and does not come back, his wife and children are where they were before, in their mother's house, on their mother's land.”" |
| 179 | `Some women fall so deeply in love that they forget their own names.` ... `Into the streets, if they are not.` | stock_phrase: romance hyperbole; a mirrored pair; an urban idiom (P, H) | Keep only "“Then she is a fool,” Padmini Amma said. “But it happens.”" |
| 181, 183 | `*Sambandham* protects women by refusing to let them be owned.` ... `No man can take that.` | modern_register: a thesis in rights language; a triad; a slogan close (P, H) | Cut 181 and 183. Keep one clause and move it into the earlier speech: "Even Marthanda Varma, who changes many things, does not change that." |
| 187 | `The Brahmins have their own customs. The Namboothiris keep their women locked in their compounds. The Syrians marry in their churches.` | tricolon: padded (Namboothiris are Brahmins) (P, H) | "“Men accept what the land demands. Those who do not are welcome to find wives in your Deccan.”" (Her wit, aimed at him.) |
| 189 | `It was a challenge, not a question.` | correction: a kicker on the cast-wide tic list; also wrong, since she asked no question (P, H) | Cut. |
| 191 | `She leaned back, studying me.` | stock_phrase: choreography (P, H) | Cut. If a beat is needed before the billeting terms: "She finished the jackfruit." |
| 193 | `That makes you part of this house's story, whether you like it or not.` | modern_register: narrative abstraction (P, H) | Cut. The three billeting terms stand. |
| 195 | `She leaned forward, her voice dropping to a flat, hard tone.` | stock_phrase: labelled tone (P, H) | Cut. Go straight from the terms to the threat. |
| 197 | `If they try anything` ... `Do not test us on this.` | modern_register: thriller idiom (P, H) | "“And tell your men to keep away from the girls of this house. If one of them lays a hand on a girl here, we will carve him from navel to feet.”" |
| 203 | `You will meet one of those tongues soon.` ... `send a representative to a gathering` ... `If you truly want to understand this kingdom` | signposting; committee register (P, H) | "“The king has asked our Velinadu kin to send someone to a gathering,” she said. “They send a princess. Revathi Bayi. She has more opinions than I have pepper vines. Listen to her as carefully as you listen to Ramayyan.”" |
| 205 | `sharp tongued royal woman who refused to act grateful when Europeans bowed` | modern_register; missing hyphen (H) | "a sharp-tongued royal woman who did not smile when the foreigners bowed to her." |
| 209 | `Padmini Amma's expression shifted, just enough to be seen.` | stock_phrase: a face beat (P, H) | Cut. |
| 211 | `Not always the same thing as supporting its current occupant. You will discover this.` | modern_register: political journalism; a foreshadow tag (P, H, register audit) | "“She supports Travancore,” she said. “That is not always the same as supporting the man on its throne.”" |
| 213 | `A man who had carved power from a fractured land. In my world, such a man expected his nobles to fall in line or fall in the field.` | stock_phrase; "in my world"; wordplay antithesis (P, H) | Keep the first sentence of 213 (the king on his platform). Then: "In the Deccan, a man like that made his nobles kneel or buried them." |
| 217 | `Older than his throne. Older than his reforms. Older than Dutch and Portuguese ships on this coast.` | fragment_list: an "Older than" ladder; "reforms" is policy vocabulary (P, H) | "“The Velinadu line is older than his throne, and older than the first Portuguese sail on this coast.”" |
| 219 | `The thuds of feet, the hiss of breath, the smack of sticks training muscles to remember.` | tricolon: the third kalari-sound beat; "muscle memory" (P, H) | "Beyond the wall the sticks went on cracking." Or cut the paragraph. |
| 225 | `using the stick more as a symbol than as a support` | explained_subtext: interprets the prop (P, H) | "She rose without leaning on the stick." |
| 227 | `Look at how our men and women move through this house.` | explained_subtext: instructs the reader in the theme (H) | Cut. |
| 227 | `without putting your Deccan boot in your mouth` | modern_register: 19th-century idiom (P, H, register audit) | "After that, we will see whether you can stand in a princess's hall without trampling anything." (Her joke, built from her own previous sentence.) |
| 231 | `listening to the layered sounds of the estate` | abstract_depth (P, H) | Cut 231 to 243. End on 229 (see Ending). |
| 233 | `Here, power sounded like pepper being sifted, like a woman's stick tapping stone, like boys shouting in a training pit` | simile_stack; a Goa/Pune/Here tricolon; the "In Goa... Here" contrast is on the book-wide cut list (P, H) | Cut. A jackfruit also does not drop "into waiting hands". |
| 235 | `something less obvious and perhaps more dangerous` | abstract_depth (P, H) | Cut. |
| 237 | `A house that remembered. A house whose women spoke.` | fragment_list: a thematic button (P, H) | Cut. |
| 239 | `the Dutch drill manuals we captured from broken forts` | summary_ending: a moral, and a timeline error (no Dutch fort has fallen and no Dutch drill has been captured before Colachel) (P, H, REVIEW_BACKLOG C10-16, N-35) | Cut. |
| 241 | `Two days to learn how not to offend a princess.` | kicker: repeats 223; Ch 9 opens on the departure (P, H) | Cut. |
| 243 | `Somehow, this felt like the more delicate task.` | summary_ending: an ironic-understatement quip; "Somehow" is on the kill list (P, H) | Cut. |

## Borderline

13 items. Each has a preferred handling, but leaving it alone would not be an error.

| Line | Quote | Why borderline | Handling |
|:-|:-|:-|:-|
| 5 | `It was months of sun and salt.` | It is part of the T6 touchstone, but it restates "For months" and "It was months of" is loose. (P, H) | Take: "Those were months of sun and salt." Cutting it is also fine. |
| 7 | `But the king did not keep me only on the beach.` | A one-line hinge paragraph, but it carries a real shift from sand to inland fighting. (P) | Take: merge it into 9 as the first sentence and drop "But". |
| 9 | `who dared to whisper a rival claim` | The lyrical third item in a list whose first two are concrete ("paid tax", "temple key"). (P, H) | Take: "who paid tax and who held a temple key." |
| 9 | `A noble house whose gates had been shut too often.` | Vague (shut to whom?), but it belongs to a real campaign list. (P) | Take: "A noble house that had shut its gates on his tax men once too often." |
| 45 | `The first time I saw Padmini Amma's house, I thought they had brought me to a temple by mistake.` | The best hook in the chapter (H protects it), but Ch 7 opens with the same shape ("The first time I tried..."), so two chapters in a row do it. (N, OEM) | Author's call. Keep the thought. If the shape changes: "Padmini Amma's house sat low and wide under the palms, and at first sight I took it for a temple." 47 must then drop "sprawled low and wide". |
| 47, 53 | `sloping gently` ... `wicks smoking gently` | Two "gently" in six lines. (P) | Take: drop both. |
| 57 | `their bangles clinking softly` | Soft adverb ration. (P) | Take: "their bangles clinking." |
| 77 | `slow enough now that I could follow` | "now" implies an earlier fast speech that is not on the page. (N) | Take: "slow enough that I could follow." |
| 85 | `She gestured with the stick.` | The stick used as punctuation, but here it also moves the action ("Come."). (N) | Keep if 105 and 159 go. |
| 173 | `She smiled, showing teeth.` | A cast-wide tic that recurs at ch9:48 ("a flash of white teeth"). Here it marks a real turn from lecture to joke. (P, OEM) | Keep this one and cut ch9:48. |
| 199, 201 | `Houses have long memories` / `And longer tongues` | A scripted quip and riposte. Nagoji's line does not answer a threat against his men, but it is the hinge to Revathi and her reply is witty. (P, H) | Preferred: "“I will tell them tonight,” I said." Cut 201. Acceptable: keep both lines and cut only the signpost at 203 (Confirmed). |
| 217 | `You outsiders see one crown. We see many layered on the same land. Sometimes they sit well together. Sometimes they cut.` | Two mirrored pairs, but "Sometimes they cut." is a blunt, good close. (P, H) | Take: "You outsiders see one crown. We see many on the same land. Sometimes they cut." |
| 229 | `Men with account books stepped aside, then resumed their counts. A young girl carrying firewood paused to watch me for a heartbeat, eyes bright, then hurried on.` | Three matched "X, then Y" beats and stock "for a heartbeat, eyes bright", but the details are concrete. (P, H) | Take: cut both sentences, so the chapter ends on the first sentence of 229 (see Ending). |

## Defended (flagged, but keep)

29 items. Each was flagged by at least one auditor. Keep it because it does narrative work that a cut would lose.

| Line | Quote | Flagged by | Reason to keep |
|:-|:-|:-|:-|
| 5 | `laughing when a charger stumbled, nodding when a formation held` | P | Concrete and comic, seen from the boats. Part of Voice Bible touchstone T6. |
| 5 | `the foreign captain who yelled at horses` | P (kicker) | The best self-portrait in the book (Voice Bible 3.3, item 7, "Self-portrait from outside"). Only "part of the landscape" changes. |
| 9 | `A pepper hill that refused the king’s men.` (and the two fragments after it) | P | A campaign inventory, the kind of genuine count Voice Bible 6b protects. The chavers and the bund are real texture. |
| 9 | `Each time speed mattered, cavalry went first, and each time` | H | Plain soldier's logic. The repetition is how he reasons. |
| 11 | `Ramayyan said it once, flatly, as if it were a note on a palm leaf.` | P | Sums up Ramayyan in one stroke. To meet the one-"as if" ration, use "the way he would enter a debt on a palm leaf" and save the "as if" for the cellar panel. |
| 11 | `The Maharaja has seen you in blood, not only in sand.` | P | Ramayyan's line does the job the cut "kind of silence" sentence tried to do. It is one of only two dialogue "not" lines left in the chapter (with 223). |
| 15, 25 | `He did not look up from his palm leaves as I entered.` / `Ramayyan finally looked up.` | P | He looks up at the caste question, not at the soldiering. That is the point of the scene, and the palm leaves are his one signature prop. |
| 19, 21 | `I prefer the sky` / `Preferences are luxuries` | H | Ramayyan's dry accounts register at its best. The exchange is short and in character. |
| 23 | `I had heard the name. The woman who owned pepper hills.` | P | Plain. A colon would do if wanted. |
| 25 | `His gaze was like a clerk’s scale, weighing gold against brass.` | P, H | A simile from his money world, and gold against brass is exactly the caste assay that follows. The Voice Bible cites it. It is the chapter's one "like" simile. |
| 37 | `Padmini Amma might tolerate a foreign captain, but she will not tolerate pollution.` | H | An unsentimental period attitude in Ramayyan's clipped voice. |
| 63 | `At the far end of the courtyard a woman stood.` | P | A plain entrance. One inverted line is not a tic. |
| 75 | `Her gaze travelled from my feet to my face.` (and the inventory) | P, H | The details (linen-wrapped hands, the brand under the sleeve, the worn belt) are exact, and they show a landholder sizing up a hired sword. Optional: "She looked me over from feet to face." |
| 97 | `Who feeds the men you count? Whose pepper pays for their powder?` | P | Her tally set against his. The chapter's argument is made by a character in dialogue, not by the narrator. |
| 99 | `I smiled at the women a bit longer than I should have.` | P (register) | A human flaw with no moral attached. It quietly sets up the threat at 197. |
| 101 | `The men come and go. The name stays here.` | P | Earned by the gossip (the dancer, the sons). Once the lecture is cut, this is the chapter's main statement of the principle. |
| 107 | `If your son's wife hates you, does that field still feel like safety?` | P (register) | Domestic, pointed and funny, and it argues through an image rather than a principle. Optional: "still keep you safe". |
| 111 | `Sticks, swords, dagger.` | P | A spoken inventory. |
| 111 | `When the king calls, they are ready. When the king forgets us, they are also ready.` | P | Menace by repetition. It is why 113 can go. |
| 117 | the Deccan contrast itself (women at the edge at home, in the middle here) | P | The Voice Bible cites it as how he sees the Nairs, measured against his own village. Only the phrasing changes (Confirmed). |
| 119 | `a spear for his hand or a knife that might cut it` | P, H | Her weapon image, and the only either/or in her speech. |
| 163 | `The father is honoured, yes. Loved, often. But he is a guest in the house where his children grow.` | P | The best line in the lecture. It goes into the condensed version unchanged. |
| 163 | `They inherit from her brothers, not from their father.` | P | Information, not a correction tic. |
| 175 | `We do not pretend men are reliable, Sawant. We plan for their failures.` | P (register) | The Voice Bible's example of Padmini at her best (her voice speaks through grain, pepper, household and threats). |
| 193 | `Your horses will graze in our fields. Your men will eat from grain we grew. You will ride from this gate when the king calls.` | P (tricolon) | The billeting terms. Concrete, and in her currency. |
| 203 | `She has more opinions than I have pepper vines.` | P | A measure in her own currency. It introduces Revathi Bayi in one line. |
| 217 | `He allows what he cannot easily stop` ... `until he broke them` | P | Real history said plainly. It plants the king's boyhood in the cellar (ch17:67 to 73). |
| 223 | `You will come as my guest, not as the king's experiment. That will confuse people. Confusion is useful.` | P | Her politics in three sentences, with a callback to ch6:167 ("You are an experiment"). It is the chapter's allowed dialogue "not X". |
| 229 | `As she walked away, the women in the courtyard parted without being told, then closed again behind her.` | P (tricolon) | The best image in the chapter, and the new last line. |

Also not an error, in case someone flags it: at 93, "near his capital and his horse" uses *horse* in the period collective sense (the king's cavalry).

## Opening

Current first lines (3 to 5):

> For months I lived near the fishermen’s village, sleeping on a mat in a small hut that smelled of dried prawns and damp thatch.
>
> It was months of sun and salt. My days were spent on the wet sands, shouting until my throat was raw...

**Verdict: keep, and trim lines 5 to 13.** Line 3 is concrete and in voice (the OEM audit keeps it too). Line 5 is Voice Bible touchstone T6, so do not open cold at the ola (13), as the holistic reader suggests as an option. That would lose one of the fifteen passages the whole edition is meant to sound like. The fault in the opening is not that it is a summary. The trouble is that its frame is written in the chapter's slop register: "part of the landscape", a hinge paragraph, "never reached European maps", the reins that do not care, and "a different kind of silence, the kind that...". With those gone, the montage runs about 270 words (from 290) and the first scene starts at line 13. The opening is barely cut: the fix is in the phrasing, not the length.

Trimmed 3 to 13, as tested:

> For months I lived near the fishermen’s village, sleeping on a mat in a small hut that smelled of dried prawns and damp thatch.
>
> Those were months of sun and salt. My days were spent on the wet sands, shouting until my throat was raw, trying to make Madurai horses and Maravar ponies understand each other. The fishermen watched us from their boats, laughing when a charger stumbled, nodding when a formation held. I ate their fish curry, spicy enough to make a Deccan man weep for milk, and drank their toddy. I became, in a small way, one of the sights of that beach: the foreign captain who yelled at horses.
>
> The king did not keep me only on the beach. There were inland fights too, small wars that no clerk in Pune would ever write down, though they decided who paid tax and who held a temple key. A pepper hill that refused the king’s men. A noble house that had shut its gates on his tax men once too often. A band of *chavers*, men sworn to die for their lord, sent to make an example of an official on a narrow bund between paddy fields. Each time speed mattered, cavalry went first, and each time I found myself at the head of it, shouting orders in broken Malayalam, the salt still in my hair, my bandaged fingers clenched on the reins.
>
> We came back with cuts and missing men. Ramayyan said it once, flatly, the way he would enter a debt on a palm leaf. “The Maharaja has seen you in blood, not only in sand.”
>
> Then the King's ola came, calling me to a small pavilion near the temple.

The section opener at 45 is the chapter's real hook. See Borderline for the "The first time I..." echo of Ch 7.

## Ending

Current last lines (239 to 243):

> If I was to survive this southern kingdom, I would have to learn its female tongues as carefully as I learned the Dutch drill manuals we captured from broken forts.
>
> Two days to learn how not to offend a princess.
>
> I had faced Portuguese interrogations and Arabian Sea storms. Somehow, this felt like the more delicate task.

**Verdict: revise (cut).** Lines 231 to 243 stack five closing moves after the image at 229: a summary tricolon, a vague abstraction, a fragment-pair button, a moral with a timeline error, and a quip. The "two days" repeats 223, and Ch 9 opens with the departure, so no bridge is needed. Three book-level rules are broken here at once: the "In Goa... Here" contrast, "If I was to survive... I would have to learn", and the figurative storm are all on the OEM cut lists.

Proposed ending. Cut the last two sentences of 229 and everything from 231, so the chapter closes on her exit:

> She rose without leaning on the stick.
>
> “Rest now,” she said. “Wash the salt from your skin. Tomorrow we walk the fields. I will show you where your horses will chew and where they will trample. After that, we will see whether you can stand in a princess's hall without trampling anything.”
>
> As she walked away, the women in the courtyard parted without being told, then closed again behind her.

Why this line: it shows her authority purely through movement. Nagoji is the one watching, and the circle closes behind her without him in it. No new prose is invented.

Alternatives I considered:

- **The OEM proposal** (a jackfruit splits on the stone at his feet, "No one came for it but the crows") is a fair image. But a fruit that size falling beside a seated man is a new event and reads as a near miss, and a household this careful with grain would not leave a fallen jackfruit to the crows.
- **A coda at the stable with Kayal** would repeat the OEM's proposed Ch 7 ending (Nagoji alone with Kayal at night). No two chapters may share a closing idea.
- **An optional coda, if the author wants the chapter to end on Nagoji.** He carries out her order: "I sat under the jackfruit tree until the lamps were lit. Then I went down to the stable, where my men were rubbing down the horses, and gave them Padmini Amma's warning in her own words. / “From the navel?” one of them asked. / “To the feet,” I said." This is new text. Use it only if the bare ending feels too abrupt.

## Flab (passages to tighten)

| Lines | Words now | Issue | Target |
|:-|:-|:-|:-|
| 5 to 11 | 266 | The montage frame is carried by slop phrasing, not by summary as such. | About 245. Keep T6, the fragments and Ramayyan's line (see Opening). |
| 35, 37, 41 | 127 | Explanation after the caste test; a trade-and-coin lecture on the way out. | About 75. |
| 47 to 51 | 195 | "Power" as a thesis, then three "Power in" fragments and a signpost on the panel. | About 150. Keep every concrete observation: tuskers, long stable, swept courtyards, thick granary, spearmen placed inside, the panel. Move 49 and 51 after 53 (see notes). |
| 59 to 61 | 58 | Recap of who Nagoji is. | Cut 61. |
| 65 to 71 | 143 | Three corrections in one paragraph, an either/or stick and a calibrated bow. | About 100 (see Confirmed). |
| 105 to 117 | 266 | A stick beat, a tone gloss (113) and a sociological summary (115) around a good contrast (117). | About 205. |
| 149 to 197 | 693 | The *sambandham* lecture (see below). | About 320. |
| 199 to 219 | 316 | Signposts (203, 211), face beats (209), stock epic phrasing (213), a fragment ladder (217) and a third kalari-sound beat (219). The content (Revathi, the king's limits, the Eight Houses) all stays. | About 230. |
| 225 to 243 | 285 | The prop gloss, the theme instruction, and the stacked close. | About 70 (see Ending). |

Condensed 147 to 197 as tested in the scratch pass (about 320 words, down from about 700). It keeps every fact in the original except the "law, temples, kings" triad: she stays in her *tharavadu*; the husband visits, fathers children and owns nothing; the children inherit from her brothers; the father is a guest with his own sisters' children to think of; the fathers of the kalari boys may ride for other lords; a widow is safe; women who follow husbands are fools; the king does not change it; the billeting terms; the threat. Nagoji supplies the Deccan custom himself, so she no longer tells him his own ways, and his prompts drop from four to two (REVIEW_BACKLOG C10-15).

> “I own this land,” she said. “Why should I not? You will hear a word here. *Sambandham*. It is what we call the tie between a man and a woman. A woman stays in her own house, her *tharavadu*. When she takes a husband, he comes to her. He may sleep in her room and father her children, but he does not own the house, or the land, or her. The children belong to her line. They inherit from her brothers, not from their father. The father is honoured, yes. Loved, often. But he is a guest in the house where his children grow. He has his own *tharavadu*, and his own sisters' children to think of.”
>
> She pointed toward the kalari. “Some of those boys have fathers who ride for other lords entirely.”
>
> “In the Deccan,” I said, “a wife goes to her husband's house. If he dies, she lives on his brothers' mercy.”
>
> “Here, if a man goes to war and does not come back, his wife and children are where they were before, in their mother's house, on their mother's land. Even Marthanda Varma, who changes many things, does not change that.” She smiled, showing teeth. “We do not pretend men are reliable, Sawant. We plan for their failures.”
>
> “And if a woman wishes to follow her husband to his house?”
>
> “Then she is a fool,” Padmini Amma said. “But it happens.”
>
> “And men accept this?”
>
> “Men accept what the land demands. Those who do not are welcome to find wives in your Deccan.”
>
> She finished the jackfruit.
>
> “You will be billeted here for a time,” she said. “Your horses will graze in our fields. Your men will eat from grain we grew. You will ride from this gate when the king calls. And tell your men to keep away from the girls of this house. If one of them lays a hand on a girl here, we will carve him from navel to feet.”
>
> “I will tell them tonight,” I said.

The one triple left ("the house, or the land, or her") is the lecture's single principle, and it stays in her mouth.

## Passages to protect

Keep these verbatim, or change only the word noted.

- **5** The T6 touchstone. Only "part of the landscape" changes.
- **9** The campaign fragments: the pepper hill, the shut gates, the chavers on the bund, "who held a temple key".
- **11** "The Maharaja has seen you in blood, not only in sand."
- **17 to 21** "The King is pleased with the sand... useful indoors as well." / "I prefer the sky." / "Preferences are luxuries."
- **25** The clerk's scale weighing gold against brass.
- **27 to 33** The caste check, ending on "We do not plough." (See notes for the conflict with ch19.)
- **37 to 39** "If you were low-caste, we would have to billet you in the stables..." / "He scratched a note on his leaf."
- **45** "I thought they had brought me to a temple by mistake." (The thought, whatever the sentence shape.)
- **51** The panel sentence, including "looked like nothing" and "as if fingers had found it in the dark". It plants the cellar of Chs 16 and 17.
- **53** Oil lamps lit at midday, scenting the air with burnt ghee.
- **57** The courtyard at work: pepper on mats, boys with short spears, the old man barking corrections.
- **73 to 83** "The sea spits out strange things." (the book's one keeper of that motif) and the insulted/measured exchange.
- **95 to 97** "I count men, hooves, distances." / "Whose pepper pays for their powder?"
- **99** "I smiled at the women a bit longer than I should have."
- **101** The grandmother, the dancer, the sons, "The men come and go. The name stays here."
- **103 to 107** The Deccan field against the son's wife.
- **111** "When the king calls, they are ready. When the king forgets us, they are also ready."
- **119 to 125** Spear or knife; "I am still an experiment"; "He is honest, then"; the jackfruit juice on her fingers.
- **129** "Some fields that do not know whether I am alive."
- **141 to 147** "You assume she would wait"; "I own this land... Why should I not?"
- **163, 175, 179** "a guest in the house where his children grow"; "We do not pretend men are reliable"; "Then she is a fool."
- **197** "we will carve them from navel to feet" (only the idiom around it changes).
- **203** "She has more opinions than I have pepper vines."
- **213** The first sentence: the king on his low platform, spear at his shoulder, maps at his feet.
- **217** "He allows what he cannot easily stop"; the Eight Houses "until he broke them"; "Sometimes they cut."
- **223** "Confusion is useful."
- **227** "where your horses will chew and where they will trample."
- **229** The women parting and closing behind her.

## Chapter-specific notes (continuity and history)

**Continuity**

- **The horse (REVIEW_BACKLOG N-03).** Line 89 says "my gelding", but Ch 7 gives him Kayal, a bay mare (ch7:161, 175, 183). The fix names Kayal at 47 and 89. This is part of the book-wide horse decision (Kanka, Kayal, Megha). Settle it once, then apply it here.
- **Ibrahim dismounts twice.** Everyone dismounts at 59, then Ibrahim speaks "dismounting" at 73. Cut "dismounting".
- **The arrival is out of order.** Line 49 describes the swept courtyards, the granary and the spearmen "under the shade of the inner verandahs", and 51 the panel "near the granary", before they ride in under the arch at 53. Move 49 and 51 after 53 (or after 57), so he sees the inside once he is inside. The fixed 49 ("where a visitor would not see them until he was among them") depends on this.
- **The cellar plant.** Ch 8 puts the panel "in the shadow near the granary"; ch16:109 has the door "through the storeroom, past the great clay vessels of rice... in the corner"; ch17:71 says "Beneath the granary". These are compatible. Keep the phrase "looked like nothing", which ch16:109 echoes.
- **"We do not plough" (33) against ch19:115** ("my father, his back bent over a plough") and ch21:47 ("father (farmer)"). REVIEW_BACKLOG N-22 suggests "We hold the sword and the plough both". I advise against that. The line is his answer to a caste test and the truest Maratha note in the chapter, and it can stand as a proud boast. Either fix ch19 and ch21 to match it, or let the later plough quietly expose the boast. Author's call.
- **"The King" and "the king".** Capitalised at 13, 17 and 41; lower case everywhere else. Pick one for the book.
- **Name slip.** "Padmini" for "Padmini Amma" at 163 and 179, only inside the lecture block, which suggests the block was drafted separately. The condensed version fixes both.
- **Smile tic.** "She smiled, showing teeth" (173) and ch9:48 "She smiled, a flash of white teeth". Keep this one and cut Ch 9's.
- **Stick.** 7 uses as a gesture in this chapter. After the edit, 4 remain (67, 85, 91, 225). The OEM plan keeps the stick as her signature, with this chapter as its introduction.
- **"It was not a question" family** (189): on the cast-wide cut list, and here it is also inaccurate. Cut.

**History and period**

- **Dress (65).** A Nair woman of 1740 wore the *mundu*, with a *neriyathu* over the shoulder when she chose to. The sari is later and generic. Ch 9 ("She wore more silk than she had at home") needs cotton at home, which the fix keeps.
- **The etymology (151, REVIEW_BACKLOG N-32).** *Sambandham* is *sam-* (together) plus *bandha* (binding), not *sama* (equal). Cut the gloss. "An equal bond" also imports a modern egalitarian reading.
- **Coins (41).** Arab traders would pay in their own silver or in Venetian gold, not in Travancore's local *chuckrams*. Cutting the clause removes the problem. If the coin names are wanted for texture, use them where the treasury is local, not in a foreign merchant's purse.
- **Temple priests as cooks (37).** Brahmin cooks in Nair houses were usually Pottis or Tamil Brahmins, not temple priests. Safer: "That will satisfy the Brahmins who cook in her kitchen."
- **Brahmins and Namboothiris (187).** The Namboothiris are Kerala's own Brahmins, so the list overlaps. If "The Brahmins" means the Tamil Pattars, say so. The fix removes the list.
- **The Eight Houses "on the marches" (217).** The historical Ettuveetil Pillamar held villages around Thiruvananthapuram and the temple, not on the frontier. But the novel already places them on the marches elsewhere: ch21:62 "Eight Houses of the Marches", and ch22:269 "One of the old Eight Houses", tied to the Kayamkulam frontier. Ch 17 calls the lords who hunted the boy king "the Pillamar". This is a book-wide decision. Do not change ch8 alone, or it will contradict Chs 21 and 22. Keep "until he broke them" either way, since it plants ch17:67 to 85, where the Pillamar's men killed Padmini's son and husband.
- **Chavers (9, REVIEW_BACKLOG C10-41).** First use, set in roman and unglossed. The fix italicises it and adds a short gloss ("men sworn to die for their lord"). The later gloss at ch23:427 can then go.
- **Dutch drill before Colachel (239, REVIEW_BACKLOG N-35).** No Dutch fort had fallen by 1740, and de Lannoy's drill comes after 1741. The line is cut with the ending.
- **"Matrilineal" (55)** is a 20th-century word (REGISTER P1). It is cut. The same word recurs at 17:111, 21:69, 25:144, 27:101 and 27:145, so use the same replacement across the book ("the law of the mothers", *marumakkathayam*).
- **Register items folded into the fixes:** "Pack your kit" and "salary" (41), "stretcher" (61), "system" (171), "current occupant" (211), "reforms" (217), "muscles to remember" (219), "boot in your mouth" (227), "Europeans" and "act grateful" (205).

**Copyedit (not slop, fix in the same pass)**

- 87: the closing quotation mark is missing after "Leave the horses to the boys."
- 101: "nodding toward the room in th house". Cut the clause, since "that room" already points.
- 55: straight double quotes in a chapter otherwise set with curly quotes. Apostrophes are mixed (curly at 3, 9, 25, 33; straight at 13, 41, 45 and elsewhere), as in F12-03.
- 205: "sharp tongued" should be "sharp-tongued".
- 183: a comma splice ("The kings say it, even Marthanda Varma... does not change that"). The line is cut in the condensed version.

**Maratha texture (optional, author's call)**

The holistic reader notes that the Deccan in this chapter is abstract ("Pune... silk and pearls"). The fixes add a little in place of cut abstractions: the Deccan temple seen from half a day's ride (47), the granary as thick as a fort's (49), his own village's women (117), the Deccan king who makes nobles kneel (213), and "find wives in your Deccan" (187). If the author wants one more, the natural place is 47, measuring the tharavadu against a deshmukh's stone *wada*. That would be new text and is not needed.
