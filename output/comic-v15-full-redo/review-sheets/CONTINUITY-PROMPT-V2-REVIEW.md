# CONTINUITY.md changes for prompt v2

For your approval before any chapter 9 images. Nothing is applied yet: CONTINUITY.md is unchanged, and the
proposed text sits in `CONTINUITY-PROMPT-V2-PROPOSED.md` with the diff in `review-sheets/CONTINUITY-PROMPT-V2.diff`.

## The three edits

1. **Nagoji, chapter 9 split by page.** The single 9-15 row becomes five chapter 9 rows plus a 10-15 row with the
   old text. Sleeves stay down and hide the brand and scar, except on 5.2 and page 11, where the script shows them.
   Boots until 2.3; barefoot from 2.4, when he leaves them on the verandah step.
2. **Padmini's base line.** Drops "at first", "going grey later" and "Dies ch27", and "cotton sari" becomes "muted
   earth-toned silk sari" to match the chapter 9 script. v2 refuses timeline words inside a look, because the model
   reads "going grey later" as grey hair now. When she greys needs a row of its own (question 2).
3. **New section: scoped art rules.** Eight rules, each tagged with the settings it belongs to. A panel's prompt
   gets only the rules for its own setting, so the Portuguese rope rule no longer reaches a Kerala verandah.

## One side effect

Chapters 1 to 8 still use the v1 prompts, built from the live bible. Edit 2 would change 29 chapter 8 prompts if
chapter 8 were ever prepared again. The chapter 8 package keeps its own frozen copy of the bible, so the current art
and builds are not affected.

## The diff

```diff
--- CONTINUITY.md
+++ CONTINUITY-PROMPT-V2-PROPOSED.md
@@ -31,7 +31,12 @@
 | 5 | Pages 1 and 2, before he is given new clothes: bare-chested in the cream captivity dhoti, no shirt, hair loose, hands wrapped in clean linen, rope burns across the chest, faint chafe rings at the ankles, no irons. From page 3: a collarless cream tunic-shirt over a village cotton dhoti, bare-headed, hair tied back, hands still bandaged. |
 | 6 | Village cotton dhoti and simple cream shirt, bare-headed, hair loose or tied back, hands still bandaged. |
 | 7-8 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. The Portuguese brand on the inner LEFT forearm, a hand's width above the wrist, seen when sleeves are pushed up: a pale puckered patch of raised ridges blurred past reading, not a cross. |
-| 9-15 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. The Portuguese brand on the inner LEFT forearm, a hand's width above the wrist, seen when sleeves are pushed up: a pale puckered patch of raised ridges blurred past reading, not a cross. A long, thin white scar along the same forearm, running from the wrist toward the elbow, beside the brand. |
+| 9 @1-2.3 | Commander sheet: rust-red turban, cream tunic with sleeves down to the wrists, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 9 @2.4-5.1 | Commander sheet: rust-red turban, cream tunic with sleeves down to the wrists, broad red sash, cream trousers, barefoot, talwar. Nails healed but ridged. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 9 @5.2 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, barefoot, talwar. Nails healed but ridged. The left sleeve is pushed back: the brand on the inner LEFT forearm is a pale puckered patch of raised ridges a hand's width above the wrist, with no letters or numerals, and a long, thin WHITE scar runs from the wrist toward the elbow alongside it. |
+| 9 @5.3-10.5 | Commander sheet: rust-red turban, cream tunic with sleeves down to the wrists, broad red sash, cream trousers, barefoot, talwar. Nails healed but ridged. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 9 @11- | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, barefoot, talwar. Nails healed but ridged. The left sleeve is pushed back: the brand on the inner LEFT forearm is a pale puckered patch of raised ridges a hand's width above the wrist, with no letters or numerals, and a long, thin WHITE scar runs from the wrist toward the elbow alongside it. |
+| 10-15 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. The Portuguese brand on the inner LEFT forearm, a hand's width above the wrist, seen when sleeves are pushed up: a pale puckered patch of raised ridges blurred past reading, not a cross. A long, thin white scar along the same forearm, running from the wrist toward the elbow, beside the brand. |
 | 16 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. The Portuguese brand on the inner LEFT forearm, a hand's width above the wrist, seen when sleeves are pushed up: a pale puckered patch of raised ridges blurred past reading, not a cross. A long, thin white scar along the same forearm, running from the wrist toward the elbow, beside the brand. First grey at the temples. On parade days, a blue Travancore drill coat over his clothes. |
 | 17 | Pages 1 to 8.3: commander look (rust-red turban, cream tunic, broad red sash, cream trousers), no talwar, barefoot at home. From panel 8.4 to the end of page 10: bare-headed, long curly hair loose, still in tunic and sash, the turban folded in his hand or set down; the ivory-handled knife with the conch mark at his sash from 9.5; on 10.1 he gathers his hair into a knot for the first time. Pages 11 to 13: Ananthan Pillai, Kerala topknot, hair still black with only the first grey at the temples, NO turban, plain cream mundu with no gold border, cream shoulder cloth, bare arms, the conch knife at the mundu's waist fold, no silver chain yet. Throughout, the brand and the long white forearm scar on the inner LEFT forearm above the wrist. |
 | 18-19 | Ananthan Pillai: Kerala topknot high on the crown, NO turban, cream or white mundu with shoulder cloth, first grey at the temples, the brand and the long white forearm scar on the inner LEFT forearm above the wrist; silver chain of office; the ivory-handled knife with the conch mark at his waist. |
@@ -60,7 +65,7 @@
   | 28 | Dedication: same face aged, low knot, plain mundu, bare torso, no jewels, no headwear, the sacred thread across his chest. |
 - **Ramayyan Dalawa**: thin, sharp fine features, receding hair, plain white cloth, palm-leaf bundles and stylus.
   | 14 | Battle: mud-splattered white dhoti, curved Nair sword. |
-- **Padmini Amma**: in her fifties at first; thick black hair coiled at the nape, going grey later; simple gold; cotton sari hitched for walking, the old Kerala drape with no stitched blouse; long walking stick. Dies ch27.
+- **Padmini Amma**: in her fifties; thick black hair coiled at the nape; simple gold; muted earth-toned silk sari hitched for walking, the old Kerala drape with no stitched blouse; long walking stick.
 - **Revathi Bayi**: a little younger than Nagoji; deep blue or indigo sari with gold; jasmine in a braid; flat-coin necklace; gold armlets; sandalwood line at the hairline.
   | 11 | Deep green sari in place of the indigo. |
   | 20-28 | Wears a tali; grey threading in her hair. |
@@ -121,6 +126,17 @@
 - **Nagoji's grey gelding**: his plain grey daytime mount in ch7-8, distinct from Kayal.
 - **Megha**: a grey horse with a black mane, named for the monsoon clouds; ridden in ch16 only, where his death frames the chapter.
 
+## Scoped art rules (prompt profile v2)
+
+- [all] 1740s dress, arms, objects.
+- [all] No blood or gore; stage aftermath.
+- [kerala, court, coast, travancore_camp] Clay or brass oil lamps; open wicks.
+- [deccan] The Maratha flag is a saffron swallow-tailed pennant; Maratha riders in the background wear white or cream angarkhas and pagdis, never a rust-red turban with a red sash.
+- [carnatic, travancore_camp, dutch] Raiders' and rivals' banners are plain cloth.
+- [dutch] Dutch East India Company soldiers wear blue coats. No soldier, Indian or European, wears a British red coat.
+- [portuguese] Portuguese guards never wear British red coats or Dutch blue coats.
+- [portuguese] Interrogation ropes hang from an iron ring for binding wrists, never tied as nooses.
+
 ## Standing rules for generated art
 
 - No text of any kind in the art, and no painted balloons, caption boxes or frames: leave clear, low-detail space where the lettering will go. The letterer draws every balloon and caption over the finished art.
```

## Questions

1. Approve the diff, and how to handle the chapter 8 side effect.
2. Padmini's grey hair: from which chapter?
3. The Velinadu banners (2.2 and 6.5): plain cloth, or a colour or emblem?
4. Chapter 9 panels 10.3 and 10.4: the draft says morning light, and 10.5 is "That night". Keep morning, or late
   afternoon?

## Also done today

- The two reviewer fixes are in, with tests:
  - The prompt audit no longer counts a NOT SHOWN line ("Dutch envoys is outside the frame") as a foreign term.
  - Page-span rows for one character may not overlap. Chapter rows still stack: Revathi's ch20-28 tali row plus
    her ch27 funeral row both apply.
- The reviewer's broader suggestion, refusing any second row, would have blocked that legitimate Revathi
  chapter 27 case, so the check covers only span rows.
