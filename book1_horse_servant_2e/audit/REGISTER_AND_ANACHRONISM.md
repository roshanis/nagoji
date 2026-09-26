# Register and Anachronism Audit

*Horse of the Servant*, first edition, Chapters 1 to 28. Prepared for the second-edition line edit.

- Source audited: `book1_horse_servant/book*_chapter*.md` (the frozen first edition). Line numbers are the physical line numbers in those files, blank lines included. The 2e working copies in `manuscript/` will match until they are edited, so apply fixes from the bottom of each chapter upward.
- Brief: find modern concepts, idioms and registers in a narrator who is a Maratha cavalryman recalling 1738 to the 1750s. Plain modern English is the translation medium and stays; modern *ideas and phrasings* go.
- Out of scope here: the structural "slop" patterns in `STYLE_SHEET.md` (kickers, "Not X, but Y", fragment triples) except where they overlap with register. A short list of continuity slips noticed along the way is at the end.

## 1. Summary

**290 findings** across all 28 chapters: **52 P1**, **127 P2**, **111 P3**.

| Priority | Meaning | Count |
|---|---|---|
| P1 | A clear anachronism or unmistakably modern phrase that a reader will notice. Fix in the 2e pass. | 52 |
| P2 | Modern register that jars against a 1740s voice. Fix unless the author wants it. | 127 |
| P3 | Borderline or cheap to fix. Consider during the line edit. | 111 |

| Category (tag used in the table) | Findings |
|---|---|
| Modern idiom and colloquialism (`idiom`) | 63 |
| Management, business and bureaucratic vocabulary (`management`) | 52 |
| Modern military jargon (`military`) | 49 |
| Wrong-period names, titles, people and facts (`names/facts`) | 32 |
| Scholars' and historians' labels (`scholarly`) | 21 |
| Material culture (dress, food, buildings, objects) (`material`) | 20 |
| Psychology, therapy and self-help register (`psychology`) | 18 |
| Science, technology and machine images (`tech`) | 16 |
| Spelling and typography (`typography`) | 10 |
| Clock time and measurement (`time/measure`) | 9 |

Heaviest chapters: Ch 24 (26, of which 4 P1), Ch 16 (22, of which 7 P1), Ch 13 (20, of which 4 P1), Ch 23 (18, of which 3 P1), Ch 15 (17, of which 4 P1), Ch 11 (16, of which 5 P1). The Part 1 chapters (1 to 6) are the cleanest; the problems thicken from Chapter 11, where the book starts to deal in treaties, ledgers and armies.

### How it was checked

1. Grep sweeps of all 28 files for the brief's watch list plus about 150 further modern terms (management, therapy, military, computing, finance), clock and measurement units, machine and electrical metaphors, post-1750 technology, American spellings, contractions, spaced hyphens, and every transliterated term (counts, spellings, italics).
2. A full read of every chapter, line by line, for the idioms no word list catches ("a window", "reached out", "It makes for vivid reading").
3. Every excerpt in the Section 3 table was checked by script against the cited line of the source file, so each one can be found with a plain search.

### Results for the brief's watch list

| Word or family | Hits | Verdict |
|---|---|---|
| process, stress, trauma, team, closure, mindset, okay | 0 | Clean. None in the text. |
| focus / focused | 6 | Five flagged (9:24, 13:199, 13:281, 14:127, 22:75). 22:197 "eyes lost focus" is the optical sense and can stay. |
| navigate | 1 | Flagged, P1 (16:297). |
| leverage / lever | 1 + 4 | "Leverage: significant." in the ledger is flagged (21:71). "Use it as a lever" (1:55, 12:73, 13:161, 11:269) is an old mechanical image and can stay. |
| journey | 3 | All literal travel (2:67, 2:99, 3:67). Keep. |
| bond | 4 | 8:151 translates *bandham* and 17:97 is ceremonial; keep. 7:181 is a slop line for other reasons. The ledger's "Velinadu bond" (21:49) is flagged with the ledger. |
| deal with / handle / manage | 8 | Flagged: 11:225 ("management"), 12:131, 19:139, 22:383, 22:401. Kept: 3:203 and 24:75 ("managed" = succeeded), 7:161 ("dealt with" = traded). Physical "handle/handled" (8:89, 16:213, 17:169) is fine. |
| strategy / strategic / strategist | 5 | All flagged (12:57, 13:113, 13:123, 14:29, 17:137). "Tactics" does not occur. |
| seconds / minutes | 0 / 3 | Every "second" is an ordinal. All three "minutes" flagged (4:9, 9:58, 15:145). |
| percent, yards, miles, pounds, hands, inches, clock time | 10 | Flagged: 7:145, 7:147, 10:57, 11:127, 11:141, 14:131. Tolerable as idiom: "several yards" (23:219) and "inches" (22:153, 22:403, 26:43). |

## 2. Patterns worth fixing globally

These clusters account for most of the P1 and P2 rows. Fixing each one as a pattern, rather than line by line, will keep the voice consistent.

1. **Ramayyan's records read as a modern risk register.** 18:121 ("The entry marked HIGH"), 19:149 ("expiry date", "asset", "risk"), 21:43 to 21:72 ("Skills", "adaptability", "mitigated", "emotional ties", "Leverage", "Risk assessment: HIGH. Timeline"), 25:90 ("'risk' column ... 'asset' one"). This is the single most visible modern intrusion in the book. Rewrite the entries as a revenue clerk's palm-leaf notes: names, kin, lands, debts, grudges, and short verbs ("watch", "doubtful", "to be settled before the rains"). The leaf at 25:208 to 25:210 ("tested with northern letter ... Is ours.") is already close to the right idiom and can be the model.
2. **Management and office vocabulary.** schedule (5:115, 20:5, 26:27), management (11:225), career (13:131), industry (13:127), partnership / partners (18:87, 24:59, 24:87), structure (24:39, 24:49), network (19:195, 25:296), potential (24:661), mission and vision (24:239), company policy (24:679), logistics and "executed" (20:292), reach out (25:234), "Preventable deaths" (24:63), written off / red ink (15:199, 15:201, 24:209). Nagoji's own trade words are ledger, tally, account, debt, coin, levy, grain, and they do the same work.
3. **Modern military jargon.** perimeter (13:187, 14:31, 14:69, 17:5, 23:419), unit (10:179, 16:219, 16:265, 16:305, 16:435, 23:37, 24:7), company-sized units (16:291), supply lines (10:179, 14:167), casualty and intelligence reports (13:141, 14:71), secondary explosions and cooking off (14:105, 14:107), pocket of resistance (14:141), friendly fire (16:219), shock troops (7:155), downrange (24:673), troop movements (25:240), fallout (23:505), checkpoints (17:61). The period word-stock is plenty: ring, lines, troop, company, battery, the carts, the dead and wounded, spies, word.
4. **Therapy and self-help register.** identity (15:55), "your feelings to catch up" (24:179), "you deserve one" (17:275), "preparation meeting opportunity" (14:89), "have a conversation" (13:289), replaying (16:59), paralysis (24:491), "have your moment" (25:274). Nagoji should not have the vocabulary to describe his own feelings this way (STYLE_SHEET section 4 says the same).
5. **Machine, computing and science images.** reset (15:141, 23:181), regenerate (16:233), tripwire (23:181), thermal (20:17), weather front (19:5), shockwave (14:101), cyclone (14:103), controlled burn (26:135), black oxide (17:49, 17:159), spent cartridges (16:399), edited (17:99), momentum (22:111). Replace with images from his world: horses, rope, fire, monsoon, the forge.
6. **Clock and measure.** Nagoji should reckon time in breaths, watches of the night, the time it takes to milk a cow (the old *godohan* measure), sunrise and noon; distance in paces, bowshots and kos. "Hour", "day" and "week" are fine as translation. Minutes, seconds, clock times, percentages, yards, pounds and miles are not.
7. **Titles and names from the wrong century.** "Sri Lanka" four times (2:55, 11:121, 11:129, 13:105) against "Ceylon" three times; "diwan" for Ramayyan 18 times (a Travancore title only after 1809); "Your Majesty" and "Highness" for the king and the Rani (British-era styles); "the Honourable Company" (that is the English company's style); "British" for the English; "the Carnatic wars" and "the Maratha confederacy" (historians' labels); "Nair Brigade" (19th century); Mathu Tharakan (born 1741) as an adult merchant and minister in 1739 to 1741; a treaty of Mavelikkara named ten years early.
8. **Scholars' words.** matrilineal (8:55, 17:111, 21:69, 25:144, 27:101, 27:145), patrilineal (20:113), consolidation (10:185, 11:3, 18:105, 28:169), state-building (10:181), foreshadowing (27:55). Characters on this coast name the thing itself: the law of the mothers, *marumakkathayam*, the house, the line.
9. **The filing-cabinet habit.** 2:39, 2:45, 5:21, 11:267, 21:5, 28:11 all "file" things away. Once is a quirk; six times is a tic, and a modern one.

## 3. Line-by-line findings

Tags in the Problem column: `idiom`, `management`, `military`, `names/facts`, `material`, `scholarly`, `psychology`, `tech`, `typography`, `time/measure`. Excerpts are exact substrings of the cited line. Where the suggested replacement covers two phrases in one line, they are separated by "...".


### Chapter 1 (`book1_chapter01_dungeons_of_goa.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 1 | 49 | `chosen by your sardars for your initiative` | **P2** `management` "Initiative" as a personal quality is a late 18th-century sense and reads like an appraisal form. | chosen by your sardars for your daring |
| 1 | 59 | `If you cooperate, your suffering can end.` | **P3** `idiom` Police-procedural register. | If you speak, your suffering can end. |
| 1 | 63 | `with the impact of Maratha cannon` | **P3** `tech` "Impact" as a noun for a blow is late and technical. | the ground above this dungeon would shake under Maratha cannon |
| 1 | 93 | `How often they changed shifts.` | **P2** `management` "Shift" as a spell of work is 19th-century factory usage. | How often the watch changed. |

### Chapter 2 (`book1_chapter02_slave_ship_south.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 2 | 39 | `I filed his face away` | **P3** `idiom` Filing-cabinet metaphor, the first of six (see pattern 9). | I stored his face away in the part of my mind that kept accounts. |
| 2 | 45 | `filed the calculations away` | **P3** `idiom` Same filing idiom, second use in six lines. | and put the sum away in minds that already carried too much |
| 2 | 55 | `Some place beyond Sri Lanka.` | **P1** `names/facts` "Sri Lanka" has been the island's official name only since 1972. A Goan prisoner in 1738 would say Ceylon (Portuguese Ceilão) or Lanka. | Some place beyond Ceylon. |

### Chapter 3 (`book1_chapter03_choice_in_the_storm.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 3 | 31 | `They draw every eye in a space.` | **P3** `idiom` "A space" for a room is modern design talk. | They draw every eye in a room. |
| 3 | 69 | `His Adam's apple bobbed against his collar.` | **P3** `idiom` English anatomical nickname built on a Bible joke; outside Nagoji's frame. | His throat worked against the iron collar. |
| 3 | 109-111 | `On three.` ... `On three we both jerked backwards` | **P2** `idiom` Counting a lift "on three" is a modern convention. | "When I say now, pull as if you are trying to tear your own head off. Now." / At the word we both jerked backwards |

### Chapter 4 (`book1_chapter04_fishermen_of_the_pepper_coast.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 4 | 9 | `a time that could have been minutes or hours` | **P2** `time/measure` Clock minutes; Nagoji has no clock (pattern 6). | for a time that could have been a few breaths or half a day |
| 4 | 25 | `wore lungis hitched up around their thighs and short, sleeveless vests` | **P2** `material` Tailored vests are a modern garment for Mukkuvar fishermen of 1738, and "lungi" is a Persian-derived trade word; the coast's own word is *mundu*. | wore cloths hitched up around their thighs and nothing above the waist but salt |
| 4 | 97 | `used to making decisions that stuck` | **P3** `idiom` Modern colloquial "stuck". | used to having her word obeyed |

### Chapter 5 (`book1_chapter05_road_to_travancore.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 5 | 21 | `he was filing information away` | **P2** `idiom` Office-filing metaphor plus "information" in the intelligence sense. | a habit, I would learn, that meant he was putting something by for later |
| 5 | 115 | `The sea does not consult my schedule` | **P1** `management` "Schedule" as a personal timetable is 19th-century and reads as a modern diary. | The sea does not keep my hours |

### Chapter 6 (`book1_chapter06_coastal_hall.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 6 | 13 | `a short coat over his vest` | **P3** `material` Same garment problem as 4:25. | a short coat over his shirt |
| 6 | 41 | `this was his diwan, Ramayyan` | **P1** `names/facts` Travancore's chief minister was styled Dalawa in this period; "Dewan" replaced it as the Travancore title only in the early 19th century. Ramayyan held the Dalawa office from about 1737. "Diwan" appears 18 times, from 6:41 to 14:167 (see house list). | this was his Dalawa, Ramayyan |
| 6 | 49 | `Your Majesty` | **P2** `names/facts` European royal address, used nowhere else in the book. | "Maharaja," Ibrahim said |
| 6 | 143 | `as expendable labour` | **P2** `military` "Expendable" in this sense is a Second World War word. | consigned to some pepper estate as labour nobody would miss |

### Chapter 7 (`book2_chapter07_horses_in_wet_sand.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 7 | 31 | `you are not a soldier, you are a target` | **P3** `idiom` Sounds like a modern drill instructor. | you are not a soldier, you are a mark for their muskets |
| 7 | 77 | `Precise. Mechanical.` | **P3** `tech` Machine image, and a fragment pair of the kind STYLE_SHEET section 1 cuts. | They load and fire like one man. |
| 7 | 89 | `we take them with the sabre` | **P3** `names/facts` "Sabre" is the European word; the house term is talwar. | we take them with the talwar |
| 7 | 103 | `the subtle shift from resistance to acceptance` | **P3** `psychology` Counselling vocabulary applied to horses. | the give of a horse that has stopped arguing |
| 7 | 137 | `Responsibility, sharp as any spear point.` | **P3** `psychology` Abstract noun; Nagoji names things. | The weight of other men's lives, sharp as any spear point. |
| 7 | 145 | `I had walked the last miles to Goa` | **P3** `time/measure` English miles; a Maratha counts in kos. | I had walked the last kos to Goa |
| 7 | 147 | `stood barely fourteen hands` | **P3** `time/measure` English horse measure. Tolerable as translation; decide once for the whole book. | Keep, or: stood no higher than my chin |
| 7 | 155 | `The smart commanders` ... `for the shock troops` | **P1** `military` "Shock troops" is a First World War coinage (German Stosstruppen). "Smart" for clever is colloquial. | The wise commanders ... Madurai and Arab stock for the heavy charge |

### Chapter 8 (`book2_chapter08_padmini_ammas_estate.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 8 | 5 | `part of the landscape` | **P3** `idiom` Modern idiom. | I became, in a small way, one of the sights of that beach |
| 8 | 41 | `Pack your kit.` ... `pays for your salary` | **P3** `military` "Kit" for a soldier's gear is late 18th-century British army slang; "pays for your salary" is payroll phrasing. | Gather your things. ... She supplies half the pepper that pays your wages |
| 8 | 55 | `the matrilineal line` | **P1** `scholarly` "Matrilineal" is a 1900s anthropologists' coinage, here in Ibrahim's mouth. | It belongs to the name that passes through the mothers. |
| 8 | 61 | `instead of a stretcher` | **P2** `material` "Stretcher" for carrying the sick is mid-19th century. | and now arrived here on a horse instead of a litter |
| 8 | 171 | `In your system, his wife and children are ruined.` | **P2** `management` "System" for a social order is modern. | In your way of things, his wife and children are ruined. |
| 8 | 211 | `supporting its current occupant` | **P2** `idiom` Modern political-journalism idiom. | Not always the same thing as supporting the man on its throne. |
| 8 | 227 | `without putting your Deccan boot in your mouth` | **P2** `idiom` "Foot in mouth" is a 19th-century idiom. | without tripping over your Deccan tongue |

### Chapter 9 (`book2_chapter09_princess_of_velinadu.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 9 | 6 | `quilted with rubbery green` | **P1** `material` Rubber is a word of the 1780s onward and Kerala's rubber estates date from the 1900s; the image reads as a modern plantation. | low hills quilted with glossy green |
| 9 | 24 | `seemed more focused on who entered than what` | **P2** `psychology` "Focused" for attention (pattern 2). | seemed to care more about who entered than what |
| 9 | 52 | `somewhere deeper within the complex` | **P2** `material` "Complex" for a group of buildings is 20th century. | somewhere deeper within the compound |
| 9 | 56 | `Coconut instead of groundnut.` | **P2** `material` Groundnut was not a Deccan staple in the 1730s; large-scale cultivation came in the 19th century. Maratha kitchens cooked with sesame and safflower oil. | Coconut instead of sesame. |
| 9 | 58 | `as the minutes stretched` | **P2** `time/measure` Clock minutes. | as the waiting stretched |
| 9 | 162 | `The question was hypothetical` | **P3** `scholarly` Logician's word. | It was only a question, but it landed like a thrown dagger. |
| 9 | 188 | `The world falls over itself to give them offers. I state my position early.` | **P2** `idiom` Modern negotiating idiom. | The world runs to give them things. I say where I stand before anyone asks. |
| 9 | 218 | `had made her position clear` | **P3** `idiom` Same negotiating phrase. | Revathi Bayi had said her piece. |

### Chapter 10 (`book2_chapter10_lessons_in_travancore.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 10 | 57 | `roughly five hundred pounds` | **P2** `time/measure` English avoirdupois weight in a Maratha's head. | each sack a *candi*, I had learned, a full cartload by the weight of this coast |
| 10 | 139 | `buzzed with the weight of new connections` | **P3** `management` Networking register. | My head, too, was full of new threads. |
| 10 | 175 | `turned a “request” into a “requirement.”` | **P3** `management` Bureaucratic wordplay in scare quotes. | turned a request into an order. |
| 10 | 179 | `a recalcitrant` ... `Ramayyan had mapped his supply lines` ... `a unit of Maravar horsemen` | **P2** `military` "Recalcitrant" is 1840s; "supply lines" and "unit" are modern military terms. | a stubborn *madampi* ... that Ramayyan had counted every cart that fed him ... a troop of Maravar horsemen |
| 10 | 181 | `the brutal efficiency of state-building` ... `total submission or total erasure` | **P1** `scholarly` "State-building" is 20th-century political science; "erasure" in this sense is modern. | There was no glory in it, only the hard work of making one kingdom out of many. ... submit wholly, or see his house wiped from the land. |
| 10 | 185 | `these “years of consolidation”` | **P2** `scholarly` Historian's label in scare quotes; recurs at 11:3 and 18:105. | It was during those years of swallowing small houses |

### Chapter 11 (`book2_chapter11_dutch_on_the_horizon.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 11 | 3 | `ending the years of quiet consolidation` | **P3** `scholarly` Same historian's label. | ending the quiet years |
| 11 | 7 | `Kollam (Quilon)` | **P3** `names/facts` Parenthetical gloss is an editor's voice, not Nagoji's. Same at 11:121, 12:13, 12:91; the glossary already carries the old names. | marching north to swallow Kollam |
| 11 | 121 | `The Dutch Governor of Sri Lanka (Ceylon)` | **P1** `names/facts` Anachronistic name plus editorial gloss. Van Imhoff was Governor of Ceylon. | The Dutch Governor of Ceylon |
| 11 | 123 | `We were theatre.` | **P3** `idiom` Modern figurative use. | We were there to be seen. |
| 11 | 127 | `Van Imhoff had arrived at half past eleven` | **P1** `time/measure` Clock time to the half hour (lifted from the Dutch diary) is outside Nagoji's reckoning, and clashes with "that night" at 11:123. | Van Imhoff had arrived a little before noon |
| 11 | 129 | `He had governed Sri Lanka.` | **P1** `names/facts` As 11:121. | He had governed Ceylon. |
| 11 | 141 | `Less than one percent` ... `It was not a negotiation.` | **P2** `time/measure` Percentage arithmetic and "negotiation" as a set term are modern register. | Not one part in a hundred of what the ceremony required. It was not bargaining. |
| 11 | 145 | `called it diplomacy` | **P2** `names/facts` "Diplomacy" enters English in the 1790s. | They measured out their contempt in gold and called it friendship. |
| 11 | 187 | `The Honourable Company brings greetings` | **P2** `names/facts` "Honourable" is the English East India Company's style, not the VOC's. Same at 18:43. | The Company brings greetings |
| 11 | 225 | `another management` | **P1** `management` Corporate "management" as a governing team. | They belonged to another time, another Commander at Kochi. |
| 11 | 267 | `I filed the name away.` | **P3** `idiom` Filing idiom again (pattern 9). | I kept the name. |
| 11 | 361 | `fitting new pieces into a puzzle` | **P3** `idiom` Jigsaw-puzzle image; the toy is later 18th century. | fitting new stones into a wall he had already half built |
| 11 | 401 | `each thinking they had an exclusive arrangement` | **P3** `management` Commercial jargon. | each thinking he was the only buyer |
| 11 | 419 | `where Mathoo Tharakan's people held sway` | **P1** `names/facts` Mathu Tharakan was born in 1741 and rose under Rama Varma in the 1780s; he cannot be a grown merchant in 1739 to 1741. Recurs at 13:91 to 13:129 and 15:173 to 15:201. | Give the role to an invented Syrian merchant of the period, or to "the Tharakan families" unnamed. |
| 11 | 427 | `Thankfully, their men are equally brave.` | **P2** `idiom` "Thankfully" as a sentence adverb meaning "luckily" is 20th century. | Happily, their men are brave enough. |
| 11 | 439 | `put his own coin on the line` ... `We call it buying time.` | **P2** `idiom` "On the line" is a 20th-century gambling idiom; "buying time" reads modern. | put up his own coin ... We call it a season's grace. |

### Chapter 12 (`book2_chapter12_the_shadow_from_arcot.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 12 | 7 | `the wreckage of the Carnatic wars` | **P1** `scholarly` "The Carnatic Wars" is the historians' name for the Anglo-French wars of 1746 to 1763, after this scene. | climbed through the wreckage of the Carnatic's quarrels |
| 12 | 17 | `Protection money is what it was.` | **P1** `idiom` 20th-century gangster idiom. | A robber's toll is what it was. |
| 12 | 35 | `sends a message` ... `to be pushed around` | **P2** `idiom` "Send a message" and "pushed around" are modern idioms. | A king who builds walls tells the world he will not be bullied. ... not a chieftain's court to be shoved about with gifts and threats |
| 12 | 57 | `a strategic town` | **P2** `military` "Strategic" is 1820s. | Shenkottai, the town that held the passes on the southeastern frontier |
| 12 | 71 | `was overextended` | **P2** `military` 20th-century business and military term. | had stretched his arm too far |
| 12 | 125 | `Then we have a window` | **P1** `idiom` A "window" of opportunity is late 20th century. | Then we have a season |
| 12 | 131 | `Let the Marathas deal with the shadow` | **P3** `management` "Deal with" is on the author's watch list; easy to improve. | Let the Marathas see to the shadow at our back. |
| 12 | 141 | `testing our defenses` | **P3** `typography` American spelling; the house form is "defences". | testing our defences |
| 12 | 143 | `The irony was not lost on me.` | **P2** `idiom` Modern stock phrase. | Cut; 12:145 already makes the point. |

### Chapter 13 (`book2_chapter13_eve_of_colachel.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 13 | 13 | `anchors sabotaged` | **P1** `military` "Sabotage" is a 20th-century borrowing from French. | anchor cables cut in the night |
| 13 | 91 | `Mathoo Tharakan, a Syrian Christian merchant` | **P1** `names/facts` See 11:419. | As 11:419. |
| 13 | 93 | `their books are bleeding` | **P3** `management` Red-ink accounting image. | They are here because their ledgers show loss |
| 13 | 95 | `Your Highness` | **P2** `names/facts` British-era princely style (see house list, forms of address). | Their anger is cheaper than their pepper, Maharaja. |
| 13 | 105 | `Our spies in Sri Lanka` | **P1** `names/facts` See 2:55. | Our spies in Ceylon |
| 13 | 109 | `The Java War` | **P3** `scholarly` Historians' label; in 1741 it was the Chinese rising around Batavia. | "Trouble in Java," Ramayyan said |
| 13 | 113 | `understanding a man's strategy reveals his blindness` | **P2** `military` "Strategy" is 1810 in English; also 13:123 "A sailor's strategy" and 14:29. | Because knowing a man's plan shows you where he is blind. |
| 13 | 121 | `cardamom - the crown` | **P2** `typography` Spaced hyphen used as a dash (breaks the no-dash rule). | every measure of cardamom: the crown takes its share. |
| 13 | 123 | `A sailor's strategy` | **P2** `military` As 13:113. | A sailor's plan |
| 13 | 127 | `The centres of the pepper and cloth industry` | **P2** `management` "Industry" as an economic sector is modern. | The pepper and cloth markets are not on the coast. |
| 13 | 131 | `His career taught him` | **P2** `management` "Career" as a working life is 1800s. | His years at sea taught him |
| 13 | 141 | `the intelligence reports` | **P2** `military` Modern bureaucratic phrase; "intelligence" again at 13:145. | Ramayyan had shown me what his spies wrote |
| 13 | 153 | `a skeleton garrison` | **P3** `military` Early 19th-century military usage. | a starved garrison |
| 13 | 167 | `Professional soldiers.` | **P2** `military` Professional against amateur is a 19th-century distinction. | Paid soldiers, drilled for years. |
| 13 | 175 | `Block the outcome to the inland road.` | **P2** `typography` Wrong word: "outcome" means result (probably meant "outlet"). | Block the way to the inland road. |
| 13 | 187 | `You will patrol the perimeter.` | **P2** `military` "Perimeter" in the modern military sense; recurs at 14:31, 14:69, 17:5, 23:419. | You will ride the ring around them. |
| 13 | 199 | `a focused, tight ceremony` | **P2** `psychology` Modern "focused". | a short, close ceremony |
| 13 | 269 | `one of the oldest in the state` | **P1** `names/facts` "The state" reads as the modern Indian state of Kerala. | This house is one of the oldest on this coast. |
| 13 | 281 | `the focus of the cobra` | **P2** `psychology` Modern "focus". | I prayed for the cobra's stillness, the patience of the stone. |
| 13 | 289 | `we will have a conversation about queens and guests` | **P2** `psychology` Therapeutic phrasing. | we will talk of queens and guests |

### Chapter 14 (`book3_chapter14_charge_at_colachel.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 14 | 13 | `that foreign umbrella` | **P2** `idiom` Umbrella as political protection is a 20th-century figure. | were quick to stand in that foreign shade |
| 14 | 29 | `Strategy had shifted` | **P2** `military` As 13:113. | The plan had changed, just as Varma had promised. |
| 14 | 31 | `the gaolers of the perimeter` | **P2** `military` As 13:187. | We became the gaolers of the ring. |
| 14 | 61 | `terrifyingly efficient alliance` | **P3** `management` Modern "efficient". | It was a terrible alliance, and it worked. |
| 14 | 69 | `paced the perimeter` | **P2** `military` As 13:187. | a tall figure paced the edge of their shrinking fort |
| 14 | 71 | `looking over the casualty reports` | **P2** `military` Modern military paperwork. | looking over the lists of our dead and wounded |
| 14 | 73 | `They think they serve their nation` | **P2** `scholarly` Nation-state loyalty is a later idea, and 16:171 says these men came from half of Europe. | They think they serve their flag |
| 14 | 89 | `I believe in preparation meeting opportunity.` | **P1** `psychology` Paraphrase of a modern self-help maxim. | I believe in dry powder and open eyes. |
| 14 | 101 | `by the shockwave` | **P1** `tech` "Shock wave" is an early 20th-century physics term. | the breath driven from my lungs by the blast |
| 14 | 103 | `like leaves in a cyclone` | **P2** `tech` "Cyclone" was coined in 1848. | like leaves in a whirlwind |
| 14 | 105 | `They hit the powder room.` ... `muskets cooking off in the heat` | **P2** `military` "Powder room" now reads as a ladies' lavatory; "cooking off" is modern ordnance jargon. | They hit the powder store. ... muskets going off in the heat |
| 14 | 107 | `Secondary explosions rippled out` | **P2** `military` Modern ordnance jargon. | More blasts rippled out |
| 14 | 127 | `They were focused on the infantry ahead.` | **P2** `psychology` Modern "focused". | Their eyes were on the infantry ahead. |
| 14 | 131 | `The last hundred yards` ... `as they registered what was coming` | **P2** `time/measure` English yards; "registered" for noticing is modern. | The last long bowshot stretched like hours. ... as they saw what was coming |
| 14 | 141 | `one desperate pocket at a time` | **P2** `military` "Pocket of resistance" is a Second World War phrase. | cutting down each knot of men that still stood |
| 14 | 167 | `he had planned the supply lines` | **P2** `military` 19th-century military term. | he had planned the cart roads that kept our batteries fed |

### Chapter 15 (`book3_chapter15_prisoners_of_a_new_king.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 15 | 31 | `prisoners of the State of Travancore` | **P2** `names/facts` Formal "State of ..." is princely-state or modern usage. | You are prisoners of the Maharaja of Travancore. |
| 15 | 35 | `simply wave goodbye` | **P3** `idiom` Modern idiom. | Did you think we would simply let you walk away? |
| 15 | 45 | `a man realizes` | **P3** `typography` American -ize; the house form is -ise. | The moment when a man realises |
| 15 | 55 | `had been his identity since he was a boy` | **P2** `psychology` "Identity" in the psychological sense is 20th century. | the VOC mark he had served under since he was a boy |
| 15 | 141 | `They tried to reset. They tried to lock into the comfort of drill.` | **P1** `tech` "Reset" is a machine and computing image; "the comfort of drill" echoes "comfort zone". | They tried to form again. They tried to find the old steadiness of drill. |
| 15 | 145 | `It lasted minutes. It felt like an hour.` | **P2** `time/measure` Clock minutes. | It lasted no longer than milking a cow. It felt like a whole watch of the night. |
| 15 | 173 | `Mathoo Tharakan` ... `It was a statement as loud as any cannon` | **P1** `names/facts` Tharakan anachronism (see 11:419); "make a statement" is modern. | As 11:419. ... It spoke as loud as any cannon |
| 15 | 191 | `the vocabulary of the aftermath` | **P3** `scholarly` Academic register. | He knew enough of war to know that the beaten man does not choose the words. |
| 15 | 199 | `And books with too much red ink are burned` | **P1** `management` "Red ink" for losses is a 20th-century accounting idiom. | And ledgers that show only loss are burned |
| 15 | 201 | `It has already written you off` | **P2** `management` Figurative "write off" is modern. | It has already struck you from its books |
| 15 | 243 | `the corporate master` | **P2** `management` "Corporate" in the business sense is modern. | the indifference of the merchant masters he had served |
| 15 | 255 | `Ram will draw up the papers. You start tomorrow.` | **P2** `management` Job-offer phrasing. | Ram will write the leaves. You begin tomorrow. |
| 15 | 259 | `The war isn't over` | **P3** `typography` Contraction; dialogue elsewhere avoids them. | The war is not over |
| 15 | 273 | `Life is complicated` | **P3** `idiom` Modern platitude. | Cut the line; the next sentence carries it. |
| 15 | 277 | `the Travancore Nair Brigade` | **P1** `names/facts` "Nair Brigade" is the 19th-century name of the force under British paramountcy. | they had just become the seed of the king's new army |
| 15 | 319 | `is going to take some getting used to` | **P2** `idiom` Modern colloquial. | "The rice," he said, "will take time." |
| 15 | 321 | `Welcome to Travancore, Kappittan.` | **P3** `idiom` Modern greeting formula. | "Then you are Travancore's now, Kappittan." |

### Chapter 16 (`book3_chapter16_building_a_new_army.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 16 | 59 | `My mind would not stop replaying the moment` | **P1** `tech` "Replay" is a recording and sports image. | My mind kept going back to the moment |
| 16 | 105 | `She was giving me the choice to refuse.` | **P3** `psychology` Modern consent phrasing that also explains the subtext. | Cut. |
| 16 | 109 | `a repair panel` | **P3** `material` Modern builder's phrase. | the low wooden door in the corner that looked like nothing more than a patch in the boards |
| 16 | 171 | `Frenchmen fleeing conscription` | **P1** `names/facts` National conscription begins with Revolutionary France in the 1790s. Under the old regime men fled the militia drawn by lot. | Frenchmen fleeing the militia lot |
| 16 | 187 | `blind spots` | **P3** `tech` "Blind spot" is a 19th-century optics term. | where its teeth sat and where its blind corners lay |
| 16 | 201 | `forced to share space` | **P3** `idiom` Modern "share space". | because Ramayyan liked the results when we were forced to work side by side |
| 16 | 213 | `not the end of the world` | **P3** `idiom` Modern idiom. | that the first volley does not kill everyone |
| 16 | 219 | `a passing cavalry unit` ... `Too much risk of friendly fire.` | **P1** `military` "Friendly fire" is 20th-century military slang; "unit" is modern. | a passing troop of horse. "Too much risk of shooting our own." |
| 16 | 233 | `Our horses are not war machines that regenerate overnight.` ... `one dramatic impact` | **P1** `tech` "Regenerate" is a video-game image; "war machine" and "impact" are modern. | Our horses do not grow back overnight like grass. We cannot afford to lose them in piles for the pleasure of one great crash. |
| 16 | 265 | `a captain whose unit had improved` | **P3** `military` "Unit" in the modern military sense (pattern 3). | a brief word to a captain whose company had improved |
| 16 | 291 | `to be integrated into company-sized units` | **P1** `military` Modern military and administrative jargon. | began to send those men into companies under the king's officers |
| 16 | 295 | `rise through a system that recognised skill more than birth` | **P2** `management` "System" in the institutional sense. | younger men welcomed the chance to rise in a service that valued skill more than birth |
| 16 | 297 | `Padmini Amma navigated these shifts` | **P1** `management` "Navigate" is on the author's banned list (STYLE_SHEET section 4). | Padmini Amma met these changes with her usual sharp tongue and practical sense |
| 16 | 305 | `a mixed unit of Nair and Madurai infantry` | **P3** `military` As 16:265. | as we watched a mixed company of Nair and Madurai infantry fire in turn |
| 16 | 365 | `project our power into strange lands` | **P2** `military` "Project power" is modern strategic jargon. | imagined walls that would carry our flag into strange lands |
| 16 | 369 | `win - you had` | **P2** `typography` Spaced hyphen used as a dash. | Not because I thought you would win. You had already won. |
| 16 | 385 | `“Regret” I said.` | **P3** `typography` Missing comma after the quoted word. | "Regret," I said. |
| 16 | 391 | `enough overlapping fire` | **P3** `military` Modern "fields of fire" talk. | arguing over whether a particular angle let two bastions fire across it |
| 16 | 399 | `three spent cartridges` | **P1** `tech` Paper cartridges were torn open and rammed down the barrel; spent cartridges left on the ground are the brass cases of the 19th century onward. | They found only three torn cartridge papers |
| 16 | 401 | `taking potshots at their own fort` | **P2** `idiom` 19th-century idiom. | Our guards do not waste powder on their own fort. |
| 16 | 419 | `They do not like being told no.` | **P3** `idiom` Modern idiom. | They do not like refusal. |
| 16 | 435 | `a new unit march past` | **P3** `military` As 16:265. | when I watched a new company march past in neat order |

### Chapter 17 (`book3_chapter17_adoption_of_the_stranger.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 17 | 5 | `scanning the perimeter` | **P2** `military` As 13:187. | their eyes on the walls with the ease of men who expected trouble even in peace |
| 17 | 11 | `This is not a state visit.` | **P2** `names/facts` Modern diplomatic term. | This is not a court matter. |
| 17 | 49 | `a seamless expanse of black oxide` | **P1** `material` "Oxide" floors are 20th-century cement work and the word is 1790s chemistry. Also 17:159. The famous black floors were lime, burnt coconut shell and egg white. | a seamless floor of lime and burnt coconut shell, polished with egg whites |
| 17 | 61 | `pass my checkpoints without being searched` | **P1** `military` "Checkpoint" is a 1940s word. | Why her grain wagons pass my toll posts without being searched? |
| 17 | 81 | `it didn't reach his eyes` | **P3** `typography` Contraction plus stock phrase. | The King smiled, but his eyes stayed cold. |
| 17 | 99 | `even the gods' writing can be edited` | **P2** `tech` "Edit" as a verb is late 18th century and modern in feel. | even the gods' writing can be scraped and rewritten, if the ink is gold |
| 17 | 103 | `donation to the temple roof fund` | **P2** `management` Modern charity phrasing. | after a surprisingly generous gift toward the temple roof |
| 17 | 111 | `a *tharavadu* inclusion` ... `the matrilineal houses` | **P2** `scholarly` "Inclusion" is modern institutional language; "matrilineal" is 20th century. | a taking-in by the *tharavadu* ... the houses that pass through the mothers |
| 17 | 137 | `not as the strategist or the warlord` | **P3** `military` Both words post-date the period; mild. | not as the general or the conqueror |
| 17 | 145 | `four-storied complex` ... `the grammar of the wood and stone` | **P2** `material` "Complex" for buildings is modern; "grammar" of design is a critic's word. | with its four-storeyed hall ... but the manner of the wood and stone was the same |
| 17 | 157 | `The records will reflect it.` | **P2** `management` Modern bureaucratic formula. | "It will do. I will write it in the leaves." |
| 17 | 159 | `the black oxide floor` | **P2** `material` As 17:49. | soft on the black floor |
| 17 | 179 | `a *Thampuran* and trusted general` | **P2** `names/facts` Thampuran is a royal or Samantan title a Pillai could not hold. | a Pillai of Padmini's house and a trusted general of the king |
| 17 | 275 | `because you finally believe you deserve one` | **P2** `psychology` Self-help register. | But because you have finally stopped waiting to be sent away. |

### Chapter 18 (`book3_chapter18_dutch_come_bowing.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 18 | 13 | `priests heard confessions` | **P2** `material` Confession is a Catholic sacrament, not a temple practice. | In the temples, priests took offerings from men who had once taken Dutch bribes |
| 18 | 43 | `the Honourable Dutch East India Company` ... `restore relations based on mutual advantage` | **P2** `names/facts` Wrong company style (see 11:187); modern diplomatic register. | the Dutch Company conveys its regrets ... and wishes to return to friendship and trade, to the profit of both |
| 18 | 87 | `We would like stability` ... `trading partners` | **P2** `management` Modern economics vocabulary. | "We would like quiet on this coast," the envoy said. "... We would rather buy your pepper than fight for it." |
| 18 | 105 | `enthusiasm for consolidation` | **P3** `scholarly` Historian's word (see 10:185). | not all houses on this coast share the Maharaja's appetite for his neighbours' lands |
| 18 | 121 | `The entry marked HIGH.` | **P1** `management` A capitalised rating from a modern risk register. | Elayadathu. The name he had marked twice. |
| 18 | 157 | `the Treaty of Mavelikkara` | **P2** `names/facts` Ramayyan names a treaty signed ten years later, at a place not yet chosen. | But the real treaty, the one where you promise never to stand in our way again, that will come when we are finished with the north. |
| 18 | 199 | `Small victories add up` | **P3** `idiom` Modern idiom. | Small victories pile up |
| 18 | 247 | `or in obituaries` | **P2** `material` Newspaper register. | written in treaties or on funeral stones |

### Chapter 19 (`book3_chapter19_shadows_of_the_deccan.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 19 | 5 | `a single, clear front` | **P1** `tech` The weather "front" is a 1919 meteorological term. | Not as a single wall of cloud, but as a series of clouds |
| 19 | 23 | `Nagoji anna` | **P3** `names/facts` Marathi does use Anna for an elder, often a father, but Dada is the usual elder-brother word around Nashik; decide deliberately. | Nagoji Dada, |
| 19 | 101 | `The Maratha confederacy` | **P2** `scholarly` "Maratha Confederacy" is a 19th-century British historians' label; also 21:207 and 25:144. | The Peshwa's chiefs are a storm with many centres. |
| 19 | 139 | `Dutch paper to manage` | **P3** `management` "Manage" is on the watch list. | There is still Dutch paper to answer |
| 19 | 149 | `a clear expiry date` ... `I was an asset` ... `I would become a risk` | **P1** `management` Shop-shelf and balance-sheet vocabulary. | my usefulness had a season, like fruit. ... I was a sword worth keeping. ... I would become a danger. |
| 19 | 185 | `the stone *sil-batta*` | **P3** `material` Hindi term; a Marathi kitchen has the *pata-varvanta*. | the grinding stone keeping time with her morning prayers |
| 19 | 195 | `whose networks of trust ran deeper` | **P2** `management` "Network" of people is modern. | whose web of trust ran deeper than any royal decree |
| 19 | 197 | `Padmini Amma’s private vault` | **P3** `material` Banking "vault". | borrowed from Padmini Amma's strongroom |
| 19 | 263 | `Welcome home, Ananthan Pillai` | **P3** `idiom` Modern domestic formula, with "Dinner is ready" after it. | "Come in, Ananthan Pillai," she said. "The rice is served. Do not make us wait." |

### Chapter 20 (`book3_chapter20_guest_in_velinadu.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 20 | 5 | `levy schedules` ... `required for security` ... `no one who needed securing` | **P2** `management` "Schedule" and "security" in their modern senses; "levy schedules" again at 26:27. | letters about levy dates ... as if my presence were needed for her guard but attended by no one who needed guarding |
| 20 | 17 | `spotted the same thermal` | **P1** `tech` "Thermal" as rising air is a 1930s gliding term. | circling each other like two hawks over the same field |
| 20 | 113 | `the patrilineal certainty of the Marathas` | **P2** `scholarly` 20th-century anthropology word. | the Maratha certainty that a house passes from father to son |
| 20 | 141 | `the possible outcomes` | **P3** `management` Modern decision language. | He has already written three lines about how it might go |
| 20 | 171 | `on the Deccan plateau` | **P3** `scholarly` "Plateau" is a late 18th-century geographers' word. | racing horses across the Deccan |
| 20 | 175 | `does not believe in long engagements` | **P3** `idiom` Western betrothal idiom. | Revathi does not believe in long waiting. |
| 20 | 208 | `The bride deserves to know what she is getting.` | **P3** `idiom` Modern wedding-toast line. | The bride should know what she has taken on. |
| 20 | 280 | `practiced rhythm` ... `smelling of smoke and *jeera*` | **P3** `material` American spelling; *jeera* is Hindi (Kerala says *jeerakam*, Marathi *jire*). | practised rhythm ... smelling of smoke and cumin |
| 20 | 292 | `I solved a logistics problem` ... `The cooks merely executed.` | **P1** `management` "Logistics" is 1840s; "execute" in the management sense is modern. | "I had too many vegetables and too little time," he said without looking up. "The cooks did the rest." |
| 20 | 296 | `in one of his notebooks` | **P2** `material` Ramayyan writes on palm leaves. | He wrote it on one of his leaves. |
| 20 | 300 | `both nutritious and flavourful` | **P2** `idiom` Modern food-label register. | to make one pot that fed everyone |
| 20 | 302 | `the flavours layering on my tongue` ... `creamy and earthy` | **P3** `idiom` Restaurant-review language. | the tastes coming one after another ... soft and sour, the vegetables still holding their shape |
| 20 | 348 | `remove her jewelry` | **P3** `typography` American spelling. | She began to remove her jewellery |
| 20 | 404 | `I think I can do that.` | **P3** `idiom` Modern colloquial. | "Company," I said. "Yes. That I can do." |
| 20 | 414 | `The British and the French` | **P3** `names/facts` Contemporaries said "English" (see house list). | The English and the French still bargained with Arcot. |

### Chapter 21 (`book3_chapter21_ramayyans_ledger.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 21 | 5 | `filing the words away on some inner page` | **P3** `idiom` Filing idiom (pattern 9); the palm-leaf image is better without it. | as if he were already scratching the words onto some inner leaf |
| 21 | 45-49 | `First appearance:` ... `Skills: cavalry command, European engagement, adaptability.` ... `Risks: potential Maratha recall (mitigated by Velinadu bond), emotional ties northward, relationship with Revathi Bayi` | **P1** `management` A modern personnel file and risk register: "skills", "adaptability", "mitigated", "emotional ties", "relationship". | Rewrite in a revenue clerk's idiom, for example: "Came from the Goa ship, taken up by the fishermen. Rides well. Knows how Europeans stand and how they fall. Father a cultivator; mother; one younger brother. Holds to the Peshwa's name and his own honour, and each year more to the king. Watch: a letter from the north; his heart toward home; the Velinadu woman." |
| 21 | 63 | `Possible breaking points.` | **P2** `psychology` Psychological and engineering jargon. | Where he may give. |
| 21 | 69-72 | `Claims: legitimate under matrilineal law. Disposition: hostile.` ... `Leverage: significant.` ... `Risk assessment: HIGH. Timeline: before next monsoon.` | **P1** `management` Modern intelligence-brief format. | "Her claim good by the law of the mothers. Unfriendly. ... Holds Velinadu by blood. Dangerous. To be settled before the rains." (Adjust 21:74, "before next monsoon", to match.) |
| 21 | 102 | `Is that not... exhausting?` | **P3** `psychology` Modern emotional sense. | "Does it not wear you down?" I asked. |
| 21 | 123 | `merely delays the avalanche` | **P3** `material` Alpine image outside both men's world. | merely delays the flood |
| 21 | 203 | `I had been a prisoner number` | **P3** `material` Modern penal term. | There, I had been a number in a gaoler's book. |
| 21 | 207 | `machines like the Dutch company` ... `storm bent confederacies like my own` | **P3** `scholarly` Organisation-as-machine image and the "confederacy" label. | against the Dutch company with its thousand clerks and the Peshwa's storm of chiefs |

### Chapter 22 (`book4_chapter22_command_of_the_marches.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 22 | 61 | `Count the exits.` | **P3** `military` Modern security-drill phrase. | Count the ways out. |
| 22 | 75 | `the unblinking focus of a man` | **P2** `psychology` Modern "focus". | fixed on the heir with the unblinking stare of a man who has burned away every other thought |
| 22 | 109 | `The heir stood like a deer in torchlight.` | **P2** `idiom` A rewording of the 20th-century "deer in the headlights"; repeated at 24:491. | The heir stood rooted. |
| 22 | 111 | `His momentum carried us both forward.` | **P3** `tech` Newtonian physics term. | His rush carried us both forward. |
| 22 | 119 | `taking down their target` ... `a single moment of impact` | **P2** `military` Action-film idiom. | swore to die in the act of killing their man ... trained not for survival, but for a single blow |
| 22 | 155 | `Kanjav,` ... `pupils blown` | **P2** `material` Modern clinical jargon; the drug name is capitalised and roman here but italic in 23:427. | *Kanjavu*, chewed ... His eyes were wide, the black of them swollen, not with terror |
| 22 | 221 | `Then training took over.` | **P3** `idiom` Modern sports idiom. | Then my hands remembered their drill. |
| 22 | 381 | `So noted,` | **P2** `management` Courtroom formula. | "I will write it," he said softly. |
| 22 | 383 | `The rest we will handle as it comes.` | **P2** `management` "Handle" is on the watch list. | The rest we will meet as it comes. |
| 22 | 401 | `You managed a chaver` | **P3** `management` "Managed" is on the watch list. | "You killed a chaver," she said. |

### Chapter 23 (`book4_chapter23_first_campaign_for_the_tiger.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 23 | 37 | `a unit of musketeers and a small, mobile gun` | **P2** `military` Modern military terms. | a company of musketeers and a light field gun |
| 23 | 69 | `business never slept` | **P3** `idiom` Modern slogan. | as if to say that trade did not stop for gods |
| 23 | 103 | `walked the line between mockery and welcome` | **P3** `idiom` Modern idiom. | His tone sat halfway between mockery and welcome. |
| 23 | 177 | `to prove a point` | **P3** `idiom` Modern idiom. | Only fools stand in front of a cannon for pride. |
| 23 | 181 | `step over a tripwire that could be reset behind us` | **P1** `tech` Tripwire and reset are mechanical-trap images of a later age. | like being let past a snare that would be set again behind us |
| 23 | 191 | `establishing our new patrol patterns` | **P2** `military` Modern military jargon. | while we were still riding out our new patrol routes |
| 23 | 347 | `It makes for... vivid reading.` | **P2** `idiom` Modern book-review irony. | "It reads... like a butcher's tally." |
| 23 | 349 | `We secured the border` | **P3** `military` Modern military verb; echoed at 23:351. | "We held the border," I said ... "You held a slaughter." |
| 23 | 359 | `got out of hand` | **P3** `idiom` Modern idiom. | "It... ran away from me," I said |
| 23 | 361 | `That is for foot soldiers and berserkers.` | **P1** `names/facts` Berserker is Norse, known in English only from the 19th century, and outside this king's world. | That is for foot soldiers and chavers. |
| 23 | 363 | `I apologise, Your Highness` | **P2** `names/facts` British-era princely style (see house list). | "Forgive me, Maharaja," I said |
| 23 | 365 | `It better not` | **P2** `idiom` American colloquial. | "See that it does not," Ramayyan said. |
| 23 | 383 | `I saluted and left` | **P3** `military` European hand salute. | I touched my forehead and left |
| 23 | 419 | `the outer perimeter of the *belikal* stones` | **P2** `military` As 13:187. | We stood at the outer ring of the *belikal* stones |
| 23 | 427 | `A *chaver*.` ... `*kanjav*` ... `come to their mission` | **P3** `typography` Italics clash with ch22 (roman chaver, capital Kanjav); "mission" is mildly modern. | A chaver. ... They come to the task with *kanjavu* or *bhang* in their blood |
| 23 | 429 | `Ideally, my guards should have stopped him.` | **P3** `idiom` Modern sentence adverb. | My guards should have stopped him. |
| 23 | 457 | `I am fine` | **P2** `idiom` Modern "I'm fine". | "It is nothing," Marthanda Varma rasped. |
| 23 | 505 | `the political fallout` | **P1** `tech` "Fallout" is a 1950 nuclear term. | "Maharaja," Ramayyan started, "the other houses will talk..." |

### Chapter 24 (`book4_chapter24_under_de_lannoys_standard.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 24 | 7 | `a unit of cavalry and infantry move through a combined drill` | **P2** `military` Modern military terms. | watched a mixed body of horse and foot move through one drill together |
| 24 | 39 | `new levy structures` | **P2** `management` Modern organisational jargon. | when Ramayyan suggested new ways of raising men |
| 24 | 41 | `a force within a force` ... `when the monarchy changes` | **P3** `scholarly` Modern political phrasing. | an army inside the army ... when the throne passes |
| 24 | 49 | `We fight for the structure, then` | **P2** `management` Institutional abstraction. | We fight for the kingdom, then. Not the man. |
| 24 | 57 | `There you go with your unpleasant truths again` | **P2** `idiom` Modern colloquial. | "Again you bring me unpleasant truths," he said. |
| 24 | 59 | `Our partnership had settled into a rough rhythm.` | **P2** `management` Business "partnership"; again at 24:87. | Our work together had settled into a rough rhythm. |
| 24 | 63 | `Preventable deaths exhaust me.` | **P1** `management` Public-health jargon. | "It is all the same work. Deaths I could have stopped weary me." |
| 24 | 87 | `our partnership took root` | **P2** `management` As 24:59. | It was in such small, shared approvals that the two of us learned to pull together. |
| 24 | 165 | `Dismissed.` | **P3** `military` Modern drill formula. | Officers will wear them first. Go. |
| 24 | 177 | `Knowing and feeling are different animals` | **P3** `idiom` Modern idiom. | "Knowing and feeling are not the same horse," I said. |
| 24 | 179 | `wait for your feelings to catch up with your knowledge` | **P2** `psychology` Therapeutic register. | But I do not have time to wait for your heart to agree with your head. |
| 24 | 209 | `the company's books had written me off` | **P2** `management` As 15:201. | That the company's books had struck me out. |
| 24 | 239 | `I believed in their mission, their maps, their vision` | **P1** `management` Corporate mission-and-vision language. | I believed in their charter, their maps, their dream of what these coasts should become. |
| 24 | 407 | `Understood?` | **P3** `military` Modern drill-master tag. | Is that clear? |
| 24 | 413 | `Highness, the Maharaja's orders were...` | **P3** `names/facts` Address form; the heir apparent in Travancore was the Elaya Raja. | "Elaya Raja, the Maharaja's orders were..." |
| 24 | 429 | `when he overcommitted` | **P2** `idiom` Modern sports term. | swept his legs when he reached too far |
| 24 | 443 | `special treatment` | **P3** `idiom` Modern phrase. | Not once asked to be spared. |
| 24 | 491 | `stood like a deer in torchlight` ... `his own paralysis` | **P2** `psychology` As 22:109; "paralysis" in the psychological sense is modern. | stood rooted while men died around him. I cannot protect him from his own stillness. |
| 24 | 533 | `an extension of your body` | **P3** `idiom` Modern phrasing. | The kind where the horse is part of your body |
| 24 | 597 | `as a junior officer` | **P3** `military` 19th-century rank term. | Not as a prince, but as a young officer. |
| 24 | 661 | `What Lannoy saw was potential` | **P2** `management` Human-resources sense of "potential". | What Lannoy saw was promise |
| 24 | 673 | `Downrange, a wooden target exploded into splinters.` | **P1** `military` "Downrange" is 20th-century range jargon. | Across the field, a wooden target burst into splinters. |
| 24 | 679 | `was against company policy` | **P1** `management` Modern corporate phrase. | before they decided that teaching Indians to cast good bronze was against the company's interest |
| 24 | 687 | `a shipment of saltpetre` | **P3** `management` "Shipment" is early 19th century; again at 24:779. | We were inspecting a load of saltpetre |
| 24 | 749 | `currency exchanges` | **P3** `management` Modern financial phrase. | trade routes and the rates between coins |
| 24 | 753 | `Every transaction is a story.` | **P3** `management` Business-book aphorism. | Every bargain is a story. |

### Chapter 25 (`book4_chapter25_ramayyans_test.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 25 | 21 | `Putting out small fires along the northern border.` | **P2** `idiom` Office idiom for handling problems. | Riding from one small quarrel to the next along the northern border. |
| 25 | 90 | `move me from the 'risk' column in your books to the 'asset' one` | **P1** `management` Balance-sheet and risk-register terms. | "You want to move me from the column of men you watch to the column of men you keep." |
| 25 | 144 | `the confederacy` ... `matrilineal estates` | **P3** `scholarly` Historians' label (see 19:101) and 20th-century anthropology word. | if the Peshwa's chiefs wished to ride south ... that estates held through the mothers did not answer threats the way some fief holders did |
| 25 | 209 | `Burned the bridge himself.` | **P3** `idiom` "Burn one's bridges" is a 19th-century idiom; also 25:252. | Cut the rope himself. |
| 25 | 234 | `He reached out to us` | **P1** `management` "Reach out" in this sense is late 20th century. | He sent to us through a Marakkar trader |
| 25 | 240 | `Portuguese troop movements` | **P2** `military` Modern military phrase. | sending us word of where the Portuguese moved their soldiers |
| 25 | 248 | `with surgical precision` | **P2** `idiom` Modern idiom. | João's tools laid out as neatly as a barber's |
| 25 | 274 | `I let you have your moment` | **P3** `psychology` Modern phrase. | "I let you speak your anger," Ramayyan said. |
| 25 | 290 | `you can work with him directly` | **P3** `management` Modern management phrase. | now that you know, you can speak with him yourself |
| 25 | 296 | `I build the network` | **P2** `management` "Network" as above. | I build the web of eyes that tells us where enemies will strike |
| 25 | 312 | `men thinking of defecting` | **P3** `military` Cold War flavour. | who can ease the conscience of men thinking of changing sides |

### Chapter 26 (`book4_chapter26_fire_in_the_pepper_fields.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 26 | 27 | `levy schedules` | **P2** `management` As 20:5. | having come to argue over grain rates and levy dates |
| 26 | 57 | `We can drive them out of that corridor.` | **P2** `military` Military "corridor" is 20th century; also 26:69 and 26:157. | We can drive them out of that strip. |
| 26 | 135 | `A controlled burn` | **P1** `tech` Forestry term of the 20th century. | A fire held on a short rein, as far as any fire can be held in war. |
| 26 | 201 | `that the state will help replant, will support your house` | **P2** `management` Welfare-state phrasing. | that the treasury will pay for new vines and feed your house through the years |

### Chapter 27 (`book4_chapter27_the_last_of_the_old_houses.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 27 | 9 | `for breakfast and forgotten their names by dinner` | **P3** `idiom` Modern idiom. | They had swallowed kingdoms larger than Travancore in a single season. |
| 27 | 11 | `played games with the British and the French` | **P3** `names/facts` Contemporaries said "English"; also 27:13 and 28:165. | played games with the English and the French |
| 27 | 39 | `I became its caretaker` | **P3** `material` 19th-century word. | I became its steward |
| 27 | 55 | `The foreshadowing had been there for years` | **P1** `scholarly` A literary critic's term: the narrator is describing his own book. | The signs had been there for years |
| 27 | 63 | `“alternatives”` | **P3** `idiom` Political euphemism in scare quotes. | Letters intercepted that spoke of other masters for his land. |
| 27 | 69 | `pride is a powerful drug` | **P2** `psychology` Drug as an addiction metaphor is modern. | pride is strong toddy |
| 27 | 89 | `our forward positions` | **P3** `military` Modern military phrase. | as we watched supply carts move toward our siege lines |
| 27 | 101 | `Under the matrilineal laws of her house` | **P3** `scholarly` As 8:55. | Under the law of the mothers that ruled her house |
| 27 | 119 | `Sharp. Legitimate. Connected.` | **P2** `idiom` "Connected" for well-connected is modern; also a STYLE_SHEET fragment triple. | Sharp, with a good claim and powerful kin. |
| 27 | 145 | `fears the matrilineal law` | **P2** `scholarly` As 8:55. | Do you know why your king fears the law of the mothers? |
| 27 | 163 | `It was their last play` ... `through proxy` | **P2** `military` "Last play" is a game image; "proxy" war is a Cold War term. | It was their last throw, their attempt to win back through her hand what they had lost on Colachel's beach. |

### Chapter 28 (`book4_chapter28_servant_of_padmanabha.md`)

| Chapter | Line | Text | Problem | Suggested replacement |
|---|---|---|---|---|
| 28 | 5 | `in the monsoon month of 1750` | **P3** `names/facts` The Thrippadidanam took place in January 1750 (Makaram), the dry season. | in the month of Makaram, 1750 |
| 28 | 11 | `weighed, filed away` | **P3** `idiom` Filing idiom (pattern 9). | Her absence was noted and weighed. |
| 28 | 17 | `His Highness Sree Anizham Thirunal Marthanda Varma` | **P2** `names/facts` "His Highness" is the style fixed on Indian princes under British rule. | "Listen and witness. Sree Anizham Thirunal Marthanda Varma, Maharaja of Travancore..." |
| 28 | 33 | `Roman aurae` ... `a hoard vast enough to buy the Dutch East India Company three times over` | **P2** `names/facts` The coin list mirrors the 2011 vault inventory, not what an officer knew in 1750; "aurae" is wrong Latin (the plural of aureus is aurei); buying a company is a modern corporate image. | Gold from Rome and Venice and Holland, men whispered ... a hoard that could buy every Dutch ship on this coast. |
| 28 | 157 | `It silenced the internal threats.` ... `the external threats withered` | **P2** `military` Modern security-policy phrasing. | It silenced the enemies within. And with the house secure, the enemies outside lost heart. |
| 28 | 165 | `talking about shared interests` ... `The British have begun` | **P3** `names/facts` Diplomatic jargon; "English" per house list. | Mysore's man was here before that, talking of friendship. The English have begun building at Madras |
| 28 | 169 | `Consolidating for survival.` | **P3** `scholarly` Historian's word. | Gathering in, to survive. |
| 28 | 283 | `the kind the priest was selling` | **P2** `idiom` "Selling" an idea is a 20th-century sense. | just not the kind the priest was preaching |

## 4. Proposed house spelling list

Rule used to choose each form, in this order: (1) historically sound for the 1740s, (2) matches `glossary.md`, (3) matches the majority usage already in the text, so the fewest lines change.

Italics rule: italicise non-English common nouns every time they appear; set in roman proper nouns, titles and forms of address (Dalawa, Kappittan, Amma, Ayya, Maharaja), and words already in standard English dictionaries (dhoti, ghee, toddy, sardar, pagoda). Two frequent key words of the book, *chaver* and *kalari*, are treated as naturalised and set in roman because the text already does so almost everywhere.

| Term | House form | Style | Variants found (chapter:line) | Action |
|---|---|---|---|---|
| Kappittan | Kappittan; Valiya Kappittan | roman, capital (a title) | *kapitan* 4:97, 4:99, 4:119, 4:127, 5:3, 5:113; kapitan 4:111, 4:113, 18:179; Kappittan 15:223, 15:321, 16:409, 24:83 | One spelling, as in the glossary. Use it for the fishermen's name for Ibrahim too. |
| Valiya | Valiya | roman | Valiya 15:223; *Valia* 18:23 | Change 18:23. |
| Dalawa | Dalawa | roman, capital | diwan 6:41, 6:43, 6:69, 6:83, 6:85, 6:93, 6:103, 6:113, 6:127, 6:155, 6:161, 6:171, 6:183, 7:105, 10:13, 10:79; Diwanji 10:117; Diwan 14:167; Dalawa 11 times from 13:91 | Replace all 18. "Dewan" is a post-1809 Travancore title. If a Deccan flavour is wanted, let Nagoji think "diwan" once in Ch 6 and be told the local word. |
| Karyakkar titles | Valiya Karyakkar; Sarvadhikaryakkar | roman (titles, like Dalawa) | *Sarvadhi Karyakkar* 15:173; *Valia Karyakkar* 18:23; *Karyakkar* 19:201 | Sarvadhikaryakkar is one word in Travancore usage. The 15:173 appointment belongs to the Tharakan problem (11:419). |
| chaver | chaver, chavers | roman, lower case | roman 21 times (8:9, 19:181, Ch 22 throughout, 23:427 "chavers"); *chaver* 23:427, 23:469; *Chavers* 23:495 | Majority form wins; unitalicise the three in Ch 23. |
| kanjavu | *kanjavu* | italic, lower case | Kanjav 22:155; *kanjav* 23:427 | Malayalam form. |
| ola | ola, olas | roman | 8:13, 12:81, 25:3 | Consistent; keep. |
| tharavadu | *tharavadu* | italic | 8 uses, all italic | Consistent; keep. |
| mundu | *mundu*, *mundus* | italic | *mundu* 15:283, 15:301; mundus 7:17; mundu 23:425; "lungis" 4:25 | Kerala dress word. Keep "dhoti" (roman) only where Nagoji uses his own Deccan word. |
| konda | *konda* | italic, lower case | *Konda* 6:39 | Common noun. |
| huzurat | *huzurat* | italic | 1:7, 1:49, 5:145 | Capitalise at a sentence start: "*Huzurat* cavalry" (5:145). |
| bhau | *bhau* | italic | 4:29, 4:75, 6:15 | Consistent; keep. |
| Portuguese words | *marata*, *maratas*, *senhor*, *Este* | italic | *prisioneiro marata* 1:7; marata 1:31, 1:89, 2:13, 4:53; maratas 2:57; senhor 1:31; Senhor 24:319; Este 1:21 | Words left in Portuguese take italics, as 1:7 already does. |
| chuckram | *chuckram* | italic | *chuckrams* 8:41, 10:57 | Glossary spelling. Malayalam *chakram* is the alternative; choose one for text and glossary together. |
| varahan, pagoda | *varahan*; pagoda | varahan italic; pagoda roman | *varahans* 8:41; varahans 11:249; pagodas 7:151, 11:249; pagoda 12:117 | Italicise 11:249 "varahans". |
| candi | *candi* | italic | *candi* 10:57; candi 11:249 | Italicise 11:249. |
| hundi | *hundi*, *hundis* | italic | *hundis* 10:57; hundi 11:321; *hundi* 19:203 | Italicise 11:321. |
| kalanju | *kalanju*, *kalanjus* | italic | kalanjus 11:135, 11:141 | Italicise both. |
| Ettuveetil Pillamar | Ettuveetil Pillamar; the Pillamar; the Eight Houses | roman (proper noun) | *Ettuveetil Pillamar* 17:67; Pillamar 12:9, 17:73, 17:85, 24:545 | Set 17:67 in roman. |
| kalari | kalari | roman | 14 uses, roman | Consistent; keep. |
| sambandham | *sambandham* | italic | *Sambandham* 8:151, 8:183 (both sentence starts) | Fine; lower case if it ever falls mid-sentence. |
| sarpa kavu | *sarpa kavu* | italic, lower case | *Sarpa Kavu* 13:259 | Common noun. |
| Words in roman that should be italic | *angavastram*, *namaskaram*, *kumkum*, *yogakkar*, *chauth*, *sardeshmukhi*, *bhakri*, *nadaswaram(s)* | italic | angavastram 23:453; namaskaram 22:47; kumkum 13:201; yogakkar 10:151; chauth and sardeshmukhi 12:19; bhakri 9:56; nadaswarams 23:57 | Bring into line with *tali*, *prasadam*, *kanikka*, *belikal*, *nettipattam*. |
| Already consistent | *tali*, *prasadam*, *chenda*, *thimila*, *kanikka*, *belikal*, *nettipattam*, *nalukettu*, *madampi*, *sowcar*, *lingam*, *sambar*, *rasam*, *pappadam*, *avial* | italic | none | Keep. |
| Naturalised English words | dhoti, ghee, toddy, arrack, sardar, sahib, rupee, pagoda, godown, puja, durbar, lascar, guilder, rixdollar, cruzado, betel, jackfruit, chutney | roman | *chutney* 20:280 | Set 20:280 in roman. |
| talwar | talwar | roman | talwar 11:123, 13:221, 23:281, 24:781; sabre 7:89 | Change 7:89. |
| Hindi words in the wrong kitchen | cumin; the grinding stone (or Marathi *pata-varvanta*) | | *jeera* 20:280; *sil-batta* 19:185 | Replace. |
| Ceylon | Ceylon in European and court speech; Lanka in Indian speech | roman | Sri Lanka 2:55, 11:121, 11:129, 13:105; Ceylon 11:121, 16:169, 16:353 | Replace every "Sri Lanka". |
| Place names | Kollam, Shenkottai, Tiruchirappalli, Kochi, Anchuthengu, Kanyakumari | roman, no bracketed colonial form | Kollam (Quilon) 11:7; Sri Lanka (Ceylon) 11:121; Shenkottai (Shencotta) 12:13; Tiruchirappalli (Trichinopoly) 12:91 | Drop the brackets; the glossary carries the old names. |
| Ponnan | Ponnan | | Ponnam 7:17, 7:25; Ponnan 19 times | Change 7:17 and 7:25. |
| De Lannoy | De Lannoy; Lannoy | | "De Lannoy" 34 times, no variants | Keep. |
| The English | English (the people and their company) | | British 20:414, 27:11, 27:13, 28:165; English 10 times | Replace "British"; contemporaries said English (Angrez). |
| The Dutch company | the company (lower case); full names capitalised: the Dutch East India Company, the VOC | | company about 65 times; Company 22 times (e.g. 11:25, 11:187, 14:27, 15:55, 16:279, 16:353 to 16:373, 18:43) | Majority lower case. Drop "Honourable" (11:187, 18:43). |
| Addressing the king | Maharaja (Malayalam speakers may use Thampuran) | | Your Majesty 6:49; Your Highness 13:95, 23:363; Highness 17:21, 17:45, 17:59, 17:65, 17:141, 23:455, 23:487, 23:505 | No "Majesty" or "Highness". |
| Addressing the Rani and the heir | Rani (for the Senior Rani); Elaya Raja (for the heir) | | Highness 24:413, 24:467, 24:509; "His Highness" 28:17 (the herald) | As above. |
| king, heir, prince as common nouns | lower case, except before a name or in direct address | | King 54 times against king 253; Heir 22:87, 23:435; Prince 20 times against prince 6 | Lower case; the capitals cluster in Ch 17 and Ch 23. |

### Spelling and typography rules

- **British -ise and -our spellings.** Change: 15:45 "realizes", 7:161 "recognized", 16:69 "recognize", 20:280 "practiced", 12:141 "defenses", 20:348 "jewelry", 25:270 "pretense". Keep "judgment" (used consistently, three times).
- **toward, not towards.** 109 against 3; change 3:61 (twice) and 13:207.
- **dryly, not drily.** Change 17:79 to match 8:141 and 11:383.
- **The plural of cannon is cannon** (period usage, and the text's majority). Change the 11 "cannons": 11:427, 13:137, 13:147, 16:185, 16:299, 19:115, 23:21, 23:143, 24:675, 24:739, 28:157.
- **No contractions in dialogue.** The book avoids them except 15:259 "isn't", 17:81 "didn't", 23:329 "hadn't".
- **Dates in words.** 14:79 "the 10th of August" becomes "the tenth of August", matching 15:5 "the twelfth of August".
- **No spaced hyphens as dashes.** 13:121 and 16:369 (both in the table).
- **Letters and written messages** in italics, set off as block quotes. Now mixed: italic at 19:213 to 19:219 and 20:49; roman at 19:23 to 19:53, 25:35 to 25:60 and 25:334.
- **Stray leading spaces** at the start of paragraphs 23:417 to 23:529 and 25:165 to 25:198. Clean them in the 2e files.

### Time and measure for Nagoji

| Instead of | Use |
|---|---|
| minutes, seconds | breaths, heartbeats, "as long as it takes to milk a cow" (the old *godohan* measure) |
| half past eleven, clock times | before noon, at lamp-lighting, the second watch of the night |
| percent | one part in a hundred, one in ten |
| yards, miles | paces, a bowshot, a kos |
| pounds | a cartload, a bullock's load, so many maunds (Marathi *man*) |
| hands (horse height) | keep as translation, or "no higher than my chin" |
| hours, days, weeks, months | fine as translation; keep |

## 5. Out of scope, noticed in passing

Not register problems, but they surfaced during the full read and will be cheaper to fix in the same pass.

- **Kanka.** "the black horse Kanka ... his easy stride", shot by the Portuguese in Goa (1:7, 1:53 to 1:55), becomes "a black mare ... She had died at Vasai, a Portuguese ball through her chest" (7:145).
- **Nagoji's horses.** 7:183 says Kayal "would carry me through Colachel and beyond", but 8:89 has a gelding, 14:101 calls the Colachel horse "him", and 16:5 mourns Megha as "not as fine as the mount I had lost in the storm" (no horse was lost in the storm).
- **De Lannoy.** Born in Arras (15:291, 16:345 to 16:349) or in Zeeland (24:239); Arras is in Artois, French since 1659, not "a city in Flanders" (16:349). He says he is "forty-three" (16:361) against seventeen years of service from age seventeen (15:291, 16:353); the historical De Lannoy was about 26 in 1741.
- **Nagoji's past.** A captured *huzurat* rider in Ch 1, but "a fugitive" who "fled the Peshwa's justice" at 11:129, 12:71 and 12:145, and a veteran of "the Carnatic campaigns before my troubles began" (25:64), though that campaign was 1740, after his capture.
- **Dhanaji** "survived Goa's dungeons alongside me" (13:221) and "we washed up on this coast" (16:21), but Chapters 1 to 4 show only Keshavrao.
- **Chronology.** 19:181 remembers holding "a dying chaver's wrist while a king drove steel through his throat", an event of Chapter 22, where Nagoji himself cuts the throat. 28:5 places the Thrippadidanam in the monsoon and "three days" after Kottarakkara; it was January 1750.
- **Small slips.** 16:271 "when he said Tamil" (he did not); 10:75 "the queen in Padmanabhapuram" (the king or the treasury); 11:217 the envoy "realised she spoke his language" when she spoke Portuguese to a Dutchman; 17:145 "the Mint Palace" is not part of Padmanabhapuram Palace; 20:300 credits sambar to "King Sambhaji ... when he took refuge in the south" (the legend belongs to the Thanjavur court, and Sambhaji never took refuge there).
- **Typos and duplicated lines.** 8:87 missing closing quotation mark; 8:101 "in th house"; 9:112 and 9:128 repeat "She picked up a piece of plantain"; 9:114 and 9:116 are two speeches with no break; 10:23 "a Deccan non-Brahmins"; 17:185 "I understood them now." repeats 17:183; 18:151 missing full stop; 20:115 to 20:117 and 20:324 to 20:326 give Nagoji two speeches in a row (20:326 reads as Revathi's); 22:5 "mangotrees".
