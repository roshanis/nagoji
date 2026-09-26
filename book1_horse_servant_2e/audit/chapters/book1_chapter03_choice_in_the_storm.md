# Chapter 3 Audit: The Choice in the Storm

Source: `book1_horse_servant/book1_chapter03_choice_in_the_storm.md` (first edition, frozen; 231 lines, 2,845 words by `wc -w`). Line numbers are the physical lines of that file, blank lines included.

Adjudicated from two independent reports (a pattern auditor with 76 flags and a holistic reader with 23 suspect passages). Checked against a full read of the chapter; Chapters 2 and 4 read alongside; every later callback to this chapter (ch6:151, ch13:313, ch15:45, ch16:383, ch17:31-33, ch19:47 and 189, ch24:621, ch25:130); `STYLE_SHEET.md`, `VOICE_BIBLE.md`, `OPENINGS_ENDINGS_MOTIFS.md`, `REGISTER_AND_ANACHRONISM.md` and `REVIEW_BACKLOG.md`; and the sibling audits for Chapters 2 and 4 in this folder, so that the three chapters' fixes agree. Duplicates across the two reports are merged into single rows. The word-cut figure was measured on a scratch draft (kept outside the repo) with every confirmed fix and the three applied borderline trims in place.

## Verdict

| | |
|:-|:-|
| Severity | **3 of 5**: a noticeable pattern throughout, not pervasive |
| Recommended intensity | **Medium**: cut the tics and tighten. Re-voice at line level only in two stretches: the lead-in (L3 to L45) and the last page (L203 to L231). |
| Estimated word cut | **About 21 percent** (2,845 to about 2,230 words) |

The events of this chapter are sound and often very good. A ring bolt tears out "like a tooth being pulled from rotten gum". A guard promises "a ball in your gut". Nagoji reckons his odds in clipped soldier's shorthand at L181, and the rope "took the wrong kind of weight". The slop is not in what happens. It sits in a layer of commentary laid over the action:

- eight "not X, but Y" turns, one of them the first sentence;
- about a dozen maxims and one-line kickers, four of which make the storm a character with a punchline (L73, L161, L193, L211);
- twelve "for a moment / instant / heartbeat" time-stamps and five abstract uses of "world";
- nine similes where the style sheet allows two;
- a stack of five resolution devices after Keshavrao dies, while a wave is rearing.

Nearly every fix below deletes part of that layer. No event is lost, and neither is any line of dialogue that moves the plot.

The cut is twice the plan's 5 to 10 percent, as in the Chapter 2 audit, because the commentary sits in two thick clusters. One is the lead-in (L11 to L45), where a single dropped musket collects four devices and L45 then recaps a storm the reader has just lived through. The other is the page after Keshavrao's death (L209 to L231). Between L47 and L199 the chapter needs only trims.

Before and after (first edition counted by `audit/tools/scan_slop.py` plus a hand count; "after" counted on the scratch draft):

| Marker | First edition | After confirmed fixes |
|:-|:-|:-|
| "Not X, but Y" corrections in narration | 8 (L3, 17, 45, 85, 101, 107, 165, 205). The scanner finds 6 and misses L3 and L45 | 0 |
| "like a" similes / "as if" (ration 2 / 1) | 6 plus "Muskets are like horses" / 2 | 1 (L99, the tooth) plus the horses line / 1, in dialogue (L109) |
| "For a moment / instant / heartbeat" | 12 uses on 10 lines | 3 (L47, L185 "For a time", L203 "For a breath") |
| Abstract "world" | 5 (L75, 125, 145, 169, 199) | 0 |
| "loomed" / "hammered" | 3 / 3 | 0 / 0 |
| Fragment sentences | 13 | 2, inside the L181 reckoning (defended) |
| One-sentence paragraphs | 23 | 17, after the merges listed under Flab |

## Confirmed issues

| Line | Quote | Category | Suggested fix |
|:-|:-|:-|:-|
| 3, 5 | "The first warning was not the shout of a sailor or the crack of thunder. It was the change in the way the ship moved." / "with a certain patience ... her creaks and groans almost like a breathing beast. One night, as the air in the hold grew thick and hot, that rhythm snapped." | correction (first sentence of the chapter); hedged simile; stock atmosphere | Cut L3. L5 becomes: "Even in chains I had learned the gait of this hull. For days she had kept one pace over the long swells, rising and settling, and I had stopped feeling her under me. One night, in the heat of the hold, she broke stride." (A rider reading a moving body. See Opening.) |
| 7 | "Above, heavy boots thudded across the deck with new urgency." | stock tag | "Above, heavy boots thudded across the deck, running now." |
| 11, 13 | "I let the word hang and listened. Ships speak when they are in trouble. The strain of timbers changes." / "Now those voices were raised." | borrowed sea maxim (this is a landsman's first voyage) | "I did not answer. I was listening to the timbers, which had changed their note, and to the sailors above, who had stopped trading insults and started giving orders. Portuguese words rattled overhead, sharp and fast." (L13's first sentence goes; its second joins L11.) |
| 17 | "Not a cannon, but thunder, the long growl of a sky gathering its strength." | correction; stock personification | "Then, farther off, a deep boom rolled across the water. My shoulders hunched for a gun before my ears knew it for thunder." (The soldier's reflex does the work the formula was faking.) |
| 19 | "Rain hammered down in a sheet for a heartbeat ... Grey light poured into the hold" | continuity (it is night, L5); near-repeat of L163; time-stamp | "The hatch above us slammed open. Rain came through the square until a canvas was dragged across it. By the light of a lantern swinging at the hatch, the filth on the floor glistened." (Matches "the square of light" at L27 and L143.) |
| 25 | "No one laughed at his bravado. It is easy to make threats on solid ground. At sea ... every man knows he is at the mercy of things greater than muskets." | kicker (present-tense sermon) | Cut. L27 follows the threat directly. |
| 29 to 33 | "For an instant the hold went very still." / "They draw every eye in a space. Even men who have never fired one recognise the shape of power." / "The spell broke." | stock suspense beat; abstraction; modern "in a space"; stock phrase | One paragraph: "Every eye in the hold went to it. Muskets are like horses that way. Then the hull heaved once more, someone shouted, and a chain yanked tight." (Keeps the horse comparison the Voice Bible cites, and cuts the rest.) |
| 37 | "like something washed up by a strange tide. Too far to reach. Too close to ignore." | mirrored fragment pair; vague simile; contradicts L27 ("not far from me") | "The musket lay between us and the ladder, a body's length past the end of my chain." (It is near and out of reach, for a reason the reader can see.) |
| 39 to 41 | "“Sahib,” Keshavrao murmured, “if the ship breaks...” / “If the ship breaks,” I said, “no musket will save them.”" | repetition; mirrored exchange | Cut both lines. Keshavrao already asked "will the ship break?" at ch2:113, and Nagoji says it again at L57 ("Storms break ships"). "Them" has no clear referent. The same If/If frame returns at L131 to L133, which is the better one (see Defended). The Chapter 2 audit flagged this duplicate. |
| 45 | "The storm did not descend at once; it built in layers. First the tilt of the deck, then the drum of rain, then the cracks of closer thunder. Only when the first real wave hit us broadside did the men in the hold understand what it meant." | recap; correction; explained subtext | Cut. Open L47 with the one event it held: "The first big wave took us on the side. The ship rolled so violently..." |
| 59 | "His eyes were wide in the gloom." | stock beat, repeated at L171 | Cut, and leave "“Move where?”" untagged. Keep the eyes at L171 instead, because later chapters recall "Keshavrao's eyes in the storm" (see Defended). |
| 63 | "The hull groaned like an animal in pain." | stock simile (the second ship-as-beast) | "Another crash of water, and a groan from the timbers that went on too long." |
| 67 | "You have seen the dungeon. That is what awaits us at the end of this journey in another land." | dialogue exposition; "journey" is on the style sheet's banned list | "“Then we die here in the dark,” I said, “or in their cane fields, slower. Tell me which death you prefer.”" (It uses Keshavrao's own fear of the cane fields, ch2:87.) |
| 69 | "He swallowed. His Adam's apple bobbed against his collar." | stock beat; English Bible idiom | "His throat worked against the iron collar." (as REGISTER_AND_ANACHRONISM ch3:69) |
| 73 | "The storm grew teeth." | kicker; the storm as a character (1 of 4); "teeth" is reserved for Part IV | Cut. |
| 75 | "only violent, unpredictable lurches. The world narrowed to wood, iron, cold and noise. ... turning the hold into brief, harsh portraits of fear. Men clung to each other, to beams, to whatever they could find." | "the world narrowed to" formula; named emotion; doubled adjectives; reflex triple | "Soon there was no rhythm left in the ship, only lurches from any side. Lightning flashed through the gaps around the hatch cover and showed me faces for a blink at a time, mouths open, eyes screwed shut. Men clung to each other and to the beams." |
| 81 | "The ship shuddered as if struck by a giant hand. ... More shouting, this time with the edge of terror men do not bother to hide." | stock simile (it comes back in the last line); emotional label | "A new sound joined the rest, a long, splintering crack that ran through the hull and into our backs. Something heavy crashed on the deck above." (The cry for the pumps at L83 carries the terror.) |
| 85 | "not in thin sheets but in surges ... The cold stole breath." | correction; contradicts L43 (a trickle, never sheets); stock | "Now the water came in surges that smacked into our legs and bellies. Chains grew heavier as they dragged through it." |
| 89 | "He was right. If the ship sank with us still chained to the beams, the sea would fill our mouths before we even reached the surface." | explains the obvious; the logic fails (chained men never reach the surface) | Cut. |
| 97 | "We did not have to wait long." | stock transition | Cut. |
| 99, 107 | "The ring tore free from the beam" ... "perhaps the iron could be slipped, not from the cuffs themselves, but from the weakened timber." | continuity (the anchor tears out twice: L99, then L115); correction | L99: "The ring tore half out of the beam in a spray of splinters. The chain that held our section dropped a hand's breadth, yanking our collars and wrists, and caught." (The tooth simile is untouched.) L107: "I worked my hands along the slack chain until my wrists were near the bolt. The wood around it was ragged and soft, soft enough, perhaps, to give up the iron if we pulled together." |
| 101 | "Men screamed, not in pain but in wild, sudden hope." | correction; named emotion | "The men around us yelled, and one of them laughed out loud." |
| 105 | "The noise above would hide a great deal, but panic makes men loud. Loud men attract attention." | aphorism that explains the order just given | Cut. |
| 111 | "Muscles screamed. ... For a moment nothing moved." | stock strain beat; time-stamp | Cut "Muscles screamed." "For a moment nothing moved." becomes "Nothing moved." |
| 117 | "We stumbled, suddenly unmoored. ... our ankles still chained in pairs" | modern emotional metaphor; ambiguous blocking (each man's ankles, or two men chained together?) | "We fell back against each other. Our wrists were still shackled and our ankles still hobbled, but for the first time since Goa there was open space above our heads." ("Hobbled" is a horseman's word, and it settles who is bound to whom for L141, L177 and L229.) |
| 125 | "with a storm trying to tear the world apart above us. Yet the feel of slack iron at our throats did something to the spine that torture had not. It made men stand a little straighter" | explained subtext; vague depth | "Liberty was a generous word. We were still in a dark box, chained at wrists and ankles." Cut the rest. |
| 135 | "every step a battle against the water ... It was not loaded. Sensible men do not leave a primed weapon lying about." | stock collocation; a maxim that gets the event wrong (the guard fell and dropped it; he did not leave it) | "I sloshed forward against the water and the drag of the chain. My fingers closed around the stock of the musket. The pan was full of seawater. It would fire nothing tonight. Still, weight is weight, and a length of hardwood with an iron barrel can break a wrist or a skull more cleanly than bare hands." (A soldier knows a drowned pan when he sees one; see Notes.) |
| 143 | "backlit by a flash of lightning. For an instant he was only a silhouette" | photographic register ("backlit"; "silhouette" comes from a French minister of 1759 and entered English later still); time-stamp | "Halfway up, a figure filled the hatch, black against a flash of lightning, musket in hand." |
| 145 | "the word broken by fear and the tilt of the world" | named emotion; abstract "world" | "“Back,” he shouted, his voice gone high. “Back, or I fire.”" |
| 147 | "The ship chose that moment to lurch." | convenience phrase that shows the author's hand | "The ship lurched." |
| 149, 151 | "had trained my body to move in such instants before my mind could think." / "with all the force I could muster. It connected with his wrist." | body-before-mind formula; sports-commentary register | Cut L149. L151: "I had ridden at enough gaps in a line to know one when it opened. I drove the butt of the musket upward and caught his wrist. Bone cracked. His weapon spun away. He cried out, reaching blindly for support, and missed." (The cavalry lens stays, as a fact rather than an explanation.) |
| 153 | "with a wet, final sound. The water took him, rolling him against the planks like a piece of discarded cargo." | stock death cue; simile repeated at L169 | "He fell past me, hitting the rungs once, twice, then the flooded floor of the hold. He did not get up. The water rolled him against the planks." |
| 159, 175, 179 | "The hatch opened just aft of the mainmast, near the middle of the ship." / "on our starboard side, to my right" / "by the starboard rail at my right" | staging notes left in the prose; double glosses | Cut the second sentence of L159. L175: "on our right". L179: "A coil of rope lay half loose at my feet by the rail. Off the ship's side a shattered spar turned in the eddy." (This also drops "momentarily".) L171's "at the hatch by the mast" stays as the chapter's one piece of ship geography. |
| 161 | "The storm greeted me like an enemy who had been waiting." | personification simile (the storm as a character, 2 of 4) | Cut. |
| 163 | "Rain hammered down in sheets. ... what remained of the mast loomed at an angle, torn canvas snapping like flags of surrender." | repeats L19; "loomed" (1 of 3); a European literary simile | "Rain drove flat across the deck." and "Above, what remained of the mast leaned at an angle, rags of canvas cracking in the wind." The rest of the paragraph stands. |
| 165 | "Men fought everywhere. Not each other, but the elements. Sailors wrestled with lines, knives in their teeth ... hand levers that fed water from the bilges back to the sea" | correction; cliché; pump mechanics he would not know | "Sailors hacked at the tangled rigging, trying to cut the broken mast free before it dragged the ship over. Others heaved at the pump handles, their faces white in the lightning." |
| 169 | "To them I was just another piece of loose cargo tossed up from below. Their world had shrunk to ropes, timbers and the next wave." | explains L167; repeats the cargo simile (L153) and the "world narrowed" formula (L75) | Cut. "No one looked at me." (L167) does the work. |
| 175, 177 | "a wall of water lit silver for a moment by lightning. For that instant everything was clear." / "The broken mast. The men at the pumps. The open sea beyond, white-capped and hungry. ... The chain still linking his ankles. The iron still binding his wrists." | two time-stamps and a cue line; a six-fragment catalogue (the chapter's clearest single tell) | One paragraph: "Another wave reared on our right, higher than the rest, and lightning lit it from crest to foot. In that light I saw the broken mast, the men bent at the pumps, and Keshavrao's thin hands on the top rung, iron on his wrists, his ankles still hobbled." (An inventory sentence, which is how Nagoji sees: Voice Bible 3.4.) |
| 181 | "Calculations raced through me faster than words." | stock introduction | Cut, and start the paragraph at "Leap now, reach the spar." The reckoning itself stays. |
| 185 | "a force that tore screams from every throat ... For a moment I was nowhere, only a body in a cold, roaring universe. ... fingers clawed into that coil of rope." | stock phrase; modern cosmic abstraction | "It came down on the deck and flattened us. For a time I had no up or down, only cold water in my mouth and nose. Then the ship lurched up again, and I found myself on my knees, my ruined fingers hooked into that coil of rope." (First sight of his tortured hands in this chapter; see Notes.) |
| 187 | "His right hand still twitched at his side, reaching for a sword that would never come." | doom tag; impossible as written (both wrists ironed, clinging to the hatch) | Keep the Chapter 2 echo and drop the forecast: "Even now his right hand kept jerking toward his hip, as far as the irons let it, for a hilt that was not there." (It matches the Chapter 2 audit's wording at ch2:17, "a sword hilt that was not there".) |
| 193 | "The storm offered no time for noble speeches now." | meta kicker; the storm as a character (3 of 4); the speech at L227 undercuts it | Cut. |
| 199 | "Another wave loomed. ... For a moment the world became only grey and white." | "loomed" (3 of 3); time-stamp; abstract "world" | "Another wave came. The ship's bow plunged into it, and I could see nothing but white water." |
| 205 | "Not a man's body tied with intent, but the dead drag of something pulled by a force greater than any arm." | correction at the emotional peak; abstraction | Cut this sentence: "Then the line took the wrong kind of weight. The rope burned across my palm." |
| 211 | "the empty hatch, the broken ladder, the absence where his face had been. The rope burns on my palms throbbed, the only proof he had been there at all. The storm did not pause to mark his passing." | continuity (the ladder was never broken); "the absence where" formula; two stock grief lines; the storm as a character (4 of 4) | "I stared at the empty hatch. The rope had taken the skin off both palms, and blood was coming through the rags on my fingers. The next wave was already rising." (The rags stay on because ch4:43 and ch5:11 still show him bandaged.) |
| 215 | "On the field there was no room for hesitation." | explains the pact; takes the word "field" that L217 needs | Cut, so that "This was my field now." (kept) lands fresh. |
| 219 | "I wrapped the remaining coil of rope around my chest ... leaving the free end trailing. It was a poor excuse for a plan, but sometimes the gods look kindly on men who refuse to freeze." | continuity (the coil went over the side at L207, and ch4:7 has him tied to the spar); closing maxim; modern "freeze" | "A length of cut rigging lay across the deck at my knees. I wrapped it twice around my chest and knotted it as best I could with fingers that would not close, leaving a long end free to make fast to the spar." (The sailors cut the rigging at L165.) |
| 223 | "The sea clawed at the hull. ... the barnacles clinging to its underside." | stock personification; barnacles cannot grow on a spar that was aloft an hour ago | Join to L221: "I staggered to the rail. The spar rose on the swell, close enough now that I could see the raw splinters at one end and a tail of rigging still knotted round the other." |
| 225 | "I took one breath, tasting salt and fear. ... of his quiet “with you, sahib” in the dark." | cliché that pairs a taste with an emotion; misquotation (Keshavrao never said it) | "I took one breath and tasted salt. I thought of his narrow shoulders beside me in the hold, and of what he had said there in the dark: “I will follow wherever you jump, sahib.”" (His real words, ch2:117, moved here from L191.) |
| 227 | "“Forgive me,” I said, to the boy I promised not to leave, to the horse who died better than I would, to whatever gods listen to men who jump into storms." | rhetorical tricolon; generic gods; tense slip ("promised" for "had promised") | "“Forgive me, Rao,” I said." (Rao is what he calls Keshavrao at ch2:21 and ch2:75. See Borderline for the horse.) |
| 229, 231 | "The sea closed over my head like the hand of an angry god." | stock simile; repeats L81's giant hand; clashes with his scepticism (backlog C10-06) | Merge: "Then I hurled myself over the side, and the black water shut over my head." |

## Borderline

These are judgment calls. The recommendation is given, but each one could go either way without harm. The first three trims are already counted in the 21 percent estimate; the rest are not.

| Line | Quote | Issue | Recommendation |
|:-|:-|:-|:-|
| 191 | "He had said, in the dark below, that he would follow wherever I jumped." | A true callback, but it stalls the wave and needs L193 to explain it | Cut here. Put his exact words at L225, the pause before the jump (see the L225 row). Applied in the estimate. |
| 203 | "that I could haul him up and over the hatch, that we would stand together on the deck and leap in our own time." | Three false-hope clauses slow the fastest beat in the chapter | "For a breath I thought he had tied it, and that I could haul him up and we would go over the side together." Join it to L201 as one paragraph. Applied. |
| 207 | "vanished over the side, whipped away by retreating water" | Repeats "The wave receded" and the "whipped away" of L173 | "The rope peeled my skin and went over the side." Applied. |
| 47 | "Stomachs lurched." | Plural-noun montage, a rhythm the chapter repeats | Cut this one sentence. Keep the chains, the bodies and the man's arm. |
| 71 | "I prefer the one that involves a chance." | "involves" is office register, but this is the only trace of the camp joker from ch2:89 | "I prefer the one with a chance in it." Keep the joke. |
| 77 | "Above, voices rose in panic." | A small emotional label | "Above, the shouting rose." Or keep it, since the fragments at L79 show the panic anyway. |
| 109 | "“On three. ... One, two...”" | REGISTER_AND_ANACHRONISM rates "on three" P2 (modern convention) | Keep. Counting is his habit ("When he is afraid he counts", Voice Bible 1), and the count carries on to "On the fourth attempt" at L115. If it has to go, use the register audit's "When I say now". |
| 123 | "grabbing at iron, yanking at rings, kicking at weak points in the wood" | A parallel triple | It is an action list inside an honest-failure paragraph. Optional: "yanking at rings and kicking at the wood where it looked weak". |
| 141 | "Water slapped the underside of the deck in heavy blows." | Water in the hold cannot reach the underside of the deck. What he hears is the sea breaking on top of it | "Seas broke on the deck over my head in heavy blows." |
| 173 | "The word was whipped away by the wind." | Stock storm-dialogue beat | "I saw his mouth make the word more than I heard it." |
| 215 | "In the Deccan, before we rode into Portuguese fire, my troop and I had made a pact." | "pact" is formal for a troop's custom; the Portuguese fighting was in the Konkan, not the Deccan (see Notes) | "Before we rode down into the Konkan, my troop had a rule." Optional: the line can be read as a pact made on the plateau before the ride. |
| 227 | "to the horse who died better than I would" | This is the one clause in the triple worth saving: it answers "Then he died better than I will" (ch1:57) and keeps the title motif in view | Cut it anyway. The horse needs no forgiveness, the clause makes the address a list again, and it depends on Kanka's history, which is still unsettled (backlog BL-01, N-03). If the author wants the horse at the jump, give it a line of its own at L225, not a slot in the address. |

## Defended (flagged, but keep)

| Line | Quote | Flagged by | Why it stays |
|:-|:-|:-|:-|
| 5 | "She rolled and heaved" (the ship as "she") | holistic | Chapter 2 uses "she" and "her" for this ship throughout (ch2:51, 59, 129), and the sailors say "She is taking water" (L83). It is consistent, and the proposed opening turns it into a rider's "her under me". |
| 15 | "“Reef the sails... haul, haul... tie that down... move, you son of a dog...”" | holistic ("reef") | Portuguese heard in pieces and rendered in English. He understands more Portuguese than he admits (ch1:31-33), and the fragments with the insult left in are the most real sound in the opening. |
| 31 | "Muskets are like horses." | both | The Voice Bible (3.2) cites it as one of his home-made comparisons. The abstraction after it is cut, and it survives as "Muskets are like horses that way": the one proverb this scene is allowed. |
| 43 | "The air grew colder as wind forced itself into the seams." | pattern | It is concrete (wind forced through seams, water running with the slope of the boards) and not the style sheet's "air was thick with". |
| 47 | "for a few heartbeats we were almost weightless" | pattern (time-stamp tally) | This is the one literal time-stamp: a ship dropping out from under chained men. Keep it and let the other eleven go. |
| 57 | "“Storms break ships. When wood breaks, iron bolts pull out. Chains go loose.”" | both (predicts the escape) | This is Nagoji doing what he does: counting chances aloud, as in "All ships break" (ch2:115). The set-up and payoff with the ring is a craft choice, not slop, and Keshavrao spots the ring first (L91), so the plan is not a script. |
| 61 | "“Towards air,” I said. “Towards anything that floats.”" | holistic | His answers run shorter than the questions (Voice Bible 3.4). Only the spelling changes: "Toward" (see Notes). |
| 99 | "a sound like a tooth being pulled from rotten gum" | none; both praise it | The best simile in the chapter, and one of the two the ration allows. It comes from a body that has been tortured. |
| 109 | "“Pull as if you are trying to tear your own head off.”" | pattern (as-if tally) | A grim order in a commander's voice, spoken in dialogue. It is the one "as if" left. |
| 117 | "for the first time since Goa there was open space above our heads" | scanner ("first time") | It is literally the first time, and it matters. The style sheet exempts exactly this case. |
| 125 | "Liberty was a generous word." | pattern (kicker) | His shrinking humour (Voice Bible 3.3). It is the undercut, not a summary. The explanation after it is cut instead. |
| 127 | "“We need air. We need to see.”" | holistic | Spoken rhythm under pressure. The repetition is how an officer gives an order in a flooding hold. |
| 131 to 133 | "“If we take it,” Keshavrao said, “they will shoot us.” / “If we stay,” I said, “we may drown before they can load.”" | both | Keep this mirrored exchange and cut the one at L39 to L41. "Drown before they can load" is his gallows economy (Voice Bible 3.3, item 8), and the wet pan at L135 now pays it off. |
| 135 | "Still, weight is weight, and a length of hardwood ... can break a wrist or a skull" | pattern | A soldier's plain reasoning, and it plants the broken wrist at L151. Only "metal" becomes "iron". |
| 141 | "The ladder felt narrower than any siege stair I had ever mounted." | none | A comparison from his own life. The chapter needs more of these, not fewer. |
| 155 | "The ladder was clear." | pattern | A short sentence that carries a fact and cues the order at L157. This is how the Voice Bible says short sentences should work. |
| 167 | "No one looked at me." | holistic (as part of 161 to 169) | It shows what L169 then explains. Cut L169 and keep this. |
| 171 | "His eyes were huge in the storm light." | pattern (repeat of L59) | Later chapters pay this image off: "Keshavrao's eyes in the storm" (ch6:151), "on Keshavrao's face in the storm" (ch15:45), "eyes wide, mouth open" (ch19:47). Cut L59 instead. |
| 181 | "Leap now, reach the spar. Keshavrao follows, chains drag him under. Wait to free him, we both get smashed against the rail." | scanner (fragments) | The counting habit from ch1:93-95 in telegraphic form. It is the character thinking, not the author, and it is where the title's choice is made. |
| 183 | "The wave fell." | scanner (one-line paragraph) | A fact, and the hinge of the scene. |
| 187 | Keshavrao's right hand reaching for a missing hilt | both | OPENINGS_ENDINGS_MOTIFS rates it "Keep. An earned two-beat" with ch2:17. Only the doom tag and the physics change. |
| 209 | "Keshavrao was gone." | pattern (kicker) | The key beat. It earns its own line once the recap at L211 is gone. |
| 215 | "If a man fell, the others rode on. We would mourn later, in camp, with liquor and song and stories." | both (backstory, polysyndeton) | The Voice Bible (3.5) names this as one of his four channels for grief: soldier's custom. The triple is made of camp nouns, not abstractions. "Song" quietly answers Keshavrao, the camp singer (ch2:89). The pact is planted nowhere earlier, but it is short and in his idiom. |
| 217 | "This was my field now." | both (kicker, thesis) | The Voice Bible cites it with L215. It is the hinge from memory back to action, not a restatement, and it works once L215's "On the field there was no room for hesitation" is cut. |
| various | spar, hatch, scuppers, mainmast, "starboard" once | holistic (sea vocabulary a Nashik horseman would not own) | He writes in the 1740s and 1750s, after years among Marakkar seamen and after Colachel, and the Voice Bible's lexicon lists spar and hatch. The tell was the double glosses ("on our starboard side, to my right"), and those are cut under L159. "Bilges" goes with the L165 rewrite. |

## Opening

Current first lines (3 to 5):

> The first warning was not the shout of a sailor or the crack of thunder. It was the change in the way the ship moved.
>
> Even in chains I had learned the rhythm of this hull. She rolled and heaved with a certain patience, rising over long swells and settling again, her creaks and groans almost like a breathing beast. One night, as the air in the hold grew thick and hot, that rhythm snapped.

Verdict: **rewrite.** The first sentence is the "It was not X. It was Y." opener, which a practised reader spots at once. It names two stock sounds only to wave them away, and then the paragraph explains the ship instead of letting us feel it. The second paragraph holds the chapter's best unused idea: "Even in chains I had learned the rhythm of this hull." A *huzurat* rider whose horse was shot under him feels a change in a moving body before he hears one. That lens should carry the opening, in place of "a breathing beast".

Proposed opening (replaces 3 to 5):

> Even in chains I had learned the gait of this hull. For days she had kept one pace over the long swells, rising and settling, and I had stopped feeling her under me. One night, in the heat of the hold, she broke stride.
>
> The roll sharpened. ...

"Gait", "pace", "under me" and "broke stride" come from the saddle, and none of them needs "like", so the simile ration stays free for the tooth at L99. L7, where the chapter really starts (chains jerking, a man retching, boots running), follows unchanged apart from its last clause.

Coordination with Chapter 2: the Chapter 2 audit cuts ch2:129 to 131, where the timbers creak "in a new rhythm" and the ship rolls more sharply, so that the storm is not begun twice, and it ends Chapter 2 on the twelfth mark scratched in the plank. "For days" and "One night" depend on that change. If Chapter 2 keeps its storm-onset ending, use "That night" here and drop "For days".

The rest of the lead-in (L7 to L45) is slow for a storm chapter. The storm is built in six stages (L7, 13, 17, 19, 27, 43), L45 recaps them, and the dropped musket collects four devices (L29, 31, 33, 37). The cuts at L11, 25, 29 to 37, 39 to 41 and 45 take about 250 words out of the lead-in without losing one event.

## Ending

Current last lines (225 to 231):

> I took one breath, tasting salt and fear. I thought of Keshavrao's narrow shoulders in the hold, of his quiet “with you, sahib” in the dark.
>
> “Forgive me,” I said, to the boy I promised not to leave, to the horse who died better than I would, to whatever gods listen to men who jump into storms.
>
> Then I hurled myself over the side.
>
> The sea closed over my head like the hand of an angry god.

Verdict: **revise.** OPENINGS_ENDINGS_MOTIFS counts this as the only chapter in the book that ends on action, and that should stay. What fails is the approach to the jump and the last image. After "Keshavrao was gone." (L209) the page stacks resolution devices one after another:

- the absence and the "only proof" line (L211);
- the indifferent storm (L211);
- the maxim (L219);
- "tasting salt and fear" (L225);
- a three-part address to boy, horse and gods (L227);
- a generic god-simile (L231) that repeats the "giant hand" of L81.

Each device settles guilt that the rest of the book needs to carry. Chapter 19 says "And I had let go" (ch19:189), and that only works if Chapter 3 leaves the loss raw.

The plot stays exactly as written: the rope goes over the side with Keshavrao on it, and Nagoji jumps alone. What changes is that his tortured hands, absent from the whole chapter, finally show. They are what failed on the rope. That lets Chapter 19's "I had let go" stand as a survivor's guilt rather than a contradiction.

Proposed ending (replaces 209 to 231):

> Keshavrao was gone.
>
> I stared at the empty hatch. The rope had taken the skin off both palms, and blood was coming through the rags on my fingers. The next wave was already rising.
>
> The spar I had seen floated closer, riding the foam just off the rail.
>
> In the Deccan, before we rode into Portuguese fire, my troop and I had made a pact. If a man fell, the others rode on. We would mourn later, in camp, with liquor and song and stories.
>
> This was my field now.
>
> A length of cut rigging lay across the deck at my knees. I wrapped it twice around my chest and knotted it as best I could with fingers that would not close, leaving a long end free to make fast to the spar.
>
> I staggered to the rail. The spar rose on the swell, close enough now that I could see the raw splinters at one end and a tail of rigging still knotted round the other.
>
> I took one breath and tasted salt. I thought of his narrow shoulders beside me in the hold, and of what he had said there in the dark: “I will follow wherever you jump, sahib.”
>
> “Forgive me, Rao,” I said.
>
> Then I hurled myself over the side, and the black water shut over my head.

It ends on action and a physical image, in words Nagoji owns. Keshavrao's real promise is now quoted at the moment Nagoji jumps without him, so the irony does the work the address used to do. "Rao" is the name he used for the boy in the hold. "The black water" is the phrase later chapters use when they remember the wreck ("as Keshavrao vanished into the black water", ch13:313; "died in the black water", ch19:259). The last line matches the fix proposed in OPENINGS_ENDINGS_MOTIFS. Chapter 4 opens "When the sea finally spat me out", so no closing flourish is needed.

Alternative, if the author wants sound at the jump: the war cry his troop rode with ("Har Har Mahadev") in place of "Forgive me, Rao" would tie the jump to the pact. It is a weaker choice, because it swaps grief for a charge. Either way, the generic plural "gods" should go.

## Flab (passages to tighten)

| Lines | Issue | Fix |
|:-|:-|:-|
| 3 to 13 | A corrective opener, two explanations of how ships behave, then the raised voices shown anyway | Rows 3 to 5, 11 to 13 |
| 25 to 41 | A threat sermon, then four devices around one dropped musket, then a repeat of Chapter 2's ship-break question | Keep L27's action, one proverb and the chain-length fact; cut L25 and L39 to L41 |
| 45 | A pure recap of a storm the reader has just lived through, line by line | Cut |
| 81 to 89 | A giant-hand simile, a terror label, a correction and an explained danger around one good cry for the pumps | Rows 81, 85, 89 |
| 97 to 117 | A stock transition, an emotion label and an aphorism, plus the release told twice (the ring tears free at L99, then the bolt again at L115) | Rows 97 to 111; settle on one release (half-torn ring, then bolt) |
| 125 | Everything after "Liberty was a generous word." explains it | Keep the first two sentences |
| 143 to 153 | Four time-stamps and stock beats in one ten-line fight | Rows 143 to 153 |
| 159 to 169 | A staging note, the storm greeting him, a correction, and a paragraph explaining "No one looked at me" | Rows 159 to 169 |
| 175 to 181 | Two time-stamps, a cue line, a six-fragment catalogue and "Calculations raced" before a reckoning that needs no introduction | Rows 175 to 181 |
| 185 to 193 | "Universe", a doom tag, a callback explained, then a meta line, all while a wave breaks | Rows 185 to 193 and the L191 borderline |
| 203 to 231 | The resolution stack (see Ending) | See Ending |
| whole chapter | 12 time-stamps (L19, 29, 47, 111, 143, 175 twice, 185, 199, 203, 211 and "such instants" at 149) | Three are left: L47, L185, L203 |
| whole chapter | 23 one-sentence paragraphs used as a drumbeat | The cuts remove the kicker ones (29, 73, 97, 149, 161, 193, 231). Also merge L13 into L11, L33 into the new L29, L177 into L175, and L203 into L201. That leaves 17, nearly all of them actions or facts. |
| whole chapter | "world" 5, "loomed" 3, "hammered" 3, "whipped away" 2, the cargo simile 2, the ship as a beast 2 | All handled in the rows above |

## Passages to protect

- L7: "our chains jerked and bodies slid against one another. A few men cursed. One began to retch." The chapter's real first paragraph.
- L15: the Portuguese orders heard in pieces, the insult included.
- L23: "we put a ball in your gut and throw you over." Crude and practical, and it sets up the musket.
- L27: the musket clattering down the ladder and coming to rest against a beam. Precise, with no commentary.
- L35: "The pigs below are not our problem if the mast goes." It prices the prisoners without narration.
- L47 (last sentence): "a man screamed as his arm bent under another's weight at the wrong angle."
- L51 to 55: "Hook your arms over the wood above", then "It was useless advice for some." Know-how, with the admission.
- L71: Keshavrao's joke, the only trace of the camp singer. Change one word at most.
- L79, L83: the sailors' fragments, including "pump, for the love of God".
- L93: the ring and the cracks spreading around the bolt as the hull flexes. A mechanism the reader can watch.
- L99: "a sound like a tooth being pulled from rotten gum".
- L109: "Pull as if you are trying to tear your own head off."
- L115: "timing our efforts with the wildest rolls of the ship. On the fourth attempt". A horseman's timing and his count.
- L117: "for the first time since Goa there was open space above our heads".
- L123: rings "buried in sound timber that would not yield". They cannot free everyone, and nobody makes a speech about it.
- L125: "Liberty was a generous word."
- L135: "weight is weight".
- L141: "narrower than any siege stair I had ever mounted".
- L181: the clipped reckoning.
- L187: "Blood ran from somewhere on his forehead, thin in the rain."
- L195: the rope that "slapped wetly against the deck, then slipped". The rescue fails on the first try, and you can hear it.
- L201, L205 (first sentence), L207: "The rope went taut in my hands." / "the wrong kind of weight" / "The rope peeled my skin". The peak of the chapter, and it works because it stays physical.
- L209: "Keshavrao was gone."
- L215 to 217: the troop's custom and "This was my field now."

## Chapter-specific notes

1. **His hands (missed by the pattern audit).** Chapter 1 pulls his fingernails, ch2:123 has his "bandaged hand", ch4:43 has "the bandages ... around my ruined fingers" and ch5:11 "the bandaged hands ... the rope burns". In this chapter he climbs, strikes, hauls and knots rope as if uninjured. The fixes at L185, L211 and L219 bring the hands in at three points without adding a scene. The bandages must stay on to reach Chapter 4.
2. **The rope (continuity).** At L207 the rope goes over the side, yet at L219 he wraps "the remaining coil" around his chest and leaves the end trailing. Ch4:7 then says the rope "had come free of the spar", though he never tied it to one. The L219 and L223 fixes use cut rigging (set up at L165), leave a long end "to make fast to the spar", and put a tail of rigging on the spar itself. Chapter 4's line then works as written, as the Chapter 4 audit keeps it.
3. **The irons.** He jumps hobbled and in wrist irons (L117). His own reckoning at L181 says chains drag a man under. The Chapter 4 audit handles the irons on the beach (a fisherman strikes them off; backlog N-20). Optional here, for honesty at the rail: "The irons would drag at me as they would have dragged at him." Not included in the estimate.
4. **The seam with Chapter 2.** Chapter 2 ends on the storm's onset ("the timbers creaked in a new rhythm", ch2:129), and Chapter 3 opens on "The first warning". The Chapter 2 audit cuts ch2:129 to 131, and this audit's opening ("For days ... One night") assumes that cut. The two must be adopted together, or the fallback in Opening applies.
5. **Wet powder.** Ch2:27 shows the Goa musketeers with matchcords. Whether the ship's guards carry matchlocks or flintlocks, no pan stays dry at a hatch in this rain, and a Maratha trooper would know it. The L135 fix gives him that knowledge. It also makes the second guard's "Back, or I fire" hollow in a way Nagoji can read, which explains why he climbs into a levelled musket.
6. **The guard's death and Chapter 17.** "He did not get up" (the L153 fix) keeps the first edition's implied kill. Ch17:33 has "It was two men. The third I only broke", and so far Chapters 1 to 3 show one death. This is logged as backlog N-41; decide the count there.
7. **Keshavrao's death retold.** This chapter is the source of truth: he was tied or tangled in the line, the wave took him, and the rope ran out through Nagoji's hands. Later mentions drift ("a rope that broke", ch19:181; "Keshavrao's hand slipping from the rope", ch16:383 and ch24:621; "the rope slipped from his grasp", ch25:130; seeing his face go under, ch19:47). Backlog N-39 asks that they match Chapter 3. The ruined-fingers detail is what makes "I had let go" (ch19:189) true as guilt.
8. **Geography of the pact (L215).** Ch1:11 puts the fighting "along the Konkan", and the 1737 to 1739 campaign under Chimaji Appa was fought below the ghats (Salsette, Thana, Vasai, Chaul). "In the Deccan, before we rode into Portuguese fire" can stand if the pact was sworn on the plateau before the ride down; otherwise use "Before we rode down into the Konkan". This matches the Chapter 2 audit's note on Nashik.
9. **Kanka.** Cutting the horse clause at L227 removes one more place that assumes the first-edition capture story (ch1:57), while Kanka's sex and death are still unsettled (backlog BL-01, N-03). If the author restores the clause, check it against whichever horse history wins.
10. **"Toward" / "towards".** L61 has the book's only two "Towards" against 109 uses of "toward". Use "Toward air" and "Toward anything that floats".
11. **Scanner gap.** `scan_slop.py`'s `not_but` marker missed L3 ("was not ... It was", across a sentence break) and L45 ("did not ...; it built"). Worth adding both shapes before the re-scan, so the after-count for this chapter is honest.
12. **Word notes for the line edit.** "Silhouette" (L143) postdates the narrator: it comes from Étienne de Silhouette, the French minister of 1759. "Journey" (L67) is on the style sheet's banned list. "Unmoored" (L117), "universe" (L185) and "refuse to freeze" (L219) are modern emotional registers. All are handled in the rows above.
