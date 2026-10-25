import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

import review_sheets as rs

COLOURS = {'v01': (200, 30, 30), 'v02': (30, 200, 30), 'v03': (30, 30, 200)}
DECOY = (255, 0, 255)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_frame(path, size, colour):
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new('RGB', size, colour).save(path)


def write_candidate(pkg, panel, version, size, colour):
    frame = pkg / 'frames' / f'{panel}-{version}.png'
    write_frame(frame, size, colour)
    record = {'id': panel, 'path': str(frame), 'sha256': sha(frame), 'width': size[0], 'height': size[1],
              'prompt_path': str(pkg / 'prompts' / f'{panel}.txt'), 'references': [], 'visual_review': 'pending'}
    (pkg / 'candidates').mkdir(parents=True, exist_ok=True)
    (pkg / 'candidates' / f'{panel}-{version}.json').write_text(json.dumps(record))
    return record


def make_package(root):
    pkg = Path(root) / 'pkg'
    (pkg / 'candidates').mkdir(parents=True)
    jobs = [{'id': 'page-01-panel-01', 'cast': ['nagoji', 'duarte']},
            {'id': 'page-01-panel-02', 'cast': []},
            {'id': 'page-02-panel-01', 'cast': ['varma']}]
    (pkg / 'IMAGEGEN-JOBS.json').write_text(json.dumps({'jobs': jobs}))
    for version, colour in COLOURS.items():
        write_candidate(pkg, 'page-01-panel-01', version, (2000, 760), colour)
    write_candidate(pkg, 'page-01-panel-02', 'v01', (800, 1200), (240, 200, 20))
    # Provenance files sit beside candidates but are not candidates.
    decoy = pkg / 'frames' / 'decoy.png'
    write_frame(decoy, (600, 300), DECOY)
    for version in COLOURS:
        (pkg / 'candidates' / f'page-01-panel-01-{version}-provenance.json').write_text(
            json.dumps({'id': 'page-01-panel-01', 'path': str(decoy), 'sha256': sha(decoy)}))
    return pkg


def near(image, colour):
    """Mask of pixels within 2 levels of a colour (resampling may shift a level)."""
    array = np.asarray(image.convert('RGB')).astype(int)
    return (np.abs(array - np.array(colour)) <= 2).all(axis=2)


def pixel_count(image, colour):
    return int(near(image, colour).sum())


def listing(root):
    return {str(p.relative_to(root)): (p.stat().st_mtime_ns, p.stat().st_size)
            for p in sorted(Path(root).rglob('*')) if p.is_file()}


class ReviewSheetTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.pkg = make_package(self.root)
        self.out = self.root / 'sheets'

    def test_one_sheet_per_panel_with_one_tile_per_candidate(self):
        index = rs.make_review_sheets(self.pkg, self.out)
        self.assertEqual(sorted(index), ['page-01-panel-01', 'page-01-panel-02', 'page-02-panel-01'])
        for panel, entry in index.items():
            self.assertTrue(Path(entry['sheet']).is_file(), panel)
            self.assertEqual(Path(entry['sheet']).parent, self.out.resolve())
        with Image.open(index['page-01-panel-01']['sheet']) as sheet:
            self.assertEqual(sheet.width, 1600)
            for colour in COLOURS.values():
                # Each 2000x760 frame is downscaled to fit; a real tile is thousands of pixels.
                self.assertGreater(pixel_count(sheet, colour), 100000)
            self.assertEqual(pixel_count(sheet, DECOY), 0)
        self.assertEqual([c['version'] for c in index['page-01-panel-01']['candidates']], ['v01', 'v02', 'v03'])
        with Image.open(index['page-01-panel-02']['sheet']) as sheet:
            self.assertEqual(sheet.width, 1600)
            self.assertGreater(pixel_count(sheet, (240, 200, 20)), 100000)
        with Image.open(index['page-02-panel-01']['sheet']) as sheet:
            self.assertEqual(sheet.width, 1600)
        self.assertEqual(index['page-02-panel-01']['candidates'], [])

    def test_tile_count_scales_the_sheet_and_frames_are_not_upscaled(self):
        small = write_candidate(self.pkg, 'page-02-panel-01', 'v01', (400, 200), (10, 120, 200))
        self.assertEqual(small['width'], 400)
        index = rs.make_review_sheets(self.pkg, self.out)
        with Image.open(index['page-02-panel-01']['sheet']) as sheet:
            mask = near(sheet, (10, 120, 200))
            columns = np.where(mask.any(axis=0))[0]
            self.assertEqual(columns.max() - columns.min() + 1, 400)
        with Image.open(index['page-01-panel-01']['sheet']) as three, \
                Image.open(index['page-01-panel-02']['sheet']) as one:
            self.assertGreater(three.height, 0)
            self.assertGreater(one.height, 0)

    def test_index_json_lists_cast_and_candidates_but_not_provenance(self):
        index = rs.make_review_sheets(self.pkg, self.out)
        on_disk = json.loads((self.out / 'INDEX.json').read_text())
        self.assertEqual(on_disk, json.loads(json.dumps(index)))
        entry = on_disk['page-01-panel-01']
        self.assertEqual(entry['cast'], ['nagoji', 'duarte'])
        self.assertEqual(len(entry['candidates']), 3)
        for candidate in entry['candidates']:
            self.assertEqual(set(candidate), {'version', 'record', 'frame', 'sha256'})
            self.assertNotIn('provenance', candidate['record'])
            self.assertTrue(candidate['record'].endswith(f"page-01-panel-01-{candidate['version']}.json"))
            self.assertEqual(candidate['sha256'], sha(candidate['frame']))
            self.assertTrue(Path(candidate['record']).is_file())
        self.assertEqual(on_disk['page-01-panel-02']['cast'], [])

    def test_extra_records_are_listed_only_when_they_add_a_new_frame(self):
        candidates = self.pkg / 'candidates'
        duplicate = (candidates / 'page-01-panel-01-v01.json').read_text()
        (candidates / 'page-01-panel-01-r7-a01.json').write_text(duplicate)             # same frame as v01
        (candidates / 'page-01-panel-01-v01-root-ready-r1.json').write_text(duplicate)  # same frame as v01
        (candidates / 'page-01-panel-01-v02-provenance-corrected.json').write_text(
            json.dumps({'id': 'page-01-panel-01', 'candidate': 'x'}))                   # not a record
        write_candidate(self.pkg, 'page-01-panel-01', 'r7-a02', (1000, 400), (9, 99, 99))
        index = rs.make_review_sheets(self.pkg, self.out)
        self.assertEqual([c['version'] for c in index['page-01-panel-01']['candidates']],
                         ['v01', 'v02', 'v03', 'r7-a02'])

    def test_relative_frame_paths_resolve_against_the_package(self):
        record_path = self.pkg / 'candidates' / 'page-01-panel-01-v03.json'
        record = json.loads(record_path.read_text())
        record['path'] = 'frames/page-01-panel-01-v03.png'
        record_path.write_text(json.dumps(record))
        index = rs.make_review_sheets(self.pkg, self.out)
        frame = index['page-01-panel-01']['candidates'][2]['frame']
        self.assertEqual(Path(frame), (self.pkg / 'frames' / 'page-01-panel-01-v03.png').resolve())

    def test_refuses_an_existing_out_dir_and_leaves_it_alone(self):
        self.out.mkdir()
        (self.out / 'keep.txt').write_text('mine')
        with self.assertRaises(FileExistsError):
            rs.make_review_sheets(self.pkg, self.out)
        self.assertEqual([p.name for p in self.out.iterdir()], ['keep.txt'])

    def test_never_writes_inside_the_package(self):
        before = listing(self.pkg)
        rs.make_review_sheets(self.pkg, self.out)
        self.assertEqual(listing(self.pkg), before)
        with self.assertRaises(ValueError):
            rs.make_review_sheets(self.pkg, self.pkg / 'sheets')
        self.assertFalse((self.pkg / 'sheets').exists())

    def test_frame_that_differs_from_its_record_is_refused(self):
        frame = self.pkg / 'frames' / 'page-01-panel-01-v02.png'
        write_frame(frame, (2000, 760), (1, 2, 3))
        with self.assertRaisesRegex(ValueError, 'page-01-panel-01-v02'):
            rs.make_review_sheets(self.pkg, self.out)
        self.assertFalse(self.out.exists() and any(self.out.iterdir()))

    def test_missing_jobs_file_is_a_clear_error(self):
        (self.pkg / 'IMAGEGEN-JOBS.json').unlink()
        with self.assertRaises(FileNotFoundError):
            rs.make_review_sheets(self.pkg, self.out)
        self.assertFalse(self.out.exists())


if __name__ == '__main__':
    unittest.main()
