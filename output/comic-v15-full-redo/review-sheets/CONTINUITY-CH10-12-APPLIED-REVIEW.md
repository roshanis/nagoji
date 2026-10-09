# CONTINUITY.md changes for chapters 10 to 12 (applied)

You asked me to go ahead with my recommendations while you were out, so I applied these bible changes before
generating chapters 10 to 12. Please look them over when you can. To undo them, I restore
`pipeline/review/CONTINUITY-pre-ch10-12-2026-10-02.md` and regenerate the affected panels.

## How they were checked

- Codex drafted the chapter 10 to 12 art direction and these bible rows.
- An independent review, one reviewer per chapter, found 29 fixes, and they were all applied.
- Chapter 1 to 9 rows are byte-identical, and the frozen v1 prompts of chapters 5 to 8 are unchanged. One drafted
  edit, Kayal's chapter list, would have changed 13 chapter 7 prompts, so I put it back.
- All 187 chapter 10 to 12 prompts pass the audit: the SETTING paragraph comes last, no dialogue leaks into the art
  prompt, and there are no foreign terms.

## What changed

- **Nagoji:** page-span rows for chapters 10 to 12.
  - Boots off and barefoot at the Ayyappa temple, on the barracks mat, in the chapter 11 war hall and audience hall
    (Kerala court custom), and on the chapter 12 shrine steps.
  - Sleeves down, with the brand and scar hidden, except where the script shows them (10 @9.4, 11 @21.3), and then
    always on the inner LEFT forearm.
- **Varma:** campaign court look in 10 @8.4 to 8.5. In chapter 11, the white cloth band in the war hall and the
  crested turban at the formal audience. In chapter 12, the court look and then the war-hall look.
- **Padmini:** a cotton sari in chapters 10 and 11.
- **Revathi:** in chapter 11, a deep green sari with quieter jewellery.
- **Chanda Sahib:** listed as "Chanda Sahib of Arcot".
- **Scoped rule:** "Non-Maratha raiders' banners are plain cloth", so the Maratha pennants in the scripts stay.

## Decisions I made for you

1. **Chapter 11 footwear:** barefoot on pages 3 to 4, 7 to 17 and 20, booted elsewhere. Pages 8 to 16 are the
   royal audience hall with mats, where he stood barefoot in chapter 6.
2. **Chapter 10, 8.4:** the defeated chief's sword is now "thrust through the waist sash, one hand on its hilt".
   The script said "belted, one hand on the buckle", which invites a European belt.
3. **Chapter 11, 21.3:** the brand is on "the inner left forearm, a hand's width above the wrist". The script said
   "left wrist", which disagreed with the bible.
4. **Kayal:** Nagoji's bay mare is named, with her sheet, in every chapter 10 to 12 panel where he rides.

## The diff

```diff
--- CONTINUITY.md.before
+++ CONTINUITY.md
@@ -36,7 +36,26 @@
 | 9 @5.2 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, barefoot, talwar. Nails healed but ridged. The left sleeve is pushed back: the brand on the inner LEFT forearm is a pale puckered patch of raised ridges a hand's width above the wrist, with no letters or numerals, and a long, thin WHITE scar runs from the wrist toward the elbow alongside it. |
 | 9 @5.3-10.5 | Commander sheet: rust-red turban, cream tunic with sleeves down to the wrists, broad red sash, cream trousers, barefoot, talwar. Nails healed but ridged. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
 | 9 @11- | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, barefoot, talwar. Nails healed but ridged. The left sleeve is pushed back: the brand on the inner LEFT forearm is a pale puckered patch of raised ridges a hand's width above the wrist, with no letters or numerals, and a long, thin WHITE scar runs from the wrist toward the elbow alongside it. |
-| 10-15 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. The Portuguese brand on the inner LEFT forearm, a hand's width above the wrist, seen when sleeves are pushed up: a pale puckered patch of raised ridges blurred past reading, not a cross. A long, thin white scar along the same forearm, running from the wrist toward the elbow, beside the brand. |
+| 10 @1-1.3 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 10 @1.4-2.5 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, barefoot, no carried talwar; boots and talwar remain at the outer temple steps. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 10 @3-8.5 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 10 @9.1 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, barefoot, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 10 @9.2-9.3 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 10 @9.4 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. His LEFT forearm rests on his knee palm up, the LEFT sleeve pushed back, so the inner forearm faces the viewer: the old brand is a pale puckered patch of raised ridges a hand's width above the wrist, with no letters or numerals and not a cross; a long thin WHITE scar runs from wrist toward elbow beside it. Nothing on the wrist. |
+| 10 @9.5- | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 11 @1-2 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 11 @3-4 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, barefoot on the floor and mats with his boots left at the door, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 11 @5-6 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 11 @7-17 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, barefoot on the floor and mats with his boots left at the door, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 11 @18-19 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 11 @20 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, barefoot on the floor and mats with his boots left at the door, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 11 @21.1-21.2 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 11 @21.3 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. The LEFT sleeve is eased back and the forearm turned slightly outward as the palm presses the rock, so only the edge of the old pale puckered brand shows on the INNER forearm, a hand's width above the wrist; no letters or numerals, never on the back of the hand or the outer forearm. The long white scar beside it stays mostly covered. |
+| 11 @21.4- | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 12 @1 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 12 @2-3 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, barefoot, talwar across his knees; boots together below the shrine steps. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 12 @4- | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. Sleeves down to the wrists. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |
+| 13-15 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. The Portuguese brand on the inner LEFT forearm, a hand's width above the wrist, seen when sleeves are pushed up: a pale puckered patch of raised ridges blurred past reading, not a cross. A long, thin white scar along the same forearm, running from the wrist toward the elbow, beside the brand. |
 | 16 | Commander sheet: rust-red turban, cream tunic, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. The Portuguese brand on the inner LEFT forearm, a hand's width above the wrist, seen when sleeves are pushed up: a pale puckered patch of raised ridges blurred past reading, not a cross. A long, thin white scar along the same forearm, running from the wrist toward the elbow, beside the brand. First grey at the temples. On parade days, a blue Travancore drill coat over his clothes. |
 | 17 | Pages 1 to 8.3: commander look (rust-red turban, cream tunic, broad red sash, cream trousers), no talwar, barefoot at home. From panel 8.4 to the end of page 10: bare-headed, long curly hair loose, still in tunic and sash, the turban folded in his hand or set down; the ivory-handled knife with the conch mark at his sash from 9.5; on 10.1 he gathers his hair into a knot for the first time. Pages 11 to 13: Ananthan Pillai, Kerala topknot, hair still black with only the first grey at the temples, NO turban, plain cream mundu with no gold border, cream shoulder cloth, bare arms, the conch knife at the mundu's waist fold, no silver chain yet. Throughout, the brand and the long white forearm scar on the inner LEFT forearm above the wrist. |
 | 18-19 | Ananthan Pillai: Kerala topknot high on the crown, NO turban, cream or white mundu with shoulder cloth, first grey at the temples, the brand and the long white forearm scar on the inner LEFT forearm above the wrist; silver chain of office; the ivory-handled knife with the conch mark at his waist. |
@@ -56,7 +75,13 @@
 
 - **Marthanda Varma**: V13 varma-v1 face. Dress by occasion. Formal court audiences and campaign: the V13 court look, a cream-and-gold turban with a jewelled peacock-feather crest, cream and gold cloth, gold necklaces, often a spear, frequently bare-chested. Beach, field, war hall, temple and private scenes: bare-headed with his hair in a side knot above his left ear, no turban, no crest, bare-chested, a cream mundu with a gold border and gold necklaces. Never a crown.
   | 7 | Beach and field: Vaishnavite forehead lines, one cream-and-gold cloth over the shoulder. |
-  | 11 | Formal court adds a plain shoulder cloth and a string of rudraksha beads among the gold. Informal war hall: hair pulled back under a narrow white cloth band, spear laid aside. |
+  | 10 @8.4-8.5 | This scene uses the campaign court look: cream-and-gold turban with jewelled peacock-feather crest, bare chest, cream-and-gold cloth and gold necklaces. Keep this same headwear on the return ride; no bare-headed side knot. |
+  | 11 @1-4 | Instead of the side knot: This scene is the informal war hall: hair pulled back under a narrow white cloth band, no turban or crest, bare chest, cream mundu with gold border and gold necklaces; seated cross-legged or leaning over the floor map, spear laid aside. |
+  | 11 @5-6 | This scene is the formal Tengapattanam audience: cream-and-gold turban with jewelled peacock-feather crest, bare chest, cream-and-gold cloth and gold necklaces. No white headband. |
+  | 11 @7 | Instead of the side knot: This scene is the informal war hall: hair pulled back under a narrow white cloth band, no turban or crest, bare chest, cream mundu with gold border and gold necklaces; leaning over the floor map, spear laid aside. |
+  | 11 @8- | This scene is the formal coastal audience: cream-and-gold turban with jewelled peacock-feather crest, bare chest, cream-and-gold cloth, plain shoulder cloth and a string of rudraksha beads among the gold necklaces. No white headband. |
+  | 12 @1-4 | This scene uses the formal court look: cream-and-gold turban with jewelled peacock-feather crest, bare chest, cream-and-gold cloth and gold necklaces; spear grounded when standing in the hall. |
+  | 12 @5- | This scene is the informal coastal war hall: bare head, hair in a side knot above the LEFT ear, no turban, crest or white headband, bare chest, cream mundu with gold border and gold necklaces. Spear at his right hand by the low dais, carried when he rises. |
   | 16 | Temple visit at Tiruvattar and the ride back: plain white cloth, a narrow shoulder dressing, bare-headed. |
   | 21 | Festival memory, younger than the ch28 dedication: dark hair bound back, bare-chested in a plain mundu. |
   | 22 | Hill shrine: plain temple dress, one gold chain, no spear, cream mundu with a thin gold border. Fort room after the attack: the same, with a cream cloth over his injured right shoulder and a stitched brow. |
@@ -66,9 +91,10 @@
 - **Ramayyan Dalawa**: thin, sharp fine features, receding hair, plain white cloth, palm-leaf bundles and stylus.
   | 14 | Battle: mud-splattered white dhoti, curved Nair sword. |
 - **Padmini Amma**: in her fifties; thick black hair coiled at the nape; simple gold; muted earth-toned silk sari hitched for walking, the old Kerala drape with no stitched blouse; long walking stick.
+  | 10-11 | Cotton sari in place of silk, hitched for walking, old Kerala drape with no stitched blouse; thick black hair coiled at the nape, simple gold and long walking stick. |
   | 16-27 | Grey threading through her black hair. |
 - **Revathi Bayi**: a little younger than Nagoji; deep blue or indigo sari with gold; jasmine in a braid; flat-coin necklace; gold armlets; sandalwood line at the hairline.
-  | 11 | Deep green sari in place of the indigo. |
+  | 11 | Deep green sari in place of the indigo; quieter jewellery than at her first meeting with Nagoji: the flat-coin necklace, no gold armlets. |
   | 20-28 | Wears a tali; grey threading in her hair. |
   | 27 | At Padmini's funeral: plain white, no jasmine, no gold except the tali. |
 - **Father Duarte**: thin, gaunt Portuguese Jesuit in his fifties, lined face, grey hair swept back with loose curls at the sides, scholar's stoop, grey tired eyes, ink-stained fingers, callused right hand, plain black cassock with a plain standing collar and a small cross on a thin chain. NO white Roman collar tab (a 19th-century anachronism).
@@ -104,7 +130,7 @@
 - **Avraham ben Ephraim** (ch24): a Kochi Jewish trader in a dark coat and cap, with a chest-length beard.
 - **Nandini** (ch27): a small girl, Padmini's sister's daughter and heir.
 - **Temple priest face** (V13): ONLY for a confirmed Hindu ritual priest. Never for Duarte, Ramayyan or bystanders.
-- **Chanda Sahib**: a Carnatic rival, never shown face-on; heavy build, beard, white Mughal jama, high cream turban, no red. His riders: dust-coloured quilted coats, dark indigo or black turbans, never green, no red sashes, so they are never confused with Raza Khan's Madurai lancers.
+- **Chanda Sahib of Arcot**: a Carnatic rival, never shown face-on; heavy build, beard, white Mughal jama, high cream turban, no red. His riders: dust-coloured quilted coats, dark indigo or black turbans, never green, no red sashes, so they are never confused with Raza Khan's Madurai lancers.
   | 11-12 | Seen only backlit, silhouetted or shadowed. |
   | 25 | Led away in chains, at a distance. |
 - **Gustaaf Willem van Imhoff**: the Dutch Governor of Ceylon, ch11 only. Heavy-set, in his thirties, a dark coat with gold braid, a full powdered wig.
@@ -133,7 +159,7 @@
 - [all] No blood or gore; stage aftermath.
 - [kerala, court, coast, travancore_camp] Clay or brass oil lamps; open wicks.
 - [deccan] The Maratha flag is a saffron swallow-tailed pennant; Maratha riders in the background wear white or cream angarkhas and pagdis, never a rust-red turban with a red sash.
-- [carnatic, travancore_camp, dutch] Raiders' and rivals' banners are plain cloth.
+- [carnatic, travancore_camp, dutch] Non-Maratha raiders' and rivals' banners are plain cloth.
 - [dutch] Dutch East India Company soldiers wear blue coats. No soldier, Indian or European, wears a British red coat.
 - [portuguese] Portuguese guards never wear British red coats or Dutch blue coats.
 - [portuguese] Interrogation ropes hang from an iron ring for binding wrists, never tied as nooses.
```
