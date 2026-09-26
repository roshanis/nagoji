# Second-Edition Audit: Chapter 18, Dutch Come Bowing

- Source (frozen first edition): `book1_horse_servant/book3_chapter18_dutch_come_bowing.md`, 269 lines, 2,651 words by `wc` (2,643 in SOURCE_OF_TRUTH's count). The chapter file and the EPUB text are identical here.
- Line numbers are physical lines in that file, blank lines included. `manuscript/` does not yet hold a copy of this chapter. A fresh copy will match these numbers until its first edit, so apply the fixes from the bottom up.
- Method: I read the chapter in full and ruled on every flag from the pattern auditor (79 flags) and the holistic reader (22 suspect passages, 22 protected passages, 21 flab notes), merging duplicates. I checked the passages this chapter plants or pays off in Chs 9, 10, 11, 12, 15, 16, 17, 19, 20, 21 and 28, and the book-level audits (`OPENINGS_ENDINGS_MOTIFS.md`, `REGISTER_AND_ANACHRONISM.md`, `REPETITION_AND_DENSITY.md`, `VOICE_BIBLE.md`, `REVIEW_BACKLOG.md`, `SOURCE_OF_TRUTH.md`). I ran `audit/tools/scan_slop.py` on the chapter. To test the cut estimate, I applied every confirmed fix plus the "take" borderlines to a scratch copy outside the repo and rescanned it.
- Source tags in the tables: **P** = pattern auditor, **H** = holistic reader, **N** = new in this pass.

## Verdict

| Measure | Call |
|:-|:-|
| Severity | **4 of 5** |
| Recommended intensity | **Medium** (tics plus tightening), with the heaviest edit of any chapter audited so far. About two thirds of the confirmed fixes are straight cuts. Line-level re-voicing is limited to the opening (3 to 19), the envoy's diction, the threat block (103 to 127) and Nagoji's reaction to the Pune news (241). |
| Estimated word cut | **About 30%** (2,651 to about 1,850 words). The scratch pass with every confirmed fix plus the "take" borderlines came to 1,846 words (30.4%). |
| Scanner, before and after the scratch pass | not-X-but-Y 2 to 0; "Not" openers 2 to 1 (235, kept); "as if" 4 to 1; soft adverbs 4 to 1; one-sentence paragraphs 45 to 26; short paragraph-final kickers 8 to 3; verbless fragments 11 to 4 (three are treaty clauses); triads 1 to 0; narration questions 1 to 0; "hung in the air" 1 to 0; "somewhere" 3 to 1; "jaw" 2 to 1; eye verbs 5 to 2; "long moment" 1 to 0 |

The scanner ranks this chapter mid-table (tic index 1.00, 14th of 28), but it undercounts badly here. Most of the chapter's slop is in its structure and dialogue, where the scanner cannot see it. That is why I rate it 4 and not 3.

The chapter's bones are good. A chastened embassy is received with protocol that humiliates it: Ramayyan will not touch their paper, and the king refuses the alliance clause. De Lannoy meets his old masters, the verandah counts the cost, and a late summons turns the book north. Several exchanges are as good as anything in the book: "You were told many things... Some of them were true." (37), "Read," (63), "I have work... Men here do not waste tools." (169), "Paper burns... Land remembers." (193), "Not Dutch... North." (235). The slop gathers in five places:

1. **The opening (3 to 13).** It uses a "less of X, more of Y" smell, "some time", two "Long enough for" paragraphs, the stock "heard of them before we saw them", and a three-location rumour montage with a Catholic confession in a Hindu temple.
2. **The threat block (103 to 127).** This reads as machine-written: "something flickered", "He did not need to.", a three-camera reaction pan, "The words hung in the air like smoke", "The threat was clear." plus a fragment list, a forward reference to Ch 21's ledger, "very still for a long moment" and "his voice was calm". The threat itself is delivered three times.
3. **The thesis, guns against paper.** It is stated about eight times (15, 19, 189, 193, 207, 211, 215, 247). Keep two, 15 and 189, and let Revathi's "Paper burns" (193) and Nagoji's second copy (new 215) act it out.
4. **Aphorism ping-pong.** "Small victories add up" / "So do small betrayals", "treaties or obituaries", "It makes life interesting". Everyone in the chapter speaks in the same mirrored epigram. Keep one epigram per speaker per scene.
5. **The close.** The chapter ends four times: Revathi's sermon (207 to 215), the summons (219), Ramayyan's "bring it to me" (261), and a coda made of a title-drop, a maxim and a weather omen (265 to 269).

Two habits run through every scene. The first is stock body business: Ramayyan's stylus reacts at nine points, and there are seven eye beats, two tightened jaws and two careful expressions. The second is dialogue tags in a hush: softly twice, quietly, murmured twice, under her breath.

## Confirmed issues

62 rows, in text order. Several merge flags from both auditors.

| Line | Quote | Category | Suggested fix |
|:-|:-|:-|:-|
| 3 | "The second time Dutchmen entered the coastal hall, they smelled less of salt and more of caution." | balanced antithesis opener; abstract noun given a smell; "The second time..." template (OEM 29) (P, H) | "The Dutch came back to the coastal hall two monsoons after Colachel." (Check the monsoon count against the date, Notes 1.) |
| 5 | "It had been some time since Colachel." | vague time marker (P, H) | Cut. The new line 3 carries the date. |
| 7, 9 | "Long enough for new walls to rise... into places where men in powdered wigs frowned over them." / "Long enough for Batavia to send new instructions." | anaphora; tricolon; stock caricature (ch11:183 gives the envoys tied-back hair, not wigs); standalone kicker (P, H) | Cut both. The envoy names Batavia's instructions at 49 to 53, and Ch 16 has shown the new walls and muskets. |
| 11 | "We heard of the envoys before we saw them." | stock transition (P, H) | Cut. |
| 13 | "In the markets... In the backwaters... In the temples, priests heard confessions from men who... feared they had backed the wrong god." and "Yusuf Marakkar in particular always seemed to know a little more than he said, his comments about company moods shaped like bait." | rumour montage no single observer could see; confession is a Catholic sacrament (REGISTER 18:13); a pun on "backed the wrong horse"; stock "knew more than he said" tag (P, H) | "Yusuf Marakkar had the news first, and sold it to Ramayyan a spoonful at a time, the way he sold everything. Dutch factors at Kochi were counting their coins twice. Company captains no longer pressed the small chiefs for pepper at the old prices. On the backwaters the boatmen said the company landings had gone quiet, and fewer of the men in them carried muskets." (Yusuf stays; see Defended.) |
| 15 | "Not with drums, this time. With papers." | "Not X. Y." The style sheet allows one, in dialogue, and 235 has the better claim (P) | "“They will come,” Ramayyan said one morning, tapping a palm leaf with his stylus. “With papers, this time.”" |
| 17 | "He was right." | filler kicker (P, H) | Cut. |
| 19 | "their coats were more subdued... Their lace was less ostentatious, their hats held more humbly... as if they hoped paper could balance scales that guns had tipped." | comparative triad; "ostentatious" is not Nagoji's word; the as-if clause explains the thesis four lines after Ramayyan said it (P, H) | "When they came, their coats were plainer than the ones that had strutted in this hall before the battle, with less lace at the cuffs. Behind them walked scribes carrying thicker bundles than before." |
| 23 | "I stood further in to the right of the King’s platform. I was no longer the mercenary observing from the pillars. I was the *Valia Karyakkar* of the Horse... The guards knew it, the ministers knew it, and from the way the Dutch envoys’ eyes lingered on me... I was a man with a *tharavadu* now, and that gave me a weight that mere steel could not." | "no longer X. I was Y." formula; escalating triad; mind-reading; abstract "weight" kicker; capital "King’s" and curly apostrophes (P, H) | "I stood nearer the king's platform than I had ever stood, on its right hand, as *Valia Karyakkar* of the Horse. The silver chain of office Padmini Amma had fastened round my neck that morning was heavier than it looked. The envoys' eyes went to it, then to my face, and I watched them work out that the “Maratha” had found a permanent stall in this stable." (The chain's literal weight sets up Revathi's joke at ch19:169.) |
| 25 | "not the one he had surrendered at Colachel, but a similar blade" | not-X-but-Y in narration (P). The content is protected (H). | "A sword hung at his side, the same pattern as the one he had surrendered at Colachel, its hilt wrapped now in local cloth." |
| 29 | "For a heartbeat, their careful expressions cracked. Then they recovered, faces smoothing." | stock micro-expression beat (P, H) | Cut. "faltered" (27) is enough. |
| 31, 33 | "the senior envoy said in Dutch, bowing slightly." / "What had they been told? That he was dead. That he was rotting in some dungeon. That he had been shipped off to another colony." | POV: Nagoji reports Dutch word for word here and at 167 to 179 (backlog N-48); "bowing slightly" copies ch11:187 and spends the chapter's one bow on De Lannoy; narration question plus a three-fragment answer (P, H, N) | 31: "“Captain De Lannoy,” the senior envoy said in Dutch. “We were told...”" 33: "He trailed off. I had no Dutch beyond a few drill words. Lannoy gave me the rest that night, with what passed between them after the audience." (One sentence covers both Dutch exchanges.) |
| 35 | "Their eyes took in the sword at his side, the way... the way Ramayyan's gaze flicked to him with approval rather than suspicion." | catalogue; "X rather than Y"; eye beat (P, H) | Cut. Lannoy's reply at 37 already covers it. |
| 39 | "ceding the centre of the hall, making it clear that he was not the one they had to address." | explained gesture (P, H) | "He stepped back and left them the centre of the hall." |
| 41 | "If he felt any satisfaction at the sight of Dutchmen forced to greet one of their own as a subordinate in his court, he did not show it beyond the smallest narrowing of the eyes." | "If he felt X, he did not show it" formula; the eyes narrow again at 109; "subordinate" (P, H) | Cut this sentence. Keep the one before it (Protect). |
| 43 | "“Maharaja,” the envoy said in careful Portuguese, then through a Malayalam interpreter, “the Honourable Dutch East India Company conveys its formal regrets for the unfortunate conflict at Colachel and wishes to restore relations based on mutual advantage.”" | "Honourable" is the English Company's style and "Dutch East India Company" is an English name (REGISTER 18:43); modern diplomatic register; the delivery is muddled. Also, no Dutchman bows to the king anywhere in a chapter called "Dutch Come Bowing" (P, H, N) | "The envoy bowed to the platform, lower than any Dutchman had bowed in this hall before. He spoke in Portuguese, and the interpreter gave it again in Malayalam." New paragraph: "“Maharaja, the Company conveys its formal regrets for the unfortunate conflict at Colachel, and wishes to return to friendship and trade, to the profit of both.”" Change ch11:187 ("The Honourable Company") in the same pass. |
| 51 | "Ramayyan asked softly." | hush tag; one of four soft adverbs (P) | "“By whose instruction?” Ramayyan asked." |
| 65 | "Terms unrolled in the air." | decorative abstraction (P) | Cut it. The paragraph becomes: "The scribe read aloud in Portuguese, the interpreter trailing him in Malayalam." |
| 67 | "...at agreed prices. This was the Treaty of Mannar, a first step, though Ramayyan called it “only a pause for breath.”" | a historian's label mid-scene (H); no piracy clause is read, yet Revathi answers one at 69 (backlog N-45); contradicts 153 and 157 (P, H) | "...at agreed prices. Joint action against pirates on this coast." Move "a pause for breath" into Ramayyan's mouth at 157. (Mannar: Notes 2.) |
| 73 | "We propose a joint commission... Representatives from your court and ours." | modern institutional vocabulary (H) | "“We propose that men of your court and ours sit together,” he said, “and judge such matters between them.”" |
| 75, 77 | "Ramayyan's stylus scratched a note." / "“Interesting.”" | stylus reaction shot (OEM 205 allows one per chapter); modern one-word capper, echoed by the king's "It makes life interesting" at 129 (P, H) | Cut 75. At 77, end the line at "criminals" and change "he said" to "Ramayyan said", since 75 is gone. |
| 81 | "in the event of other European power encroachment." | a clerk's modern English (H) | "should any other European power press upon this coast." |
| 85 | "After you tried to land soldiers on my beach without permission." | the king makes the "land on my shore" point three times (45, 85, 129) (H) | Cut the second sentence. 89's "break my spine" is the better sting. |
| 87 | "We would like stability... We prefer to be your trading partners rather than your enemies." | modern economics vocabulary (REGISTER 18:87) (H) | "“We would like quiet on this coast,” the envoy said. “Your kingdom has proven that it can resist outsiders. We would rather be your partners in trade than your enemies.”" ("Partners" stays for the king's echo at 89.) |
| 93, 95 | "“You offer recognition,” Ramayyan said, tapping the air with his stylus. “You offer trade. You offer to pay..." / "“Yes,” the envoy said." | recap of terms just read aloud; "You offer" anaphora; stylus tic (P, H) | Cut both. |
| 103 | "The envoy paused, and something flickered behind his careful expression." | vague interiority (backlog CL-12); doubles "The envoy hesitated" (99); "careful expression" repeats 29 (P, H) | Cut. |
| 105 | "his tone shifting to something almost casual... share the Maharaja's... enthusiasm for consolidation." | hedged "something almost"; villain's ellipsis; historian's word (REGISTER 18:105) (P, H) | "“We are also aware,” the envoy went on, in the voice of a man mentioning the price of rice, “that not all houses on this coast share the Maharaja's appetite for his neighbours' lands. There are those who remember older arrangements. Older claims.”" |
| 107 | "He did not look at anyone in particular. He did not need to." | machine kicker (six in the book, OEM 240) (P, H) | Cut. |
| 109 | "Ramayyan's stylus stopped moving. Marthanda Varma's eyes narrowed by a fraction. Revathi's hand, resting on her knee, curled into a loose fist." | a three-shot reaction pan (P, H) | "Ramayyan's stylus stopped moving. Beside Padmini, Revathi's hand closed on her knee." This is the chapter's one stylus reaction. Revathi's hand matters because the "older claims" are her kin (ch9:146). |
| 111 | "Support those who feel aggrieved. Let internal divisions do what external force could not." | internal/external mirror; the threat spelled out a second time (P, H) | "“If the company wished,” the envoy continued, “we could simply wait.”" The king's "You could" still answers it. |
| 113 | "The words hung in the air like smoke after a musket shot." | kill-list cliche (STYLE_SHEET 1) (P, H) | Cut. |
| 119 | "The threat was clear. Somewhere, someone the Dutch could use was waiting. A claim. A grievance. A kinswoman with long memories." | explained subtext; three-fragment list (P, H) | Cut. The kinswoman moves into 121. |
| 121 | "I thought of the name I had seen in Ramayyan's register. Elayadathu. The entry marked HIGH." | callback to the ledger room before Ch 21 reveals it (ch21:7, backlog N-07); a capitalised modern risk rating (REGISTER 18:121) (P, H) | "I thought of Kottarakkara, where the Elayadathu chief still took Dutch factors at his table, and of the kinswoman there who wrote to Revathi about what was owed." (Grounded in ch11:253 and ch9:146, both scenes Nagoji witnessed.) |
| 123 | "“Misunderstandings,” Padmini said under her breath, her voice harder than before. “A pretty word for greed.”" | misplaced: it answers the envoy's word at 101 twenty lines late; "harder than before" has no before (P, H) | Move it to directly after 101, and drop "her voice harder than before": "“Misunderstandings,” Padmini said under her breath. “A pretty word for greed.”" The envoy's "We are also aware" then reads as his reply to her. |
| 125, 127 | "Marthanda Varma sat very still for a long moment." / "When he spoke, his voice was calm." | stock pause and calm-voice beats (P, H) | Cut both. 129 opens "“You come here,” the king said, ..." |
| 129 | "You have learned... You have learned... You have learned that some of our houses, like Velinadu and Padmini's line, will not sign papers that erase their names. So you bring different papers. Clever. I approve of cleverness. It makes life interesting." | anaphoric triad; the chapter's premise recited back; modern quip; the Velinadu clause muddles who resists whom (P, H) | "“You come here,” the king said, “because you have learned that your guns cannot keep us from killing your men if you land them without leave, and that this small strip of coast is not as easy to bully as some others. So you bring papers instead. Clever.”" |
| 133 | "“Do not mistake my approval for weakness,” he said. “We will sign treaties that benefit us. We will not sign away our children's choices... This army is not for hire.”" | stock ruler line; mirrored pair; modern "choices"; closing kicker (P, H) | "“We will sign what profits us, and nothing more,” he said. “If you wish pepper, you will pay for it. If you wish safe anchorage, you will keep our rules. If you wish warriors, you will not have them.”" (The three terms stay; see Defended.) |
| 135 | "Ramayyan's stylus paused over his leaf. He glanced at the king, then wrote something with quick strokes." | stylus reaction shot (P, H) | "Ramayyan wrote it down." |
| 139 | "The envoy's throat worked." | stock swallow (P) | Cut. |
| 147 | "a hint of something like kindness in his tone" | hedged emotion (P, H) | Cut the phrase: "“If you wish to send him letters,” Ramayyan said, “we will read them first..." |
| 149 | "looked as if he might choke. The older man kept his features composed through will alone." | two stock reactions; Nagoji cannot see "will alone" (P, H) | "The younger Dutchman at the envoy's side went red to the ears. The older man's face did not change." |
| 151 | "trade and recognition”" | missing question mark (backlog N-44) (P, H) | "...trade and recognition?”" |
| 157 | "We have learned to be patient. We will sign this truce at Mannar now. But the real treaty, the one where you promise never to stand in our way again, the Treaty of Mavelikkara, that will come when we are finished with the north." | echoes the envoy's 117 too neatly; contradicts 153 ("When both sides match, we will sign"); a 1742 or 1743 character names a 1753 treaty (REGISTER 18:157); it steals ch28:159's payoff (P, H) | "“As long as needed,” Ramayyan replied. “What we sign now is a truce, a pause for breath. The real treaty, the one where you promise never to stand in our way again, will come when we are finished with the north.”" Keep "the real treaty": ch28:159 quotes it. |
| 159 to 163 | "After the formal session ended, the hall thinned." / "Chiefs drifted away... what the gods had known: that Travancore would not be an easy feast." / "...watching as his old compatriots were escorted out." | dispersal montage; the thesis again; "compatriots" (P, H) | Merge into one paragraph: "When the hall emptied, Lannoy stood near a pillar, hands clasped behind his back, watching the men of his old company escorted out." |
| 173 | "Lannoy replied quietly. “I prefer to be remembered by someone closer than Amsterdam.”" | hush tag; the polished second half of a mirrored comeback (P, H) | "“It forgets those who die for it,” Lannoy replied." |
| 175 | "The envoy's jaw tightened." | repeats 71 (H) | Cut. 177 becomes "“They call you traitor in Batavia,” the envoy said." |
| 179 | "Here, they call me kapitan. That is enough." | "That is enough" closing sting; the title is spelled "Kappittan" at ch15:223, ch15:321 and ch24:83 (P; backlog N-42) | "“They can call me what they like,” Lannoy said. “Here, they call me Kappittan.”" This pairs with Ibrahim's "Pillai" at 227: two foreigners renamed by this coast in one chapter. |
| 183 | "For a moment I imagined what it would be to see that glint across a courtyard that smelled of rice and lamp smoke, not ink and powder." | stock "For a moment"; an X-not-Y tail that drags the tender image back to the thesis (P, H) | "The light caught the coins at her throat and turned them into small, steady suns. For as long as it took her to notice me, I imagined that glint across a courtyard that smelled of rice and lamp smoke." |
| 187 | "She made a noncommittal sound." | stock beat; "noncommittal" (P, H) | Cut. |
| 197 to 201 | "That is a small victory." / "“Small victories add up,” I said." / "“So do small betrayals,” Revathi replied." | aphorism ping-pong; modern idiom (REGISTER 18:199) (P, H) | Keep only 197's first sentence: "“Today, my son, we have made them pay to do what they once did for free,” she said." Cut 199 and 201. |
| 203 | "Her hand brushed mine briefly as she turned back toward the sea, the contact so light it might have been an accident. My pulse did not think so." | romance cliche; filler adverb. Also a continuity slip: they became lovers in ch17:189 to 269, so a maybe-accidental touch cannot be news to his pulse (P, H, N) | "Revathi's hand brushed mine as she turned back toward the sea, lightly enough that anyone watching would have called it an accident." (With Padmini standing there, this reads as lovers' discretion. Keep the touch: ch20:163 calls back to it.) |
| 205 to 213 | "She looked at me." / "“Remember this, Nagoji,”... Those days matter too.”" / "“I will remember,”" / "“Good,”... The dead on the sand and the men who bowed here today.”" / "Her words settled into me like stones in a pouch." | blocking slip (she has just turned to the sea); the chapter's thesis lectured twice; therapeutic phrasing; paired fragments; stock simile (P, H) | Cut all five paragraphs. A short keep is offered under Borderline. |
| 215 | "I noted the date, the names, the key terms. Not because I trusted my memory, but because I had learned from watching Ramayyan that paper, in the right hands, could be a weapon." | "Not because X, but because Y", logically inverted (one writes things down because one does not trust memory); a moral; "key terms" (P, H) | "Later, by lamplight, I wrote down the date, the envoys' names and what they had offered for pepper, as I had watched Ramayyan do. Then I wrote it all out a second time." The second copy answers "Paper burns" without saying so. |
| 227 | "Pillai," with straight quotes | typography (P, H) | Curly quotes, to match the file. |
| 237 | "Ibrahim's eyes held mine." | eye beat (P) | Cut. 239 takes the tag "Ibrahim said". |
| 239 | "They carry pepper and cloth and silver. They carry talk too... Some men call it luck. Some call it warning. Some say... Others say... the English, who are beginning to look south with hungry eyes." | four-part rumour structure; cliche. The English already sit at Anchuthengu on this coast (ch11:431), so "beginning to look south" is also wrong (P, H, N) | "“My cousins trade in the Maratha ports,” Ibrahim said. “Pepper, cloth, silver. Talk too. Pune has heard of Colachel. Some there say a kingdom that can break a company square may one day trouble their southern border. Others say it would make a useful friend against the English.”" |
| 241 | "I felt the room tighten around those names. Pune. English. Ally. Threat." | stock beat plus a four-fragment list; "Ally" and "Threat" are not names; the chapter's most personal news gets no personal reaction (P, H, N) | "Pune. I had told myself that no one there would know my name if I rode back." (Ch12:141 has him think exactly this. Ibrahim's "It carries your name north" at 247 now answers it.) |
| 247 | "Somewhere in the middle, men are deciding whether those names should be written in treaties or in obituaries." | newspaper-era word (REGISTER 18:247); neat antithesis (P, H) | Cut this sentence. Keep the two before it, because ch19:81 quotes them. |
| 249, 251 | "He touched his forehead in a gesture of respect and walked out, leaving the smell of sea salt behind him." / "I watched him go." | labelled gesture; stock exit beats (P, H) | "He touched his forehead and went out." Cut 251. |
| 255, 257 | "Ramayyan's stylus paused." / "“I trust his web,” he said. “Every strand vibrates when something moves. If he lies to me, another strand will tell me.”" | stylus reaction shot. "You trust him?" / "I trust his X" copies ch11:441 to 443 ("I trust his fear"), and web-and-strand figures are rationed to Ch 20 (OEM 173, 208) (P, N) | Cut 255. 257: "“He has cousins,” Ramayyan said. “If he lies to me, one of them will tell me.”" The cousins are Yusuf (13) and the traders in the Maratha ports (239), so line 13 now pays off. |
| 259, 261 | "He returned to his leaf as if nothing had been said." / "he added, voice calm," | stock as-if; redundant manner tag ("voice calm" repeats 127) (P, H) | See Ending. |
| 263 to 269 | "The Dutch had come bowing." / "It did not mean they had forgotten how to bite." / "But as I went back to my lamp and my notes, I could taste dust on the wind..." | title-drop; maxim with a mixed image (bowing men, biting dogs); a last paragraph that opens with "But" (STYLE_SHEET 3); weather-omen coda (P, H, OEM 144) | Cut, with the section break at 263. See Ending. |

## Borderline

The author's call. Rows marked "take" are counted in the scratch estimate.

| Line | Quote | Issue | Option |
|:-|:-|:-|:-|
| 91 | "There was a murmur in the hall." | Filler (H), but it gives the hall a sound between two speeches, and once 93 to 95 go it is the only crowd reaction in the audience. | Leave. |
| 117 | "“Perhaps,” the envoy said. “Or perhaps not. We have learned patience.”" | A stock villain's hedge. "We have learned patience" is worth keeping now that Ramayyan no longer echoes it at 157. | Take: "“Perhaps,” the envoy said. “We have learned patience.”" |
| 131 | "The envoy opened his mouth to speak. The king lifted a hand." | Stock gesture (H), but it stages the king's authority, and the lifted hand is his habit (ch11:229). | Leave. |
| 143 | "“You had hoped many things,” the king said." | Copies the shape of Lannoy's 37. "Hopes are not terms" is the line (Defended). | Take: "“Hopes are not terms,” the king said." |
| 145 | "eyes fixed somewhere past the envoys' shoulders" | "Somewhere" is a scanner hit, and it adds to the eye count. | Leave, or "his eyes on the wall behind the envoys." |
| 177, 179 | the "traitor" and "Kappittan" pair | Backlog C10-33 would cut 175 to 179 and end on 173. | I recommend the trimmed pair (Confirmed 175, 179) because it pairs with "Pillai" at 227. C10-33's harder cut is acceptable. |
| 195 | "Padmini joined us, her stick ticking against the floor." | OEM 210 rations the stick to Chs 8, 26 and 28. | Take: "Padmini joined us." |
| 205 to 213 | Revathi's two speeches | If the author wants to keep her "another Goa" line, which is Nagoji's own prison and a real stake, keep one short speech in place of 205 to 213. | Not taken: "“One day some young rider will ask you how we kept this coast from becoming another Goa,” she said. “Tell him about the papers too.”" |
| 67 | the Treaty of Mannar name | The fixes remove it from the chapter. If the history check (Notes 2) confirms a Dutch truce at Mannar, the name can return as a memoir aside after 157. | Not taken: "The truce was signed at Mannar some months later." |
| 223 | "stylus moving as if the day had never ended" | The chapter's one "as if" (ration 1). It characterises Ramayyan's endless work. | Leave. |

## Defended (flagged, keep)

28 items.

| Line | Quote | Flag | Why it stays |
|:-|:-|:-|:-|
| 13 | Yusuf Marakkar | dangling character; merge with Ibrahim (P, H) | Not dangling. Ch10:65 introduces Yusuf as Ibrahim's cousin, and ch23:67 uses him again. In the fixes he sells the first news (13) and is one of the cousins who would expose Ibrahim's lies (257). Only the stock tag goes. |
| 15 | the paper idea itself | first of eight thesis statements (P) | Once, in the mouth of the kingdom's man of paper, trimmed of its correction. |
| 21, 27 | "Lannoy stood at the edge of the hall as they entered." / "The Dutch envoys saw him and faltered." | one-sentence paragraphs (scanner) | Plain staging that does the work 29 to 35 over-explained. |
| 23 | "the “Maratha” had found a permanent stall in this stable" | part of the flagged triad (P) | The chapter's only cavalryman's idiom (H). It is kept inside the rewrite. |
| 25 | Lannoy's cotton coat and the rewrapped hilt | not-X-but-Y (P) | The object tells Lannoy's whole situation (H). Only the construction changes. |
| 37 | "“You were told many things... Some of them were true.”" | echoed by 143 (H) | Dry and in character. 143 changes instead. |
| 47 | "spread his hands in that same well-practised manner that men of his trade seemed to learn along with their letters" | stock diplomat gesture (P) | A sardonic generalisation with Nagoji's attitude in it (H). |
| 53 | "our superiors in the chambers that oversee company trade in Europe" | none | Accurate. The VOC was run through six chambers under the Heeren XVII. It is a rare period-exact detail, so protect it. |
| 55, 69, 97 | Padmini and Revathi speak in the audience | ensemble zingers, not court protocol (H) | The book established this at ch11:215 to 227, where Revathi addresses the Dutch envoys in Portuguese and Padmini sits near the front. Their lines here carry the moral challenge (97) and the piracy point (69). The fixes trim their zingers, not their presence. |
| 69 | "“Who decides who is a pirate?”" | answers a clause no one read (P, H) | Kept, and fixed by adding the clause at 67. |
| 71 | "The envoy's jaw tightened." | stock (H) | One of the two jaws stays, and this is the better placed one. |
| 83 | "I saw one corner of his mouth twitch at that" | stock reaction (P) | Unexplained, so the reader works out why "friendship and alliance" amuses him (H). Optional trim: "Lannoy's face did not move, but one corner of his mouth twitched." |
| 115 | "the king said softly" | hush tag (P) | The one soft adverb kept (ration 2). A threat said softly is the king's manner. |
| 123 | "A pretty word for greed." | ready-made aphorism (P) | Short, and in Padmini's register. It is moved, not cut. |
| 133 | "If you wish pepper... If you wish safe anchorage... If you wish warriors, you will not have them." | strict triple (P, H) | A king giving terms in a formal audience lists them. The third breaks the pattern and refuses the "friendship and alliance" clause at 81, which is real plot work. Only the frame around it goes. |
| 137 | "they may address them to me, not to him" | comma-not (scanner) | Natural speech, and it is the point of the sentence. |
| 143 | "Hopes are not terms." | aphorism (P) | VOICE_BIBLE cites it as the king's register: short and exact. |
| 145 | "Lannoy stood very straight" | eye beat (P) | Parade posture while his fate is discussed. It is physical and a soldier's reaction. |
| 163 | "hands clasped behind his back" | none | OEM 222: keep. This is how the watch boy recognises him. |
| 173 | "It forgets those who die for it" | mirrored comeback (P) | A soldier's bitterness that fits Ch 16's Company pay grievances. Only the polished second sentence goes. |
| 189 | "They put quills where they once put muskets. Also something." | thesis hammering (P) | This is the one statement of the idea to keep (H), in Revathi's grudging spoken rhythm. |
| 191 | "“Ram will keep copies,” I said." | none | "Ram" is established (ch6:113, ch15:255, ch25:326), and the line sets up both "Paper burns" and the new second copy at 215. |
| 193 | "“Paper burns,” she said. “Land remembers.”" | epigram (P, H) | OEM 190 and VOICE_BIBLE 400 both choose it as Revathi's one epigram for the chapter. With 199, 201, 207 and 211 gone, it is the only one in the scene. |
| 203 | the hand brush itself | romance beat (P, H) | Load-bearing. Ch20:163 says "the same light touch as on that verandah after the Dutch bowed". Only "My pulse did not think so" and "briefly" go. |
| 227 | "“Pillai,” Ibrahim said" | none | Nagoji's new house name in a trader's mouth, the first outsider to use it. It pairs with "Kappittan" (179). |
| 235 | "“Not Dutch,” Ramayyan said. “North.”" | "Not X. Y." (P) | The one allowed in the chapter: dialogue, a natural answer to "Dutch?", and it turns the chapter (H). |
| 243, 247 | "“And which way does the wind blow?”" / "“The wind blows in circles... It carries your name north and the Peshwa's name south.”" | stock prompt (H); antithesis (P) | Ch19:81 quotes it: "the wind blows in circles, and names travel". Only the obituaries sentence goes. |
| 261 | "“When the first letter comes... bring it to me.”" | vague foreshadowing hook (P) | It is the chapter's real ending, and Ch 19 pays it at once (ch19:11, the letter from his brother). Only the tag changes. |

Two protections asked for by the holistic reader are overruled:

- **"I trust his web" (257).** It copies the form of ch11:443 ("I trust his fear"), which follows the same "You trust him?" question. The web-and-strand figure is also rationed to Ch 20. The replacement keeps the spymaster's logic in concrete terms.
- **The Deccan dust at 269, moved into 241.** Not done. Ch19:9 to 11 opens on "dreams of black soil and dry wind" and "a letter... with my village's dust still clinging to it", so the image belongs to Ch 19. The new 241 does the personal work with Ch 12's thought instead.

## Opening

**Current (3 to 19):**

> The second time Dutchmen entered the coastal hall, they smelled less of salt and more of caution.
>
> It had been some time since Colachel.
>
> Long enough for new walls to rise, for fresh muskets to find their way into Travancore hands, for stories of the broken company square to spread along the Malabar coast and into places where men in powdered wigs frowned over them.
>
> Long enough for Batavia to send new instructions.
>
> We heard of the envoys before we saw them.

This is followed by the markets, backwaters and temples montage, Ramayyan's "Not with drums", "He was right." and the three comparatives.

**Verdict: rewrite.** OEM lists the first line among the book's "The first / second..." openers, and its less/more smell is copied by the Ch 23 opener (OEM 65). The next four paragraphs are stacked one-liners with no place, body or date in them. The first voiced moment is Ramayyan at 15. The rewrite starts with a date, gives the rumours one source who pays off at 257, and lets the envoys' clothes and bundles show the change of fortune.

**Proposed (replaces 3 to 19):**

> The Dutch came back to the coastal hall two monsoons after Colachel.
>
> Yusuf Marakkar had the news first, and sold it to Ramayyan a spoonful at a time, the way he sold everything. Dutch factors at Kochi were counting their coins twice. Company captains no longer pressed the small chiefs for pepper at the old prices. On the backwaters the boatmen said the company landings had gone quiet, and fewer of the men in them carried muskets.
>
> “They will come,” Ramayyan said one morning, tapping a palm leaf with his stylus. “With papers, this time.”
>
> When they came, their coats were plainer than the ones that had strutted in this hall before the battle, with less lace at the cuffs. Behind them walked scribes carrying thicker bundles than before.

Leave 21 ("Lannoy stood at the edge of the hall as they entered.") as it is, then continue with the new 23.

## Ending

**Current last lines (253 to 269):**

> “You trust him?” I asked.
>
> Ramayyan's stylus paused.
>
> “I trust his web,” he said. “Every strand vibrates when something moves. If he lies to me, another strand will tell me.”
>
> He returned to his leaf as if nothing had been said.
>
> “When the first letter comes,” he added, voice calm, “bring it to me.”
>
> (section break)
>
> The Dutch had come bowing.
>
> It did not mean they had forgotten how to bite.
>
> But as I went back to my lamp and my notes, I could taste dust on the wind, dry and far away, carrying the Deccan toward this coast.

**Verdict: revise.** The chapter already ends well at 261. The coda after the break makes three mistakes:

- It drops the title in as a summary.
- It adds a maxim that mixes courtiers with dogs.
- It closes on a weather omen that begins with "But" (STYLE_SHEET 3) and uses up the image Ch 19 opens with.

VOICE_BIBLE 566 counts this as one of the book's few image endings, but here the image comes after a title-drop and a maxim, and it foreshadows rather than shows. OEM 144 reaches the same cut. The work is small: cut the coda, the stylus beat and the as-if, and trim two tags.

**Proposed close (replaces 253 to 269):**

> “You trust him?” I asked.
>
> “He has cousins,” Ramayyan said. “If he lies to me, one of them will tell me.”
>
> He went back to his leaf. I had my hand on the door when he spoke again, still writing.
>
> “When the first letter comes, bring it to me.”

Why this close:

- It ends on a line of dialogue, which is plain, specific and ominous. It also implies that Pune will write to Nagoji himself.
- The hand on the door is a small action that makes the line land as an afterthought, which is how a spymaster gives his most important order.
- Ch19:11 pays it at once ("Then a letter arrived with my village's dust still clinging to it"), and the dust image stays with Ch 19.
- No other chapter closes on this idea.

## Flab (passages to tighten)

| Lines | Issue | Action |
|:-|:-|:-|
| 3 to 19 | Throat-clearing: a smell conceit, "some time", two "Long enough" paragraphs, "heard before we saw", a montage, "He was right.", three comparatives. About 230 words before the envoys walk in. | Opening, about 110 words. |
| 23 | A status recap in four sentences around one good idiom. | Confirmed 23. |
| 29 to 41 | The envoys' surprise is explained four ways (29, 33, 35, 39), and the king's feelings are denied in a formula (41). Lannoy's reply at 37 covers it. | Keep 27, 31, 37, a trimmed 39 and the first half of 41. 33 becomes the Dutch gloss. |
| 45, 85, 129 | The king makes the "land on my shore" point three times. | Keep 45 (Protect), cut 85's second sentence, and reduce 129 to one clause. |
| 65 to 95 | A metronome of line, reaction tag, riposte: jaw, stylus, "Interesting.", murmur. Then Ramayyan recaps terms just read. | Confirmed 65, 75, 77, 93 to 95. Keep 71 and 91. |
| 99 to 127 | The threat is delivered three times (105, 111, 119), with eight stock beats stacked around it, and Padmini's retort is stranded at 123. About 250 words. | Confirmed 103 to 127. About 120 words, with Padmini's line moved to 101. |
| 129 to 133 | The king's speech recites the chapter's premise, adds a modern quip, then a stock ruler line and a mirrored pair, before the good terms. | Confirmed 129, 133. |
| 155 to 161 | A patience echo, two treaty names, a contradiction of 153, then a dispersal montage. | Confirmed 157, 159 to 163. |
| 171 to 179 | Two cappers in a row ("Amsterdam", "That is enough") and a second tightened jaw. | Confirmed 173, 175, 179. |
| 183 to 215 | The thesis is stated six times, the verandah ends three times (speech, simile, note), and the aphorisms trade back and forth. About 390 words. | Confirmed 183 to 215. About 190 words, ending on the second copy. |
| 237 to 251 | Four-part rumours, a fragment list, a labelled gesture, stock exits. | Confirmed 237 to 251. |
| 255 to 269 | Stylus beat, as-if, manner tag, and a three-part coda. | Ending. |
| Whole chapter | Ramayyan's stylus reacts at 75, 93, 109, 135, 255 and 259. There are seven eye beats (23, 35, 41, 109, 145, 237, 239) and four hushed tags (51, 115, 123, 173). | Stylus: keep 15 and 61 (tools), 109 (the one reaction) and 223 (setting), and make 135 "wrote it down". Eyes: keep 23 (the chain glance) and 145. Keep one soft adverb, 115. |

## Passages to protect

- **23**, "the “Maratha” had found a permanent stall in this stable" and the silver chain Padmini fastened that morning.
- **25**, "Lannoy wore a simple cotton coat over his European shirt... its hilt now wrapped in local cloth."
- **37**, "“You were told many things,” Lannoy replied in the same language. “Some of them were true.”"
- **41 (first sentence)**, "Marthanda Varma sat on his platform as before, bare feet on the mat, spear within reach."
- **45**, "“Regrets,” Marthanda Varma repeated. “You regret that your men died when they tried to land on my shore. Do you regret sending them here at all?”"
- **47**, the envoy's well-practised hands.
- **53**, "the chambers that oversee company trade in Europe."
- **55**, Padmini's driftwood.
- **59 to 63**, Ramayyan will not take their paper: the empty palm leaf, "Read,". This is the best-staged moment in the chapter.
- **67 and 81**, the clause lists (with the new piracy clause).
- **83**, Lannoy's unexplained twitch.
- **89**, "“Partners,” the king said. “Partners who once tried to break my spine.”"
- **97 to 101**, Revathi's question for the dead, and "misunderstandings".
- **137**, "he is now my officer... address them to me, not to him."
- **143**, "Hopes are not terms."
- **147**, the letters policy, minus its tag. Procedure as cruelty and kindness at once.
- **153**, "We will draft our own version... When both sides match, we will sign."
- **163**, De Lannoy at the pillar, hands clasped behind his back.
- **167 to 169**, "“You seem healthy,”... “I have work,” Lannoy said. “Men here do not waste tools.”" This is the most alive exchange in the chapter.
- **173 (first sentence)**, "It forgets those who die for it."
- **189 to 193**, "They bowed... That is something... Also something." / "Ram will keep copies." / "Paper burns. Land remembers."
- **197 (first sentence)**, "Today, my son, we have made them pay to do what they once did for free."
- **217 to 219**, the lamp oil half burned, and "Now."
- **225 to 229**, buttermilk, the low stool, a voice that stops, "Pillai," and "Stay."
- **233 to 235**, "Dutch?" / "Not Dutch. North."
- **243 to 247 (first two sentences)**, the wind in circles, the names that travel.
- **261**, "When the first letter comes... bring it to me."

## Chapter-specific notes (continuity and history)

1. **The chapter never gives a date.** Ch16:21 ("Four monsoons since we washed up", from 1738) puts Ch 16 in 1742. The Author's Historical Note timeline dates the truce 1743. "Two monsoons after Colachel" (August 1741) fits 1743. If the author settles on 1742, write "a monsoon after Colachel".
2. **Mannar needs checking before print.** Several standard accounts of Marthanda Varma's reign give the Treaty of Mannar (1742) as Kayamkulam's submission to Travancore. They place the Dutch negotiations at Mavelikkara from 1743, concluded in 1753. The Author's Historical Note (Selected Timeline) calls Mannar "an early settlement with the Dutch" (1743). The proposed fixes remove the name from the chapter, so Ch 18 is safe either way. If the check goes against the Note, correct the Note (a sync file), and do not restore the name here (Borderline 67). Also, the old line 157 had the truce signed "at Mannar now", in the coastal hall, which does not work geographically.
3. **Optional payoff.** If the chapter is set in 1743, the "Governor General... at Batavia" (53) was Gustaaf Willem van Imhoff, who took office there in 1743. He is the man who threatened the king in Ch 11. Verify, and consider one line from the king ("Van Imhoff? Then he remembers this hall."). Not required.
4. **"tried to land" (45).** In Ch 14 the Dutch did land, and held Colachel until they were besieged. Consider "died when they landed on my shore". Protect the rest of the line.
5. **The Revathi relationship does not agree across chapters.** Ch17:189 to 269 makes them lovers. Ch18:203 (as first written) and ch20:5 to 7 play the touch as unspoken courtship, and ch20:163 calls back to this verandah. The proposed 203 reconciles Ch 17 with Ch 20 by making the touch lovers' discretion in front of Padmini. Ch20:5 to 7 needs the same look in its own pass.
6. **The title's bow.** In the first edition the only bow on the page is "bowing slightly" to De Lannoy (31), copied from ch11:187. The fix at 43 puts a low bow before the king, so Revathi's "They bowed" (189) has something to point at.
7. **The envoy is unnamed** (backlog C10-22). The new 215 has Nagoji writing down "the envoys' names". Name the senior envoy there, or at 31, and reuse the name in Ch 11.
8. **Company style.** "Honourable" appears here and at ch11:187. Decide once for both: "the Company", or the VOC's own style, "the Noble Company". The chapter writes "company" in lower case in narration. Keep that, except in the envoy's formal style.
9. **Names and titles** (backlog N-42, FM-10). Use "Kappittan", not "kapitan" (179). "*Valia Karyakkar*" (23) against "Valiya" elsewhere: settle the spelling and add it to the glossary.
10. **De Lannoy arc.** "the one he had surrendered at Colachel" (25) fits the surrender arc in the chapter files, which SOURCE_OF_TRUTH recommends (Decision 1). This chapter's text is identical in the EPUB, so the published desertion-arc book already carried the mismatch. If the desertion arc is kept, write "the one he had carried across the lines".
11. **Payoffs this chapter must keep planting:** ch19:81 (the wind and the names, from 247), ch19:11 (the first letter, from 261), ch20:163 (the verandah touch, from 203), ch28:159 (Ramayyan's "real treaty", from 157).
12. **The rumour at 239 is historically sound.** Maratha forces under Murari Rao Ghorpade held Trichinopoly from 1741 to 1743, within reach of Travancore's eastern passes, so Pune had a southern border to worry about. The English clause is cut because the English were already on this coast at Anchuthengu (ch11:431).
13. **Mechanics** (backlog N-44 and REPETITION 647): 23 uses curly apostrophes and a capital "King’s"; 151 is missing its question mark; 227 uses straight quotes.
14. **Sync files.** The Author's Historical Note (lines 53 and 82) says Ch 18 "represents" the Mannar truce. That still reads correctly if the name leaves the chapter. Update the Note only if the Mannar check in note 2 fails.
