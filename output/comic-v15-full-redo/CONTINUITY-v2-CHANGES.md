# CONTINUITY v2 draft: change log

Consolidates every bible proposal found in the ch2 to ch28 script adaptation notes and
script-reviews into `CONTINUITY-v2-DRAFT.md`. `CONTINUITY.md` (v1) was read but not edited.

Two items were pre-decided by the author rather than drawn from the scripts, and are applied
verbatim, superseding every competing script proposal:

- **Dhanaji's look** (superseding differing proposals in ch11, ch12, ch13 and ch14).
- **The Portuguese brand's location and appearance** on the inner LEFT forearm, a hand's width
  above the wrist (superseding differing proposals in ch4, ch5, ch8, ch9 and ch17, which variously
  called it a "crude cross" on the upper arm or outer forearm).

A note on a repeated false alarm: five scripts (ch2, ch6, ch8, ch13, ch18) flag that the bullet
`- **Ibrahim Marakkar** ("kapitan"):` does not parse as its own continuity block and gets merged
into Keshavrao's. Checked against the current `CONTINUITY.md` and `pipeline/script_pipeline.py`:
this is already resolved. `_continuity_blocks`'s bullet regex matches the parenthetical fine, and
`ibrahim` already resolves to its own block (confirmed in the VERIFY output below). No bible or
pipeline change was needed for this.

## 1. Table of changes

| Entry | Old | New | Source chapters |
| --- | --- | --- | --- |
| Nagoji, constant identity | No pre-capture look specified | Added: in memory panels before his capture, plain Maratha cavalry dress matching the commander sheet, hands unbandaged | ch6 (also needed by ch10) |
| Nagoji, row 1-3 | "...ankle irons, barefoot, hair loose. No turban." | Added: from ch2 a hinged collar and wrist chain, from ch3 a hobble chain on the ankle cuffs; staging note to keep the left arm hidden; noted that ch4 shows none of this with no explanation | ch2, ch3 |
| Nagoji, row 4 | "Portuguese brand visible on his upper arm" | Brand moved to the inner LEFT forearm, a hand's width above the wrist; described as a pale puckered patch of raised ridges, blurred past reading, no letters, no numerals, not a cross | Author lock (see above) |
| Nagoji, row 5-6 | No page-level override | Added: ch5 pages 1-2 costume override (bare-chested, captivity dhoti, no shirt, clean linen hand wraps, rope burns, chafe rings, no irons) before he is given village clothes on page 3 | ch5 |
| Nagoji, row 7-16 | "brand on the left wrist or forearm" | Brand reworded to match the inner LEFT forearm location; added the long, thin white forearm scar from ch9 onward, beside the brand | Author lock; ch9 |
| Nagoji, row 17-27 | "Ch22: bound shoulder and cut palm after the temple fight."; "Ch24 onward in uniform" | Added first grey/brand/scar continuity from ch16; added the ch17 pages 8-10 bare-headed transition; reworded the ch22 wound (uninjured until the fight, healed by ch23); reworded ch24 to "from the issue of the coats (script page 14) onward" | ch17, ch22, ch24 |
| Nagoji, row 28 epilogue | No scoping note | Added: the later-life sheet is for the true epilogue only; ch28 pages 1-5 use the ch17-27 look, the uniform returns at the fort from page 6 | ch28 |
| Marthanda Varma | One bullet: "Court" and "Ch28 dedication" only | Added ch6/ch11 court additions (shoulder cloth, rudraksha), the ch11 informal war-hall look, the ch7 beach and field look, the ch16 Tiruvattar look, the ch22 hill-shrine and fort-room looks, the ch23 shoulder wound, the ch21 festival-memory look, and the ch28 sacred thread. The turban-versus-bare-head disagreement is flagged, not resolved (see Conflicts) | ch6, ch7, ch11, ch16, ch21, ch22, ch23, ch28 |
| Padmini Amma | No blouse note | Added "no stitched blouse" | ch8 |
| Revathi Bayi | No funeral look | Added ch27 funeral: plain white, no jasmine, no gold except the tali | ch27 |
| Keshavrao | Generic prisoner description | Added the ch2 lock: about nineteen, faint moustache, grey-brown tunic, no ear stud | ch2, ch3 |
| Ibrahim Marakkar | Build, scar, ch6 coat only | Added white turban and grey-flecked beard from ch4; pale vest over white mundu through ch5; ash on his forehead from ch5 5.3 | ch4, ch5, ch6 |
| Eustachius De Lannoy | Coat timeline without the tricorne or the ch15 injury | Added the ch11 black tricorne; added the ch15 linen hand/wrist bandage and the change into a white mundu, tunic-coat and sandals | ch11, ch15 |
| Ponnan | No mount detail | Added bare knees; rides a smaller Maravar horse, a head lower than Nagoji's | ch14, ch26 |
| Dhanaji | "a Deccan rider of Nagoji's generation, talwar" | Full author-locked look (see above) | Author lock (supersedes ch11, ch12, ch13, ch14) |
| Mathoo Tharakan | Gold cross and white cloth, then silk and chains from ch15 | Added the dark maroon tunic and small St Thomas cross, so he reads as a lay noble | ch15 |
| The Prince / heir | Ages only | Added the ch17/ch22 costume (small white mundu, thin gold chain, small topknot) and the ch23 refinement (uncle's cheekbones, watchful eyes, white silk mundu) | ch17, ch22, ch23 |
| New entry: Chanda Sahib | (none) | Added: never shown face-on, build and dress, his riders' dress | ch11, ch12, ch25 |
| New entry: Gustaaf Willem van Imhoff | (none) | Added | ch11 |
| New entry: Dutch envoys | (none) | Added two distinct delegations (ch11 and ch18) | ch11, ch18 |
| New entry: Yusuf Marakkar | (none) | Added | ch10, ch18, ch23 |
| New entry: Nagoji's father | (none) | Added | ch19 |
| New entry: Nagoji's mother | (none) | Added | ch19 |
| New entry: Bhalerao | (none) | Added | ch19 |
| New entry: the Gujarati sowcar | (none) | Added | ch19 |
| New entry: Joseph Donnadi | (none) | Added | ch15 |
| New entry: the Madurai troop | (none) | Added | ch7, ch8, ch13 |
| New entry: the Kollamkara Raja | (none) | Added, with his raiders' dress and banner | ch23, ch26 |
| New section: Horses (Kanka) | (none) | Added | ch1, ch6, ch7 |
| New section: Horses (Kayal) | (none) | Added | ch7, ch13, ch14, ch15, ch16, ch20, ch22, ch23, ch24, ch26 |
| New section: Horses (grey gelding) | (none) | Added | ch7, ch8 |
| New section: Horses (Megha) | (none) | Added | ch16 |
| Standing rules | No banner/flag or lamp rules | Added a flags-and-banners rule (Travancore standard, Maratha memory pennant, raider banners, no redcoat misreads) and an oil-lamp rule (clay or brass, no glass) | ch12, ch13, ch26 |

34 entries changed or added in total (7 rows in Nagoji's table, 10 edited "Other principals"
bullets, 11 new character bullets, 4 new horse entries, 2 new standing rules).

## 2. Conflicts for the author

These are left as the current bible's wording in the draft; do not treat the additions above as
having resolved them.

1. **Varma's headwear in court/formal scenes.** The current line "Court: cream and gold, peacock
   crest..." is read two different ways by different scripts:
   - **Bare-headed, no turban:** the peacock crest is a single feather pinned into a bare side-knot
     (konda) above his left ear, with no turban and no crown. Used in ch6 (coastal hall), ch7
     (beach and field), ch11 (informal war hall) and ch18 (coastal hall). These scripts explicitly
     note that this overrides the varma-v1 concept sheet, which shows him in a turban.
   - **Turban worn:** a cream-and-gold turban carrying a jewelled peacock crest, matching the
     varma-v1 concept sheet as drawn. Used in ch14 (campaign dress, on the march and in camp) and
     ch19 (a formal seated court audience with Nagoji). ch11 (5.2, the formal court look, as
     opposed to its own 3.1 informal war hall) and ch13/ch15/ch23/ch26 also say only "peacock crest"
     without stating turban or bare head either way.
   Neither side is clearly superseded: ch19 is a formal court scene like ch6, so this cannot be
   resolved by a court/informal distinction alone. Needs an author decision.

2. **Nagoji entering the sea still ironed.** Ch3 ends with him going into the sea in the collar,
   wrist chain and ankle irons described in that chapter's 1.1. Ch4 shows him with none of these
   and gives no account of how or when they came off. Neither script resolves this; it is carried
   into the draft as a stated gap (see the row 1-3 change above) rather than invented.

3. **Nagoji's pre-capture look.** No look was ever locked for Nagoji before his capture. Only ch6
   proposes one, for its 8.2 memory panel (Maratha cavalry dress off the commander sheet, hands
   unbandaged), and ch6's own note asks the author to confirm it. Ch10's opening panel (1.1) was
   left figure-less specifically because of this gap. The draft adopts ch6's proposal in the
   constant-identity paragraph because nothing contradicts it, but it rests on a single script's
   inference and should get an explicit author sign-off before ch10 or any other memory panel of
   this kind is generated.

4. **Checked, not a conflict: Revathi's sari colour.** Every chapter that dresses her (ch9, ch13,
   ch16 to ch21, ch24 to ch28) uses "deep indigo sari with gold" or "deep blue," and only ch11 uses
   "deep green," exactly matching the current bible's "deep blue or indigo... deep green in ch11."
   No script proposes a different colour anywhere else. Flagging this explicitly since it was
   raised as a candidate conflict; it is not one.

## 3. Needs a pipeline alias

`pipeline/script_pipeline.py`'s `CHARACTER_ALIASES` (read, not edited) has no key for any of these
new entries, so `infer_cast` will never add them to a panel's cast from their bible entry, and
`_character_look` will only be reached if a chapter script passes them in explicitly via
`--cast-overrides` or the panel text alone. Suggested tuples, in the same form as the existing
dict:

| New entry | Suggested key | Suggested aliases |
| --- | --- | --- |
| Chanda Sahib | `chanda_sahib` | `("chanda sahib",)` |
| Gustaaf Willem van Imhoff | `van_imhoff` | `("van imhoff", "governor van imhoff")` |
| Dutch envoys | `dutch_envoys` | `("envoy", "envoys")` |
| Yusuf Marakkar | `yusuf` | `("yusuf",)` |
| Nagoji's father | `nagoji_father` | `("nagoji's father",)` |
| Nagoji's mother | `nagoji_mother` | `("nagoji's mother",)` |
| Bhalerao | `bhalerao` | `("bhalerao",)` |
| The Gujarati sowcar | `sowcar` | `("sowcar",)` |
| Joseph Donnadi | `donnadi` | `("donnadi",)` |
| The Madurai troop | `madurai_troop` | `("madurai troop", "madurai lancers", "madurai riders")` |
| The Kollamkara Raja | `kollamkara` | `("kollamkara",)` |
| Kanka | `kanka` | `("kanka",)` |
| Kayal | `kayal` | `("kayal",)` |
| Nagoji's grey gelding | `grey_gelding` | `("grey gelding",)` |
| Megha | `megha` | `("megha",)` |

All 20 pre-existing keys in `CHARACTER_ALIASES` still resolve correctly against the draft (see the
VERIFY output below); none needed a new alias.

## VERIFY output

```
1 Constant identity: strong cheekbones, straight nose, thick curled moustache, CLEAN-SHAVEN CHIN (light stubble at most, captivity only), long curly black hair, s
2 Constant identity: strong cheekbones, straight nose, thick curled moustache, CLEAN-SHAVEN CHIN (light stubble at most, captivity only), long curly black hair, s
4 Constant identity: strong cheekbones, straight nose, thick curled moustache, CLEAN-SHAVEN CHIN (light stubble at most, captivity only), long curly black hair, s
5 Constant identity: strong cheekbones, straight nose, thick curled moustache, CLEAN-SHAVEN CHIN (light stubble at most, captivity only), long curly black hair, s
7 Constant identity: strong cheekbones, straight nose, thick curled moustache, CLEAN-SHAVEN CHIN (light stubble at most, captivity only), long curly black hair, s
17 Constant identity: strong cheekbones, straight nose, thick curled moustache, CLEAN-SHAVEN CHIN (light stubble at most, captivity only), long curly black hair, s
24 Constant identity: strong cheekbones, straight nose, thick curled moustache, CLEAN-SHAVEN CHIN (light stubble at most, captivity only), long curly black hair, s
28 Constant identity: strong cheekbones, straight nose, thick curled moustache, CLEAN-SHAVEN CHIN (light stubble at most, captivity only), long curly black hair, s
nagoji -> Constant identity: strong cheekbones, straight nose, thick curled moustache, CLEAN-SHAVEN CHIN (light stubble at most, c
varma -> - **Marthanda Varma**: V13 varma-v1 face. Court: cream and gold, peacock crest, gold necklaces, often a spear, frequentl
duarte -> - **Father Duarte**: thin Portuguese Jesuit, scholar's stoop, grey tired eyes, ink-stained fingers, callused right hand,
joao -> - **Joao**: broad, heavy, ruddy Portuguese gaoler; brown leather jerkin over a cream shirt; wide belt; iron key ring. NO
ramayyan -> - **Ramayyan Dalawa**: thin, sharp fine features, receding hair, plain white cloth, palm-leaf bundles and stylus. Ch14 b
padmini -> - **Padmini Amma**: in her fifties at first; thick black hair coiled at the nape, going grey later; simple gold; cotton
revathi -> - **Revathi Bayi**: a little younger than Nagoji; deep blue or indigo sari with gold, deep green in ch11; jasmine in a b
ibrahim -> - **Ibrahim Marakkar** ("kapitan"): shorter than the fishermen but broader, scar from the LEFT ear to the jaw, a coastal
eustachius -> - **Eustachius De Lannoy**: tall, pale hair. A distant figure in a Dutch blue coat and black tricorne in ch11; torn and
raza -> - **Raza Khan**: lean, hawk nose, pointed moustache, scar on his ANATOMICAL LEFT cheek, green high-wrapped turban. Madur
ponnan -> - **Ponnan (Ponnam Pandya Deven)**: broad-shouldered Maravar, curly hair, thick moustache, clean chin, red shoulder clot
dhanaji -> - **Dhanaji**: a Deccan rider of Nagoji's generation, stockier and heavier than Nagoji, short black beard, white Maratha
keshavrao -> - **Keshavrao**: young, narrow shoulders, black hair hacked short, prisoner rags; the ch2 lock: about nineteen, a faint
senior_rani -> - **The Senior Rani of Attingal**: Varma's sister; dressed in white; cool and measured.
prince -> - **The Prince / heir**: about ten in ch17 and ch22-23, about fourteen in ch24; in ch17 and ch22, a small clean white mu
savitri -> - **Savitri of Kottarakkara**: older, with lines of care; white mourning clothes in ch27.
thoma -> - **Thoma Ittyerah** (ch24): a Syrian Christian artillery commander, broad, in a white tunic, with betel-stained teeth.
avraham -> - **Avraham ben Ephraim** (ch24): a Kochi Jewish trader in a dark coat and cap, with a chest-length beard.
nandini -> - **Nandini** (ch27): a small girl, Padmini's sister's daughter and heir.
mathoo -> - **Mathoo Tharakan**: an older Syrian Christian merchant with grey receding hair, a fine grey moustache, a gold cross a
karl -> - **Karl August**: a pale German deserter with a sickly yellow cast, cropped greying hair, rough cotton shirt. Ch11.
```

Every chapter number resolves to the correct table row (confirmed by inspecting the tail of each
`_nagoji_look` result, not just the shared constant-identity prefix shown above): row 1-3 for
chapters 1 and 2, row 4 for chapter 4, row 5-6 for chapter 5, row 7-16 for chapter 7, row 17-27 for
chapters 17 and 24, and the 28 epilogue row for chapter 28. Every one of the 20 pre-existing
`CHARACTER_ALIASES` keys resolves to its own dedicated bible entry, not a neighbour's (in
particular `ibrahim` correctly finds its own block and not Keshavrao's, and `dhanaji` returns the
author-locked line in full).

## 4. Resolutions (applied to CONTINUITY.md on 2026-09-27)

- **Varma's headwear (conflict 1):** author decision, dress by occasion. The approved V13 turban with the jewelled peacock-feather crest at formal court audiences and on campaign; bare-headed with a side knot on the beach and field, in the war hall, at temples and in private. The ch6 and ch18 audience panels change to the turban.
- **Irons between ch3 and ch4 (conflict 2):** author decision, leave the gap as the novel does. The sentence noting the gap was removed from Nagoji's ch1-3 row, because rows are pasted into image prompts.
- **Pre-capture look (conflict 3):** kept as a note below Nagoji's table, where it is not injected into prompts. In the draft it sat in the constant-identity block, which would have put a rust-red turban into every Nagoji prompt, including the captivity chapters.
- **Chapter rows:** the pipeline now gives each prompt a character's base line plus only that chapter's rows (`_look_for_chapter` in pipeline/script_pipeline.py, tests in ChapterRowTests). Varma, Ramayyan, Revathi, Duarte, Ibrahim, De Lannoy, Mathoo, the heir, Savitri, Chanda Sahib and the Dutch envoys use rows. Nagoji's table is split so every row is self-contained: 1, 2, 3, 4, 5, 6, 7-8, 9-15, 16, 17, 18-19, 20, 21, 22, 23, 24, 25-27 and 28 epilogue. The single 17-27 row had put the ch24 uniform, the ch22 injuries and the ch17 turban scene into every chapter from 17 to 27.
- **Duarte:** base line gains the face approved in Chapter 1 (gaunt, lined, grey hair swept back with loose curls at the sides, plain standing collar, small cross on a thin chain).
- **Lamps:** the rule applies to Kerala and Travancore settings only; European lanterns stay in Portuguese and Dutch settings.
- **Aliases:** 15 new CHARACTER_ALIASES keys. The draft's bare "envoy" alias was narrowed to "Dutch envoy(s)", because "envoy" also appears in ch25 and ch28 dialogue about other envoys.
