# CONTINUITY proposal: span rows for chapters 15, 17, 20, 22, 24 and 28

Status: APPROVED by the author on 2026-10-07 and applied to CONTINUITY.md exactly as below (backup: pipeline/review/CONTINUITY-pre-span-rows-ch15-28-2026-10-07.md). Tested beforehand on a scratch copy: all six chapters prepare cleanly (ch15 69 panels, ch17 64, ch20 84, ch22 67, ch24 145, ch28 64).

## Why

Six chapters cannot generate art yet. Each has a CONTINUITY row that describes a costume change in words ("until", "afterwards", "after he changes", "pages 1 to 13", "from page 6", "epilogue"). The prompt builder gives every panel exactly one row, so it refuses rows whose meaning depends on where in the chapter the panel falls. The fix is to cut each such row into span rows (the "@page.panel" form chapters 9 to 12 already use), keeping your wording. Panels affected: ch15 30, ch17 40, ch20 59, ch22 57, ch24 all Nagoji panels, ch28 25.

The other ten new chapters (13, 14, 16, 18, 19, 21, 23, 25, 26, 27) are not blocked and are generating now.

## Proposed rows

Wording is yours unless marked NEW. NEW wording is taken from the chapter script's panel descriptions; please accept, change or strike it.

### Chapter 15, De Lannoy (row 112)

- Replace "| 15 | First in the torn, soot-stained blue coat ... the bandage still on. |" with:
- | 15 @1-13.2 | The torn, soot-stained blue coat with a linen bandage on his left hand and wrist. |
- | 15 @13.3 | NEW: Barefoot, in a sweat-stained shirt open at the throat, the coat folded on the bench, the linen bandage on his left hand and wrist. |
- | 15 @13.4- | A white ankle-length mundu, a plain white cotton tunic-coat and sandals, the linen bandage still on his left hand and wrist. |
- Note: the drafting agent proposed the change at 13.4, but the script has him already out of the coat in 13.3.

### Chapter 17, Nagoji (row 60)

- | 17 @1-8.3 | Commander look (rust-red turban, cream tunic, broad red sash, cream trousers), no talwar, barefoot at home. The brand and the long white forearm scar on the inner LEFT forearm above the wrist. |
- | 17 @8.4-9.4 | Bare-headed, long curly hair loose, still in tunic and sash, the turban folded in his hand or set down. The brand and the long white forearm scar on the inner LEFT forearm above the wrist. |
- | 17 @9.5-9 | Bare-headed, long curly hair loose, still in tunic and sash, the turban set down; the ivory-handled knife with the conch mark. The brand and the long white forearm scar on the inner LEFT forearm above the wrist. |
- | 17 @10.1-10 | Bare-headed, his long curly hair gathered into a knot on his crown for the first time, still in tunic and sash; the conch knife at his sash. The brand and the long white forearm scar on the inner LEFT forearm above the wrist. |
- | 17 @11- | Ananthan Pillai, Kerala topknot, hair still black with only the first grey at the temples, NO turban, plain cream mundu with no gold border, cream shoulder cloth, bare arms, the conch knife at the mundu's waist fold, no silver chain yet. The brand and the long white forearm scar on the inner LEFT forearm above the wrist. |
- Question: the current row says hair loose "to the end of page 10" and also that he knots it on 10.1. The script shows the new knot at 10.4. I have assumed the knot holds from 10.1 to the end of page 10.

### Chapter 20, Nagoji (row 62)

- | 20 @1-10.2 | Ananthan Pillai: Kerala topknot high on the crown, NO turban, cream or white mundu with shoulder cloth, first grey at the temples, the brand and the long white forearm scar on the inner LEFT forearm above the wrist; silver chain of office; the ivory-handled knife with the conch mark at his waist. |
- | 20 @10.3- | The same, with no knife at his waist (he gives it to Dhanaji in 10.3 to 10.5). |

### Chapter 22, Nagoji (row 64) and Varma (row 87)

- Nagoji:
- | 22 @1-7.2 | Ananthan Pillai: Kerala topknot high on the crown, NO turban, cream or white mundu with shoulder cloth, first grey at the temples, the brand and the long white forearm scar on the inner LEFT forearm above the wrist; silver chain of office; no knife; uninjured. |
- | 22 @7.3-9 | NEW: the same, his right arm hanging useless from the fall on the stone, his left palm cut and not yet wrapped (no blood shown). |
- | 22 @10.1- | The same, his right shoulder bound and his left palm wrapped. |
- Note: the drafting agent proposed 5.4 and 7.3 as the cuts. The script has his shoulder hit at 7.3 and the binding at 10.1, so I moved the last change to 10.1.
- Varma:
- | 22 @1-10 | Hill shrine: plain temple dress, one gold chain, no spear, cream mundu with a thin gold border. |
- | 22 @11- | Plain temple dress, one gold chain, no spear, cream mundu with a thin gold border, with a cream cloth over his injured right shoulder and a stitched brow. |
- This also removes the word "Fort" from the shrine panels, which the foreign-term guard otherwise trips on.

### Chapter 24, Nagoji (row 66)

- | 24 @1-14.1 | Ananthan Pillai: Kerala topknot high on the crown, NO turban, cream or white mundu with shoulder cloth, first grey at the temples, the brand and the long white forearm scar on the inner LEFT forearm above the wrist; silver chain of office; no knife; no coat. |
- | 24 @14.2- | In uniform: white European-cut coat, red waistcoat, plain brass buttons, knee breeches, buckled European riding boots, the silver chain of office worn over the coat, Kerala topknot, no hat, no turban, first grey at the temples; the brand and the long white forearm scar on the inner LEFT forearm above the wrist. |
- Note: the drafting agent proposed the change at page 14. The script puts him in uniform for the first time at 14.2; 14.1 is De Lannoy's nod on the parapet.

### Chapter 28, Nagoji (row 68, "28 epilogue")

- | 28 @1-5 | Kerala topknot, first grey at the temples, bare-chested in a cream mundu and shoulder cloth as Kerala temple custom requires. |
- | 28 @6-11 | In uniform: white European-cut coat, red waistcoat, plain brass buttons, knee breeches, buckled European riding boots, the silver chain of office worn over the coat, Kerala topknot, no hat, no turban. |
- | 28 @12-12 | Later-life sheet: grey-streaked hair in a topknot, white mundu with a gold border. |
- | 28 @13.1 | NEW: captivity sheet (young Nagoji in the Goa interrogation room memory, as the script's 13.1 describes). |
- | 28 @13.2 | NEW: Ananthan Pillai in the married years (Kerala topknot, NO turban, as the script's 13.2 describes). |
- | 28 @13.3- | Later-life sheet: grey-streaked hair in a topknot, white mundu with a gold border. |

## Not blocking, for later

- Chapters 13 to 16: Nagoji's rows say "The Portuguese brand"; rows 9 to 12 say "The old brand". The new sidecars work around it with an allowed-word list. Rewording those rows to "The old brand" would let the workaround go.
- Chapter 13: the script gives the Madurai troop "bright high-wrapped turbans"; the bible says white or off-white. The sidecar follows the bible.
- Chapter 13: Padmini's sari is "cotton" in script 2.2 but "cream silk" in the bible. The sidecar avoids naming the fabric.

## What happens after approval

I apply the rows exactly as approved, with a backup of CONTINUITY.md, prepare the six packages and start their generation the same way as the other ten.
