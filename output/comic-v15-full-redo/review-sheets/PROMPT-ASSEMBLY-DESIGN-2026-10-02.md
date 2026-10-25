# Design

# V15 prompt assembly v2: design for chapter 9 onward

Nothing was edited. The checks below ran only in memory, with PYTHONDONTWRITEBYTECODE=1.

## 0. Facts checked before designing

- **Chapters 5 to 8 can be rebuilt exactly.** Today's `assemble_prompt`, fed each package's `CONTINUITY-SNAPSHOT.md`, its `SCRIPT-SNAPSHOT.json` panels and the job's `cast`, reproduces 202 of 202 prepared prompts byte for byte (ch05 40, ch06 49, ch07 56, ch08 57).
- **Chapters 1 to 4 already differ.** 0 of 146 prompts match, because they were prepared with older wording. They are never rebuilt; `load_job` only re-checks their hashes. So the byte-identity guarantee can be tested for ch05-08 only. For ch01-04 the guarantee is that their load path does not change.
- **Test suite:** `test_script_pipeline` passes 30 of 30 under the README python (`/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python`). Plain `python3` lacks numpy.
- **Only `script_pipeline.py` reads prompt text.** The compositor and `run_chapter` take copy from the parsed script. Taking dialogue out of the prompt therefore changes no lettering.
- **The ch9 "Standing art notes" are lost.** `parse_script` drops that block (`scripts/CHAPTER-09-SCRIPT.md` lines 7-15), even though it says "Repeat the full tag ... in the generation prompt".
- **Cast gaps.** Across ch9-28, 86 panels name a principal in the description who is not in that panel's cast. In ch9 there are two: 2.2 Ramayyan (named as "NOT Ramayyan") and 10.2 Revathi (named but not shown).
- **Sheet hashes:** `nagoji-v2.png` is `bc270c0540427de10c753c9a8a6cc3eaa293c0aaba5e4d6e468c2b99134e2be0`. The Ibrahim sheet is `09-ibrahim-marakkar-v15.png`; its hash is in `APPROVED-SHEETS.json`.

## 1. Ranked changes

All new code goes in `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/script_pipeline.py` unless noted. The v1 `assemble_prompt` body is left exactly as it is. v2 is a new function, `assemble_prompt_v2(panel, chapter, continuity, cast, direction, sheet_keys)`, called only from `prepare`. Here `panel` must carry `page` and `panel`, and `sheet_keys` is the cast keys that have sheets, in attachment order.

### Section order of a v2 prompt

Parts are joined with blank lines, in this order:

1. **Header:** `V15 graphic novel panel {id} for chapter {ch}. Drawn in the book's inked graphic-novel style: clean ink line and painted colour, never photorealistic. Place: {setting.label}.`
2. **Description**, verbatim.
3. **Insert line**, optional (see change 10).
4. **FRAME SHAPE**, optional.
5. **SCRIPT DIRECTIONS**, optional, filtered (see change 10).
6. **PEOPLE line.**
7. **LOOKS block.**
8. **REFERENCE SHEETS line**, if any sheets are attached.
9. **ART RULES**, scoped.
10. **LETTERING block.**
11. **MUST MATCH block**, if any notes apply.
12. **SETTING paragraph**, which is always last.

### Change 1: per-panel setting from a sidecar file, anchor at the end (highest impact)

**New data file:** `scripts/CHAPTER-NN-ART-DIRECTION.json`.

| Key | Required | Contents |
|---|---|---|
| `prompt_profile` | yes | `"v2"` |
| `chapter` | yes | the chapter number |
| `settings` | yes | `{id: {label, scopes[], anchor, absent, time?, allow_terms?[]}}` |
| `pages` | no | `{"<page>": "<setting id>"}` defaults |
| `panels` | no | `{panel_id: {setting, time?, frame?: "strip" or "standard"}}` overrides |
| `character_notes` | no | `{cast_key: text}` |
| `not_shown` | no | `{panel_id: [cast_key]}` |

**New functions:**
- `load_art_direction(path, script, chapter) -> dict`. It validates the file and returns the parsed data plus `path`, `sha256` and `raw`.
- `_panel_direction(direction, panel)`. It returns `panels[id]`, otherwise `{"setting": pages[str(page)]}`.

**Validation rules (any failure raises ValueError):**
- Every panel resolves to exactly one setting.
- All ids and keys are known.
- Scopes are a subset of `SETTING_SCOPES = {"kerala","court","coast","travancore_camp","dutch","portuguese","deccan","carnatic","sea"}`.
- `anchor` and `absent` are non-empty.
- No em or en dashes anywhere.
- `chapter` matches.

**Prompt output:**
- The last paragraph is `SETTING (this panel): {anchor} Light: {time}. {absent}`. The panel's `time` wins over the setting's `time`; the `Light:` sentence is left out if neither is given.
- The short label also goes in the header.

**Evidence:**
- 94 panels drifted on setting.
- In ch05, all 13 panels that named no location drifted (13 of 13).
- The appended SETTING ANCHOR correction fixed most drift. The ch08 page-02-panel-04 r2 wording is the template.
- 8 of 10 ch07 lighting rejections had no time word.

**Expected effect:** every panel gets a location twice, at the start and at the end.

### Change 2: standing rules scoped by setting (replaces the paste-to-end-of-file block)

**New function:** `_scoped_rules(continuity, scopes) -> list[str]`. It reads a new CM section, `## Scoped art rules (prompt profile v2)`, which must sit between `## Horses` and `## Standing rules for generated art`. Placing it there means the v1 split-to-end-of-file sees no change.

**Format:**
- Each rule is a line `- [tag, tag] text`. These lines do not match the bold-bullet regex, so `_continuity_blocks` and alias lookup are unaffected.
- A rule is kept if its tags include `all` or overlap the setting's scopes.
- Raise ValueError if the section is missing. This fixes the `[-1]` quirk that would otherwise paste the whole bible.
- Raise ValueError if a tag is unknown.
- v2 never emits the old section, the print/upscaler bullet, or "Period: ... Portuguese Goa".

**Proposed CM text (author sign-off needed):**
- `[all] Dress, weapons and objects of the 1740s only; nothing modern.`
- `[all] No blood or gore; violence is shown through staging, distance and aftermath.`
- `[kerala, court, coast, travancore_camp] Lamps are clay or brass oil lamps with open flames.`
- `[court, travancore_camp] Travancore regular troops wear white mundu with crossed leather belts; the Travancore standard is a silver conch on red.`
- `[deccan] The Maratha flag is a saffron swallow-tailed pennant; Maratha riders in the background wear white or cream angarkhas and pagdis, never a rust-red turban with a red sash.`
- `[carnatic, travancore_camp, dutch] Raiders' and rivals' banners are plain cloth.`
- `[dutch] Dutch East India Company soldiers wear blue coats. No soldier, Indian or European, wears a British red coat.`
- `[portuguese] Portuguese guards never wear British red coats or Dutch blue coats.`
- `[portuguese] Interrogation ropes hang from an iron ring for binding wrists, never tied as nooses.`

**Evidence:**
- In 42 of the 66 European-drift panels, the standing block was the only European text in the prompt.
- 18 rejections for morion soldiers.
- 13 rejections for an iron ring, shackle or chain prop.
- The standing block was 43 to 53% of every prompt (1,555 characters).

### Change 3: sheet-use line and per-sheet caveats

The line appears only when sheets are attached:

`REFERENCE SHEETS: {n} attached image(s), in this order: 1) {Name}, 2) {Name}. They are character model sheets: use them only for faces, build, hair and costume. Ignore everything else on them: backgrounds, scenery, insets, labels, extra poses and props.`

**Nagoji clause**, chosen by how the selected row starts:

| Row starts with | Clause |
|---|---|
| "Commander sheet" | `For Nagoji use only the large full-length commander figure; his sleeves and footwear follow the text, not the sheet.` |
| "Captivity sheet" | `For Nagoji use only the captivity figure.` |
| "Later-life sheet" | `For Nagoji use only the later-life figure.` |
| anything else | `For Nagoji take only the face and build from the sheet; his costume comes from the text.` |

**New constant `SHEET_CAVEATS = {key: {"sha256", "text"}}`:**
- **nagoji** (hash bc270c05...): `The hilltop fort, stone cell and fort wall behind the figures on the Nagoji sheet are not part of this panel. His ear ornament is a tiny flush gold stud on the lobe, not the hanging drop drawn on the sheet.`
- **ibrahim:** `Ibrahim's scar is a thin pale line from his LEFT ear to the jaw, not red as drawn on his sheet.`

In `prepare` (v2), raise ValueError if an attached sheet's sha256 differs from its caveat's hash. That forces a review of the caveat whenever a sheet is re-approved.

**Evidence:**
- A hill fort appeared in 19 of 39 ch08 panels with the Nagoji sheet attached, and in 0 of 18 without it.
- 11 ear-drop failures.
- 5 red-scar failures.
- The "drawn from the commander figure" phrasing drifted in 4 of 5 prompts that used it.

### Change 4: summarise the copy instead of quoting it

**New function:** `_lettering_v2(copy, continuity) -> str`. Copy text never enters the prompt.

**Chunk kind:**
- The speaker label is `CAPTION`, or its parenthetical contains "letter": `a caption`.
- Otherwise the speaker label's base, before " (", lower-cased, equals an alias of a cast key: `a speech balloon for {Display}`.
- Otherwise: `a speech balloon for another speaker`.
- Append `, speaking from off panel` if the parenthetical matches `\boff\b|voice-over`.
- Other parenthetical text is dropped, for example "in Dutch" or "Flemish".

**Length class**, measured after removing `*`: short up to 40 characters, medium 41 to 100, long over 100.

**Block with copy:**

`LETTERING: the letterer adds it afterwards, so draw none of it. This panel will carry exactly {n} lettering area(s): {items joined by "; "}. Leave clear, low-detail space (sky, wall, floor or shadow) for them, preferably in the upper part of the frame, and keep faces, hands and important action outside that space. ` + NO_TEXT_V2

**Block without copy:** `LETTERING: none in this panel. ` + NO_TEXT_V2

**NO_TEXT_V2** = `Draw NO balloons, caption boxes, panel borders, frames or outlines, and no letters, numerals, pseudo-writing, symbols, logos or watermark anywhere, including on banners, flags, cloth, walls and documents.`

**Evidence:**
- Dialogue drift: 05:05-01 "fortresses", 06:03-05 "questioned", 06:07-01 "priests", 07:11-03 "churches". In ch9, 5.4 says "in Goa" and 3.3 says "the Portuguese".
- Markdown leaked into prompts, for example `*tharavadu.*`.
- The no-text rule was stated 4 times.
- v1's "Draw NO ... banners" contradicts ch9 2.2.
- 10 painted-border rejections.

**Expected effect:**
- The number of lettering areas is unchanged, so `reserves` and layout are unaffected.
- The no-text rule is stated once instead of four times.

### Change 5: page-aware continuity rows

**Row grammar.** A row may carry a span after its chapters: `| 9 @1-2.3 | ... |`.
- `@P` means page P.
- `@P.K` means that panel only.
- `@P-` means from page P to the end of the chapter.
- `@P.K-` means from that panel to the end.
- `@P-Q` and `@P.K-Q.L` are inclusive ranges.

**New functions:**
- `_span_contains(span, page, panel)`. It compares `(page, panel)` tuples. Defaults: start panel 1; end panel 999 when only a page is given; end (999, 999) when open-ended.
- `_rows_v2(block, chapter, page, panel)`. It uses `^\s*\|\s*(\d[\d,\s-]*?)(?:\s+epilogue)?(?:\s+@([\d.-]+))?\s*\|\s*(.+?)\s*\|?\s*$`.
- `_nagoji_look_v2`. It takes the first matching row in file order.
- `_character_look_v2`. It joins all matching rows, as v1 does.

**The one v1 edit:** `_look_for_chapter` skips any line that matches `_SPAN_ROW` (`^\s*\|\s*\d[\d,\s-]*?\s+@`). Without this, a v1 re-prepare against the live CM would paste span rows in as base text. The ch05-08 snapshots contain no `@`, so the freeze test in section 4 proves the output does not change. The v1 Nagoji regex already ignores span rows.

**CM data edit for ch9 (author sign-off needed).** Replace `| 9-15 |` with three rows:
- `| 9 @1-2.3 | Commander sheet: rust-red turban, cream tunic with the sleeves down to the wrists, broad red sash, cream trousers, boots, talwar. Nails healed but ridged. The old brand and the long white scar on the inner LEFT forearm stay hidden under the sleeve. |`
- `| 9 @2.4- |` with the same text, but `barefoot` in place of `boots`, plus: `...stay hidden under the sleeve unless this panel pushes the left sleeve back; then the brand is a pale puckered patch of raised ridges a hand's width above the wrist, with no letters or numerals, and the scar runs from the wrist toward the elbow beside it.`
- `| 10-15 |` keeping the existing text.

**Evidence:**
- Nagoji's hair came out loose from page 3 in 8 panels.
- Ibrahim's ash appeared before panel 5.3 in 6 panels.
- 7 panels showed Nagoji in the wrong-chapter look.
- 22 brand rejections. Brand failures were 0 of 17 with a "sleeves down" note and 21 of 55 without one.
- ch9 needs boots on page 1 and 2.1 to 2.3, and bare feet from 2.4.

### Change 6: clean up the looks

- **Header.** Replace the "AUTHORITATIVE CONTINUITY..." line with `LOOKS (face, build, hair, facial hair, scars, marks and ear ornament always follow these lines; footwear, sleeves, headwear, props in hand and pose follow the panel description above wherever it is more specific):`. Each look line is `{Display}: {look}`.
  - Evidence: ch08 p05-05 and p09-01, where the description says "barefoot" and the look says "boots".
- **Stubble.** In `_nagoji_look_v2`, remove `\s*\([^)]*captivity only[^)]*\)` from the constant identity unless the selected row starts with "Captivity sheet". Evidence: 26 stubble or beard rejections.
- **`_clean_base(text) -> (display, base)`**, applied to base lines only:
  1. Turn the label `- **Name** (...):` into `Name`. The display name has its parenthetical stripped.
  2. Delete parentheticals that contain `\bch\d`.
  3. Split on `(?<=[.;])\s+`.
  4. Drop clauses that match `\bch\d|\bchapters?\s+\d`.

  This removes, for example, "Dies ch27.", "Ch1-2 only." and Kayal's "Colachel in ch14" clause.
- **`_lint_look(key, base, rows)`** raises ValueError on any of:
  - base matching `\b(?:later|at first|going grey|dies|died)\b`;
  - a row matching `\b(?:until|afterwards)\b|\bafter (?:he|she|the)\b`;
  - either one matching `\b(?:pages?|panels?)\s+\d|\bepilogue\b|\bfrom (?:the )?(?:page|panel)\b`.

  This forces a CM fix for Padmini before ch9 can be prepared. Her base becomes `in her fifties; thick black hair coiled at the nape; simple gold; cotton sari hitched for walking, the old Kerala drape with no stitched blouse; long walking stick.` The author decides which chapter gets a grey-hair row. Evidence: Padmini's hair came out grey in 20 of 29 panels with her sheet.
- **`_guard_foreign_terms(...)`**, active only when the setting's scopes do not overlap `{"dutch","portuguese","sea"}`.
  - It checks looks of cast keys outside `FOREIGN_CAST = {duarte, joao, eustachius, karl, van_imhoff, dutch_envoys, donnadi}`, plus the rules, the must-match notes and the lettering items.
  - It searches for `\b(portuguese|dutch|voc|goa|european|british|redcoats?|church|chapel|jesuit|ships?|harbour|forts?|castle)\b`, minus the setting's `allow_terms`, and raises ValueError naming the panel, the term and the source.
  - The description, directions and setting text are author text and are exempt.
  - Evidence: Nagoji's "Commander sheet" row carried "Portuguese brand" in 72 prompts; 62% of them drifted, against 47% overall.

### Change 7: MUST MATCH notes from `character_notes`, for cast members only

The block is `MUST MATCH:` followed by `- {Display}: {note}`, and sits just before SETTING.

**ch9 drafts:**
- **nagoji:** `Chin and jaw cleanly shaved, smooth skin, no stubble or beard. On the earlobe a tiny flush gold stud with nothing hanging from it. Tunic sleeves down to the wrists unless this panel pushes the left sleeve back.`
- **padmini:** `Her hair is thick and BLACK with no grey at all. Muted earth-toned silk sari, the old Kerala drape with no stitched blouse; a sword with a worn leather-wrapped hilt at her right side.`
- **revathi:** `Deep indigo sari shot with gold, the end over her LEFT shoulder covering the chest, her RIGHT shoulder bare; braid looped with jasmine; a necklace of flat gold coins; gold armlets; a gold anklet; a thin sandalwood line at the hairline; kohl; no tali.`
- **ibrahim:** `His scar runs from the LEFT ear to the jaw, a thin pale line. Nothing on his forehead.`

**Evidence:** these are the reviewers' repeat flags, and the ch9 script's lost art notes.

### Change 8: cast lint in v2 `prepare`

Collect every panel where `_mentioned(description, key)` is true but the key is in neither the cast nor `not_shown[id]`. Raise once, listing all of them.

**Evidence:** 9 bearded or rag-clad stand-ins for Nagoji and 5 off-model kings. ch9 needs `not_shown` entries for 2.2 `["ramayyan"]` and 10.2 `["revathi"]`.

### Change 9: PEOPLE line and style cue

- With people in the cast: `PEOPLE IN THIS PANEL: {names}. Draw each named person once, with no doubles.` Horses (`kanka, kayal, grey_gelding, megha`) and groups (`madurai_troop, dutch_envoys`) are left out.
- With nobody: `PEOPLE IN THIS PANEL: no principal characters.`
- The style cue is in the header (change 1).

**Evidence:** 17 extra or cloned figures. All 11 photoreal rejections came from the 15 panels that had no reference image.

### Change 10: smaller wording fixes (low rank)

- **Insert line.** If the description matches `^\s*Insert\b`, add `INSERT: frame only what the description names, cropped tight; no full figure and no portrait unless the description asks for a face.` Evidence: 08:04-04.
- **Distant strips.** When the frame is a strip and the description matches `\b(far|small|distance|distant|long shot|tiny)\b`, the shape line says `keep the key action inside the middle half of the height` (no "faces and"). Evidence: 07:01-01.
- **Frame override.** The sidecar `frame` overrides the strip cue. Evidence: 07:06-05.
- **Letterer notes.** Drop directions that match `\b(letter|lettered|lettering|letterer|balloons?|captions?)\b`. These are notes for the compositor; there are 4 such directions in ch9-28 and none in ch9.

## 2. Gating

- **Opt-in.** v2 is used only when `prepare(..., art_direction_path=...)` is passed a sidecar whose `prompt_profile` is `"v2"`.
- **Chapter 9 onward must opt in.** Add the constant `V2_FIRST_CHAPTER = 9`. `prepare` raises `ValueError("Chapter N needs an art direction file (--art-direction); prompt profile v2 applies from chapter 9")` when `chapter >= 9` and no sidecar is given.
- **Chapters 1 to 8 stay on v1 by default.** Without a sidecar they take the unchanged v1 path. With one, they could opt in, but only into a sibling package; `_safe_write` already refuses to overwrite a canonical package.
- **v1 job output does not change.** It gains no new keys or files.
- **v2 job additions:**
  - Top level: `"prompt_profile": "v2"` and `"art_direction": {"path", "sha256"}`.
  - Per job: `"setting"`.
  - The package gets an `ART-DIRECTION-SNAPSHOT.json`.
- **`run_chapter.py` changes:**
  - Add `--art-direction` for prepare and pass it through.
  - `load_job` also checks `job["art_direction"]` when it is present.
  - `check_recorded_input` maps any `*-ART-DIRECTION.json` to `ART-DIRECTION-SNAPSHOT.json`.
- **CM edits are safe for existing packages.** `load_job` falls back to each package's `CONTINUITY-SNAPSHOT.md`. The live-CM tests (ch1 and ch28 Nagoji, ch24 principals) are unaffected by the ch9 row split and the new section.
- **Freeze ch9 after acceptance.** Once ch9 is accepted, extend the freeze test to it, rebuilding from its snapshots. Any later template change then needs `prompt_profile: "v3"`, so prepared packages cannot drift silently.

## 3. TDD: tests to write first, in `test_script_pipeline.py`

**Shared fixtures (new):**
- `V2_CONTINUITY` contains:
  - Nagoji: the constant with "(light stubble at most, captivity only)", plus rows `| 1 | Captivity sheet: ... |`, `| 9 @1-2.3 | Commander sheet: ... boots. |`, `| 9 @2.4- | Commander sheet: ... barefoot. |` and `| 10-15 | Commander sheet: ... the Portuguese brand ... |`.
  - Padmini: `in her fifties; thick black hair coiled at the nape. Dies ch27.`
  - Ibrahim: `("kapitan")` label, plus row `| 6-28 |`.
  - Varma: rows `| 22 @1-6 | Hill shrine... |` and `| 22 @7- | Fort room... |`.
  - Duarte: "Portuguese Jesuit".
  - The scoped section with the [all], [kerala, court], [portuguese] and [dutch] rules.
  - The old standing section.
- `direction()` returns a dict with:
  - setting `verandah` (kerala, time "morning light", with label, anchor and absent);
  - setting `cellar` (portuguese);
  - panels `page-01-panel-01` set to verandah, and `page-02-panel-04` set to verandah with time "night, oil lamps";
  - padmini in `character_notes`.

**Phase 0: guards that pass today and must stay green**

1. `V1FreezeTests.test_v1_prompts_of_prepared_chapters_5_to_8_are_byte_identical`. Skip unless the packages exist. Already confirmed at 202 of 202:
   ```python
   for chapter in range(5, 9):
       out = p.V15 / "chapters" / f"ch{chapter:02d}"
       job = json.loads((out / "IMAGEGEN-JOBS.json").read_text(encoding="utf-8"))
       continuity = p.load_continuity(out / "CONTINUITY-SNAPSHOT.md")
       source = json.loads((out / "SCRIPT-SNAPSHOT.json").read_text(encoding="utf-8"))["source"]
       panels = {x["id"]: x for page in source["pages"].values() for x in page["panels"]}
       for item in job["jobs"]:
           with self.subTest(chapter=chapter, panel=item["id"]):
               self.assertEqual(p.assemble_prompt(panels[item["id"]], chapter, continuity, item["cast"]) + "\n",
                                Path(item["prompt_path"]).read_text(encoding="utf-8"))
   ```
2. `test_v1_prepare_for_chapter_8_adds_no_v2_keys_or_files`. Run `prepare(8)` with the fixture. Assert the prompt contains "AUTHORITATIVE CONTINUITY", the job has no `prompt_profile` or `art_direction`, and there is no `ART-DIRECTION-SNAPSHOT.json`.

**Phase 1: tests that fail first**

*Gate*

3. `test_chapter_9_without_art_direction_is_refused`. `prepare(9)` with a cast file raises ValueError containing "--art-direction".
4. `test_art_direction_prepares_v2_and_records_profile_hash_and_snapshot`. Assert:
   - `job["prompt_profile"] == "v2"`;
   - `job["art_direction"]["sha256"]` equals the sidecar's sha and the snapshot's sha;
   - each job has `"setting"`;
   - `reference_images[0]` ends with `nagoji-v2.png` and the prompt contains "1) Nagoji".

*Spans and rows*

5. `test_span_contains_pages_and_panels`. Expected results:

   | Span | (page, panel) | Result |
   |---|---|---|
   | `@3` | (3, 5) | True |
   | `@3` | (4, 1) | False |
   | `@8.4-10` | (8, 3) | False |
   | `@8.4-10` | (8, 4) | True |
   | `@8.4-10` | (10, 9) | True |
   | `@8.4-10` | (11, 1) | False |
   | `@2.4-` | (99, 1) | True |
   | `@1-8.3` | (8, 3) | True |
   | `@1-8.3` | (8, 4) | False |
   | `@x` | any | ValueError |

6. `test_v2_nagoji_row_follows_page_and_panel`. For ch9, (1,1) and (2,3) contain "boots" and not "barefoot"; (2,4) and (11,5) the reverse. ch10 (1,1) contains "boots". No output contains "|" or "@".
7. `test_v2_character_rows_follow_page_and_panel`. Varma ch22 (3,2) contains "Hill shrine" and not "Fort room"; (7,1) the reverse; ch23 contains neither.
8. `test_v1_row_reader_skips_span_rows`. `p._look_for_chapter(varma_block, 22)` and `(…, 7)` contain neither "@" nor "Hill shrine".

*Looks*

9. `test_v2_looks_header_keeps_identity_and_yields_situation_to_the_panel`. The exact LOOKS header is present; "overrides the script on appearance" is absent.
10. `test_v2_drops_the_captivity_stubble_allowance_outside_captivity`. ch9 contains "CLEAN-SHAVEN CHIN" and no "stubble"; ch1 keeps "light stubble at most".
11. `test_v2_cleans_bullet_labels_and_chapter_scope_notes`. The Padmini line equals `Padmini Amma: in her fifties; thick black hair coiled at the nape.` The Ibrahim line starts `Ibrahim Marakkar:`. "kapitan", "Dies", "ch27" and "- **" are all absent.
12. `test_v2_refuses_life_arc_or_page_words_in_a_selected_look`. A Padmini base with "going grey later" raises with "padmini" and "later" in the message. A row `| 9 | Pages 1 and 2: hair loose. |` raises.
13. `test_v2_refuses_foreign_terms_from_the_bible_in_an_indian_setting`. ch10 nagoji in the verandah setting raises with "portuguese". It passes when the scopes are ["portuguese"] or when `allow_terms` is ["portuguese"]. Duarte in the verandah setting passes. A description that contains "Portuguese brand" passes.

*Rules*

14. `test_v2_rules_are_scoped_by_setting`.
    - Verandah: contains "No blood or gore" and "clay or brass".
    - Verandah does not contain: "Portuguese", "Dutch", "VOC", "Goa", "red coat", "iron ring", "Period: 1738", "upscale" or "STANDING CONTINUITY RULES".
    - Cellar: contains "iron ring" and does not contain "clay or brass".
15. `test_v2_refuses_a_bible_without_the_scoped_rules_section`. ValueError.
16. `test_v2_refuses_an_unknown_scope_tag`. `- [kerela] x` raises ValueError.

*Lettering*

17. `test_v2_summarises_copy_without_quoting_it`. Copy is:
    - `CAPTION: In Goa they wrote me down as a number.`
    - `NAGOJI: The Portuguese tried to convince me otherwise.`
    - `REVATHI (off): Our *fortresses* are both.`

    Assert none of those texts appear, and neither do "Goa", "Portuguese", "fortresses" or "*". Assert these appear: "exactly 3 lettering area(s)", "a caption (short)", "a speech balloon for Nagoji (medium)" and "a speech balloon for Revathi Bayi, speaking from off panel (short)". The Revathi case needs a Revathi block in the fixture.
18. `test_v2_silent_panel_needs_no_lettering_areas`. Contains "LETTERING: none in this panel"; does not contain "Leave clear".
19. `test_v2_states_the_no_text_rule_once_and_allows_unlettered_banners`. `prompt.count("Draw NO") == 1`; "banners or text" is absent; "including on banners, flags" is present.
20. `test_v2_drops_letterer_directions`. Directions ["(Letter as one balloon.)", "No text. Hold the silence."] keep only the second.

*Sheets*

21. `test_v2_sheet_line_lists_sheets_in_attachment_order`. With sheet_keys ["ibrahim","nagoji","padmini"], the prompt contains "3 attached image(s), in this order: 1) Ibrahim Marakkar, 2) Nagoji, 3) Padmini Amma", plus "use them only for faces, build, hair and costume", "not the hanging drop" and "not red as drawn". With sheet_keys [], "REFERENCE SHEETS" is absent.
22. `test_v2_nagoji_sheet_clause_matches_the_selected_look`. ch9 contains "full-length commander figure"; ch1 contains "captivity figure".
23. `test_v2_refuses_a_sheet_whose_caveat_hash_is_stale`. Patch the hash in `SHEET_CAVEATS["nagoji"]` to "0"*64; v2 `prepare` raises.

*Setting and end*

24. `test_v2_setting_paragraph_is_last_and_place_is_in_the_header`. The last `\n\n` part starts with "SETTING (this panel):" and contains the anchor, "Light: morning light" and the absent text. The first line contains "Place: " plus the label.
25. `test_v2_panel_time_overrides_setting_time`. page-02-panel-04 gives "Light: night, oil lamps" and no "morning light".
26. `test_v2_must_match_notes_only_for_cast_members`. With padmini cast, "BLACK with no grey" is present; without her, it is absent.
27. `test_v2_people_line_counts_people_not_horses_or_groups`. Cast ["kayal","madurai_troop","nagoji"] gives "PEOPLE IN THIS PANEL: Nagoji. Draw each named person once".
28. `test_v2_insert_and_distant_strip_wording`. "Insert, tight. His hands." produces the INSERT line. "Full width, bottom strip. Far down the beach, small." produces "keep the key action inside the middle half" without "faces and".
29. `test_v2_has_style_cue_and_no_dashes`. "never photorealistic" is in the first line; there is no chr(0x2014) or chr(0x2013).

*Validation*

30. `test_art_direction_must_cover_every_panel_and_use_known_ids`. Each of these raises ValueError: a panel with no resolvable setting, an unknown setting id, an unknown scope, a dash in the anchor, a chapter mismatch, an unknown key.
31. `test_v2_cast_lint_requires_mentioned_principals_cast_or_not_shown`. "Padmini, looking toward the doorway where Revathi went." with cast ["padmini"] raises with "page-01-panel-01" and "revathi"; it passes once `not_shown` lists revathi.

*Elsewhere*

32. In `test_run_chapter.py`: `test_prepare_passes_art_direction_and_load_job_checks_it`. A changed sidecar with no matching snapshot gives "Input changed since preparation".
33. Acceptance test, run after the data edits; skip unless `CHAPTER-09-ART-DIRECTION.json` exists: `test_chapter_9_prepares_clean_v2_prompts`. Run a real `prepare(9)` into a tempdir. Assert:
    - all 53 prompts end with a SETTING paragraph;
    - no copy chunk of 10 or more characters appears in any prompt;
    - no foreign term appears outside the description;
    - the Nagoji look line says "boots" only on 1.x and 2.1 to 2.3, and "barefoot" from 2.4;
    - no prompt contains "stubble";
    - every Padmini prompt contains "BLACK with no grey".

Then run the full pipeline suite with the README python. Per CLAUDE.md, coverage on the changed files must be over 80%. Also fix the stale comment at test line 127.

## 4. Risks and checking chapter 9 before a full generation

**Risks**
1. **Precedence.** Letting the description win on situational details could let a script costume error through, as with the ch1 beard. Identity items stay authoritative and MUST MATCH repeats them.
2. **Negative words.** The `absent` lists still name forts. They worked in the r2 corrections; keep each list to about 30 words and test it in the pilot.
3. **End-weighting is unproven** for this generator. The pilot A/B below tests it.
4. **Author sign-off.** CM edits (the scoped section, ch9 span rows, the Padmini base line) and the ch9 sidecar texts are drafts. The author must confirm:
   - the light for 10.3 and 10.4;
   - the Velinadu banners;
   - the chapter where Padmini starts to grey.
5. **Later chapters will be blocked by design.** The lints and the foreign-term guard will stop ch10-28 until their CM rows are cleaned. Known blockers:
   - Nagoji 10-15 "Portuguese brand";
   - Nagoji 17, 20, 22, 24 and 28 (page or event wording);
   - Varma 22 "after the attack";
   - De Lannoy 15 "after he changes";
   - the 24-28 uniform rows, which need `allow_terms: ["european"]`.
6. **Generator limits that prompts cannot fix:** scar side (13), triple stripes drawn instead of a single ash smear (3), handedness, and memory "stain" insets. Expect these rejections to continue; plan mirroring or compositing instead.
7. **The only v1 code change** is the span-row skip. The 202-prompt freeze test guards it.

**Verification on chapter 9**
1. Run the suite. Prepare ch9 into a scratch package (`run_chapter.py prepare --chapter 9 --package-dir chapters/ch09-pilot --cast-overrides ... --art-direction ...`). Do not use `chapters/ch09` yet, because `_safe_write` freezes whatever is written there.
2. **Prompt audit.** Add a read-only `audit_prompts(job_json_path)`, exposed as `script_pipeline.py audit --out <pkg>`, with a unit test. Targets:
   - 53 of 53 prompts end with SETTING;
   - 0 copy leaks;
   - 0 foreign terms outside author text;
   - rules make up under 10% of each prompt (v1: 43 to 53%);
   - median length at or below the v1 median for the same panels;
   - "Draw NO" exactly once per prompt;
   - the sheet order in the prompt matches `reference_images`;
   - the boots and barefoot split is correct.
3. Read five v2 prompts side by side with their v1 versions, assembled in memory.
4. **Five-panel pilot:**
   - 1.5: gate with guards; risk of a fort or bastions.
   - 2.2: banners and a crowd; the clerk who must not look like Ramayyan.
   - 5.4: Goa memory bleed, which carried Goa dialogue in v1.
   - 8.5: Padmini small in the background; hair, drape, extra figures.
   - 9.2: "Nagoji. Nothing moves in his face."; no location plus the commander sheet, the highest-risk class.
5. **Optional A/B.** Generate v1 prompts for 9.2 and 5.4 outside the package. `capture --prompt` would refuse them, so they cannot go into the package.
6. **Pass criteria:**
   - at least 4 of 5 pass on the first round (the ch5-8 baseline was 59 of 202, 29%);
   - 0 European or fort elements;
   - Nagoji has a clean chin and a flush stud, sleeves down and bare feet;
   - Padmini's hair is black;
   - no painted text or borders.
   If the pilot falls short, adjust the template, re-pilot in a new sibling package, and only then prepare the real `chapters/ch09`. After that, add ch9 to the freeze test.

**Files referenced**
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/script_pipeline.py`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/test_script_pipeline.py`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/run_chapter.py` (lines 25, 30-39, 80-90, 823, 871)
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/CONTINUITY.md`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/scripts/CHAPTER-09-SCRIPT.md`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/scripts/CHAPTER-09-CAST-OVERRIDES.json`
- New: `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/scripts/CHAPTER-09-ART-DIRECTION.json`
- Template wording: `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/chapters/ch08/prompts/page-02-panel-04-gen-r2.txt`

# Adversarial review

**Verdict: needs changes.** The overall direction is sound: per-panel setting placed at the end, scoped rules, sheet caveats, summarised copy and a gated v2. But several parts do not address the evidenced causes, contradict each other, or could still change chapter 8 output. Nothing was edited. All checks ran in memory with `PYTHONDONTWRITEBYTECODE=1`.

Confirmed:
- v1 reproduces ch05-08 exactly, 202 of 202.
- ch01-04 match 0 of 146.
- The live `CONTINUITY.md` is byte-identical to the ch05-08 snapshots (sha `33221d1c...`).
- ch9-28 have 86 cast gaps.
- The ch9 standing art notes are dropped by `parse_script`.

**Required changes**

1. **Validate before any write in v2 `prepare`.** `prepare` writes `CONTINUITY-SNAPSHOT.md`, `SCRIPT-SNAPSHOT.json` and each prompt before the per-panel lints run. `_safe_write` then freezes that partial package. Since the lints are expected to fail for ch10-28, every failed run would leave a package that can't be re-prepared after the bible is fixed. Assemble and lint all 53 prompts in memory first, then write. Also refuse v2 for chapters below 9 in their canonical package explicitly. Otherwise `ART-DIRECTION-SNAPSHOT.json` could land in `chapters/ch08` before the first conflicting prompt stops the run. Add a test that a lint failure leaves no files.

2. **The Padmini bible edit changes chapter 8.** In memory, with the proposed Padmini base line, v1 against the live bible changes 29 of 57 ch08 prompts. The freeze test can't see this because it rebuilds from snapshots. `run_chapter.py prepare` has no `--continuity`, so a sibling re-prepare (as `ch01-v2` was) would use the live bible. Either:
   - pin re-prepares of ch1-8 to the package snapshot; or
   - add a live-bible v1 freeze test for ch05-08 and keep Padmini's fix v2-only.

   Also add a fixture test showing that the new scoped-rules section leaves v1 output unchanged.

3. **`NO_TEXT_V2` contradicts the rules.** It bans "symbols ... including on banners, flags", which contradicts the design's own conch-on-red Travancore standard rule, Duarte's and Mathoo's crosses, and forehead marks. Say "no written characters, numerals or pseudo-writing" instead.

4. **The lettering classifier mislabels speakers in ch10-28.**
   - The "parenthetical contains letter" test turns these speeches into captions: `PADMINI (off, small lettering)`, `PADMINI (small, soft lettering)`, `DE LANNOY (inset, ... lettered untranslated)`.
   - Text lettered onto objects becomes "a speech balloon" with "leave sky or wall space, upper part", which contradicts descriptions that ask for empty bands on a leaf. Affected: `LEAF` (ch21, about 18 chunks), `LEDGER (lettered on the left page)`, `CAPTION (leaf)`, `CAPTION (stitched lettering)`.
   - These speakers are cast but don't equal an alias, so they become "another speaker": `RANI` (ch17), `THARAKAN` (ch13, ch15), `THOMA` (ch24), `ENVOY`, `SENIOR ENVOY` and `DUTCH SCRIBE` (ch11, ch18).

   Fixes:
   - Use a separate speaker alias map. Do not add to `CHARACTER_ALIASES`, which would change v1 cast inference.
   - Use word-boundary rules for "letter".
   - Add an "on an object" kind.
   - Keep placement parentheticals (left or right half, inset) as hints.

5. **Letterer notes inside descriptions go into the prompt verbatim.** Change 10 filters only directions (4 hits), but 68 descriptions in ch9-28 contain balloon, caption or letter words. Some of these mean a written letter, so do not filter bare "letter". In ch9:
   - 6.3: "Stack the balloons down one side"
   - 8.5: "Balloons in the upper third"
   - 10.4: "open sky above him for the captions"
   - 11.5: "Letterer: Revathi's tail goes to the foreground figure"

   These conflict with "Draw NO balloons" and "preferably upper". Add a sidecar `lettering_space` override per panel, plus one fixed sentence saying any such wording in the description means space only.

6. **The cast lint misses the evidenced cause.** None of the 13 cited stand-in or off-model panels I tested would be flagged by `_mentioned`. They refer to the person by pronoun or title: "studying him", "the king", "the stranger", "the man below". ch9 has three such panels:
   - 6.4: "not looking at him"
   - 9.1: "Her eyes never leave him"
   - 8.2: "His boots", with an empty cast

   Extend the lint to him/his/he when no male principal is cast, and to the king, Maharaja, diwan and Dalawa. Give `not_shown` a prompt effect too, for example "Nagoji is outside the frame".

7. **Remove the multi-state rows the evidence says fail.** The `| 9 @2.4- |` row and the Nagoji MUST MATCH both say "unless this panel pushes the left sleeve back". Use spans instead:
   - `@2.4-5.1`: sleeves down
   - `@5.2`: arm bared
   - `@5.3-10.5`: sleeves down
   - `@11-`: arm bared

   Drop the sleeve clause from the chapter-wide `character_notes`.

8. **Fix contradictions in the drafted text.**
   - The Nagoji MUST MATCH says "no stubble or beard", but acceptance test 33 requires that no prompt contain "stubble".
   - Padmini's LOOKS base says "cotton sari hitched for walking", while her MUST MATCH says "Muted earth-toned silk sari". Both end up in the same prompt.
   - The `[court, travancore_camp]` rule "white mundu with crossed leather belts" contradicts the ch16 blue-coat parade and the ch24-28 European-cut uniforms. Scoped rules need chapter ranges, or troop dress should move to the sidecar.

9. **Make Nagoji row selection fail closed.**
   - If no row matches, v1 falls back to the whole block; v2 must raise.
   - If rows overlap, raise instead of taking the first match.
   - Raise on a span past the chapter's page count.
   - Raise on a span row that names more than one chapter.

10. **`_panel_direction` must merge the page default with the panel override.** As specified, an override holding only `time` or `frame` loses the setting.

11. **The frame override and the distant-strip cue are fragile.**
    - The sidecar `frame` changes only the prompt. `layout_fit.layout_cues` still reads the description, so the prompt and the layout can disagree (the hard-crop problem the strip cue fixed). Feed the override into the layout, or reject contradictions.
    - The distant regex misfires in ch9: 7.5 is a face close-up but matches "far horizon", and 1.5 matches "small round shields". Make "distant" a sidecar flag.
    - Add a tall frame value for 6.3 and 10.4.

12. **Memory bleeds have no schema.** 5.4 (Goa cellar), 7.5 (Deccan fields) and the 10.3 inset each have one setting, and the anchor and absent list at the end will fight the bleed. Add a `bleed` field emitted before SETTING, or decide on compositing.

13. **Pre-generation notes and corrections land after SETTING.** 163 of 202 round-1 prompts had appended notes, and `capture --prompt` only allows appending. So every note or correction would come after SETTING and undo the end-weighting. Either:
    - move notes into the sidecar, emitted before SETTING; or
    - require every appended correction to end by repeating the SETTING paragraph, as the ch08 r2 template does.

    Audit the prompt actually sent, not just the base prompt.

14. **Add a Padmini sheet caveat.** The evidence says her nape coil on the sheet shows grey strands, behind 20 rejections, which is more than ear drop (11) or red scar (5). Her sheet's hash is `f43457565...`.

15. **The A/B baseline is invalid as planned.** After the row split, v1 for ch9 pastes the whole Nagoji block (7,982 characters, checked). Build the v1 A/B prompts from the pre-edit bible (the current file, which matches the ch05-08 snapshot).

16. **Widen the pilot.** It has no brand or insert panel, no Revathi full figure, no night lamp panel and no pronoun panel. Add:
    - 5.2 or 11.4 (brand, insert)
    - 3.1 (Revathi full figure)
    - 10.5 or 11.1 (night)
    - 9.1 (pronoun)

    For inserts, add a sidecar option to attach no sheet. Evidence 08:04-04 blames the attached sheet and the full identity row; an INSERT line alone removes neither.

17. **Back up and harden the freeze test.** `output/comic-v15-full-redo` is untracked in git (0 files tracked), so your CLAUDE.md rule needs a backup before these files are edited: commit them or copy `script_pipeline.py`, `run_chapter.py`, the tests and `CONTINUITY.md` to `.backup`. Also make the freeze test fail if `chapters/` exists but any of ch05-08 is incomplete, rather than skipping silently.

**Optional improvements**

1. **Cheaper alternative for the looks.** Put ch9's per-panel look overrides in the sidecar instead of adding span syntax to the bible. That avoids the v1 code edit, the bible split and the chapter 8 risk.
2. **Fix the sheets themselves.** Derived, author-approved, v2-only cropped sheets would remove the fort and the stubbled captivity inset (fort in 19 of 39 panels with the sheet, 0 of 18 without). They could also retouch the ear drop, Ibrahim's red scar and Padmini's grey strands. Keep `CONCEPTS` unchanged for v1.
3. **Strip prefixes from emitted looks.** Remove "Commander sheet:" and "Constant identity:", and use the prefix only to choose the sheet clause.
4. **End the SETTING paragraph on a positive sentence.** Put the absent list before Light.
5. **Display names.** Take them from a constant. Nagoji's block is a heading, not a bullet, so `_clean_base` can't produce "Nagoji". Use horse wording (coat, mane, markings) for Kayal's sheet.
6. **Lint after `_clean_base`, and have the audit list dropped clauses.** For example, Keshavrao's "the ch2 lock: about nineteen..." identity clause would be dropped, and the grey gelding's whole base line.
7. **Profile and job checks.**
   - Raise on an unknown `prompt_profile`.
   - Make `load_job` require `art_direction` when the profile is v2.
   - Record `sheet_keys` per job so a later freeze test can rebuild ch9.
8. **Add a sidecar `beat` field.** 74 panels in ch9-28 have descriptions of 8 words or fewer that carry dialogue (ch11 7.3 is just "Varma."). With the dialogue gone, nothing describes the expression.
9. **Cover the Madurai green-turban cause (6 rejections).** Add a carnatic rule, or add the troop note automatically whenever Raza is cast.
10. **CLI.** `script_pipeline.main` needs `--art-direction`, and the planned `audit` subcommand conflicts with its required `--chapter`. Reuse the audit's foreign-term check in `prepare` rather than writing a separate guard.
11. **Wording and guards.**
    - Change "outlines" to "a border line around the picture", so it doesn't read as a ban on ink line.
    - Refuse span rows for chapters below 9 in the bible.

Files checked:
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/script_pipeline.py`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/test_script_pipeline.py`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/run_chapter.py`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/layout_fit.py`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/CONTINUITY.md`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/scripts/CHAPTER-09-SCRIPT.md`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/scripts/CHAPTER-09-CAST-OVERRIDES.json`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/concepts/APPROVED-SHEETS.json`
- `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/chapters/ch08/prompts/page-02-panel-04-gen-r2.txt`

# Rejection evidence, chapters 5 to 8

**Result: 143 of 202 first-pass panels were rejected and 59 were picked.** The main cause is setting drift (94 panels). It comes mainly from what the panel prompt says and what is attached: panels that name no location drift, the standing rules are the only source of European words, and the Nagoji sheet's backdrop gets copied in. Dialogue words play a smaller part.

Note on prompt files: round 1 was generated from `<id>-gen-r1.txt`. That file is `<id>.txt` plus an appended "PRE-GENERATION NOTE" (163 of 202 have a note; the rest are identical). Both are quoted below. No project files were touched. Working files went only to the session scratchpad and `$TMPDIR`.

## 1. Picked vs rejected

| Chapter | Panels | Rejected | Picked |
|---|---|---|---|
| ch05 | 40 | 29 | 11 |
| ch06 | 49 | 24 | 25 |
| ch07 | 56 | 44 | 12 |
| ch08 | 57 | 46 | 11 |
| **All** | **202** | **143** | **59** |

## 2. Causes

Each panel can carry several causes. "Only cause" means it was the panel's single failing reason.

| Cause | Panels | ch05/06/07/08 | Example ids |
|---|---|---|---|
| **Setting drift** (forts, churches, ships, harbours, soldiers) | **94** (only cause in 10) | 22/14/34/24 | 05:01-02, 05:04-04, 06:05-02, 07:03-01, 08:09-01 |
| of which European elements | 66 | 21/14/23/8 | 05:02-03, 06:10-01, 07:08-03 |
| of which a hill fort only | 28 | 1/0/11/16 | 08:01-04, 08:12-04, 07:05-05 |
| Morion and breastplate soldiers | 18 | | 05:07-01, 06:08-04, 07:01-04 |
| Iron ring, shackle or chain prop | 13 | | 05:01-02, 06:03-05, 07:09-01 |
| **Character sheet backdrop copied** | 4 named by the reviewer, about 30 inferred | | 07:01-05, 08:06-04, 08:09-01, 08:10-05 |
| **Costume or look** | **79** | 11/14/18/36 | see below |
| Padmini: grey hair (rule: "thick BLACK hair") | 20 | ch08 only | 08:06-01, 08:06-02 (only cause) |
| Nagoji: stubble (16) or beard (10) (rule: clean-shaven chin) | 26 | | 08:12-04, 08:09-04, 06:09-03 |
| Nagoji: hair loose from page 3 (rule: tied back) | 8 | mostly ch05 | 05:04-02, 05:08-01 |
| Varma off model (beard, bare head, robe, knot on wrong side) | 7 | | 06:02-01, 06:05-04, 07:08-01 |
| Madurai troop in green turbans (rule: only Raza wears green) | 6 | ch07 | 07:02-05, 07:05-02 |
| Nagoji in captivity or commander look in the wrong chapter | 7 | | 06:09-03, 08:04-05, 06:08-04 |
| Ponnan, Maravar riders, guards, courtiers | about 12 | | 07:04-03 (zip fastener), 05:07-04 |
| Framing or beat wrong | 55 | 13/10/15/17 | 06:08-05, 07:06-05, 08:04-04 |
| Place mismatch, not European (inland plain, mandapam, waterfront) | 30 | 2/2/8/18 | 07:04-02, 08:07-02 |
| Brand wrong (placement, unasked-for, cross or letters) | 22 | 1/0/5/16 | 08:02-02 (only cause), 07:09-04 (wrong arm) |
| Lighting or time of day | 20 | 9/1/10/0 | 07:10-01, 07:12-03 |
| Scar wrong | 17 | 11/3/3/0 | |
| of which wrong side | 13 | | 05:01-05, 07:04-01 |
| of which red | 5 | | 05:01-04, 06:01-02 |
| Extra or cloned figure | 17 | | 06:08-05, 06:10-02, 08:09-04 |
| Ear ornament fail (hanging drop or earring) | 11 | 2/9/0/0 | 06:01-05, 05:05-05 |
| Ear drop as note only | in 66 reviews | | |
| Photoreal rendering | 11 | 3/1/5/2 | 07:06-03, 08:12-03 |
| Painted border | 10 | | 05:02-03, 07:05-03 |
| Text or pseudo-text | 7 | | 07:02-03 (brand reads "Pett"), 07:12-01 ("Yor"), 06:03-01 (map) |
| Anatomy | 7 | | 05:01-03 (extra hand), 07:01-02 (horse leg) |
| Forehead marks (Ibrahim ash, official's dot) | 6 | ch05 only | 05:03-02, 05:04-03 (only cause), 05:08-04 |
| Other (glass lantern, grey horses, ritual lamps, flags, writing boards) | 17 | | 05:05-04, 08:02-03 |

## 3. Top three causes: prompt text that pulled the image wrong

### A. Setting drift (94)

**1. The panel names no location.**
- In ch05, all 13 panels that named no location in the scene line or note drifted. Only 9 of 27 that named one did. In ch07 the figures are 17 of 22 vs 17 of 34.
- 05:01-02 says only "Two-shot. Ibrahim ... crouched on his heels at the edge of the mat". There is no hut. The result was a fort quay with a church, ships and an iron ring.
- 05:04-02 says "Ibrahim ... up on the cart now, looking down". The result was a Portuguese fort, church tower and morion soldiers.
- 07:05-05 says "Water pause, midday, the air rippling." There is no beach. The result was an inland riverbank under a Deccan fort.
- 07:01-05 says "Reverse angle. Nagoji, mounted on a plain grey". The result was a Portuguese fort courtyard.

**2. The standing rules are the only European vocabulary.** The rules block is identical in all 202 prompts. For 42 of the 66 European-drift panels, it was the only European text in the prompt:
- "Interrogation ropes hang from an iron ring for binding wrists" lines up with the 13 iron ring, shackle or chain rejections.
- "Portuguese guards must not read as British redcoats or as Dutch blue-coats. The Dutch VOC soldiers are the blue coats." lines up with the 18 morion-soldier rejections.
- "Period: 1738-1753 Malabar coast, Travancore and Portuguese Goa."
- "European lanterns belong only to Portuguese and Dutch settings."

**3. The Nagoji sheet's backdrop is copied.** I opened `nagoji-v2.png`. Behind the full-length commander figure is a hill fort on a rocky hill. The CAPTIVITY inset is a stone cell with a barred window. The LATER LIFE inset has a stone fort wall with palms.
- A hill fort appeared in 19 of 39 ch08 panels with this sheet attached, and in 0 of 18 without it. In ch07 the figures are 9 of 33 vs 2 of 23.
- Some prompts point straight at it. 07:01-05: "drawn from the full-length commander figure on the Nagoji sheet". 07:08-03 note: "as on the sheet's full-length commander figure". Four of the five prompts with this phrase drifted.
- Nagoji's ch07 and ch08 continuity row begins "Commander sheet: rust-red turban...". It is in 72 prompts, and 45 of them drifted (62%, against 47% overall).

**4. Dialogue words make it worse but are not the root cause.** 24 of the 59 picked panels also contained such words.
- 05:05-01 "IBRAHIM: Our fortresses are both." produced a walled fort with a domed tower.
- 05:04-04 "ride down toward the ports, strike at caravans and warehouses" produced a quay, ships and a crane.
- 06:03-05 "RAMAYYAN (off): They questioned you." produced a dungeon with shackles.
- 06:05-02 "whispers wrong directions into the ear of a pilot" produced a Portuguese court.
- 06:07-01 "trust is for priests" produced a Jesuit figure.
- 07:12-05 "On Deccan soil ... against a gun" produced a castle on a cliff.

### B. Costume or look (79)

**1. The cast list leaves out principals the text names or implies.** When that happens the panel gets no sheet and no continuity row, and the generator invents the character.
- This gave 9 bearded or rag-clad stand-ins for Nagoji: 05:06-05, 05:07-05, 06:09-01, 06:09-03, 07:11-03, 08:04-05, 08:07-05, 08:08-05, 08:09-04.
- It gave 5 off-model kings: 06:02-01, 06:05-04, 06:08-01, 07:03-02, 07:08-01.
- Examples: 08:08-05 "Padmini Amma, close, studying him." has cast ['padmini']. 06:05-04 "speaking to the king and not to the diwan" has cast ['nagoji']. 07:08-01 "answering the king at a respectful distance" has no Varma in the cast.

**2. Padmini's whole-life bible row is pasted in verbatim.** It reads "in her fifties at first; thick black hair coiled at the nape, going grey later; ... Dies ch27."
- Her hair came out grey in 20 of the 29 panels with her sheet attached.
- Her sheet's nape-coil detail also shows grey strands.

**3. Rows that hold several states at once.**
- ch05 Nagoji: "Pages 1 and 2 ... hair loose ... From page 3: ... hair tied back". Hair came out loose on page 3 and later.
- ch06 Nagoji: "hair loose or tied back".
- Ibrahim, in every ch05 prompt: "Ash on his forehead from panel 5.3 to the end of the chapter." Ash appeared on pages 3 and 4 (05:03-02, 05:04-03), whose notes did not say "no ash".

**4. The stubble token.** The Nagoji row says "CLEAN-SHAVEN CHIN (light stubble at most, captivity only)". The sheet's stubbled captivity inset adds to it. Result: 26 stubble or beard rejections.

**5. The troop rule only travels with the troop's cast tag.** All 6 green-turban rejections had cast ['raza'] or ['nagoji','raza'], with no white-turban line. Panels that had `madurai_troop` in the cast passed.

### C. Framing or beat (55)

- **Misplaced parenthetical.** 06:08-05 reads "eyes never leaving the man on the mat (face from the sheet only; a cream-and-gold turban with a jewelled peacock-feather crest)". 06:10-02 reads "looking only at the man below (face from the sheet only; ...)". Both produced a second man in the crested turban.
- **Contradictory frame instructions.**
  - 07:06-05 has "FRAME SHAPE: ... about 3 to 1", and then its note says "Ignore the 3 to 1 FRAME SHAPE line above".
  - 07:01-01's boilerplate "keep faces and the key action inside the middle half of the height" works against "Far down the beach, small". The troop came out large in the foreground.
- **Full identity row and full sheet attached to an insert.** 08:04-04 asks for "Insert: where her eyes go. Nagoji's left hand at his belt" and got a waist-up portrait.
- **Tactical words beside a negative.** 07:06-05 has "the Dutch line" and "level their muskets" alongside the note "There are no arrows, letters, symbols". The grooves were drawn as arrows.
- **Missing pose.** 08:10-04 "easing back against the trunk" never says seated, and she was drawn standing.

## 4. Other prompt-assembly causes

- **Brand.** Every ch07 and ch08 Nagoji prompt carries "The Portuguese brand on the inner LEFT forearm ... seen when sleeves are pushed up". The commander figure on the sheet also has rolled sleeves.
  - Nagoji panels with a "sleeves come down to his wrists" note: 0 of 17 had brand failures. Without it: 21 of 55.
  - ch08 had no such notes and 16 brand rejections.
  - "blurred past reading" seems to invite lettering: 05:01-03, 07:02-03, 07:12-01.
- **Photoreal.** All 11 photoreal rejections are among the 15 panels with no reference image; none of the 187 panels with references came out photoreal. Only 2 of 202 base prompts contain any style word; "V15 graphic novel panel" is the only style cue.
- **Lighting.** 8 of the 10 ch07 panels rejected for lighting have no time-of-day word in their prompt.

## 5. Not prompt problems (generator or asset limits)

- **Scar side (13).** Prompts state the side and the head orientation explicitly. For example, the 05:01-05 note says "Ibrahim large at screen right ... LEFT cheek and the pale scar toward the camera", and the result is still mirrored. This is a left/right limit in the generator.
- **Red scar (5).** The "LEFT EAR TO JAW SCAR" detail on the Ibrahim sheet is drawn red, even though notes say "no red or pink". This is an asset conflict.
- **Ear drop (11 failures, 66 mentions).** Every head on the Nagoji sheet wears a hanging gold drop. The text says "small gold ear stud" or "tiny flush gold dot". Again an asset conflict.
- **Tripundra (3).** The notes said "a single faint grey-white smear, not lines" and the generator still drew three stripes.
- **Painted borders (10).** The prompt says "Draw NO ... frames".
- **Anatomy (7) and handedness.** 05:01-04 and 05:04-05 asked for the "left thumb" and got the right hand.
- **Long-shot scale.** 07:02-02 asked for a long shot and got a medium shot.
- **Memory "stain" insets.** A single generation cannot do these: 08:08-02, 08:11-01, 06:05-01. They need compositing.

# Prompt audit

**V15 prompt drift audit: chapters 5 to 8 samples, and chapter 9's setting**

Nothing was edited or created.

**Root cause.** In `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/script_pipeline.py` (`assemble_prompt`, line 315), the standing block is `continuity["raw"].split("## Standing rules for generated art", 1)[-1]`. That pastes everything after line 124 of `CONTINUITY.md` into every prompt, whatever the chapter or setting. The header line "AUTHORITATIVE CONTINUITY, which overrides the script on appearance" then lets the character looks win over the panel description.

**1. Length and share (by characters)**

| Prompt | Total | Standing rules | Panel description | Character looks | Dialogue | Lettering boilerplate |
|---|---|---|---|---|---|---|
| ch07 p01-04 | 3586 ch / 573 w | 43.4% | 13.3% | 17.1% | 6.0% | 18.6% |
| ch07 p05-05 | 3503 / 549 | 44.4% | 9.3% | 23.0% | 2.6% | 19.0% |
| ch07 p11-03 | 2936 / 468 | 53.0% | 5.6% | 10.6% | 6.1% | 22.7% |
| ch08 p05-05 | 3478 / 551 | 44.7% | 3.6% | 25.6% | 5.2% | 19.2% |
| ch08 p09-01 | 3663 / 587 | 42.5% | 7.5% | 24.3% | 5.9% | 18.2% |
| ch05 p07-01 | 3526 / 560 | 44.1% | 5.0% | 28.1% | 2.2% | 18.9% |
| ch06 p05-04 | 3006 / 474 | 51.7% | 3.5% | 15.2% | 5.4% | 22.2% |

- The header line takes about 1.6% in each.
- The standing block is the same 1,555 characters (245 words) in all seven.
- No-text and lettering instructions (standing bullet 1 plus the boilerplate) take 24 to 30% of every prompt. The no-text rule is stated 4 times.
- Only about 50 of the 245 standing words apply to every panel: the no-text bullet and the gore bullet.
- Not part of an image prompt at all: the print bullet (29 words) with "`~/AI/upscalers/upscale2x.py` (Real-ESRGAN x2plus, BSD-3-Clause)".

**2. Europe and captivity terms in the standing block (all 7 prompts)**

Each prompt carries Portuguese x4, Dutch x4, British x2, redcoats x2, blue-coats or blue coats x2, plus VOC, Goa and European once each. The exact phrases:

- "Portuguese guards must not read as British redcoats or as Dutch blue-coats. The Dutch VOC soldiers are the blue coats."
- "Period: 1738-1753 Malabar coast, Travancore and Portuguese Goa."
- "Indian troops, like the Portuguese and the Dutch, must not read as British redcoats."
- "European lanterns belong only to Portuguese and Dutch settings."
- "No nooses. Interrogation ropes hang from an iron ring for binding wrists, never tied as hanging nooses."

By contrast, no panel description names Kerala or Travancore. Only two say where the panel is set: "on the beach" (ch07 p1-4) and "the stone platform under the jackfruit tree" (ch08 p9-1). "Kerala" appears in panel-specific text only once, as "the old Kerala drape" (Padmini, ch08). The lamp rule starts "In Kerala and Travancore settings", but no prompt says which setting applies, so the generator cannot use that condition.

**3. Prompt by prompt**

- **ch07 p01-04 (beach, Madurai troop).**
  - Panel-specific text is clean. The risk is that three white-clad troop rules compete in one prompt:
    - Madurai: "high-wrapped white or off-white turbans"
    - Maratha: "background Maratha riders ... wear white or cream angarkhas and pagdis"
    - Travancore: "its regular troops wear white mundu with crossed leather belts"
  - Two flag rules ("the Travancore standard is a silver conch on red" and "Raiders' and rivals' banners are plain, unlettered cloth") sit beside "bamboo lances gleaming with no pennons".
  - Minor mismatch: "salutes with his spear butt" against "bamboo lances" and "Madurai lancer".
- **ch07 p05-05.**
  - No location given ("Water pause, midday, the air rippling").
  - Looks add "The Portuguese brand", "captivity only" and "not a cross".
  - "seen when sleeves are pushed up" invites rolled sleeves.
  - Dialogue: "This is not war."
- **ch07 p11-03 (highest risk, 53% standing).**
  - The description is 28 words with no setting.
  - Dialogue: "The Portuguese tried to convince me otherwise" and "I have seen you bow your head in their churches".
  - Together with Portuguese x4 and Goa, the only scenery cues point to churches and Goa.
  - Ibrahim's look says "shorter than the fishermen", but no fishermen are in the panel.
- **ch08 p05-05.**
  - Description is 19 words with no setting.
  - Contradiction: the description says "Nagoji, barefoot", but the authoritative look says "cream trousers, boots, talwar", and the override header makes boots win.
  - Looks: "Portuguese brand", "captivity".
  - Dialogue: "I am a soldier" and "Whose pepper pays for their powder?"
- **ch08 p09-01.**
  - Same conflict: "(rust-red turban, barefoot)" against "boots".
  - The copy contains the markdown "*tharavadu.*", which could leak into the art as text.
- **ch05 p07-01.**
  - Looks give both time states. The panel is on page 7, yet the prompt includes "Pages 1 and 2 ... bare-chested in the cream captivity dhoti", "rope burns across the chest, faint chafe rings at the ankles, no irons".
  - Ibrahim's "Ash on his forehead from panel 5.3" is a page reference the generator cannot use. It sits next to Nagoji's "No forehead marks", so the ash could transfer between them.
  - Caption: "In Goa they had written me down as a number."
  - The setting is only "the mat" and "the platform".
- **ch06 p05-04 (highest risk with ch07 p11-03, 51.7% standing).**
  - The description is 19 words and does not describe the court: "speaking to the king and not to the diwan. Reverse angle, the open side on screen right".
  - The only place names in the whole prompt are "Malabar coast, Travancore and Portuguese Goa", plus Portuguese guards and Dutch VOC soldiers.
  - Dialogue: "You mistrust pilots?" and "men who steer ships".

**4. Contradictions in every prompt**

- The lettering rule says "Draw NO balloons, boxes, frames, outlines, banners or text of any kind ... anywhere else". This conflicts with the flags bullet, which says how banners should look.
- The override header lets the chapter-level look ("boots", "sleeves are pushed up") beat panel-level facts.
- Rules that only apply in some cases are stated without their condition being resolvable: the lamp rule, "in memory and vision panels only", and Portuguese guards.
- Naming things in a "do not" form still puts them in the prompt: "not a cross", "no glass lanterns", "never tied as hanging nooses".

**5. Chapter 9 (pages 1 and 2)**

**Setting.** "Princess of Velinadu":

- A pre-dawn ride from Padmini Amma's estate inland, through paddy bunds, pepper gardens, a pond and a tree shrine "with ... oil lamps".
- It ends at Velinadu Kovilakam, a matrilineal Nair royal household: "a low ring of red laterite and earth circling a cluster of tiled roofs", "a central hall with a tiled roof, banners hanging heavy and still", a stone verandah, "a brass tumbler of coconut water and a banana leaf parcel", and "lamplight and the shadows of drummers".
- The guards and men of the house are Nair: "bare-chested, white mundu hitched to the knee, hair knotted high at the front, no turbans", carrying "spears and small round shields".
- There are no Europeans, ships, Travancore regulars or troop scenes.
- Cast overrides use nagoji, padmini and revathi, plus ibrahim in 1.1 and 1.2.

**Standing rules that would mislead it:**

1. **"Period: 1738-1753 Malabar coast, Travancore and Portuguese Goa."** Goa does not appear, "coast" pulls the scene seaward, and the script says "The road winds inland through low green hills".
2. **"Portuguese guards must not read as British redcoats or as Dutch blue-coats. The Dutch VOC soldiers are the blue coats."** The chapter has a "GUARD" speaker and gate guards (1.5, 2.1). The only guard-uniform guidance in the prompt would be European. 1.5's "No towering walls, no bastions", together with gate and guards, already leans toward a fort.
3. **Flags bullet.**
   - "the Travancore standard is a silver conch on red" would be the only banner spec available for the Velinadu banners in 2.2.
   - "its regular troops wear white mundu with crossed leather belts" may add belts to the bare-chested Nair guards.
   - Velinadu is neither "Raiders'" nor "rivals'".
   - The lettering line "Draw NO ... banners" directly contradicts 2.2.
4. **"Interrogation ropes hang from an iron ring for binding wrists."** The chapter is a judgment ("taking me to be weighed", "That is part of the weighing", "change their fate with a word"). The script also has "inside the ring", "iron stylus" and "the sky the grey of old iron", which overlap with the rule's wording.
5. **Lamp rule.** The first clause helps (1.2 shrine lamps, 2.4 lamplight). The tail "European lanterns belong only to Portuguese and Dutch settings" only adds European terms.
6. **"Indian troops, like the Portuguese and the Dutch, must not read as British redcoats",** the Maratha clause and the print bullet are irrelevant here.

**Looks that would override the chapter 9 script:**

- **Nagoji (chapters 9 to 15 row):**
  - "boots", while the script says "Boots on page 1 and in 2.1 to 2.3 only" and barefoot after.
  - "seen when sleeves are pushed up", while the script says "Tunic sleeves DOWN to the wrists (not rolled as on the sheet)".
- **Padmini:** "cotton sari hitched for walking ... long walking stick", while the script has "muted earth-toned silk sari hitched for riding", "a sword with a worn leather-wrapped hilt at her right side" and "stick strapped to the saddle on page 1". The sword would likely be dropped.
- **Revathi:** "deep blue or indigo sari with gold" only. It is missing the script's drape ("over her LEFT shoulder and covering the chest, her RIGHT shoulder bare"), "No tali", the anklet and the kohl, and it has no "no stitched blouse" note like Padmini's.
- **Shares (my estimate):**

  | Panel | Total | Looks | Description |
  |---|---|---|---|
  | 1.2 (landscape, "riders small in the middle distance", three full looks) | ~4,030 ch | ~31% | ~10% |
  | 2.5 (Revathi's feet only) | ~3,670 ch | ~26% | ~6.5% |

- **Dialogue terms:** "company men who thought themselves safe until women closed the gates on them", "sign treaties", "Waiting is familiar to any soldier".

# Prompt assembly map

**V15 prompt assembly map** (files read only; nothing was changed)

Files: `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/script_pipeline.py` (SP), `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/CONTINUITY.md` (CM), `/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/test_script_pipeline.py` (T).

## (1) Ordered sections of an assembled prompt

`assemble_prompt` is at SP 313-348. The string is built at SP 339-346 in this order:

1. **Header plus panel description** (SP 340): `f"V15 graphic novel panel {panel['id']} for chapter {chapter}. {panel['description']}\n\n"`. The panel id looks like `page-05-panel-02` and is built in `parse_script` at SP 134.
2. **Frame shape, optional** (SP 336-338): `"FRAME SHAPE: a wide horizontal strip, about 3 to 1 (width to height), filling the whole width; keep faces and the key action inside the middle half of the height.\n\n"`. It appears only if `layout_fit.layout_cues(panel)["solo"]` is true (layout_fit.py 513-536). That function reads the description for cues such as "full width", "strip", "tier" or "splash".
3. **Script directions, optional** (SP 341): `"SCRIPT DIRECTIONS (never render as lettering): " + " ".join(panel['directions'])`. It appears only when the panel has directions.
4. **Continuity looks** (SP 342, with the looks built at SP 314): `"AUTHORITATIVE CONTINUITY, which overrides the script on appearance:\n"`, then one line per cast key, `f"{key}: {_character_look(continuity, key, chapter)}"`.
   - Nagoji goes through `_nagoji_look` (SP 220-229).
   - Everyone else goes through `_character_look` (SP 232-239) and then `_look_for_chapter` (SP 253-264).
   - The order follows `cast`, which is sorted alphabetically (SP 275, 277, 286).
5. **Standing rules** (SP 343, extracted at SP 315): `"\n\nSTANDING CONTINUITY RULES:\n" + standing`, where `standing = continuity["raw"].split("## Standing rules for generated art", 1)[-1].strip()`. That is everything after the heading to the end of CM, currently CM 126-133.
   - Quirk: if the heading were missing, `[-1]` would inject the entire bible.
6. **Copy rule** (SP 344, built at SP 316-333): `"No text of any kind in generated art. Do not render the following exact copy; it is composited later:\n"`, then the copy lines (or `[no copy]`), then `space_rule`.
   - With copy (SP 320-326): `"Leave clear, low-detail space (sky, wall, floor or shadow) for exactly {len(copy)} lettering area(s), one per copy chunk, preferably in the upper part of the frame..."`, `"Draw NO balloons, boxes, frames, outlines, banners or text of any kind..."`, `"This replaces any earlier mention of blank balloon or caption reserves."` and `"Keep faces, hands, and important action outside those areas."`
   - Without copy (SP 328-329): `"No lettering areas are needed. Draw NO balloons, boxes, frames or text of any kind. This replaces any earlier mention..."`
7. **Closing line** (SP 345): `"\nNo invented lettering, pseudo-writing, logos, watermark, gore, or anachronistic costume."`
8. **Dash guard** (SP 347): `_reject_dashes(prompt, ...)` raises an error if an em or en dash appears.

**Afterwards, in `prepare`:** the prompt is written to `prompts/<id>.txt` (SP 405-407) and put in the job as `image_gen.args.prompt` (SP 416-417). Corrections can only be appended later, through `run_chapter.py capture --prompt`, which requires the new prompt to begin with the prepared one (run_chapter.py 881-887). An example is `chapters/ch05/prompts/page-01-panel-01-gen-r1.txt`, which ends with an appended "PRE-GENERATION NOTE". Nothing in CM's preamble (CM 1-17) or the Nagoji "Note for scripts" (CM 46-48) is injected, unless no Nagoji row matches; see section 5.

## (2) Where verbatim script text enters the prompt

**Panel description**
- Enters at SP 340, verbatim.
- It is captured at SP 137 (`panel_match.group(3)`). Wrapped plain lines are appended at SP 162-166 (`current_panel["description"] += " " + line.strip()`). Any costume notes in the script (for example ch05 1.1 "costume override: ...") reach the prompt word for word.

**Directions**
- Enter at SP 341.
- Two sources:
  - Italic lines inside a panel, `*...*`, except `*Page turn.*` (SP 150-154).
  - Quoted `> *No text...*` lines, which `_copy_line` rejects as copy (SP 88-89, 160-161). For example, `> *No text. Let the buttons shine.*` becomes the direction "No text. Let the buttons shine."

**Dialogue and captions**
- Enter at SP 317 and 332 as `f"{item['speaker']}: {item['text']}"`, listed under "Do not render the following exact copy".
- They are parsed by `_copy_line` (SP 84-100). The text is exact, including markdown asterisks (ch05 example: `CAPTION: The man they called *kapitan* introduced himself as Ibrahim.`).
- The number of copy items sets "exactly N lettering area(s)" (SP 321).

**Indirect uses (not quoted into the prompt)**
- Description plus copy text drive cast inference (SP 278-285), and the cast decides which continuity looks and sheets are used. In practice this only matters for chapter 1, because chapters after 1 require a complete cast overrides file (SP 391-392, validated at SP 370-379). A `"default"` key would fail validation as an unknown id, so the `"default"` branch at SP 276-277 cannot be reached through `prepare` with a file.
- The description also drives the frame shape (SP 338).
- The script title is not put in the prompt.

## (3) Portugal, Goa, guards, forts, churches, ships and European elements

**In the standing rules (CM 126-133)**

These are injected whole into every prompt, for every chapter and every panel. They are not scoped by chapter, page or cast; SP 315 does no filtering.
- CM 128: "Portuguese guards must not read as British redcoats or as Dutch blue-coats. The Dutch VOC soldiers are the blue coats." This is unconditional, so a ch5 Travancore healer's hut panel receives it too (confirmed in `chapters/ch05/prompts/page-01-panel-01-gen-r1.txt`).
- CM 130: "Period: 1738-1753 Malabar coast, Travancore and Portuguese Goa. No anachronisms." Unconditional.
- CM 132 (last sentence): "Indian troops, like the Portuguese and the Dutch, must not read as British redcoats." Unconditional.
- CM 133: "In Kerala and Travancore settings, oil lamps are clay or brass with open wicks; no glass chimneys and no glass lanterns. European lanterns belong only to Portuguese and Dutch settings." This is conditional only in its wording ("settings"). It is still injected everywhere.
- Forts, churches and ships: the standing rules never mention them. The only CM hit for "fort" is CM 57 (a Varma ch22 row, "Fort room after the attack"), which is chapter-scoped. There are no hits for church, chapel or ship anywhere in CM.

**Elsewhere in CM**

These enter only through character looks, so they depend on the cast and, where rows exist, the chapter.
- **Nagoji chapter rows (scoped by chapter):**
  - "Portuguese brand": CM 30 (ch4), 33 (7-8), 34 (9-15), 35 (16).
  - "white European-cut coat ... buckled European riding boots": CM 42 (ch24, from page 14), 43 (25-27), 44 (ch28, from page 6).
- **Duarte base line (CM 68):** "thin, gaunt Portuguese Jesuit ... plain black cassock ... small cross on a thin chain". Not chapter-scoped; it is injected whenever `duarte` is in the cast.
- **Joao base line (CM 71):** "ruddy Portuguese gaoler ... Ch1-2 only". "Ch1-2 only" is prose, not a row, so the code does not enforce it.
- **Dutch entries:**
  - De Lannoy ch11 row (CM 78): "Dutch blue coat and black tricorne".
  - Van Imhoff (CM 104): "Dutch Governor of Ceylon, ch11 only". Prose, not enforced.
  - Dutch envoys rows (CM 106, 107): ch11 and ch18.
  - Donnadi (CM 113): "senior surviving Dutch officer at Colachel ... blue officer's coat".

## (4) Character reference sheets

**How sheets are chosen**
- `CONCEPTS` (SP 64-68) maps the three V13 sheets under `comic-v13-reference-redesign-v1/concepts/`: `nagoji` to `nagoji-v2.png`, `varma` to `varma-v1.png`, `temple_priest` to `temple-priest-v1.png`.
- `_concept_sheets()` (SP 289-301) adds every entry in `concepts/APPROVED-SHEETS.json`:
  - Each sheet's sha256 is checked; a mismatch raises "Approved sheet changed since approval".
  - A key that is already in `CONCEPTS` raises an error (SP 295-296).
  - The JSON currently holds 18 keys: ramayyan, padmini, revathi, eustachius, keshavrao, dhanaji, ibrahim, duarte, joao, karl, raza, ponnan, mathoo, senior_rani, prince, savitri, kanka and kayal. CM 10 says "17 V15 sheets".
- `_references(cast, description="")` (SP 304-306) is `[str(sheets[key].resolve()) for key in cast if key in sheets]`.
  - It follows cast order, which is alphabetical.
  - The `description` parameter is unused.
  - Cast keys with no sheet get no image. These include yusuf, thoma, avraham, nandini, van_imhoff, dutch_envoys, donnadi, chanda_sahib, madurai_troop, kollamkara, grey_gelding, megha, the Nagoji parents, bhalerao and sowcar.
  - `FACE-REFERENCES-v15.json` is not referenced by any pipeline .py or .js file.

**How sheets are attached**
- In `prepare`, sheets go into `reference_images`, `reference_image_sha256` and `image_gen.args.referenced_image_paths` (SP 404, 408-417).
- `imagegen_driver.js` line 12 calls `view_image` on each sheet, and lines 13-15 pass `referenced_image_paths` (deleted if empty).
- `run_chapter.load_job` re-checks the hashes (run_chapter.py 86-90).
- Example: ch05 job 1 has cast `['ibrahim','nagoji']` with refs `09-ibrahim-marakkar-v15.png` and `nagoji-v2.png`.

**What the prompt says about the sheets**
- The prompt text never mentions the attached images. It does not say which image is which character, that they are reference sheets, or anything about the sheets' backgrounds, layout, labels or multiple views.
- "background" appears once in CM (CM 132, "background Maratha riders"), which is unrelated, and nowhere in SP.
- The only sheet wording that reaches prompts is in the Nagoji rows: "Captivity sheet:" (CM 27-29), "Commander sheet:" (CM 33-35) and "Later-life sheet" (CM 44). Yet the same single `nagoji-v2.png` is attached in every chapter.
- CM 9 ("Attach the relevant sheet as a reference image to EVERY generation...") is preamble and is not injected.

## (5) How continuity rows are chosen per chapter (no page awareness)

**Nagoji: `_nagoji_look`, SP 220-229**
- Constant part: the text before the first `|` in the block, with heading lines dropped. That is CM 21-23, "Constant identity: ...".
- Rows are found with `re.findall(r"\|\s*(\d+)(?:-(\d+))?(?:\s+epilogue)?\s*\|\s*([^\n]+)", block)`. The first row whose range contains the chapter is returned as `constant + "; " + row`.
- If no row matches, it returns `constant + "; " + block` (the whole block, including the CM 46-48 note). Chapters 1 to 28 are all covered by rows, so this does not happen today.

**Everyone else: `_character_look`, SP 232-239**
- The first block whose name (a lowercased heading or bold bullet name, from `_continuity_blocks`, SP 195-209) contains any alias as a substring is used.
- `_look_for_chapter` (SP 253-264) keeps every line that is not a row, plus every `| chapters | look |` row (`_CHAPTER_ROW`, SP 242; `_chapters`, SP 245-250) whose chapter set includes this chapter.
- Matching rows are joined as `"\nThis chapter: " + "; ".join(looks)`. For example, Ibrahim in ch5 gets the 4-5 and 5 rows, which produces "no coat.; Ash".
- If no block matches: "No dedicated continuity block found. Use only the script description and standing rules."

**No page awareness**
- `assemble_prompt` passes only `chapter` to `_character_look` (SP 314). `panel['page']` and `panel['panel']` are never consulted.
- Page, panel or event qualifiers written inside rows therefore reach every panel of the chapter as prose:
  - Nagoji ch5 (CM 31): "Pages 1 and 2 ... From page 3".
  - Nagoji ch17 (CM 36): "Pages 1 to 8.3 ... From panel 8.4 ... Pages 11 to 13".
  - Nagoji ch20 (CM 38): "until he gives it to Dhanaji".
  - Nagoji ch22 (CM 40): "Uninjured until the temple fight; afterwards...".
  - Nagoji ch24 (CM 42): "Pages 1 to 13 ... From the issue of the coats (page 14)".
  - Nagoji ch28 (CM 44): epilogue, "pages 1 to 5", "From page 6".
  - Varma ch22 (CM 57): "Hill shrine ... Fort room after the attack".
  - Ibrahim ch5 (CM 75): "Ash on his forehead from panel 5.3".
  - De Lannoy ch15 (CM 80): "after he changes".
  - Revathi ch27 (CM 67) and Nagoji 25-27 (CM 43): "At Padmini's funeral".
- The generator can only work out the page from the `page-XX-panel-YY` id in the header.
- Observed conflict: ch05 `page-01-panel-01-gen-r1.txt` carries "Ash on his forehead from panel 5.3..." in the authoritative block, and its appended note has to say "forehead bare, no ash".

## (6) Existing tests that pin prompt content (T)

**`test_continuity_conflict_is_overridden_and_reference_is_attached` (T 77-95)**
- The prompt contains "clean-shaven chin" and "My name." and does not contain "short dark beard".
- It contains "for exactly 1 lettering area(s)" and does not contain "blank outlined".
- `refs[0]` ends with "nagoji-v2.png".

**`test_a_full_width_strip_panel_asks_for_a_strip_shaped_frame` (T 97-110)**
- "FRAME SHAPE: a wide horizontal strip, about 3 to 1 (width to height)" is present for "Full width, bottom strip..." and absent for "Insert, tight..." and "Wide, shot from a distance...".

**`test_prompt_asks_for_clear_space_and_no_painted_balloons` (T 112-139)** checks:
- "No text of any kind in generated art." and the exact `"CAPTION: The door.\nDUARTE: Come in."`.
- "Leave clear, low-detail space (sky, wall, floor or shadow) for exactly 2 lettering area(s)", "preferably in the upper part of the frame", "Draw NO balloons, boxes, frames", "text of any kind" and "replaces any earlier mention of blank balloon or caption reserves".
- The absence of "blank outlined", "Reserve exactly", "outlined text area" and any em or en dash.
- For the silent panel: "[no copy]", "No lettering areas are needed", "Draw NO balloons, boxes, frames", the "replaces" sentence, and no "Leave clear".
- Its comment at T 127 is stale. It says the CM standing rule still reads "blank balloon and caption reserves only", but CM 126 no longer says that.

**`test_existing_prepared_packages_are_not_rewritten_by_the_new_wording` (T 141-162)**
- The prepared prompt file contains "lettering area(s)".
- A changed file makes `prepare` raise `FileExistsError` and leaves the file unchanged.

**`test_nagoji_constant_identity_and_epilogue_row` (T 164-174)** (uses the real CM)
- `_nagoji_look(ch1)` contains "CLEAN-SHAVEN CHIN", "thick curled moustache", "small gold ear stud", "captivity sheet" (case-insensitive), "No facial scar", "No forehead marks" and "captivity only".
- `_nagoji_look(ch28)` contains "grey-streaked".

**`test_parenthetical_principal_labels_keep_dedicated_looks` (T 176-182)** (real CM)
- The ch24 looks contain "LEFT ear" (ibrahim), "betel-stained" (thoma), "chest-length beard" (avraham) and "sister" (nandini).
- temple_priest contains "Hindu ritual priest".

**`ChapterRowTests` (T 278-325)**
- Varma row selection: ch18 has the crest and "first grey" but not "bound right shoulder"; ch22 has the shoulder but not the crest; ch7 has none of them and no "|".
- Duarte without rows: exact equality with `"- **Father Duarte**: plain black cassock and small cross."`.
- New alias keys resolve to their own blocks.
- Horses are inferred from panel text, and a bare "envoy" does not cast `dutch_envoys`.

**Reference and job tests**
- `test_temple_priest_is_only_an_explicit_cast_key...` (T 184-188).
- `ApprovedSheetTests` (T 328-362): only V13 sheets attach without approvals; an approved sheet attaches; a changed sheet is refused; nagoji and varma keep their V13 sheets.
- `test_reference_hashes_and_lock_are_in_jobs` (T 190-205).
- `test_prepare_snapshots...` (T 226-245): `image_gen.tool == "image_gen__imagegen"` and the reference ends with "nagoji-v2.png".

**What no test pins**
- The section order, and the headings "AUTHORITATIVE CONTINUITY..." and "STANDING CONTINUITY RULES:".
- Standing-rules content in a prompt. The fixture's standing rules are only "No text of any kind in the art." and "No nooses.".
- The "SCRIPT DIRECTIONS" prompt line (directions are tested only in the parser, T 215-224 and 405-415) and the closing "No invented lettering..." line.
- Any chapter scoping of the Portuguese, Goa or European rules.
- Page-level row selection.
- Any wording about the reference sheets.

