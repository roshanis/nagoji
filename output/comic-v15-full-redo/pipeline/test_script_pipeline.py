import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import script_pipeline as p


CONTINUITY = """# continuity

## Nagoji Sawant / Ananthan Pillai
| Chapters | Look |
| --- | --- |
| 1-3 | clean-shaven chin, curled moustache, captivity rags |

## Other principals

- **Marthanda Varma**: V13 face, cream and gold.
- **Father Duarte**: plain black cassock and small cross.

## Standing rules for generated art
- No text of any kind in the art.
- No nooses.
"""


class ScriptPipelineTests(unittest.TestCase):
    def test_prefers_chapter_title_and_collects_multiline_description(self):
        raw = """# Book title
## Chapter 7: The Test
## PAGE 1
**1.1** First description.
Continuation of the same shot.
> CAPTION: Exact copy.
### What changed
## PAGE 2
**2.1** Second shot.
> CAPTION: End.
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "script.md"
            path.write_text(raw, encoding="utf-8")
            parsed = p.parse_script(path)
            self.assertEqual(parsed["title"], "Chapter 7: The Test")
            self.assertIn("Continuation of the same shot.", parsed["pages"]["1"]["panels"][0]["description"])

    def test_parse_arbitrary_pages_and_unknown_speaker_without_losing_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "CHAPTER-07-SCRIPT.md"
            path.write_text("""# Test chapter
## PAGE 1
**1.1** A named scene.
> GUARD CAPTAIN: Exact: punctuation stays.
> CAPTION: A second line.
## PAGE 2
**2.1** Another scene.
> NAGOJI: I remain.
""", encoding="utf-8")
            parsed = p.parse_script(path)
            self.assertEqual(parsed["page_count"], 2)
            self.assertEqual(parsed["panel_count"], 2)
            self.assertEqual(parsed["pages"]["1"]["panels"][0]["copy"][0]["text"], "Exact: punctuation stays.")
            self.assertEqual(parsed["pages"]["2"]["panels"][0]["id"], "page-02-panel-01")

    def test_rejects_dash_and_unparsed_quoted_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.md"
            path.write_text("## PAGE 1\n**1.1** Scene\n> CAPTION: bad " + chr(0x2014) + " dash\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                p.parse_script(path)
            path.write_text("## PAGE 1\n**1.1** Scene\n> This has no speaker\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                p.parse_script(path)

    def test_continuity_conflict_is_overridden_and_reference_is_attached(self):
        with tempfile.TemporaryDirectory() as tmp:
            continuity_path = Path(tmp) / "CONTINUITY.md"
            continuity_path.write_text(CONTINUITY, encoding="utf-8")
            continuity = p.load_continuity(continuity_path)
            panel = {"id": "page-01-panel-01", "description": "Nagoji with his horse.",
                     "copy": [{"speaker": "CAPTION", "text": "My name."}]}
            cast = p.infer_cast(panel, 1)
            self.assertIn("nagoji", cast)
            prompt = p.assemble_prompt(panel, 1, continuity, cast)
            self.assertIn("clean-shaven chin", prompt)
            self.assertNotIn("short dark beard", prompt)
            refs = p._references(cast, panel["description"])
            self.assertTrue(refs[0].endswith("nagoji-v2.png"))
            self.assertIn("My name.", prompt)
            # Deliberately changed from "Reserve exactly 1 blank outlined text area(s)": the compositor now
            # draws balloons and captions, so the generator is told to leave space and paint nothing.
            self.assertIn("for exactly 1 lettering area(s)", prompt)
            self.assertNotIn("blank outlined", prompt)

    def test_a_full_width_strip_panel_asks_for_a_strip_shaped_frame(self):
        # The generator picks the frame's shape from the prompt; without a word on it every frame came back 3:2,
        # and a full-width strip then had to be cropped hard or shown with bars.
        with tempfile.TemporaryDirectory() as tmp:
            continuity_path = Path(tmp) / "CONTINUITY.md"
            continuity_path.write_text(CONTINUITY, encoding="utf-8")
            continuity = p.load_continuity(continuity_path)
            strip = {"id": "page-01-panel-01", "description": "Full width, bottom strip. The tide line at dusk.", "copy": []}
            prompt = p.assemble_prompt(strip, 1, continuity, ["nagoji"])
            self.assertIn("FRAME SHAPE: a wide horizontal strip, about 3 to 1 (width to height)", prompt)
            for description in ("Insert, tight. His hands on the musket.", "Wide, shot from a distance. The hold."):
                with self.subTest(description=description):
                    panel = {"id": "page-01-panel-02", "description": description, "copy": []}
                    self.assertNotIn("FRAME SHAPE", p.assemble_prompt(panel, 1, continuity, ["nagoji"]))

    def test_prompt_asks_for_clear_space_and_no_painted_balloons(self):
        with tempfile.TemporaryDirectory() as tmp:
            continuity_path = Path(tmp) / "CONTINUITY.md"
            continuity_path.write_text(CONTINUITY, encoding="utf-8")
            continuity = p.load_continuity(continuity_path)
            panel = {"id": "page-01-panel-02", "description": "Nagoji and Duarte at the door.",
                     "copy": [{"speaker": "CAPTION", "text": "The door."},
                              {"speaker": "DUARTE", "text": "Come in."}]}
            prompt = p.assemble_prompt(panel, 1, continuity, ["nagoji"])
            self.assertIn("No text of any kind in generated art.", prompt)
            self.assertIn("CAPTION: The door.\nDUARTE: Come in.", prompt)
            self.assertIn("Leave clear, low-detail space (sky, wall, floor or shadow) for exactly 2 lettering area(s)", prompt)
            self.assertIn("preferably in the upper part of the frame", prompt)
            self.assertIn("Draw NO balloons, boxes, frames", prompt)
            self.assertIn("text of any kind", prompt)
            # CONTINUITY.md's standing rule still says "blank balloon and caption reserves only"; this wins.
            self.assertIn("replaces any earlier mention of blank balloon or caption reserves", prompt)
            for gone in ("blank outlined", "Reserve exactly", "outlined text area"):
                self.assertNotIn(gone, prompt)
            self.assertNotIn(chr(0x2014), prompt)
            self.assertNotIn(chr(0x2013), prompt)
            silent = p.assemble_prompt({"id": "page-01-panel-03", "description": "The empty door.", "copy": []},
                                       1, continuity, [])
            self.assertIn("[no copy]", silent)
            self.assertIn("No lettering areas are needed", silent)
            self.assertIn("Draw NO balloons, boxes, frames", silent)
            self.assertIn("replaces any earlier mention of blank balloon or caption reserves", silent)
            self.assertNotIn("Leave clear", silent)

    def test_existing_prepared_packages_are_not_rewritten_by_the_new_wording(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "CHAPTER-02-SCRIPT.md").write_text(
                "# Chapter\n## PAGE 1\n**1.1** Nagoji waits.\n> CAPTION: My watch.\n", encoding="utf-8")
            continuity_path = root / "CONTINUITY.md"
            continuity_path.write_text(CONTINUITY, encoding="utf-8")
            out, cast = root / "out", root / "CAST.json"
            cast.write_text(json.dumps({"page-01-panel-01": ["nagoji"]}), encoding="utf-8")
            p.prepare(2, out, scripts_dir=scripts, continuity_path=continuity_path, cast_overrides_path=cast)
            prompt = out / "prompts" / "page-01-panel-01.txt"
            self.assertIn("lettering area(s)", prompt.read_text(encoding="utf-8"))
            # A package prepared before the change holds the old wording; preparing again must refuse, not rewrite.
            old = prompt.read_text(encoding="utf-8").replace(
                "Leave clear, low-detail space (sky, wall, floor or shadow) for exactly 1 lettering area(s)",
                "Reserve exactly 1 blank outlined text area(s)")
            prompt.write_text(old, encoding="utf-8")
            with self.assertRaises(FileExistsError):
                p.prepare(2, out, scripts_dir=scripts, continuity_path=continuity_path, cast_overrides_path=cast)
            self.assertEqual(prompt.read_text(encoding="utf-8"), old)

    def test_nagoji_constant_identity_and_epilogue_row(self):
        continuity = p.load_continuity(Path(__file__).resolve().parents[3] / "output/comic-v15-full-redo/CONTINUITY.md")
        look = p._nagoji_look(continuity, 1)
        self.assertIn("CLEAN-SHAVEN CHIN", look)
        self.assertIn("thick curled moustache", look)
        self.assertIn("small gold ear stud", look)
        self.assertIn("captivity sheet", look.lower())
        self.assertIn("No facial scar", look)
        self.assertIn("No forehead marks", look)
        self.assertIn("captivity only", look)
        self.assertIn("grey-streaked", p._nagoji_look(continuity, 28))

    def test_parenthetical_principal_labels_keep_dedicated_looks(self):
        continuity = p.load_continuity()
        for key, detail in [('ibrahim', 'LEFT ear'), ('thoma', 'betel-stained'),
                            ('avraham', 'chest-length beard'), ('nandini', 'sister')]:
            with self.subTest(character=key):
                self.assertIn(detail, p._character_look(continuity, key, 24))
        self.assertIn('Hindu ritual priest', p._character_look(continuity, 'temple_priest', 24))

    def test_temple_priest_is_only_an_explicit_cast_key_and_empty_override_wins(self):
        self.assertFalse(any(r.endswith("temple-priest-v1.png") for r in p._references(["duarte"], "temple priest")))
        self.assertTrue(p._references(["temple_priest"])[0].endswith("temple-priest-v1.png"))
        panel = {"id": "page-01-panel-01", "description": "Nagoji", "copy": []}
        self.assertEqual(p.infer_cast(panel, 1, {panel["id"]: []}), [])

    def test_reference_hashes_and_lock_are_in_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "CHAPTER-02-SCRIPT.md").write_text(
                "# Chapter\n## Chapter 2: Test\n## PAGE 1\n**1.1** Nagoji waits.\n> CAPTION: My watch.\n", encoding="utf-8")
            continuity_path = root / "CONTINUITY.md"
            continuity_path.write_text(CONTINUITY, encoding="utf-8")
            out = root / "out"
            cast = root / "CAST.json"
            cast.write_text(json.dumps({"page-01-panel-01": ["nagoji"]}), encoding="utf-8")
            p.prepare(2, out, scripts_dir=scripts, continuity_path=continuity_path, cast_overrides_path=cast)
            job = json.loads((out / "IMAGEGEN-JOBS.json").read_text(encoding="utf-8"))["jobs"][0]
            self.assertIn("reference_image_sha256", job)
            self.assertIn("v13_lock_sha256", job["continuity_authority"])

    def test_malformed_quote_and_post_copy_prose_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'bad.md'
            for tail in ['>CAPTION: Missing separator', '> CAPTION: Exact.\nUnattached prose.']:
                path.write_text('## PAGE 1\n**1.1** Description.\n' + tail + '\n')
                with self.assertRaises(ValueError):
                    p.parse_script(path)

    def test_wordless_directions_and_interleaved_lettering_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'directions.md'
            path.write_text('## PAGE 1\n**1.1** Silent shot.\n> *No text. Let the buttons shine.*\n'
                            '**1.2** A voice.\n> CHAVER: Fragment.\n'
                            '*(Letter as one balloon.)*\n> CAPTION: Exact caption.\n')
            panels=p.parse_script(path)['pages']['1']['panels']
            self.assertEqual(panels[0]['copy'],[])
            self.assertIn('Let the buttons shine.',panels[0]['directions'][0])
            self.assertEqual(len(panels[1]['copy']),2)

    def test_prepare_snapshots_and_refuses_conflicting_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "CHAPTER-02-SCRIPT.md").write_text(
                "# Chapter\n## PAGE 1\n**1.1** Nagoji waits.\n> CAPTION: My watch.\n", encoding="utf-8")
            continuity_path = root / "CONTINUITY.md"
            continuity_path.write_text(CONTINUITY, encoding="utf-8")
            out = root / "out"
            cast = root / "CAST.json"
            cast.write_text(json.dumps({"page-01-panel-01": ["nagoji"]}), encoding="utf-8")
            result = p.prepare(2, out, scripts_dir=scripts, continuity_path=continuity_path, cast_overrides_path=cast)
            self.assertEqual(result["job_count"], 1)
            payload = json.loads((out / "IMAGEGEN-JOBS.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["jobs"][0]["image_gen"]["tool"], "image_gen__imagegen")
            self.assertTrue(payload["jobs"][0]["reference_images"][0].endswith("nagoji-v2.png"))
            (out / "SCRIPT-SNAPSHOT.json").write_text("conflict", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                p.prepare(2, out, scripts_dir=scripts, continuity_path=continuity_path, cast_overrides_path=cast)


ROWS_CONTINUITY = """# continuity

## Other principals

- **Marthanda Varma**: V13 face, refined features.
  | 6, 14, 18-19 | formal court: cream-and-gold turban with a jewelled peacock crest |
  | 22 | bound right shoulder |
  | 15-28 | first grey at the temples |
- **Father Duarte**: plain black cassock and small cross.
- **Gustaaf Willem van Imhoff**: heavy-set Dutch governor, powdered wig.
- **Dutch envoys**: dark brown and charcoal coats.
- **Yusuf Marakkar**: tall and lean, white skullcap.
- **Nagoji's father** (ch19): white-haired, bent.
- **Nagoji's mother** (ch19): white-haired, nine-yard sari.
- **Bhalerao** (ch19): thin young moustache.
- **The Gujarati sowcar** (ch19): small red pagdi.
- **Joseph Donnadi** (ch15): blue officer's coat.
- **The Madurai troop**: white jama tunics.
- **The Kollamkara Raja**: heavy, sharp-eyed.
- **Chanda Sahib**: never shown face-on.

## Horses

- **Kanka**: Nagoji's black mare.
- **Kayal**: Nagoji's bay mare.
- **Nagoji's grey gelding**: plain grey daytime mount.
- **Megha**: grey horse with a black mane.
"""


class ChapterRowTests(unittest.TestCase):
    """A character's bible entry is pasted into every prompt that shows them, so
    chapter-specific looks (injuries, costume changes) must reach only their chapters."""

    def setUp(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "CONTINUITY.md"
            path.write_text(ROWS_CONTINUITY, encoding="utf-8")
            self.c = p.load_continuity(path)

    def test_character_rows_select_only_the_current_chapter(self):
        ch18 = p._character_look(self.c, "varma", 18)
        self.assertIn("V13 face", ch18)
        self.assertIn("jewelled peacock crest", ch18)
        self.assertIn("first grey", ch18)
        self.assertNotIn("bound right shoulder", ch18)
        ch22 = p._character_look(self.c, "varma", 22)
        self.assertIn("bound right shoulder", ch22)
        self.assertNotIn("peacock crest", ch22)
        ch7 = p._character_look(self.c, "varma", 7)
        self.assertIn("V13 face", ch7)
        for absent in ("peacock crest", "bound right shoulder", "first grey", "|"):
            self.assertNotIn(absent, ch7)

    def test_entry_without_rows_is_returned_whole(self):
        self.assertEqual(p._character_look(self.c, "duarte", 2),
                         "- **Father Duarte**: plain black cassock and small cross.")

    def test_new_entries_resolve_to_their_own_block(self):
        expected = {"van_imhoff": "van Imhoff", "dutch_envoys": "Dutch envoys", "yusuf": "Yusuf",
                    "nagoji_father": "father", "nagoji_mother": "mother", "bhalerao": "Bhalerao",
                    "sowcar": "sowcar", "donnadi": "Donnadi", "madurai_troop": "Madurai troop",
                    "kollamkara": "Kollamkara", "chanda_sahib": "Chanda Sahib", "kanka": "Kanka",
                    "kayal": "Kayal", "grey_gelding": "grey gelding", "megha": "Megha"}
        for key, name in expected.items():
            with self.subTest(key=key):
                self.assertIn(key, p.CHARACTER_ALIASES)
                look = p._character_look(self.c, key, 19)
                self.assertTrue(look.startswith("- **") and name in look.split(":", 1)[0], look)

    def test_horses_are_inferred_from_panel_text(self):
        panel = {"id": "page-01-panel-01", "description": "Nagoji rides Kayal past Megha's grave.", "copy": []}
        self.assertEqual(p.infer_cast(panel, 16), ["kayal", "megha", "nagoji"])

    def test_bare_envoy_in_dialogue_does_not_cast_the_dutch_envoys(self):
        panel = {"id": "page-01-panel-01", "description": "Varma at the window.",
                 "copy": [{"text": "The Nizam sent an envoy last month."}]}
        self.assertNotIn("dutch_envoys", p.infer_cast(panel, 28))


class ApprovedSheetTests(unittest.TestCase):
    """Only sheets the author approved, at the exact bytes approved, are attached."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.saved = p.APPROVED_SHEETS
        p.APPROVED_SHEETS = self.dir / "APPROVED-SHEETS.json"
        (self.dir / "10-father-duarte-v15.png").write_bytes(b"duarte sheet")

    def tearDown(self):
        p.APPROVED_SHEETS = self.saved
        self.tmp.cleanup()

    def approve(self, digest):
        p.APPROVED_SHEETS.write_text(json.dumps({"duarte": {"file": "10-father-duarte-v15.png", "sha256": digest}}))

    def test_without_approvals_only_the_v13_sheets_attach(self):
        self.assertEqual(p._references(["duarte"]), [])
        self.assertTrue(p._references(["nagoji"])[0].endswith("nagoji-v2.png"))

    def test_approved_sheet_attaches_for_its_character(self):
        self.approve(p.sha256(self.dir / "10-father-duarte-v15.png"))
        self.assertEqual(p._references(["duarte", "joao"]), [str((self.dir / "10-father-duarte-v15.png").resolve())])

    def test_changed_sheet_is_refused(self):
        self.approve("0" * 64)
        with self.assertRaises(ValueError):
            p._references(["duarte"])

    def test_nagoji_and_varma_keep_their_v13_sheets(self):
        p.APPROVED_SHEETS.write_text(json.dumps({"nagoji": {"file": "10-father-duarte-v15.png",
                                                            "sha256": p.sha256(self.dir / "10-father-duarte-v15.png")}}))
        with self.assertRaises(ValueError):
            p._references(["nagoji"])


class CastOverrideValidationTests(unittest.TestCase):
    """Chapters after the pilot are prepared only from a complete, well-formed cast file,
    because a missing panel silently falls back to name inference."""

    SCRIPT = "# Chapter\n## Chapter 2: Test\n## PAGE 1\n**1.1** Nagoji waits.\n> CAPTION: My watch.\n\n**1.2** The empty road.\n\n> *No text.*\n"

    def run_prepare(self, cast):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "CHAPTER-02-SCRIPT.md").write_text(self.SCRIPT, encoding="utf-8")
            (root / "CONTINUITY.md").write_text(CONTINUITY, encoding="utf-8")
            path = None
            if cast is not None:
                path = root / "CAST.json"
                path.write_text(json.dumps(cast), encoding="utf-8")
            return p.prepare(2, root / "out", scripts_dir=root / "scripts",
                             continuity_path=root / "CONTINUITY.md", cast_overrides_path=path)

    def test_complete_file_prepares(self):
        self.assertEqual(self.run_prepare({"page-01-panel-01": ["nagoji"], "page-01-panel-02": []})["job_count"], 2)

    def test_chapter_after_the_pilot_needs_a_cast_file(self):
        with self.assertRaises(ValueError):
            self.run_prepare(None)

    def test_missing_panel_fails(self):
        with self.assertRaises(ValueError):
            self.run_prepare({"page-01-panel-01": ["nagoji"]})

    def test_unknown_character_key_fails(self):
        with self.assertRaises(ValueError):
            self.run_prepare({"page-01-panel-01": ["nagoj"], "page-01-panel-02": []})

    def test_unknown_panel_id_fails(self):
        with self.assertRaises(ValueError):
            self.run_prepare({"page-01-panel-01": [], "page-01-panel-02": [], "page-02-panel-01": []})



class LetteringMarkupParserTests(unittest.TestCase):
    def test_no_text_direction_is_not_lettering_and_italic_source_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'script.md'
            path.write_text('# Test\n## PAGE 1\n**1.1** A quiet scene.\n'
                            '> *No text.*\n**1.2** A voice.\n'
                            '> NAGOJI: Easy, *bhau*.\n', encoding='utf-8')
            panels = p.parse_script(path)['pages']['1']['panels']
            self.assertEqual(panels[0]['copy'], [])
            self.assertEqual(panels[0]['directions'], ['No text.'])
            self.assertEqual(panels[1]['copy'][0]['text'], 'Easy, *bhau*.')

class PrepareSnapshotsBibleTests(unittest.TestCase):
    def test_prepare_writes_a_bible_snapshot_matching_the_recorded_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts" / "CHAPTER-02-SCRIPT.md").write_text(
                "# Chapter\n## Chapter 2: Test\n## PAGE 1\n**1.1** Nagoji waits.\n> CAPTION: My watch.\n", encoding="utf-8")
            (root / "CONTINUITY.md").write_text(CONTINUITY, encoding="utf-8")
            cast = root / "CAST.json"
            cast.write_text(json.dumps({"page-01-panel-01": ["nagoji"]}), encoding="utf-8")
            p.prepare(2, root / "out", scripts_dir=root / "scripts", continuity_path=root / "CONTINUITY.md",
                      cast_overrides_path=cast)
            job = json.loads((root / "out" / "IMAGEGEN-JOBS.json").read_text(encoding="utf-8"))
            snapshot = root / "out" / "CONTINUITY-SNAPSHOT.md"
            self.assertTrue(snapshot.is_file())
            self.assertEqual(p.sha256(snapshot), job["continuity"]["sha256"])


if __name__ == "__main__":
    unittest.main()
