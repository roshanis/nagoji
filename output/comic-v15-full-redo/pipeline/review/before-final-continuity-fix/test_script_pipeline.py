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
            self.assertIn("exactly 1 blank outlined text area", prompt)

    def test_nagoji_constant_identity_and_epilogue_row(self):
        continuity = p.load_continuity(Path(__file__).resolve().parents[3] / "output/comic-v15-full-redo/CONTINUITY.md")
        look = p._nagoji_look(continuity, 1)
        self.assertIn("CLEAN-SHAVEN CHIN", look)
        self.assertIn("thick curled moustache", look)
        self.assertIn("small gold ear stud", look)
        self.assertIn("captivity sheet", look.lower())
        self.assertIn("grey-streaked", p._nagoji_look(continuity, 28))

    def test_temple_priest_is_only_an_explicit_cast_key_and_empty_override_wins(self):
        self.assertEqual(p._references(["duarte"], "temple priest"), [])
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
            p.prepare(2, out, scripts_dir=scripts, continuity_path=continuity_path)
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
            result = p.prepare(2, out, scripts_dir=scripts, continuity_path=continuity_path)
            self.assertEqual(result["job_count"], 1)
            payload = json.loads((out / "IMAGEGEN-JOBS.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["jobs"][0]["image_gen"]["tool"], "image_gen__imagegen")
            self.assertTrue(payload["jobs"][0]["reference_images"][0].endswith("nagoji-v2.png"))
            (out / "SCRIPT-SNAPSHOT.json").write_text("conflict", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                p.prepare(2, out, scripts_dir=scripts, continuity_path=continuity_path)


if __name__ == "__main__":
    unittest.main()
