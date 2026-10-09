import json
import sys
import tempfile
import unittest
import copy
import contextlib
import io
import difflib
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import script_pipeline as p

REAL_CONCEPT_SHEETS = p._concept_sheets


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


class SheetFixtureCase(unittest.TestCase):
    """Parser and package unit tests use local sheet bytes, not production art."""
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        sheets = {}
        for key, name in p.CONCEPTS.items():
            sheets[key] = root / name
            sheets[key].write_bytes((key + ' fixture').encode())
        lock = root / 'lock.json'
        lock.write_text('{}')
        for mock in (patch.object(p, '_concept_sheets', return_value=sheets), patch.object(p, 'LOCK_PATH', lock)):
            mock.start()
            self.addCleanup(mock.stop)


class ScriptPipelineTests(SheetFixtureCase):
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
            # The legacy replacement wording remains frozen for existing v1 packages.
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
        self.assertIn("THICK, bushy curled handlebar moustache", look)
        self.assertIn("one tiny flat gold stud flush on the earlobe", look)
        self.assertIn("no pearls", look)
        self.assertIn("captivity sheet", look.lower())
        self.assertIn("No facial scar", look)
        self.assertIn("No forehead marks", look)
        self.assertIn("captivity only", look)
        self.assertIn("grey-streaked", p._nagoji_look(continuity, 28))

    def test_varma_markers_keep_him_apart_from_nagoji(self):
        """Author approved 2026-10-08: review-sheets/SHEETS-AND-FIXES-PROPOSAL-2026-10-08.html."""
        continuity = p.load_continuity()
        look = p._character_look(continuity, "varma", 12)
        for marker in ("THIN, neatly waxed moustache", "never grey before the ch28 dedication", "Vaishnavite namam",
                       "pearl drop hanging from each earlobe", "knot on the left side of his head"):
            self.assertIn(marker, look)
        self.assertNotIn("bushy", look)

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


class SpannedSheetTests(unittest.TestCase):
    """A sheet approved for part of the story replaces the V13 sheet only inside its spans."""
    FILES = {"nagoji_commander": ("21-nagoji-commander-v15.png", "nagoji", [["5.3", "17.10"]]),
             "nagoji_ananthan_pillai": ("22-nagoji-ananthan-pillai-v15.png", "nagoji",
                                        [["17.11", "28.12"], ["28.13.2", "28.99"]]),
             "varma_v15": ("23-marthanda-varma-v15.png", "varma", [["1.1", "27.99"]])}

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.entries = {}
        for key, (filename, character, spans) in self.FILES.items():
            (self.dir / filename).write_bytes(key.encode())
            self.entries[key] = {"file": filename, "sha256": p.sha256(self.dir / filename),
                                 "character": character, "spans": spans}
        patcher = patch.object(p, "APPROVED_SHEETS", self.dir / "APPROVED-SHEETS.json")
        patcher.start()
        self.addCleanup(patcher.stop)
        self.write()

    def write(self):
        p.APPROVED_SHEETS.write_text(json.dumps(self.entries))

    def name(self, character, chapter, page, panel):
        return p._concept_sheets(chapter, page, panel)[character].name

    def test_commander_sheet_covers_chapter_5_page_3_to_chapter_17_page_10(self):
        for position in ((5, 3, 1), (5, 3, 6), (9, 4, 2), (17, 10, 1), (17, 10, 9)):
            with self.subTest(position=position):
                self.assertEqual(self.name("nagoji", *position), "21-nagoji-commander-v15.png")
        for position in ((1, 1, 1), (4, 12, 3), (5, 2, 1), (5, 2, 9)):
            with self.subTest(position=position):
                self.assertEqual(self.name("nagoji", *position), "nagoji-v2.png")

    def test_ananthan_pillai_sheet_skips_only_chapter_28_page_13_panel_1(self):
        for position in ((17, 11, 1), (20, 3, 2), (28, 12, 9), (28, 13, 2), (28, 13, 3), (28, 14, 1)):
            with self.subTest(position=position):
                self.assertEqual(self.name("nagoji", *position), "22-nagoji-ananthan-pillai-v15.png")
        self.assertEqual(self.name("nagoji", 28, 13, 1), "nagoji-v2.png")

    def test_varma_sheet_covers_chapters_1_to_27_and_chapter_28_keeps_v13(self):
        for position in ((1, 1, 1), (14, 6, 2), (27, 15, 3)):
            with self.subTest(position=position):
                self.assertEqual(self.name("varma", *position), "23-marthanda-varma-v15.png")
        for position in ((28, 1, 1), (28, 13, 2)):
            with self.subTest(position=position):
                self.assertEqual(self.name("varma", *position), "varma-v1.png")

    def test_other_characters_are_unaffected_by_spans(self):
        self.assertEqual(self.name("temple_priest", 17, 10, 1), "temple-priest-v1.png")
        self.assertNotIn("nagoji_commander", p._concept_sheets(17, 10, 1))

    def test_without_a_position_spanned_sheets_are_ignored(self):
        sheets = p._concept_sheets()
        self.assertEqual((sheets["nagoji"].name, sheets["varma"].name), ("nagoji-v2.png", "varma-v1.png"))
        self.assertEqual([Path(x).name for x in p._references(["nagoji", "varma"])], ["nagoji-v2.png", "varma-v1.png"])
        for partial in ({"chapter": 5}, {"chapter": 5, "page": 3}, {"page": 3, "panel": 1}):
            with self.subTest(partial=partial), self.assertRaises(ValueError):
                p._concept_sheets(**partial)

    def test_references_follow_the_panel_position(self):
        names = lambda *position: [Path(x).name for x in p._references(["nagoji", "varma", "kayal"], "", *position)]
        self.assertEqual(names(5, 3, 1), ["21-nagoji-commander-v15.png", "23-marthanda-varma-v15.png"])
        self.assertEqual(names(17, 11, 1), ["22-nagoji-ananthan-pillai-v15.png", "23-marthanda-varma-v15.png"])
        self.assertEqual(names(28, 13, 1), ["nagoji-v2.png", "varma-v1.png"])
        self.assertEqual([Path(x).name for x in p._references(["nagoji"], chapter=5, page=3, panel=1)],
                         ["21-nagoji-commander-v15.png"])

    def test_entry_without_character_serves_its_own_key(self):
        self.entries = {"varma": {key: value for key, value in self.entries["varma_v15"].items() if key != "character"}}
        self.entries["varma"]["spans"] = [["2.1", "2.9"]]
        self.write()
        self.assertEqual(self.name("varma", 2, 5, 1), "23-marthanda-varma-v15.png")
        self.assertEqual(self.name("varma", 3, 1, 1), "varma-v1.png")

    def test_overlapping_spans_for_one_character_name_both_entries(self):
        for end, start in (("17.11", "17.11"), ("17.10.3", "17.10.3"), ("20.1", "17.11")):
            self.entries["nagoji_commander"]["spans"] = [["5.3", end]]
            self.entries["nagoji_ananthan_pillai"]["spans"] = [[start, "28.12"]]
            self.write()
            with self.subTest(end=end, start=start), self.assertRaisesRegex(ValueError, "nagoji_commander.*nagoji_ananthan_pillai"):
                p._concept_sheets()

    def test_adjacent_spans_and_other_characters_do_not_overlap(self):
        self.entries["nagoji_commander"]["spans"] = [["5.3", "17.10.2"]]
        self.entries["nagoji_ananthan_pillai"]["spans"] = [["17.10.3", "28.12"]]
        self.write()
        self.assertEqual(self.name("nagoji", 17, 10, 2), "21-nagoji-commander-v15.png")
        self.assertEqual(self.name("nagoji", 17, 10, 3), "22-nagoji-ananthan-pillai-v15.png")

    def test_a_v13_character_without_spans_keeps_its_v13_sheet(self):
        del self.entries["nagoji_commander"]["spans"]
        self.write()
        with self.assertRaisesRegex(ValueError, "keeps its V13 sheet"):
            p._concept_sheets()
        self.entries["nagoji_commander"]["spans"] = []
        self.write()
        with self.assertRaisesRegex(ValueError, "keeps its V13 sheet"):
            p._concept_sheets()

    def test_every_approved_file_is_hashed_even_outside_its_span(self):
        self.entries["varma_v15"]["sha256"] = "0" * 64
        self.write()
        for args in ((), (28, 13, 1), (5, 3, 1)):
            with self.subTest(args=args), self.assertRaisesRegex(ValueError, "changed since approval"):
                p._concept_sheets(*args)

    def test_malformed_spans_are_refused(self):
        for spans in ("5.3-17.10", [["5.3"]], [["x", "1.1"]], [["5", "6"]], [["17.10", "5.3"]], [["5.3", "17.10", "18.1"]], [[5, 6]]):
            self.entries["nagoji_commander"]["spans"] = spans
            self.write()
            with self.subTest(spans=spans), self.assertRaisesRegex(ValueError, "nagoji_commander"):
                p._concept_sheets()


class CastOverrideValidationTests(SheetFixtureCase):
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

class PrepareSnapshotsBibleTests(SheetFixtureCase):
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


V2_CONTINUITY = """# Fixture continuity
## Nagoji Sawant / Ananthan Pillai
Constant identity: CLEAN-SHAVEN CHIN (light stubble at most, captivity only); thick curled moustache; small gold ear stud.
| Chapters | Look |
| --- | --- |
| 1 | Captivity sheet: cream dhoti. |
| 9 @1-2.3 | Commander sheet: cream tunic, sleeves down, boots. |
| 9 @2.4- | Commander sheet: cream tunic, sleeves down, barefoot. |
| 10-15 | Commander sheet: boots, Portuguese brand. |
## Other principals
- **Padmini Amma**: in her fifties; thick black hair coiled at the nape. Dies ch27.
- **Revathi Bayi**: indigo sari with gold.
- **Ibrahim Marakkar** ("kapitan"): white turban, pale scar from the LEFT ear to the jaw.
  | 6-28 | Short coat. |
- **Marthanda Varma**: refined features.
  | 22 @1-6 | Hill shrine. |
  | 22 @7- | Fort room. |
- **Father Duarte**: Portuguese Jesuit.
- **Ramayyan Dalawa**: white cloth.
## Horses
- **Kayal**: bay mare. Colachel in ch14.
## Scoped art rules (prompt profile v2)
- [all] No blood or gore.
- [kerala, court] Lamps are clay or brass oil lamps.
- [portuguese] Ropes hang from an iron ring, never nooses.
- [dutch] Dutch blue coats.
## Standing rules for generated art
- Period: 1738 Portuguese Goa. Print: upscale.
"""


def v2_direction():
    return {"prompt_profile": "v2", "chapter": 9, "status": "approved",
            "settings": {
                "verandah": {"label": "Velinadu verandah", "scopes": ["kerala"],
                             "anchor": "Timber verandah beside the courtyard.",
                             "absent": "No masonry towers.", "time": "morning light"},
                "cellar": {"label": "Cellar", "scopes": ["portuguese"],
                           "anchor": "Stone cellar.", "absent": "No windows."}},
            "pages": {str(n): "verandah" for n in range(1, 12)},
            "panels": {"page-02-panel-04": {"time": "night, oil lamps"}},
            "character_notes": {"padmini": "Her hair is BLACK with no grey."}, "not_shown": {}}


PRE_SHEETS_BIBLE = Path(__file__).resolve().parent / "review" / "CONTINUITY-pre-sheets-2026-10-08.md"


class V1FreezeTests(unittest.TestCase):
    def check_freeze(self, live=False, packages=((5, 40), (6, 49), (7, 56), (8, 57)), total=202):
        chapters = p.V15 / "chapters"
        if not chapters.exists():
            self.skipTest("No prepared chapters tree")
        count = 0
        for chapter, expected in packages:
            out = chapters / f"ch{chapter:02d}"
            for name in ("IMAGEGEN-JOBS.json", "CONTINUITY-SNAPSHOT.md", "SCRIPT-SNAPSHOT.json"):
                self.assertTrue((out / name).is_file(), f"Incomplete frozen package: {out / name}")
            job = json.loads((out / "IMAGEGEN-JOBS.json").read_text())
            source = json.loads((out / "SCRIPT-SNAPSHOT.json").read_text())["source"]
            panels = {x["id"]: x for page in source["pages"].values() for x in page["panels"]}
            self.assertEqual(len(job["jobs"]), expected)
            self.assertEqual(set(panels), {x["id"] for x in job["jobs"]})
            bible = p.load_continuity(PRE_SHEETS_BIBLE if live else out / "CONTINUITY-SNAPSHOT.md")
            for item in job["jobs"]:
                with self.subTest(chapter=chapter, panel=item["id"]):
                    # Resolve within this worktree, never against the recorded original checkout.
                    prompt = out / "prompts" / f"{item['id']}.txt"
                    self.assertTrue(prompt.is_file(), f"Incomplete frozen package: {prompt}")
                    self.assertEqual((p.assemble_prompt(panels[item["id"]], chapter, bible, item["cast"]) + "\n").encode('utf-8'),
                                     prompt.read_bytes())
                    self.assertEqual(p.sha256(prompt), item["prompt_sha256"])
                count += 1
        self.assertEqual(count, total)

    def test_v1_prompts_of_prepared_chapters_5_to_8_are_byte_identical(self):
        self.check_freeze()

    def test_v1_prompts_against_live_bible_are_byte_identical(self):
        """Chapter 8 is pinned to its own snapshot (the approved v2 Padmini line changes 29 of its v1 prompts), chapter 7 too (the
        approved Kayal line adds her ch9 to ch12 service and changes 13 of its v1 prompts), and chapters 5 and 6 to the bible archived
        just before the approved 2026-10-08 Nagoji and Varma lines, which change their v1 prompts."""
        self.check_freeze(live=True, packages=((5, 40), (6, 49)), total=89)

    def test_v1_freeze_fails_for_incomplete_existing_packages(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(p, "V15", Path(tmp)):
            (Path(tmp) / "chapters").mkdir()
            with self.assertRaisesRegex(AssertionError, "Incomplete frozen package"):
                self.check_freeze()


class PromptV2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bible = self.root / "bible.md"
        self.bible.write_text(V2_CONTINUITY)
        self.continuity = p.load_continuity(self.bible)
        self.direction = v2_direction()
        self.direction_path = self.root / "direction.json"
        self.scripts = self.root / "scripts"
        self.scripts.mkdir()
        self.script_path = self.scripts / "CHAPTER-09-SCRIPT.md"
        self.script_path.write_text("# Test\n" + "".join(
            f"## PAGE {page}\n" + "".join(f"**{page}.{panel}** Nagoji waits.\n> CAPTION: A private thought.\n"
                                         for panel in range(1, 6)) for page in range(1, 12)))
        self.script = p.parse_script(self.script_path)
        self.cast_path = self.root / "cast.json"
        self.cast_path.write_text(json.dumps({x['id']: ['nagoji'] for page in self.script['pages'].values()
                                             for x in page['panels']}))
        self.lock = self.root / "lock.json"
        self.lock.write_text('{}')
        lock_patch = patch.object(p, "LOCK_PATH", self.lock)
        lock_patch.start(); self.addCleanup(lock_patch.stop)
        baseline_patch = patch.object(p, 'CONTINUITY', self.bible)
        baseline_patch.start(); self.addCleanup(baseline_patch.stop)
        self.sheets = {}
        for key, filename in (("nagoji", "nagoji-v2.png"), ("padmini", "padmini.png"), ("ibrahim", "ibrahim.png")):
            self.sheets[key] = self.root / filename
            self.sheets[key].write_bytes((key + ' fixture sheet').encode())
        sheet_patch = patch.object(p, "_concept_sheets", return_value=self.sheets)
        sheet_patch.start(); self.addCleanup(sheet_patch.stop)

    def panel(self, page=1, panel=1, description="Nagoji waits.", copy_items=None):
        return {'id': f'page-{page:02d}-panel-{panel:02d}', 'page': page, 'panel': panel,
                'description': description, 'copy': copy_items or []}

    def prompt(self, panel=None, cast=None, chapter=9, sheets=None):
        return p.assemble_prompt_v2(panel or self.panel(), chapter, self.continuity,
                                    ['nagoji'] if cast is None else cast, self.direction, sheets or [])

    def prepare(self, **kwargs):
        self.direction_path.write_text(json.dumps(self.direction))
        caveats = copy.deepcopy(getattr(p, 'SHEET_CAVEATS', {}))
        for key in caveats:
            if key in self.sheets:
                caveats[key]['sha256'] = p.sha256(self.sheets[key])
        with patch.object(p, 'SHEET_CAVEATS', caveats, create=True):
            return p.prepare(9, self.root / 'out', scripts_dir=self.scripts, continuity_path=self.bible,
                             cast_overrides_path=self.cast_path, art_direction_path=self.direction_path, **kwargs)

    def test_chapter_9_without_art_direction_is_refused(self):
        with self.assertRaisesRegex(ValueError, '--art-direction'):
            p.prepare(9, self.root/'out', scripts_dir=self.scripts, continuity_path=self.bible,
                      cast_overrides_path=self.cast_path)
        self.assertFalse((self.root/'out').exists())

    def test_art_direction_prepares_v2_and_records_profile_hash_and_snapshot(self):
        result = self.prepare()
        job = json.loads(Path(result['job_json']).read_text())
        self.assertEqual(job['prompt_profile'], 'v2')
        self.assertEqual(job['art_direction']['sha256'], p.sha256(self.direction_path))
        self.assertEqual(job['art_direction']['sha256'], p.sha256(self.root/'out/ART-DIRECTION-SNAPSHOT.json'))
        self.assertTrue(all(item['setting'] == 'verandah' for item in job['jobs']))
        self.assertEqual(job['jobs'][0]['sheet_keys'], ['nagoji'])
        self.assertTrue(job['jobs'][0]['reference_images'][0].endswith('nagoji-v2.png'))
        self.assertIn('1) Nagoji', job['jobs'][0]['image_gen']['args']['prompt'])

    def test_draft_requires_allow_draft_and_unknown_profile_is_refused(self):
        self.direction['status'] = 'draft'
        with self.assertRaisesRegex(ValueError, '--allow-draft'):
            self.prepare()
        self.prepare(allow_draft=True)
        self.direction['prompt_profile'] = 'v3'
        with self.assertRaisesRegex(ValueError, 'prompt_profile'):
            self.prepare(allow_draft=True)

    def test_span_contains_pages_and_panels(self):
        for span, page, panel, expected in [('@3',3,5,True),('@3',4,1,False),('@8.4-10',8,3,False),
                ('@8.4-10',8,4,True),('@8.4-10',10,9,True),('@8.4-10',11,1,False),
                ('@2.4-',99,1,True),('@1-8.3',8,3,True),('@1-8.3',8,4,False)]:
            self.assertEqual(p._span_contains(span,page,panel),expected,span)
        for span in ('@x','@0','@3-2','@1.0','@1--2'):
            with self.subTest(span=span), self.assertRaises(ValueError):
                p._span_contains(span,1,1)

    def test_v2_nagoji_row_follows_page_and_panel(self):
        for page, panel, footwear in ((1,1,'boots'),(2,3,'boots'),(2,4,'barefoot'),(11,5,'barefoot')):
            look = p._nagoji_look_v2(self.continuity,9,page,panel)
            self.assertIn(footwear, look)
            self.assertNotIn('barefoot' if footwear == 'boots' else 'boots', look)
            self.assertNotIn('|',look); self.assertNotIn('@',look)

    def test_v2_character_rows_follow_page_and_panel(self):
        for page, included, excluded in ((3,'Hill shrine','Fort room'),(7,'Fort room','Hill shrine')):
            look = p._character_look_v2(self.continuity,'varma',22,page,1)
            self.assertIn(included,look); self.assertNotIn(excluded,look)
        self.assertNotIn('shrine',p._character_look_v2(self.continuity,'varma',23,1,1))

    def test_v1_row_reader_skips_span_rows(self):
        for chapter in (7,22):
            look = p._look_for_chapter(self.continuity['blocks']['marthanda varma'],chapter)
            self.assertNotIn('@',look); self.assertNotIn('Hill shrine',look)

    def test_v1_scoped_section_does_not_change_prompts(self):
        raw = V2_CONTINUITY.split('## Scoped art rules')[0] + '## Standing rules' + V2_CONTINUITY.split('## Standing rules')[1]
        without = {'raw':raw,'blocks':p._continuity_blocks(raw)}
        self.assertEqual(p.assemble_prompt(self.panel(),1,self.continuity,['nagoji']),
                         p.assemble_prompt(self.panel(),1,without,['nagoji']))

    def test_v2_looks_header_keeps_identity_and_yields_situation_to_the_panel(self):
        prompt = self.prompt()
        self.assertIn('LOOKS (face, build, hair, facial hair, scars, marks and ear ornament always follow these lines;',prompt)
        self.assertIn('footwear, sleeves, headwear, props in hand and pose follow the panel description above wherever it is more specific)',prompt)
        self.assertNotIn('overrides the script on appearance',prompt)

    def test_v2_drops_the_captivity_stubble_allowance_outside_captivity(self):
        self.assertIn('CLEAN-SHAVEN CHIN',self.prompt())
        self.assertNotIn('stubble',self.prompt())
        self.assertIn('light stubble at most',self.prompt(chapter=1))

    def test_v2_cleans_bullet_labels_and_chapter_scope_notes(self):
        prompt = self.prompt(cast=['padmini','ibrahim'])
        self.assertIn('Padmini Amma: in her fifties; thick black hair coiled at the nape.',prompt)
        self.assertIn('Ibrahim Marakkar: white turban',prompt)
        for unwanted in ('kapitan','Dies','ch27','- **'):
            self.assertNotIn(unwanted,prompt)

    def test_v2_refuses_life_arc_or_page_words_in_a_selected_look(self):
        for old, new in [('in her fifties','going grey later'),('Short coat.','Pages 1 and 2: hair loose.'),
                         ('Short coat.','after he changes'),('Short coat.','until the rain')]:
            raw = V2_CONTINUITY.replace(old,new)
            self.continuity={'raw':raw,'blocks':p._continuity_blocks(raw)}
            with self.assertRaises(ValueError): self.prompt(cast=['padmini','ibrahim'])

    def test_v2_refuses_foreign_terms_from_the_bible_in_an_indian_setting(self):
        with self.assertRaisesRegex(ValueError,'page-01-panel-01.*portuguese.*look'):
            self.prompt(chapter=10)
        self.direction['settings']['verandah']['allow_terms']=['portuguese']
        self.prompt(chapter=10)
        self.direction['settings']['verandah']['scopes']=['portuguese']
        self.prompt(chapter=10)
        self.direction=v2_direction()
        self.prompt(cast=['duarte'])
        self.prompt(self.panel(description='Portuguese brand.'))

    def test_v2_rules_are_scoped_by_setting(self):
        prompt = self.prompt()
        self.assertIn('No blood or gore',prompt); self.assertIn('clay or brass',prompt)
        for unwanted in ('Portuguese','Dutch','VOC','Goa','iron ring','Period: 1738','upscale','STANDING CONTINUITY RULES'):
            self.assertNotIn(unwanted,prompt)
        self.direction['pages']['1']='cellar'
        self.assertIn('iron ring',self.prompt()); self.assertNotIn('clay or brass',self.prompt())

    def test_v2_refuses_a_bible_without_the_scoped_rules_section(self):
        self.continuity={'raw':CONTINUITY,'blocks':p._continuity_blocks(CONTINUITY)}
        with self.assertRaisesRegex(ValueError,'Scoped art rules'): self.prompt(cast=[])

    def test_v2_refuses_an_unknown_scope_tag(self):
        self.continuity['raw']=V2_CONTINUITY.replace('[dutch]','[kerela]')
        with self.assertRaisesRegex(ValueError,'kerela'): self.prompt()

    def test_v2_summarises_copy_without_quoting_it(self):
        items=[{'speaker':'CAPTION','text':'In Goa they wrote me down as a number.'},
               {'speaker':'NAGOJI','text':'The Portuguese tried to convince me otherwise.'},
               {'speaker':'REVATHI (off)','text':'Our *fortresses* are both.'}]
        prompt=self.prompt(self.panel(copy_items=items))
        for word in ('Goa','Portuguese','fortresses','*'): self.assertNotIn(word,prompt)
        for wording in ('exactly 3 lettering area(s)','a caption (short)','a speech balloon for Nagoji (medium)',
                        'a speech balloon for Revathi Bayi, speaking from off panel (short)'):
            self.assertIn(wording,prompt)

    def test_v2_lettering_word_boundaries_aliases_objects_and_placement(self):
        for speaker, expected in [('PADMINI (off, small lettering)','speech balloon for Padmini Amma'),
                ('PADMINI (letter)','a caption'),('RANI','The Senior Rani of Attingal'),
                ('THARAKAN','Mathoo Tharakan'),('THOMA','Thoma Ittyerah'),('ENVOY','Dutch envoys'),
                ('SENIOR ENVOY','Dutch envoys'),('DUTCH SCRIBE','Dutch envoys'),
                ('LEAF','on an object'),('LEDGER (lettered on the left page)','on an object'),
                ('CAPTION (leaf)','on an object'),('CAPTION (stitched lettering)','on an object'),
                ('DE LANNOY (inset, lettered untranslated)','speech balloon for Eustachius De Lannoy')]:
            block=p._lettering_v2([{'speaker':speaker,'text':'Private.'}],self.continuity)
            self.assertIn(expected,block,speaker)
            if 'object' in expected: self.assertNotIn('upper part',block)
        block=p._lettering_v2([{'speaker':'NAGOJI (left half, inset)','text':'x'*101}],self.continuity)
        self.assertIn('left half',block); self.assertIn('inset',block); self.assertIn('(long)',block)

    def test_v2_silent_panel_needs_no_lettering_areas(self):
        self.assertIn('LETTERING: none in this panel',self.prompt()); self.assertNotIn('Leave clear',self.prompt())

    def test_v2_states_the_no_text_rule_once_and_allows_unlettered_banners(self):
        prompt=self.prompt()
        self.assertEqual(prompt.count('Draw NO'),1)
        self.assertIn('including on banners, flags',prompt)
        self.assertNotIn('symbols',prompt); self.assertNotIn('banners or text',prompt)

    def test_v2_drops_letterer_directions(self):
        panel=self.panel(); panel['directions']=['(Letter as one balloon.)','No text. Hold the silence.']
        prompt=self.prompt(panel)
        self.assertNotIn('Letter as one balloon',prompt); self.assertIn('Hold the silence',prompt)

    def test_v2_sheet_line_lists_sheets_in_attachment_order(self):
        prompt=self.prompt(cast=['ibrahim','nagoji','padmini'],sheets=['ibrahim','nagoji','padmini'])
        self.assertIn('3 attached image(s), in this order: 1) Ibrahim Marakkar, 2) Nagoji, 3) Padmini Amma',prompt)
        for text in ('use them only for faces, build, hair and costume','not the hanging drop','not red as drawn','grey strands'):
            self.assertIn(text,prompt)
        self.assertNotIn('REFERENCE SHEETS',self.prompt())

    def test_v2_nagoji_sheet_clause_matches_the_selected_look(self):
        self.assertIn('full-length commander figure',self.prompt(sheets=['nagoji']))
        self.assertIn('captivity figure',self.prompt(chapter=1,sheets=['nagoji']))

    def test_v2_refuses_a_sheet_whose_caveat_hash_is_stale(self):
        self.direction_path.write_text(json.dumps(self.direction))
        for key in ('nagoji','padmini','ibrahim'):
            cast={x['id']:[key] for page in self.script['pages'].values() for x in page['panels']}
            self.cast_path.write_text(json.dumps(cast))
            # Name-independent descriptions isolate sheet validation from the cast lint.
            self.script_path.write_text(self.script_path.read_text().replace('Nagoji waits.','A quiet room.'))
            with self.subTest(key=key), self.assertRaisesRegex(ValueError,'caveat'):
                p.prepare(9,self.root/'out',scripts_dir=self.scripts,continuity_path=self.bible,
                          cast_overrides_path=self.cast_path,art_direction_path=self.direction_path)
        self.assertFalse((self.root/'out').exists())

    def spanned_sheets(self, spans):
        """Real sheet resolution over the fixture sheets, with a commander sheet approved for the given spans."""
        (self.root / '21-nagoji-commander-v15.png').write_bytes(b'commander fixture sheet')
        entry = {'file': '21-nagoji-commander-v15.png', 'sha256': p.sha256(self.root / '21-nagoji-commander-v15.png'),
                 'character': 'nagoji', 'spans': spans}
        (self.root / 'APPROVED-SHEETS.json').write_text(json.dumps({'nagoji_commander': entry}))
        for name, value in (('APPROVED_SHEETS', self.root / 'APPROVED-SHEETS.json'), ('CONCEPT_ROOT', self.root),
                            ('_concept_sheets', REAL_CONCEPT_SHEETS)):
            patcher = patch.object(p, name, value)
            patcher.start(); self.addCleanup(patcher.stop)

    def prepared_jobs(self):
        job = json.loads((self.root / 'out/IMAGEGEN-JOBS.json').read_text())
        return {(item['page'], item['panel']): item for item in job['jobs']}

    def test_v2_jobs_attach_the_sheet_that_covers_the_panel(self):
        self.spanned_sheets([['9.3', '9.4.2']])
        self.prepare()
        jobs = self.prepared_jobs()
        for (page, panel), item in jobs.items():
            covered = (page, panel) >= (3, 1) and (page, panel) <= (4, 2)
            self.assertEqual([Path(x).name for x in item['reference_images']],
                             ['21-nagoji-commander-v15.png' if covered else 'nagoji-v2.png'], (page, panel))
            self.assertEqual(item['sheet_keys'], ['nagoji'])
            self.assertEqual(list(item['reference_image_sha256']), item['reference_images'])
            self.assertEqual(item['image_gen']['args']['referenced_image_paths'], item['reference_images'])
        self.assertEqual(p.audit_prompts(self.root / 'out/IMAGEGEN-JOBS.json')['sheet_order_matches'], 55)

    def test_v2_caveat_is_attached_only_to_panels_on_the_caveats_own_sheet(self):
        self.spanned_sheets([['9.3', '9.4.2']])
        self.prepare()
        for (page, panel), item in self.prepared_jobs().items():
            covered = (page, panel) >= (3, 1) and (page, panel) <= (4, 2)
            prompt = Path(item['prompt_path']).read_text()
            self.assertIn('REFERENCE SHEETS: 1 attached image(s)', prompt)
            self.assertEqual('not the hanging drop' in prompt, not covered, (page, panel))
            self.assertEqual('hilltop fort' in prompt, not covered, (page, panel))

    def test_v2_stale_caveat_hash_is_refused_only_for_panels_on_the_caveats_own_sheet(self):
        self.direction_path.write_text(json.dumps(self.direction))
        stale = copy.deepcopy(p.SHEET_CAVEATS)
        stale['nagoji']['sha256'] = 'f' * 64
        def run():
            with patch.object(p, 'SHEET_CAVEATS', stale):
                p.prepare(9, self.root / 'out', scripts_dir=self.scripts, continuity_path=self.bible,
                          cast_overrides_path=self.cast_path, art_direction_path=self.direction_path)
        self.spanned_sheets([['9.3', '9.4']])
        with self.assertRaisesRegex(ValueError, 'caveat'):
            run()
        self.assertFalse((self.root / 'out').exists())
        self.spanned_sheets([['9.1', '9.99']])
        run()
        jobs = self.prepared_jobs()
        self.assertEqual({Path(x).name for item in jobs.values() for x in item['reference_images']},
                         {'21-nagoji-commander-v15.png'})
        self.assertNotIn('not the hanging drop', Path(jobs[(1, 1)]['prompt_path']).read_text())

    def test_v1_jobs_attach_the_sheet_that_covers_the_panel(self):
        self.spanned_sheets([['8.2', '8.3.1']])
        (self.scripts / 'CHAPTER-08-SCRIPT.md').write_text(self.script_path.read_text())
        p.prepare(8, self.root / 'out', scripts_dir=self.scripts, continuity_path=self.bible, cast_overrides_path=self.cast_path)
        for (page, panel), item in self.prepared_jobs().items():
            covered = (2, 1) <= (page, panel) <= (3, 1)
            self.assertEqual([Path(x).name for x in item['reference_images']],
                             ['21-nagoji-commander-v15.png' if covered else 'nagoji-v2.png'], (page, panel))
            self.assertEqual(item['image_gen']['args']['referenced_image_paths'], item['reference_images'])
            self.assertEqual(list(item['reference_image_sha256']), item['reference_images'])

    def test_v2_setting_paragraph_is_last_and_place_is_in_the_header(self):
        prompt=self.prompt(); end=prompt.split('\n\n')[-1]
        self.assertTrue(end.startswith('SETTING (this panel):'))
        self.assertIn('Timber verandah',end); self.assertIn('Light: morning light',end)
        self.assertIn('No masonry towers',end); self.assertIn('Place: Velinadu verandah',prompt.splitlines()[0])

    def test_v2_panel_time_overrides_setting_time_and_merges_default(self):
        prompt=self.prompt(self.panel(2,4))
        self.assertIn('Light: night, oil lamps',prompt); self.assertNotIn('morning light',prompt)

    def test_v2_must_match_notes_only_for_cast_members(self):
        self.assertIn('BLACK with no grey',self.prompt(cast=['padmini']))
        self.assertNotIn('BLACK with no grey',self.prompt())

    def test_v2_people_line_counts_people_not_horses_or_groups(self):
        self.assertIn('PEOPLE IN THIS PANEL: Nagoji. Draw each named person once',
                      self.prompt(cast=['kayal','madurai_troop','nagoji']))

    def test_v2_insert_and_explicit_distant_strip_wording(self):
        self.assertIn('INSERT: frame only',self.prompt(self.panel(description='Insert, tight. His hands.')))
        self.direction['panels']['page-01-panel-01']={'frame':'strip','distant':True}
        prompt=self.prompt(self.panel(description='Full width, bottom strip. The beach.'))
        self.assertIn('keep the key action inside the middle half',prompt)
        self.assertNotIn('keep faces and the key action',prompt)
        self.direction['panels']['page-01-panel-01']['distant']=False
        self.assertIn('keep faces and',self.prompt(self.panel(description='Full width. Small round shields.')))

    def test_v2_tall_frame_and_conflicting_override(self):
        self.direction['panels']['page-01-panel-01']={'frame':'tall'}
        self.assertIn('FRAME SHAPE: a tall',self.prompt(self.panel(description='Tall panel. Nagoji stands.')))
        self.assertIn('FRAME SHAPE: a tall',self.prompt(self.panel(description='Taller than the other panels. Nagoji stands.')))
        for description,frame in [('Full width. Nagoji.','standard'),('Nagoji waits.','strip'),('Full width. Nagoji.','tall')]:
            self.direction['panels']['page-01-panel-01']={'frame':frame}
            with self.subTest(description=description),self.assertRaisesRegex(ValueError,'frame'):
                self.prompt(self.panel(description=description))

    def test_v2_distant_flag_on_standard_frame_does_not_invent_strip(self):
        self.direction['panels']['page-01-panel-01']={'distant':True}
        prompt=self.prompt(self.panel(description='Wide. A rider small in the distance.'))
        self.assertNotIn('FRAME SHAPE',prompt)

    def test_v2_bleed_lettering_space_and_no_sheet_insert(self):
        self.direction['panels']['page-01-panel-01']={'bleed':'A memory of the Goa cellar within the arm.',
            'lettering_space':'Stack down the left side.', 'sheets':False}
        prompt=self.prompt(self.panel(description='Insert. Stack the balloons down one side.',
                                      copy_items=[{'speaker':'CAPTION','text':'Private words.'}]))
        self.assertIn('MEMORY BLEED:',prompt); self.assertIn('Stack down the left side',prompt)
        self.assertIn('means space only',prompt); self.assertNotIn('preferably in the upper',prompt)
        self.prepare()
        job=json.loads((self.root/'out/IMAGEGEN-JOBS.json').read_text())['jobs'][0]
        self.assertEqual(job['reference_images'],[]); self.assertEqual(job['sheet_keys'],[])

    def test_v2_has_style_cue_and_no_dashes(self):
        self.assertIn('never photorealistic',self.prompt().splitlines()[0])
        for dash in (chr(0x2013),chr(0x2014)): self.assertNotIn(dash,self.prompt())

    def test_art_direction_must_cover_every_panel_and_use_known_ids(self):
        mutations=[lambda d:d['pages'].pop('1'),lambda d:d['pages'].update({'1':'unknown'}),
            lambda d:d['settings']['verandah'].update(scopes=['kerela']),
            lambda d:d['settings']['verandah'].update(anchor='bad'+chr(0x2014)),
            lambda d:d.update(chapter=10),lambda d:d.update(typo=True),
            lambda d:d['panels'].update({'page-99-panel-01':{'time':'night'}}),
            lambda d:d['panels']['page-02-panel-04'].update(unknown=True),
            lambda d:d['panels']['page-02-panel-04'].update(sheets='false'),
            lambda d:d['settings']['verandah'].update(absent=''),
            lambda d:d['character_notes'].update(unknown='bad'),lambda d:d.update(status='pending'),
            lambda d:d['not_shown'].update({'page-01-panel-01':['unknown']})]
        for mutate in mutations:
            direction=v2_direction(); mutate(direction); self.direction_path.write_text(json.dumps(direction))
            with self.subTest(direction=direction),self.assertRaises(ValueError):
                p.load_art_direction(self.direction_path,self.script,9)

    def test_v2_cast_lint_requires_mentioned_principals_cast_or_not_shown(self):
        panel=self.panel(description='Padmini, looking toward the doorway where Revathi went.')
        with self.assertRaisesRegex(ValueError,'page-01-panel-01.*revathi'):
            p._lint_cast_v2([panel],{panel['id']:['padmini']},self.direction)
        self.direction['not_shown'][panel['id']]=['revathi']
        p._lint_cast_v2([panel],{panel['id']:['padmini']},self.direction)
        self.assertIn('Revathi Bayi is outside the frame',self.prompt(panel,cast=['padmini']))

    def test_v2_cast_lint_covers_pronouns_titles_and_aggregates(self):
        panels=[self.panel(i,1,description) for i,description in enumerate(
                ['Not looking at him.','His boots.','Her eyes never leave him.','The king.','Maharaja.','The diwan.','Dalawa.'],1)]
        with self.assertRaises(ValueError) as caught:
            p._lint_cast_v2(panels,{x['id']:[] for x in panels},self.direction)
        for panel in panels: self.assertIn(panel['id'],str(caught.exception))
        for panel in panels[:3]: self.direction['not_shown'][panel['id']]=['nagoji']
        p._lint_cast_v2(panels[:3],{x['id']:[] for x in panels[:3]},self.direction)

    def test_v2_nagoji_missing_overlapping_and_invalid_spans_fail_closed(self):
        for raw in [V2_CONTINUITY.replace('| 9 @2.4- |','| 8 |'),
                V2_CONTINUITY.replace('| 9 @2.4- |','| 9 @2.3- |'),
                V2_CONTINUITY.replace('| 9 @1-2.3 |','| 9 @1-12 |'),
                V2_CONTINUITY.replace('| 9 @1-2.3 |','| 9-10 @1-2.3 |')]:
            self.bible.write_text(raw)
            with self.subTest(raw=raw),self.assertRaises(ValueError): self.prepare()
            self.assertFalse((self.root/'out').exists())

    def test_v2_late_lint_failure_leaves_no_files(self):
        self.direction['pages']={str(page):'cellar' for page in range(1,12)}
        self.direction['panels']['page-11-panel-05']={'setting':'verandah'}
        self.direction['character_notes']['nagoji']='A Portuguese guard.'
        with self.assertRaises(ValueError): self.prepare()
        self.assertFalse((self.root/'out').exists())

    def test_v2_refuses_canonical_pre9_package_before_writes(self):
        self.direction['chapter']=8
        self.direction_path.write_text(json.dumps(self.direction))
        with patch.object(p,'V15',self.root):
            with self.assertRaisesRegex(ValueError,'canonical'):
                p.prepare(8,self.root/'chapters/ch08',art_direction_path=self.direction_path)
        self.assertFalse((self.root/'chapters').exists())

    def test_v1_prepare_for_chapter_8_adds_no_v2_keys_or_files(self):
        path=self.scripts/'CHAPTER-08-SCRIPT.md'; path.write_text(self.script_path.read_text())
        p.prepare(8,self.root/'out',scripts_dir=self.scripts,continuity_path=self.bible,cast_overrides_path=self.cast_path)
        job=json.loads((self.root/'out/IMAGEGEN-JOBS.json').read_text())
        self.assertNotIn('prompt_profile',job); self.assertNotIn('art_direction',job)
        self.assertFalse((self.root/'out/ART-DIRECTION-SNAPSHOT.json').exists())
        self.assertIn('AUTHORITATIVE CONTINUITY',job['jobs'][0]['image_gen']['args']['prompt'])

    def test_prompt_audit_is_read_only_and_audits_sent_corrections(self):
        self.prepare(); out=self.root/'out'; job_path=out/'IMAGEGEN-JOBS.json'
        before={str(x):p.sha256(x) for x in out.rglob('*') if x.is_file()}
        audit=p.audit_prompts(job_path)
        self.assertEqual(audit['prompt_count'],55); self.assertEqual(audit['setting_last'],55)
        self.assertEqual(audit['copy_leaks'],0); self.assertEqual(audit['foreign_terms'],0)
        self.assertEqual(audit['draw_no_once'],55); self.assertEqual(audit['sheet_order_matches'],55)
        self.assertEqual(before,{str(x):p.sha256(x) for x in out.rglob('*') if x.is_file()})
        sent=out/'sent.txt'
        base=(out/'prompts/page-01-panel-01.txt').read_text().strip()
        sent.write_text(base+'\n\nPortuguese castle. A private thought.\n')
        candidates=out/'candidates'; candidates.mkdir()
        (candidates/'page-01-panel-01-v01.json').write_text(json.dumps({'id':'page-01-panel-01',
                'prompt_path':str(sent),'prompt_sha256':p.sha256(sent)}))
        audit=p.audit_prompts(job_path)
        self.assertEqual(audit['sent_prompt_count'],1)
        self.assertGreater(audit['copy_leaks'],0); self.assertGreater(audit['foreign_terms'],0)
        self.assertEqual(audit['setting_last'],55)

    def test_audit_cli_does_not_require_chapter(self):
        self.prepare()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(p.main(['audit','--out',str(self.root/'out')]),0)
        self.assertEqual(json.loads(output.getvalue())['prompt_count'],55)

    def test_audit_verifies_reference_hashes(self):
        self.prepare()
        self.sheets['nagoji'].write_bytes(b'changed sheet')
        with self.assertRaisesRegex(ValueError,'reference.*hash'):
            p.audit_prompts(self.root/'out/IMAGEGEN-JOBS.json')

    def test_audit_does_not_exempt_unrecognised_appended_sections(self):
        self.prepare(); out=self.root/'out'
        base=(out/'prompts/page-01-panel-01.txt').read_text().strip()
        sent=out/'sent.txt'
        sent.write_text(base+'\n\nSETTING (this panel): Portuguese castle.\n\n'+base.split('\n\n')[-1])
        (out/'candidates').mkdir()
        (out/'candidates/page-01-panel-01-v01.json').write_text(json.dumps({'id':'page-01-panel-01',
            'prompt_path':str(sent),'prompt_sha256':p.sha256(sent)}))
        audit=p.audit_prompts(out/'IMAGEGEN-JOBS.json')
        self.assertEqual(audit['setting_last'],56)
        self.assertGreaterEqual(audit['foreign_terms'],2)

    def test_audit_exempts_only_the_assembled_not_shown_line(self):
        self.direction['not_shown']['page-01-panel-01']=['dutch_envoys']
        self.prepare(); out=self.root/'out'
        base=(out/'prompts/page-01-panel-01.txt').read_text().strip()
        self.assertIn('NOT SHOWN: Dutch envoys is outside the frame.',base)
        self.assertEqual(p.audit_prompts(out/'IMAGEGEN-JOBS.json')['foreign_terms'],0)
        sent=out/'sent.txt'
        sent.write_text(base.replace('NOT SHOWN: Dutch envoys is outside the frame.','NOT SHOWN: A Portuguese castle.'))
        (out/'candidates').mkdir()
        (out/'candidates/page-01-panel-01-v01.json').write_text(json.dumps({'id':'page-01-panel-01',
            'prompt_path':str(sent),'prompt_sha256':p.sha256(sent)}))
        self.assertGreaterEqual(p.audit_prompts(out/'IMAGEGEN-JOBS.json')['foreign_terms'],1)

    def test_overlapping_span_rows_for_one_character_are_refused(self):
        p._validate_spans(p.load_continuity(self.bible),self.script,22)
        self.bible.write_text(V2_CONTINUITY.replace('| 22 @7- | Fort room. |','| 22 @5- | Fort room. |'))
        with self.assertRaisesRegex(ValueError,'marthanda varma: chapter 22 span rows overlap at page 5 panel 1'):
            p._validate_spans(p.load_continuity(self.bible),self.script,22)

    def test_chapter_rows_still_layer_with_each_other(self):
        self.bible.write_text(V2_CONTINUITY.replace('- **Revathi Bayi**: indigo sari with gold.',
            '- **Revathi Bayi**: indigo sari with gold.\n  | 9-28 | Wears a tali. |\n  | 9 | Plain white. |'))
        bible=p.load_continuity(self.bible)
        p._validate_spans(bible,self.script,9)
        self.assertEqual(p._character_look_v2(bible,'revathi',9,1,1),'indigo sari with gold. Wears a tali. Plain white.')

    def test_prepare_late_conflicting_file_does_not_write_snapshots(self):
        out=self.root/'out'; (out/'prompts').mkdir(parents=True)
        prompt=out/'prompts/page-11-panel-05.txt'; prompt.write_text('frozen')
        with self.assertRaises(FileExistsError): self.prepare()
        self.assertEqual([x for x in out.rglob('*') if x.is_file()],[prompt])

    def test_foreign_guard_applies_to_rules_notes_and_lettering(self):
        for source in ('rules','notes','lettering'):
            self.continuity=p.load_continuity(self.bible); self.direction=v2_direction()
            panel=self.panel()
            if source=='rules': self.continuity['raw']=V2_CONTINUITY.replace('No blood or gore.','A Portuguese soldier.')
            elif source=='notes': self.direction['character_notes']['nagoji']='A Portuguese soldier.'
            else: panel['copy']=[{'speaker':'DUTCH SCRIBE','text':'Private.'}]
            with self.subTest(source=source),self.assertRaises(ValueError): self.prompt(panel)

    def test_art_direction_rejects_nested_types_and_escaped_dashes(self):
        cases=[None,[],{'prompt_profile':'v2'},v2_direction(),v2_direction(),v2_direction()]
        cases[3]['settings']['verandah']['scopes']=[{}]
        cases[4]['settings']['verandah']['anchor']='bad'+chr(0x2013)
        cases[5]['pages']=[]
        for direction in cases:
            self.direction_path.write_text(json.dumps(direction))
            with self.subTest(direction=direction),self.assertRaises(ValueError):
                p.load_art_direction(self.direction_path,self.script,9)


class Chapter9V2AcceptanceTests(unittest.TestCase):
    def test_live_bible_carries_the_approved_v2_edits(self):
        """Author approved 2026-10-02: review-sheets/CONTINUITY-PROMPT-V2-REVIEW.html, plus Padmini grey from ch16."""
        bible=p.load_continuity(p.CONTINUITY)
        for text in ('| 9 @1-2.3 |','| 9 @14- |','| 10 @1-1.3 |','| 13-15 |','## Scoped art rules (prompt profile v2)'):   # 9 @11- became @14- in the 2026-10-07 split
            self.assertIn(text,bible['raw'])
        self.assertNotIn('| 9-15 |',bible['raw'])
        for chapter in (9,15):
            self.assertNotIn('grey',p._character_look_v2(bible,'padmini',chapter,1,1).lower())
        for chapter in (16,27):
            self.assertIn('grey',p._character_look_v2(bible,'padmini',chapter,1,1).lower())

    def test_chapter_9_prepares_clean_v2_prompts(self):
        """Real script and draft data, with explicit test sheet bytes and approval hashes."""
        sidecar=p.SCRIPTS/'CHAPTER-09-ART-DIRECTION.json'
        self.assertTrue(sidecar.is_file())
        live=p.CONTINUITY; live_hash=p.sha256(live)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            approved=json.loads(p.APPROVED_SHEETS.read_text())
            names={**{key:value['file'] for key,value in approved.items()},**p.CONCEPTS}
            sheets={key:root/name for key,name in names.items()}
            for key,path in sheets.items(): path.write_bytes((key+' test sheet').encode())
            caveats=copy.deepcopy(p.SHEET_CAVEATS)
            for key in caveats: caveats[key]['sha256']=p.sha256(sheets[key])
            lock=root/'lock.json'; lock.write_text('{}')
            baseline=p.V15/'chapters/ch05/CONTINUITY-SNAPSHOT.md'
            with patch.object(p,'_concept_sheets',return_value=sheets),patch.object(p,'SHEET_CAVEATS',caveats), \
                    patch.object(p,'LOCK_PATH',lock),patch.object(p,'CONTINUITY',baseline):
                result=p.prepare(9,root/'out',continuity_path=live,
                    cast_overrides_path=p.SCRIPTS/'CHAPTER-09-CAST-OVERRIDES.json',
                    art_direction_path=sidecar,allow_draft=True)
                job=json.loads(Path(result['job_json']).read_text())
                audit=p.audit_prompts(Path(result['job_json']))
            self.assertEqual(result['job_count'],53)
            for key in ('setting_last','draw_no_once','sheet_order_matches','rules_under_10_percent'):
                self.assertEqual(audit[key],53,key)
            self.assertEqual(audit['copy_leaks'],0); self.assertEqual(audit['foreign_terms'],0)
            self.assertEqual(audit['footwear_checks'],34); self.assertEqual(audit['footwear_matches'],34)
            self.assertTrue(audit['median_at_or_below_v1'])
            for item in job['jobs']:
                prompt=Path(item['prompt_path']).read_text()
                self.assertIn('No blood or gore',prompt)
                self.assertNotIn('stubble',prompt)
                if 'padmini' in item['cast']: self.assertIn('BLACK with no grey',prompt)
                if item['id'] in ('page-07-panel-02','page-11-panel-02'):   # 5.2 and 8.2 before the 2026-10-07 page splits
                    self.assertEqual(item['reference_images'],[])
                if item['id'] in ('page-08-panel-03','page-13-panel-04'):
                    self.assertIn('FRAME SHAPE: a tall',prompt)
                if item['id'] in ('page-07-panel-04','page-10-panel-05','page-13-panel-03'):
                    self.assertIn('MEMORY BLEED:',prompt)
                if item['id'] in ('page-13-panel-03','page-13-panel-04'):
                    self.assertIn('Light: late afternoon',prompt)
                if 'SETTING (this panel): Velinadu Kovilakam' in prompt:
                    self.assertIn('Any banners are plain cloth with no emblem.',prompt)
            self.assertEqual(job['art_direction']['sha256'],p.sha256(sidecar))
        self.assertEqual(p.sha256(p.CONTINUITY),live_hash)


if __name__ == "__main__":
    unittest.main()
