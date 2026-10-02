import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
import run_chapter as r


class PackageDirTests(unittest.TestCase):
    """A chapter can be rebuilt in a sibling package (ch01-v2) without touching the original."""

    def test_default_package(self):
        self.assertEqual(r.package(2), r.V15 / "chapters" / "ch02")

    def test_sibling_package_for_the_same_chapter(self):
        self.assertEqual(r.package(1, r.V15 / "chapters" / "ch01-v2"), r.V15 / "chapters" / "ch01-v2")

    def test_package_of_another_chapter_is_refused(self):
        with self.assertRaises(ValueError):
            r.package(1, r.V15 / "chapters" / "ch02")
        with self.assertRaises(ValueError):
            r.package(1, r.V15 / "chapters" / "ch010")

    def test_package_outside_chapters_is_refused(self):
        with self.assertRaises(ValueError):
            r.package(1, Path("/tmp/ch01-v2"))
        with self.assertRaises(ValueError):
            r.package(1, r.V15 / "chapters" / "ch01-v2" / ".." / ".." / "ch01-v2")

    def test_prepare_forwards_art_direction_and_allow_draft(self):
        package_dir = r.V15 / "chapters" / "ch09-pilot"
        with mock.patch.object(r.s, "prepare", return_value={"ok": True}) as prepare:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                r.main([
                    "prepare", "--chapter", "9", "--package-dir", str(package_dir),
                    "--cast-overrides", "cast.json", "--art-direction", "direction.json",
                    "--allow-draft",
                ])
        prepare.assert_called_once_with(
            9, package_dir, cast_overrides_path=Path("cast.json"),
            art_direction_path=Path("direction.json"), allow_draft=True,
        )

    def test_prepare_without_art_direction_keeps_v1_call_shape(self):
        package_dir = r.V15 / "chapters" / "ch02-pilot"
        with mock.patch.object(r.s, "prepare", return_value={"ok": True}) as prepare:
            with contextlib.redirect_stdout(io.StringIO()):
                r.main(["prepare", "--chapter", "2", "--package-dir", str(package_dir)])
        prepare.assert_called_once_with(2, package_dir, cast_overrides_path=None,
                                        art_direction_path=None, allow_draft=False)



class StyledReservePixelTests(unittest.TestCase):
    def test_unreadable_ink_bounds_are_used_by_native_pixel_audit(self):
        import tempfile
        from types import SimpleNamespace
        from PIL import Image, ImageDraw
        import compositor as c
        from test_compositor import lettering_fixture
        with tempfile.TemporaryDirectory() as tmp:
            rows, script, geometry = lettering_fixture(tmp, '... *kapitan* ...', 'unreadable')
            measured = c.copy_fit_measurements(rows, script, geometry,
                SimpleNamespace(B=SimpleNamespace(measure=c.measure)))
            report = r.audit_reserve_pixels(rows, geometry, measured)
            self.assertEqual(report['minimum_light_fraction'], 1)
            rect = report['lines'][0]['source_pixel_rect']
            with Image.open(rows[0]['path']) as image:
                ImageDraw.Draw(image).rectangle([rect[0], rect[1], rect[0] + 15, rect[3] - 1], fill='black')
                image.save(rows[0]['path'])
            with self.assertRaisesRegex(ValueError, 'nonblank art'):
                r.audit_reserve_pixels(rows, geometry, measured)


SCRIPT = """# Horse of the Servant, graphic novel V15

## Chapter 2: Test Chapter

## PAGE 1

Two panels.

**1.1** Wide panel. The cellar before dawn.

> CAPTION: They woke us under cover of bells.

> JOÃO: Up! Those marked go to the docks.

**1.2** A silent beat.

> *No text.*
"""
PANEL = 'page-01-panel-01'
SILENT = 'page-01-panel-02'
BOXES = [(60, 30, 560, 150), (660, 40, 1140, 150)]
BASE_PROMPT = 'V15 graphic novel panel page-01-panel-01. Reserve exactly 2 blank outlined text area(s).'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class PackageCase(unittest.TestCase):
    """A tiny prepared chapter package inside a temporary V15, so the real chapters/ stay untouched."""

    SCRIPT_TEXT = SCRIPT

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.v15 = self.root / 'v15'
        patch = mock.patch.object(r, 'V15', self.v15)
        patch.start()
        self.addCleanup(patch.stop)
        self.pkg = self.v15 / 'chapters' / 'ch02-test'
        (self.pkg / 'prompts').mkdir(parents=True)
        self.script = self.root / 'CHAPTER-02-SCRIPT.md'
        self.script.write_text(self.SCRIPT_TEXT, encoding='utf-8')
        self.continuity = self.root / 'CONTINUITY.md'
        self.continuity.write_text('continuity', encoding='utf-8')
        self.lock = self.root / 'LOCK.json'
        self.lock.write_text('{}', encoding='utf-8')
        jobs = []
        for panel in (PANEL, SILENT):
            prompt = self.pkg / 'prompts' / f'{panel}.txt'
            prompt.write_text(BASE_PROMPT.replace(PANEL, panel) + '\n', encoding='utf-8')
            jobs.append({'id': panel, 'cast': [], 'prompt_path': str(prompt), 'prompt_sha256': sha(prompt),
                         'reference_image_sha256': {}})
        (self.pkg / 'IMAGEGEN-JOBS.json').write_text(json.dumps({
            'script': {'path': str(self.script), 'sha256': sha(self.script)},
            'continuity': {'path': str(self.continuity), 'sha256': sha(self.continuity)},
            'character_lock': {'path': str(self.lock), 'sha256': sha(self.lock)},
            'jobs': jobs}), encoding='utf-8')

    def run_cli(self, *argv, chapter='2'):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            r.main([argv[0], '--chapter', chapter, '--package-dir', str(self.pkg), *argv[1:]])
        return json.loads(out.getvalue()) if out.getvalue().strip() else None

    def generated(self, name, boxes=BOXES, size=(1200, 500)):
        from test_reserves import frame
        path = self.root / name
        frame(size=size, boxes=boxes).save(path)
        return path

    def capture(self, generated, panel=PANEL, *extra):
        return self.run_cli('capture', '--frame-id', panel, '--generated', str(generated), *extra)

    def candidate_path(self, panel=PANEL, version='v01'):
        return self.pkg / 'candidates' / f'{panel}-{version}.json'

    def test_v1_load_job_without_art_direction_needs_no_v2_keys(self):
        job = r.load_job(self.pkg)
        self.assertNotIn('prompt_profile', job)
        self.assertNotIn('art_direction', job)


class ScriptRevisionTests(PackageCase):
    """accept-script-revision: an author's change to a script's directions is accepted when the lettering is untouched."""

    def freeze(self):
        (self.pkg / 'SCRIPT-SOURCE.md').write_text(self.script.read_text(encoding='utf-8'), encoding='utf-8')

    def fails(self, *argv):
        with self.assertRaises(SystemExit) as caught:
            self.run_cli(*argv)
        return str(caught.exception.code)

    def test_a_direction_change_is_refused_until_accepted_and_then_loads(self):
        self.freeze()
        self.script.write_text(self.SCRIPT_TEXT.replace('The cellar before dawn.', 'The cellar before dawn, men bare-chested.'),
                               encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Input changed since preparation'):
            r.load_job(self.pkg)
        result = self.run_cli('accept-script-revision', '--reason', 'author: the men are bare-chested')
        self.assertEqual(result['accepted'], sha(self.script))
        revisions = json.loads((self.pkg / 'SCRIPT-REVISIONS.json').read_text())
        self.assertEqual(revisions[-1]['sha256'], sha(self.script))
        self.assertEqual(revisions[-1]['reason'], 'author: the men are bare-chested')
        r.load_job(self.pkg)                                                   # no longer refused
        # A later, unaccepted change is refused again.
        self.script.write_text(self.script.read_text(encoding='utf-8') + '\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Input changed since preparation'):
            r.load_job(self.pkg)

    def test_a_second_revision_is_appended_and_both_load(self):
        # Chapter 4 had its costume revision accepted; a later direction change ('full width' on 4.1) failed because
        # the revisions file could only be created, never added to.
        self.freeze()
        self.script.write_text(self.SCRIPT_TEXT.replace('The cellar before dawn.', 'The cellar before dawn, men bare-chested.'),
                               encoding='utf-8')
        first = self.run_cli('accept-script-revision', '--reason', 'first')
        self.script.write_text(self.script.read_text(encoding='utf-8').replace('A silent beat.', 'A silent beat, full width.'),
                               encoding='utf-8')
        second = self.run_cli('accept-script-revision', '--reason', 'second')
        revisions = json.loads((self.pkg / 'SCRIPT-REVISIONS.json').read_text())
        self.assertEqual([entry['reason'] for entry in revisions], ['first', 'second'])
        self.assertEqual([entry['sha256'] for entry in revisions], [first['accepted'], second['accepted']])
        self.assertEqual(second['revisions'], 2)
        r.load_job(self.pkg)                                                   # the latest revision loads

    def test_a_change_to_the_lettering_or_the_panels_is_never_accepted(self):
        self.freeze()
        for changed in (self.SCRIPT_TEXT.replace('Up! Those marked', 'Up! All of you'),            # copy
                        self.SCRIPT_TEXT.replace('> CAPTION: They woke us under cover of bells.\n\n', ''),  # a chunk gone
                        self.SCRIPT_TEXT.replace('**1.2** A silent beat.', '')):                    # a panel gone
            with self.subTest(changed=changed[-60:]):
                self.script.write_text(changed, encoding='utf-8')
                message = self.fails('accept-script-revision', '--reason', 'x')
                self.assertIn('lettering', message)
                self.assertFalse((self.pkg / 'SCRIPT-REVISIONS.json').exists())

    def test_a_wording_trim_needs_allow_lettering_and_is_logged(self):
        # Chapter 7 page 12 was too full to letter; the author shortens lines, and only the text may change.
        self.freeze()
        self.script.write_text(self.SCRIPT_TEXT.replace('Up! Those marked go to the docks.', 'Up! To the docks.'),
                               encoding='utf-8')
        message = self.fails('accept-script-revision', '--reason', 'author trims')
        self.assertIn('--allow-lettering', message)
        self.assertFalse((self.pkg / 'SCRIPT-REVISIONS.json').exists())
        result = self.run_cli('accept-script-revision', '--reason', 'author trims', '--allow-lettering')
        entry = json.loads((self.pkg / 'SCRIPT-REVISIONS.json').read_text())[-1]
        self.assertEqual(entry['sha256'], result['accepted'])
        self.assertEqual(entry['lettering_changes'], [{'panel': PANEL, 'chunk': 1, 'speaker': 'JOÃO',
                                                       'before': 'Up! Those marked go to the docks.',
                                                       'after': 'Up! To the docks.'}])
        self.assertEqual(result['lettering_changes'], 1)
        r.load_job(self.pkg)

    def test_allow_lettering_still_refuses_panel_balloon_and_speaker_changes(self):
        self.freeze()
        for changed in (self.SCRIPT_TEXT.replace('> CAPTION: They woke us under cover of bells.\n\n', ''),  # a chunk gone
                        self.SCRIPT_TEXT.replace('**1.2** A silent beat.', ''),                     # a panel gone
                        self.SCRIPT_TEXT.replace('> JOÃO: Up!', '> GUARD: Up!')):                   # a new speaker
            with self.subTest(changed=changed[-60:]):
                self.script.write_text(changed, encoding='utf-8')
                message = self.fails('accept-script-revision', '--reason', 'x', '--allow-lettering')
                self.assertIn('panels, balloons or speakers', message)
                self.assertFalse((self.pkg / 'SCRIPT-REVISIONS.json').exists())

    def test_allow_lettering_refuses_dashes_in_the_new_text(self):
        self.freeze()
        for dash in (chr(0x2014), chr(0x2013)):
            with self.subTest(dash=hex(ord(dash))):
                self.script.write_text(self.SCRIPT_TEXT.replace('Up! Those marked', 'Up' + dash + 'those marked'),
                                       encoding='utf-8')
                self.assertIn('dash', self.fails('accept-script-revision', '--reason', 'x', '--allow-lettering'))
                self.assertFalse((self.pkg / 'SCRIPT-REVISIONS.json').exists())

    def test_allow_lettering_applies_only_to_accept_script_revision(self):
        with self.assertRaises(SystemExit):
            self.run_cli('verify', '--revision', 'r1', '--allow-lettering')

    def test_it_needs_the_frozen_original_and_a_reason(self):
        self.script.write_text(self.SCRIPT_TEXT.replace('A silent beat.', 'A silent beat, rain.'), encoding='utf-8')
        self.assertIn('SCRIPT-SOURCE.md', self.fails('accept-script-revision', '--reason', 'x'))
        (self.pkg / 'SCRIPT-SOURCE.md').write_text('not the original', encoding='utf-8')
        self.assertIn('does not match', self.fails('accept-script-revision', '--reason', 'x'))
        self.freeze_from = None
        (self.pkg / 'SCRIPT-SOURCE.md').write_text(self.SCRIPT_TEXT, encoding='utf-8')
        self.assertIn('--reason', self.fails('accept-script-revision'))


class RecordedArtDirectionTests(PackageCase):
    def _job_data(self):
        return json.loads((self.pkg / 'IMAGEGEN-JOBS.json').read_text(encoding='utf-8'))

    def test_load_job_checks_recorded_art_direction_hash(self):
        import script_pipeline as s
        sidecar = self.root / 'pilot-direction.json'
        sidecar.write_text('draft v1\n', encoding='utf-8')
        jobs_path = self.pkg / 'IMAGEGEN-JOBS.json'
        data = json.loads(jobs_path.read_text(encoding='utf-8'))
        data['art_direction'] = {'path': str(sidecar), 'sha256': s.sha256(sidecar)}
        jobs_path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        sidecar.write_text('draft v2\n', encoding='utf-8')
        (self.pkg / 'ART-DIRECTION-SNAPSHOT.json').write_text('draft v1\n', encoding='utf-8')
        r.load_job(self.pkg)
        (self.pkg / 'ART-DIRECTION-SNAPSHOT.json').write_text('draft v0\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Input changed since preparation'):
            r.load_job(self.pkg)

    def test_v2_load_job_requires_art_direction_record(self):
        jobs_path = self.pkg / 'IMAGEGEN-JOBS.json'
        data = self._job_data()
        data['prompt_profile'] = 'v2'
        jobs_path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'art_direction'):
            r.load_job(self.pkg)

    def test_load_job_rejects_unknown_prompt_profile(self):
        jobs_path = self.pkg / 'IMAGEGEN-JOBS.json'
        data = self._job_data()
        data['prompt_profile'] = 'v99'
        jobs_path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'prompt_profile'):
            r.load_job(self.pkg)

    def test_missing_art_direction_source_uses_matching_snapshot(self):
        import script_pipeline as s
        sidecar = self.root / 'pilot-direction.json'
        sidecar.write_text('draft v1\n', encoding='utf-8')
        data = self._job_data()
        data['art_direction'] = {'path': str(sidecar), 'sha256': s.sha256(sidecar)}
        (self.pkg / 'ART-DIRECTION-SNAPSHOT.json').write_text('draft v1\n', encoding='utf-8')
        sidecar.unlink()
        (self.pkg / 'IMAGEGEN-JOBS.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        r.load_job(self.pkg)


class AutoGeometryTests(PackageCase):
    def auto(self, candidate, name='geometry.json'):
        geometry = self.root / name
        result = self.run_cli('auto-geometry', '--candidate', str(candidate), '--geometry-out', str(geometry))
        return geometry, result

    def test_writes_geometry_that_select_accepts_and_the_build_audits_pass(self):
        import compositor as c
        import script_pipeline as s
        self.capture(self.generated('a.png'))
        self.capture(self.generated('silent.png', boxes=[]), SILENT)
        geometry, result = self.auto(self.candidate_path())
        data = json.loads(geometry.read_text())
        self.assertEqual(data['visible_rect'], [0, 0, 1200, 500])
        self.assertNotIn('art_rect', data)                      # the inset path does not crop
        self.assertEqual([x['kind'] for x in data['reserves']], ['caption', 'speech'])
        self.assertEqual([x['copy_indices'] for x in data['reserves']], [[0], [1]])
        self.assertNotIn('style', json.dumps(data))
        self.assertEqual(result['geometry_out'], str(geometry))
        silent, _ = self.auto(self.candidate_path(SILENT), 'silent.json')
        self.assertEqual(json.loads(silent.read_text()), {'visible_rect': [0, 0, 1200, 500], 'reserves': []})
        for panel, path in ((PANEL, geometry), (SILENT, silent)):
            self.run_cli('select', '--candidate', str(self.candidate_path(panel)), '--geometry', str(path),
                         '--reviewer', 'Test', '--review-note', 'Blank reserves visually passed.')
        job = r.load_job(self.pkg)
        script = s.parse_script(Path(job['script']['path']))
        rows = r.selected_rows(self.pkg, job)
        c.validate_selection(rows, script, self.pkg)
        layout = c.geometry_for_script(script)
        measured = c.copy_fit_measurements(rows, script, layout, SimpleNamespace(B=SimpleNamespace(measure=c.measure)))
        self.assertEqual(r.audit_reserve_pixels(rows, layout, measured)['status'], 'pass')

    def test_fails_cleanly_when_a_reserve_is_too_small_for_its_text(self):
        self.capture(self.generated('small.png', boxes=[BOXES[0], (900, 40, 1010, 110)]))
        geometry = self.root / 'geometry.json'
        with self.assertRaises(SystemExit) as caught:
            self.run_cli('auto-geometry', '--candidate', str(self.candidate_path()), '--geometry-out', str(geometry))
        message = str(caught.exception.code)
        self.assertIn('does not fit', message)
        self.assertIn('chunk 1', message)
        self.assertIn(PANEL, message)
        self.assertFalse(geometry.exists())

    def test_inset_option_rescues_a_reserve_that_is_a_few_points_short(self):
        # Shallow boxes: the default 6 px inset leaves too little height for a line; 2 px is enough.
        self.capture(self.generated('shallow.png', boxes=[(60, 30, 560, 80), (660, 40, 1140, 90)]))
        candidate = str(self.candidate_path())
        geometry = self.root / 'default.json'
        with self.assertRaises(SystemExit) as caught:
            self.run_cli('auto-geometry', '--candidate', candidate, '--geometry-out', str(geometry))
        self.assertIn('does not fit', str(caught.exception.code))
        self.assertFalse(geometry.exists())
        result = self.run_cli('auto-geometry', '--candidate', candidate,
                              '--geometry-out', str(self.root / 'two.json'), '--inset', '2')
        self.assertEqual(result['inset_px'], 2)
        self.assertTrue((self.root / 'two.json').is_file())
        with self.assertRaises(SystemExit):
            self.run_cli('auto-geometry', '--candidate', candidate,
                         '--geometry-out', str(self.root / 'bad.json'), '--inset', '99')
        self.assertFalse((self.root / 'bad.json').exists())
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.run_cli('next-job', '--inset', '2')

    def test_wrong_number_of_blank_areas_fails_cleanly(self):
        self.capture(self.generated('one.png', boxes=[BOXES[0]]))
        geometry = self.root / 'geometry.json'
        with self.assertRaises(SystemExit) as caught:
            self.run_cli('auto-geometry', '--candidate', str(self.candidate_path()), '--geometry-out', str(geometry))
        self.assertIn('found 1', str(caught.exception.code))
        self.assertFalse(geometry.exists())

    def test_refuses_to_overwrite_an_existing_geometry_file(self):
        self.capture(self.generated('a.png'))
        geometry = self.root / 'geometry.json'
        geometry.write_text('keep me')
        with self.assertRaises(SystemExit) as caught:
            self.run_cli('auto-geometry', '--candidate', str(self.candidate_path()), '--geometry-out', str(geometry))
        self.assertIn('exists', str(caught.exception.code))
        self.assertEqual(geometry.read_text(), 'keep me')

    def test_requires_candidate_and_geometry_out_and_a_known_panel(self):
        self.capture(self.generated('a.png'))
        with self.assertRaises(SystemExit) as caught:
            self.run_cli('auto-geometry', '--candidate', str(self.candidate_path()))
        self.assertIn('--geometry-out', str(caught.exception.code))
        stranger = self.root / 'stranger.json'
        record = json.loads(self.candidate_path().read_text())
        record['id'] = 'page-09-panel-09'
        stranger.write_text(json.dumps(record))
        with self.assertRaises(SystemExit) as caught:
            self.run_cli('auto-geometry', '--candidate', str(stranger), '--geometry-out', str(self.root / 'g.json'))
        self.assertIn('page-09-panel-09', str(caught.exception.code))
        self.assertFalse((self.root / 'g.json').exists())

    def test_honours_the_chapter_layout_page_rows(self):
        # The same frame fits at the default row height but not in a much shorter slot.
        self.capture(self.generated('a.png'))
        ok, _ = self.auto(self.candidate_path(), 'default.json')
        self.assertTrue(ok.exists())
        (self.pkg / 'LAYOUT.json').write_text(json.dumps({'page_rows': {'1': [30, 491.5]}}))
        tight = self.root / 'tight.json'
        with self.assertRaises(SystemExit) as caught:
            self.run_cli('auto-geometry', '--candidate', str(self.candidate_path()), '--geometry-out', str(tight))
        self.assertIn('does not fit', str(caught.exception.code))
        self.assertFalse(tight.exists())

    def test_layout_option_overrides_the_chapter_layout(self):
        # --layout names the rows to place against, so a fitted layout can be tried before LAYOUT.json changes.
        self.capture(self.generated('a.png'))
        ok, _ = self.auto(self.candidate_path(), 'default.json')
        self.assertTrue(ok.exists())
        tight = self.root / 'tight-layout.json'
        tight.write_text(json.dumps({'page_rows': {'1': [30, 491.5]}}))
        geometry = self.root / 'tight.json'
        with self.assertRaises(SystemExit) as caught:
            self.run_cli('auto-geometry', '--candidate', str(self.candidate_path()), '--geometry-out', str(geometry),
                         '--layout', str(tight))
        self.assertIn('does not fit', str(caught.exception.code))
        self.assertFalse(geometry.exists())
        # A package LAYOUT.json that is too tight is overridden by a roomy --layout.
        (self.pkg / 'LAYOUT.json').write_text(json.dumps({'page_rows': {'1': [30, 491.5]}}))
        roomy = self.root / 'roomy-layout.json'
        roomy.write_text(json.dumps({'page_rows': {'1': [261.75, 259.75]}}))
        result = self.run_cli('auto-geometry', '--candidate', str(self.candidate_path()),
                              '--geometry-out', str(self.root / 'roomy.json'), '--layout', str(roomy))
        self.assertTrue((self.root / 'roomy.json').is_file())
        self.assertEqual(result['panel'], PANEL)

    def test_existing_commands_still_work_and_new_flags_are_scoped(self):
        self.assertEqual(self.run_cli('next-job')['id'], PANEL)
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                r.main(['bogus', '--chapter', '2'])
            with self.assertRaises(SystemExit):
                self.run_cli('next-job', '--geometry-out', str(self.root / 'g.json'))
            with self.assertRaises(SystemExit):
                self.run_cli('next-job', '--prompt', str(self.root / 'p.txt'))


class CapturePromptTests(PackageCase):
    def job(self, panel=PANEL):
        return next(j for j in r.load_job(self.pkg)['jobs'] if j['id'] == panel)

    def revised(self, extra='\nCORRECTION: keep the hands visible.\n', name='revised.txt'):
        path = self.root / name
        path.write_text(BASE_PROMPT + '\n' + extra, encoding='utf-8')
        return path

    def test_capture_without_prompt_is_unchanged(self):
        record = self.capture(self.generated('a.png'))
        job = self.job()
        self.assertEqual(record['prompt_path'], job['prompt_path'])
        self.assertEqual(record['prompt_sha256'], job['prompt_sha256'])
        self.assertNotIn('base_prompt_path', record)
        self.assertNotIn('base_prompt_sha256', record)
        self.assertEqual(json.loads(self.candidate_path().read_text()), record)

    def test_moderated_rewrite_needs_the_flag_and_is_recorded(self):
        softened = self.root / 'softened.txt'
        softened.write_text('A calm scene, softened after a moderation refusal.\n', encoding='utf-8')
        with self.assertRaises(Exception):
            self.capture(self.generated('a.png'), PANEL, '--prompt', str(softened))
        record = self.capture(self.generated('b.png'), PANEL, '--prompt', str(softened), '--moderated')
        job = self.job()
        self.assertTrue(record['moderated_rewrite'])
        self.assertEqual(record['prompt_path'], str(softened.resolve()))
        self.assertEqual(record['base_prompt_path'], job['prompt_path'])

    def test_capture_skips_an_orphan_frame_without_a_record(self):
        orphan = self.pkg / 'frames' / f'{PANEL}-v01.png'
        orphan.parent.mkdir(parents=True, exist_ok=True)
        orphan.write_bytes(b'left by an earlier run')
        record = self.capture(self.generated('a.png'))
        self.assertTrue(record['path'].endswith(f'{PANEL}-v02.png'))
        self.assertEqual(orphan.read_bytes(), b'left by an earlier run')

    def test_capture_with_prompt_records_the_revised_prompt_and_keeps_the_base(self):
        revised = self.revised()
        record = self.capture(self.generated('a.png'), PANEL, '--prompt', str(revised))
        job = self.job()
        self.assertEqual(record['prompt_path'], str(revised.resolve()))
        self.assertEqual(record['prompt_sha256'], sha(revised))
        self.assertEqual(record['base_prompt_path'], job['prompt_path'])
        self.assertEqual(record['base_prompt_sha256'], job['prompt_sha256'])
        self.assertEqual(json.loads(self.candidate_path().read_text()), record)

    def test_prompt_identical_to_the_prepared_prompt_is_accepted(self):
        same = self.root / 'same.txt'
        same.write_text(Path(self.job()['prompt_path']).read_text(encoding='utf-8'), encoding='utf-8')
        record = self.capture(self.generated('a.png'), PANEL, '--prompt', str(same))
        self.assertEqual(record['prompt_sha256'], self.job()['prompt_sha256'])

    def test_prompt_that_does_not_begin_with_the_prepared_prompt_is_refused(self):
        bad = self.root / 'bad.txt'
        bad.write_text('CORRECTION first.\n' + BASE_PROMPT + '\n', encoding='utf-8')
        edited = self.root / 'edited.txt'
        edited.write_text(BASE_PROMPT.replace('2 blank', '3 blank') + '\n', encoding='utf-8')
        for path in (bad, edited, self.root / 'missing.txt'):
            with self.assertRaises(ValueError, msg=path.name):
                self.capture(self.generated('a.png'), PANEL, '--prompt', str(path))
        # Refusal happens before anything is written.
        self.assertFalse(list((self.pkg / 'candidates').glob('*')) if (self.pkg / 'candidates').exists() else [])
        self.assertFalse(list((self.pkg / 'frames').glob('*')) if (self.pkg / 'frames').exists() else [])

    def _install_v2_base_prompt(self):
        base = BASE_PROMPT + "\n\nSETTING (this panel): a dark cellar."
        prompt_path = Path(self.job()['prompt_path'])
        prompt_path.write_text(base + "\n", encoding='utf-8')
        jobs_path = self.pkg / 'IMAGEGEN-JOBS.json'
        data = json.loads(jobs_path.read_text(encoding='utf-8'))
        item = next(item for item in data['jobs'] if item['id'] == PANEL)
        item['prompt_sha256'] = sha(prompt_path)
        data['prompt_profile'] = 'v2'
        sidecar = self.root / 'CHAPTER-02-ART-DIRECTION.json'
        sidecar.write_text('{}\n', encoding='utf-8')
        data['art_direction'] = {'path': str(sidecar), 'sha256': sha(sidecar)}
        (self.pkg / 'ART-DIRECTION-SNAPSHOT.json').write_text('{}\n', encoding='utf-8')
        jobs_path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        return base

    def test_revised_prompt_must_repeat_original_setting_at_the_end(self):
        base = self._install_v2_base_prompt()
        missing = self.root / 'missing-setting.txt'
        missing.write_text(base + "\nCORRECTION: keep the hands visible.\n", encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'SETTING'):
            self.capture(self.generated('a.png'), PANEL, '--prompt', str(missing))
        complete = self.root / 'complete-setting.txt'
        complete.write_text(
            base + "\nCORRECTION: keep the hands visible.\n\nSETTING (this panel): a dark cellar.\n",
            encoding='utf-8')
        record = self.capture(self.generated('b.png'), PANEL, '--prompt', str(complete))
        self.assertEqual(record['prompt_path'], str(complete.resolve()))

    def test_moderated_rewrite_must_repeat_original_setting_at_the_end(self):
        base = self._install_v2_base_prompt()
        missing = self.root / 'moderated-missing-setting.txt'
        missing.write_text('A calm scene after moderation.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'SETTING'):
            self.capture(self.generated('a.png'), PANEL, '--prompt', str(missing), '--moderated')
        complete = self.root / 'moderated-complete-setting.txt'
        complete.write_text(
            'A calm scene after moderation.\n\nSETTING (this panel): a dark cellar.\n',
            encoding='utf-8')
        record = self.capture(self.generated('b.png'), PANEL, '--prompt', str(complete), '--moderated')
        self.assertTrue(record['moderated_rewrite'])

    def test_v2_revised_setting_must_be_a_separate_final_paragraph(self):
        base = self._install_v2_base_prompt()
        joined = self.root / 'joined-setting.txt'
        joined.write_text(base + "\nCORRECTION: keep the hands visible. SETTING (this panel): a dark cellar.\n",
                          encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'SETTING'):
            self.capture(self.generated('a.png'), PANEL, '--prompt', str(joined))

    def test_v2_revised_prompt_rejects_em_and_en_dashes(self):
        base = self._install_v2_base_prompt()
        for mark in ('\u2014', '\u2013'):
            with self.subTest(mark=mark):
                path = self.root / 'dashed.txt'
                path.write_text(base + f"\nCORRECTION: keep the hands {mark} visible.\n\n"
                                "SETTING (this panel): a dark cellar.\n", encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'dash'):
                    self.capture(self.generated('a.png'), PANEL, '--prompt', str(path))

    def test_select_and_validate_selection_accept_a_candidate_captured_with_prompt(self):
        import compositor as c
        import script_pipeline as s
        self.capture(self.generated('a.png'), PANEL, '--prompt', str(self.revised()))
        self.capture(self.generated('silent.png', boxes=[]), SILENT)
        for panel in (PANEL, SILENT):
            geometry = self.root / f'{panel}.json'
            self.run_cli('auto-geometry', '--candidate', str(self.candidate_path(panel)),
                         '--geometry-out', str(geometry))
            self.run_cli('select', '--candidate', str(self.candidate_path(panel)), '--geometry', str(geometry),
                         '--reviewer', 'Test', '--review-note', 'Passed.')
        job = r.load_job(self.pkg)
        script = s.parse_script(Path(job['script']['path']))
        rows = r.selected_rows(self.pkg, job)
        c.validate_selection(rows, script, self.pkg)
        self.assertIn('base_prompt_sha256', rows[0])
        # A revised prompt that changes afterwards is caught like any prompt drift.
        Path(rows[0]['prompt_path']).write_text('tampered', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Prompt hash mismatch'):
            c.validate_selection(rows, script, self.pkg)


LONG_SCRIPT = SCRIPT.replace(
    'They woke us under cover of bells.',
    'They woke us under cover of bells, and the whole dark hold went silent at once, every chained man '
    'listening for the count.').replace(
    'Up! Those marked go to the docks.',
    'Up! Those marked go to the docks, and be quick about it, you lazy lot, before the tide turns against us.')
PAINTED = [(120, 60, 800, 200), (1520, 80, 2200, 220)]      # painted boxes, far too small for LONG_SCRIPT
BIG = (2400, 1000)
SILENT_BIG = (3000, 1250)     # same shape; a silent panel is cropped to its slot too, which magnifies it: it needs the pixels for 300 PPI


class DrawnAutoGeometryTests(PackageCase):
    """auto-geometry --draw: the compositor draws the balloons, so the painted ones only mark the spot."""

    SCRIPT_TEXT = LONG_SCRIPT

    def candidate(self, boxes=PAINTED, name='big.png', panel=PANEL):
        self.capture(self.generated(name, boxes=boxes, size=BIG), panel)
        return str(self.candidate_path(panel))

    def write_tails(self, value, name='tails.json'):
        path = self.root / name
        path.write_text(json.dumps(value))
        return str(path)

    def draw(self, candidate, tails, geometry='drawn.json', *extra):
        out = self.root / geometry
        result = self.run_cli('auto-geometry', '--candidate', candidate, '--geometry-out', str(out),
                              '--draw', '--tails', tails, *extra)
        return out, result

    def fails(self, *argv):
        with self.assertRaises(SystemExit) as caught:
            self.run_cli('auto-geometry', *argv)
        return str(caught.exception.code)

    def test_styles_size_their_chunk_for_its_lettering_and_are_written_into_the_geometry(self):
        # A styled chunk wraps differently (unreadable strokes), so its box must be sized for the style the
        # build will measure, and only that chunk may carry it.
        import compositor as c
        import script_pipeline as s
        from types import SimpleNamespace
        candidate = self.candidate()
        styles = self.write_tails({'1': 'unreadable'}, 'styles.json')
        out, _ = self.draw(candidate, self.write_tails({'1': [0.5, 0.95]}), 'styled.json', '--styles', styles)
        caption, speech = json.loads(out.read_text())['reserves']
        self.assertNotIn('style', caption)
        self.assertEqual(speech['style'], 'unreadable')
        row = json.loads(Path(candidate).read_text())
        row.update(json.loads(out.read_text()))
        script = s.parse_script(Path(r.load_job(self.pkg)['script']['path']))
        geometry = c.geometry_for_script(script, None)
        measured = c.copy_fit_measurements([row], script, geometry, SimpleNamespace(B=SimpleNamespace(measure=c.measure)),
                                           reject_failures=False)
        self.assertTrue(all(m['fits'] for m in measured))
        for bad in ({'1': 'bold'}, {'5': 'unreadable'}):
            with self.subTest(bad=bad):
                self.assertIn('--styles', self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'bad.json'),
                                                     '--draw', '--tails', self.write_tails({'1': [0.5, 0.95]}, 't.json'),
                                                     '--styles', self.write_tails(bad, 'bad-styles.json')))
        self.assertIn('--draw', self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'nodraw.json'),
                                           '--styles', styles))

    def test_draw_covers_the_painted_boxes_and_fits_text_that_failed_before(self):
        import compositor as c
        import script_pipeline as s
        candidate = self.candidate()
        self.assertIn('does not fit', self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'plain.json')))
        out, result = self.draw(candidate, self.write_tails({'1': [0.5, 0.95]}))
        geometry = json.loads(out.read_text())
        caption, speech = geometry['reserves']
        self.assertEqual((caption['kind'], caption['draw'], speech['kind'], speech['draw']),
                         ('caption', 'caption', 'speech', 'speech'))
        self.assertNotIn('tail', caption)
        self.assertEqual(speech['tail'], [1200, 950])
        self.assertEqual([caption['copy_indices'], speech['copy_indices']], [[0], [1]])
        self.assertNotIn('style', json.dumps(geometry))
        for reserve, painted in zip(geometry['reserves'], PAINTED):
            x0, y0, x1, y1 = reserve['rect']
            self.assertTrue(x0 <= painted[0] and y0 <= painted[1] and x1 >= painted[2] and y1 >= painted[3])
            self.assertTrue(0 <= x0 < x1 <= 2400 and 0 <= y0 < y1 <= 1000)
        self.assertTrue(separate_boxes(caption['rect'], speech['rect']))
        self.assertEqual(result['draw'], True)
        self.assertEqual(result['partly_covered'], [])
        # The candidate is accepted end to end: select, validate_selection, fit, audit and a verified PDF.
        self.capture(self.generated('silent.png', boxes=[], size=SILENT_BIG), SILENT)
        silent, _ = self.draw(str(self.candidate_path(SILENT)), self.write_tails([]), 'silent.json')
        self.assertEqual(json.loads(silent.read_text())['reserves'], [])
        for panel, path in ((PANEL, out), (SILENT, silent)):
            self.run_cli('select', '--candidate', str(self.candidate_path(panel)), '--geometry', str(path),
                         '--reviewer', 'Test', '--review-note', 'Drawn balloons visually passed.')
        job = r.load_job(self.pkg)
        script = s.parse_script(Path(job['script']['path']))
        rows = r.selected_rows(self.pkg, job)
        c.validate_selection(rows, script, self.pkg)
        layout = c.geometry_for_script(script)
        measured = c.copy_fit_measurements(rows, script, layout, SimpleNamespace(B=SimpleNamespace(measure=c.measure)))
        self.assertTrue(all(m['fits'] for m in measured))
        self.assertEqual(r.audit_reserve_pixels(rows, layout, measured)['line_count'], 0)
        pdf = self.root / 'drawn.pdf'
        composition = c.compose(rows, script, layout, pdf, chapter=2)
        self.assertEqual(c.verify_pdf(pdf, rows, script, composition['placements'])['script_chunks_verified'], 2)

    def test_draw_writes_the_cover_crop_as_visible_rect_and_the_uncropped_art_as_art_rect(self):
        candidate = self.candidate()
        out, result = self.draw(candidate, self.write_tails({'1': [0.5, 0.95]}))
        geometry = json.loads(out.read_text())
        self.assertEqual(geometry['art_rect'], [0, 0, 2400, 1000])
        x0, y0, x1, y1 = geometry['visible_rect']
        self.assertEqual((y0, y1), (0, 1000))                                # the slot is taller than the art: the width is cropped
        self.assertGreater(x0, 0)
        self.assertLess(x1, 2400)
        for painted in PAINTED:                                              # both painted boxes are kept whole
            self.assertTrue(x0 <= painted[0] and painted[2] <= x1)
        for index, reserve in enumerate(geometry['reserves']):              # a balloon may bleed past an edge its painted box touches
            rx0, ry0, rx1, ry1 = reserve['rect']
            left, top, right, bottom = (result['bleeds'] or {}).get(str(index), [0, 0, 0, 0])
            self.assertTrue(x0 - left <= rx0 < rx1 <= x1 + right and y0 - top <= ry0 < ry1 <= y1 + bottom)
            self.assertTrue(rx0 >= x0 - 12 and rx1 <= x1 + 12)
        self.assertEqual(result['visible_rect'], geometry['visible_rect'])
        self.assertEqual(geometry['reserves'][1]['tail'], [1200, 950])
        # A crop goes through select, validation and the build like any visible_rect, and the row keeps the art rect.
        import compositor as c
        import script_pipeline as s
        self.capture(self.generated('silent.png', boxes=[], size=SILENT_BIG), SILENT)
        silent, _ = self.draw(str(self.candidate_path(SILENT)), self.write_tails([]), 'silent.json')
        self.assertEqual(json.loads(silent.read_text())['art_rect'], [0, 0, 3000, 1250])
        for panel, path in ((PANEL, out), (SILENT, silent)):
            self.run_cli('select', '--candidate', str(self.candidate_path(panel)), '--geometry', str(path),
                         '--reviewer', 'Test', '--review-note', 'Cropped balloons visually passed.')
        job = r.load_job(self.pkg)
        script = s.parse_script(Path(job['script']['path']))
        rows = r.selected_rows(self.pkg, job)
        self.assertEqual([row['art_rect'] for row in rows], [[0, 0, 2400, 1000], [0, 0, 3000, 1250]])
        c.validate_selection(rows, script, self.pkg)
        layout = c.geometry_for_script(script)
        measured = c.copy_fit_measurements(rows, script, layout, SimpleNamespace(B=SimpleNamespace(measure=c.measure)))
        self.assertTrue(all(m['fits'] for m in measured))
        pdf = self.root / 'cropped.pdf'
        composition = c.compose(rows, script, layout, pdf, chapter=2)
        self.assertEqual(c.verify_pdf(pdf, rows, script, composition['placements'])['script_chunks_verified'], 2)

    def test_audit_skips_drawn_reserves_and_still_checks_painted_ones(self):
        import compositor as c
        from test_compositor import drawn_fixture, CAPTION
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            rows, script, geometry = drawn_fixture(tmp, 'Short.', CAPTION)
            v14 = SimpleNamespace(B=SimpleNamespace(measure=c.measure))
            measured = c.copy_fit_measurements(rows, script, geometry, v14)
            report = r.audit_reserve_pixels(rows, geometry, measured)
            self.assertEqual((report['status'], report['line_count']), ('pass', 0))
            rows[0]['reserves'][0].pop('draw')
            measured = c.copy_fit_measurements(rows, script, geometry, v14)
            with self.assertRaisesRegex(ValueError, 'nonblank art'):
                r.audit_reserve_pixels(rows, geometry, measured)

    def test_every_speech_chunk_needs_a_tail_point_and_nothing_is_guessed(self):
        candidate = self.candidate()
        geometry = self.root / 'g.json'
        base = ['--candidate', candidate, '--geometry-out', str(geometry), '--draw']
        message = self.fails(*base)
        self.assertIn('chunk 1', message)
        self.assertIn('tail', message)
        self.assertIn('--tails', message)
        message = self.fails(*base, '--tails', self.write_tails({}))
        self.assertIn('chunk 1', message)
        self.assertFalse(geometry.exists())
        for bad, expect in (({'1': [1.4, .5]}, 'between 0 and 1'), ({'1': [.5]}, '[x_frac, y_frac]'),
                            ({'0': [.5, .5], '1': [.5, .9]}, 'caption'), ({'5': [.5, .5]}, 'chunk 5'),
                            ('nope', 'list or a map'), ({'1': ['a', .5]}, '[x_frac, y_frac]')):
            with self.subTest(tails=bad):
                self.assertIn(expect, self.fails(*base, '--tails', self.write_tails(bad, 'bad.json')))
        self.assertFalse(geometry.exists())

    def test_tails_can_be_a_list_or_a_map(self):
        candidate = self.candidate()
        by_map, _ = self.draw(candidate, self.write_tails({'1': [.5, .95]}), 'map.json')
        by_list, _ = self.draw(candidate, self.write_tails([None, [.5, .95]], 'list-tails.json'), 'list.json')
        self.assertEqual(json.loads(by_map.read_text()), json.loads(by_list.read_text()))

    def accept(self, out):
        """select both panels, then the same audits and a verified PDF the build performs."""
        import compositor as c
        import script_pipeline as s
        self.capture(self.generated('silent.png', boxes=[], size=SILENT_BIG), SILENT)
        silent, _ = self.draw(str(self.candidate_path(SILENT)), self.write_tails([]), 'silent.json')
        for panel, path in ((PANEL, out), (SILENT, silent)):
            self.run_cli('select', '--candidate', str(self.candidate_path(panel)), '--geometry', str(path),
                         '--reviewer', 'Test', '--review-note', 'Drawn balloons visually passed.')
        job = r.load_job(self.pkg)
        script = s.parse_script(Path(job['script']['path']))
        rows = r.selected_rows(self.pkg, job)
        c.validate_selection(rows, script, self.pkg)
        layout = c.geometry_for_script(script)
        measured = c.copy_fit_measurements(rows, script, layout, SimpleNamespace(B=SimpleNamespace(measure=c.measure)))
        pdf = self.root / 'accepted.pdf'
        composition = c.compose(rows, script, layout, pdf, chapter=2)
        self.assertEqual(c.verify_pdf(pdf, rows, script, composition['placements'])['script_chunks_verified'], 2)
        return measured

    def test_faces_file_is_used_reported_and_validated(self):
        candidate = self.candidate()
        tails = self.write_tails({'1': [.5, .95]})
        faces = self.write_tails([{'x': 1860 / 2400, 'y': .8, 'r': .05, 'name': 'Duarte'}], 'faces.json')
        out, result = self.draw(candidate, tails, 'faced.json', '--faces', faces)
        self.assertEqual(result['face_clearance']['1']['face'] if '1' in result['face_clearance']
                         else result['face_clearance'][1]['face'], 'Duarte')
        self.assertGreater(min(v['px'] for v in result['face_clearance'].values()), 0)
        self.assertIn("head of chunk 1's speaker", ' '.join(result['head_zones']))
        # A face entry that covers the mouth replaces the implied head zone.
        covers = self.write_tails([{'x': .5, 'y': .95, 'r': .05, 'name': 'Nagoji'}], 'covers.json')
        out, result = self.draw(candidate, tails, 'covered.json', '--faces', covers)
        self.assertEqual(result['head_zones'], [])
        # Scoping and validation.
        bad = self.write_tails([{'x': 2, 'y': .5, 'r': .1}], 'bad-faces.json')
        self.assertIn('face', self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'x.json'),
                                         '--draw', '--tails', tails, '--faces', bad))
        self.assertIn('--draw', self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'y.json'),
                                           '--faces', faces))
        self.assertFalse((self.root / 'x.json').exists() or (self.root / 'y.json').exists())
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.run_cli('next-job', '--faces', faces)

    def test_keep_file_holds_the_crop_open_is_reported_and_validated(self):
        candidate = self.candidate()
        tails = self.write_tails({'1': [.5, .95]})
        plain_out, _ = self.draw(candidate, tails, 'plain.json')
        plain = json.loads(plain_out.read_text())['visible_rect']
        self.assertLess(plain[2], 2400 * .96)                          # the tall slot crops the width: the far right is cut
        keep = self.write_tails([{'x0': .96, 'y0': .4, 'x1': .99, 'y1': .6, 'what': 'a gripping hand'}], 'keep.json')
        out, result = self.draw(candidate, tails, 'kept.json', '--keep', keep)
        kept = json.loads(out.read_text())['visible_rect']
        self.assertGreaterEqual(kept[2], round(.99 * 2400))            # the crop now holds the whole zone
        self.assertNotEqual(kept, plain)
        self.assertEqual(result['visible_rect'], kept)
        self.assertEqual(json.loads(out.read_text())['art_rect'], [0, 0, 2400, 1000])
        # Validation and scoping.
        for bad, expect in (({'x0': .1}, 'list'), ([{'x0': .5, 'y0': .4, 'x1': .4, 'y1': .6}], 'x0 below x1'),
                            ([{'x0': -.1, 'y0': .4, 'x1': .4, 'y1': .6}], 'between 0 and 1'), ([{'x0': 'a'}], 'keep zone 0')):
            with self.subTest(keep=bad):
                message = self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'bad.json'), '--draw',
                                     '--tails', tails, '--keep', self.write_tails(bad, 'bad-keep.json'))
                self.assertIn(expect, message)
        self.assertFalse((self.root / 'bad.json').exists())
        self.assertIn('--keep needs --draw', self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'nodraw.json'),
                                                        '--keep', keep))
        self.assertFalse((self.root / 'nodraw.json').exists())
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.run_cli('next-job', '--keep', keep)

    def test_the_output_lists_the_chunks_that_cover_a_keep_zone_and_the_voices_left_without_tail_room(self):
        candidate = self.candidate()
        tails = self.write_tails({'1': [.5, .95]})
        _, plain = self.draw(candidate, tails, 'plain.json')
        self.assertEqual((plain['keep_overlaps'], plain['edge_voice_no_tail']), ({}, []))
        zone = self.write_tails([{'x0': .04, 'y0': .05, 'x1': .35, 'y1': .22, 'what': 'the ledger'}], 'ledger.json')   # under painted box 0
        _, result = self.draw(candidate, tails, 'ledger-kept.json', '--keep', zone)
        self.assertEqual(result['keep_overlaps'], {'0': [0]})                # the caption must hide its painted box, and says so
        self.assertEqual(result['edge_voice_no_tail'], [])

    def test_a_tail_point_right_beside_the_painted_region_now_implies_a_head_it_would_cover(self):
        # Deliberately changed: this used to grow the box away from a mouth 50 px beside the painted balloon.
        # The head the mouth implies (0.09 of the frame height) is larger than that gap, so the painted balloon
        # would cover the speaker's head, and the chunk fails instead. Growing away from a bare tail point is
        # still tested in test_reserves, where no head zone is passed.
        candidate = self.candidate()
        message = self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'g.json'), '--draw',
                             '--tails', self.write_tails({'1': [2250 / 2400, .15]}))
        self.assertIn('would cover a face', message)
        self.assertIn("head of chunk 1's speaker", message)
        self.assertFalse((self.root / 'g.json').exists())
        # With the mouth well clear of the painted balloon the same chunk is placed.
        out, result = self.draw(candidate, self.write_tails({'1': [.5, .95]}), 'clear.json')
        self.assertEqual(result['head_zones'], ["head of chunk 1's speaker"])
        self.assertGreater(result['face_clearance']['1']['px'], 0)

    def test_a_tail_point_inside_the_painted_region_now_fails_because_the_balloon_covers_the_speaker(self):
        # Deliberately changed: this used to leave the region partly covered and report it. A mouth inside the
        # painted balloon means the generated art put the balloon over the speaker's face, so the chunk fails.
        candidate = self.candidate()
        message = self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'g.json'), '--draw',
                             '--tails', self.write_tails({'1': [1860 / 2400, 150 / 1000]}))
        self.assertIn('would cover a face', message)
        self.assertIn('chunk 1', message)
        self.assertFalse((self.root / 'g.json').exists())

    def test_a_tail_point_on_the_frame_edge_never_fails_and_the_page_composes(self):
        touching = [(120, 0, 800, 200), (1520, 0, 2200, 220)]        # painted boxes flush with the top edge
        candidate = self.candidate(boxes=touching, name='touching.png')
        out, result = self.draw(candidate, self.write_tails({'1': [.5, 0.0]}))    # the speaker is above the frame
        self.assertEqual(result['partly_covered'], [])
        geometry = json.loads(out.read_text())
        self.assertEqual(geometry['reserves'][1]['tail'], [1200, 0])
        self.assertEqual(geometry['visible_rect'][1], 0)
        # The box reaches the top edge and may run past it by its reported bleed (the crop changes the scale the planner works at).
        self.assertEqual(geometry['reserves'][1]['rect'][1], -result['bleeds']['1'][1])
        self.accept(out)

    def test_boxes_that_cannot_be_placed_fail_clearly_and_write_nothing(self):
        huge = ' '.join(['Endless words fill this whole balloon and never stop talking about it.'] * 40)
        script = self.root / 'CHAPTER-02-SCRIPT.md'
        text = LONG_SCRIPT.replace('They woke us under cover of bells, and the whole dark hold went silent at once, every chained man listening for the count.', huge)
        text = text.replace('Up! Those marked go to the docks, and be quick about it, you lazy lot, before the tide turns against us.', huge)
        script.write_text(text, encoding='utf-8')
        job_path = self.pkg / 'IMAGEGEN-JOBS.json'
        job = json.loads(job_path.read_text())
        job['script']['sha256'] = sha(script)
        job_path.write_text(json.dumps(job))
        candidate = self.candidate()
        geometry = self.root / 'g.json'
        message = self.fails('--candidate', candidate, '--geometry-out', str(geometry), '--draw',
                             '--tails', self.write_tails({'1': [.5, .95]}))
        self.assertIn('auto-geometry failed', message)
        self.assertIn('chunk', message)
        self.assertFalse(geometry.exists())

    def test_without_painted_regions_boxes_go_in_clear_space_and_fit(self):
        import compositor as c
        candidate = self.candidate(boxes=[], name='bare.png')
        out, result = self.draw(candidate, self.write_tails({'1': [.5, .95]}))
        caption, speech = json.loads(out.read_text())['reserves']
        self.assertTrue(separate_boxes(caption['rect'], speech['rect']))
        for reserve in (caption, speech):
            self.assertTrue(0 <= reserve['rect'][0] and reserve['rect'][2] <= 2400 and 0 <= reserve['rect'][1] and reserve['rect'][3] <= 1000)
        self.assertEqual(result['painted'], [False, False])
        self.assertLess(caption['rect'][1], 500)          # the top half, reading order

    def test_new_flags_are_scoped_to_auto_geometry_draw(self):
        candidate = self.candidate()
        tails = self.write_tails({'1': [.5, .95]})
        with contextlib.redirect_stderr(io.StringIO()):
            for argv in (('next-job', '--draw'), ('next-job', '--tails', tails)):
                with self.subTest(argv=argv), self.assertRaises(SystemExit):
                    self.run_cli(*argv)
        self.assertIn('--draw', self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'a.json'),
                                           '--tails', tails))
        self.assertIn('--inset', self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'b.json'),
                                            '--draw', '--tails', tails, '--inset', '2'))
        # Without --draw, auto-geometry is exactly what it was.
        self.assertIn('does not fit', self.fails('--candidate', candidate, '--geometry-out', str(self.root / 'c.json')))


def separate_boxes(a, b):
    return a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1]


class TailParsingTests(unittest.TestCase):
    COPY = [{'speaker': 'CAPTION', 'text': 'One.'}, {'speaker': 'JO\u00c3O', 'text': 'Two.'},
            {'speaker': 'VOICE (off)', 'text': 'Three.'}]

    def test_list_and_map_forms_give_one_point_per_chunk(self):
        expected = [None, (600.0, 500.0), (300.0, 50.0)]
        self.assertEqual(r.parse_tails([None, [.5, .5], [.25, .05]], self.COPY, 1200, 1000), expected)
        self.assertEqual(r.parse_tails({'1': [.5, .5], '2': [.25, .05]}, self.COPY, 1200, 1000), expected)
        self.assertEqual(r.parse_tails(None, self.COPY[:1], 1200, 1000), [None])

    def test_missing_speech_tail_names_the_chunk(self):
        with self.assertRaisesRegex(r.AutoGeometryError, 'chunk 2'):
            r.parse_tails({'1': [.5, .5]}, self.COPY, 1200, 1000)


class RealChapterFourFrameTests(unittest.TestCase):
    """The frame the reviewers rejected: a caption and three painted balloons far too small for their text."""

    def test_page_01_panel_04_gets_drawn_boxes_that_cover_the_painted_ones_and_fit(self):
        import compositor as c
        import reserves as rv
        package = r.V15 / 'chapters' / 'ch04'
        try:
            job = json.loads((package / 'IMAGEGEN-JOBS.json').read_text())
            layout = json.loads((package / 'LAYOUT.json').read_text())
            record = json.loads((package / 'candidates' / 'page-01-panel-04-v01.json').read_text())
            frame = r.frame_file(record, package)
        except (OSError, ValueError):
            self.skipTest('chapter 4 frame is not readable')
        script = job['script']
        panel = next(p for page in script['pages'].values() for p in page['panels'] if p['id'] == 'page-01-panel-04')
        geometry = c.geometry_for_script(script, layout['page_rows'])
        slot = next(p for p in geometry['pages']['1'] if p['id'] == 'page-01-panel-04')
        tails = r.parse_tails({'1': [.56, .78], '2': [.66, .8], '3': [.88, .8]}, panel['copy'], record['width'], record['height'])
        plan = r.drawn_geometry(frame, panel['copy'], slot, tails)
        self.assertEqual(len(plan['reserves']), 4)
        painted = rv.find_regions(frame, 4)['regions']
        for reserve, region in zip(plan['reserves'], painted):
            x0, y0, x1, y1 = reserve['rect']
            self.assertTrue(x0 <= region['bbox'][0] and y0 <= region['bbox'][1] and x1 >= region['bbox'][2] and y1 >= region['bbox'][3])
        for a, b in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
            self.assertTrue(separate_boxes(plan['reserves'][a]['rect'], plan['reserves'][b]['rect']))
        row = dict(record, path=str(frame), **{'visible_rect': plan['visible_rect'], 'reserves': plan['reserves']})
        measured = c.copy_fit_measurements([row], script, geometry, SimpleNamespace(B=SimpleNamespace(measure=c.measure)))
        self.assertTrue(all(m['fits'] for m in measured))
        # Painted reserves for the same frame did not fit (that is why it was rejected).
        plain = rv.detect_reserves(frame, 4, [x['speaker'] for x in panel['copy']])
        row['reserves'] = plain['reserves']
        unfit = c.copy_fit_measurements([row], script, geometry, SimpleNamespace(B=SimpleNamespace(measure=c.measure)),
                                        reject_failures=False)
        self.assertFalse(all(m['fits'] for m in unfit))


from test_reserves import painted_outside


class ReviewerPicksTests(unittest.TestCase):
    """Every reviewer-approved chapter 4 pick, with the tail points the reviewers gave, through the planner."""

    # Picks that cannot be placed while covering their painted regions, and the cause the planner must give.
    # page-01-panel-04-v05 used to be here ("would always overlap": an unwrappable word between three tight painted
    # regions). Its 4.5 slot crops the frame to 63 percent of its height, which magnifies the art 1.6 times, so the
    # same text needs fewer source pixels and the boxes are placed; it now goes through every check below.
    CANNOT_BE_PLACED = {
        'page-03-panel-03-v04': 'tail point',                # a box covering the region must reach the mouth
        'page-05-panel-03-v04': 'painted region is within',  # two painted regions nearly touching
        # The painted balloon reaches the head its speaker's mouth implies (painted tails run up to the mouth).
        'page-02-panel-02-v02': 'would cover a face', 'page-05-panel-05-v04': 'would cover a face',
        'page-06-panel-01-v04': 'would cover a face',
        # Two painted balloons 51 px apart, each reaching the head of its speaker. Before the cover crop the binding
        # cause was the corner room between their boxes (about 33 px needed, 31 there); the crop trims 46 px of width
        # to the slot's shape, which moves the scale slightly and puts the head zone first.
        'page-03-panel-01-v09': 'would cover a face',
        # Three voices off frame above, their painted balloons side by side along the top edge. The first's tail leaves
        # its balloon sideways and runs on to a mouth above the frame through the next balloon: refused by the tail rules
        # (see test_reserves.TailCrossTests), where before it was placed with the tail drawn under that balloon.
        'page-01-panel-04-v01': "its tail would cross chunk 2's balloon",
        'page-01-panel-04-v05': "its tail would cross chunk 2's balloon",
    }

    def test_picks_assemble_with_valid_geometry_except_the_four_that_cannot(self):
        import compositor as c
        import reserves as rv
        from PIL import Image
        package = r.V15 / 'chapters' / 'ch04'
        folder = package / 'review' / 'geometry-drawn-r1'
        try:
            job = json.loads((package / 'IMAGEGEN-JOBS.json').read_text())
            layout = json.loads((package / 'LAYOUT.json').read_text())
            picks = sorted(folder.glob('*-tails.json'))
        except (OSError, ValueError):
            self.skipTest('chapter 4 review files are not readable')
        if not picks:
            self.skipTest('no reviewer tail files')
        if not any((package / 'frames').glob('*.png')):
            self.skipTest('chapter 4 local frames are not available')
        script = job['script']
        geometry = c.geometry_for_script(script, layout['page_rows'])
        panels = {p['id']: p for page in script['pages'].values() for p in page['panels']}
        v14 = SimpleNamespace(B=SimpleNamespace(measure=c.measure))
        assembled = 0
        for tails_path in picks:
            stem = tails_path.name[:-len('-tails.json')]
            panel_id = stem.rsplit('-v', 1)[0]
            try:
                record = json.loads((package / 'candidates' / f'{stem}.json').read_text())
                recorded_path = Path(record['path'])
                if recorded_path.is_absolute() and package not in recorded_path.parents:
                    continue
                frame = r.frame_file(record, package)
                raw = json.loads(tails_path.read_text())
            except (OSError, ValueError):
                continue
            panel = panels[panel_id]
            slot = next(p for p in geometry['pages'][str(panel['page'])] if p['id'] == panel_id)
            with Image.open(frame) as image:
                width, height = image.size
            tails = r.parse_tails(raw, panel['copy'], width, height)
            with self.subTest(pick=stem):
                if stem in self.CANNOT_BE_PLACED:
                    with self.assertRaisesRegex(r.AutoGeometryError, self.CANNOT_BE_PLACED[stem]):
                        r.drawn_geometry(frame, panel['copy'], slot, tails)
                    continue
                plan = r.drawn_geometry(frame, panel['copy'], slot, tails)
                assembled += 1
                reserves, bounds = plan['reserves'], plan['visible_rect']
                self.assertEqual(len(reserves), len(panel['copy']))
                for a in range(len(reserves)):
                    for b in range(a + 1, len(reserves)):
                        self.assertTrue(separate_boxes(reserves[a]['rect'], reserves[b]['rect']), (a, b))
                regions = rv.find_regions(frame, len(panel['copy']))['regions']
                for index, reserve in enumerate(reserves):
                    x0, y0, x1, y1 = reserve['rect']
                    if reserve['draw'] == 'speech' and index < len(regions) and index not in plan['partly_covered']:
                        ratio = reserve.get('corner', c.BALLOON_RADIUS_RATIO)
                        self.assertEqual(painted_outside(regions[index], reserve['rect'], ratio), 0,
                                         f'chunk {index} leaves painted pixels showing')
                    # A balloon may run past the frame only by its corner clearance (the text area and its padding
                    # stay inside); a caption not at all.
                    clear = (rv.CORNER_CLEAR * reserve.get('corner', c.BALLOON_RADIUS_RATIO) * min(x1 - x0, y1 - y0)
                             if reserve['draw'] == 'speech' else 0)
                    overhang = max(bounds[0] - x0, bounds[1] - y0, x1 - bounds[2], y1 - bounds[3])
                    self.assertTrue(x0 < x1 and y0 < y1 and overhang <= clear + 1e-6, f'chunk {index} overhangs the frame')
                    point = tails[index]
                    if point is not None and not rv.on_frame_edge(point, bounds):
                        self.assertFalse(x0 - 6 < point[0] < x1 + 6 and y0 - 6 < point[1] < y1 + 6,
                                         f'chunk {index} covers its mouth')
                    if index < len(regions) and index not in plan['partly_covered']:
                        bx0, by0, bx1, by1 = regions[index]['bbox']
                        self.assertTrue(x0 <= bx0 and y0 <= by0 and x1 >= bx1 and y1 >= by1, f'chunk {index} uncovered')
                # No box covers the head its mouth implies, measured to its rounded shape.
                for zone in r.head_zones(tails, [], bounds, height):
                    for index, reserve in enumerate(reserves):
                        ratio = reserve.get('corner', c.BALLOON_RADIUS_RATIO) if reserve['draw'] == 'speech' else None
                        self.assertGreaterEqual(rv.face_gap(reserve['rect'], ratio, zone), 0,
                                                f'chunk {index} covers {zone[3]}')
                row = dict(record, path=str(frame), visible_rect=bounds, reserves=reserves)
                measured = c.copy_fit_measurements([row], script, geometry, v14)
                self.assertTrue(all(m['fits'] for m in measured))
        if assembled:
            # 16 placed before the tail rules; the two page 1 panel 4 picks are now refused (see CANNOT_BE_PLACED).
            self.assertGreaterEqual(assembled, 14)


def poppler():
    import shutil
    bundled = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm'
    return shutil.which('pdftoppm') or (str(bundled) if bundled.exists() else None)


class PaintedPixelRenderTests(unittest.TestCase):
    """Render drawn balloons over painted regions: no painted pixel may show outside the drawn shape.

    The same reserves are rendered over the frame as generated and over a copy whose painted
    pixels are replaced by a flat colour. Where the two renders differ, a painted pixel is visible.
    """

    DPI = 200

    def setUp(self):
        import tempfile
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.dir = Path(self.temporary.name)
        if not poppler():
            self.skipTest('pdftoppm is not available')

    def render(self, frame, reserves, copy, slot, name, visible=None):
        import subprocess
        import numpy as np
        import compositor as c
        from PIL import Image
        with Image.open(frame) as image:
            width, height = image.size
        pid = 'page-01-panel-01'
        rows = [{'id': pid, 'path': str(frame), 'sha256': c.sha256(frame), 'width': width, 'height': height,
                 'visible_rect': visible or [0, 0, width, height], 'reserves': reserves}]
        script = {'title': 'Chapter 4: pixels', 'sha256': 'x', 'pages': {'1': {'panels': [{'id': pid, 'copy': copy}]}}}
        geometry = {'pages': {'1': [{'id': pid, 'rect_pt': slot['rect_pt']}]}}
        pdf = self.dir / f'{name}.pdf'
        c.compose(rows, script, geometry, pdf, chapter=4)
        subprocess.run([poppler(), '-png', '-singlefile', '-r', str(self.DPI), str(pdf), str(self.dir / name)], check=True)
        with Image.open(self.dir / f'{name}.png') as image:
            return np.asarray(image.convert('RGB')).astype(int)

    @staticmethod
    def visible_difference(a, b, tolerance=3):
        import numpy as np
        return int((np.abs(a - b).max(axis=2) > tolerance).sum())

    def wiped(self, frame, regions, name):
        """The frame with every painted pixel (region and outline ring) replaced by magenta."""
        import numpy as np
        from PIL import Image
        with Image.open(frame) as image:
            pixels = np.asarray(image.convert('RGB')).copy()
        for region in regions:
            ox, oy = region['painted']['origin']
            ys, xs = np.nonzero(region['painted']['mask'])
            pixels[ys + oy, xs + ox] = (255, 0, 255)
        path = self.dir / f'{name}.png'
        Image.fromarray(pixels).save(path)
        return path

    def test_no_painted_pixel_shows_outside_a_balloon_over_a_rectangular_painted_region(self):
        import reserves as rv
        from unittest import mock
        from test_reserves import frame as painted_frame
        painted = [(200, 150, 1000, 300), (1300, 150, 2100, 420)]      # rectangular painted balloons
        path = self.dir / 'painted.png'
        painted_frame(size=(2400, 1000), boxes=painted).save(path)
        clean = self.dir / 'clean.png'
        painted_frame(size=(2400, 1000), boxes=[]).save(clean)
        copy = [{'speaker': 'NAGOJI', 'text': 'Look at his hands.'}, {'speaker': 'DUARTE', 'text': 'See the brand.'}]
        slot = {'id': 'page-01-panel-01', 'rect_pt': [36, 300, 369, 153.75]}
        tails = r.parse_tails({'0': [.3, .9], '1': [.8, .95]}, copy, 2400, 1000)
        plan = r.drawn_geometry(path, copy, slot, tails)
        shown = self.render(path, plan['reserves'], copy, slot, 'painted-render')
        hidden = self.render(clean, plan['reserves'], copy, slot, 'clean-render')
        self.assertEqual(self.visible_difference(shown, hidden), 0)
        # The test can see the defect: without corner-aware placement the painted corners show.
        original = rv.place_boxes
        naive_calls = lambda *a, **k: original(*a, **{key: v for key, v in k.items() if key != 'rounded'})
        with mock.patch.object(rv, 'place_boxes', naive_calls):
            naive = r.drawn_geometry(path, copy, slot, tails)
        shown = self.render(path, naive['reserves'], copy, slot, 'naive-painted')
        hidden = self.render(clean, naive['reserves'], copy, slot, 'naive-clean')
        self.assertGreater(self.visible_difference(shown, hidden), 100)

    def test_a_balloon_over_a_corner_pinned_painted_region_bleeds_off_the_frame_and_hides_it(self):
        import compositor as c
        import reserves as rv
        from unittest import mock
        from test_reserves import frame as painted_frame
        path = self.dir / 'pinned.png'
        painted_frame(size=(2400, 1000), boxes=[(8, 8, 900, 200)]).save(path)          # in the frame's corner
        clean = self.dir / 'pinned-clean.png'
        painted_frame(size=(2400, 1000), boxes=[]).save(clean)
        copy = [{'speaker': 'NAGOJI', 'text': 'Look at his hands.'}]
        slot = {'id': 'page-01-panel-01', 'rect_pt': [36, 300, 369, 153.75]}
        tails = r.parse_tails({'0': [.3, .9]}, copy, 2400, 1000)
        plan = r.drawn_geometry(path, copy, slot, tails)
        reserve = plan['reserves'][0]
        x0, y0, x1, y1 = reserve['rect']
        self.assertTrue(x0 < 0 or y0 < 0)                                   # the balloon runs off the frame
        self.assertTrue(x1 <= 2400 and y1 <= 1000)                          # and only where its region is
        self.assertEqual(list(plan['bleeds']), [0])
        self.assertEqual(plan['bleeds'][0][2:], [0, 0])
        # The text area and its padding stay inside visible_rect (the compositor's own check).
        rows = [{'id': 'page-01-panel-01', 'path': str(path), 'sha256': c.sha256(path), 'width': 2400, 'height': 1000,
                 'visible_rect': plan['visible_rect'], 'reserves': plan['reserves']}]
        script = {'title': 'x', 'pages': {'1': {'panels': [{'id': 'page-01-panel-01', 'copy': copy}]}}}
        geometry = {'pages': {'1': [{'id': 'page-01-panel-01', 'rect_pt': slot['rect_pt']}]}}
        measured = c.copy_fit_measurements(rows, script, geometry, SimpleNamespace(B=SimpleNamespace(measure=c.measure)))
        self.assertTrue(all(m['fits'] for m in measured))
        shown = self.render(path, plan['reserves'], copy, slot, 'pinned-shown')
        hidden = self.render(clean, plan['reserves'], copy, slot, 'pinned-hidden')
        self.assertEqual(self.visible_difference(shown, hidden), 0)
        # Without the bleed option the same chunk is refused for its corners.
        original = rv.place_boxes
        no_bleed = lambda *a, **k: original(*a, **{key: v for key, v in k.items() if key != 'bleed'})
        with mock.patch.object(rv, 'place_boxes', no_bleed):
            with self.assertRaisesRegex(r.AutoGeometryError, 'corner'):
                r.drawn_geometry(path, copy, slot, tails)

    def test_geometry_with_a_reduced_corner_renders_with_that_radius(self):
        import compositor as c
        from test_reserves import frame as painted_frame
        path = self.dir / 'painted.png'
        painted_frame(size=(2400, 1000), boxes=[(200, 150, 1000, 300)]).save(path)
        copy = [{'speaker': 'NAGOJI', 'text': 'Look at his hands.'}]
        slot = {'id': 'page-01-panel-01', 'rect_pt': [36, 300, 369, 153.75]}
        plan = r.drawn_geometry(path, copy, slot, r.parse_tails({'0': [.3, .9]}, copy, 2400, 1000))
        reserve = plan['reserves'][0]
        self.assertIn(reserve.get('corner', .45), (.45, .4))
        self.assertGreaterEqual(reserve.get('corner', .45), c.BALLOON_MIN_RATIO)

    def test_real_frames_show_no_painted_pixel_outside_their_balloons(self):
        """Real chapter 4 frames: rendered balloons hide their painted pixels, or the planner refuses and says why."""
        import compositor as c
        import reserves as rv
        from PIL import Image
        package = r.V15 / 'chapters' / 'ch04'
        try:
            job = json.loads((package / 'IMAGEGEN-JOBS.json').read_text())
            layout = json.loads((package / 'LAYOUT.json').read_text())
        except (OSError, ValueError):
            self.skipTest('chapter 4 files are not readable')
        script = job['script']
        geometry = c.geometry_for_script(script, layout['page_rows'])
        panels = {p['id']: p for page in script['pages'].values() for p in page['panels']}
        # The page 6 frames have painted balloons in the frame's corner, so their balloons bleed off the frame.
        # Page 1 panel 4 has a balloon whose radius had to be reduced to 40 percent.
        # page-06-panel-01-v04 is now refused: its painted balloon reaches the head of the speaker's mouth.
        # page-01-panel-04-v01 is now refused for a tail through the next balloon (the tail rules); its balloons are still
        # checked here, with those rules lifted, because its radius-reduced corner is what this test is about.
        expected = {'page-06-panel-01-v04': 'would cover a face', 'page-06-panel-03-v03': 'hidden',
                    'page-01-panel-04-v01': 'hidden with the tail rules lifted', 'page-02-panel-03-v02': 'hidden'}
        checked = 0
        for stem, outcome in expected.items():
            try:
                record = json.loads((package / 'candidates' / f'{stem}.json').read_text())
                frame = r.frame_file(record, package)
                raw = json.loads((package / 'review' / 'geometry-drawn-r1' / f'{stem}-tails.json').read_text())
            except (OSError, ValueError):
                continue
            panel_id = stem.rsplit('-v', 1)[0]
            panel = panels[panel_id]
            slot = next(p for p in geometry['pages'][str(panel['page'])] if p['id'] == panel_id)
            with Image.open(frame) as image:
                width, height = image.size
            tails = r.parse_tails(raw, panel['copy'], width, height)
            with self.subTest(pick=stem):
                if not outcome.startswith('hidden'):
                    with self.assertRaisesRegex(r.AutoGeometryError, outcome):
                        r.drawn_geometry(frame, panel['copy'], slot, tails)
                    continue
                if outcome == 'hidden with the tail rules lifted':
                    with self.assertRaisesRegex(r.AutoGeometryError, "its tail would cross chunk 2's balloon"):
                        r.drawn_geometry(frame, panel['copy'], slot, tails)
                    with mock.patch.object(rv, 'RULES', ()):
                        plan = r.drawn_geometry(frame, panel['copy'], slot, tails)
                else:
                    plan = r.drawn_geometry(frame, panel['copy'], slot, tails)
                regions = rv.find_regions(frame, len(panel['copy']))['regions']
                shown = self.render(frame, plan['reserves'], panel['copy'], slot, f'{stem}-shown', plan['visible_rect'])
                hidden = self.render(self.wiped(frame, regions, f'{stem}-wiped'), plan['reserves'], panel['copy'], slot,
                                     f'{stem}-hidden', plan['visible_rect'])
                self.assertEqual(self.visible_difference(shown, hidden), 0)
                checked += 1
        if checked:
            self.assertEqual(checked, 3)


class FaceZoneTests(unittest.TestCase):
    """Faces, and the head zone every tail point implies, must never be covered by a drawn box."""

    def test_faces_are_parsed_into_pixel_circles_with_r_relative_to_the_frame_height(self):
        faces = r.parse_faces([{'x': .25, 'y': .5, 'r': .1}, {'x': .7, 'y': .4, 'r': .08, 'name': 'Nagoji'}], 2000, 1000)
        self.assertEqual(faces, [(500.0, 500.0, 100.0, 'face 0'), (1400.0, 400.0, 80.0, 'Nagoji')])
        self.assertEqual(r.parse_faces(None, 2000, 1000), [])
        self.assertEqual(r.parse_faces([], 2000, 1000), [])
        for bad in ('x', {'x': .5}, [1], [{'x': .5, 'y': .5}], [{'x': 1.5, 'y': .5, 'r': .1}],
                    [{'x': .5, 'y': .5, 'r': 0}], [{'x': .5, 'y': .5, 'r': -.1}], [{'x': 'a', 'y': .5, 'r': .1}],
                    [{'x': .5, 'y': .5, 'r': 2}], [{'x': True, 'y': .5, 'r': .1}]):
            with self.subTest(faces=bad), self.assertRaisesRegex(r.AutoGeometryError, 'face'):
                r.parse_faces(bad, 2000, 1000)

    def test_a_tail_point_implies_a_head_zone_just_above_the_mouth(self):
        bounds = [0, 0, 2000, 1000]
        zones = r.head_zones([(600.0, 500.0), None, (1000.0, 0.0)], [], bounds, 1000)
        # Radius 0.09 of the frame height, centred half a radius above the mouth. No caption tail, and a
        # tail at the frame edge (an off-frame speaker) has no head in the frame.
        self.assertEqual(zones, [(600.0, 455.0, 90.0, "head of chunk 0's speaker")])
        # A face entry that covers the mouth stands in for the implied head; one that does not leaves it.
        self.assertEqual(r.head_zones([(600.0, 500.0)], [(600.0, 420.0, 100.0, 'Nagoji')], bounds, 1000), [])
        self.assertEqual(len(r.head_zones([(600.0, 500.0)], [(1500.0, 420.0, 100.0, 'far')], bounds, 1000)), 1)
        self.assertEqual(r.head_zones([], [], bounds, 1000), [])
        # Two chunks from the same speaker share one mouth, and so one zone; another speaker gets its own.
        zones = r.head_zones([(600.0, 500.0), (610.0, 505.0), (1400.0, 520.0)], [], bounds, 1000)
        self.assertEqual([z[3] for z in zones], ["head of chunk 0's speaker", "head of chunk 2's speaker"])

    def test_a_balloon_that_would_have_covered_the_speakers_head_now_fails_with_the_reason(self):
        import reserves as rv
        from unittest import mock
        from test_reserves import frame as painted_frame
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'f.png'
            painted_frame(size=(2400, 1000), boxes=[(200, 150, 1000, 300)]).save(path)
            copy = [{'speaker': 'NAGOJI', 'text': 'Look at his hands.'}]
            slot = {'id': 'page-01-panel-01', 'rect_pt': [36, 300, 369, 153.75]}
            tails = r.parse_tails({'0': [.3, .35]}, copy, 2400, 1000)      # the mouth is just under the painted balloon
            original = rv.place_boxes
            no_faces = lambda *a, **k: original(*a, **{key: v for key, v in k.items() if key not in ('faces', 'face_margin')})
            with mock.patch.object(rv, 'place_boxes', no_faces):
                old = r.drawn_geometry(path, copy, slot, tails)
            x0, y0, x1, y1 = old['reserves'][0]['rect']
            zone = (720.0, 305.0, 90.0)                                      # 0.09 of the height, above the mouth
            self.assertLess(rv.face_gap([x0, y0, x1, y1], .45, zone + ('head',)), 0)        # the old balloon covers it
            with self.assertRaisesRegex(r.AutoGeometryError, r"would cover a face.*head of chunk 0's speaker"):
                r.drawn_geometry(path, copy, slot, tails)

    def test_a_given_face_moves_the_box_clear_of_it_and_the_clearance_is_reported(self):
        import reserves as rv
        import tempfile
        from test_reserves import frame as painted_frame
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'f.png'
            painted_frame(size=(2400, 1000), boxes=[(200, 150, 1000, 300)]).save(path)
            copy = [{'speaker': 'NAGOJI', 'text': 'Look at his hands and see the brand on his arm, said the voice.'}]
            slot = {'id': 'page-01-panel-01', 'rect_pt': [36, 300, 369, 153.75]}
            tails = r.parse_tails({'0': [.3, .9]}, copy, 2400, 1000)
            free = r.drawn_geometry(path, copy, slot, tails)
            fx0, fy0, fx1, fy1 = free['reserves'][0]['rect']
            self.assertGreater(fx1, 1008)                                     # the text box reaches past the painted region
            face = (fx1 - 25.0, (fy0 + fy1) / 2, 45.0, 'face 0')             # a face in the part that overhangs it
            moved = r.drawn_geometry(path, copy, slot, tails, faces=[face])
            box = moved['reserves'][0]['rect']
            self.assertNotEqual(box, free['reserves'][0]['rect'])
            ratio = moved['reserves'][0].get('corner', .45)
            self.assertGreater(rv.face_gap(box, ratio, face), 0)
            report = moved['face_clearance'][0]
            self.assertEqual(report['face'], 'face 0')
            self.assertAlmostEqual(report['px'], rv.face_gap(box, ratio, face), places=3)
            self.assertAlmostEqual(report['pt'], report['px'] * .15375, delta=.02)
            # Without a given face the only one is the head the tail implies, and it is reported.
            self.assertEqual(free['face_clearance'][0]['face'], "head of chunk 0's speaker")
            self.assertEqual(free['head_zones'], ["head of chunk 0's speaker"])


if __name__ == "__main__":
    unittest.main()


class CoverCropGeometryTests(unittest.TestCase):
    """drawn_geometry crops a 3:2 frame toward its slot's shape and keeps what must stay in view."""

    SIZE = (1536, 1024)
    ART = [0, 0, 1536, 1024]
    SLOT = {'id': 'page-01-panel-01', 'rect_pt': [36, 56.25, 369, 153.75]}       # 369 x 153.75 pt: aspect 2.4
    PAINTED = (900, 350, 1300, 450)
    FACE = (400.0, 700.0, 80.0, 'Nagoji')
    COPY = [{'speaker': 'NAGOJI', 'text': 'Look at his hands.'}]

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.dir = Path(self.temporary.name)

    def frame(self, boxes):
        from test_reserves import frame
        path = self.dir / 'f.png'
        frame(size=self.SIZE, boxes=list(boxes)).save(path)
        return path

    def plan(self, boxes, copy, tails, faces=(), slot=None, keep=None):
        return r.drawn_geometry(self.frame(boxes), copy, slot or self.SLOT, tails, list(faces), keep=keep)

    @staticmethod
    def inside(inner, outer):
        return outer[0] <= inner[0] and outer[1] <= inner[1] and inner[2] <= outer[2] and inner[3] <= outer[3]

    def painted_extent(self, index=0):
        """The rectangle holding a painted region's pixels, outline included."""
        import reserves as rv
        painted = rv.find_regions(self.dir / 'f.png', index + 1)['regions'][index]['painted']
        (x, y), (height, width) = painted['origin'], painted['mask'].shape
        return [x, y, x + width, y + height]

    def test_a_wide_slot_crops_the_frame_to_its_shape_keeping_the_face_and_the_painted_region(self):
        import reserves as rv
        plan = self.plan([self.PAINTED], self.COPY, [(400.0, 740.0)], [self.FACE])       # the mouth is inside the face
        crop = plan['visible_rect']
        self.assertEqual(plan['art_rect'], self.ART)
        self.assertNotEqual(crop, self.ART)
        self.assertEqual((crop[0], crop[2]), (0, 1536))                                # only the height is cropped
        self.assertLessEqual(abs((crop[2] - crop[0]) / (crop[3] - crop[1]) / 2.4 - 1), .02)
        x, y, radius, _ = self.FACE
        self.assertTrue(self.inside([x - radius, y - radius, x + radius, y + radius], crop))
        self.assertTrue(self.inside(rv.find_regions(self.dir / 'f.png', 1)['regions'][0]['bbox'], crop))
        self.assertTrue(self.inside(self.painted_extent(), crop))                      # outline pixels and all
        for reserve in plan['reserves']:
            self.assertTrue(self.inside(reserve['rect'], crop))
        self.assertTrue(all(isinstance(v, int) for v in crop))

    def test_the_planner_works_inside_the_crop_and_the_slot_is_filled(self):
        import compositor as c
        plan = self.plan([self.PAINTED], self.COPY, [(400.0, 740.0)], [self.FACE])
        row = {'width': 1536, 'height': 1024, 'visible_rect': plan['visible_rect']}
        clip, _ = c.fit_clip_contain(row, self.SLOT)
        self.assertAlmostEqual(clip[2], 369, delta=369 * .02)                          # the crop spans the whole column
        self.assertAlmostEqual(clip[3], 153.75, delta=153.75 * .02)
        uncropped, _ = c.fit_clip_contain({'width': 1536, 'height': 1024, 'visible_rect': self.ART}, self.SLOT)
        self.assertLess(uncropped[2], 260)                                             # as it was: bars either side

    def test_a_slot_with_the_art_s_own_shape_is_left_alone(self):
        slot = {'id': 'page-01-panel-01', 'rect_pt': [36, 56.25, 369, 246]}            # aspect 1.5
        plan = self.plan([self.PAINTED], self.COPY, [(400.0, 740.0)], [self.FACE], slot)
        self.assertEqual((plan['visible_rect'], plan['art_rect']), (self.ART, self.ART))

    def test_the_head_a_tail_implies_is_kept_in_the_crop(self):
        painted = (100, 40, 500, 120)                                                  # near the top
        plan = self.plan([painted], self.COPY, [(1200.0, 960.0)])                      # the speaker's head is near the bottom
        crop = plan['visible_rect']
        self.assertEqual(plan['head_zones'], ["head of chunk 0's speaker"])
        self.assertTrue(self.inside([1200 - 92, 914 - 92, 1200 + 92, 914 + 92], crop))    # 0.09 of the height, above the mouth
        self.assertTrue(self.inside(self.painted_extent(), crop))
        self.assertGreater(crop[3] - crop[1], 640)                                     # so it could not be cropped to the slot
        self.assertEqual(plan['reserves'][0]['tail'], [1200, 960])                     # an on-frame tail point is never moved

    def test_an_off_frame_tail_point_is_moved_onto_the_crop_edge_and_does_not_hold_the_crop_open(self):
        import reserves as rv
        for name, tail in (('top edge', (768.0, 0.0)), ('bottom edge', (768.0, 1023.0)), ('left edge, above the crop', (0.0, 60.0)),
                           ('right edge, below the crop', (1536.0, 990.0))):
            with self.subTest(name):
                self.assertTrue(rv.on_frame_edge(tail, self.ART))
                plan = self.plan([self.PAINTED], self.COPY, [tail], [self.FACE])
                crop = plan['visible_rect']
                self.assertEqual(crop, rv.cover_crop(self.ART, 2.4, [[320, 620, 480, 780], self.painted_extent()]))
                point = plan['reserves'][0]['tail']
                self.assertTrue(rv.on_frame_edge(point, crop))                        # still off frame, now at the crop's edge
                self.assertTrue(crop[0] <= point[0] <= crop[2] and crop[1] <= point[1] <= crop[3])
                if tail[1] <= 3 or tail[1] >= 1020:
                    self.assertEqual(point[1], crop[1] if tail[1] <= 3 else crop[3])  # snapped to the edge it was on
                    self.assertEqual(point[0], round(tail[0]))
                else:
                    self.assertEqual(point[0], round(tail[0]))
                    self.assertEqual(point[1], crop[1] if tail[1] < crop[1] else crop[3])

    def test_an_off_frame_tail_point_on_an_edge_the_crop_did_not_cut_is_left_where_it_is(self):
        plan = self.plan([self.PAINTED], self.COPY, [(0.0, 500.0)], [self.FACE])
        self.assertEqual(plan['reserves'][0]['tail'], [0, 500])

    def test_a_tall_slot_crops_the_width_and_moves_off_frame_points_onto_the_crop_s_sides(self):
        import reserves as rv
        slot = {'id': 'page-01-panel-01', 'rect_pt': [36, 56.25, 369, 300]}               # aspect 1.23: the art is wider
        for tail in ((100.0, 0.0), (0.0, 500.0), (1536.0, 300.0)):
            with self.subTest(tail=tail):
                plan = self.plan([self.PAINTED], self.COPY, [tail], [self.FACE], slot)
                crop = plan['visible_rect']
                self.assertEqual((crop[1], crop[3]), (0, 1024))                          # only the width is cropped
                self.assertLessEqual(abs((crop[2] - crop[0]) / (crop[3] - crop[1]) / (369 / 300) - 1), .02)
                self.assertTrue(self.inside([320, 620, 480, 780], crop))
                point = plan['reserves'][0]['tail']
                self.assertTrue(rv.on_frame_edge(point, crop))
                self.assertEqual(point[0], crop[0] if tail[0] < crop[0] else crop[2] if tail[0] > crop[2] else round(tail[0]))
                self.assertEqual(point[1], round(tail[1]))                               # the height is not cropped: unchanged

    def test_a_silent_panel_is_cropped_to_its_slot_too(self):
        import reserves as rv
        plain = r.drawn_geometry(self.frame([]), [], self.SLOT, [], [])
        self.assertEqual(plain['art_rect'], self.ART)
        self.assertEqual(plain['visible_rect'], rv.cover_crop(self.ART, 2.4, []))
        self.assertEqual(plain['visible_rect'], [0, 192, 1536, 832])
        self.assertEqual(plain['reserves'], [])
        faced = r.drawn_geometry(self.frame([]), [], self.SLOT, [], [(700.0, 900.0, 80.0, 'Nagoji')])
        self.assertEqual(faced['art_rect'], self.ART)
        self.assertTrue(self.inside([620, 820, 780, 980], faced['visible_rect']))
        self.assertLess(faced['visible_rect'][3] - faced['visible_rect'][1], 1024)
        self.assertLessEqual(abs((faced['visible_rect'][2] - faced['visible_rect'][0])
                                 / (faced['visible_rect'][3] - faced['visible_rect'][1]) / 2.4 - 1), .02)


class TailReadingGeometryTests(unittest.TestCase):
    """drawn_geometry gives place_boxes the plan's scale, so no tail crosses another balloon or face."""

    SIZE = (1536, 1024)
    SLOT = {'id': 'page-01-panel-01', 'rect_pt': [36, 56.25, 369, 246]}                    # aspect 1.5: nothing is cropped
    COPY = [{'speaker': 'NAGOJI', 'text': 'Look at his hands and see the brand.'},
            {'speaker': 'RAMAYYAN', 'text': 'I see it, and I will say nothing.'}]
    SCALE = 369 / 1536

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.dir = Path(self.temporary.name)

    def frame(self):
        from test_reserves import quiet_frame
        path = self.dir / 'q.png'
        quiet_frame(size=self.SIZE, busy=()).save(path)
        return path

    def test_the_planner_passes_the_panels_scale_in_points_per_source_pixel(self):
        import reserves as rv
        with mock.patch.object(rv, 'place_boxes', wraps=rv.place_boxes) as spy:
            r.drawn_geometry(self.frame(), self.COPY, self.SLOT, [(300.0, 700.0), (200.0, 120.0)], [])
        self.assertAlmostEqual(spy.call_args.kwargs['scale'], self.SCALE, places=6)

    def test_a_tail_does_not_run_through_the_other_balloon(self):
        import reserves as rv
        from test_reserves import line_hits
        # The second speaker was at (200, 120): with the tail-tip rule the planner's placement for that input is still
        # valid (reserves.tail_crosses) but its first tail passes 8 px from the other balloon, inside this test's own
        # stricter margin (half the wedge's base), so the speaker stands a little further left.
        tails = [(300.0, 700.0), (120.0, 120.0)]
        plan = r.drawn_geometry(self.frame(), self.COPY, self.SLOT, tails, [])
        boxes = [reserve['rect'] for reserve in plan['reserves']]
        for index, reserve in enumerate(plan['reserves']):
            ratio = reserve.get('corner', .45)
            (bx, by), (tx, ty), half, _ = rv.tail_wedge(boxes[index], ratio, tails[index], plan['visible_rect'], self.SCALE)
            other = boxes[1 - index]
            self.assertFalse(line_hits((bx, by), (tx, ty), other, half * .5), (index, boxes))
            centre = ((boxes[index][0] + boxes[index][2]) / 2, (boxes[index][1] + boxes[index][3]) / 2)
            self.assertFalse(line_hits(centre, (tx, ty), other), (index, boxes))
            self.assertEqual(reserve['tail'], [round(tails[index][0]), round(tails[index][1])])

    def test_a_tail_that_can_only_cross_another_face_fails_in_the_chapters_own_error(self):
        from test_reserves import frame
        path = self.dir / 'w.png'
        frame(size=self.SIZE, boxes=[(100, 200, 400, 300)]).save(path)
        copy = [{'speaker': 'NAGOJI', 'text': 'Look.'}]
        speaker = (1000.0, 250.0)
        faces = [(1000.0, 200.0, 60.0, 'Nagoji'), (700.0, 250.0, 60.0, 'Duarte')]          # Duarte stands between them
        with self.assertRaises(r.AutoGeometryError) as caught:
            r.drawn_geometry(path, copy, self.SLOT, [speaker], faces)
        self.assertIn('chunk 0: its tail would cross a face (Duarte)', str(caught.exception))
        self.assertEqual(len(r.drawn_geometry(path, copy, self.SLOT, [speaker], faces[:1])['reserves']), 1)


class KeepZoneGeometryTests(unittest.TestCase):
    """Keep zones (a gripping hand, a prop) are held in the cover crop exactly as faces are, and are soft obstacles to boxes."""

    SIZE = (1536, 1024)
    ART = [0, 0, 1536, 1024]
    SLOT = {'id': 'page-01-panel-01', 'rect_pt': [36, 56.25, 369, 153.75]}       # aspect 2.4: the crop is 640 px tall
    PAINTED = (900, 450, 1300, 550)
    FACE = (400.0, 700.0, 80.0, 'Nagoji')
    COPY = [{'speaker': 'NAGOJI', 'text': 'Look at his hands.'}]

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.dir = Path(self.temporary.name)

    def frame(self, boxes=()):
        from test_reserves import frame
        path = self.dir / 'f.png'
        frame(size=self.SIZE, boxes=list(boxes)).save(path)
        return path

    def plan(self, keep=None, boxes=(PAINTED,), faces=(FACE,), copy=None, tails=((400.0, 740.0),)):
        return r.drawn_geometry(self.frame(boxes), self.COPY if copy is None else copy, self.SLOT, list(tails), list(faces), keep=keep)

    @staticmethod
    def inside(inner, outer):
        return outer[0] <= inner[0] and outer[1] <= inner[1] and inner[2] <= outer[2] and inner[3] <= outer[3]

    def test_keep_zones_are_parsed_as_fractions_of_the_frame_and_extra_keys_are_ignored(self):
        zones = r.parse_keep([{'x0': .1, 'y0': .2, 'x1': .3, 'y1': .4, 'what': 'the brand'}, {'x0': 0, 'y0': 0, 'x1': 1, 'y1': 1}], 1000, 500)
        self.assertEqual(zones, [[100.0, 100.0, 300.0, 200.0], [0.0, 0.0, 1000.0, 500.0]])
        self.assertEqual(r.parse_keep(None, 1000, 500), [])
        self.assertEqual(r.parse_keep([], 1000, 500), [])

    def test_bad_keep_zones_fail_clearly(self):
        good = {'x0': .1, 'y0': .2, 'x1': .3, 'y1': .4}
        for bad, expect in (('nope', 'list'), ({'x0': .1}, 'list'), ([5], 'keep zone 0'), ([{'x0': .1, 'y0': .2, 'x1': .3}], 'keep zone 0'),
                            ([good, {'x0': .1, 'y0': .2, 'x1': 'a', 'y1': .4}], 'keep zone 1'),
                            ([dict(good, x0=-.1)], 'between 0 and 1'), ([dict(good, y1=1.2)], 'between 0 and 1'),
                            ([dict(good, x0=.3)], 'x0 below x1'), ([dict(good, y0=.5)], 'y0 below y1'),
                            ([dict(good, x0=True)], 'keep zone 0')):
            with self.subTest(bad=bad), self.assertRaises(r.AutoGeometryError) as caught:
                r.parse_keep(bad, 1000, 500)
            self.assertIn(expect, str(caught.exception))

    def test_a_keep_zone_near_the_bottom_moves_the_crop_band_down_to_include_it(self):
        keep = [900.0, 880.0, 1300.0, 1000.0]
        without = self.plan()['visible_rect']
        held = self.plan([keep])['visible_rect']
        self.assertFalse(self.inside(keep, without))                                 # the band sat higher, on the face and the region
        self.assertTrue(self.inside(keep, held))
        self.assertGreater(held[1], without[1])                                      # and moved down to hold it
        self.assertEqual((held[0], held[2]), (0, 1536))
        self.assertLessEqual(abs((held[2] - held[0]) / (held[3] - held[1]) / 2.4 - 1), .02)   # still the slot's shape
        x, y, radius, _ = self.FACE
        self.assertTrue(self.inside([x - radius, y - radius, x + radius, y + radius], held))   # the face is still held
        import reserves as rv
        region = rv.find_regions(self.dir / 'f.png', 1)['regions'][0]['painted']
        (px, py), (ph, pw) = region['origin'], region['mask'].shape
        self.assertTrue(self.inside([px, py, px + pw, py + ph], held))                # and so is the painted region

    def test_a_keep_zone_that_cannot_fit_with_the_faces_leaves_the_crop_taller_not_cut(self):
        import compositor as c
        keep = [200.0, 20.0, 500.0, 100.0]                                           # the top, with the face at y 620 to 780
        plan = self.plan([keep])
        crop = plan['visible_rect']
        self.assertTrue(self.inside(keep, crop))
        x, y, radius, _ = self.FACE
        self.assertTrue(self.inside([x - radius, y - radius, x + radius, y + radius], crop))
        self.assertGreater(crop[3] - crop[1], 640)                                   # taller than the slot's shape needs
        clip, _ = c.fit_clip_contain({'width': 1536, 'height': 1024, 'visible_rect': crop}, self.SLOT)
        self.assertLess(clip[2], 369 * .98)                                          # so the slot is filled with bars either side

    def test_a_silent_panel_keeps_a_keep_zone_too(self):
        keep = [200.0, 900.0, 400.0, 1010.0]
        plain = r.drawn_geometry(self.frame(), [], self.SLOT, [], [])
        held = r.drawn_geometry(self.frame(), [], self.SLOT, [], [], keep=[keep])
        self.assertFalse(self.inside(keep, plain['visible_rect']))
        self.assertTrue(self.inside(keep, held['visible_rect']))
        self.assertEqual(held['art_rect'], self.ART)
        self.assertEqual(held['reserves'], [])

    def test_a_balloon_that_must_cover_a_keep_zone_does_and_says_so(self):
        region = self.PAINTED
        plan = self.plan([[float(v) for v in region]])                              # the keep zone is the painted region itself
        x0, y0, x1, y1 = plan['reserves'][0]['rect']
        self.assertTrue(x0 <= region[0] and y0 <= region[1] and x1 >= region[2] and y1 >= region[3])   # the balloon covers it
        self.assertTrue(self.inside([float(v) for v in region], plan['visible_rect']))
        self.assertEqual(plan['keep_overlaps'], {0: [0]})                           # it is a soft wish, and it is reported

    def test_no_keep_zones_is_exactly_the_plan_it_was(self):
        self.assertEqual(self.plan(None), self.plan([]))
        self.assertEqual(self.plan(None)['keep_overlaps'], {})
        self.assertEqual(self.plan(None)['edge_voice_no_tail'], [])

    def test_the_planner_hands_the_zones_to_the_placer_as_soft_obstacles(self):
        import reserves as rv
        keep = [[900.0, 880.0, 1300.0, 1000.0]]
        with mock.patch.object(rv, 'place_boxes', wraps=rv.place_boxes) as spy:
            self.plan(keep)
        self.assertEqual(spy.call_args.kwargs['keep'], keep)

    def test_a_free_caption_keeps_off_a_keep_zone_where_it_can(self):
        copy = [{'speaker': 'CAPTION', 'text': 'The hold was dark.'}]
        slot = {'id': 'page-01-panel-01', 'rect_pt': [36, 56.25, 369, 246]}                # 1.5: nothing is cropped
        from test_reserves import quiet_frame
        path = self.dir / 'k.png'
        quiet_frame(size=self.SIZE, busy=()).save(path)
        plain = r.drawn_geometry(path, copy, slot, [None], [])
        x0, y0, x1, y1 = plain['reserves'][0]['rect']
        zone = [float(x0 + 10), float(y0), float(x1 - 10), float(y1 + 200)]                # the torsos under it
        held = r.drawn_geometry(path, copy, slot, [None], [], keep=[zone])
        self.assertNotEqual(held['reserves'][0]['rect'], plain['reserves'][0]['rect'])
        a, b, c_, d = held['reserves'][0]['rect']
        covered = max(0, min(c_, zone[2]) - max(a, zone[0])) * max(0, min(d, zone[3]) - max(b, zone[1]))
        self.assertLess(covered / ((zone[2] - zone[0]) * (zone[3] - zone[1])), .10)
        self.assertEqual(held['keep_overlaps'], {})

    def test_a_voice_from_off_frame_keeps_room_for_its_tail_at_the_panels_scale(self):
        copy = [{'speaker': 'SAILOR', 'text': 'Hold fast!'}]
        slot = {'id': 'page-01-panel-01', 'rect_pt': [36, 56.25, 369, 246]}
        scale = 369 / 1536
        from test_reserves import quiet_frame
        path = self.dir / 'e.png'
        quiet_frame(size=self.SIZE, busy=()).save(path)
        plan = r.drawn_geometry(path, copy, slot, [(700.0, 0.0)], [])
        self.assertGreaterEqual(plan['reserves'][0]['rect'][1] * scale, 8.8 - 1e-6)        # TAIL_MIN_PT plus the stroke, in points
        self.assertEqual(plan['edge_voice_no_tail'], [])
        self.assertEqual(plan['reserves'][0]['tail'], [700, 0])
        silent = r.drawn_geometry(path, [], slot, [], [])
        self.assertEqual((silent['keep_overlaps'], silent['edge_voice_no_tail']), ({}, []))


class BibleSnapshotTests(unittest.TestCase):
    """A later bible edit must not break a package prepared against the earlier bible."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.live = self.root / "CONTINUITY.md"
        self.live.write_text("# bible v1\n", encoding="utf-8")
        self.pkg = self.root / "pkg"
        self.pkg.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def item(self):
        import compositor as c
        return {"path": str(self.live), "sha256": c.sha256(self.live)}

    def test_live_file_matching_passes(self):
        r.check_recorded_input(self.item(), self.pkg)

    def test_changed_live_file_without_snapshot_fails(self):
        item = self.item()
        self.live.write_text("# bible v2\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            r.check_recorded_input(item, self.pkg)

    def test_changed_live_file_with_matching_package_snapshot_passes(self):
        item = self.item()
        (self.pkg / "CONTINUITY-SNAPSHOT.md").write_text("# bible v1\n", encoding="utf-8")
        self.live.write_text("# bible v2\n", encoding="utf-8")
        r.check_recorded_input(item, self.pkg)

    def test_snapshot_with_wrong_content_fails(self):
        item = self.item()
        (self.pkg / "CONTINUITY-SNAPSHOT.md").write_text("# something else\n", encoding="utf-8")
        self.live.write_text("# bible v2\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            r.check_recorded_input(item, self.pkg)

    def test_art_direction_snapshot_name_is_independent_of_sidecar_filename(self):
        sidecar = self.root / "CHAPTER-09-ART-DIRECTION.json"
        sidecar.write_text("draft v1\n", encoding="utf-8")
        item = {"path": str(sidecar), "sha256": r.c.sha256(sidecar)}
        (self.pkg / "ART-DIRECTION-SNAPSHOT.json").write_text("draft v1\n", encoding="utf-8")
        sidecar.write_text("draft v2\n", encoding="utf-8")
        r.check_recorded_input(item, self.pkg)

    def test_changed_art_direction_without_matching_snapshot_fails(self):
        sidecar = self.root / "pilot-ART-DIRECTION.json"
        sidecar.write_text("draft v1\n", encoding="utf-8")
        item = {"path": str(sidecar), "sha256": r.c.sha256(sidecar)}
        sidecar.write_text("draft v2\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, 'Input changed since preparation'):
            r.check_recorded_input(item, self.pkg)


class TallCoverTests(unittest.TestCase):
    """A balloon over a painted region taller than its text keeps the text width its wrap needs.

    The taller shape takes more corner clearance, which narrows the padded text area; a box sized for the
    text alone then re-wraps the copy to an extra line and the fit check says "copy does not fit its reserve".
    """

    SIZE = (2400, 1000)
    TEXT = 'Look at his hands...'

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.dir = Path(self.temporary.name)

    def plan(self, region, text=None, faces=None, slot_height=153.75, tail=(.5, .95)):
        from test_reserves import frame
        path = self.dir / 'tall.png'
        frame(size=self.SIZE, boxes=[region]).save(path)
        panel = {'id': 'page-01-panel-01', 'page': 1, 'copy': [{'speaker': 'VOICE', 'text': text or self.TEXT}]}
        script = {'pages': {'1': {'panels': [panel]}}}
        slot = {'id': panel['id'], 'rect_pt': [36, 56.25, 369, slot_height]}
        tails = r.parse_tails({'0': list(tail)}, panel['copy'], *self.SIZE)
        zones = r.parse_faces(faces, *self.SIZE) if faces else []
        found = r.drawn_geometry(path, panel['copy'], slot, tails, zones)
        row = {'id': panel['id'], 'path': str(path), 'width': self.SIZE[0], 'height': self.SIZE[1]}
        return found, r.drawn_fits(row, panel, slot, tails, zones, script)

    def test_a_region_taller_than_the_text_no_longer_narrows_the_balloon_below_its_wrap(self):
        import reserves as rv
        found, fits = self.plan((900, 100, 1020, 290))                 # a 190 px painted box: its cover is 206 px tall
        x0, y0, x1, y1 = found['reserves'][0]['rect']
        bx0, by0, bx1, by1 = rv.find_regions(self.dir / 'tall.png', 1)['regions'][0]['bbox']
        self.assertTrue(fits)
        self.assertTrue(x0 <= bx0 - 8 and y0 <= by0 - 8 and x1 >= bx1 + 8 and y1 >= by1 + 8)     # still covers the region
        self.assertGreater(y1 - y0, 190)                               # the tall cover is what made it taller than the text
        self.assertGreater(x1 - x0, 472)                               # wider than the 472 px the text alone needed

    def test_a_region_no_taller_than_the_text_is_placed_exactly_as_before(self):
        found, fits = self.plan((900, 100, 1020, 240))
        self.assertTrue(fits)
        self.assertEqual(found['reserves'][0]['rect'], [724, 81, 1196, 260])

    def test_a_balloon_widened_for_a_tall_region_stays_clear_of_a_face(self):
        import reserves as rv
        face = {'x': 1190 / 2400, 'y': 200 / 1000, 'r': 40 / 1000}
        zone = (1190.0, 200.0, 40.0, 'face')
        # The speaker's mouth was at (.5, .95), far below the balloon: with the tail-tip rule the tip of such a long tail
        # ends nearer the face than the speaker, so the planner takes a narrower wrap and the widening shows nothing.
        # A nearer speaker, at (.5, .8), keeps this test on what it is about: the widened box keeping clear of the face.
        free, _ = self.plan((900, 100, 1020, 290), tail=(.5, .8))
        self.assertLess(rv.face_gap(free['reserves'][0]['rect'], .45, zone), 6)    # unconstrained, it would sit on the face
        found, fits = self.plan((900, 100, 1020, 290), faces=[face], tail=(.5, .8))    # was (.5, .95): see below
        reserve = found['reserves'][0]
        self.assertTrue(fits)
        self.assertGreaterEqual(rv.face_gap(reserve['rect'], reserve.get('corner', .45), zone), 6)
        self.assertGreater(reserve['rect'][2] - reserve['rect'][0], 472)            # and it is still widened

    def test_a_widened_balloon_beside_the_frame_edge_stays_inside_the_frame(self):
        found, fits = self.plan((20, 100, 140, 290))
        x0, y0, x1, y1 = found['reserves'][0]['rect']
        self.assertTrue(fits)
        self.assertTrue(0 <= x0 < x1 <= self.SIZE[0] and 0 <= y0 < y1 <= self.SIZE[1])

    def test_a_caption_is_not_widened(self):
        from test_reserves import frame
        path = self.dir / 'cap.png'
        frame(size=self.SIZE, boxes=[(900, 100, 1020, 290)]).save(path)
        copy = [{'speaker': 'CAPTION', 'text': self.TEXT}]
        slot = {'id': 'page-01-panel-01', 'rect_pt': [36, 56.25, 369, 153.75]}
        found = r.drawn_geometry(path, copy, slot, [None], [])
        self.assertEqual(found['reserves'][0]['rect'], [748, 96, 1173, 295])   # as before: a rectangle has no corner clearance


class RealTallCoverTests(unittest.TestCase):
    """The two chapter 4 panels the ratio-only fit broke, and every placement the fix must leave alone."""

    def setUp(self):
        import script_pipeline as s
        self.package = r.V15 / 'chapters' / 'ch04'
        try:
            self.job = json.loads((self.package / 'IMAGEGEN-JOBS.json').read_text())
            self.lean = json.loads((self.package / 'review' / 'LEAN-SELECTION-drawn-merged-r2.json').read_text())['decisions']
        except (OSError, ValueError):
            self.skipTest('chapter 4 files are not readable')
        self.script = self.job['script']
        self.geometry_dir = self.package / 'review' / 'geometry-drawn-r4'
        self.panels = {p['id']: p for page in self.script['pages'].values() for p in page['panels']}

    def inputs(self, stem):
        from PIL import Image
        panel_id = stem.rsplit('-v', 1)[0]
        record = json.loads((self.package / 'candidates' / f'{stem}.json').read_text())
        frame = r.frame_file(record, self.package)
        with Image.open(frame) as image:
            width, height = image.size
        panel = self.panels[panel_id]
        tails = r.parse_tails(json.loads((self.geometry_dir / f'{stem}-tails.json').read_text()), panel['copy'], width, height)
        raw = json.loads((self.geometry_dir / f'{stem}-faces.json').read_text())
        faces = r.parse_faces([dict(face, r=face['r'] * .55) for face in raw], width, height)
        return panel, frame, {'id': panel_id, 'path': str(frame), 'width': width, 'height': height}, tails, faces

    def placed(self, stem, slot_height, width=369):
        panel, frame, row, tails, faces = self.inputs(stem)
        slot = {'id': panel['id'], 'rect_pt': [36, 56.25, width, slot_height]}
        try:
            plan = r.drawn_geometry(frame, panel['copy'], slot, tails, faces)
        except r.AutoGeometryError as error:
            return None, str(error)
        return plan, r.drawn_fits(row, panel, slot, tails, faces, self.script)

    def test_page_01_panel_04_in_a_109_7_pt_row_is_now_refused_for_a_tail_through_the_next_balloon(self):
        # Deliberately changed: this pick used to fit here (its tall painted regions widened to keep their wrap, which
        # TallCoverTests still covers). Its first voice's tail now runs through the painted balloon of the next, so the
        # planner refuses it, naming both chunks, rather than place a balloon whose tail reads as pointing at the wrong one.
        plan, message = self.placed('page-01-panel-04-v01', 109.7)
        self.assertIsNone(plan)
        self.assertIn("chunk 1: its tail would cross chunk 2's balloon", message)

    def test_page_06_panel_03_in_a_184_5_pt_row_fits(self):
        plan, fits = self.placed('page-06-panel-03-v03', 184.5)
        self.assertIsNotNone(plan)
        self.assertTrue(fits)

    def test_every_placement_the_fit_check_passed_before_is_unchanged(self):
        # The golden holds the planner's output with the cover crop (its visible_rects are crops); the one from before
        # the crop is in review/ as golden_ch04_drawn_planner.json.backup-pre-cover-crop.
        golden = json.loads((Path(__file__).resolve().parent / 'golden_ch04_drawn_planner.json').read_text())
        checked = 0
        for name, layout in golden['layouts'].items():
            geometry = __import__('compositor').geometry_for_script(self.script, layout)
            for stem, before in golden['placements'][name].items():
                panel, frame, row, tails, faces = self.inputs(stem)
                slot = next(p for p in geometry['pages'][str(panel['page'])] if p['id'] == panel['id'])
                with self.subTest(layout=name, pick=stem):
                    plan = r.drawn_geometry(frame, panel['copy'], slot, tails, faces)
                    self.assertEqual({'visible_rect': plan['visible_rect'], 'reserves': plan['reserves']}, before)
                    checked += 1
        self.assertGreaterEqual(checked, 60)

    def test_the_fix_recovers_the_broken_picks_under_the_ratio_only_layout_without_losing_others(self):
        import compositor as c
        golden = json.loads((Path(__file__).resolve().parent / 'golden_ch04_drawn_planner.json').read_text())
        geometry = c.geometry_for_script(self.script, golden['layouts']['ratio'])
        passed = 0
        for decision in self.lean:
            if not decision['pick']:
                continue
            stem = f"{decision['id']}-{decision['pick']}"
            panel, frame, row, tails, faces = self.inputs(stem)
            slot = next(p for p in geometry['pages'][str(panel['page'])] if p['id'] == panel['id'])
            try:
                r.drawn_geometry(frame, panel['copy'], slot, tails, faces)
            except r.AutoGeometryError:
                continue
            passed += r.drawn_fits(row, panel, slot, tails, faces, self.script)
        # 21 before the fix, plus the two it broke, less page-05-panel-05-v05: in this layout it only fitted with its
        # answer lettered above the question, which the reading order rule now refuses (2026-10-01).
        self.assertGreaterEqual(passed, 22)


class RepairPlacementTests(unittest.TestCase):
    """A later chunk stopped by an earlier chunk's box is placed once that box is barred from the spot it took."""

    def test_chapter_2_page_5_panel_5_places_its_four_lines_in_order(self):
        # Two officer lines, a sailor line and a caption in one hatch shot: the greedy order gave the officer's first line
        # the sky beside him and left his second line no place whose tail did not cross it (2026-10-01).
        import reserves as rv
        import script_pipeline as s
        pkg = r.V15 / 'chapters' / 'ch02'
        try:
            decisions = json.loads((pkg / 'review' / 'LEAN-SELECTION-drawn-merged-d3.json').read_text())['decisions']
            faces_file = json.loads((pkg / 'review' / 'FACES-v5.json').read_text())['panels']
            keep_file = json.loads((pkg / 'review' / 'KEEP-c4.json').read_text())['panels']
            script = s.parse_script(r.V15 / 'scripts' / 'CHAPTER-02-SCRIPT.md')
        except (OSError, ValueError):
            self.skipTest('chapter 2 files are not readable')
        pid, version = 'page-05-panel-05', 'v10'
        frame = pkg / 'frames' / f'{pid}-{version}.png'
        if not frame.is_file():
            self.skipTest('frame missing')
        panel = next(p for page in script['pages'].values() for p in page['panels'] if p['id'] == pid)
        decision = next(d for d in decisions if d['id'] == pid)
        tails = r.parse_tails({str(t['copy_index']): [t['x'], t['y']] for t in decision['tails']}, panel['copy'], 1536, 1024)
        faces = r.parse_faces(next(p for p in faces_file if (p['id'], p['version']) == (pid, version))['faces'], 1536, 1024)
        keep = r.parse_keep([{k: z[k] for k in ('x0', 'y0', 'x1', 'y1')}
                             for z in next(p for p in keep_file if (p['id'], p['version']) == (pid, version))['keep']], 1536, 1024)
        plan = r.drawn_geometry(frame, panel['copy'], {'id': pid, 'rect_pt': [36, 56.25, 369, 194]}, tails, faces, keep=keep)
        boxes = [x['rect'] for x in sorted(plan['reserves'], key=lambda x: x['copy_indices'][0])]
        self.assertEqual(len(boxes), 4)
        for i in range(4):
            for j in range(i):
                self.assertTrue(rv._reads_after(boxes[j], boxes[i]), (j, i, boxes))


class FitLayoutCommandTests(PackageCase):
    """fit-layout: re-balance a chapter's row heights for its lettering, without touching LAYOUT.json."""

    SCRIPT_TEXT = LONG_SCRIPT

    def setUp(self):
        super().setUp()
        self.capture(self.generated('a.png', boxes=PAINTED, size=BIG), PANEL)
        self.capture(self.generated('s.png', boxes=[], size=BIG), SILENT)
        self.prior = self.root / 'prior.json'
        self.prior.write_text(json.dumps({'page_rows': {'1': [100, 421.5]}}))
        self.layout_out = self.root / 'fitted.json'

    def frame_row(self, panel, version='v01'):
        record = json.loads(self.candidate_path(panel, version).read_text())
        return {key: record[key] for key in ('id', 'path', 'width', 'height')} | {'visible_rect': [0, 0, 2400, 1000]}

    def manifest(self, panels=(PANEL, SILENT), name='manifest.json'):
        path = self.root / name
        path.write_text(json.dumps({'frames': [self.frame_row(panel) for panel in panels]}))
        return path

    def fit(self, *extra, manifest=None):
        return self.run_cli('fit-layout', '--manifest', str(manifest or self.manifest()), '--layout', str(self.prior),
                            '--layout-out', str(self.layout_out), *extra)

    def fails(self, *argv):
        with self.assertRaises(SystemExit) as caught:
            self.run_cli('fit-layout', *argv)
        return str(caught.exception.code)

    def test_writes_a_layout_that_geometry_for_script_accepts_and_reports_before_and_after(self):
        import compositor as c
        result = self.fit()
        layout = json.loads(self.layout_out.read_text())
        import script_pipeline as s
        script = s.parse_script(Path(r.load_job(self.pkg)['script']['path']))
        geometry = c.geometry_for_script(script, layout['page_rows'])
        self.assertEqual(sorted(geometry['pages']), ['1'])
        rows = layout['page_rows']['1']
        self.assertAlmostEqual(sum(rows) + c.GAP_PT * (len(rows) - 1), c.STORY_HEIGHT_PT, places=9)
        self.assertGreater(rows[0], 100)                                   # the two-line strip grows
        self.assertLess(rows[1], 421.5)                                    # the silent one gives height up
        self.assertEqual(result['layout_out'], str(self.layout_out))
        page = result['pages']['1']
        self.assertEqual([row['prior_pt'] for row in page['rows']], [100, 421.5])
        self.assertEqual([row['new_pt'] for row in page['rows']], rows)
        self.assertGreater(page['min_ratio_after'], page['min_ratio_before'])
        self.assertIn(page['status'], ('ok', 'tight', 'cannot_fit'))
        self.assertEqual(json.loads(self.prior.read_text()), {'page_rows': {'1': [100, 421.5]}})

    def test_refuses_to_overwrite_and_needs_its_inputs(self):
        self.layout_out.write_text('keep me')
        self.assertIn('exists', self.fails('--manifest', str(self.manifest()), '--layout', str(self.prior),
                                           '--layout-out', str(self.layout_out)))
        self.assertEqual(self.layout_out.read_text(), 'keep me')
        self.layout_out.unlink()
        for missing, argv in (('--manifest', ['--layout', str(self.prior), '--layout-out', str(self.layout_out)]),
                              ('--layout', ['--manifest', str(self.manifest()), '--layout-out', str(self.layout_out)]),
                              ('--layout-out', ['--manifest', str(self.manifest()), '--layout', str(self.prior)])):
            with self.subTest(missing=missing):
                self.assertIn(missing, self.fails(*argv))
        self.assertFalse(self.layout_out.exists())

    def test_a_bad_prior_layout_fails_cleanly_and_writes_nothing(self):
        self.prior.write_text(json.dumps({'page_rows': {'1': [100, 100]}}))        # does not fill the page
        self.assertIn('do not fill', self.fails('--manifest', str(self.manifest()), '--layout', str(self.prior),
                                                '--layout-out', str(self.layout_out)))
        self.prior.write_text(json.dumps({'page_rows': {'1': [100, 100, 319.5]}}))    # three rows for two panels
        self.assertIn('panel count', self.fails('--manifest', str(self.manifest()), '--layout', str(self.prior),
                                                '--layout-out', str(self.layout_out)))
        self.assertFalse(self.layout_out.exists())

    def test_frames_come_from_the_manifest_and_picks_fill_in_the_rest(self):
        only_first = self.manifest(panels=(PANEL,), name='partial.json')
        decisions = self.root / 'decisions.json'
        decisions.write_text(json.dumps({'decisions': [{'id': PANEL, 'pick': 'v01'}, {'id': SILENT, 'pick': 'v01'}]}))
        inputs = r.fit_inputs(self.pkg, only_first, decisions)
        self.assertEqual(sorted(inputs['frames']), [PANEL, SILENT])
        self.assertEqual(inputs['frames'][SILENT]['visible_rect'], [0, 0, 2400, 1000])
        self.assertEqual(inputs['frames'][SILENT]['width'], 2400)
        self.assertEqual(inputs['sources'], {PANEL: 'manifest', SILENT: 'pick v01'})
        # With neither a frame nor a pick, a panel is fitted as art that fills its slot.
        none = r.fit_inputs(self.pkg, only_first, None)
        self.assertEqual(sorted(none['frames']), [PANEL])
        result = self.fit(manifest=only_first)
        self.assertEqual(result['pages']['1']['panels'][SILENT]['frame'], 'none')

    def test_a_row_made_after_the_cover_crop_is_fitted_on_its_art_rect_not_its_cropped_visible_rect(self):
        row = self.frame_row(PANEL) | {'visible_rect': [0, 200, 2400, 840], 'art_rect': [0, 0, 2400, 1000]}
        path = self.root / 'cropped.json'
        path.write_text(json.dumps({'frames': [row, self.frame_row(SILENT)]}))
        inputs = r.fit_inputs(self.pkg, path)
        self.assertEqual(inputs['frames'][PANEL]['visible_rect'], [0, 0, 2400, 1000])      # the key keeps its name, now the art
        self.assertEqual(inputs['frames'][SILENT]['visible_rect'], [0, 0, 2400, 1000])     # no art_rect: as before
        plain = self.frame_row(PANEL) | {'visible_rect': [0, 200, 2400, 840]}
        path.write_text(json.dumps({'frames': [plain]}))
        self.assertEqual(r.fit_inputs(self.pkg, path)['frames'][PANEL]['visible_rect'], [0, 200, 2400, 840])

    def test_a_pick_s_candidate_record_is_fitted_on_its_art_rect_too(self):
        record_path = self.candidate_path(SILENT)
        record = json.loads(record_path.read_text())
        decisions = self.root / 'decisions.json'
        decisions.write_text(json.dumps({'decisions': [{'id': SILENT, 'pick': 'v01'}]}))
        only_first = self.manifest(panels=(PANEL,), name='partial.json')
        record_path.write_text(json.dumps(record | {'visible_rect': [0, 100, 2400, 900], 'art_rect': [0, 0, 2400, 1000]}))
        self.assertEqual(r.fit_inputs(self.pkg, only_first, decisions)['frames'][SILENT]['visible_rect'], [0, 0, 2400, 1000])
        record_path.write_text(json.dumps(record | {'visible_rect': [0, 100, 2400, 900]}))
        self.assertEqual(r.fit_inputs(self.pkg, only_first, decisions)['frames'][SILENT]['visible_rect'], [0, 100, 2400, 900])

    def test_a_pick_without_a_frame_or_a_record_is_named(self):
        decisions = self.root / 'decisions.json'
        decisions.write_text(json.dumps({'decisions': [{'id': SILENT, 'pick': 'v09'}]}))
        with self.assertRaisesRegex(ValueError, SILENT):
            r.fit_inputs(self.pkg, self.manifest(panels=(PANEL,), name='partial.json'), decisions)

    def test_faces_are_read_by_frame_version_and_scaled(self):
        faces = self.root / 'faces'
        faces.mkdir()
        (faces / f'{PANEL}-v01-faces.json').write_text(json.dumps([{'x': .3, 'y': .4, 'r': .2}]))
        inputs = r.fit_inputs(self.pkg, self.manifest(), None, faces, .5)
        self.assertEqual(inputs['faces'], {PANEL: [(.3, .4, .1)]})
        self.assertNotIn(SILENT, inputs['faces'])
        with_faces = self.fit('--faces-dir', str(faces), '--face-scale', '0.5')
        self.assertGreater(with_faces['pages']['1']['panels'][PANEL]['faces_share'], 0)
        self.layout_out.unlink()
        without = self.fit()
        self.assertEqual(without['pages']['1']['panels'][PANEL]['faces_share'], 0)

    def test_face_files_are_read_as_written_by_default(self):
        # The assembler writes <stem>-faces.json with radii already scaled for auto-geometry, which reads
        # them as they are; scaling them again here would let the probe pass layouts the planner rejects.
        faces = self.root / 'faces'
        faces.mkdir()
        (faces / f'{PANEL}-v01-faces.json').write_text(json.dumps([{'x': .3, 'y': .4, 'r': .2}]))
        inputs = r.fit_inputs(self.pkg, self.manifest(), None, faces)
        self.assertEqual(inputs['faces'], {PANEL: [(.3, .4, .2)]})
        self.assertEqual(self.fit('--faces-dir', str(faces))['face_scale'], 1.0)

    def test_painted_regions_are_measured_as_the_planner_keeps_them_and_silent_panels_have_none(self):
        import reserves as rv
        import script_pipeline as s
        script = s.parse_script(Path(r.load_job(self.pkg)['script']['path']))
        inputs = r.fit_inputs(self.pkg, self.manifest(), script=script)
        regions = rv.find_regions(inputs['frames'][PANEL]['path'], 2)['regions']
        self.assertEqual(len(regions), 2)
        expected = []
        for region in regions:                                      # the same extent _crop_keep gives the planner
            (x, y), (h, w) = region['painted']['origin'], region['painted']['mask'].shape
            expected.append([x / 2400, y / 1000, (x + w) / 2400, (y + h) / 1000])
        self.assertEqual(inputs['painted'], {PANEL: expected})
        self.assertNotIn(SILENT, inputs['painted'])
        self.assertEqual(inputs['keep'], {})
        # Without the script nothing is measured: the copy counts come from it.
        self.assertEqual(r.fit_inputs(self.pkg, self.manifest())['painted'], {})

    def test_the_painted_regions_are_found_once_per_frame(self):
        import reserves as rv
        import script_pipeline as s
        script = s.parse_script(Path(r.load_job(self.pkg)['script']['path']))
        with mock.patch.object(rv, 'find_regions', wraps=rv.find_regions) as spy:
            first = r.fit_inputs(self.pkg, self.manifest(), script=script)
            second = r.fit_inputs(self.pkg, self.manifest(), script=script)
        self.assertEqual(first['painted'], second['painted'])
        self.assertEqual(spy.call_count, 1)                            # the silent panel's frame is never searched

    def test_keep_files_are_read_by_frame_version_as_fractions(self):
        folder = self.root / 'keep'
        folder.mkdir()
        zone = {'x0': .1, 'y0': .6, 'x1': .3, 'y1': .9, 'what': 'the brand'}
        (folder / f'{PANEL}-v01-keep.json').write_text(json.dumps([zone]))
        (folder / f'{SILENT}-v01-keep.json').write_text(json.dumps([dict(zone, x0=.2)]))
        inputs = r.fit_inputs(self.pkg, self.manifest(), None, folder)
        self.assertEqual(inputs['keep'], {PANEL: [[.1, .6, .3, .9]], SILENT: [[.2, .6, .3, .9]]})
        self.assertEqual(r.fit_inputs(self.pkg, self.manifest())['keep'], {})                # no faces dir: none
        (folder / f'{PANEL}-v01-keep.json').write_text(json.dumps([dict(zone, x1=.05)]))
        with self.assertRaises(r.LayoutFitError) as caught:
            r.fit_inputs(self.pkg, self.manifest(), None, folder)
        self.assertIn(f'{PANEL}-v01-keep.json', str(caught.exception))

    def test_the_fit_holds_the_keep_zones_and_painted_regions_like_the_planner(self):
        folder = self.root / 'keep'
        folder.mkdir()
        (folder / f'{PANEL}-v01-keep.json').write_text(json.dumps([{'x0': .4, 'y0': 0, 'x1': .6, 'y1': 1}]))   # the frame's full height
        held = self.fit('--faces-dir', str(folder))
        self.assertEqual(held['keep'], [PANEL])
        self.assertEqual(held['painted'], [PANEL])
        panel = held['pages']['1']['panels'][PANEL]
        self.layout_out.unlink()
        plain = self.fit()
        self.assertEqual(plain['keep'], [])
        self.assertEqual(plain['painted'], [PANEL])
        self.assertLess(panel['fill_before'], plain['pages']['1']['panels'][PANEL]['fill_before'])   # the crop cannot narrow

    def test_the_probe_hands_keep_zones_to_the_planner_and_fit_layout_gets_them_with_the_painted_regions(self):
        import layout_fit as lf
        folder = self.probe_folder()
        (folder / f'{PANEL}-v01-keep.json').write_text(json.dumps([{'x0': .125, 'y0': .625, 'x1': .25, 'y1': .875}]))
        seen = []

        def placed(row, panel, slot, tails, faces, script):
            seen.append(row.get('keep'))
            return True
        with mock.patch.object(r, 'drawn_fits', side_effect=placed), \
                mock.patch.object(lf, 'fit_layout', wraps=lf.fit_layout) as fit:
            self.fit('--faces-dir', str(folder), '--probe')
        self.assertTrue(seen)
        self.assertTrue(all(keep == [[300.0, 625.0, 600.0, 875.0]] for keep in seen))            # source pixels of the 2400 x 1000 frame
        for call in fit.call_args_list:
            self.assertEqual(call.kwargs['keep'], {PANEL: [[.125, .625, .25, .875]]})
            self.assertEqual(list(call.kwargs['painted']), [PANEL])

    def test_drawn_fits_gives_the_planner_the_rows_keep_zones(self):
        import script_pipeline as s
        script = s.parse_script(Path(r.load_job(self.pkg)['script']['path']))
        panel = {p['id']: p for page in script['pages'].values() for p in page['panels']}[PANEL]
        record = json.loads(self.candidate_path(PANEL).read_text())
        row = {'id': PANEL, 'path': record['path'], 'width': record['width'], 'height': record['height'], 'keep': [[1.0, 2.0, 3.0, 4.0]]}
        slot = {'id': PANEL, 'rect_pt': [36, 56.25, 369, 100]}
        with mock.patch.object(r, 'drawn_geometry', side_effect=r.AutoGeometryError('stop')) as plan:
            self.assertFalse(r.drawn_fits(row, panel, slot, [None, (1200.0, 950.0)], [], script))
        self.assertEqual(plan.call_args.kwargs['keep'], [[1.0, 2.0, 3.0, 4.0]])
        row.pop('keep')
        with mock.patch.object(r, 'drawn_geometry', side_effect=r.AutoGeometryError('stop')) as plan:
            r.drawn_fits(row, panel, slot, [None, (1200.0, 950.0)], [], script)
        self.assertIsNone(plan.call_args.kwargs['keep'])

    def probe_folder(self):
        folder = self.root / 'geometry'
        folder.mkdir()
        (folder / f'{PANEL}-v01-tails.json').write_text(json.dumps({'1': [.5, .95]}))
        return folder

    def auto_draw(self, layout, name):
        folder = self.root / 'geometry'
        return self.run_cli('auto-geometry', '--candidate', str(self.candidate_path()), '--geometry-out',
                            str(self.root / name), '--draw', '--tails', str(folder / f'{PANEL}-v01-tails.json'),
                            '--layout', str(layout))

    def test_probe_asks_the_planner_and_the_fitted_layout_places_a_panel_the_prior_could_not(self):
        folder = self.probe_folder()
        self.prior.write_text(json.dumps({'page_rows': {'1': [60, 461.5]}}))
        with self.assertRaises(SystemExit) as caught:                        # the strip is too short for its balloons
            self.auto_draw(self.prior, 'drawn-prior.json')
        self.assertIn('cannot be placed', str(caught.exception.code))
        result = self.fit('--faces-dir', str(folder), '--probe')
        probe = result['probe']
        self.assertGreater(probe['floors'][PANEL], 60)
        self.assertEqual(probe['verified'], {PANEL: True})
        self.assertEqual((probe['unplaceable'], probe['pins'], probe['unprobed']), ([], {}, []))
        self.assertGreater(probe['planner_calls'], 0)
        row = result['pages']['1']['rows'][0]
        self.assertTrue(row['floor_met'])
        self.assertGreaterEqual(row['new_pt'], probe['floors'][PANEL])
        self.assertEqual(result['pages']['1']['status'], 'ok')
        self.auto_draw(self.layout_out, 'drawn-fitted.json')                       # the fitted layout places it
        self.assertTrue((self.root / 'drawn-fitted.json').is_file())

    def test_probe_needs_the_faces_dir_and_is_scoped_to_fit_layout(self):
        self.assertIn('--faces-dir', self.fails('--manifest', str(self.manifest()), '--layout', str(self.prior),
                                                '--layout-out', str(self.layout_out), '--probe'))
        self.assertFalse(self.layout_out.exists())
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.run_cli('next-job', '--probe')

    def test_a_panel_that_fails_at_the_height_the_fit_chose_is_pinned_to_the_nearest_that_works(self):
        folder = self.probe_folder()
        self.prior.write_text(json.dumps({'page_rows': {'1': [60, 461.5]}}))
        placed = lambda row, panel, slot, tails, faces, script: 90 <= slot['rect_pt'][3] < 110    # a window, not a floor
        with mock.patch.object(r, 'drawn_fits', side_effect=placed):
            result = self.fit('--faces-dir', str(folder), '--probe')
        layout = json.loads(self.layout_out.read_text())['page_rows']['1']
        self.assertTrue(90 <= layout[0] < 110)
        self.assertEqual(result['probe']['pins'], {PANEL: layout[0]})
        self.assertEqual(result['probe']['verified'], {PANEL: True})
        self.assertGreater(result['probe']['rounds'], 1)
        self.assertAlmostEqual(layout[0] + layout[1] + 2, 523.5, places=9)

    def test_a_narrow_window_between_scan_steps_is_found_by_the_verification(self):
        folder = self.probe_folder()
        placed = lambda row, panel, slot, tails, faces, script: 121 <= slot['rect_pt'][3] <= 124   # between 5 pt steps
        with mock.patch.object(r, 'drawn_fits', side_effect=placed):
            result = self.fit('--faces-dir', str(folder), '--probe')
        probe = result['probe']
        layout = json.loads(self.layout_out.read_text())['page_rows']['1']
        self.assertEqual(probe['floors'], {})                                # the scan missed it
        self.assertEqual(probe['off_grid'], [PANEL])
        self.assertEqual((probe['unplaceable'], probe['verified']), ([], {PANEL: True}))
        self.assertTrue(121 <= layout[0] <= 124)
        self.assertEqual(probe['pins'], {PANEL: layout[0]})

    def test_a_panel_no_height_can_place_is_reported_and_left_to_the_ratio_fit(self):
        folder = self.probe_folder()
        with mock.patch.object(r, 'drawn_fits', return_value=False):
            result = self.fit('--faces-dir', str(folder), '--probe')
        probe = result['probe']
        self.assertEqual(probe['unplaceable'], [PANEL])
        self.assertEqual(probe['verified'], {PANEL: False})
        self.assertEqual(probe['floors'], {})
        self.assertNotIn('floor_pt', result['pages']['1']['rows'][0])
        layout = json.loads(self.layout_out.read_text())['page_rows']['1']
        self.assertGreater(layout[0], 100)                                   # still the ratio fit

    def test_panels_without_a_tails_file_are_listed_as_unprobed(self):
        folder = self.root / 'empty'
        folder.mkdir()
        result = self.fit('--faces-dir', str(folder), '--probe')
        self.assertEqual(result['probe']['unprobed'], [PANEL])
        self.assertEqual(result['probe']['verified'], {})
        self.assertEqual(result['probe']['planner_calls'], 0)

    def test_a_malformed_faces_file_names_the_file(self):
        faces = self.root / 'faces'
        faces.mkdir()
        (faces / f'{PANEL}-v01-faces.json').write_text(json.dumps({'x': 1}))
        message = self.fails('--manifest', str(self.manifest()), '--layout', str(self.prior),
                             '--layout-out', str(self.layout_out), '--faces-dir', str(faces))
        self.assertIn(f'{PANEL}-v01-faces.json', message)
        self.assertFalse(self.layout_out.exists())

    def test_margin_option_is_used(self):
        result = self.fit('--margin', '1.5')
        self.assertEqual(result['margin'], 1.5)

    def rewrite_script(self, old, new):
        """Change a line of the chapter script (and the hash the job records for it), to give a panel a layout cue."""
        text = self.script.read_text(encoding='utf-8')
        self.assertIn(old, text)
        self.script.write_text(text.replace(old, new), encoding='utf-8')
        job_path = self.pkg / 'IMAGEGEN-JOBS.json'
        job = json.loads(job_path.read_text())
        job['script']['sha256'] = sha(self.script)
        job_path.write_text(json.dumps(job))

    def test_structures_chooses_each_pages_rows_and_reports_the_alternatives(self):
        import compositor as c
        import script_pipeline as s
        result = self.fit('--structures')
        structure = result['pages']['1']['structure']
        self.assertEqual(structure['prior'], [1, 1])
        self.assertEqual(sum(structure['chosen']), 2)
        self.assertEqual(sorted(tuple(alt['structure']) for alt in structure['alternatives']), [(1, 1), (2,)])
        for alt in structure['alternatives']:
            self.assertEqual(set(alt), {'structure', 'rows_pt', 'min_fill', 'mean_fill', 'min_ratio', 'cues_ok', 'verified',
                                        'prior', 'chosen'})
            self.assertIsNone(alt['verified'])
        self.assertEqual([alt['chosen'] for alt in structure['alternatives']].count(True), 1)
        self.assertEqual((structure['candidates'], structure['excluded'], structure['verified']), (2, 0, None))
        self.assertEqual(result['structure_search'],
                         {'row_sizes': [1, 2], 'pages_changed': int(structure['chosen'] != [1, 1]), 'probe_top': None})
        layout = json.loads(self.layout_out.read_text())
        self.assertTrue(layout['fitted_from']['structures'])
        script = s.parse_script(Path(r.load_job(self.pkg)['script']['path']))
        rows = layout['page_rows']['1']
        self.assertEqual(len(rows), len(structure['chosen']))
        self.assertEqual([len(row) if isinstance(row, list) else 1 for row in rows], structure['chosen'])
        c.geometry_for_script(script, layout['page_rows'])
        self.assertAlmostEqual(sum(row[0] if isinstance(row, list) else row for row in rows) + c.GAP_PT * (len(rows) - 1),
                               c.STORY_HEIGHT_PT, places=9)
        self.assertEqual(json.loads(self.prior.read_text()), {'page_rows': {'1': [100, 421.5]}})

    def test_without_structures_the_fit_and_its_layout_file_are_unchanged(self):
        result = self.fit()
        self.assertNotIn('structure', result['pages']['1'])
        self.assertNotIn('structure_search', result)
        self.assertNotIn('structures', json.loads(self.layout_out.read_text())['fitted_from'])

    def test_structures_reads_the_layout_cues_from_the_script(self):
        self.rewrite_script('**1.1** Wide panel.', '**1.1** Full width, wide panel.')
        structure = self.fit('--structures')['pages']['1']['structure']
        self.assertEqual(structure['chosen'], [1, 1])
        self.assertEqual([alt['structure'] for alt in structure['alternatives']], [[1, 1]])     # the pair is not tried
        self.assertEqual((structure['candidates'], structure['excluded']), (2, 1))
        cue = structure['cues'][PANEL]
        self.assertEqual((cue['solo'], cue['min_share']), (True, None))
        self.assertGreater(cue['min_pt'], 0)                  # full width floors the row where the art spans the column

    def test_structures_honours_a_size_cue_the_prior_heights_cannot_meet(self):
        self.rewrite_script('**1.1** Wide panel.', '**1.1** Large, top half of the page. Wide panel.')
        result = self.fit('--structures')
        page = result['pages']['1']
        self.assertEqual(page['structure']['cues'], {PANEL: {'solo': False, 'min_share': .5, 'min_pt': 235.6}})
        row = next(row for row in page['rows'] if PANEL in row['panels'])
        self.assertGreaterEqual(row['new_pt'], 235.6)
        self.assertTrue(row['cue_met'])
        prior = next(alt for alt in page['structure']['alternatives'] if alt['prior'])          # 2 x 100 pt is under 235.6
        self.assertFalse(prior['cues_ok'])
        self.assertTrue(next(alt for alt in page['structure']['alternatives'] if alt['chosen'])['cues_ok'])

    def test_structures_with_the_probe_verifies_each_candidate_with_the_planner(self):
        folder = self.probe_folder()
        with mock.patch.object(r, 'drawn_fits', return_value=True):
            result = self.fit('--faces-dir', str(folder), '--probe', '--structures')
        structure = result['pages']['1']['structure']
        self.assertIs(structure['verified'], True)
        self.assertEqual([alt['verified'] for alt in structure['alternatives']], [True, True])       # both are in the top three
        self.assertEqual(result['structure_search']['probe_top'], 3)
        probe = result['probe']
        self.assertEqual((probe['verified'], probe['unplaceable'], probe['unprobed']), ({PANEL: True}, [], []))
        self.assertGreater(probe['planner_calls'], 0)

    def test_the_probe_chooses_a_structure_the_planner_can_place(self):
        folder = self.probe_folder()
        placed = lambda row, panel, slot, tails, faces, script: slot['rect_pt'][2] > 300       # a full-width row only
        with mock.patch.object(r, 'drawn_fits', side_effect=placed):
            result = self.fit('--faces-dir', str(folder), '--probe', '--structures')
        structure = result['pages']['1']['structure']
        self.assertEqual(structure['chosen'], [1, 1])
        self.assertTrue(structure['verified'])
        pair = next(alt for alt in structure['alternatives'] if alt['structure'] == [2])
        self.assertIs(pair['verified'], False)
        self.assertEqual(result['probe']['verified'], {PANEL: True})                   # the probe section is the chosen one's
        self.assertEqual(result['probe']['unplaceable'], [])

    def test_when_the_planner_places_nothing_the_best_candidate_stands_unverified(self):
        folder = self.probe_folder()
        with mock.patch.object(r, 'drawn_fits', return_value=False):
            result = self.fit('--faces-dir', str(folder), '--probe', '--structures')
        structure = result['pages']['1']['structure']
        self.assertIs(structure['verified'], False)
        self.assertEqual([alt['verified'] for alt in structure['alternatives']], [False, False])
        self.assertEqual(result['probe']['unplaceable'], [PANEL])
        self.assertEqual(result['probe']['verified'], {PANEL: False})
        self.assertTrue(self.layout_out.is_file())

    def test_probe_fit_scans_from_a_cue_minimum_and_can_share_its_probe(self):
        import layout_fit as lf
        import script_pipeline as s
        folder = self.probe_folder()
        script = s.parse_script(Path(r.load_job(self.pkg)['script']['path']))
        inputs = r.fit_inputs(self.pkg, self.manifest(), None, folder, 1.0, script)
        probe = r.SlotProbe(script, inputs, folder)
        with mock.patch.object(r, 'drawn_fits', return_value=True):
            plain = r.probe_fit(lf, script, {'1': [100, 421.5]}, inputs, folder, 3.0, probe=r.SlotProbe(script, inputs, folder))
            fitted = r.probe_fit(lf, script, {'1': [100, 421.5]}, inputs, folder, 3.0, probe=probe, minimums={PANEL: 150})
        self.assertEqual(plain['report']['probe']['floors'][PANEL], 60)                # its row's lower bound
        self.assertEqual(fitted['report']['probe']['floors'][PANEL], 150)              # the scan starts at the cue's minimum
        self.assertGreaterEqual(fitted['page_rows']['1'][0], 150)
        self.assertTrue(fitted['report']['pages']['1']['rows'][0]['cue_met'])
        self.assertEqual(fitted['report']['probe']['planner_calls'], probe.calls)      # the shared probe did the asking
        self.assertGreater(probe.calls, 0)

    def test_new_flags_are_scoped_to_fit_layout(self):
        with contextlib.redirect_stderr(io.StringIO()):
            for argv in (('next-job', '--layout-out', str(self.layout_out)), ('next-job', '--decisions', str(self.prior)),
                         ('next-job', '--faces-dir', str(self.root)), ('next-job', '--face-scale', '0.5'),
                         ('next-job', '--margin', '2'), ('next-job', '--probe'), ('next-job', '--structures')):
                with self.subTest(argv=argv), self.assertRaises(SystemExit):
                    self.run_cli(*argv)
        self.assertIsNone(self.run_cli('next-job'))        # both panels already have candidates


class UnpaintedTests(unittest.TestCase):
    """--unpainted: a chapter generated with no painted balloons has no painted regions to cover.

    Chapter 6 r1, 9.5: open sky left between a pillar and the roof read as a painted blank region; its balloon had to
    cover all of it, which reached the king's face at every row height, and the panel could not be lettered.
    """

    COPY = [{'speaker': 'CAPTION', 'text': 'The hall waited for the king.'}]
    SLOT = {'id': 'page-01-panel-01', 'rect_pt': [36, 300, 369, 153.75]}

    def setUp(self):
        from test_reserves import frame as painted_frame
        self.dir = Path(tempfile.mkdtemp())
        self.path = self.dir / 'pale.png'
        painted_frame(size=(2400, 1000), boxes=[(1300, 150, 2100, 420)]).save(self.path)   # a pale outlined area
        self.tails = r.parse_tails(None, self.COPY, 2400, 1000)
        self.faces = r.parse_faces([{'x': 0.9, 'y': 0.3, 'r': 0.08}], 2400, 1000)          # a face beside it

    def test_a_pale_area_is_open_space_not_a_region_to_cover_when_unpainted(self):
        with self.assertRaisesRegex(r.AutoGeometryError, 'painted region it must hide reaches face 0'):
            r.drawn_geometry(self.path, self.COPY, self.SLOT, self.tails, self.faces)            # as before
        plan = r.drawn_geometry(self.path, self.COPY, self.SLOT, self.tails, self.faces, unpainted=True)
        self.assertEqual(plan['painted'], [False])
        self.assertEqual(len(plan['reserves']), 1)

    def test_the_module_switch_sets_the_default(self):
        with mock.patch.object(r, 'UNPAINTED', True):
            plan = r.drawn_geometry(self.path, self.COPY, self.SLOT, self.tails, self.faces)
        self.assertEqual(plan['painted'], [False])

    def test_fit_inputs_measures_no_painted_regions_when_unpainted(self):
        manifest = self.dir / 'manifest.json'
        manifest.write_text(json.dumps({'frames': [{'id': 'page-01-panel-01', 'path': str(self.path), 'width': 2400,
                                                    'height': 1000, 'visible_rect': [0, 0, 2400, 1000]}]}))
        script = {'pages': {'1': {'panels': [{'id': 'page-01-panel-01', 'page': 1, 'copy': self.COPY}]}}}
        self.assertIn('page-01-panel-01', r.fit_inputs(self.dir, manifest, script=script)['painted'])
        self.assertEqual(r.fit_inputs(self.dir, manifest, script=script, unpainted=True)['painted'], {})

    def test_the_flag_applies_only_to_auto_geometry_and_fit_layout(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            r.main(['build', '--chapter', '1', '--unpainted'])


class MalayalamLetteringTests(unittest.TestCase):
    """Lines tagged (Malayalam) are lettered inside angle brackets, the chapter 4 convention for speech Nagoji cannot follow.

    Chapter 5 r2: its script tags 22 lines "(Malayalam)" and asks for a distinct treatment, but they were lettered as
    plain balloons, so Nagoji seemed to follow Malayalam unaided. The brackets are added where the runner reads the
    script for lettering; the script text and the image prompts are unchanged.
    """

    SCRIPT = ("# Chapter 5\n\n## PAGE 1\n\n**1.1** A hut.\n\n> IBRAHIM (Malayalam): Can he travel?\n\n"
              "> NAGOJI: I can ride.\n\n> GIRL (Malayalam): <Portuguese.>\n\n> GUARD (off, Malayalam): You come late, *kapitan*.\n")

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.path = self.dir / 'CHAPTER-05-SCRIPT.md'
        self.path.write_text(self.SCRIPT, encoding='utf-8')

    def texts(self, script):
        return [chunk['text'] for page in script['pages'].values() for panel in page['panels'] for chunk in panel['copy']]

    def test_malayalam_lines_are_bracketed_for_lettering_only(self):
        import script_pipeline as s
        self.assertEqual(self.texts(r.lettered_script(self.path)),
                         ['<Can he travel?>', 'I can ride.', '<Portuguese.>', '<You come late, *kapitan*.>'])
        self.assertEqual(self.texts(s.parse_script(self.path))[0], 'Can he travel?')     # the parsed script is unchanged

    def test_the_runner_letters_from_the_lettered_script(self):
        source = (Path(__file__).resolve().parent / 'run_chapter.py').read_text(encoding='utf-8')
        self.assertEqual(source.count("script=lettered_script(Path(job['script']['path']))"), 4)
        self.assertNotIn("script=s.parse_script(Path(job['script']['path']))", source)
