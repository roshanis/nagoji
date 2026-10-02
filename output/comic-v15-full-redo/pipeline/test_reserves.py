import itertools
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
from PIL import Image, ImageDraw

import reserves as rv

V15 = Path(__file__).resolve().parent.parent
OUTLINE = 4
INK = (15, 15, 15)


def painted_background(size, seed=7):
    """Smooth, noisy, mid to dark colour field that never reaches the near-white range."""
    width, height = size
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:height, 0:width]
    base = np.zeros((height, width, 3), float)
    base[..., 0] = 80 + 40 * np.sin(xx / 90.0) + 30 * np.cos(yy / 60.0)
    base[..., 1] = 60 + 35 * np.sin(yy / 70.0)
    base[..., 2] = 50 + 30 * np.cos((xx + yy) / 110.0)
    base += rng.normal(0, 14, base.shape)
    return np.clip(base, 0, 175).astype(np.uint8)


def frame(size=(1200, 600), boxes=(), balloons=(), distractors=(), specks=(), seed=7):
    """Return a PIL image with outlined blank shapes on a painted background.

    boxes: (x0, y0, x1, y1) rounded rectangles. balloons: (x0, y0, x1, y1, tail_tip)
    ellipses with a triangular tail. distractors: unoutlined bright polygons. specks:
    (x, y) dark marks drawn inside shapes.
    """
    rng = np.random.default_rng(seed + 1)
    image = Image.fromarray(painted_background(size, seed))
    draw = ImageDraw.Draw(image)
    interior = Image.new('L', size, 0)
    idraw = ImageDraw.Draw(interior)
    for rect in boxes:
        draw.rounded_rectangle(rect, radius=18, fill=INK)
        inner = [rect[0] + OUTLINE, rect[1] + OUTLINE, rect[2] - OUTLINE, rect[3] - OUTLINE]
        idraw.rounded_rectangle(inner, radius=14, fill=255)
    for x0, y0, x1, y1, tip in balloons:
        cx = (x0 + x1) // 2
        draw.ellipse([x0, y0, x1, y1], fill=INK)
        draw.polygon([(cx - 30, y1 - 8), (cx + 30, y1 - 8), tip], fill=INK)
        idraw.ellipse([x0 + OUTLINE, y0 + OUTLINE, x1 - OUTLINE, y1 - OUTLINE], fill=255)
        idraw.polygon([(cx - 26, y1 - 8), (cx + 26, y1 - 8), (tip[0], tip[1] - 6)], fill=255)
    array = np.asarray(image).copy()
    mask = np.asarray(interior) > 0
    array[mask] = 250 - rng.integers(0, 5, size=(int(mask.sum()), 1))
    image = Image.fromarray(array)
    draw = ImageDraw.Draw(image)
    for polygon in distractors:
        draw.polygon(polygon, fill=(240, 232, 216))
    for x, y in specks:
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(60, 50, 40))
    return image


def save(image, directory, name='frame.png'):
    path = Path(directory) / name
    image.save(path)
    return path


def light_everywhere(image, rect):
    x0, y0, x1, y1 = rect
    pixels = np.asarray(image.convert('RGB'), dtype=float)[y0:y1, x0:x1]
    return bool((pixels.mean(axis=2) > 190).all())


class Tmp(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.dir = Path(self.temporary.name)


class HelperTests(unittest.TestCase):
    def test_largest_rectangle_finds_the_biggest_all_true_block(self):
        mask = np.zeros((12, 14), bool)
        mask[2:7, 3:10] = True      # 5 rows by 7 columns = 35
        mask[9:11, 0:4] = True      # smaller blob
        self.assertEqual(tuple(rv.largest_rectangle(mask)), (3, 2, 10, 7))

    def test_largest_rectangle_of_empty_mask_is_none(self):
        self.assertIsNone(rv.largest_rectangle(np.zeros((5, 5), bool)))

    def test_reading_order_rows_then_left_to_right(self):
        rects = [
            [700, 30, 1000, 120],    # top row, right
            [100, 300, 500, 380],    # bottom row
            [100, 20, 400, 100],     # top row, left
            [520, 50, 650, 130],     # top row: overlaps the row by more than half, middle
        ]
        self.assertEqual(rv.reading_order(rects), [2, 3, 0, 1])

    def test_reading_order_barely_overlapping_rects_are_separate_rows(self):
        rects = [[0, 0, 100, 100], [200, 90, 300, 190]]   # 10 px overlap of 100
        self.assertEqual(rv.reading_order(rects), [0, 1])
        # The lower-left one is a later row even though it is further left.
        rects = [[200, 0, 300, 100], [0, 90, 100, 190]]
        self.assertEqual(rv.reading_order(rects), [0, 1])


class DetectReservesTests(Tmp):
    def test_two_outlined_boxes_found_in_reading_order_inset_and_fully_light(self):
        left = (60, 40, 560, 160)
        right = (660, 90, 1140, 200)
        image = frame(boxes=[right, left])    # drawn in the opposite order on purpose
        path = save(image, self.dir)
        result = rv.detect_reserves(path, 2, ['CAPTION', 'JOÃO'])
        self.assertEqual(result['visible_rect'], [0, 0, 1200, 600])
        found = result['reserves']
        self.assertEqual(len(found), 2)
        self.assertEqual([r['kind'] for r in found], ['caption', 'speech'])
        self.assertEqual([r['copy_indices'] for r in found], [[0], [1]])
        for reserve, box in zip(found, [left, right]):
            x0, y0, x1, y1 = reserve['rect']
            self.assertTrue(all(isinstance(v, int) for v in reserve['rect']))
            self.assertTrue(light_everywhere(image, reserve['rect']))
            # Inset from the outline: 4 px stroke plus the 6 px inset, one pixel of slack.
            self.assertGreaterEqual(x0, box[0] + OUTLINE + 5)
            self.assertGreaterEqual(y0, box[1] + OUTLINE + 5)
            self.assertLessEqual(x1, box[2] - OUTLINE - 5 + 1)
            self.assertLessEqual(y1, box[3] - OUTLINE - 5 + 1)
            # Still uses most of the blank space.
            area = (x1 - x0) * (y1 - y0)
            self.assertGreater(area, .6 * (box[2] - box[0]) * (box[3] - box[1]))

    def test_balloon_with_tail_caption_and_reading_order_across_rows(self):
        caption_a = (40, 30, 520, 120)
        balloon = (600, 50, 1120, 190, (700, 330))
        caption_b = (60, 440, 700, 560)
        image = frame(boxes=[caption_b, caption_a], balloons=[balloon])
        path = save(image, self.dir)
        result = rv.detect_reserves(path, 3, ['CAPTION', 'NAGOJI', 'CAPTION'])
        found = result['reserves']
        self.assertEqual([r['kind'] for r in found], ['caption', 'speech', 'caption'])
        centres = [((r['rect'][0] + r['rect'][2]) / 2, (r['rect'][1] + r['rect'][3]) / 2) for r in found]
        self.assertLess(centres[0][0], 520)
        self.assertGreater(centres[1][0], 600)
        self.assertGreater(centres[2][1], 400)
        for reserve in found:
            self.assertTrue(light_everywhere(image, reserve['rect']))
        # The balloon rectangle sits inside the ellipse body, not down the tail.
        self.assertLess(found[1]['rect'][3], 190)

    def test_bright_unoutlined_shape_is_not_taken_for_a_reserve(self):
        real = [(40, 40, 540, 150), (640, 40, 1140, 150)]
        star = [(300, 300), (340, 380), (430, 370), (370, 430), (400, 520), (320, 470),
                (240, 520), (270, 430), (210, 370), (300, 380)]
        blob = [(800, 300), (1000, 320), (1100, 420), (1020, 540), (860, 500), (760, 420)]
        image = frame(boxes=real, distractors=[star, blob])
        path = save(image, self.dir)
        result = rv.detect_reserves(path, 2, ['CAPTION', 'CAPTION'])
        for reserve, box in zip(result['reserves'], real):
            self.assertLess(reserve['rect'][3], 200)
            self.assertTrue(light_everywhere(image, reserve['rect']))
            self.assertGreater(reserve['rect'][0], box[0])
            self.assertLess(reserve['rect'][2], box[2])

    def test_a_small_outlined_bright_patch_is_not_taken_for_a_painted_region(self):
        # Chapter 2 5.5 and 4.5: a patch of bright sky framed by an arm and the hatch coaming, and pale cloth, measured
        # 0.31 to 0.46 percent of the frame, were found as painted blank shapes the lettering had to cover. Real painted
        # boxes in the reviewed selections have bounding boxes of 1.6 percent of the frame or more.
        small = (100, 100, 170, 160)                       # its blank interior is about 0.45 percent of 1200 x 600
        real = (400, 300, 760, 420)                        # 360 x 120 = 6 percent
        path = save(frame(boxes=[small, real]), self.dir)
        regions = rv.find_regions(path, 2)['regions']
        self.assertEqual(len(regions), 1)
        self.assertGreater(regions[0]['bbox'][0], 300)
        self.assertLess(rv.MIN_AREA_FRACTION, .01)          # a box near the smallest real ones keeps a wide margin

    def test_small_dark_mark_inside_a_box_does_not_lose_or_split_it(self):
        box = (100, 100, 700, 260)
        image = frame(boxes=[box], specks=[(400, 180)])
        path = save(image, self.dir)
        result = rv.detect_reserves(path, 1, ['CAPTION'])
        self.assertEqual(len(result['reserves']), 1)
        self.assertTrue(light_everywhere(image, result['reserves'][0]['rect']))

    def test_frame_without_padding_keeps_the_whole_image_as_visible(self):
        path = save(frame(boxes=[(100, 100, 700, 260)]), self.dir)
        self.assertEqual(rv.art_bounds(np.asarray(Image.open(path).convert('RGB'))), [0, 0, 1200, 600])

    def test_a_thin_noisy_white_margin_is_trimmed_but_a_pale_sky_is_not(self):
        # A real frame had a 12 px white margin down each side that was only 92 to 98 percent near-white (soft specks),
        # so the strict 99.5 percent rule kept it and it printed as a white strip inside the panel border.
        rng = np.random.default_rng(5)
        array = rng.integers(20, 120, (600, 1200, 3), dtype=np.uint8)
        margin = np.full((600, 12, 3), 250, dtype=np.uint8)
        specks = rng.random((600, 12)) < .06
        margin[specks] = 150
        array[:, :12] = margin
        array[:, -12:] = margin
        array[::3, 10] = 140                                     # a faint grey line inside the left margin, as on the real frame
        self.assertEqual(rv.art_bounds(array), [12 + rv.PAD_SAFETY_PX, 0, 1200 - 12 - rv.PAD_SAFETY_PX, 600])
        # A pale, nearly white sky across the top fifth is art, not a margin: it is too deep, and it fades into the scene.
        sky = rng.integers(20, 120, (600, 1200, 3), dtype=np.uint8)
        sky[:120] = 245
        sky[:120][rng.random((120, 1200)) < .05] = 200
        self.assertEqual(rv.art_bounds(sky)[1], 0)

    def test_a_thin_cream_paper_margin_is_trimmed_and_is_not_taken_for_a_painted_region(self):
        # A real frame (3.7.4) was painted inside a cream paper border, (251, 244, 234) with a little grain, 25 px
        # deep under a black frame line. Its blue channel sits just below the near-white test, so the margin was
        # kept and then found as a painted blank shape that the lettering had to cover.
        rng = np.random.default_rng(7)
        array = rng.integers(20, 120, (1024, 1536, 3), dtype=np.uint8)
        paper = np.array([251, 244, 234]) + rng.integers(-5, 4, (1024, 1536, 3))
        border = np.zeros((1024, 1536), dtype=bool)
        border[-25:], border[:, :14], border[:, -13:] = True, True, True
        array[border] = paper[border]
        array[-28:-25, 14:-13] = 15                                   # the black frame line above the bottom margin
        bounds = rv.art_bounds(array)
        self.assertEqual(bounds[3], 1024 - 25 - rv.PAD_SAFETY_PX)
        self.assertEqual(bounds[0], 14 + rv.PAD_SAFETY_PX)
        path = self.dir / 'paper.png'
        Image.fromarray(array).save(path)
        self.assertEqual(rv.find_regions(path, 1)['regions'], [])

    def test_black_letterbox_bars_are_trimmed_but_dark_art_is_kept(self):
        # The generator sometimes pads with pure black bars (a 1976 x 796 frame with 186 and 200 px bars);
        # rows of dark but textured art are not padding.
        array = np.asarray(frame(boxes=[(100, 100, 700, 260)])).copy()
        array[:70] = 0
        array[-50:] = 3
        array[:, :4] = 2                                   # a thin black side border
        bounds = rv.art_bounds(array)
        self.assertEqual(bounds, [4 + rv.PAD_SAFETY_PX, 70 + rv.PAD_SAFETY_PX, 1200, 600 - 50 - rv.PAD_SAFETY_PX])
        rng = np.random.default_rng(3)
        dark = rng.integers(0, 40, (600, 1200, 3), dtype=np.uint8)     # a night scene: dark, never flat black
        self.assertEqual(rv.art_bounds(dark), [0, 0, 1200, 600])

    def test_white_letterbox_bars_are_excluded_from_visible_rect_and_search(self):
        box = (60, 140, 560, 260)
        image = frame(boxes=[box])
        array = np.asarray(image).copy()
        array[:80] = 255
        array[-90:] = 255
        array[80:83] = 15        # the art's own black frame line
        array[-93:-90] = 15
        image = Image.fromarray(array)
        path = save(image, self.dir)
        result = rv.detect_reserves(path, 1, ['CAPTION'])
        # 80 and 90 px of bars, plus two pixels of seam on each padded side.
        self.assertEqual(result['visible_rect'], [0, 82, 1200, 600 - 92])
        x0, y0, x1, y1 = result['reserves'][0]['rect']
        self.assertGreaterEqual(y0, 140 + OUTLINE + 5)
        self.assertTrue(light_everywhere(image, [x0, y0, x1, y1]))
        # The bars alone never count as reserves.
        with self.assertRaises(rv.ReserveError):
            rv.detect_reserves(path, 2, ['CAPTION', 'CAPTION'])

    def test_thin_white_border_all_round_is_excluded(self):
        box = (100, 100, 700, 260)
        array = np.asarray(frame(boxes=[box])).copy()
        pad = 12
        array[:pad] = 255; array[-pad:] = 255; array[:, :pad] = 255; array[:, -pad:] = 255
        image = Image.fromarray(array)
        path = save(image, self.dir)
        result = rv.detect_reserves(path, 1, ['CAPTION'])
        self.assertEqual(result['visible_rect'], [14, 14, 1200 - 14, 600 - 14])
        self.assertEqual(len(result['reserves']), 1)
        x0, y0, x1, y1 = result['reserves'][0]['rect']
        self.assertTrue(100 < x0 < x1 < 700 and 100 < y0 < y1 < 260)
        self.assertTrue(light_everywhere(image, [x0, y0, x1, y1]))

    def test_double_outlined_box_counts_once(self):
        array = np.asarray(frame()).copy()
        image = Image.fromarray(array)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((100, 100, 700, 280), radius=20, fill=INK)
        draw.rounded_rectangle((104, 104, 696, 276), radius=17, fill=(250, 250, 248))   # white rim
        draw.rounded_rectangle((116, 116, 684, 264), radius=12, fill=INK)               # inner line
        draw.rounded_rectangle((119, 119, 681, 261), radius=10, fill=(250, 250, 248))   # blank interior
        path = save(image, self.dir)
        result = rv.detect_reserves(path, 1, ['CAPTION'])
        self.assertEqual(len(result['reserves']), 1)
        self.assertTrue(light_everywhere(image, result['reserves'][0]['rect']))
        with self.assertRaises(rv.ReserveError) as caught:
            rv.detect_reserves(path, 2, ['CAPTION', 'CAPTION'])
        self.assertEqual(caught.exception.found, 1)

    def test_inset_is_six_pixels_by_default_and_can_be_changed(self):
        path = save(frame(boxes=[(100, 100, 700, 260)]), self.dir)
        default = rv.detect_reserves(path, 1, ['CAPTION'])['reserves'][0]['rect']
        bare = rv.detect_reserves(path, 1, ['CAPTION'], inset=0)['reserves'][0]['rect']
        self.assertEqual(default, [bare[0] + 6, bare[1] + 6, bare[2] - 6, bare[3] - 6])
        two = rv.detect_reserves(path, 1, ['CAPTION'], inset=2)['reserves'][0]['rect']
        self.assertEqual(two, [bare[0] + 2, bare[1] + 2, bare[2] - 2, bare[3] - 2])
        for bad in (-1, 9, 2.5):
            with self.assertRaises(ValueError):
                rv.detect_reserves(path, 1, ['CAPTION'], inset=bad)

    def test_count_larger_than_available_raises_with_summary(self):
        image = frame(boxes=[(100, 100, 700, 260)])
        path = save(image, self.dir)
        with self.assertRaises(rv.ReserveError) as caught:
            rv.detect_reserves(path, 2, ['CAPTION', 'CAPTION'])
        error = caught.exception
        self.assertEqual(error.found, 1)
        self.assertEqual(error.count, 2)
        self.assertEqual(len(error.regions), 1)
        self.assertIn('bbox', error.regions[0])
        self.assertIn('found 1', str(error))
        self.assertIn('2', str(error))

    def test_tiny_outlined_shapes_are_ignored(self):
        image = frame(boxes=[(100, 100, 700, 260), (900, 400, 930, 430)])
        path = save(image, self.dir)
        with self.assertRaises(rv.ReserveError) as caught:
            rv.detect_reserves(path, 2, ['CAPTION', 'CAPTION'])
        self.assertEqual(caught.exception.found, 1)

    def test_zero_count_returns_no_reserves(self):
        for boxes in ([], [(100, 100, 700, 260)]):
            path = save(frame(boxes=boxes), self.dir, f'z{len(boxes)}.png')
            result = rv.detect_reserves(path, 0, [])
            self.assertEqual(result, {'visible_rect': [0, 0, 1200, 600], 'reserves': []})

    def test_kind_comes_from_speaker(self):
        boxes = [(40, 40, 400, 140), (440, 40, 800, 140), (840, 40, 1160, 140)]
        path = save(frame(boxes=boxes), self.dir)
        result = rv.detect_reserves(path, 3, ['CAPTION', 'Caption (voice over)', 'PRISONER'])
        self.assertEqual([r['kind'] for r in result['reserves']], ['caption', 'caption', 'speech'])
        self.assertEqual([r['copy_indices'] for r in result['reserves']], [[0], [1], [2]])

    def test_speakers_must_match_count(self):
        path = save(frame(boxes=[(100, 100, 700, 260)]), self.dir)
        with self.assertRaises(ValueError):
            rv.detect_reserves(path, 1, ['CAPTION', 'JOÃO'])

    def test_result_is_json_serialisable_and_missing_image_is_clear(self):
        path = save(frame(boxes=[(100, 100, 700, 260)]), self.dir)
        json.dumps(rv.detect_reserves(path, 1, ['CAPTION']))
        with self.assertRaises(FileNotFoundError):
            rv.detect_reserves(self.dir / 'absent.png', 1, ['CAPTION'])


def quiet_frame(size=(1200, 600), busy=((0, 0, 400, 600), (0, 300, 1200, 600)), seed=11):
    """Smooth art with busy (noisy) areas: the quiet part is the top right."""
    rng = np.random.default_rng(seed)
    width, height = size
    yy, xx = np.mgrid[0:height, 0:width]
    base = np.stack([60 + 20 * xx / width, 70 + 20 * yy / height, 90 + 0 * xx], axis=-1).astype(float)
    for x0, y0, x1, y1 in busy:
        base[y0:y1, x0:x1] += rng.normal(0, 55, (y1 - y0, x1 - x0, 3))
    return Image.fromarray(np.clip(base, 0, 200).astype(np.uint8))


def separate(a, b):
    return a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1]


class FindRegionsTests(Tmp):
    def test_regions_listed_in_reading_order_and_a_shortage_does_not_raise(self):
        path = save(frame(boxes=[(700, 100, 1100, 200), (100, 100, 500, 200)]), self.dir)
        found = rv.find_regions(path, 3)
        self.assertEqual(found['size'], [1200, 600])
        self.assertEqual(found['visible_rect'], [0, 0, 1200, 600])
        self.assertEqual(len(found['regions']), 2)
        left, right = found['regions']
        self.assertLess(left['bbox'][0], right['bbox'][0])
        for region, box in zip(found['regions'], [(100, 100, 500, 200), (700, 100, 1100, 200)]):
            x0, y0, x1, y1 = region['bbox']
            self.assertTrue(box[0] <= x0 <= box[0] + 8 and box[1] <= y0 <= box[1] + 8)
            self.assertTrue(box[2] - 8 <= x1 <= box[2] and box[3] - 8 <= y1 <= box[3])
        self.assertEqual(len(rv.find_regions(path, 1)['regions']), 1)
        self.assertEqual(rv.find_regions(path, 0)['regions'], [])
        self.assertEqual(rv.find_regions(save(frame(), self.dir, 'none.png'), 2)['regions'], [])


class PlaceBoxesTests(Tmp):
    def found(self, image, name='p.png', count=4):
        return rv.find_regions(save(image, self.dir, name), count), self.dir / name

    def test_box_covers_the_painted_region_and_eight_more_pixels(self):
        found, path = self.found(frame(boxes=[(100, 100, 700, 260)]))
        bbox = found['regions'][0]['bbox']
        result = rv.place_boxes(path, found, [[(300, 60)]])
        box = result['boxes'][0]
        self.assertEqual(result['painted'], [True])
        self.assertTrue(box[0] <= bbox[0] - 8 and box[1] <= bbox[1] - 8 and box[2] >= bbox[2] + 8 and box[3] >= bbox[3] + 8)
        # The painted outline (the drawn box 100..700 by 100..260) is fully hidden.
        self.assertTrue(box[0] <= 100 and box[1] <= 100 and box[2] >= 700 and box[3] >= 260)

    def test_box_grows_to_the_needed_size_centred_on_the_region(self):
        found, path = self.found(frame(boxes=[(100, 100, 700, 260)]))
        box = rv.place_boxes(path, found, [[(800, 300)]])['boxes'][0]
        self.assertEqual((box[2] - box[0], box[3] - box[1]), (800, 300))
        bbox = found['regions'][0]['bbox']
        self.assertAlmostEqual((box[0] + box[2]) / 2, (bbox[0] + bbox[2]) / 2, delta=1)
        self.assertAlmostEqual((box[1] + box[3]) / 2, (bbox[1] + bbox[3]) / 2, delta=1)

    def test_box_is_kept_inside_the_visible_rect_and_still_covers_the_region(self):
        found, path = self.found(frame(boxes=[(10, 10, 300, 120)]))
        bbox = found['regions'][0]['bbox']
        box = rv.place_boxes(path, found, [[(500, 200)]])['boxes'][0]
        self.assertTrue(box[0] >= 0 and box[1] >= 0 and box[2] <= 1200 and box[3] <= 600)
        self.assertTrue(box[0] <= bbox[0] and box[1] <= bbox[1] and box[2] >= bbox[2] and box[3] >= bbox[3])
        with self.assertRaisesRegex(rv.PlacementError, 'chunk 0'):
            rv.place_boxes(path, found, [[(1300, 200)]])          # wider than the frame

    def test_first_option_that_avoids_overlap_is_used(self):
        found, path = self.found(frame(boxes=[(100, 100, 500, 200), (520, 100, 920, 200)]))
        result = rv.place_boxes(path, found, [[(900, 100), (380, 100)], [(380, 100)]])
        self.assertEqual(result['choice'], [1, 0])
        self.assertTrue(separate(*result['boxes']))

    def test_overlapping_boxes_are_shifted_apart_when_room_allows(self):
        found, path = self.found(frame(boxes=[(100, 100, 400, 200), (600, 100, 900, 200)]))
        result = rv.place_boxes(path, found, [[(500, 120)], [(500, 120)]])
        first, second = result['boxes']
        self.assertTrue(separate(first, second))
        for box, bbox in zip(result['boxes'], [r['bbox'] for r in found['regions']]):
            self.assertTrue(box[0] <= bbox[0] and box[2] >= bbox[2] and box[1] <= bbox[1] and box[3] >= bbox[3])

    def test_boxes_that_cannot_be_kept_apart_fail_clearly(self):
        found, path = self.found(frame(boxes=[(100, 100, 500, 200), (520, 100, 920, 200)]))
        with self.assertRaises(rv.PlacementError) as caught:
            rv.place_boxes(path, found, [[(900, 100)], [(380, 100)]])
        self.assertIn('chunk 0', str(caught.exception))
        self.assertIn('overlap', str(caught.exception))

    def test_without_painted_regions_boxes_go_in_the_quietest_area_near_the_top(self):
        image = quiet_frame()
        found, path = self.found(image, 'quiet.png')
        self.assertEqual(found['regions'], [])
        result = rv.place_boxes(path, found, [[(300, 100)]])
        x0, y0, x1, y1 = result['boxes'][0]
        self.assertEqual(result['painted'], [False])
        self.assertEqual((x1 - x0, y1 - y0), (300, 100))
        self.assertGreaterEqual(x0, 380)             # right of the busy band on the left
        self.assertLess(y0, 200)                     # top of the frame, above the busy lower half

    def test_boxes_avoid_each_other_and_a_margin_around_every_tail_target(self):
        found, path = self.found(quiet_frame(), 'quiet2.png')
        targets = [(900, 60), (520, 200)]
        result = rv.place_boxes(path, found, [[(300, 100)], [(300, 100)]], targets)
        first, second = result['boxes']
        self.assertTrue(separate(first, second))
        guard = .08 * 600
        for box in result['boxes']:
            for tx, ty in targets:
                nearest = np.hypot(max(box[0] - tx, 0, tx - box[2]), max(box[1] - ty, 0, ty - box[3]))
                self.assertGreaterEqual(nearest, guard - 1)
        centre = lambda b: ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        (cx1, cy1), (cx2, cy2) = centre(first), centre(second)
        self.assertTrue(cy2 > cy1 + 50 or (abs(cy2 - cy1) <= 50 and cx2 > cx1))   # reading order

    def test_no_clear_area_fails_clearly(self):
        found, path = self.found(quiet_frame(), 'quiet3.png')
        with self.assertRaisesRegex(rv.PlacementError, 'chunk 1'):
            rv.place_boxes(path, found, [[(1100, 400)], [(1100, 400)]])


def near(box, point, margin):
    """True when a point is inside a box or within `margin` pixels of it."""
    return box[0] - margin < point[0] < box[2] + margin and box[1] - margin < point[1] < box[3] + margin


class TailAvoidanceTests(Tmp):
    """A box must not cover its speaker's mouth: it grows away from the tail point instead."""

    MARGIN = 12

    def place(self, boxes, options, targets, name='t.png', margin=None):
        found = rv.find_regions(save(frame(boxes=boxes), self.dir, name), 4)
        path = self.dir / name
        result = rv.place_boxes(path, found, options, targets, tail_margin=margin or self.MARGIN)
        return found, result

    @staticmethod
    def cover(found, i=0):
        x0, y0, x1, y1 = found['regions'][i]['bbox']
        return [x0 - 8, y0 - 8, x1 + 8, y1 + 8]

    def test_a_box_that_would_swallow_the_tail_point_grows_away_from_it(self):
        found, result = self.place([(400, 100, 800, 200)], [[(700, 100)]], [(900, 150)])
        box, cover = result['boxes'][0], self.cover(found)
        self.assertFalse(near(box, (900, 150), self.MARGIN))
        # The tail point is to the right, so the right edge stays at the region's edge and the box extends left.
        self.assertEqual(box[2], cover[2])
        self.assertEqual(box[2] - box[0], 700)
        self.assertTrue(box[0] <= cover[0] and box[1] <= cover[1] and box[3] >= cover[3])
        self.assertEqual(result['partial'], [False])

    def test_the_perpendicular_directions_are_tried_when_the_first_is_blocked(self):
        # At the left edge the box cannot extend left, so it grows up, away from a tail point below it.
        found, result = self.place([(10, 200, 310, 300)], [[(500, 300)]], [(400, 380)])
        box, cover = result['boxes'][0], self.cover(found)
        self.assertFalse(near(box, (400, 380), self.MARGIN))
        self.assertEqual(box[0], 0)
        self.assertEqual(box[3], cover[3])                 # bottom edge anchored at the region, extending upward
        self.assertTrue(box[1] < cover[1])

    def test_a_tail_point_inside_the_painted_region_leaves_it_partly_covered_and_is_reported(self):
        found, result = self.place([(100, 100, 700, 260)], [[(250, 100)]], [(400, 180)])
        box, cover = result['boxes'][0], self.cover(found)
        self.assertEqual(result['partial'], [True])
        self.assertEqual(result['painted'], [True])
        self.assertFalse(near(box, (400, 180), self.MARGIN))
        # It covers the larger side of the region rather than nothing.
        self.assertGreaterEqual((box[2] - box[0]) * (box[3] - box[1]), .3 * (cover[2] - cover[0]) * (cover[3] - cover[1]))
        self.assertTrue(box[0] >= 0 and box[1] >= 0 and box[2] <= 1200 and box[3] <= 600)

    def test_a_tail_point_on_the_frame_edge_is_outside_the_frame_and_never_blocks(self):
        found, result = self.place([(400, 10, 800, 110)], [[(500, 150)]], [(600, 0)])
        box = result['boxes'][0]
        self.assertEqual(box[1], 0)                        # the box may touch the edge its speaker is beyond
        self.assertEqual(result['partial'], [False])
        for edge in ((0, 300), (1199, 300), (600, 599), (600, -20)):
            with self.subTest(target=edge):
                found, result = self.place([(400, 250, 800, 350)], [[(500, 150)]], [edge], name='e.png')
                self.assertEqual(result['partial'], [False])
        # The same x just inside the frame is an ordinary target, inside the painted region: it is kept clear
        # and the region is reported as only partly covered.
        found, result = self.place([(400, 10, 800, 110)], [[(500, 150)]], [(600, 40)], name='inside.png')
        self.assertEqual(result['partial'], [True])
        self.assertFalse(near(result['boxes'][0], (600, 40), self.MARGIN))

    def test_narrower_wraps_are_tried_with_growth_away_before_failing(self):
        found, result = self.place([(500, 200, 700, 300)], [[(1000, 150), (300, 150)]], [(740, 250)])
        self.assertEqual(result['choice'], [1])
        box, cover = result['boxes'][0], self.cover(found)
        self.assertFalse(near(box, (740, 250), self.MARGIN))
        self.assertEqual(box[2], cover[2])

    def test_another_chunks_tail_point_is_kept_clear_too(self):
        image = frame(boxes=[(100, 100, 500, 200)])
        found = rv.find_regions(save(image, self.dir, 'k.png'), 1)
        result = rv.place_boxes(self.dir / 'k.png', found, [[(800, 120), (450, 120)], [(200, 60)]],
                                [None, (560, 205)], tail_margin=self.MARGIN)
        self.assertEqual(result['choice'][0], 1)
        first, second = result['boxes']
        self.assertFalse(near(first, (560, 205), self.MARGIN))
        self.assertTrue(separate(first, second))
        guard = .08 * 600
        nearest = np.hypot(max(second[0] - 560, 0, 560 - second[2]), max(second[1] - 205, 0, 205 - second[3]))
        self.assertGreaterEqual(nearest, guard - 1)

    def test_when_no_box_can_avoid_the_tail_point_the_error_says_so(self):
        found = rv.find_regions(save(frame(boxes=[(0, 96, 1199, 204)]), self.dir, 'w.png'), 1)
        with self.assertRaises(rv.PlacementError) as caught:
            rv.place_boxes(self.dir / 'w.png', found, [[(1200, 590)]], [(600, 230)], tail_margin=self.MARGIN)
        self.assertIn('chunk 0', str(caught.exception))
        self.assertIn('tail point', str(caught.exception))

    def test_the_error_names_why_a_box_cannot_be_placed(self):
        # Painted regions too close for their boxes to cover both: the regions themselves collide.
        found = rv.find_regions(save(frame(boxes=[(100, 100, 500, 200), (506, 100, 900, 200)]), self.dir, 'c.png'), 2)
        with self.assertRaises(rv.PlacementError) as caught:
            rv.place_boxes(self.dir / 'c.png', found, [[(300, 60)], [(300, 60)]])
        message = str(caught.exception)
        self.assertIn('chunk 0', message)
        self.assertIn("painted region is within 4 px of chunk 1's painted region", message)
        # A box that must be wider than the gap between two painted regions always overlaps them.
        found = rv.find_regions(save(frame(boxes=[(100, 100, 400, 200), (430, 100, 730, 200), (760, 100, 1060, 200)]),
                                     self.dir, 'g.png'), 3)
        with self.assertRaises(rv.PlacementError) as caught:
            rv.place_boxes(self.dir / 'g.png', found, [[(320, 100)], [(500, 100)], [(320, 100)]])
        self.assertIn('chunk 1', str(caught.exception))
        self.assertIn('would always overlap', str(caught.exception))
        # A box tall enough to reach the speaker's mouth whatever its position.
        found = rv.find_regions(save(frame(boxes=[(100, 100, 700, 200)]), self.dir, 'm.png'), 1)
        with self.assertRaises(rv.PlacementError) as caught:
            rv.place_boxes(self.dir / 'm.png', found, [[(300, 290)]], [(400, 280)], tail_margin=12)
        self.assertIn('tail point', str(caught.exception))
        self.assertIn('(400, 280)', str(caught.exception))

    def test_results_without_targets_are_unchanged(self):
        found = rv.find_regions(save(frame(boxes=[(100, 100, 700, 260)]), self.dir, 'n.png'), 1)
        result = rv.place_boxes(self.dir / 'n.png', found, [[(300, 60)]])
        self.assertEqual(result['partial'], [False])
        self.assertEqual(result['painted'], [True])


def line_hits(p, q, rect, margin=0.0):
    """Independent brute force: does the segment p to q pass within `margin` px of a rectangle (sampled every pixel)?"""
    steps = int(max(abs(q[0] - p[0]), abs(q[1] - p[1]))) + 1
    for k in range(steps + 1):
        x, y = p[0] + (q[0] - p[0]) * k / steps, p[1] + (q[1] - p[1]) * k / steps
        if rect[0] - margin <= x <= rect[2] + margin and rect[1] - margin <= y <= rect[3] + margin:
            return True
    return False


def reads_after(first, second):
    """Independent statement of the reading-order rule, by tops: `second` (a later chunk) is to the right of `first`
    when their tops are within half of the shorter box's height, and otherwise starts lower than it."""
    if abs(second[1] - first[1]) <= .5 * min(first[3] - first[1], second[3] - second[1]):
        return (second[0] + second[2]) / 2 > (first[0] + first[2]) / 2
    return second[1] > first[1]


class TailCrossTests(Tmp):
    """A speech balloon's tail never runs through another balloon, and no balloon sits across another's tail."""

    SCALE = .3                       # points per source pixel, as a drawn panel has it
    R = (.45, .4)                    # a balloon's corner ratio and its minimum
    BOUNDS = [0, 0, 1200, 600]

    def quiet(self, name='q.png'):
        path = save(quiet_frame(busy=()), self.dir, name)
        return rv.find_regions(path, 2), path

    def painted(self, boxes, name='p.png'):
        path = save(frame(boxes=boxes), self.dir, name)
        return rv.find_regions(path, len(boxes)), path

    def place(self, found, path, targets, options=None, rounded='balloons', **extra):
        options = options or [[(300, 100)], [(300, 100)]]
        rounded = [self.R] * len(options) if rounded == 'balloons' else rounded
        return rv.place_boxes(path, found, options, targets, rounded=rounded, scale=self.SCALE, tail_margin=12, **extra)

    def crossings(self, result, targets, scale=None):
        """(tail owner, other chunk) pairs where the wedge or the line from the box's centre to the mouth meets the other box."""
        boxes, hits = result['boxes'], []
        for i, target in enumerate(targets):
            if target is None:
                continue
            wedge = rv.tail_wedge(boxes[i], result['corner'][i], target, self.BOUNDS, scale or self.SCALE)
            (bx, by), (tx, ty), half, _ = wedge
            centre = ((boxes[i][0] + boxes[i][2]) / 2, (boxes[i][1] + boxes[i][3]) / 2)
            for j, other in enumerate(boxes):
                if j != i and (line_hits(centre, (tx, ty), other) or line_hits((bx, by), (tx, ty), other, half)):
                    hits.append((i, j))
        return hits

    def test_the_wedge_follows_the_compositors_tail(self):
        import compositor as c
        for scale in (.3, 1.0):
            for ratio in (.45, .4):
                for box in ([432, 100, 732, 200], [100, 300, 160, 340], [0, 0, 300, 100], [900, 480, 1200, 600]):
                    for target in ((600, 300), (600, 20), (50, 150), (900, 150), (200, 250), (900, 590), (0, 300),
                                   (600, 599), (1199, 10), (350, 150), (1000, 560)):
                        with self.subTest(scale=scale, ratio=ratio, box=box, target=target):
                            wedge = rv.tail_wedge(box, ratio, target, self.BOUNDS, scale)
                            x0, y0, x1, y1 = [v * scale for v in box]
                            clip = [v * scale for v in (0, 0, 1200, 600)]
                            try:
                                tail = c._drawn_shape('speech', [x0, y0, x1 - x0, y1 - y0], [v * scale for v in target],
                                                      clip, ratio)['tail']
                            except ValueError:
                                tail = None               # the mouth is inside the balloon
                            if tail is None:
                                self.assertIsNone(wedge)
                                continue
                            (ax, ay), (bx, by) = tail['base_pt']
                            (base_x, base_y), mouth, half, length = wedge
                            self.assertAlmostEqual(base_x * scale, (ax + bx) / 2, places=6)
                            self.assertAlmostEqual(base_y * scale, (ay + by) / 2, places=6)
                            self.assertAlmostEqual(half * scale, math.hypot(bx - ax, by - ay) / 2, places=6)
                            self.assertAlmostEqual(mouth[0] * scale, tail['target_pt'][0], places=6)
                            self.assertAlmostEqual(mouth[1] * scale, tail['target_pt'][1], places=6)
                            self.assertAlmostEqual(length * scale, tail['length_pt'], places=6)
                            tip = rv._tail_parts(wedge)[1]
                            self.assertAlmostEqual(tip[0] * scale, tail['tip_pt'][0], places=6)
                            self.assertAlmostEqual(tip[1] * scale, tail['tip_pt'][1], places=6)

    def test_a_tail_path_meets_a_rectangle_only_where_the_wedge_or_the_line_on_from_it_does(self):
        level = ((0, 0), (100, 0), 5, 40)                       # base, mouth, half the base's width, the wedge's length
        self.assertTrue(rv.tail_crosses(level, [20, -1, 30, 1]))          # inside the wedge
        self.assertTrue(rv.tail_crosses(level, [20, 1, 30, 30]))          # the wedge is 5 either side of its centre at the base,
        self.assertFalse(rv.tail_crosses(level, [20, 4, 30, 30]))         # ...and 2.5 at the half way: it tapers
        self.assertTrue(rv.tail_crosses(level, [60, -2, 80, 2]))          # the line on from the tip to the mouth
        self.assertFalse(rv.tail_crosses(level, [60, 1, 80, 30]))         # which has no width
        self.assertFalse(rv.tail_crosses(level, [101, -2, 120, 2]))       # past the mouth
        self.assertFalse(rv.tail_crosses(level, [-30, -2, -1, 2]))        # behind the base
        slanted = ((0, 0), (100, 100), 5, 40)
        self.assertTrue(rv.tail_crosses(slanted, [70, 65, 80, 75]))       # on the line, past the tip
        self.assertFalse(rv.tail_crosses(slanted, [55, 70, 62, 80]))      # 5.7 px off it, past the tip
        self.assertFalse(rv.tail_crosses(slanted, [10, 25, 15, 30]))      # off the wedge near the base
        self.assertTrue(rv.tail_crosses(((0, 0), (0, -100), 5, 40), [-3, -60, 3, -50]))

    def test_a_tail_path_meets_a_face_zone_by_the_same_path(self):
        level = ((0, 0), (100, 0), 5, 40)
        self.assertTrue(rv.tail_meets_face(level, (50, 10, 12, 'near')))      # within the radius of the line past the tip
        self.assertFalse(rv.tail_meets_face(level, (50, 14, 12, 'beside')))
        self.assertTrue(rv.tail_meets_face(level, (10, 12, 10, 'wedge')))     # grazes the wedge near its base, 5 wide there
        self.assertFalse(rv.tail_meets_face(level, (30, 20, 10, 'clear')))    # the wedge is thin by now
        self.assertTrue(rv.tail_meets_face(level, (100, 0, 3, 'mouth')))      # a zone round the mouth: the speaker's own
        self.assertFalse(rv.tail_meets_face(level, (130, 0, 20, 'past')))
        self.assertTrue(rv.tail_meets_face(level, (10, 0, 2, 'inside')))

    def test_a_tail_that_would_run_through_the_other_balloon_is_placed_clear_of_it(self):
        found, path = self.quiet()
        targets = [(600, 300), (200, 70)]
        legacy = rv.place_boxes(path, found, [[(300, 100)], [(300, 100)]], targets)
        self.assertEqual(legacy['boxes'][0], [432, 0, 732, 100])
        self.assertEqual(self.crossings(legacy | {'corner': [.45, .45]}, targets), [(1, 0)])   # the old placement
        result = self.place(found, path, targets)
        self.assertEqual(self.crossings(result, targets), [])
        self.assertTrue(separate(*result['boxes']))
        for box in result['boxes']:
            self.assertTrue(box[0] >= 0 and box[1] >= 0 and box[2] <= 1200 and box[3] <= 600)

    def test_a_balloon_is_not_placed_across_another_chunks_tail(self):
        found, path = self.quiet()
        targets = [(1190, 100), (300, 400)]
        legacy = rv.place_boxes(path, found, [[(300, 100)], [(300, 100)]], targets)
        self.assertEqual(self.crossings(legacy | {'corner': [.45, .45]}, targets), [(0, 1)])   # chunk 1 sat on chunk 0's tail
        result = self.place(found, path, targets)
        self.assertEqual(self.crossings(result, targets), [])
        self.assertTrue(separate(*result['boxes']))

    def test_a_tail_to_an_off_frame_speaker_runs_to_the_edge_and_is_kept_clear_too(self):
        found, path = self.quiet()
        targets = [(600, 300), (0, 70)]                                      # on the left edge: nobody is in the frame
        legacy = rv.place_boxes(path, found, [[(300, 100)], [(300, 100)]], targets)
        self.assertTrue(rv.on_frame_edge(targets[1], self.BOUNDS))
        self.assertEqual(self.crossings(legacy | {'corner': [.45, .45]}, targets), [(1, 0)])
        result = self.place(found, path, targets)
        self.assertEqual(self.crossings(result, targets), [])

    def test_painted_regions_are_kept_off_a_tail_path_too(self):
        # Chunk 1 is painted under chunk 0's box and its mouth is above it: the tail can only go through chunk 0.
        found, path = self.painted([(400, 40, 800, 140), (400, 200, 800, 300)])
        with self.assertRaises(rv.PlacementError) as caught:
            self.place(found, path, [(100, 90), (600, 10)], [[(300, 60)], [(300, 60)]])
        message = str(caught.exception)
        self.assertIn('chunk 1', message)
        self.assertIn("its tail would cross chunk 0's balloon", message)
        self.assertIn('size(s) tried', message)
        # A painted region ahead of the chunk is in the way as well: chunk 0's tail would run through chunk 1's balloon.
        with self.assertRaises(rv.PlacementError) as caught:
            self.place(found, path, [(600, 590), (100, 250)], [[(300, 60)], [(300, 60)]])
        self.assertIn("chunk 0: its tail would cross chunk 1's balloon", str(caught.exception))
        self.assertIn('painted region', str(caught.exception))

    def test_a_balloon_that_could_only_sit_across_another_tail_fails_naming_that_chunk(self):
        # Chunk 0 is painted at the top and its mouth is below it: its tail runs straight down the middle. Chunk 1 is a
        # wide balloon with no painted region; below chunk 0 it would lie across that tail (and above the mouth the
        # mouth's own keep-out stops it reaching the bottom), and beside it there is no room.
        path = save(frame(boxes=[(500, 30, 700, 100)]), self.dir, 'w.png')
        found = rv.find_regions(path, 1)
        targets = [(600, 420), None]
        with self.assertRaises(rv.PlacementError) as caught:
            self.place(found, path, targets, [[(200, 70)], [(1100, 150)]])
        message = str(caught.exception)
        self.assertIn('chunk 1', message)
        self.assertIn("its box would cross chunk 0's tail", message)
        self.assertEqual(len(rv.place_boxes(path, found, [[(200, 70)], [(1100, 150)]], targets)['boxes']), 2)   # no balloons: fine

    def test_captions_and_chunks_without_tails_are_unaffected(self):
        found, path = self.quiet()
        targets = [(600, 300), (200, 70)]
        legacy = rv.place_boxes(path, found, [[(300, 100)], [(300, 100)]], targets)
        captions = self.place(found, path, targets, rounded=[None, None])                  # rectangles draw no tail
        self.assertEqual(captions['boxes'], legacy['boxes'])
        # A caption keeps its place among balloons, and a balloon with no tail is placed as any box always was.
        mixed = self.place(found, path, [(600, 300), None], rounded=[None, self.R])
        self.assertEqual(mixed['boxes'], rv.place_boxes(path, found, [[(300, 100)], [(300, 100)]], [(600, 300), None])['boxes'])
        bare = rv.place_boxes(path, found, [[(300, 100)], [(300, 100)]], targets, rounded=[self.R, self.R])
        self.assertEqual(self.crossings(bare, targets, 1.0), [])                        # an omitted scale is one point per pixel


def gap(box, point):
    """Distance from a point to a box, 0 inside it."""
    return math.hypot(max(box[0] - point[0], 0, point[0] - box[2]), max(box[1] - point[1], 0, point[1] - box[3]))


class NearSpeakerTests(Tmp):
    """A balloon goes near its own speaker, its tail crosses no other face, and boxes read in script order."""

    R = (.45, .4)
    SCALE = .3
    BOUNDS = [0, 0, 1200, 600]
    DIAGONAL = math.hypot(1200, 600)
    A, B = (200, 520), (1000, 250)                        # two speakers, far apart
    FACES = [(200, 470, 70, 'A'), (1000, 200, 70, 'B')]    # a zone above each mouth

    def setUp(self):
        super().setUp()
        # A busy band on the left and the whole lower half: the quiet space is the top right, beside B.
        self.path = save(quiet_frame(), self.dir, 'q.png')
        self.found = rv.find_regions(self.path, 0)

    def place(self, targets, options=None, rounded=None, faces=None, found=None, path=None, **extra):
        options = options or [[(300, 100)]] * len(targets)
        return rv.place_boxes(path or self.path, found or self.found, options, targets, faces=self.FACES if faces is None else faces,
                              rounded=[self.R] * len(options) if rounded is None else rounded, scale=self.SCALE, tail_margin=12,
                              **extra)

    def length(self, result, i, target):
        (bx, by), (tx, ty), _, _ = rv.tail_wedge(result['boxes'][i], result['corner'][i], target, self.BOUNDS, self.SCALE)
        return math.hypot(tx - bx, ty - by)

    def test_a_balloon_goes_near_its_own_speaker_not_into_the_quietest_space(self):
        targets = [self.B, self.A]
        legacy = rv.place_boxes(self.path, self.found, [[(300, 100)], [(300, 100)]], targets, faces=self.FACES)
        self.assertEqual(legacy['boxes'], [[432, 0, 732, 100], [840, 0, 1140, 100]])   # both in the quiet top, beside B
        result = self.place(targets)
        first, second = result['boxes']
        self.assertLess(gap(first, self.B), 100)                                        # beside its own speaker
        self.assertLess(gap(second, self.A), 100)
        self.assertGreater(gap(legacy['boxes'][1], self.A), 400)                        # A's balloon used to be far across
        self.assertLess(self.length(result, 0, self.B), 100)
        self.assertLess(self.length(result, 1, self.A), 100)
        for i, target in enumerate(targets):                                            # and no tail crosses the other face
            wedge = rv.tail_wedge(result['boxes'][i], result['corner'][i], target, self.BOUNDS, self.SCALE)
            for face in self.FACES:
                if math.hypot(target[0] - face[0], target[1] - face[1]) > face[2]:
                    self.assertFalse(rv.tail_meets_face(wedge, face), (i, face[3]))

    def test_quietness_only_breaks_ties_between_positions_of_similar_tail_length(self):
        # The same chunk placed beside a speaker in the quiet top right and beside one in the busy lower left.
        quiet = self.place([self.B])['boxes'][0]
        busy = self.place([self.A])['boxes'][0]
        self.assertLess(gap(quiet, self.B), 100)
        self.assertLess(gap(busy, self.A), 100)
        # Deliberately changed: a speaker off frame is ranked by nearness to its edge point too (the tail shows where
        # the voice comes from), so the balloon no longer goes to the quiet top right when the voice is off the left edge.
        off = self.place([(0, 300)])['boxes'][0]
        self.assertLess(gap(off, (0, 300)), 150)

    def test_a_tail_never_enters_a_face_that_is_not_its_speakers_even_when_that_leaves_one_position(self):
        # The painted region is fixed at the left and the speaker is far to its right, with another face between.
        path = save(frame(boxes=[(100, 100, 400, 200)]), self.dir, 'f.png')
        found = rv.find_regions(path, 1)
        faces = [(900, 110, 70, 'A'), (650, 150, 50, 'C')]
        with self.assertRaises(rv.PlacementError) as caught:
            self.place([(900, 150)], [[(200, 60)]], faces=faces, found=found, path=path)
        message = str(caught.exception)
        self.assertIn('chunk 0', message)
        self.assertIn('its tail would cross a face (C)', message)
        # Without the face between them the same chunk is placed, and the speaker's own zone is never a problem.
        result = self.place([(900, 150)], [[(200, 60)]], faces=faces[:1], found=found, path=path)
        wedge = rv.tail_wedge(result['boxes'][0], result['corner'][0], (900, 150), self.BOUNDS, self.SCALE)
        self.assertTrue(rv.tail_meets_face(wedge, faces[0]))                           # it ends in its own speaker's zone

    def test_the_path_to_a_speaker_behind_another_face_is_rejected_and_other_wraps_are_tried(self):
        # B's face sits right above A's mouth. A wide balloon can only go along the top, and its tail would cross B's face.
        faces = [(600, 535, 30, 'A'), (600, 400, 80, 'B')]
        target = (600, 560)
        with self.assertRaises(rv.PlacementError) as caught:
            self.place([target], [[(1100, 120)]], faces=faces)
        self.assertIn('chunk 0: its tail would cross a face (B)', str(caught.exception))
        result = self.place([target], [[(1100, 120), (300, 100)]], faces=faces)       # a narrower wrap finds room beside them
        self.assertEqual(result['choice'], [1])
        wedge = rv.tail_wedge(result['boxes'][0], result['corner'][0], target, self.BOUNDS, self.SCALE)
        self.assertFalse(rv.tail_meets_face(wedge, faces[1]))

    def test_off_frame_speakers_go_near_their_edge_point_and_two_voices_keep_to_their_own_sides(self):
        # Two voices off the top edge, the first at the left and the second at the right (a real panel: "the first
        # balloon upper left, the second lower right"); ranked by quietness the first went right and the second's tail
        # then had to cross it, so the panel could not be placed at all.
        left, right = (150, 0), (1050, 0)
        result = self.place([left, right])
        first, second = result['boxes']
        self.assertLess((first[0] + first[2]) / 2, 600)
        self.assertGreater((second[0] + second[2]) / 2, 600)
        for i, target in enumerate((left, right)):
            wedge = rv.tail_wedge(result['boxes'][i], result['corner'][i], target, self.BOUNDS, self.SCALE)
            self.assertFalse(rv.tail_crosses(wedge, result['boxes'][1 - i]))

    def test_off_frame_speakers_are_exempt_from_the_face_rule_and_captions_from_proximity(self):
        edge = (0, 300)                                              # the speaker is off frame on the left edge
        near = self.place([edge], faces=[(150, 300, 60, 'X')])['boxes'][0]       # a face between the edge and the balloon
        self.assertIsNotNone(near)                                   # is not a speaker's face to protect from its tail
        caption = rv.place_boxes(self.path, self.found, [[(300, 100)]], [self.A], faces=self.FACES)
        self.assertEqual(self.place([self.A], rounded=[None])['boxes'], caption['boxes'])

    def test_a_tail_within_the_limit_is_always_preferred(self):
        path = save(frame(boxes=[(80, 10, 1150, 400)]), self.dir, 'c3.png')
        found = rv.find_regions(path, 1)
        result = self.place([None, (20, 20)], [[(1000, 300)], [(300, 60)]], rounded=[None, self.R], faces=[], found=found, path=path)
        self.assertLessEqual(self.length(result, 1, (20, 20)), rv.TAIL_MAX_SHARE * self.DIAGONAL)

    def test_a_tail_longer_than_the_limit_is_taken_only_when_nothing_shorter_is_valid(self):
        # A big painted caption leaves only a strip at the bottom: every window is farther from the mouth than the limit.
        path = save(frame(boxes=[(80, 10, 1150, 490)]), self.dir, 'c.png')
        found = rv.find_regions(path, 1)
        mouth = (20, 20)
        result = self.place([None, mouth], [[(1000, 300)], [(300, 60)]], rounded=[None, self.R], faces=[], found=found, path=path)
        box = result['boxes'][1]
        chosen = self.length(result, 1, mouth)
        self.assertGreater(chosen, rv.TAIL_MAX_SHARE * self.DIAGONAL)
        best = min(math.hypot(tx - bx, ty - by) for x0 in range(0, 901, 2) for y0 in range(502, 541, 2)
                   for (bx, by), (tx, ty), _, _ in [rv.tail_wedge([x0, y0, x0 + 300, y0 + 60], .45, mouth, self.BOUNDS, self.SCALE)])
        self.assertLessEqual(chosen, best + 10)                                          # the shortest, to within the search step
        self.assertEqual(box[1], 504)

    def test_a_later_box_that_starts_higher_on_another_line_reads_first(self):
        # A real chapter 3 panel: the second line's balloon sat above the first's, overlapping it by a few pixels, so it
        # was not "entirely above" and passed, yet readers took it first. Off a shared line, the later box must start lower.
        first, second = [300, 657, 700, 740], [0, 578, 280, 662]
        self.assertFalse(rv._reads_after(first, second))
        self.assertTrue(rv._reads_after(second, first))
        self.assertFalse(rv._reads_after([0, 100, 200, 200], [300, 0, 500, 90]))           # entirely above, as before
        self.assertTrue(rv._reads_after([0, 100, 200, 200], [300, 110, 500, 190]))         # same line, to the right
        self.assertFalse(rv._reads_after([300, 100, 500, 200], [0, 110, 200, 190]))        # same line, to the left
        self.assertTrue(rv._reads_after([300, 100, 500, 200], [0, 260, 200, 330]))         # the next line down, anywhere

    def test_a_tall_later_box_beside_a_short_one_reads_first_when_its_top_is_higher(self):
        # Real panels: a tall second balloon beside a short first one overlapped its whole height, so it counted as the
        # same line and passed for being to the right, yet its top sat far higher and readers took it first.
        short, tall = [0, 300, 200, 350], [300, 100, 500, 400]
        self.assertFalse(rv._reads_after(short, tall))
        # The reverse, a short later box at the left inside the tall box's band, is no longer allowed either: readers
        # disagree on it (chapter 3 r6, 6.1), so a later box at the left must start below the earlier box.
        self.assertFalse(rv._reads_after(tall, short))
        self.assertTrue(rv._reads_after(tall, [0, 395, 200, 445]))                         # below it (10 percent grace)
        self.assertTrue(rv._reads_after([0, 90, 300, 300], [350, 100, 500, 150]))          # tops level: to the right reads after
        self.assertFalse(rv._reads_after([350, 100, 500, 150], [0, 90, 300, 300]))         # tops level: to the left reads first
        self.assertTrue(rv._reads_after([600, 100, 800, 150], [0, 200, 200, 250]))         # clearly lower reads after, anywhere

    def test_a_box_beside_an_earlier_one_reads_left_to_right_and_a_higher_one_reads_first(self):
        # Chapter 3 r4, as lettered (frame pixels), all read out of script order by the review.
        # 6.3: the second caption starts 49 px lower but inside the upper part of the first, beside it on the left: level.
        self.assertFalse(rv._reads_after([952, 507, 1523, 646], [624, 556, 939, 653]))
        self.assertTrue(rv._reads_after([624, 556, 939, 653], [952, 540, 1523, 646]))     # nearly level, to the right
        # 10.3: "Forgive me." at the far left starts 66 px below two captions, within their upper part: read before them.
        self.assertFalse(rv._reads_after([1728, 104, 2164, 234], [330, 170, 643, 346]))
        self.assertFalse(rv._reads_after([930, 104, 1712, 224], [330, 170, 643, 346]))
        # 3.5: two tall balloons, the later one starting 112 px higher on the right: read first, not level.
        self.assertFalse(rv._reads_after([84, 272, 711, 500], [1148, 160, 1521, 388]))
        # A later box to the RIGHT that starts lower reads after, even where the two overlap in height.
        self.assertTrue(rv._reads_after([0, 100, 300, 200], [400, 150, 700, 250]))
        # Chapter 1 r10, 1.5: two equal captions, the second starting 55 px (61 percent of a box) lower on the left;
        # readers took the left one first. Beside is judged against the shorter box, so this is level and out of order.
        self.assertFalse(rv._reads_after([1094, 360, 1618, 450], [379, 415, 885, 505]))
        # Chapter 3 r6, placed at the edge of the earlier thresholds and read out of order by the review:
        # 6.1, "Quickly." at the left starting two thirds of a box lower, inside the band of the balloon before it;
        self.assertFalse(rv._reads_after([1088, 91, 1295, 233], [418, 186, 640, 340]))
        # 3.5, "And if there is no such thing?" starting 84 px higher on the right, 37 percent of the boxes' height.
        self.assertFalse(rv._reads_after([84, 272, 710, 500], [1176, 188, 1518, 416]))

    def test_the_fallback_reads_a_short_later_box_inside_a_tall_earlier_ones_band_left_to_right(self):
        # Chapter 2 r2, 5.3: no strict order fitted, and the fallback put Nagoji's one-line reply at the left, 135 px
        # below the top of Keshavrao's three-line balloon but inside its band, so readers took the reply first. Tops
        # alone cannot see that a short box sits inside a tall one's band; the share of the short box inside it can.
        tall, short = [1150, 1000, 1480, 1220], [700, 1135, 1000, 1245]
        self.assertFalse(rv._reads_after(tall, short, strict=False))
        self.assertFalse(rv._reads_after(tall, short))                                     # the strict rule already refused it
        self.assertTrue(rv._reads_after([700, 1000, 1000, 1220], [1150, 1135, 1480, 1245], strict=False))   # to the right
        self.assertTrue(rv._reads_after(tall, [700, 1170, 1000, 1280], strict=False))      # mostly below the band: as before
        self.assertTrue(rv._reads_after([0, 100, 300, 200], [400, 160, 700, 260], strict=False))
        self.assertFalse(rv._reads_after([400, 100, 700, 200], [0, 160, 300, 260], strict=False))   # equal heights: as before

    def test_boxes_read_in_script_order(self):
        # Chunk 0's speaker is on the right and chunk 1's on the left, on the same line. Each balloon beside its own
        # speaker would put chunk 1 left of chunk 0, out of order; chunk 1 goes lower instead, still on its speaker's side.
        right, left = (1000, 250), (200, 250)
        faces = [(1000, 200, 60, 'R'), (200, 200, 60, 'L')]
        result = self.place([right, left], faces=faces)
        first, second = result['boxes']
        alone = self.place([left], faces=faces)['boxes'][0]                               # chunk 1 with nothing before it
        self.assertFalse(reads_after(first, alone))                                        # there it would read first
        self.assertTrue(reads_after(first, second))
        self.assertGreater(second[1], alone[1])                                            # so it is lower
        self.assertLess((second[0] + second[2]) / 2, (first[0] + first[2]) / 2)            # on its speaker's side
        self.assertLess(gap(second, left), 120)
        free = rv.place_boxes(self.path, self.found, [[(300, 100)], [(300, 100)]], [right, left], faces=faces)
        self.assertTrue(reads_after(free['boxes'][0], free['boxes'][1]))                  # boxes without tails read in order too

    def test_captions_that_the_greedy_order_strands_are_placed_by_preferring_the_top(self):
        # Chapter 1 9.4: four captions over a close-up. The top of the frame was busy stone and the bottom a smooth
        # blanket, so the first caption took the bottom left, the second the bottom right, and the third had nowhere
        # left that reads after them. A retry that prefers the top more strongly places all four, in order.
        rng = np.random.default_rng(11)
        array = painted_background((1200, 600)).copy()
        array[:260] = rng.integers(0, 175, (260, 1200, 3))              # busy texture across the top
        array[510:] = (70, 60, 50)                                       # a smooth band at the bottom, one caption deep
        path = save(Image.fromarray(array), self.dir, 'stranded.png')
        found = rv.find_regions(path, 4)
        face = [(600, 330, 120, 'face')]
        result = rv.place_boxes(path, found, [[(320, 70)]] * 4, [None] * 4, faces=face)
        boxes = result['boxes']
        for i in range(4):
            for j in range(i):
                self.assertTrue(rv._reads_after(boxes[j], boxes[i]), (j, i, boxes))
        self.assertLess(boxes[0][3], 510)                                # the first caption no longer takes the bottom band
        unchanged = rv.place_boxes(path, found, [[(320, 70)]], [None], faces=face)['boxes'][0]
        self.assertGreater(unchanged[1], 500)                            # a single caption still takes the quiet bottom

    def test_a_box_that_could_only_go_above_an_earlier_one_fails_naming_both_chunks(self):
        path = save(frame(boxes=[(300, 450, 700, 550)]), self.dir, 'o.png')
        found = rv.find_regions(path, 1)
        with self.assertRaises(rv.PlacementError) as caught:
            rv.place_boxes(path, found, [[(300, 100)], [(1100, 280)]], [None, None])
        message = str(caught.exception)
        self.assertIn('chunk 1', message)
        self.assertIn("its box would read before chunk 0's", message)
        self.assertIn('script order', message)

    def test_the_fallback_gives_up_nearness_only_for_the_chunks_that_need_it(self):
        # On a real panel one balloon could not be placed near its speaker, and the all-or-nothing fallback then moved
        # every balloon, including an off-frame voice that had been placed beside its edge, across the frame.
        found = {'visible_rect': [0, 0, 1200, 600], 'regions': []}
        targets = [(0, 100), (600, 300), (600, 300)]

        def run(fails):
            calls = []

            def fake(image_path, found, options, targets, near, **kwargs):
                flags = list(near) if isinstance(near, (list, tuple)) else [near] * len(options)
                calls.append(flags)
                if fails(flags):
                    raise rv.PlacementError('chunk 2: no room', chunk=2)
                return {'near': flags}

            with mock.patch.object(rv, '_place_boxes', fake):
                result = rv.place_boxes('x.png', found, [[(100, 50)]] * 3, targets, rounded=[self.R] * 3)
            return result['near'], calls

        # Only the failing chunk gives up nearness; chunks 0 and 1 keep theirs.
        near, calls = run(lambda flags: flags[2])
        self.assertEqual(near, [True, True, False])
        self.assertEqual(calls, [[True, True, True], [True, True, False]])
        # When an earlier chunk's nearness is what leaves no room, one earlier chunk at a time gives it up, the nearest first.
        near, calls = run(lambda flags: flags[0] or flags[2])
        self.assertEqual(near, [False, True, False])
        self.assertEqual(calls, [[True, True, True], [True, True, False], [True, False, False], [False, True, False]])
        # Only when no such choice works is every chunk placed by quietness, as before.
        near, calls = run(lambda flags: (flags[0] or flags[1] or flags[2]))
        self.assertEqual(near, [False, False, False])
        self.assertEqual(calls[-1], [False, False, False])

    def test_when_the_nearest_position_leaves_a_later_chunk_no_room_the_placement_falls_back_to_quietness(self):
        # A tall caption (chunk 1) must read after the balloon (chunk 0). Beside its speaker the balloon leaves no room
        # for it, below or beside (it would read first or overlap the line); at the quiet top it does.
        mouth = (900, 400)
        result = self.place([mouth, None], [[(300, 100)], [(400, 450)]], rounded=[self.R, None], faces=[])
        first, second = result['boxes']
        self.assertTrue(reads_after(first, second))
        self.assertLess(first[1], 60)                                   # the quiet top: far from its speaker
        self.assertGreater(gap(first, mouth), 200)
        self.assertEqual(result['choice'], [0, 0])
        # Where even that fails, there is no placement and the chunk is named.
        with self.assertRaises(rv.PlacementError) as caught:
            self.place([mouth, None], [[(300, 100)], [(400, 560)]], rounded=[self.R, None], faces=[])
        self.assertIn('chunk 1', str(caught.exception))
        # A chunk that is placed near its speaker the first time is never moved by the fallback.
        near = self.place([mouth, None], [[(300, 100)], [(200, 100)]], rounded=[self.R, None], faces=[])
        self.assertLess(gap(near['boxes'][0], mouth), 100)
        # A speaker who is off frame, or a caption, has nothing to be near, so there is no second pass to make.
        with self.assertRaises(rv.PlacementError):
            self.place([(0, 300), None], [[(300, 100)], [(1100, 590)]], rounded=[self.R, None], faces=[])

    def test_the_tail_length_helper_matches_the_wedge(self):
        import numpy as np
        rng = np.random.default_rng(3)
        for _ in range(200):
            w, h = int(rng.integers(120, 500)), int(rng.integers(60, 200))
            x0, y0 = int(rng.integers(0, 1200 - w)), int(rng.integers(0, 600 - h))
            target = (float(rng.integers(0, 1200)), float(rng.integers(0, 600)))
            wedge = rv.tail_wedge([x0, y0, x0 + w, y0 + h], .45, target, self.BOUNDS, self.SCALE)
            if wedge is None:
                continue
            (bx, by), (tx, ty), _, _ = wedge
            got = rv._tail_lengths(np.array([[x0]]), np.array([[y0]]), w, h, .45, target, self.BOUNDS, self.SCALE)
            self.assertAlmostEqual(float(got[0, 0]), math.hypot(tx - bx, ty - by), places=6)


def tip_of(wedge):
    """The tip of a drawn tail, stated afresh from tail_wedge: its length along the line from the base to the mouth."""
    (bx, by), (tx, ty), _, length = wedge
    distance = math.hypot(tx - bx, ty - by)
    return bx + (tx - bx) * length / distance, by + (ty - by) * length / distance


class OffFrameVoiceFaceTests(Tmp):
    """An off-frame voice's tail, which now runs to the frame's edge, never crosses a face: none of them is its speaker's.

    Chapter 6 r1, 4.5: Nagoji's off-panel line had a long tail from its balloon to the left edge, straight across
    Varma's eyes; only tails to on-frame speakers were checked against the faces they pass.
    """

    R = (.45, .4)
    SCALE = .3
    BOUNDS = [0, 0, 1200, 600]
    EDGE = (0, 300)                                     # the voice is off the left edge
    FACE = (400, 300, 60, 'K')                          # a face between the edge and the balloon's painted region

    def setUp(self):
        super().setUp()
        self.path = save(frame(boxes=[(800, 250, 1100, 350)]), self.dir, 'v.png')    # holds the balloon at the right
        self.found = rv.find_regions(self.path, 1)

    def place(self, faces):
        return rv.place_boxes(self.path, self.found, [[(320, 120)]], [self.EDGE], faces=faces, scale=self.SCALE,
                              tail_margin=12, rounded=[self.R])

    def test_the_tail_to_an_off_frame_voice_may_not_cross_any_face(self):
        free = self.place([])                                                        # the face is not protected:
        wedge = rv.tail_wedge(free['boxes'][0], free['corner'][0], self.EDGE, self.BOUNDS, self.SCALE)
        self.assertTrue(rv.tail_meets_face(wedge, self.FACE))                         # the tail runs through it
        with self.assertRaises(rv.PlacementError) as caught:
            self.place([self.FACE])
        self.assertIn('chunk 0: its tail would cross a face (K)', str(caught.exception))


class TailTipTests(Tmp):
    """A reader credits a balloon to whoever its drawn tail's tip lands nearest, so the tip never lands nearer another face."""

    R = (.45, .4)
    SCALE = .3
    BOUNDS = [0, 0, 1200, 600]
    MOUTH = (660, 250)                                        # Nagoji speaks; Duarte stands on the same line, to his left
    FACES = [(660, 200, 50, 'Nagoji'), (380, 250, 40, 'Duarte')]

    def setUp(self):
        super().setUp()
        self.path = save(frame(boxes=[(150, 50, 300, 120)]), self.dir, 'p.png')          # a balloon painted at the top left
        self.found = rv.find_regions(self.path, 1)

    def place(self, options=None, targets=None, faces=None, rounded=None, **extra):
        options = options or [[(300, 100)]]
        return rv.place_boxes(self.path, self.found, options, [self.MOUTH] if targets is None else targets,
                              faces=self.FACES if faces is None else faces, scale=self.SCALE, tail_margin=12,
                              rounded=[self.R] * len(options) if rounded is None else rounded, **extra)

    def lifted(self, *args, **kwargs):
        """The same placement with the tip rule lifted: what the planner did before it."""
        with mock.patch.object(rv, 'RULES', tuple(kind for kind in rv.RULES if kind != 'tip')):
            return self.place(*args, **kwargs)

    def tip_gaps(self, result, faces=None, target=None):
        """Distance from the drawn tail's tip to each face zone's edge (0 inside), by name."""
        wedge = rv.tail_wedge(result['boxes'][0], result['corner'][0], target or self.MOUTH, self.BOUNDS, self.SCALE)
        tip = tip_of(wedge)
        return {f[3]: max(0.0, math.hypot(tip[0] - f[0], tip[1] - f[1]) - f[2]) for f in faces or self.FACES}

    def test_the_rule_is_one_more_placement_rule(self):
        self.assertIn('tip', rv.RULES)
        self.assertEqual(rv.RULES[-1], 'order')

    def test_a_tail_that_would_end_at_another_mans_collar_is_not_placed_there(self):
        old = self.lifted()
        gaps = self.tip_gaps(old)
        self.assertLess(gaps['Duarte'], gaps['Nagoji'])              # before: the short tail's tip stopped at Duarte
        result = self.place()
        gaps = self.tip_gaps(result)
        self.assertLessEqual(gaps['Nagoji'], gaps['Duarte'])         # now it ends nearer its own speaker
        box, bbox = result['boxes'][0], self.found['regions'][0]['bbox']
        self.assertTrue(box[0] <= bbox[0] and box[1] <= bbox[1] and box[2] >= bbox[2] and box[3] >= bbox[3])   # still covers it
        self.assertGreater(box[0], old['boxes'][0][0])               # it slid toward its speaker
        self.assertEqual(result['choice'], [0])

    def test_narrower_wraps_are_tried_before_the_chunk_fails(self):
        sizes = [[(150, 60), (300, 100)]]                             # the first is as small as the painted region: no room to slide
        self.assertEqual(self.lifted(sizes)['choice'], [0])
        result = self.place(sizes)
        self.assertEqual(result['choice'], [1])
        gaps = self.tip_gaps(result)
        self.assertLessEqual(gaps['Nagoji'], gaps['Duarte'])

    def test_a_chunk_no_position_can_place_fails_naming_the_chunk_and_the_face(self):
        self.assertEqual(len(self.lifted([[(150, 60)]])['boxes']), 1)    # it was placed, its tip at Duarte
        with self.assertRaises(rv.PlacementError) as caught:
            self.place([[(150, 60)]])
        message = str(caught.exception)
        self.assertEqual(caught.exception.chunk, 0)
        self.assertIn('chunk 0', message)
        self.assertIn('tail tip', message)
        self.assertIn('Duarte', message)
        self.assertIn('size(s) tried', message)
        self.assertNotIn('cross', message)

    def test_a_tip_that_reaches_the_speakers_own_face_first_is_accepted(self):
        faces = self.FACES[:1]                                        # nobody else to point at
        self.assertEqual(self.place(faces=faces)['boxes'], self.lifted(faces=faces)['boxes'])
        near = [(660, 200, 50, 'Nagoji'), (600, 160, 60, 'hat')]      # a zone that overlaps his own is his, not another man's
        placed = self.place(faces=near)
        self.assertEqual(placed['boxes'], self.lifted(faces=near)['boxes'])
        self.assertLess(self.tip_gaps(placed, near)['hat'], self.tip_gaps(placed, near)['Nagoji'])
        held = [(330, 200, 50, 'Nagoji'), (380, 250, 40, 'Duarte')]   # the mouth inside both zones: both are the speaker's
        self.assertEqual(self.place(targets=[(360, 240)], faces=held)['boxes'],
                         self.lifted(targets=[(360, 240)], faces=held)['boxes'])

    def test_captions_and_off_frame_voices_are_not_held_to_it(self):
        caption = self.place(rounded=[None])
        self.assertEqual(caption['boxes'], self.lifted(rounded=[None])['boxes'])
        off = (600, 0)                                                # a voice off the top edge has no face in the frame
        self.assertEqual(self.place(targets=[off])['boxes'], self.lifted(targets=[off])['boxes'])
        self.assertEqual(self.place(targets=[None])['boxes'], self.lifted(targets=[None])['boxes'])

    def test_without_faces_nothing_changes(self):
        self.assertEqual(self.place(faces=[])['boxes'], self.lifted(faces=[])['boxes'])


class OffFrameWedgeTests(unittest.TestCase):
    def test_a_wedge_to_an_off_frame_speaker_reaches_the_frame_edge(self):
        import math
        bounds = [0, 0, 1200, 600]
        (bx, by), (tx, ty), _, length = rv.tail_wedge([100, 200, 400, 300], .45, (1200, 250), bounds, .3)
        self.assertAlmostEqual(length, math.hypot(tx - bx, ty - by), places=6)      # all the way to the edge point
        (bx, by), (tx, ty), _, length = rv.tail_wedge([100, 200, 400, 300], .45, (900, 250), bounds, .3)
        self.assertLess(length, math.hypot(tx - bx, ty - by) * .95)                  # a mouth inside: stops short


class OffFrameTailTests(Tmp):
    """A voice from off frame keeps room between its balloon and that edge for a tail, unless nothing else fits."""

    R = (.45, .4)
    SCALE = .3
    BOUNDS = [0, 0, 1200, 600]
    ROOM = (8.0 + .8) / .3                                            # the tail's shortest length plus the stroke, in pixels

    def setUp(self):
        super().setUp()
        self.path = save(quiet_frame(busy=()), self.dir, 'q.png')
        self.found = rv.find_regions(self.path, 0)

    def place(self, targets, options=None, rounded=None, found=None, path=None, **extra):
        options = options or [[(300, 100)]] * len(targets)
        return rv.place_boxes(path or self.path, found or self.found, options, targets, scale=self.SCALE, tail_margin=12,
                              rounded=[self.R] * len(options) if rounded is None else rounded, **extra)

    def drawn(self, result, i, target):
        """The compositor's own tail for chunk i at the placed size: None when it draws none."""
        import compositor as c
        x0, y0, x1, y1 = [v * self.SCALE for v in result['boxes'][i]]
        clip = [v * self.SCALE for v in self.BOUNDS]
        return c._drawn_shape('speech', [x0, y0, x1 - x0, y1 - y0], [v * self.SCALE for v in target], clip,
                              result['corner'][i])['tail']

    @staticmethod
    def room(box, edge):
        """How far a box is from the frame's left, top, right or bottom edge."""
        return {'left': box[0], 'top': box[1], 'right': 1200 - box[2], 'bottom': 600 - box[3]}[edge]

    def test_the_room_is_the_compositors_shortest_tail_plus_its_stroke(self):
        import compositor as c
        self.assertEqual(rv.WEDGE_MIN_PT, c.TAIL_MIN_PT)
        self.assertEqual(rv.WEDGE_STROKE_PT, c.DRAW_STROKE_PT)

    def test_a_voice_off_any_edge_gets_a_box_clear_of_it_and_a_tail_the_compositor_draws(self):
        for edge, target in (('top', (600, 0)), ('bottom', (600, 600)), ('left', (0, 300)), ('right', (1200, 300))):
            with self.subTest(edge=edge):
                result = self.place([target])
                self.assertGreaterEqual(self.room(result['boxes'][0], edge), self.ROOM)
                self.assertIsNotNone(rv.tail_wedge(result['boxes'][0], result['corner'][0], target, self.BOUNDS, self.SCALE))
                tail = self.drawn(result, 0, target)
                self.assertIsNotNone(tail)
                self.assertGreater(tail['length_pt'], 4.0)
                self.assertEqual(result['edge_voice_no_tail'], [])

    def test_the_balloon_still_goes_near_its_edge_point_and_the_room_holds_without_a_scale_too(self):
        near = self.place([(150, 0)])['boxes'][0]
        self.assertLess(near[0], 300)                                 # beside its own point on the edge, not across the frame
        self.assertLess(near[1], 80)
        bare = rv.place_boxes(self.path, self.found, [[(300, 100)]], [(600, 0)], rounded=[self.R])   # one point per pixel
        self.assertGreaterEqual(bare['boxes'][0][1], 8.8)

    def test_two_voices_off_the_top_edge_both_keep_clear_of_it(self):
        result = self.place([(150, 0), (1050, 0)])
        for box in result['boxes']:
            self.assertGreaterEqual(box[1], self.ROOM)
        self.assertEqual(result['edge_voice_no_tail'], [])
        for i, target in enumerate(((150, 0), (1050, 0))):
            self.assertIsNotNone(self.drawn(result, i, target))

    def test_when_there_is_no_room_the_balloon_touches_the_edge_and_is_reported(self):
        target = (600, 0)
        result = self.place([target], [[(300, 590)]])                  # taller than the frame leaves room for
        self.assertEqual(result['boxes'][0][1], 0)
        self.assertEqual(result['edge_voice_no_tail'], [0])
        # A chunk that did find room is not reported beside one that did not.
        both = self.place([(150, 0), (900, 0)], [[(300, 100)], [(300, 590)]])
        self.assertEqual(both['edge_voice_no_tail'], [1])
        self.assertGreaterEqual(both['boxes'][0][1], self.ROOM)

    def test_a_balloon_over_a_painted_region_against_the_border_keeps_its_place_and_is_reported(self):
        path = save(frame(boxes=[(400, 6, 700, 84)]), self.dir, 'edge.png')
        found = rv.find_regions(path, 1)
        result = self.place([(550, 0)], [[(300, 60)]], found=found, path=path)
        self.assertEqual(result['boxes'][0][1], 0)                     # it must hide the painted balloon, which is on the border
        self.assertEqual(result['edge_voice_no_tail'], [0])

    def test_speakers_in_the_frame_and_captions_are_never_reported_and_keep_their_places(self):
        inside = self.place([(600, 300)])
        self.assertEqual(inside['edge_voice_no_tail'], [])
        self.assertEqual(self.place([(600, 300)], rounded=[None])['boxes'], rv.place_boxes(self.path, self.found, [[(300, 100)]], [(600, 300)])['boxes'])
        caption = self.place([None], rounded=[None])
        self.assertEqual(caption['boxes'], rv.place_boxes(self.path, self.found, [[(300, 100)]])['boxes'])
        self.assertEqual(caption['edge_voice_no_tail'], [])
        self.assertEqual(rv.place_boxes(self.path, self.found, [[(300, 100)]], [(600, 0)])['edge_voice_no_tail'], [])   # no balloons


class KeepAvoidTests(Tmp):
    """Keep zones (story-critical art) are soft obstacles: avoided when a place exists, covered and reported when none does."""

    def setUp(self):
        super().setUp()
        self.path = save(quiet_frame(), self.dir, 'q.png')             # busy left band and lower half: the quiet spot is the top right
        self.found = rv.find_regions(self.path, 0)
        self.legacy = rv.place_boxes(self.path, self.found, [[(300, 100)]])['boxes'][0]

    @staticmethod
    def share(box, zone):
        """Independent statement: the part of the keep zone the box covers."""
        ix = max(0, min(box[2], zone[2]) - max(box[0], zone[0]))
        iy = max(0, min(box[3], zone[3]) - max(box[1], zone[1]))
        return ix * iy / ((zone[2] - zone[0]) * (zone[3] - zone[1]))

    def test_a_caption_whose_quietest_spot_covers_a_keep_zone_goes_elsewhere(self):
        zone = [self.legacy[0] + 40, self.legacy[1], self.legacy[2] - 40, self.legacy[3] + 100]    # the torsos under the quiet spot
        self.assertGreater(self.share(self.legacy, zone), .3)
        result = rv.place_boxes(self.path, self.found, [[(300, 100)]], keep=[zone])
        self.assertNotEqual(result['boxes'][0], self.legacy)
        self.assertLess(self.share(result['boxes'][0], zone), rv.KEEP_OVERLAP_MAX)
        self.assertEqual(result['keep_overlaps'], {})
        x0, y0, x1, y1 = result['boxes'][0]
        self.assertTrue(x0 >= 0 and y0 >= 0 and x1 <= 1200 and y1 <= 600)

    def test_a_small_overlap_is_allowed_and_a_larger_one_is_not(self):
        x, y = self.legacy[2] - 20, self.legacy[3] - 20
        small = [x, y, x + 100, y + 100]                               # 20 x 20 px of a 100 x 100 zone: 4 percent
        result = rv.place_boxes(self.path, self.found, [[(300, 100)]], keep=[small])
        self.assertEqual(result['boxes'][0], self.legacy)
        self.assertEqual(result['keep_overlaps'], {})
        x, y = self.legacy[2] - 40, self.legacy[3] - 40
        large = [x, y, x + 100, y + 100]                               # 16 percent
        moved = rv.place_boxes(self.path, self.found, [[(300, 100)]], keep=[large])
        self.assertNotEqual(moved['boxes'][0], self.legacy)
        self.assertLess(self.share(moved['boxes'][0], large), rv.KEEP_OVERLAP_MAX)
        self.assertEqual(rv.KEEP_OVERLAP_MAX, .10)

    def test_when_every_spot_overlaps_the_chunk_is_placed_as_before_and_reported(self):
        small = save(quiet_frame(size=(400, 200), busy=()), self.dir, 's.png')
        found = rv.find_regions(small, 0)
        zone = [100, 50, 300, 150]                                     # any 300 x 100 box in this frame covers half of it
        plain = rv.place_boxes(small, found, [[(300, 100)]])
        result = rv.place_boxes(small, found, [[(300, 100)]], keep=[zone])
        self.assertEqual(result['boxes'], plain['boxes'])
        self.assertGreaterEqual(self.share(result['boxes'][0], zone), .5)
        self.assertEqual(result['keep_overlaps'], {0: [0]})

    def test_the_report_names_the_zones_by_their_place_in_the_list_and_only_the_chunks_that_cover_them(self):
        small = save(quiet_frame(size=(400, 200), busy=()), self.dir, 's.png')
        found = rv.find_regions(small, 0)
        zones = [[380, 180, 400, 200], [100, 50, 300, 150], [120, 60, 280, 140]]      # the first is in a corner nobody reaches
        result = rv.place_boxes(small, found, [[(300, 100)]], keep=zones)
        self.assertEqual(result['keep_overlaps'], {0: [1, 2]})

    def test_a_painted_chunk_covers_its_region_and_says_so_while_a_free_one_keeps_off(self):
        path = save(frame(boxes=[(400, 60, 700, 160)]), self.dir, 'p.png')
        found = rv.find_regions(path, 1)
        zone = [380, 40, 720, 180]                                     # the painted balloon sits on it
        result = rv.place_boxes(path, found, [[(300, 100)], [(300, 100)]], keep=[zone])
        first, second = result['boxes']
        bbox = found['regions'][0]['bbox']
        self.assertTrue(first[0] <= bbox[0] and first[1] <= bbox[1] and first[2] >= bbox[2] and first[3] >= bbox[3])
        self.assertLess(self.share(second, zone), rv.KEEP_OVERLAP_MAX)
        self.assertEqual(result['keep_overlaps'], {0: [0]})

    def test_a_balloon_avoids_a_keep_zone_as_well_and_keeps_its_tail_rules(self):
        target = (900, 450)
        common = dict(rounded=[(.45, .4)], scale=.3, tail_margin=12)
        free = rv.place_boxes(self.path, self.found, [[(300, 100)]], [target], **common)
        box = free['boxes'][0]
        zone = [box[0] + 40, box[1] - 20, box[2] - 40, box[3] + 60]          # the art the balloon would have covered
        self.assertGreater(self.share(box, zone), .3)
        held = rv.place_boxes(self.path, self.found, [[(300, 100)]], [target], keep=[zone], **common)
        self.assertNotEqual(held['boxes'][0], box)
        self.assertLess(self.share(held['boxes'][0], zone), rv.KEEP_OVERLAP_MAX)
        self.assertEqual(held['keep_overlaps'], {})
        self.assertIsNotNone(rv.tail_wedge(held['boxes'][0], held['corner'][0], target, [0, 0, 1200, 600], .3))

    def test_zones_are_taken_inside_the_visible_frame_and_one_outside_it_is_ignored(self):
        outside = [1300, 0, 1500, 200]
        result = rv.place_boxes(self.path, self.found, [[(300, 100)]], keep=[outside])
        self.assertEqual(result['boxes'][0], self.legacy)
        self.assertEqual(result['keep_overlaps'], {})
        # A zone that runs past the frame counts by the part that is inside it: this one is 95 percent off the top.
        tall = [self.legacy[0], -2000, self.legacy[2], self.legacy[3]]
        self.assertLess(self.share(self.legacy, tall), rv.KEEP_OVERLAP_MAX)        # by its whole area the box barely touches it
        moved = rv.place_boxes(self.path, self.found, [[(300, 100)]], keep=[tall])
        self.assertNotEqual(moved['boxes'][0], self.legacy)                        # by the part in the frame it covers all of it
        self.assertLess(self.share(moved['boxes'][0], [tall[0], 0, tall[2], tall[3]]), rv.KEEP_OVERLAP_MAX)

    def test_no_zones_changes_nothing_and_reports_nothing(self):
        for keep in (None, [], ()):
            result = rv.place_boxes(self.path, self.found, [[(300, 100)]], keep=keep)
            self.assertEqual(result['boxes'][0], self.legacy)
            self.assertEqual(result['keep_overlaps'], {})
            self.assertEqual(result['edge_voice_no_tail'], [])

    def test_a_keep_zone_outranks_an_off_frame_tail_when_both_cannot_be_had(self):
        # In this small frame every place that leaves room for the tail at the top covers more than a tenth of the zone
        # (the lower half); the top edge itself clears it. The balloon gives up its tail, not the art.
        small = save(quiet_frame(size=(400, 200), busy=()), self.dir, 'k.png')
        found = rv.find_regions(small, 0)
        zone = [0, 100, 400, 200]
        common = dict(rounded=[(.45, .4)], scale=.3, tail_margin=12)
        free = rv.place_boxes(small, found, [[(300, 100)]], [(200, 0)], **common)
        self.assertGreaterEqual(free['boxes'][0][1], 8.8 / .3)                        # without the zone it has its tail
        result = rv.place_boxes(small, found, [[(300, 100)]], [(200, 0)], keep=[zone], **common)
        self.assertLess(result['boxes'][0][1], 8.8 / .3)
        self.assertEqual(result['edge_voice_no_tail'], [0])
        self.assertEqual(result['keep_overlaps'], {})
        self.assertLess(self.share(result['boxes'][0], zone), rv.KEEP_OVERLAP_MAX)


def painted_outside(region, box, ratio):
    """Independent brute force: painted pixels (the region plus its outline ring) outside a rounded rectangle."""
    ox, oy = region['painted']['origin']
    ys, xs = np.nonzero(region['painted']['mask'])
    px, py = xs + ox + .5, ys + oy + .5
    x0, y0, x1, y1 = box
    r = ratio * min(x1 - x0, y1 - y0)
    dx, dy = np.minimum(px - x0, x1 - px), np.minimum(py - y0, y1 - py)
    inside = (dx >= 0) & (dy >= 0) & ((dx >= r) | (dy >= r) | ((r - dx) ** 2 + (r - dy) ** 2 <= (r - 1) ** 2))
    return int((~inside).sum())


class CornerCoverTests(Tmp):
    """A drawn balloon must hide every painted pixel of its region, corners included."""

    ROUND = (.45, .40)

    def setup_region(self, rect=(300, 200, 900, 300), name='r.png'):
        path = save(frame(boxes=[rect]), self.dir, name)
        return path, rv.find_regions(path, 1)

    def test_find_regions_reports_the_painted_pixels_with_their_outline_ring(self):
        path, found = self.setup_region()
        region = found['regions'][0]
        painted = region['painted']
        ox, oy = painted['origin']
        mask = painted['mask']
        x0, y0, x1, y1 = region['bbox']
        self.assertEqual((ox, oy), (x0 - 5, y0 - 5))
        self.assertEqual(mask.shape, (y1 - y0 + 10, x1 - x0 + 10))
        self.assertTrue(mask[5:-5, 5:-5].all() or mask.sum() > 0.9 * mask.size)       # rectangular region
        self.assertGreater(len(painted['edge']), 0)
        for px, py in painted['edge'][:50]:
            self.assertTrue(mask[int(py - oy), int(px - ox)])                          # edge points are painted pixels

    def test_the_hidden_test_needs_the_corners_inside_the_rounded_shape(self):
        path, found = self.setup_region()
        region = found['regions'][0]
        x0, y0, x1, y1 = region['bbox']
        cover = [x0 - 8, y0 - 8, x1 + 8, y1 + 8]
        self.assertFalse(rv.painted_hidden(region['painted'], cover, .45))
        self.assertGreater(painted_outside(region, cover, .45), 0)
        for ratio in (.45, .40):
            r = ratio * (cover[3] - cover[1])
            e = int(np.ceil(.30 * r))
            grown = [cover[0] - e, cover[1] - e, cover[2] + e, cover[3] + e]
            with self.subTest(ratio=ratio):
                self.assertTrue(rv.painted_hidden(region['painted'], grown, ratio))
                self.assertEqual(painted_outside(region, grown, ratio), 0)
        # Sharp corners need nothing beyond the box itself.
        self.assertTrue(rv.painted_hidden(region['painted'], cover, 0.0))

    def test_a_rounded_box_over_a_rectangular_region_grows_until_its_corners_are_hidden(self):
        path, found = self.setup_region()
        options = [[(620, 110)]]
        plain = rv.place_boxes(path, found, options)
        rounded = rv.place_boxes(path, found, options, rounded=[self.ROUND])
        box, ratio = rounded['boxes'][0], rounded['corner'][0]
        area = lambda b: (b[2] - b[0]) * (b[3] - b[1])
        self.assertIn(ratio, self.ROUND)
        self.assertEqual(painted_outside(found['regions'][0], box, ratio), 0)
        self.assertGreater(area(box), area(plain['boxes'][0]))
        self.assertEqual(plain['corner'], [None])
        # Whichever keeps the box smaller: never larger than expanding at the full radius alone.
        full = rv.place_boxes(path, found, options, rounded=[(.45, .45)])
        self.assertEqual(painted_outside(found['regions'][0], full['boxes'][0], .45), 0)
        self.assertLessEqual(area(box), area(full['boxes'][0]))
        self.assertEqual(ratio, .40)                       # the smaller radius needs the smaller expansion here

    def test_a_box_that_already_hides_the_corners_is_not_enlarged(self):
        path, found = self.setup_region()
        options = [[(1000, 400)]]
        plain = rv.place_boxes(path, found, options)
        rounded = rv.place_boxes(path, found, options, rounded=[self.ROUND])
        self.assertEqual(rounded['boxes'], plain['boxes'])
        self.assertEqual(rounded['corner'], [.45])
        self.assertEqual(painted_outside(found['regions'][0], rounded['boxes'][0], .45), 0)

    def test_captions_and_chunks_without_a_region_are_untouched(self):
        path, found = self.setup_region()
        plain = rv.place_boxes(path, found, [[(620, 110)], [(300, 80)]])
        mixed = rv.place_boxes(path, found, [[(620, 110)], [(300, 80)]], rounded=[None, self.ROUND])
        self.assertEqual(mixed['boxes'], plain['boxes'])
        self.assertEqual(mixed['corner'], [None, .45])

    def test_a_partly_covered_region_is_not_held_to_the_corner_rule(self):
        path, found = self.setup_region((100, 100, 700, 260), 'p.png')
        result = rv.place_boxes(path, found, [[(250, 100)]], [(400, 180)], rounded=[self.ROUND], tail_margin=12)
        self.assertEqual(result['partial'], [True])

    def test_corners_that_cannot_be_hidden_fail_and_say_so(self):
        # A painted box in the frame's corner: the box cannot grow past the frame, and a balloon keeps
        # at least 40 percent of its shorter side as corner radius.
        path, found = self.setup_region((6, 6, 500, 120), 'c.png')
        with self.assertRaises(rv.PlacementError) as caught:
            rv.place_boxes(path, found, [[(520, 140), (600, 200)]], rounded=[self.ROUND])
        self.assertIn('chunk 0', str(caught.exception))
        self.assertIn('corner', str(caught.exception))
        # The same chunk as a caption (no rounding) is fine.
        rv.place_boxes(path, found, [[(520, 140)]], rounded=[None])


class EdgeBleedTests(Tmp):
    """A balloon may run off a frame edge its painted region touches, by no more than it needs."""

    ROUND = (.45, .40)
    CLEAR = 1 - float(np.sqrt(.5))
    BOUNDS = (0, 0, 1200, 600)

    def place(self, rect, options, rounded=None, **kwargs):
        path = save(frame(boxes=[rect]), self.dir, 'b.png')
        found = rv.find_regions(path, 1)
        rounded = [self.ROUND] if rounded is None else rounded
        return found, rv.place_boxes(path, found, options, rounded=rounded, **kwargs)

    def bleeds(self, box):
        b = self.BOUNDS
        return [max(0, b[0] - box[0]), max(0, b[1] - box[1]), max(0, box[2] - b[2]), max(0, box[3] - b[3])]

    def test_a_corner_pinned_region_bleeds_off_the_edges_it_touches_and_hides_completely(self):
        found, result = self.place((6, 6, 500, 120), [[(520, 140)]], bleed=40)
        box, ratio = result['boxes'][0], result['corner'][0]
        left, top, right, bottom = self.bleeds(box)
        self.assertGreater(left + top, 0)
        self.assertEqual((right, bottom), (0, 0))                                # the far edges are not touched
        self.assertEqual(result['bleed'], [[left, top, 0, 0]])
        self.assertEqual(painted_outside(found['regions'][0], box, ratio), 0)
        # The padded text area (the box inset by the corner clearance) stays inside the frame.
        clear = self.CLEAR * ratio * min(box[2] - box[0], box[3] - box[1])
        self.assertLessEqual(max(left, top), clear + 1e-6)
        # No more than needed: moving the box inward a little would expose painted pixels again.
        if left > 2:
            self.assertGreater(painted_outside(found['regions'][0], [box[0] + 2, box[1], box[2] + 2, box[3]], ratio), 0)
        if top > 2:
            self.assertGreater(painted_outside(found['regions'][0], [box[0], box[1] + 2, box[2], box[3] + 2], ratio), 0)

    def test_without_the_bleed_option_the_same_chunk_fails(self):
        with self.assertRaisesRegex(rv.PlacementError, 'corner'):
            self.place((6, 6, 500, 120), [[(520, 140)]])

    def test_a_box_never_extends_past_an_edge_its_region_does_not_touch(self):
        # The painted balloon is 10 px from the left edge and 70 px from the top. Only the left may bleed.
        found, result = self.place((6, 66, 500, 180), [[(520, 400)]], bleed=40)
        left, top, right, bottom = self.bleeds(result['boxes'][0])
        self.assertGreater(left, 0)
        self.assertEqual((top, right, bottom), (0, 0, 0))
        self.assertEqual(painted_outside(found['regions'][0], result['boxes'][0], result['corner'][0]), 0)
        # With nothing close enough to count as touching, it fails instead of bleeding.
        with self.assertRaisesRegex(rv.PlacementError, 'corner'):
            self.place((6, 66, 500, 180), [[(520, 400)]], bleed=5)

    def test_growth_is_measured_from_the_box_as_drawn_not_from_the_text_size(self):
        # The painted region (885 x 185 px) is larger than the text box (451 x 179 px). Growth counted from
        # the text size would inflate the height, which only enlarges the corner radius and defeats the rule.
        found, result = self.place((8, 8, 900, 200), [[(451, 179)]], bleed=39)
        box, ratio = result['boxes'][0], result['corner'][0]
        self.assertEqual(painted_outside(found['regions'][0], box, ratio), 0)
        self.assertLess(box[3] - box[1], 260)
        self.assertLess(box[2] - box[0], 960)

    def test_a_caption_never_bleeds(self):
        found, result = self.place((6, 6, 500, 120), [[(520, 140)]], rounded=[None], bleed=40)
        self.assertEqual(self.bleeds(result['boxes'][0]), [0, 0, 0, 0])

    def test_nothing_bleeds_when_the_box_hides_the_region_inside_the_frame(self):
        path = save(frame(boxes=[(300, 200, 900, 300)]), self.dir, 'mid.png')
        found = rv.find_regions(path, 1)
        with_bleed = rv.place_boxes(path, found, [[(620, 110)]], rounded=[self.ROUND], bleed=40)
        without = rv.place_boxes(path, found, [[(620, 110)]], rounded=[self.ROUND])
        self.assertEqual(with_bleed['boxes'], without['boxes'])
        self.assertEqual(with_bleed['bleed'], [[0, 0, 0, 0]])
        # A region against the frame edge that is already hidden inside it does not bleed either.
        found, result = self.place((6, 6, 500, 120), [[(1000, 500)]], bleed=40)
        self.assertEqual(result['bleed'], [self.bleeds(result['boxes'][0])])
        self.assertLessEqual(max(result['bleed'][0]), self.CLEAR * result['corner'][0] * 500 + 1e-6)


class FaceAvoidTests(Tmp):
    """A drawn box must never cover a face: it moves clear of it, or placement fails and says so."""

    MARGIN = 4

    def place(self, rects, options, faces=None, **kwargs):
        path = save(frame(boxes=rects), self.dir, 'fc.png')
        found = rv.find_regions(path, max(1, len(rects)))
        return found, rv.place_boxes(path, found, options, faces=faces, face_margin=self.MARGIN, **kwargs)

    def test_the_shape_distance_uses_the_rounded_corner_not_the_rectangle(self):
        face = (-6.0, -6.0, 2.0, 'face 0')                          # just off the box's top-left corner
        box = [0, 0, 100, 100]
        rectangle = rv.face_gap(box, None, face)
        rounded = rv.face_gap(box, .4, face)
        self.assertAlmostEqual(rectangle, np.hypot(6, 6) - 2, places=6)
        self.assertAlmostEqual(rounded, np.hypot(46, 46) - 40 - 2, places=6)        # past the arc, not the corner
        self.assertGreater(rounded, rectangle)
        self.assertLess(rv.face_gap(box, .4, (50.0, 50.0, 10.0, 'inside')), 0)     # overlapping is negative
        self.assertAlmostEqual(rv.face_gap(box, .4, (150.0, 50.0, 10.0, 'beside')), 40.0, places=6)

    def test_a_box_that_would_have_covered_a_face_moves_clear_of_it(self):
        rect = (300, 150, 700, 250)
        options = [[(900, 200), (500, 200)]]
        found, without = self.place([rect], options)
        face = (850.0, 200.0, 60.0, 'face 0')
        self.assertEqual(without['choice'], [0])
        self.assertLess(rv.face_gap(without['boxes'][0], None, face), 0)          # the old placement covers it
        found, result = self.place([rect], options, faces=[face])
        self.assertEqual(result['choice'], [1])                                    # a narrower box, clear of it
        self.assertGreaterEqual(rv.face_gap(result['boxes'][0], None, face), self.MARGIN)
        self.assertEqual(result['face_clearance'][0][1], 'face 0')
        self.assertAlmostEqual(result['face_clearance'][0][0], rv.face_gap(result['boxes'][0], None, face), places=6)
        bbox = found['regions'][0]['bbox']
        box = result['boxes'][0]
        self.assertTrue(box[0] <= bbox[0] - 8 and box[2] >= bbox[2] + 8)           # and it still covers the painted region

    def test_when_the_painted_region_cannot_be_covered_without_a_face_it_fails_naming_both(self):
        with self.assertRaises(rv.PlacementError) as caught:
            self.place([(300, 150, 700, 250)], [[(500, 200), (400, 200)]], faces=[(500.0, 200.0, 40.0, 'the Woman')])
        message = str(caught.exception)
        self.assertIn('chunk 0', message)
        self.assertIn('would cover a face', message)
        self.assertIn('the Woman', message)

    def test_a_face_only_a_larger_box_would_reach_also_fails_with_the_reason(self):
        # The region itself is clear of the face; every box that holds the text reaches it.
        with self.assertRaises(rv.PlacementError) as caught:
            self.place([(300, 150, 700, 250)], [[(900, 200), (850, 200)]], faces=[(850.0, 200.0, 60.0, 'the Woman')])
        self.assertIn('would cover a face', str(caught.exception))
        self.assertIn('the Woman', str(caught.exception))

    def test_without_a_painted_region_the_quiet_window_search_avoids_faces_too(self):
        image = quiet_frame()
        path = save(image, self.dir, 'quietface.png')
        found = rv.find_regions(path, 1)
        free = rv.place_boxes(path, found, [[(300, 100)]])
        x0, y0, x1, y1 = free['boxes'][0]
        face = ((x0 + x1) / 2, (y0 + y1) / 2, 70.0, 'face 0')
        result = rv.place_boxes(path, found, [[(300, 100)]], faces=[face], face_margin=self.MARGIN)
        self.assertNotEqual(result['boxes'], free['boxes'])
        self.assertGreaterEqual(rv.face_gap(result['boxes'][0], None, face), self.MARGIN)
        self.assertEqual(result['face_clearance'][0][1], 'face 0')
        # A face on every clear window leaves nowhere to put it.
        blanket = [(x, y, 140.0, f'face {x}-{y}') for x in range(100, 1200, 150) for y in range(100, 600, 150)]
        with self.assertRaisesRegex(rv.PlacementError, 'would cover a face'):
            rv.place_boxes(path, found, [[(300, 100)]], faces=blanket, face_margin=self.MARGIN)

    def test_a_rounded_box_keeps_its_rounded_shape_clear_and_bleed_is_included(self):
        path = save(frame(boxes=[(6, 6, 500, 120)]), self.dir, 'corner.png')
        found = rv.find_regions(path, 1)
        plain = rv.place_boxes(path, found, [[(520, 140)]], rounded=[(.45, .40)], bleed=40)
        self.assertGreater(max(plain['bleed'][0]), 0)                                  # it bleeds off the corner
        box, ratio = plain['boxes'][0], plain['corner'][0]
        # A face just beyond the frame corner (where the bleed reaches) now blocks that bleed.
        face = (-20.0, -20.0, 45.0, 'face 0')
        self.assertLess(rv.face_gap(box, ratio, face), self.MARGIN)
        with self.assertRaisesRegex(rv.PlacementError, 'would cover a face|corner'):
            rv.place_boxes(path, found, [[(520, 140)]], rounded=[(.45, .40)], bleed=40, faces=[face],
                           face_margin=self.MARGIN)

    def test_without_faces_nothing_changes_and_no_clearance_is_reported(self):
        found, result = self.place([(300, 150, 700, 250)], [[(900, 200), (500, 200)]])
        self.assertEqual(result['face_clearance'], [None])
        found, empty = self.place([(300, 150, 700, 250)], [[(900, 200), (500, 200)]], faces=[])
        self.assertEqual(empty['boxes'], result['boxes'])


class TallCoverTests(Tmp):
    """A balloon over a painted region taller than its text keeps the interior width its wrap needs.

    A taller rounded shape takes more corner clearance, so a box sized for the text alone would narrow
    the text area and re-wrap the copy. `widen[i][k](height_px, ratio)` names the width (px) option k of
    chunk i needs at a box height and corner ratio; the box is widened to it.
    """

    ROUND = (.45, .40)
    REGION = (300, 200, 600, 400)            # 300 x 200 px: its cover is 316 x 216 px
    MARGIN = 4

    def place(self, widen, rect=REGION, options=((340, 100),), faces=None):
        path = save(frame(boxes=[rect]), self.dir, 'tall.png')
        found = rv.find_regions(path, 1)
        result = rv.place_boxes(path, found, [list(options)], rounded=[self.ROUND], widen=widen, faces=faces,
                                face_margin=self.MARGIN)
        return found, result

    def test_the_box_is_widened_to_the_width_its_height_needs_and_still_covers_the_region(self):
        seen = []

        def need(height, ratio):
            seen.append((height, ratio))
            return 2 * height

        found, result = self.place([[need]])
        x0, y0, x1, y1 = result['boxes'][0]
        _, plain = self.place(None)
        self.assertLess(plain['boxes'][0][2] - plain['boxes'][0][0], 2 * (y1 - y0))         # it would have been too narrow
        self.assertEqual(x1 - x0, 2 * (y1 - y0) + 1)                                        # the width asked for, plus a pixel
        bx0, by0, bx1, by1 = found['regions'][0]['bbox']
        self.assertTrue(x0 <= bx0 - 8 and y0 <= by0 - 8 and x1 >= bx1 + 8 and y1 >= by1 + 8)
        self.assertTrue(all(height >= y1 - y0 - 1 for height, _ in seen))                   # asked about boxes this tall
        self.assertTrue(all(.40 <= ratio <= .45 for _, ratio in seen))

    def test_without_a_widener_or_with_one_that_asks_for_less_nothing_changes(self):
        _, plain = self.place(None)
        for widen in ([[None]], [[lambda height, ratio: 100]], [[lambda height, ratio: 340]], [None]):
            _, result = self.place(widen)
            self.assertEqual(result['boxes'], plain['boxes'])
            self.assertEqual(result['corner'], plain['corner'])

    def test_widening_is_clamped_to_the_frame(self):
        found, result = self.place([[lambda height, ratio: 2 * height]], rect=(20, 200, 320, 400))
        x0, y0, x1, y1 = result['boxes'][0]
        self.assertGreaterEqual(x0, 0)
        self.assertEqual(x1 - x0, 2 * (y1 - y0) + 1)
        self.assertLessEqual(x0, found['regions'][0]['bbox'][0] - 8)                        # still covers the region's left edge

    def test_a_widened_box_keeps_clear_of_a_face(self):
        wide = lambda height, ratio: 2 * height
        face = (670.0, 300.0, 20.0, 'face 0')                                               # the centred wide box would reach it
        _, without = self.place([[wide]])
        self.assertLess(rv.face_gap(without['boxes'][0], self.ROUND[0], face), self.MARGIN)
        found, result = self.place([[wide]], faces=[face])
        box = result['boxes'][0]
        self.assertGreaterEqual(rv.face_gap(box, result['corner'][0], face), self.MARGIN)
        self.assertEqual(box[2] - box[0], 2 * (box[3] - box[1]) + 1)
        self.assertLessEqual(box[0], found['regions'][0]['bbox'][0] - 8)                    # moved left, still covering the region

    def test_a_region_that_cannot_hold_the_widened_box_fails_to_place(self):
        with self.assertRaises(rv.PlacementError):
            self.place([[lambda height, ratio: 1300]])                          # wider than the 1200 px frame


class CoverCropTests(unittest.TestCase):
    """cover_crop: the part of a frame's art to show so that it fills its slot, without losing what must stay."""

    ART = [0, 0, 1536, 1024]             # a 3:2 generator frame
    OFFSET = [100, 50, 1400, 900]        # art that starts away from the origin, 1300 x 850

    def inside(self, inner, outer):
        return outer[0] <= inner[0] and outer[1] <= inner[1] and inner[2] <= outer[2] and inner[3] <= outer[3]

    def test_min_keep_is_forty_five_percent(self):
        self.assertEqual(rv.MIN_KEEP, .45)

    def test_a_slot_with_the_same_aspect_leaves_the_art_unchanged(self):
        self.assertEqual(rv.cover_crop(self.ART, 1.5, [[700, 400, 800, 500]]), self.ART)
        self.assertEqual(rv.cover_crop(self.ART, 1.5 * 1.02, []), self.ART)              # within 2 percent, as fit_clip_contain
        self.assertEqual(rv.cover_crop(self.ART, 1.5 / 1.015, []), self.ART)
        self.assertNotEqual(rv.cover_crop(self.ART, 1.5 * 1.05, []), self.ART)

    def test_a_wide_slot_crops_the_height_only_and_centres_on_the_keep_span(self):
        keep = [[700, 400, 900, 500]]                                   # centre y 450
        crop = rv.cover_crop(self.ART, 2.4, keep)                       # 1536 / 2.4 = 640 px tall
        self.assertEqual(crop, [0, 130, 1536, 770])
        self.assertTrue(self.inside(keep[0], crop))
        self.assertEqual(rv.cover_crop(self.ART, 2.4, []), [0, 192, 1536, 832])      # no keep: the art's centre

    def test_the_band_is_moved_inside_the_art_when_the_keep_sits_near_an_edge(self):
        keep = [[100, 20, 300, 120]]
        crop = rv.cover_crop(self.ART, 2.4, keep)
        self.assertEqual(crop, [0, 0, 1536, 640])
        low = rv.cover_crop(self.ART, 2.4, [[100, 900, 300, 1000]])
        self.assertEqual(low, [0, 384, 1536, 1024])

    def test_the_crop_stops_at_min_keep_and_leaves_a_remainder_for_the_slot_to_fit(self):
        crop = rv.cover_crop(self.ART, 4.0, [[700, 400, 900, 500]])      # 1536 / 4 = 384 px, but 45 percent is 460.8
        height = crop[3] - crop[1]
        self.assertGreaterEqual(height, .45 * 1024)
        self.assertLess(height, .45 * 1024 + 2)                          # only rounded outward
        self.assertGreater(height, 1536 / 4.0)
        self.assertLess((crop[2] - crop[0]) / height, 4.0)                # still not as wide as the slot: side bars remain
        self.assertEqual(rv.cover_crop(self.ART, 4.0, [[700, 400, 900, 500]], min_keep=.25), [0, 258, 1536, 642])

    def test_a_keep_span_taller_than_the_target_wins(self):
        keep = [[0, 100, 100, 300], [1400, 700, 1500, 900]]             # spans y 100 to 900
        crop = rv.cover_crop(self.ART, 2.4, keep)
        self.assertEqual(crop, [0, 100, 1536, 900])
        for rect in keep:
            self.assertTrue(self.inside(rect, crop))

    def test_a_tall_slot_crops_the_width_only(self):
        keep = [[1200, 300, 1300, 400]]
        crop = rv.cover_crop(self.ART, .75, keep)                        # 1024 * .75 = 768 px wide
        self.assertEqual(crop, [768, 0, 1536, 1024])                     # centre 1250 would pass the right edge: clamped
        self.assertTrue(self.inside(keep[0], crop))
        self.assertEqual(rv.cover_crop(self.ART, .75, []), [384, 0, 1152, 1024])
        near = rv.cover_crop(self.ART, .75, [[0, 0, 900, 100]])          # a keep span wider than the target wins
        self.assertEqual(near, [0, 0, 900, 1024])
        limited = rv.cover_crop(self.ART, .4, [[700, 100, 800, 200]])    # 410 px is under 45 percent of 1536
        self.assertGreaterEqual(limited[2] - limited[0], .45 * 1536)

    def test_art_that_does_not_start_at_the_origin_is_cropped_inside_itself(self):
        crop = rv.cover_crop(self.OFFSET, 2.4, [[900, 300, 1000, 400]])   # 1300 / 2.4 = 541.7 px tall
        self.assertTrue(self.inside(crop, self.OFFSET))
        self.assertEqual((crop[0], crop[2]), (100, 1400))
        self.assertTrue(self.inside([900, 300, 1000, 400], crop))
        self.assertAlmostEqual(crop[3] - crop[1], 1300 / 2.4, delta=2)
        self.assertEqual(rv.cover_crop(self.OFFSET, 2.4, []), [100, 204, 1400, 746])

    def test_keep_rects_are_clipped_to_the_art_and_empty_ones_ignored(self):
        self.assertEqual(rv.cover_crop(self.ART, 2.4, [[-500, -500, -100, -100], [2000, 50, 2100, 90]]),
                         rv.cover_crop(self.ART, 2.4, []))
        self.assertEqual(rv.cover_crop(self.ART, 2.4, [[-50, -80, 40, 90]]), [0, 0, 1536, 640])   # clipped to y 0..90
        self.assertEqual(rv.cover_crop(self.ART, 2.4, [[10, 10, 10, 900]]), rv.cover_crop(self.ART, 2.4, []))

    def test_keep_on_the_axis_that_is_not_cropped_changes_nothing(self):
        self.assertEqual(rv.cover_crop(self.ART, 2.4, [[0, 400, 1536, 500]]), rv.cover_crop(self.ART, 2.4, [[700, 400, 800, 500]]))

    def test_the_result_is_always_whole_pixels_inside_the_art_and_holds_every_keep_rect(self):
        import random
        rng = random.Random(15)
        for art in (self.ART, self.OFFSET, [2, 2, 1900, 820]):
            for _ in range(300):
                aspect = rng.choice([.3, .5, .9, 1.0, 1.4, 1.5, 2.0, 3.0, 3.69, 5.0, 7.0])
                keep = []
                for _ in range(rng.randint(0, 4)):
                    x0, y0 = rng.uniform(art[0] - 50, art[2]), rng.uniform(art[1] - 50, art[3])
                    keep.append([x0, y0, x0 + rng.uniform(1, 400.5), y0 + rng.uniform(1, 300.5)])
                crop = rv.cover_crop(art, aspect, keep)
                with self.subTest(art=art, aspect=aspect, keep=keep):
                    self.assertTrue(all(isinstance(v, int) for v in crop))
                    self.assertTrue(self.inside(crop, art))
                    for rect in keep:
                        clipped = [max(rect[0], art[0]), max(rect[1], art[1]), min(rect[2], art[2]), min(rect[3], art[3])]
                        if clipped[2] > clipped[0] and clipped[3] > clipped[1]:
                            self.assertTrue(self.inside(clipped, crop))
                    w, h = art[2] - art[0], art[3] - art[1]
                    if aspect > w / h * 1.02:                               # only the height is cropped
                        self.assertEqual((crop[0], crop[2]), (art[0], art[2]))
                    elif aspect < w / h / 1.02:                             # only the width is cropped
                        self.assertEqual((crop[1], crop[3]), (art[1], art[3]))
                    else:
                        self.assertEqual(crop, art)


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union else 0


def agrees(det, hand, grow=40):
    inside = (det[0] >= hand[0] - grow and det[1] >= hand[1] - grow
              and det[2] <= hand[2] + grow and det[3] <= hand[3] + grow)
    return inside or iou(det, hand) >= .5


def best_matching(dets, hands):
    """Pair detections with hand rects to maximise agreements (hand order can differ from reading order)."""
    n = len(hands)
    if n <= 7:
        best = max(itertools.permutations(range(n)),
                   key=lambda perm: (sum(agrees(dets[i], hands[j]) for i, j in enumerate(perm)),
                                     sum(iou(dets[i], hands[j]) for i, j in enumerate(perm))))
        return list(enumerate(best))
    return [(i, i) for i in range(n)]


class RealDataRegressionTests(unittest.TestCase):
    """Detected reserves versus the rects Codex measured by hand on accepted selections."""

    PACKAGES = ('ch02', 'ch01-v2')

    def selections(self):
        """Selections with hand-measured, unstyled reserves.

        Provisional selections carry placeholder reserves (no "kind", a rect spanning the
        frame edge, several chunks in one) and their frames hold no blank boxes at all, so
        they are not evidence of what Codex measured and are left out.
        """
        found, placeholders = [], []
        for package in self.PACKAGES:
            for path in sorted((V15 / 'chapters' / package / 'selections').glob('*.json')):
                record = json.loads(path.read_text())
                reserves = record.get('reserves') or []
                if not reserves or any('style' in r for r in reserves) or not Path(record['path']).is_file():
                    continue
                if not all('kind' in r for r in reserves):
                    placeholders.append(f"{package}/{record['id']}")
                    continue
                found.append((package, record))
        self.placeholders = placeholders
        return found

    def test_detector_agrees_with_hand_measured_reserves(self):
        selections = self.selections()
        if not selections:
            self.skipTest('no reviewed selections available')
        total = agreed = 0
        disagreements = []
        for package, record in selections:
            hands = [r['rect'] for r in record['reserves']]
            speakers = ['CAPTION' if r['kind'] == 'caption' else 'SPEAKER' for r in record['reserves']]
            try:
                dets = [r['rect'] for r in rv.detect_reserves(record['path'], len(hands), speakers)['reserves']]
            except rv.ReserveError as error:
                total += len(hands)
                disagreements.append(f"{package}/{record['id']}: {error}")
                continue
            for i, j in best_matching(dets, hands):
                total += 1
                if agrees(dets[i], hands[j]):
                    agreed += 1
                else:
                    disagreements.append(f"{package}/{record['id']}: detected {dets[i]} hand {hands[j]}")
        rate = agreed / total
        print(f'\nreserve detection agreement: {agreed}/{total} = {rate:.1%} over {len(selections)} selections')
        print(f'  skipped {len(self.placeholders)} provisional selections with placeholder reserves: '
              + ', '.join(self.placeholders))
        for line in disagreements:
            print('  disagrees:', line)
        self.assertGreaterEqual(rate, .8)


if __name__ == '__main__':
    unittest.main()
