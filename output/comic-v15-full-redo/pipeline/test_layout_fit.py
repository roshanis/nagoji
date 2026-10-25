import json
import math
import unittest
from pathlib import Path
from unittest import mock

import compositor as c
import layout_fit as lf

V15 = Path(__file__).resolve().parent.parent

HEAVY = ('Look at his hands and see the brand on his arm, said the voice, and every head in the hold '
         'turned toward the man in the chains.')
LIGHT = 'The sea was no longer alone.'


def chunk(text, speaker='NAGOJI'):
    return {'speaker': speaker, 'text': text}


def script_of(pages):
    """pages: {page number: [copy list per panel]}"""
    return {'pages': {str(n): {'panels': [
        {'id': f'page-{n:02d}-panel-{i + 1:02d}', 'copy': copy} for i, copy in enumerate(panels)]}
        for n, panels in pages.items()}}


def described(script, descriptions):
    """Give a script_of() script its panels' script descriptions, by panel id (the layout cues live there)."""
    for page in script['pages'].values():
        for panel in page['panels']:
            panel['description'] = descriptions.get(panel['id'], '')
    return script


def frame(aspect=2.0, width=2000):
    height = round(width / aspect)
    return {'visible_rect': [0, 0, width, height], 'width': width, 'height': height}


def totals(rows, gap=2.0):
    flat = [r[0] if isinstance(r, list) else r for r in rows]
    return sum(flat) + gap * (len(flat) - 1)


def heights(rows):
    return [r[0] if isinstance(r, list) else r for r in rows]


def shape(rows):
    return [len(r) if isinstance(r, list) else 0 for r in rows]


class FitLayoutTests(unittest.TestCase):
    """Row heights are re-balanced per page, keeping the row structure and the 523.5 pt total."""

    def one_page(self, prior, copies, frames=None, faces=None, margin=3.0):
        script = script_of({1: copies})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = frames or {pid: frame() for pid in ids}
        return lf.fit_layout(script, {'1': prior}, frames, faces, margin=margin), ids

    def test_a_dialogue_heavy_strip_gets_taller_and_a_silent_one_shorter(self):
        prior = [70, 200, 249.5]
        result, ids = self.one_page(prior, [[chunk(HEAVY), chunk(HEAVY), chunk(HEAVY)], [], [chunk(LIGHT)]])
        new = heights(result['page_rows']['1'])
        self.assertGreater(new[0], 70)                       # the dialogue-heavy strip grows
        self.assertLess(new[1], 200)                         # the silent one gives height up
        self.assertGreaterEqual(new[1], lf.MIN_ROW_PT)       # but not below 55 pt
        page = result['report']['pages']['1']
        self.assertGreater(page['min_ratio_after'], page['min_ratio_before'])

    def test_every_page_totals_exactly_523_5_and_geometry_for_script_accepts_it(self):
        script = script_of({1: [[chunk(HEAVY)] * 3, [], [chunk(LIGHT)]],
                            2: [[chunk(HEAVY)] * 2, [chunk(LIGHT)], [chunk(HEAVY)] * 3, []]})
        frames = {p['id']: frame(1.4) for pg in script['pages'].values() for p in pg['panels']}
        prior = {'1': [70, 200, 249.5], '2': [110, 140, 140.5, 127]}
        result = lf.fit_layout(script, prior, frames)
        for page, rows in result['page_rows'].items():
            self.assertAlmostEqual(totals(rows), c.STORY_HEIGHT_PT, places=9, msg=page)
            self.assertEqual(round(totals(rows) * 10), round(c.STORY_HEIGHT_PT * 10))
        geometry = c.geometry_for_script(script, result['page_rows'])
        self.assertEqual(sorted(geometry['pages']), ['1', '2'])

    def test_row_structure_is_preserved_including_side_by_side_rows(self):
        script = script_of({1: [[chunk(HEAVY)] * 2, [chunk(LIGHT)], [chunk(LIGHT)], [chunk(HEAVY)], []]})
        frames = {p['id']: frame(1.2) for p in script['pages']['1']['panels']}
        prior = [[120, 120], 150, 100, 147.5]
        result = lf.fit_layout(script, {'1': prior}, frames)
        rows = result['page_rows']['1']
        self.assertEqual(shape(rows), shape(prior))          # which panels share a row is unchanged
        self.assertEqual(rows[0][0], rows[0][1])             # and a shared row has one common height
        c.geometry_for_script(script, result['page_rows'])

    def test_bounds_are_respected(self):
        script = script_of({1: [[chunk(HEAVY)] * 3, [chunk(HEAVY)] * 3, [], [chunk(LIGHT)], []]})
        frames = {p['id']: frame(1.0) for p in script['pages']['1']['panels']}
        prior = [90, 120, 90, 110, 105.5]
        silent = [False, False, True, False, True]
        result = lf.fit_layout(script, {'1': prior}, frames)
        for new, old, quiet in zip(heights(result['page_rows']['1']), prior, silent):
            floor = lf.MIN_ROW_PT if quiet else max(lf.MIN_ROW_PT, lf.MIN_SHARE * old)
            self.assertGreaterEqual(new, floor - 1e-9)
            self.assertLessEqual(new, lf.MAX_GROWTH * old + 1e-9)

    def test_a_page_whose_load_cannot_fit_is_reported_and_bounds_still_hold(self):
        hopeless = [chunk(HEAVY * 3)] * 4
        script = script_of({1: [hopeless, hopeless, [chunk(LIGHT)]]})
        frames = {p['id']: frame(1.0) for p in script['pages']['1']['panels']}
        result = lf.fit_layout(script, {'1': [60, 60, 399.5]}, frames)
        page = result['report']['pages']['1']
        self.assertEqual(page['status'], 'cannot_fit')
        self.assertLess(page['min_ratio_after'], 1.0)
        new = heights(result['page_rows']['1'])
        self.assertAlmostEqual(totals(result['page_rows']['1']), c.STORY_HEIGHT_PT, places=9)
        for height, old in zip(new, [60, 60, 399.5]):
            self.assertGreaterEqual(height, max(lf.MIN_ROW_PT, lf.MIN_SHARE * old) - 1e-9)
            self.assertLessEqual(height, lf.MAX_GROWTH * old + 1e-9)
        self.assertIn('reason', page)

    def test_a_row_whose_art_is_narrower_than_the_column_grows_toward_filling_it(self):
        # A square frame in a 100 pt strip fills 27 percent of the column; its neighbour's wide frame leaves
        # spare height. With little lettering, the strip is given height so the art fills more of the column.
        script = script_of({1: [[chunk(LIGHT)], [chunk(LIGHT)]]})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = {ids[0]: frame(1.0), ids[1]: frame(3.69)}
        result = lf.fit_layout(script, {'1': [100, 421.5]}, frames)
        new = heights(result['page_rows']['1'])
        self.assertGreater(new[0], 100)
        panel = result['report']['pages']['1']['panels'][ids[0]]
        self.assertGreater(panel['fill_after'], panel['fill_before'])
        self.assertLessEqual(new[0], 200 + 1e-9)             # never more than twice the prior

    def test_raising_the_minimum_ratio_is_the_first_priority(self):
        script = script_of({1: [[chunk(HEAVY)] * 3, [chunk(HEAVY)] * 2, [chunk(LIGHT)]]})
        frames = {p['id']: frame(1.5) for p in script['pages']['1']['panels']}
        result = lf.fit_layout(script, {'1': [100, 140, 279.5]}, frames)
        page = result['report']['pages']['1']
        self.assertGreater(page['min_ratio_after'], page['min_ratio_before'])
        self.assertEqual(set(page['panels']), {p['id'] for p in script['pages']['1']['panels']})
        for info in page['panels'].values():
            self.assertIn('ratio_before', info)
            self.assertIn('ratio_after', info)

    def test_faces_reduce_the_usable_area(self):
        script = script_of({1: [[chunk(HEAVY)] * 2, [chunk(LIGHT)]]})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = {pid: frame(1.5) for pid in ids}
        plain = lf.fit_layout(script, {'1': [200, 321.5]}, frames)
        faced = lf.fit_layout(script, {'1': [200, 321.5]}, frames, {ids[0]: [(0.3, 0.5, 0.3), (0.7, 0.5, 0.3)]})
        self.assertLess(faced['report']['pages']['1']['panels'][ids[0]]['ratio_before'],
                        plain['report']['pages']['1']['panels'][ids[0]]['ratio_before'])
        # Faces that leave the crop free (they span 60 percent of the width and 40 percent of the height) cost
        # usable area, so the row needs at least the height it needs without them. Faces as wide as the ones
        # above hold the crop open instead, and a taller row shows no more art: see CoverCropFitTests.
        modest = lf.fit_layout(script, {'1': [200, 321.5]}, frames, {ids[0]: [(0.3, 0.5, 0.15), (0.7, 0.5, 0.15)]})
        self.assertLess(modest['report']['pages']['1']['panels'][ids[0]]['ratio_before'],
                        plain['report']['pages']['1']['panels'][ids[0]]['ratio_before'])
        self.assertGreaterEqual(heights(modest['page_rows']['1'])[0], heights(plain['page_rows']['1'])[0])

    def test_a_panel_without_a_frame_is_handled_and_reported(self):
        script = script_of({1: [[chunk(LIGHT)], [chunk(HEAVY)] * 2, []]})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        result = lf.fit_layout(script, {'1': [150, 200, 169.5]}, {ids[0]: frame(2.0)})
        self.assertAlmostEqual(totals(result['page_rows']['1']), c.STORY_HEIGHT_PT, places=9)
        self.assertEqual(result['report']['pages']['1']['panels'][ids[1]]['frame'], 'none')

    def test_a_page_missing_from_the_prior_layout_keeps_one_equal_row_per_panel(self):
        script = script_of({1: [[chunk(LIGHT)], [chunk(LIGHT)]], 2: [[chunk(LIGHT)], [chunk(LIGHT)], []]})
        frames = {p['id']: frame() for pg in script['pages'].values() for p in pg['panels']}
        result = lf.fit_layout(script, {'1': [200, 321.5]}, frames)
        self.assertEqual(len(result['page_rows']['2']), 3)
        self.assertAlmostEqual(totals(result['page_rows']['2']), c.STORY_HEIGHT_PT, places=9)

    def test_a_prior_with_the_wrong_panel_count_is_refused(self):
        script = script_of({1: [[chunk(LIGHT)], [chunk(LIGHT)]]})
        frames = {p['id']: frame() for p in script['pages']['1']['panels']}
        with self.assertRaises(ValueError):
            lf.fit_layout(script, {'1': [100, 100, 319.5]}, frames)
        with self.assertRaises(ValueError):
            lf.fit_layout(script, {'1': [100, 300]}, frames)            # does not fill the page

    def test_fitting_is_deterministic(self):
        script = script_of({1: [[chunk(HEAVY)] * 3, [], [chunk(LIGHT)]]})
        frames = {p['id']: frame(1.3) for p in script['pages']['1']['panels']}
        first = lf.fit_layout(script, {'1': [70, 200, 249.5]}, frames)
        second = lf.fit_layout(script, {'1': [70, 200, 249.5]}, frames)
        self.assertEqual(first, second)

    def test_output_has_no_dashes_and_serialises(self):
        script = script_of({1: [[chunk(HEAVY)] * 3, [], [chunk(LIGHT)]]})
        frames = {p['id']: frame() for p in script['pages']['1']['panels']}
        text = json.dumps(lf.fit_layout(script, {'1': [70, 200, 249.5]}, frames))
        self.assertNotIn(chr(0x2014), text)
        self.assertNotIn(chr(0x2013), text)


class FloorTests(unittest.TestCase):
    """Floors are heights a planner probe has proved: a row never gets less, and the ratio fit works above them."""

    def page(self, prior, copies, frames=None, floors=None, margin=3.0):
        script = script_of({1: copies})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = frames or {pid: frame(2.0) for pid in ids}
        return lf.fit_layout(script, {'1': prior}, frames, floors=floors, margin=margin), ids

    def test_a_floor_keeps_a_row_the_ratio_fit_would_shrink(self):
        copies = [[chunk(LIGHT)], [chunk(LIGHT)], [chunk(HEAVY)] * 2]
        plain, ids = self.page([200, 150, 169.5], copies)
        self.assertLess(heights(plain['page_rows']['1'])[0], 200)
        result, _ = self.page([200, 150, 169.5], copies, floors={ids[0]: 195})
        new = heights(result['page_rows']['1'])
        self.assertGreaterEqual(new[0], 195)
        self.assertAlmostEqual(totals(result['page_rows']['1']), c.STORY_HEIGHT_PT, places=9)
        row = result['report']['pages']['1']['rows'][0]
        self.assertEqual(row['floor_pt'], 195)
        self.assertTrue(row['floor_met'])
        self.assertEqual(result['report']['pages']['1']['status'] in ('ok', 'tight'), True)

    def test_floors_move_the_spare_height_to_the_rows_that_are_not_held(self):
        copies = [[chunk(LIGHT)], [chunk(HEAVY)] * 2, [chunk(LIGHT)]]
        result, ids = self.page([170, 170, 179.5], copies, floors={'page-01-panel-01': 165})
        new = heights(result['page_rows']['1'])
        self.assertGreaterEqual(new[0], 165)
        self.assertGreater(new[1], 170)            # the lettering-heavy row still gains from the rest

    def test_a_floor_above_the_upper_bound_is_reported_and_the_bound_holds(self):
        copies = [[chunk(LIGHT)], [chunk(LIGHT)], [chunk(LIGHT)]]
        result, ids = self.page([100, 210, 209.5], copies, floors={'page-01-panel-01': 260})
        new = heights(result['page_rows']['1'])
        self.assertLessEqual(new[0], lf.MAX_GROWTH * 100 + 1e-9)
        page = result['report']['pages']['1']
        self.assertEqual(page['status'], 'cannot_fit')
        self.assertFalse(page['rows'][0]['floor_met'])
        self.assertIn('floor', page['reason'])

    def test_floors_that_total_more_than_the_page_are_reported_and_totals_stay_exact(self):
        copies = [[chunk(LIGHT)], [chunk(LIGHT)], [chunk(LIGHT)]]
        floors = {'page-01-panel-01': 300, 'page-01-panel-02': 300, 'page-01-panel-03': 300}
        result, ids = self.page([173, 173, 173.5], copies, floors=floors)
        self.assertAlmostEqual(totals(result['page_rows']['1']), c.STORY_HEIGHT_PT, places=9)
        page = result['report']['pages']['1']
        self.assertEqual(page['status'], 'cannot_fit')
        self.assertIn('floor', page['reason'])
        for height, old in zip(heights(result['page_rows']['1']), [173, 173, 173.5]):
            self.assertGreaterEqual(height, max(lf.MIN_ROW_PT, lf.MIN_SHARE * old) - 1e-9)
            self.assertLessEqual(height, lf.MAX_GROWTH * old + 1e-9)

    def test_a_floor_on_a_shared_row_holds_for_the_row(self):
        script = script_of({1: [[chunk(LIGHT)], [chunk(LIGHT)], [chunk(LIGHT)]]})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = {pid: frame(2.0) for pid in ids}
        result = lf.fit_layout(script, {'1': [[150, 150], 371.5]}, frames, floors={ids[1]: 148})
        self.assertGreaterEqual(result['page_rows']['1'][0][0], 148)
        self.assertEqual(result['page_rows']['1'][0][0], result['page_rows']['1'][0][1])

    def test_a_ceiling_caps_a_row_and_a_pin_fixes_it(self):
        copies = [[chunk(HEAVY)] * 2, [chunk(LIGHT)], [chunk(LIGHT)]]
        script = script_of({1: copies})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = {pid: frame(2.0) for pid in ids}
        capped = lf.fit_layout(script, {'1': [100, 210, 209.5]}, frames, ceilings={ids[0]: 120})
        self.assertLessEqual(heights(capped['page_rows']['1'])[0], 120)
        self.assertAlmostEqual(totals(capped['page_rows']['1']), c.STORY_HEIGHT_PT, places=9)
        pinned = lf.fit_layout(script, {'1': [100, 210, 209.5]}, frames, floors={ids[0]: 125}, ceilings={ids[0]: 125})
        self.assertEqual(heights(pinned['page_rows']['1'])[0], 125)
        self.assertTrue(pinned['report']['pages']['1']['rows'][0]['floor_met'])

    def test_a_floor_above_a_ceiling_is_reported(self):
        copies = [[chunk(LIGHT)], [chunk(LIGHT)], [chunk(LIGHT)]]
        script = script_of({1: copies})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = {pid: frame(2.0) for pid in ids}
        result = lf.fit_layout(script, {'1': [170, 170, 179.5]}, frames, floors={ids[0]: 160}, ceilings={ids[0]: 150})
        self.assertLessEqual(heights(result['page_rows']['1'])[0], 150)
        page = result['report']['pages']['1']
        self.assertEqual(page['status'], 'cannot_fit')
        self.assertFalse(page['rows'][0]['floor_met'])

    def test_no_floors_is_exactly_the_plain_fit(self):
        copies = [[chunk(HEAVY)] * 3, [], [chunk(LIGHT)]]
        script = script_of({1: copies})
        frames = {p['id']: frame() for p in script['pages']['1']['panels']}
        plain = lf.fit_layout(script, {'1': [70, 200, 249.5]}, frames)
        self.assertEqual(lf.fit_layout(script, {'1': [70, 200, 249.5]}, frames, floors={}), plain)
        self.assertEqual(lf.fit_layout(script, {'1': [70, 200, 249.5]}, frames, floors=None), plain)

    def test_structure_lists_each_row_with_its_bounds(self):
        script = script_of({1: [[chunk(LIGHT)], [chunk(LIGHT)], []]})
        rows = lf.structure(script, {'1': [[200, 200], 321.5]})['1']
        self.assertEqual([row['panels'] for row in rows],
                         [['page-01-panel-01', 'page-01-panel-02'], ['page-01-panel-03']])
        self.assertEqual([row['width_pt'] for row in rows], [183.5, 369])
        self.assertEqual([(row['prior_pt'], row['min_pt'], row['max_pt'], row['silent']) for row in rows],
                         [(200, 120, 400, False), (321.5, 55, 643, True)])


class CoverCropFitTests(unittest.TestCase):
    """The clip models the compositor's input: the planner crops the art toward the slot's shape first."""

    HEIGHT = 1024                                      # a 3:2 generator frame, 1536 x 1024

    def panel(self, faces=None, width_pt=369.0, chunks=None, painted=None, keep=None):
        spec = {'id': 'page-01-panel-01', 'copy': [chunk(LIGHT)] if chunks is None else chunks}
        return lf._Panel(spec, width_pt, frame(1.5, 1536), faces, painted, keep)

    def test_a_crop_within_min_keep_fills_the_slot_exactly(self):
        self.assertEqual(lf.MIN_KEEP, .45)
        panel = self.panel()
        self.assertEqual(panel.clip(153.75), (369.0, 153.75))            # a 2.4 slot needs 62.5 percent of the height
        self.assertEqual(panel.fill(153.75), 1.0)
        self.assertEqual(panel.fill(250.0), 1.0)                          # 1.476 is the art's own shape, within 2 percent

    def test_a_slot_wider_than_min_keep_allows_leaves_side_bars(self):
        panel = self.panel()
        clip_w, clip_h = panel.clip(100.0)                                # a 3.69 strip would need 40.7 percent: stops at 45
        self.assertEqual(clip_h, 100.0)
        self.assertLess(panel.fill(100.0), 1.0)
        self.assertAlmostEqual(clip_w, 100.0 * 1536 / (.45 * self.HEIGHT), delta=2.0)
        self.assertGreater(panel.fill(100.0), .8)                         # far better than the 41 percent of uncropped art

    def test_a_tall_slot_crops_the_width_instead(self):
        panel = self.panel(width_pt=183.5)
        self.assertEqual(panel.clip(200.0), (183.5, 200.0))               # a 0.92 slot needs 61 percent of the width
        self.assertEqual(panel.fill(200.0), 1.0)
        clip_w, clip_h = panel.clip(400.0)                                # a 0.46 slot is beyond 45 percent: stops there
        self.assertEqual(clip_w, 183.5)
        self.assertLess(clip_h, 400.0)

    def test_a_face_zone_stops_the_crop_where_it_would_cut_it(self):
        panel = self.panel(faces=[(.5, .5, .4)])                          # the zone spans y 102 to 922: 820 of 1024 px
        clip_w, clip_h = panel.clip(153.75)
        self.assertEqual(clip_h, 153.75)
        self.assertAlmostEqual(clip_w, 153.75 * 1536 / 820, delta=1.0)
        self.assertLess(panel.fill(153.75), 1.0)
        self.assertEqual(self.panel().fill(153.75), 1.0)                  # the same slot without the face

    def test_the_face_share_is_measured_against_what_the_crop_shows(self):
        import math
        panel = self.panel(faces=[(.5, .5, .1)])
        clip_w, clip_h = panel.clip(100.0)
        disc = math.pi * (.1 * self.HEIGHT) ** 2
        self.assertAlmostEqual(panel.usable(100.0) / (clip_w * clip_h), 1 - disc / (1536 * 462), places=2)
        clip_w, clip_h = panel.clip(246.0)                                # the art's own shape: nothing cropped
        self.assertAlmostEqual(panel.usable(246.0) / (clip_w * clip_h), 1 - disc / (1536 * 1024), places=2)

    def test_the_height_that_fills_the_column_comes_from_the_crop(self):
        panel = self.panel()
        height = panel.fill_height()
        self.assertAlmostEqual(height, 369.0 / (1.5 / .45), delta=1.0)    # 110.7 pt, not the 246 pt of uncropped art
        self.assertAlmostEqual(panel.fill(height + .1), 1.0, places=6)
        self.assertLess(panel.fill(height - 5.0), 1.0)
        faced = self.panel(faces=[(.5, .5, .4)])
        self.assertAlmostEqual(faced.fill_height(), 369.0 * 820 / 1536, delta=1.0)    # the face zone holds the crop open
        self.assertAlmostEqual(faced.fill(faced.fill_height() + .1), 1.0, places=6)
        self.assertLess(faced.fill(faced.fill_height() - 5.0), 1.0)
        none = lf._Panel({'id': 'x', 'copy': []}, 369.0, None, None)
        self.assertEqual(none.fill_height(), 0.0)
        self.assertIsNone(none.fill(100.0))

    def test_faces_that_span_the_width_hold_the_crop_open_so_a_taller_row_shows_no_more_art(self):
        panel = self.panel(faces=[(.3, .5, .3), (.7, .5, .3)])            # x 154 to 1382 of 1536: 80 percent of the width
        locked = panel.clip(330.0)
        self.assertEqual(panel.clip(400.0), locked)                        # no crop can narrow below the faces
        self.assertEqual(panel.usable(400.0), panel.usable(330.0))
        self.assertLess(locked[1], 330.0)                                  # bars above and below the art remain
        self.assertGreater(self.panel().clip(400.0)[1], locked[1])         # without the faces the width crop keeps growing

    def test_a_panel_without_a_frame_is_untouched(self):
        none = lf._Panel({'id': 'x', 'copy': [chunk(LIGHT)]}, 369.0, None, None)
        self.assertEqual(none.clip(120.0), (369.0, 120.0))
        with_keep = lf._Panel({'id': 'x', 'copy': [chunk(LIGHT)]}, 369.0, None, None, [[0, .4, 1, .5]], [[0, .4, 1, .5]])
        self.assertEqual(with_keep.clip(120.0), (369.0, 120.0))
        self.assertEqual(with_keep.fill_height(), 0.0)


class PaintedKeepFitTests(unittest.TestCase):
    """The planner keeps every painted region in view (the balloon must hide it), so the fitter's crop must too.

    Painted and keep rectangles are fractions of the frame, as faces are; they go to reserves.cover_crop with the faces.
    """

    FULL_WIDTH = [[0.0, .40, 1.0, .50]]             # painted boxes that span the frame's width
    FULL_HEIGHT = [[.40, 0.0, .60, 1.0]]            # ... and one that spans its height

    def panel(self, width_pt=369.0, faces=None, painted=None, keep=None):
        spec = {'id': 'page-01-panel-01', 'copy': [chunk(LIGHT)]}
        return lf._Panel(spec, width_pt, frame(1.5, 1536), faces, painted, keep)

    def test_a_full_width_painted_region_cannot_be_narrowed_so_a_tall_slot_is_letterboxed(self):
        plain, held = self.panel(width_pt=183.5), self.panel(width_pt=183.5, painted=self.FULL_WIDTH)
        self.assertEqual(plain.clip(200.0), (183.5, 200.0))                      # a 0.92 slot: the width is cropped to fit
        clip_w, clip_h = held.clip(200.0)
        self.assertEqual(clip_w, 183.5)
        self.assertAlmostEqual(clip_h, 183.5 / 1.5, places=6)                    # the art keeps its shape: bars above and below
        self.assertLess(clip_h, 200.0)
        self.assertLess(held.usable(200.0), plain.usable(200.0))                 # so the row has less art than it was thought to
        self.assertEqual(held.clip(400.0)[1], clip_h)                            # and a taller row shows no more of it
        self.assertEqual(held.usable(400.0), held.usable(200.0))
        self.assertEqual(plain.fill(200.0), 1.0)                                 # the clip is the slot
        self.assertEqual(held.fill_width(200.0), 1.0)                            # the held art still spans the column ...
        self.assertAlmostEqual(held.fill(200.0), clip_h / 200.0, places=6)       # ... but covers only its height of the slot

    def test_a_painted_region_that_spans_the_frames_height_pillarboxes_a_wide_slot(self):
        plain, held = self.panel(), self.panel(painted=self.FULL_HEIGHT)
        self.assertEqual(plain.fill(153.75), 1.0)                                # a 2.4 slot crops the height to fit
        self.assertEqual(held.fill(153.75), held.clip(153.75)[0] / 369.0)
        self.assertAlmostEqual(held.fill(153.75), 153.75 * 1.5 / 369.0, places=6)    # the art keeps its shape: bars either side
        self.assertLess(held.fill(153.75), 1.0)
        self.assertLess(held.usable(153.75), plain.usable(153.75))

    def test_the_height_that_fills_the_column_is_found_with_the_painted_region_held(self):
        held = self.panel(painted=[[0.0, .30, 1.0, .80]])                        # 50 percent of the height must stay
        self.assertAlmostEqual(held.fill_height(), 369.0 * (.5 * 1024) / 1536, delta=1.0)    # tighter crops are refused
        self.assertAlmostEqual(held.fill(held.fill_height() + .1), 1.0, places=6)
        self.assertLess(held.fill(held.fill_height() - 5.0), 1.0)
        self.assertGreater(held.fill_height(), self.panel().fill_height())       # the plain crop goes down to 45 percent

    def test_painted_regions_and_faces_are_held_together(self):
        faced = self.panel(faces=[(.5, .2, .1)], painted=[[0.0, .7, 1.0, .9]])   # face zone y .1 to .3, painted y .7 to .9
        self.assertAlmostEqual(faced.fill_height(), 369.0 * (.8 * 1024) / 1536, delta=1.0)

    def test_a_keep_zone_holds_the_crop_as_a_face_does(self):
        keep = [[.2, .80, .6, .95]]                                              # near the bottom of the frame
        plain, held = self.panel(), self.panel(keep=keep)
        self.assertEqual(held.fill(153.75), 1.0)                                 # it fits: the band moves down to include it
        self.assertEqual(held.clip(153.75), plain.clip(153.75))
        # With a face as well the two together need more than a 2.4 slot shows: the crop is left taller, not cut.
        both = self.panel(faces=[(.5, .3, .2)], keep=keep)                       # face zone y .1 to .5, keep down to .95
        self.assertAlmostEqual(both.fill_height(), 369.0 * (.85 * 1024) / 1536, delta=1.0)
        self.assertLess(both.fill(153.75), 1.0)
        self.assertEqual(both.fill(both.fill_height() + .1), 1.0)

    def test_fit_layout_takes_painted_and_keep_like_faces_and_defaults_to_none(self):
        script = script_of({1: [[chunk(HEAVY)] * 2, [chunk(LIGHT)]]})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = {pid: frame(1.5, 1536) for pid in ids}
        prior = {'1': [200, 321.5]}
        plain = lf.fit_layout(script, prior, frames)
        self.assertEqual(lf.fit_layout(script, prior, frames, painted=None, keep=None), plain)
        self.assertEqual(lf.fit_layout(script, prior, frames, painted={}, keep={}), plain)
        held = lf.fit_layout(script, prior, frames, painted={ids[0]: self.FULL_HEIGHT})
        self.assertLess(held['report']['pages']['1']['panels'][ids[0]]['fill_before'],
                        plain['report']['pages']['1']['panels'][ids[0]]['fill_before'])
        self.assertLess(held['report']['pages']['1']['panels'][ids[0]]['usable_pt2_after'],
                        plain['report']['pages']['1']['panels'][ids[0]]['usable_pt2_after'] + 1)
        kept = lf.fit_layout(script, prior, frames, keep={ids[0]: self.FULL_HEIGHT})
        self.assertEqual(kept['report']['pages']['1']['panels'][ids[0]], held['report']['pages']['1']['panels'][ids[0]])
        self.assertAlmostEqual(totals(held['page_rows']['1']), c.STORY_HEIGHT_PT, places=9)
        self.assertEqual(lf.structure(script, prior), lf.structure(script, prior))

    def test_the_fit_sees_the_lower_ratio_a_letterboxed_row_really_has(self):
        # A row taller than the art's own shape (369 x 246 pt here) shows its painted, full-width art letterboxed: the
        # crop cannot be narrowed to fill it, so the lettering has the art's area to sit in, not the whole row's.
        script = script_of({1: [[chunk(HEAVY)] * 2, [chunk(LIGHT)]]})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = {pid: frame(1.5, 1536) for pid in ids}
        prior = {'1': [300, 221.5]}
        plain = lf.fit_layout(script, prior, frames)['report']['pages']['1']['panels'][ids[0]]
        held = lf.fit_layout(script, prior, frames, painted={ids[0]: self.FULL_WIDTH})['report']['pages']['1']['panels'][ids[0]]
        self.assertLess(held['ratio_before'], plain['ratio_before'])
        self.assertAlmostEqual(held['ratio_before'] / plain['ratio_before'], 246 / 300, places=2)
        self.assertEqual(held['fill_width_before'], plain['fill_width_before'])     # both span the column's width ...
        self.assertAlmostEqual(held['fill_before'] / plain['fill_before'], 246 / 300, places=2)   # ... but not the row's area
        # A panel without a painted region is exactly what it was, at the height it had.
        other = lf.fit_layout(script, prior, frames, painted={ids[0]: self.FULL_WIDTH})['report']['pages']['1']['panels'][ids[1]]
        unchanged = lf.fit_layout(script, prior, frames)['report']['pages']['1']['panels'][ids[1]]
        for key in ('ratio_before', 'fill_before', 'faces_share'):
            self.assertEqual(other[key], unchanged[key])


class AreaFillTests(unittest.TestCase):
    """fill is the share of the slot's AREA the placed clip covers, so a panel boxed top and bottom counts as under-filled."""

    FULL_WIDTH = [[0.0, .40, 1.0, .50]]           # a painted region that spans the frame's width: the crop cannot be narrowed

    def panel(self, width_pt=183.5, painted=None, faces=None):
        spec = {'id': 'page-01-panel-01', 'copy': [chunk(LIGHT)]}
        return lf._Panel(spec, width_pt, frame(1.5, 1536), faces, painted)

    def test_a_3_to_2_frame_in_a_tall_half_width_slot_spans_the_width_but_not_the_area(self):
        held = self.panel(painted=self.FULL_WIDTH)                 # the half-width slot of a pair row, 300 pt tall
        clip_w, clip_h = held.clip(300.0)
        self.assertEqual(clip_w, 183.5)
        self.assertAlmostEqual(clip_h, 183.5 / 1.5, places=6)      # the art keeps its shape: 122 pt tall in a 300 pt slot
        self.assertEqual(held.fill_width(300.0), 1.0)              # the old fill: it spans the column
        self.assertAlmostEqual(held.fill(300.0), clip_w * clip_h / (183.5 * 300.0), places=9)
        self.assertAlmostEqual(held.fill(300.0), 183.5 / 1.5 / 300.0, places=6)
        self.assertLess(held.fill(300.0), .5)                      # well under 1: big gaps above and below
        self.assertEqual(self.panel().fill(250.0), 1.0)            # without the painted region the crop narrows to fit the slot

    def test_the_area_fill_falls_as_the_slot_grows_taller_while_the_art_stays_put(self):
        held = self.panel(painted=self.FULL_WIDTH)
        fills = [held.fill(height) for height in (150.0, 200.0, 300.0, 400.0)]
        self.assertEqual(fills, sorted(fills, reverse=True))
        self.assertEqual({held.fill_width(height) for height in (150.0, 200.0, 300.0, 400.0)}, {1.0})

    def test_when_the_clip_is_the_slot_or_only_narrower_the_two_fills_agree(self):
        plain = self.panel(width_pt=369.0)
        self.assertEqual(plain.fill(153.75), 1.0)                  # the crop fits the slot exactly
        self.assertEqual(plain.fill_width(153.75), 1.0)
        pillar = self.panel(width_pt=369.0, painted=[[.40, 0.0, .60, 1.0]])
        self.assertLess(pillar.fill(153.75), 1.0)                  # bars at the sides only: the clip is as tall as the slot
        self.assertEqual(pillar.fill(153.75), pillar.fill_width(153.75))

    def test_a_panel_without_a_frame_has_no_fill_of_either_kind(self):
        none = lf._Panel({'id': 'x', 'copy': []}, 369.0, None, None)
        self.assertIsNone(none.fill(100.0))
        self.assertIsNone(none.fill_width(100.0))

    def test_the_reports_give_the_area_fill_under_the_old_names_and_the_width_fill_beside_it(self):
        script = script_of({1: [[chunk(HEAVY)] * 2, [chunk(LIGHT)]]})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = {pid: frame(1.5, 1536) for pid in ids}
        result = lf.fit_layout(script, {'1': [300, 221.5]}, frames, painted={ids[0]: self.FULL_WIDTH})
        info = result['report']['pages']['1']['panels'][ids[0]]
        self.assertEqual(info['fill_width_before'], 1.0)           # both span the column's width ...
        self.assertAlmostEqual(info['fill_before'], 246 / 300, places=2)    # ... but the art is 246 pt tall in a 300 pt row
        for key in ('fill_before', 'fill_after', 'fill_width_before', 'fill_width_after'):
            self.assertIn(key, info)
            self.assertLessEqual(info['fill_after'], info['fill_width_after'] + 1e-9)
        other = result['report']['pages']['1']['panels'][ids[1]]
        self.assertGreater(other['fill_width_after'], 0)
        blank = lf.fit_layout(script, {'1': [300, 221.5]}, {}, None)['report']['pages']['1']['panels'][ids[0]]
        self.assertIsNone(blank['fill_before'])
        self.assertIsNone(blank['fill_width_before'])


class AreaFillStructureTests(unittest.TestCase):
    """fit_structures ranks by how much of each slot the art covers: a pair row that letterboxes a frame loses to rows that do not."""

    FULL_WIDTH = [[0.0, .40, 1.0, .50]]            # the landscape panel's painted region spans its width: its crop cannot be narrowed
    FULL_HEIGHT = [[.40, 0.0, .60, 1.0]]           # the portrait panel's spans its height: it is pillarboxed in a wide slot

    def setUp(self):
        self.script = described(script_of({1: [[chunk(LIGHT)], [chunk(LIGHT)]]}), {})
        self.ids = [p['id'] for p in self.script['pages']['1']['panels']]
        self.frames = {self.ids[0]: frame(1.5, 1536), self.ids[1]: {'visible_rect': [0, 0, 1024, 1536], 'width': 1024, 'height': 1536}}
        self.painted = {self.ids[0]: self.FULL_WIDTH, self.ids[1]: self.FULL_HEIGHT}

    def fit(self, prior):
        return lf.fit_structures(self.script, {'1': prior}, self.frames, None, painted=self.painted)['report']['pages']['1']

    def test_the_pair_row_spans_the_column_but_letterboxes_the_landscape_frame(self):
        landscape = lf._Panel(self.script['pages']['1']['panels'][0], 183.5, self.frames[self.ids[0]], None, self.FULL_WIDTH)
        self.assertEqual(landscape.fill_width(523.5), 1.0)
        self.assertLess(landscape.fill(523.5), .25)                # 122 pt of art in a 523.5 pt slot

    def test_the_structure_that_does_not_letterbox_is_chosen(self):
        for prior in ([260.7, 260.8], [[523.5, 523.5]]):           # whichever structure the page started as
            with self.subTest(prior=prior):
                page = self.fit(prior)
                structure = page['structure']
                self.assertEqual(structure['chosen'], [1, 1])
                alternatives = {tuple(alt['structure']): alt for alt in structure['alternatives']}
                self.assertLess(alternatives[(2,)]['min_fill'], .3)             # the pair row is mostly cream above and below
                self.assertGreater(alternatives[(1, 1)]['min_fill'], .6)
                self.assertGreaterEqual(alternatives[(1, 1)]['min_ratio'], 1.0)   # lettering allows it
                self.assertGreaterEqual(alternatives[(2,)]['min_ratio'], 1.0)

    def test_by_width_alone_the_letterboxed_pair_row_used_to_win(self):
        with mock.patch.object(lf._Panel, 'fill', lf._Panel.fill_width):
            page = self.fit([260.7, 260.8])
        self.assertEqual(page['structure']['chosen'], [2])
        self.assertEqual(page['structure']['min_fill'], 1.0)

    def test_the_report_keeps_fill_for_the_area_and_adds_the_width(self):
        page = self.fit([260.7, 260.8])
        portrait = page['panels'][self.ids[1]]
        self.assertLess(portrait['fill_after'], 1.0)                # pillarboxed: bars at the sides only
        self.assertEqual(portrait['fill_after'], portrait['fill_width_after'])
        self.assertAlmostEqual(page['structure']['min_fill'], portrait['fill_after'], delta=.01)     # to three places and to two


class LayoutCueTests(unittest.TestCase):
    """layout_cues reads what a panel's script description asks of its row: alone, and how much of the page."""

    NOTHING = {'solo': False, 'min_share': None}

    def cues(self, description):
        return lf.layout_cues({'id': 'page-01-panel-01', 'description': description, 'copy': []})

    def test_a_description_with_no_layout_cue_asks_for_nothing(self):
        for text in ('Wide, shot from a distance. A storm-spent sea.', 'Insert, tight.', 'Small inset, lower corner of 1.',
                     'Small.', 'Close on Nagoji.', '', 'Two-shot. Nagoji half sitting, centre, the tunic open.',
                     "Large, the page's biggest panel.", "The king's forefinger, tapping one line near the foot of the page."):
            with self.subTest(text=text):
                self.assertEqual(self.cues(text), self.NOTHING)
        self.assertEqual(lf.layout_cues({'id': 'x'}), self.NOTHING)              # a panel with no description at all
        self.assertEqual(lf.layout_cues({'id': 'x', 'description': None}), self.NOTHING)

    def test_full_width_wording_keeps_a_panel_alone(self):
        for text in ('Full width, bottom strip. Same low angle along the sand.', 'Wide, full page width. A storm-spent sea.',
                     'Full-width tier, not a narrow strip.', 'FULL WIDTH.', 'full page width',
                     'Wide, full-width, the last panel of the chapter.', 'Full-page-width splash.'):
            with self.subTest(text=text):
                self.assertEqual(self.cues(text), {'solo': True, 'min_share': None})

    def test_strip_tier_and_splash_at_the_head_of_the_description_keep_a_panel_alone(self):
        for text in ('Narrow strip.', 'Bottom strip.', 'Widescreen strip, top.', 'Narrow panel, bottom strip.',
                     "Tight horizontal strip across Varma's eyes as they leave the map.", 'Large, most of a tier.',
                     'Splash. The wave.', 'STRIP, tight.'):
            with self.subTest(text=text):
                self.assertEqual(self.cues(text), {'solo': True, 'min_share': None})

    def test_those_words_as_scene_nouns_are_not_layout_cues(self):
        for text in ('Joao working down the line, a leather strip held up in one hand, notched along one edge.',
                     'A narrow strip of Malabar beach pinned between a low laterite bluff and the sea.',
                     'Wide. The strip as Nagoji pictures it, an aerial view.',
                     'Revathi leaning on the parapet beside Nagoji, staring north at the strip.',
                     'Wide. The black surf. Mukkuvar men paddle almost without a splash.'):
            with self.subTest(text=text):
                self.assertEqual(self.cues(text), self.NOTHING)

    def test_wording_that_asks_for_panels_side_by_side_does_not_make_a_panel_solo(self):
        for text in ('Split tier, two narrow panels side by side.', 'Left half of the third tier.',
                     'Right half of the third tier, side by side with 4.3.',
                     'Three narrow insets side by side across one strip, each showing only hands.'):
            with self.subTest(text=text):
                self.assertEqual(self.cues(text), self.NOTHING)
        self.assertTrue(self.cues('Full width, two figures side by side.')['solo'])      # an explicit full width still wins

    def test_a_full_width_cue_in_the_second_sentence_counts_but_a_third_does_not(self):
        self.assertTrue(self.cues('Flashback, desaturated palette, soft borders. Full width.')['solo'])
        self.assertFalse(self.cues('Wide. Dawn on the sea. The surf fills the full width of the frame.')['solo'])

    def test_a_size_cue_names_a_share_of_the_page(self):
        for text, solo, share in (
                ('Large, about the bottom 40 percent of the page.', False, .4),
                ('About a third of the page, full width.', True, 1 / 3),
                ('Large, top half of the page.', False, .5),
                ('Large, the lower half of the page, full width at ground level.', True, .5),
                ('Wide, half the page.', False, .5),
                ('A quarter of the page.', False, .25),
                ('Large, two thirds of the page.', False, 2 / 3),
                ('Large, about two fifths of the page.', False, .4),
                ('Tall panel, about a third of the page.', False, 1 / 3),
                ('Large, about 45% of the page.', False, .45),
                ('About 40 percent.', False, .4),
                ('Narrow strip, about a sixth of the page.', True, 1 / 6),
                ('Full width, bottom, a full third of the page so the face reads.', True, 1 / 3),
                ('Full-width dark strip, about a third of the page tall, between 2.2 and 2.4.', True, 1 / 3)):
            with self.subTest(text=text):
                cues = self.cues(text)
                self.assertEqual(cues['solo'], solo)
                self.assertAlmostEqual(cues['min_share'], share, places=9)
                self.assertEqual(set(cues), {'solo', 'min_share'})

    def test_a_share_that_is_not_a_share_of_a_page_is_ignored(self):
        for text in ('Close on a 0 percent grey.', 'Large, 150 percent of the page.',
                     'Wide. Dawn on the sea. A third of the page is sky.', 'Nagoji, half sitting.'):
            with self.subTest(text=text):
                self.assertIsNone(self.cues(text)['min_share'])

    def test_a_size_cue_floors_its_row_at_nine_tenths_of_the_share(self):
        self.assertAlmostEqual(lf.cue_floor_pt(1 / 3), .9 * 523.5 / 3)
        self.assertAlmostEqual(lf.cue_floor_pt(.4), 188.46)
        self.assertAlmostEqual(lf.cue_floor_pt(.5), 235.575)


class StructureEnumerationTests(unittest.TestCase):
    """Every way to cut a page's panels, in reading order, into consecutive rows of one or two panels."""

    def test_rows_of_one_or_two_panels_give_the_fibonacci_counts(self):
        self.assertEqual([len(lf.row_sizes(n)) for n in range(1, 7)], [1, 2, 3, 5, 8, 13])
        self.assertEqual(len(lf.row_sizes(5)), 8)

    def test_each_structure_covers_the_panels_once_in_reading_order(self):
        found = lf.row_sizes(5)
        self.assertEqual(len(set(found)), 8)
        for sizes in found:
            self.assertEqual(sum(sizes), 5)
            self.assertTrue(set(sizes) <= {1, 2})
        self.assertIn((1, 1, 1, 1, 1), found)
        self.assertIn((2, 2, 1), found)
        self.assertEqual(lf.rows_of((2, 1, 2)), [[0, 1], [2], [3, 4]])
        self.assertEqual(lf.row_sizes(5), found)                        # deterministic

    def test_a_solo_panel_removes_the_structures_that_pair_it(self):
        found = lf.structure_candidates(5, [False, True, False, False, False], (1, 1, 1, 1, 1))
        self.assertEqual(sorted(found), [(1, 1, 1, 1, 1), (1, 1, 1, 2), (1, 1, 2, 1)])
        for sizes in found:
            self.assertIn([1], lf.rows_of(sizes))                           # panel 2 (index 1) is alone in its row
        middle = lf.structure_candidates(5, [False, False, True, False, False], (1, 1, 1, 1, 1))
        self.assertEqual(len(middle), 4)
        for sizes in middle:
            self.assertIn([2], lf.rows_of(sizes))
        self.assertEqual(lf.structure_candidates(5, [True] * 5, (1, 1, 1, 1, 1)), [(1, 1, 1, 1, 1)])
        self.assertEqual(len(lf.structure_candidates(5, [False] * 5, (1, 1, 1, 1, 1))), 8)

    def test_the_prior_structure_is_always_a_candidate_and_comes_first(self):
        found = lf.structure_candidates(5, [True, False, False, False, False], (2, 1, 2))   # the prior pairs a solo panel
        self.assertEqual(found[0], (2, 1, 2))
        self.assertEqual(len(found), len(set(found)))
        rows_of_three = lf.structure_candidates(5, [False] * 5, (3, 2))                     # hand-made rows of three are kept
        self.assertEqual(rows_of_three[0], (3, 2))
        self.assertEqual(len(rows_of_three), 9)
        self.assertEqual(lf.rows_of((3, 2)), [[0, 1, 2], [3, 4]])


class SpreadPriorTests(unittest.TestCase):
    """The start a candidate structure is fitted from: rows in proportion to their panels' prior heights, meeting floors."""

    def test_heights_follow_the_weights_and_total_the_budget_exactly(self):
        heights = lf._spread_prior([1, 1, 2], [0, 0, 0], 4001)
        self.assertEqual(sum(heights), 4001)
        self.assertLessEqual(abs(heights[2] - 2 * heights[0]), 2)
        self.assertLessEqual(abs(heights[0] - heights[1]), 1)

    def test_a_floor_lifts_its_row_and_the_others_share_what_is_left(self):
        heights = lf._spread_prior([1, 1, 1], [0, 3000, 0], 5000)
        self.assertEqual(heights[1], 3000)
        self.assertEqual(sum(heights), 5000)
        self.assertEqual(heights[0], heights[2])

    def test_floors_that_together_exceed_the_budget_leave_no_start(self):
        self.assertIsNone(lf._spread_prior([1, 1], [3000, 3000], 5000))
        self.assertIsNone(lf._spread_prior([1, 1, 1], [0, 0, 6000], 5000))


class RankKeyTests(unittest.TestCase):
    """Candidates rank by lettering, then the minimum fill, the mean fill and the minimum lettering ratio."""

    def key(self, cues_ok=True, min_ratio=2.0, min_fill=.9, mean_fill=.95, order=1):
        return lf.rank_key({'cues_ok': cues_ok, 'min_ratio': min_ratio, 'min_fill': min_fill, 'mean_fill': mean_fill}, order)

    def test_a_ratio_of_at_least_one_comes_before_any_fill(self):
        self.assertGreater(self.key(min_ratio=1.0, min_fill=.3, mean_fill=.3), self.key(min_ratio=.99, min_fill=1.0, mean_fill=1.0))
        self.assertGreater(self.key(min_ratio=1.0), self.key(min_ratio=.5))
        self.assertGreater(self.key(min_ratio=1.0, min_fill=.3), self.key(min_ratio=.5, min_fill=.3))   # both below 1 is not a tie

    def test_a_page_with_no_lettering_passes_the_lettering_test(self):
        self.assertGreater(self.key(min_ratio=math.inf), self.key(min_ratio=.9))

    def test_the_minimum_fill_comes_before_the_mean_fill(self):
        self.assertGreater(self.key(min_fill=.8, mean_fill=.8), self.key(min_fill=.7, mean_fill=1.0))

    def test_the_mean_fill_comes_before_the_minimum_ratio(self):
        self.assertGreater(self.key(mean_fill=.9, min_ratio=1.0), self.key(mean_fill=.8, min_ratio=5.0))

    def test_the_minimum_ratio_breaks_what_is_left(self):
        self.assertGreater(self.key(min_ratio=3.0), self.key(min_ratio=2.0))

    def test_respecting_the_cues_comes_before_everything(self):
        self.assertGreater(self.key(min_ratio=.2, min_fill=.1, mean_fill=.1), self.key(cues_ok=False))

    def test_a_tie_goes_to_the_earlier_candidate(self):
        self.assertGreater(self.key(order=0), self.key(order=1))

    def test_fills_that_agree_to_three_places_are_a_tie(self):
        self.assertGreater(self.key(min_fill=.9001, mean_fill=.9, min_ratio=3.0), self.key(min_fill=.9004, mean_fill=.9, min_ratio=2.0))


class StructureFitTests(unittest.TestCase):
    """fit_structures chooses each page's rows (which panels share a row) as well as their heights."""

    PRIOR = [103.1] * 5                     # five full-width rows: 5 x 103.1 + 4 x 2 = 523.5

    def setup_page(self, descriptions=None, copies=None, count=5, faces=True, aspect=1.5, prior=None):
        copies = copies or [[chunk(LIGHT)]] * count
        script = described(script_of({1: copies}), descriptions or {})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = {pid: frame(aspect, 1536) for pid in ids}
        zones = {pid: [(.5, .5, .3)] for pid in ids} if faces else None      # a face zone holds the crop open
        return script, ids, frames, zones, {'1': prior or self.PRIOR}

    def fit(self, *args, **kwargs):
        script, ids, frames, zones, prior = self.setup_page(*args, **kwargs)
        return lf.fit_structures(script, prior, frames, zones), ids

    def row_of(self, result, panel_id):
        return next(row for row in result['report']['pages']['1']['rows'] if panel_id in row['panels'])

    def test_side_by_side_pairs_lift_the_minimum_fill_of_five_3_to_2_panels(self):
        script, ids, frames, zones, prior = self.setup_page()
        fixed = lf.fit_layout(script, prior, frames, zones)
        fixed_min = min(info['fill_after'] for info in fixed['report']['pages']['1']['panels'].values())
        self.assertLess(fixed_min, .8)                                    # five full-width rows cannot all span the column
        result = lf.fit_structures(script, prior, frames, zones)
        structure = result['report']['pages']['1']['structure']
        self.assertIn(2, structure['chosen'])                             # some panels now share a row
        self.assertEqual(sum(structure['chosen']), 5)
        self.assertGreater(structure['min_fill'], .95)
        self.assertGreater(structure['min_fill'], fixed_min + .2)
        self.assertAlmostEqual(structure['min_fill'], min(info['fill_after'] for info in
                                                          result['report']['pages']['1']['panels'].values()), places=2)
        self.assertAlmostEqual(totals(result['page_rows']['1']), c.STORY_HEIGHT_PT, places=9)
        self.assertEqual(round(totals(result['page_rows']['1']) * 10), round(c.STORY_HEIGHT_PT * 10))
        self.assertIn(2, shape(result['page_rows']['1']))
        geometry = c.geometry_for_script(script, result['page_rows'])
        self.assertEqual([p['id'] for p in geometry['pages']['1']], ids)              # every panel once, in reading order

    def test_the_alternatives_are_listed_with_their_scores_and_the_prior_is_one_of_them(self):
        result, ids = self.fit()
        structure = result['report']['pages']['1']['structure']
        alternatives = structure['alternatives']
        self.assertEqual(len(alternatives), 8)
        self.assertEqual(structure['candidates'], 8)
        self.assertEqual(structure['excluded'], 0)
        self.assertEqual(sorted(tuple(alt['structure']) for alt in alternatives), sorted(lf.row_sizes(5)))
        for alt in alternatives:
            self.assertEqual(set(alt), {'structure', 'rows_pt', 'min_fill', 'mean_fill', 'min_ratio', 'cues_ok', 'verified',
                                        'prior', 'chosen'})
            self.assertIsNone(alt['verified'])                             # nothing asked the planner
        self.assertEqual([alt['chosen'] for alt in alternatives].count(True), 1)
        self.assertEqual([alt['prior'] for alt in alternatives].count(True), 1)
        self.assertEqual(alternatives[0]['chosen'], True)                  # best first
        self.assertEqual(alternatives[0]['structure'], structure['chosen'])
        prior = next(alt for alt in alternatives if alt['prior'])
        self.assertEqual(prior['structure'], [1, 1, 1, 1, 1])
        self.assertEqual(structure['prior'], [1, 1, 1, 1, 1])
        self.assertLess(prior['min_fill'], alternatives[0]['min_fill'])
        self.assertEqual((structure['min_fill'], structure['mean_fill']), (alternatives[0]['min_fill'], alternatives[0]['mean_fill']))
        self.assertIsNone(structure['verified'])
        fills = [(alt['min_fill'], alt['mean_fill']) for alt in alternatives]
        self.assertEqual(fills, sorted(fills, reverse=True))

    def test_the_before_numbers_are_the_prior_layouts_own(self):
        script, ids, frames, zones, prior = self.setup_page()
        fixed = lf.fit_layout(script, prior, frames, zones)['report']['pages']['1']
        result = lf.fit_structures(script, prior, frames, zones)['report']['pages']['1']
        self.assertEqual(result['min_ratio_before'], fixed['min_ratio_before'])
        for pid in ids:
            self.assertEqual(result['panels'][pid]['fill_before'], fixed['panels'][pid]['fill_before'])
            self.assertEqual(result['panels'][pid]['ratio_before'], fixed['panels'][pid]['ratio_before'])
        self.assertLess(min(v['fill_before'] for v in result['panels'].values()), .8)
        self.assertGreater(min(v['fill_after'] for v in result['panels'].values()), .95)
        for row in result['rows']:                                         # a row that is new has no prior height
            if len(row['panels']) == 2:
                self.assertIsNone(row['prior_pt'])
            else:
                self.assertEqual(row['prior_pt'], 103.1)

    def test_a_panel_that_must_be_solo_stays_alone_in_every_structure(self):
        script, ids, frames, zones, prior = self.setup_page({'page-01-panel-02': 'Full width, bottom strip. Same low angle.'})
        result = lf.fit_structures(script, prior, frames, zones)
        page = result['report']['pages']['1']
        self.assertEqual(self.row_of(result, ids[1])['panels'], [ids[1]])
        self.assertEqual(page['structure']['candidates'], 8)
        self.assertEqual(page['structure']['excluded'], 5)                 # 8 groupings, 3 keep panel 2 alone
        self.assertEqual(len(page['structure']['alternatives']), 3)
        for alt in page['structure']['alternatives']:
            self.assertIn([1], lf.rows_of(tuple(alt['structure'])))            # panel 2 (index 1) is alone in its row
            self.assertTrue(alt['cues_ok'])
        free, _ = self.fit()                                               # without the cue the winner pairs that panel
        self.assertEqual(len(self.row_of(free, ids[1])['panels']), 2)

    def test_a_size_cue_floors_its_row_height(self):
        result, ids = self.fit({'page-01-panel-01': 'Large, top half of the page.'})
        row = self.row_of(result, ids[0])
        self.assertGreaterEqual(row['new_pt'], lf.cue_floor_pt(.5) - 1e-9)
        self.assertEqual(row['cue_min_pt'], 235.6)                         # to the next tenth of a point, as the heights are
        self.assertTrue(row['cue_met'])
        free, _ = self.fit()
        self.assertLess(self.row_of(free, ids[0])['new_pt'], lf.cue_floor_pt(.5))   # it is the cue that holds the row up
        self.assertNotIn('cue_min_pt', self.row_of(free, ids[0]))
        self.assertAlmostEqual(totals(result['page_rows']['1']), c.STORY_HEIGHT_PT, places=9)
        self.assertEqual(result['report']['pages']['1']['structure']['cues'],
                         {ids[0]: {'solo': False, 'min_share': .5, 'min_pt': 235.6}})

    def test_a_full_width_cue_makes_its_art_span_the_column(self):
        # Chapter 4 page 6 in miniature: "Full-width tier, not a narrow strip" over 3:1 art whose keep zones span most of
        # its height. The ratio fit gave the lettering rows the height first and left the tier a narrow centred strip.
        copies = [[chunk(HEAVY), chunk(HEAVY)], [chunk(HEAVY)], [chunk(HEAVY), chunk(HEAVY)], [chunk(LIGHT), chunk(LIGHT)],
                  [chunk(LIGHT)]]
        script = described(script_of({1: copies}), {'page-01-panel-04': 'Full-width tier, not a narrow strip. Eyes closed.',
                                                     'page-01-panel-05': 'Large, about the bottom 40 percent of the page.'})
        ids = [p['id'] for p in script['pages']['1']['panels']]
        frames = {pid: frame(1.5, 1536) for pid in ids}
        frames[ids[3]] = frame(3.0, 2169)
        faces = {pid: [(.5, .5, .1)] for pid in ids}
        keep = {ids[3]: [[.37, .16, .61, .5], [.62, .73, .91, 1.0]]}
        result = lf.fit_structures(script, {'1': [[106, 106], 106, 100, 205.5]}, frames, faces, keep=keep)
        page = result['report']['pages']['1']
        self.assertEqual(self.row_of(result, ids[3])['panels'], [ids[3]])
        self.assertGreaterEqual(page['panels'][ids[3]]['fill_width_after'], lf.SPAN_SHARE - .005)
        cue = page['structure']['cues'][ids[3]]
        self.assertTrue(cue['solo'])
        self.assertGreater(cue['min_pt'], 60)                             # the height at which the art spans the column
        self.assertGreaterEqual(self.row_of(result, ids[4])['new_pt'], lf.cue_floor_pt(.4) - 1e-9)   # the closer keeps its cue
        self.assertAlmostEqual(totals(result['page_rows']['1']), c.STORY_HEIGHT_PT, places=9)

    def test_cues_that_no_separate_rows_can_meet_pair_their_panels(self):
        descriptions = {'page-01-panel-01': 'Large, two thirds of the page.', 'page-01-panel-02': 'Large, two thirds of the page.'}
        script, ids, frames, zones, prior = self.setup_page(descriptions, count=3, prior=[170, 170, 179.5])
        result = lf.fit_structures(script, prior, frames, zones)
        page = result['report']['pages']['1']
        self.assertEqual(page['structure']['chosen'], [2, 1])              # 2 x 314 pt cannot fit in separate rows
        self.assertEqual(self.row_of(result, ids[0])['panels'], ids[:2])
        self.assertGreaterEqual(self.row_of(result, ids[0])['new_pt'], lf.cue_floor_pt(2 / 3) - 1e-9)
        prior_alt = next(alt for alt in page['structure']['alternatives'] if alt['prior'])
        self.assertFalse(prior_alt['cues_ok'])                             # the prior is kept as a candidate, but flagged
        self.assertTrue(next(alt for alt in page['structure']['alternatives'] if alt['chosen'])['cues_ok'])

    def test_a_tie_keeps_the_prior_structure_and_its_fixed_fit(self):
        script, ids, frames, zones, prior = self.setup_page(faces=False, aspect=3.0, count=3,
                                                            copies=[[], [], []], prior=[170, 170, 179.5])
        fixed = lf.fit_layout(script, prior, frames)
        result = lf.fit_structures(script, prior, frames)
        self.assertEqual(result['report']['pages']['1']['structure']['chosen'], [1, 1, 1])
        self.assertEqual(result['page_rows'], fixed['page_rows'])
        self.assertEqual(result['report']['pages']['1']['rows'], fixed['report']['pages']['1']['rows'])

    def test_a_page_missing_from_the_prior_layout_starts_from_one_equal_row_per_panel(self):
        script, ids, frames, zones, _ = self.setup_page(count=4)
        result = lf.fit_structures(script, {}, frames, zones)
        page = result['report']['pages']['1']
        self.assertEqual(page['structure']['prior'], [1, 1, 1, 1])
        self.assertTrue(page['default_rows'])
        self.assertEqual(page['structure']['candidates'], 5)
        self.assertAlmostEqual(totals(result['page_rows']['1']), c.STORY_HEIGHT_PT, places=9)
        self.assertEqual(sum(page['structure']['chosen']), 4)
        c.geometry_for_script(script, result['page_rows'])

    def test_lettering_comes_before_fill(self):
        # Two pairs span the column (fill 1.0) where four full-width rows cannot (0.87), but each panel has half the width
        # and its lettering wraps long: the ratio falls below 1, so the structure whose ratio holds is chosen.
        copies = [[chunk(HEAVY)] * 3 + [chunk(LIGHT)]] * 4
        script, ids, frames, zones, prior = self.setup_page(copies=copies, count=4, prior=[129.4, 129.4, 129.4, 129.3])
        page = lf.fit_structures(script, prior, frames, zones)['report']['pages']['1']
        alternatives = {tuple(alt['structure']): alt for alt in page['structure']['alternatives']}
        pairs, singles = alternatives[(2, 2)], alternatives[(1, 1, 1, 1)]
        self.assertGreater(pairs['min_fill'], singles['min_fill'])
        self.assertLess(pairs['min_ratio'], 1.0)
        self.assertGreaterEqual(singles['min_ratio'], 1.0)
        self.assertEqual(page['structure']['chosen'], [1, 1, 1, 1])
        self.assertLess(page['structure']['min_fill'], pairs['min_fill'])

    def test_the_fit_is_deterministic_and_the_output_has_no_dashes(self):
        first, _ = self.fit()
        second, _ = self.fit()
        self.assertEqual(first, second)
        text = json.dumps(first)
        self.assertNotIn(chr(0x2014), text)
        self.assertNotIn(chr(0x2013), text)

    def test_every_page_is_chosen_on_its_own_and_the_summary_counts_them(self):
        script = described(script_of({1: [[chunk(LIGHT)]] * 5, 2: [[chunk(LIGHT)]] * 3}), {})
        frames = {p['id']: frame(1.5, 1536) for pg in script['pages'].values() for p in pg['panels']}
        zones = {p['id']: [(.5, .5, .3)] for pg in script['pages'].values() for p in pg['panels']}
        result = lf.fit_structures(script, {'1': self.PRIOR}, frames, zones)              # page 2 has no prior rows
        self.assertEqual(sorted(result['page_rows']), ['1', '2'])
        self.assertEqual(sum(result['report']['statuses'].values()), 2)
        self.assertEqual(result['report']['structure_search']['row_sizes'], [1, 2])
        self.assertEqual(result['report']['structure_search']['pages_changed'], 1)       # three rows of 173 pt span the column
        self.assertEqual(result['report']['pages']['2']['structure']['chosen'], [1, 1, 1])
        self.assertIn(2, result['report']['pages']['1']['structure']['chosen'])
        self.assertEqual(result['report']['margin'], lf.MARGIN)


class StructureRefineTests(unittest.TestCase):
    """With a refine hook (the planner probe), the top candidates are refined and the best verified one is chosen."""

    def setUp(self):
        self.script = described(script_of({1: [[chunk(LIGHT)]] * 5}), {})
        self.ids = [p['id'] for p in self.script['pages']['1']['panels']]
        self.frames = {pid: frame(1.5, 1536) for pid in self.ids}
        self.faces = {pid: [(.5, .5, .3)] for pid in self.ids}
        self.prior = {'1': [103.1] * 5}
        self.calls = []

    def refiner(self, verified, **extra):
        def refine(page_no, page, entry, minimums):
            self.calls.append((page_no, entry, dict(minimums)))
            fitted = lf.fit_layout({'pages': {page_no: page}}, {page_no: entry}, self.frames, self.faces, minimums=minimums, **extra)
            return fitted, verified(len(self.calls))
        return refine

    def sizes(self, entry):
        return [len(row) if isinstance(row, list) else 1 for row in entry]

    def test_only_the_top_three_candidates_are_refined(self):
        result = lf.fit_structures(self.script, self.prior, self.frames, self.faces, refine=self.refiner(lambda n: True))
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(lf.PROBE_TOP, 3)
        analytic = lf.fit_structures(self.script, self.prior, self.frames, self.faces)['report']['pages']['1']['structure']
        self.assertEqual([self.sizes(entry) for _, entry, _ in self.calls],
                         [alt['structure'] for alt in analytic['alternatives'][:3]])

    def test_when_no_top_candidate_verifies_the_search_goes_on_down_the_ranking(self):
        # On a real chapter 3 page the top three structures all shared the row of a panel the planner can only
        # place full width; stopping there shipped an unverified layout although a lower-ranked one verified.
        result = lf.fit_structures(self.script, self.prior, self.frames, self.faces, refine=self.refiner(lambda n: n == 5))
        structure = result['report']['pages']['1']['structure']
        self.assertEqual(len(self.calls), 5)                                          # stops at the first that verifies
        self.assertTrue(structure['verified'])
        self.assertEqual(structure['chosen'], self.sizes(self.calls[4][1]))
        verdicts = [alt['verified'] for alt in structure['alternatives']]
        self.assertEqual((verdicts.count(True), verdicts.count(False), verdicts.count(None)), (1, 4, 3))

    def test_the_best_verified_candidate_is_chosen_and_the_others_are_marked(self):
        result = lf.fit_structures(self.script, self.prior, self.frames, self.faces, refine=self.refiner(lambda n: n == 2))
        structure = result['report']['pages']['1']['structure']
        self.assertEqual(structure['chosen'], self.sizes(self.calls[1][1]))        # the second-ranked one passed its probe
        self.assertTrue(structure['verified'])
        verdicts = [alt['verified'] for alt in structure['alternatives']]
        self.assertEqual(verdicts.count(True), 1)
        self.assertEqual(verdicts.count(False), 2)
        self.assertEqual(verdicts.count(None), 5)                                   # the rest were never asked
        self.assertEqual(next(alt for alt in structure['alternatives'] if alt['chosen'])['verified'], True)

    def test_when_none_verifies_the_best_analytic_candidate_stands_unverified(self):
        result = lf.fit_structures(self.script, self.prior, self.frames, self.faces, refine=self.refiner(lambda n: False))
        structure = result['report']['pages']['1']['structure']
        self.assertEqual(structure['chosen'], self.sizes(self.calls[0][1]))
        self.assertIs(structure['verified'], False)
        # Deliberately changed from 3: when none of the top three verifies, every other candidate is asked too.
        self.assertEqual(len(self.calls), 8)
        self.assertEqual([alt['verified'] for alt in structure['alternatives']].count(False), 8)

    def test_the_refined_heights_are_the_ones_written_and_cues_reach_the_hook(self):
        script = described(script_of({1: [[chunk(LIGHT)]] * 5}), {self.ids[0]: 'Large, top half of the page.'})
        seen = []

        def refine(page_no, page, entry, minimums):
            seen.append(dict(minimums))
            fitted = lf.fit_layout({'pages': {page_no: page}}, {page_no: entry}, self.frames, self.faces,
                                   minimums=minimums, floors={self.ids[4]: 150})
            return fitted, True
        result = lf.fit_structures(script, self.prior, self.frames, self.faces, refine=refine)
        self.assertEqual(seen[0], {self.ids[0]: lf.cue_floor_pt(.5)})
        last = next(row for row in result['report']['pages']['1']['rows'] if self.ids[4] in row['panels'])
        self.assertGreaterEqual(last['new_pt'], 150)                               # the hook's floor is in the chosen layout
        plain = lf.fit_structures(script, self.prior, self.frames, self.faces)
        self.assertLess(next(row for row in plain['report']['pages']['1']['rows'] if self.ids[4] in row['panels'])['new_pt'], 150)
        self.assertEqual(result['report']['pages']['1']['min_ratio_before'],
                         lf.fit_layout(script, self.prior, self.frames, self.faces)['report']['pages']['1']['min_ratio_before'])

    def test_a_refined_candidate_is_ranked_by_its_refined_heights(self):
        # The hook's floors change the fills, so the verified candidates are ranked again on what they became.
        result = lf.fit_structures(self.script, self.prior, self.frames, self.faces, refine=self.refiner(lambda n: True))
        structure = result['report']['pages']['1']['structure']
        probed = [alt for alt in structure['alternatives'] if alt['verified']]
        self.assertEqual(len(probed), 3)
        keys = [(round(alt['min_fill'], 3), round(alt['mean_fill'], 3)) for alt in probed]
        self.assertEqual(keys, sorted(keys, reverse=True))
        self.assertEqual(probed[0]['chosen'], True)


class RealChapterFourTests(unittest.TestCase):
    """The real chapter 4 frames, through the same fit (skipped when they are not readable)."""

    def test_the_chapter_fits_with_exact_totals_bounds_and_a_better_minimum(self):
        import run_chapter as r
        package = V15 / 'chapters' / 'ch04'
        try:
            prior = json.loads((package / 'LAYOUT.json').read_text())['page_rows']
            job = json.loads((package / 'IMAGEGEN-JOBS.json').read_text())
            script = job['script']
            inputs = r.fit_inputs(package, package / 'SELECTION-INPUT-drawn-r4.json',
                                  package / 'review' / 'LEAN-SELECTION-drawn-merged-r2.json',
                                  package / 'review' / 'geometry-drawn-r4', 0.55, script=script)
        except (OSError, ValueError, KeyError):
            self.skipTest('chapter 4 files are not readable')
        self.assertGreaterEqual(len(inputs['painted']), 8)             # the planner's painted regions are held in the crop too
        result = lf.fit_layout(script, prior, inputs['frames'], inputs['faces'], painted=inputs['painted'], keep=inputs['keep'])
        geometry = c.geometry_for_script(script, result['page_rows'])
        self.assertEqual(sorted(geometry['pages']), sorted(prior))
        for page, rows in result['page_rows'].items():
            self.assertAlmostEqual(totals(rows), c.STORY_HEIGHT_PT, places=9, msg=page)
            self.assertEqual(shape(rows), shape(prior[page]))
            report = result['report']['pages'][page]
            # Within the sawtooth a word wrap makes of the ratio (a few percent).
            self.assertGreaterEqual(report['min_ratio_after'], .95 * min(report['min_ratio_before'], lf.MARGIN))
            for new, old in zip(heights(rows), heights(prior[page])):
                self.assertGreaterEqual(new, min(lf.MIN_ROW_PT, old) - 1e-9)
                self.assertLessEqual(new, lf.MAX_GROWTH * old + 1e-9)
        # The pages with the heaviest lettering improve.
        improved = [p for p, v in result['report']['pages'].items() if v['min_ratio_after'] > v['min_ratio_before'] + .05]
        self.assertGreaterEqual(len(improved), 3)


if __name__ == '__main__':
    unittest.main()
