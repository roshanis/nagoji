import unittest
from compositor import measure, geometry_for_script, scaled_row, verify_page_chunks, pdf_image_placements


class PrintContractTests(unittest.TestCase):
    def test_crop_uses_pixels_actually_placed(self):
        m = measure([2000, 1000], [500, 0, 1500, 1000], [0, 0, 360, 360])
        self.assertEqual(m['effective_ppi'], 200)
        self.assertEqual(m['matrix'][0], 720)

    def test_upscale_updates_all_pixel_coordinates(self):
        row = {'width': 100, 'height': 50, 'visible_rect': [1, 1, 99, 49],
               'reserves': [{'rect': [3, 4, 60, 20], 'copy_indices': [0]}],
               'sound_origin': [70, 25]}
        result = scaled_row(row, 200, 100)
        self.assertEqual(result['visible_rect'], [2, 2, 198, 98])
        self.assertEqual(result['reserves'][0]['rect'], [6, 8, 120, 40])
        self.assertEqual(result['sound_origin'], [140, 50])
        self.assertEqual(row['width'], 100)

    def test_upscale_scales_the_art_rect_with_the_visible_rect(self):
        row = {'width': 100, 'height': 50, 'visible_rect': [1, 10, 99, 40], 'art_rect': [1, 1, 99, 49], 'reserves': []}
        result = scaled_row(row, 200, 100)
        self.assertEqual(result['visible_rect'], [2, 20, 198, 80])
        self.assertEqual(result['art_rect'], [2, 2, 198, 98])
        self.assertEqual(row['art_rect'], [1, 1, 99, 49])
        self.assertNotIn('art_rect', scaled_row({'width': 100, 'height': 50, 'visible_rect': [1, 1, 99, 49], 'reserves': []}, 200, 100))

    def test_dpi_gate_reuses_an_existing_upscale_only_when_it_is_this_source_doubled(self):
        # A build that fails after upscaling leaves its 2x files behind; the next build must not stop on them,
        # but must never adopt a file that is not an upscale of this frame.
        import hashlib, tempfile
        from pathlib import Path
        import numpy as np
        from PIL import Image
        from compositor import dpi_gate
        with tempfile.TemporaryDirectory() as tmp:
            chapter = Path(tmp)
            (chapter / 'frames').mkdir()
            rng = np.random.default_rng(7)
            base = rng.integers(0, 255, (25, 50, 3), dtype=np.uint8)
            source = chapter / 'frames' / 'page-01-panel-01-v01.png'
            Image.fromarray(base).resize((200, 100), Image.BICUBIC).save(source)
            row = {'id': 'page-01-panel-01', 'path': str(source), 'width': 200, 'height': 100,
                   'visible_rect': [0, 0, 200, 100], 'reserves': [],
                   'sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
            geometry = {'pages': {'1': [{'id': 'page-01-panel-01', 'rect_pt': [0, 0, 60, 30]}]}}   # 240 PPI, 480 at 2x
            dest = chapter / 'frames' / 'page-01-panel-01-v01-2x.png'
            never = Path('/usr/bin/false')                                        # the upscaler must not run
            Image.open(source).resize((400, 200), Image.BICUBIC).save(dest)
            rows, actions = dpi_gate([row], geometry, chapter, never, never)
            self.assertEqual(rows[0]['path'], str(dest.resolve()))
            self.assertEqual((rows[0]['width'], rows[0]['height']), (400, 200))
            self.assertTrue(actions[0]['reused_existing_output'])
            self.assertLess(actions[0]['reuse_mean_abs_diff'], 12)
            Image.fromarray(255 - np.asarray(Image.open(source).convert('RGB'))).resize((400, 200)).save(dest)
            with self.assertRaises(FileExistsError):
                dpi_gate([row], geometry, chapter, never, never)
            Image.open(source).resize((400, 201)).save(dest)                    # not exactly 2x
            with self.assertRaises(FileExistsError):
                dpi_gate([row], geometry, chapter, never, never)

    def test_any_chapter_length_and_panel_count(self):
        script = {'pages': {i: {'panels': [{'id': f'page-{i:02d}-panel-{j:02d}'} for j in range(1, 4)]} for i in range(1, 14)}}
        result = geometry_for_script(script)
        self.assertEqual(len(result['pages']), 13)
        self.assertEqual(len(result['pages']['13']), 3)
        for panels in result['pages'].values():
            for p in panels:
                x,y,w,h = p['rect_pt']
                self.assertGreaterEqual(y, 56.25)
                self.assertGreater(w,0)
                self.assertGreater(h,0)

    def test_missing_duplicate_and_reordered_copy_fail(self):
        chunks = ['One exact sentence.', 'Another exact sentence.']
        self.assertEqual(verify_page_chunks('Heading One exact\nsentence. Another exact sentence. 1',chunks),2)
        for text in ['One exact sentence.', 'Another exact sentence. One exact sentence.',
                     'One exact sentence. One exact sentence. Another exact sentence.']:
            with self.assertRaises(ValueError): verify_page_chunks(text,chunks)

    def test_actual_pdf_xobject_matrix_including_rotation(self):
        from io import BytesIO
        from PIL import Image
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.lib.utils import ImageReader
        from pypdf import PdfReader
        import math
        stream=BytesIO();pdf=Canvas(stream,pagesize=(441,666))
        pdf.saveState();pdf.translate(100,100);pdf.rotate(90)
        pdf.drawImage(ImageReader(Image.new('RGB',(300,150),'white')),0,0,width=72,height=36)
        pdf.restoreState();pdf.showPage();pdf.save();stream.seek(0)
        reader=PdfReader(stream);actual=pdf_image_placements(reader.pages[0],reader)
        self.assertEqual(len(actual),1)
        a,b,c,d,e,f=actual[0]['transform']
        self.assertAlmostEqual(actual[0]['width']/(math.hypot(a,b)/72),300)
        self.assertAlmostEqual(actual[0]['height']/(math.hypot(c,d)/72),300)
        self.assertEqual(len(actual[0]['rgb']),300*150*3)


class FontEmbeddingTests(unittest.TestCase):
    """KDP and IngramSpark preflight reject any unembedded font in a page's resources,
    even one that never draws a glyph. ReportLab's default canvas opens every page with
    an unembedded Helvetica, so the compositor must start pages in an embedded face."""

    def _one_page(self, canvas_factory, text=False):
        from io import BytesIO
        from pypdf import PdfReader
        stream = BytesIO(); pdf = canvas_factory(stream)
        pdf.rect(0, 0, 441, 666, stroke=0, fill=1)
        if text:
            pdf.setFont('Chapter01DIN', 10); pdf.drawString(20, 20, 'Lettered.')
        pdf.showPage(); pdf.save(); stream.seek(0)
        reader = PdfReader(stream)
        return reader.pages[0], reader

    def test_new_canvas_embeds_every_font_resource(self):
        from compositor import _new_canvas, embedded_fonts
        page, _ = self._one_page(_new_canvas)
        self.assertEqual(embedded_fonts(page), [])
        page, _ = self._one_page(_new_canvas, text=True)
        self.assertEqual(embedded_fonts(page), ['/AAAAAA+DINCondensed-Bold'])

    def test_font_audit_rejects_unembedded_helvetica(self):
        from reportlab.pdfgen.canvas import Canvas
        from compositor import embedded_fonts
        page, reader = self._one_page(lambda s: Canvas(s, pagesize=(441, 666)))
        with self.assertRaises(ValueError):
            embedded_fonts(page)



def lettering_fixture(directory, text, style=None, rect=None):
    """One deterministic 360 PPI panel, shared by rendering and pixel audits."""
    from pathlib import Path
    from PIL import Image
    import compositor as c
    image = Path(directory) / 'frame.png'
    if not image.exists():
        Image.new('RGB', (600, 300), '#fffdf7').save(image)
    reserve = {'kind': 'speech', 'rect': rect or [30, 30, 570, 230], 'copy_indices': [0]}
    if style is not None:
        reserve['style'] = style
    frame_id = 'page-01-panel-01'
    rows = [{'id': frame_id, 'path': str(image), 'sha256': c.sha256(image),
             'width': 600, 'height': 300, 'visible_rect': [0, 0, 600, 300],
             'reserves': [reserve]}]
    script = {'title': 'Lettering test', 'pages': {'1': {'panels': [
        {'id': frame_id, 'copy': [{'speaker': 'NAGOJI', 'text': text}]}]}}}
    geometry = {'pages': {'1': [{'id': frame_id, 'rect_pt': [100, 350, 120, 60]}]}}
    return rows, script, geometry


class LetteringStyleTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        from pathlib import Path
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def measurements(self, rows, script, geometry, reject=True):
        import compositor as c
        from types import SimpleNamespace
        return c.copy_fit_measurements(rows, script, geometry,
            SimpleNamespace(B=SimpleNamespace(measure=c.measure)), reject_failures=reject)

    def compose_fixture(self, text, style=None, rect=None):
        import compositor as c
        from pypdf import PdfReader
        rows, script, geometry = lettering_fixture(self.directory, text, style, rect)
        path = self.directory / 'styled.pdf'
        result = c.compose(rows, script, geometry, path)
        reader = PdfReader(path)
        return rows, script, result, path, reader

    def test_canonical_text_strips_pairs_and_preserves_unpaired_marker(self):
        import compositor as c
        self.assertEqual(c.canonical_text('Easy, *bhau*. *Come home*, now.'),
                         'Easy, bhau. Come home, now.')
        self.assertEqual(c.canonical_text('Plain copy.'), 'Plain copy.')
        self.assertEqual(c.canonical_text('A lone * remains.'), 'A lone * remains.')
        self.assertEqual(c.canonical_text('*one**two*'), 'onetwo')
        self.assertEqual(c.canonical_text('*one* *two'), 'one *two')

    def test_wrap_and_fit_use_canonical_copy(self):
        import compositor as c
        from reportlab.pdfbase import pdfmetrics
        c._register_fonts()
        font = pdfmetrics.getFont('Chapter01DIN')
        canonical = 'Easy, bhau. You are on land now.'
        marked = 'Easy, *bhau*. You are on land now.'
        width = font.stringWidth('Easy, bhau. You', c.DIN_SIZE_PT) + .01
        self.assertEqual(c._wrap_text(marked, font, c.DIN_SIZE_PT, width),
                         c._wrap_text(canonical, font, c.DIN_SIZE_PT, width))
        rows, script, geometry = lettering_fixture(self.directory, marked)
        measured = self.measurements(rows, script, geometry)[0]
        self.assertEqual(measured['lines'], c._wrap_text(canonical, font, 8.5, 104))
        self.assertNotIn('*', ''.join(measured['lines']))
        self.assertTrue(measured['fits'])

    def test_italic_pdf_is_canonical_oblique_and_verifies(self):
        import compositor as c
        from pypdf.generic import ContentStream
        marked = 'Easy, *bhau*. You are on land now.'
        rows, script, result, path, reader = self.compose_fixture(marked)
        text = reader.pages[0].extract_text()
        self.assertNotIn('*', text)
        self.assertEqual(c.verify_page_chunks(text, [marked]), 1)
        self.assertEqual(c.verify_pdf(path, rows, script, result['placements'])['script_chunks_verified'], 1)
        matrices = [args for args, op in ContentStream(reader.pages[0].get_contents(), reader).operations if op == b'Tm']
        self.assertTrue(any(abs(float(m[2]) - .21255656) < .00001 for m in matrices))
        self.assertTrue(any(float(m[2]) == 0 for m in matrices))

    def test_italic_phrase_wraps_with_punctuation_and_two_pairs(self):
        import compositor as c
        marked = 'A *long foreign phrase, carried across lines*; then *bhau*!'
        rows, script, result, path, reader = self.compose_fixture(marked)
        measured = result['copy_fit_measurements'][0]
        self.assertGreater(len(measured['lines']), 1)
        self.assertEqual(c.verify_page_chunks(reader.pages[0].extract_text(), [marked]), 1)
        self.assertEqual(c.verify_pdf(path, rows, script, result['placements'])['status'], 'pass')

    def test_plain_page_is_byte_identical_to_pre_change_compositor(self):
        import compositor as c
        from importlib.machinery import SourceFileLoader
        from importlib.util import module_from_spec, spec_from_loader
        from pathlib import Path
        backup = Path(c.__file__).parent / 'review/compositor.py.backup-pre-lettering-styles'
        loader = SourceFileLoader('pre_lettering_compositor', str(backup))
        old = module_from_spec(spec_from_loader(loader.name, loader))
        loader.exec_module(old)
        rows, script, geometry = lettering_fixture(self.directory, 'Easy, bhau. You are on land now.')
        before, after = self.directory / 'before.pdf', self.directory / 'after.pdf'
        old_result = old.compose(rows, script, geometry, before)
        new_result = c.compose(rows, script, geometry, after)
        self.assertEqual(before.read_bytes(), after.read_bytes())
        self.assertEqual(old_result, new_result)

    def test_unreadable_pdf_draws_only_vectors_and_clear_words(self):
        import compositor as c
        from pypdf.generic import ContentStream
        rows, script, result, path, reader = self.compose_fixture(
            '... *kapitan* ... *kapitan* ...', 'unreadable')
        text = reader.pages[0].extract_text()
        self.assertNotIn('...', text)
        self.assertNotIn('*', text)
        body = text.replace('Lettering test', '').replace('1', '').split()
        self.assertEqual(body, ['kapitan', 'kapitan'])
        operators = [op for args, op in ContentStream(reader.pages[0].get_contents(), reader).operations]
        self.assertGreaterEqual(operators.count(b'c'), 6)
        self.assertGreaterEqual(operators.count(b'm'), 6)
        self.assertIn(b'S', operators)
        self.assertEqual(c.verify_pdf(path, rows, script, result['placements'])['status'], 'pass')

    def test_unreadable_verification_checks_clear_word_order_and_count(self):
        import compositor as c
        chunks = ['... *kapitan* ... *bhau* ...']
        self.assertEqual(c.verify_page_chunks('kapitan bhau', chunks, styles=['unreadable']), 1)
        for text in ('bhau kapitan', 'kapitan', 'kapitan bhau kapitan bhau'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                c.verify_page_chunks(text, chunks, styles=['unreadable'])
        with self.assertRaises(ValueError):
            c.verify_page_chunks('kapitan bhau', chunks, styles=[])

    def test_unreadable_strokes_participate_in_wrap_and_fit(self):
        rows, script, geometry = lettering_fixture(self.directory, '... *kapitan* ...',
                                                   'unreadable', [30, 30, 160, 45])
        measured = self.measurements(rows, script, geometry, reject=False)[0]
        self.assertGreater(len(measured['lines']), 1)
        self.assertFalse(measured['fits'])
        with self.assertRaisesRegex(ValueError, 'does not fit'):
            self.measurements(rows, script, geometry)
        script['pages']['1']['panels'][0]['copy'][0]['text'] = '...'
        measured = self.measurements(rows, script, geometry, reject=False)[0]
        bounds = measured['actual_line_bounds_pt'][0]
        self.assertGreater(bounds[3] - bounds[1], 2)

    def test_unknown_reserve_style_is_rejected(self):
        import compositor as c
        rows, script, geometry = lettering_fixture(self.directory, 'Plain.')
        for value in ('italic', '', None, 7):
            rows[0]['reserves'][0]['style'] = value
            with self.subTest(style=value):
                with self.assertRaisesRegex(ValueError, 'style'):
                    c.validate_copy_runs(script, rows)
                with self.assertRaisesRegex(ValueError, 'style'):
                    self.measurements(rows, script, geometry)
        rows[0]['reserves'][0]['style'] = 'unreadable'
        self.assertEqual(c.scaled_row(rows[0], 1200, 600)['reserves'][0]['style'], 'unreadable')

    def test_oblique_fit_bounds_include_sheared_ink(self):
        import compositor as c
        rows, script, geometry = lettering_fixture(self.directory, '*kapitan*')
        bounds = self.measurements(rows, script, geometry)[0]['actual_line_bounds_pt'][0]
        upright = c._din_ink_metrics()('kapitan')
        self.assertAlmostEqual(bounds[2], upright[2] + c.OBLIQUE_SHEAR * upright[3])
        self.assertGreater(bounds[2], upright[2])

    def test_mixed_reserve_styles_verify_their_own_copy_indices(self):
        import compositor as c
        rows, script, geometry = lettering_fixture(self.directory, 'Easy, *bhau*.')
        script['pages']['1']['panels'][0]['copy'].append(
            {'speaker': 'NAGOJI', 'text': '... *kapitan* ...'})
        rows[0]['reserves'] = [
            {'rect': [30, 30, 570, 100], 'copy_indices': [0]},
            {'rect': [30, 130, 570, 230], 'copy_indices': [1], 'style': 'unreadable'}]
        path = self.directory / 'mixed.pdf'
        result = c.compose(rows, script, geometry, path)
        self.assertEqual(c.verify_pdf(path, rows, script, result['placements'])['script_chunks_verified'], 2)

    def test_adjacent_clear_pairs_verify_without_invented_spaces(self):
        import compositor as c
        rows, script, result, path, reader = self.compose_fixture('*ka**pitan* ...', 'unreadable')
        self.assertIn('kapitan', reader.pages[0].extract_text())
        self.assertEqual(c.verify_pdf(path, rows, script, result['placements'])['status'], 'pass')

    def test_wholly_unreadable_chunk_has_no_pdf_letters(self):
        import compositor as c
        rows, script, result, path, reader = self.compose_fixture('rushing speech ...', 'unreadable')
        self.assertEqual(reader.pages[0].extract_text().split(), ['Lettering', 'test', '1'])
        self.assertEqual(c.verify_pdf(path, rows, script, result['placements'])['script_chunks_verified'], 1)

def drawn_fixture(directory, text, reserve, size=(1600, 800), panel=(36, 300, 369, 184.5), style=None):
    """A dark 1600 x 800 frame in a 369 x 184.5 pt slot: 0.2306 pt per source pixel, 312 PPI."""
    from pathlib import Path
    from PIL import Image
    import compositor as c
    image = Path(directory) / 'drawn-frame.png'
    if not image.exists():
        Image.new('RGB', size, (58, 66, 84)).save(image)
    frame_id = 'page-01-panel-01'
    reserve = dict(reserve)
    if style is not None:
        reserve['style'] = style
    rows = [{'id': frame_id, 'path': str(image), 'sha256': c.sha256(image),
             'width': size[0], 'height': size[1], 'visible_rect': [0, 0, size[0], size[1]],
             'reserves': [reserve]}]
    script = {'title': 'Drawn test', 'pages': {'1': {'panels': [
        {'id': frame_id, 'copy': [{'speaker': 'NAGOJI', 'text': text}]}]}}}
    geometry = {'pages': {'1': [{'id': frame_id, 'rect_pt': list(panel)}]}}
    return rows, script, geometry


CAPTION = {'kind': 'caption', 'draw': 'caption', 'rect': [100, 80, 900, 220], 'copy_indices': [0]}
SPEECH = {'kind': 'speech', 'draw': 'speech', 'rect': [500, 180, 1300, 400], 'copy_indices': [0],
          'tail': [750, 760]}


class DrawnReserveTests(unittest.TestCase):
    """The compositor draws captions and balloons itself when a reserve says "draw"."""

    def setUp(self):
        import tempfile
        from pathlib import Path
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def measure(self, rows, script, geometry, reject=True):
        import compositor as c
        from types import SimpleNamespace
        return c.copy_fit_measurements(rows, script, geometry,
            SimpleNamespace(B=SimpleNamespace(measure=c.measure)), reject_failures=reject)

    def compose(self, text, reserve, style=None, name='drawn.pdf'):
        import compositor as c
        from pypdf import PdfReader
        rows, script, geometry = drawn_fixture(self.directory, text, reserve, style=style)
        path = self.directory / name
        result = c.compose(rows, script, geometry, path)
        return rows, script, geometry, result, path, PdfReader(path)

    @staticmethod
    def operations(reader):
        from pypdf.generic import ContentStream
        return [(args, op) for args, op in ContentStream(reader.pages[0].get_contents(), reader).operations]

    def test_drawn_caption_emits_white_rectangle_with_a_point_eight_stroke_and_text_verifies(self):
        import compositor as c
        text = 'When the sea finally spat me out.'
        rows, script, geometry, result, path, reader = self.compose(text, CAPTION)
        shape = result['copy_fit_measurements'][0]['drawn']
        self.assertEqual(shape['draw'], 'caption')
        x, y, w, h = shape['rect_pt']
        operations = self.operations(reader)
        filled = [i for i, (args, op) in enumerate(operations)
                  if op == b're' and all(abs(float(a) - b) < .01 for a, b in zip(args, (x, y, w, h)))]
        self.assertEqual(len(filled), 1)
        self.assertIn(operations[filled[0] + 1][1], (b'B', b'B*'))   # fill and stroke together
        before = operations[:filled[0]]
        self.assertIn(b'w', [op for _, op in before])
        widths = [float(args[0]) for args, op in before if op == b'w']
        self.assertAlmostEqual(widths[-1], .8)
        fills = [tuple(float(a) for a in args) for args, op in before if op == b'rg']
        self.assertEqual(fills[-1], (1.0, 1.0, 1.0))
        strokes = [tuple(float(a) for a in args) for args, op in before if op == b'RG']
        self.assertEqual(strokes[-1], (0.0, 0.0, 0.0))
        self.assertEqual(c.verify_page_chunks(reader.pages[0].extract_text(), [text]), 1)
        self.assertEqual(c.verify_pdf(path, rows, script, result['placements'])['script_chunks_verified'], 1)

    def test_drawn_speech_emits_a_rounded_balloon_and_a_tail(self):
        import compositor as c
        text = 'Look at his hands...'
        rows, script, geometry, result, path, reader = self.compose(text, SPEECH)
        shape = result['copy_fit_measurements'][0]['drawn']
        operations = self.operations(reader)
        ops = [op for _, op in operations]
        self.assertGreaterEqual(ops.count(b'c'), 4)                 # four rounded corners
        tri = shape['tail']['triangle_pt']
        moves = [tuple(float(a) for a in args) for args, op in operations if op == b'm']
        self.assertTrue(any(abs(m[0] - tri[0][0]) < .01 and abs(m[1] - tri[0][1]) < .01 for m in moves))
        lines = [tuple(float(a) for a in args) for args, op in operations if op == b'l']
        tip = shape['tail']['tip_pt']
        self.assertTrue(any(abs(l[0] - tip[0]) < .01 and abs(l[1] - tip[1]) < .01 for l in lines))
        self.assertEqual(c.verify_pdf(path, rows, script, result['placements'])['script_chunks_verified'], 1)
        # The tail is stroked and filled first, then the balloon, then the mouth patch: three painting operators.
        painters = [op for op in ops if op in (b'B', b'B*', b'f', b'f*')]
        self.assertEqual([op in (b'B', b'B*') for op in painters[-3:]], [True, True, False])

    def test_tail_tip_stops_short_of_the_speaker_and_nearer_than_the_balloon_centre(self):
        import compositor as c
        import math
        rect, clip = [100.0, 200.0, 180.0, 40.0], [36.0, 60.0, 369.0, 300.0]
        for target in ([150.0, 90.0], [400.0, 215.0], [60.0, 300.0], [190.0, 355.0]):
            with self.subTest(target=target):
                shape = c._drawn_shape('speech', rect, target, clip)
                tail = shape['tail']
                centre = (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2)
                tip = tail['tip_pt']
                self.assertLess(math.dist(tip, target), math.dist(centre, target))
                self.assertGreater(math.dist(tip, target), 0.5)              # stops short
                self.assertGreaterEqual(tail['length_pt'], 8 - 1e-6)
                self.assertLessEqual(tail['length_pt'], 28 + 1e-6)
                # The tip is outside the balloon and inside the panel clip.
                outside = (tip[0] < rect[0] or tip[0] > rect[0] + rect[2] or
                           tip[1] < rect[1] or tip[1] > rect[1] + rect[3])
                self.assertTrue(outside)
                self.assertTrue(clip[0] <= tip[0] <= clip[0] + clip[2] and clip[1] <= tip[1] <= clip[1] + clip[3])

    def test_tail_length_is_about_sixty_percent_of_the_way_clamped(self):
        import compositor as c
        import math
        rect, clip = [100.0, 200.0, 180.0, 40.0], [0.0, 0.0, 600.0, 600.0]
        near = c._drawn_shape('speech', rect, [190.0, 190.0], clip)['tail']      # 10 pt away: clamped up, then held short
        far = c._drawn_shape('speech', rect, [190.0, 20.0], clip)['tail']        # 180 pt away: clamped down to 28
        mid = c._drawn_shape('speech', rect, [190.0, 150.0], clip)['tail']       # 50 pt away: 30 -> 28
        self.assertAlmostEqual(far['length_pt'], 28.0, places=3)
        self.assertAlmostEqual(mid['length_pt'], 28.0, places=3)
        self.assertLess(near['length_pt'], 10.0)
        self.assertGreater(near['length_pt'], 0)
        between = c._drawn_shape('speech', rect, [190.0, 175.0], clip)['tail']   # 25 pt away: 15 pt
        self.assertAlmostEqual(between['length_pt'], 15.0, places=3)

    def test_text_area_is_the_padded_interior_and_the_fit_check_uses_it(self):
        import compositor as c
        text = 'One long sentence that needs a second line to fit here.'
        narrow = [100, 80, 500, 188]           # 92 x 24.9 pt: two lines fit the box, not its padded interior
        plain = dict(kind='caption', rect=narrow, copy_indices=[0])
        rows, script, geometry = drawn_fixture(self.directory, text, plain)
        undrawn = self.measure(rows, script, geometry, reject=False)[0]
        self.assertTrue(undrawn['fits'])
        rows, script, geometry = drawn_fixture(self.directory, text, dict(CAPTION, rect=narrow))
        drawn = self.measure(rows, script, geometry, reject=False)[0]
        x, y, w, h = drawn['drawn']['rect_pt']
        tx, ty, tw, th = drawn['rect_pt']
        for gap in (tx - x, ty - y, (x + w) - (tx + tw), (y + h) - (ty + th)):
            self.assertGreaterEqual(gap, 5.0 - 1e-6)
        self.assertAlmostEqual(undrawn['rect_pt'][3] - th, 10.0, places=3)
        self.assertGreater(len(drawn['lines']), 1)
        self.assertFalse(drawn['fits'])                    # fits the outer rect, not the padded interior
        with self.assertRaisesRegex(ValueError, 'does not fit'):
            self.measure(rows, script, geometry)

    def test_speech_text_area_clears_the_rounded_corners_by_five_points(self):
        import compositor as c
        import math
        rows, script, geometry = drawn_fixture(self.directory, 'Short.', SPEECH)
        measured = self.measure(rows, script, geometry)[0]
        x, y, w, h = measured['drawn']['rect_pt']
        r = measured['drawn']['radius_pt']
        tx, ty, tw, th = measured['rect_pt']
        self.assertGreater(r, .3 * min(w, h))                       # most of the shorter side
        self.assertLessEqual(r, .5 * min(w, h) + 1e-9)
        corner = (tx, ty)                                             # lower-left corner of the text area
        centre = (x + r, y + r)
        self.assertGreaterEqual(r - math.dist(corner, centre), 5.0 - 1e-6)
        self.assertGreaterEqual(c.drawn_text_inset('speech', w, h), 5.0)
        self.assertEqual(c.drawn_text_inset('caption', w, h), 5.0)

    def test_drawn_box_size_gives_a_shape_whose_padded_interior_fits_the_text(self):
        import compositor as c
        for draw in ('caption', 'speech'):
            for text in ('Short.', 'The sea was no longer alone.',
                         'See the brand on his arm, said the voice, and every head turned.', 'Easy, *bhau*.'):
                with self.subTest(draw=draw, text=text):
                    for wrap in (40.0, 90.0, 160.0):
                        box = c.drawn_box_size(text, draw, wrap)
                        w_pt, h_pt = box['shape_pt']
                        inset = c.drawn_text_inset(draw, w_pt, h_pt)
                        from reportlab.pdfbase import pdfmetrics
                        c._register_fonts()
                        din = pdfmetrics.getFont('Chapter01DIN')
                        interior_w, interior_h = w_pt - 2 * inset, h_pt - 2 * inset
                        lettering = c._wrap_lettering(text, din, c.DIN_SIZE_PT, interior_w - 4.0, None) \
                            if '*' in text else None
                        lines = [''.join(r['text'] for r in l) for l in lettering] if lettering else \
                            c._wrap_text(text, din, c.DIN_SIZE_PT, interior_w - 4.0)
                        self.assertEqual(lines, box['lines'])
                        block = c._measure_copy_block(
                            lines, interior_w, interior_h, c.DIN_SIZE_PT,
                            ink_bounds=[c._lettering_bounds(l) for l in lettering] if lettering else None)
                        self.assertTrue(block['fits'])

    def test_invalid_draw_and_tail_fields_are_rejected(self):
        import compositor as c
        rows, script, geometry = drawn_fixture(self.directory, 'Plain.', CAPTION)
        for value in ('balloon', '', None, 3):
            rows[0]['reserves'][0]['draw'] = value
            with self.subTest(draw=value):
                with self.assertRaisesRegex(ValueError, 'draw'):
                    c.validate_copy_runs(script, rows)
                with self.assertRaisesRegex(ValueError, 'draw'):
                    self.measure(rows, script, geometry)
        rows[0]['reserves'][0].update(draw='caption', tail=[10, 10])
        with self.assertRaisesRegex(ValueError, 'tail'):
            c.validate_copy_runs(script, rows)
        rows[0]['reserves'][0].update(draw='speech')
        for bad in ([1], [1, 2, 3], ['a', 2], [float('nan'), 1], 'x', [True, 2]):
            rows[0]['reserves'][0]['tail'] = bad
            with self.subTest(tail=bad), self.assertRaisesRegex(ValueError, 'tail'):
                c.validate_copy_runs(script, rows)
        rows[0]['reserves'][0]['tail'] = [500, 150]              # inside the balloon
        with self.assertRaisesRegex(ValueError, 'inside'):
            self.measure(rows, script, geometry)
        del rows[0]['reserves'][0]['tail']
        rows[0]['reserves'][0]['rect'] = [10, 10, 1700, 90]        # beyond the visible art
        with self.assertRaisesRegex(ValueError, 'visible'):
            self.measure(rows, script, geometry)

    def test_a_speech_reserve_without_a_tail_draws_a_plain_balloon(self):
        rows, script, geometry, result, path, reader = self.compose(
            'Plain.', {k: v for k, v in SPEECH.items() if k != 'tail'})
        self.assertIsNone(result['copy_fit_measurements'][0]['drawn']['tail'])

    def test_italic_and_unreadable_lettering_work_inside_drawn_reserves(self):
        import compositor as c
        marked = 'Easy, *bhau*. You are on land now.'
        rows, script, geometry, result, path, reader = self.compose(marked, CAPTION)
        self.assertEqual(c.verify_page_chunks(reader.pages[0].extract_text(), [marked]), 1)
        self.assertEqual(c.verify_pdf(path, rows, script, result['placements'])['status'], 'pass')
        text = '... *kapitan* ... *kapitan* ...'
        rows, script, geometry, result, path, reader = self.compose(text, SPEECH, style='unreadable', name='u.pdf')
        self.assertEqual(c.verify_pdf(path, rows, script, result['placements'])['script_chunks_verified'], 1)
        self.assertIn('kapitan', reader.pages[0].extract_text())

    def test_page_without_draw_fields_is_byte_identical_to_the_previous_compositor(self):
        import compositor as c
        from importlib.machinery import SourceFileLoader
        from importlib.util import module_from_spec, spec_from_loader
        from pathlib import Path
        backup = Path(c.__file__).parent / 'review/compositor.py.backup-pre-drawn-balloons'
        loader = SourceFileLoader('pre_drawn_compositor', str(backup))
        old = module_from_spec(spec_from_loader(loader.name, loader))
        loader.exec_module(old)
        cases = [('Easy, bhau. You are on land now.', None), ('Easy, *bhau*. You are on land now.', None),
                 ('... *kapitan* ...', 'unreadable')]
        for index, (text, style) in enumerate(cases):
            with self.subTest(text=text):
                rows, script, geometry = lettering_fixture(self.directory, text, style)
                before, after = self.directory / f'before{index}.pdf', self.directory / f'after{index}.pdf'
                old_result = old.compose(rows, script, geometry, before)
                new_result = c.compose(rows, script, geometry, after)
                self.assertEqual(before.read_bytes(), after.read_bytes())
                self.assertEqual(old_result, new_result)
        self.assertEqual(old.scaled_row(rows[0], 1200, 600), c.scaled_row(rows[0], 1200, 600))

    def test_scaling_a_row_scales_the_tail_point_and_keeps_draw(self):
        import compositor as c
        rows, script, geometry = drawn_fixture(self.directory, 'Plain.', SPEECH)
        scaled = c.scaled_row(rows[0], 3200, 1600)
        reserve = scaled['reserves'][0]
        self.assertEqual(reserve['tail'], [1500, 1520])
        self.assertEqual(reserve['draw'], 'speech')
        self.assertEqual(reserve['rect'], [1000, 360, 2600, 800])
        self.assertEqual(rows[0]['reserves'][0]['tail'], [750, 760])

    def test_a_tail_target_on_the_frame_edge_draws_no_tail_when_the_balloon_touches_that_edge(self):
        import compositor as c
        touching = {'kind': 'speech', 'draw': 'speech', 'rect': [500, 0, 1300, 220], 'copy_indices': [0],
                    'tail': [900, 0]}                                   # the speaker is above the frame
        rows, script, geometry, result, path, reader = self.compose('Look.', touching)
        self.assertIsNone(result['copy_fit_measurements'][0]['drawn']['tail'])
        self.assertEqual(c.verify_pdf(path, rows, script, result['placements'])['script_chunks_verified'], 1)
        for edge in ([0, 100], [1600, 100], [900, 800], [900, -30]):
            with self.subTest(target=edge):
                inside_by_clamp = {'kind': 'speech', 'draw': 'speech', 'rect': [0, 0, 1600, 800],
                                   'copy_indices': [0], 'tail': edge}
                rows, script, geometry = drawn_fixture(self.directory, 'Look.', inside_by_clamp)
                self.assertIsNone(self.measure(rows, script, geometry, reject=False)[0]['drawn']['tail'])

    def test_a_tail_target_on_the_frame_edge_points_to_that_edge_when_there_is_room(self):
        import math
        rows, script, geometry = drawn_fixture(self.directory, 'Look.', dict(SPEECH, rect=[500, 100, 1300, 320], tail=[900, 0]))
        shape = self.measure(rows, script, geometry)[0]['drawn']
        tail = shape['tail']
        self.assertIsNotNone(tail)
        x, y, w, h = shape['rect_pt']
        self.assertGreater(tail['tip_pt'][1], y + h)                    # leaves through the top edge, upward
        self.assertLess(math.dist(tail['tip_pt'], tail['target_pt']), math.dist((x + w / 2, y + h / 2), tail['target_pt']))
        self.assertGreaterEqual(tail['length_pt'], 1.0)

    def test_a_tail_to_an_off_panel_speaker_runs_to_the_panel_border(self):
        # Chapter 1 r12, 3.1: a voice off the right edge had a tail that stopped 60 percent of the way there, on the man
        # between the balloon and the edge, so the line read as his. A tail to an off-panel speaker reaches the border.
        import math
        rows, script, geometry = drawn_fixture(self.directory, 'Look.', dict(SPEECH, rect=[100, 300, 700, 500], tail=[1600, 400]))
        tail = self.measure(rows, script, geometry)[0]['drawn']['tail']
        self.assertLess(math.dist(tail['tip_pt'], tail['target_pt']), .5)        # the tip is at the clamped border point
        rows, script, geometry = drawn_fixture(self.directory, 'Look.', dict(SPEECH, rect=[100, 300, 700, 500], tail=[1300, 400]))
        inside = self.measure(rows, script, geometry)[0]['drawn']['tail']
        self.assertGreater(math.dist(inside['tip_pt'], inside['target_pt']), 5)   # a mouth inside the panel: stops short, as before

    def test_an_interior_tail_point_inside_its_balloon_is_still_rejected(self):
        rows, script, geometry = drawn_fixture(self.directory, 'Look.', dict(SPEECH, tail=[900, 300]))
        with self.assertRaisesRegex(ValueError, 'inside'):
            self.measure(rows, script, geometry)

    def test_corner_sets_the_balloon_radius_and_shrinks_the_text_inset(self):
        import compositor as c
        rows, script, geometry = drawn_fixture(self.directory, 'Short.', SPEECH)
        default = self.measure(rows, script, geometry)[0]['drawn']
        rows, script, geometry = drawn_fixture(self.directory, 'Short.', dict(SPEECH, corner=.40))
        measured = self.measure(rows, script, geometry)[0]
        shape = measured['drawn']
        x, y, w, h = shape['rect_pt']
        self.assertAlmostEqual(shape['radius_pt'], .40 * min(w, h))
        self.assertAlmostEqual(shape['corner'], .40)
        self.assertAlmostEqual(default['radius_pt'], .45 * min(w, h))
        self.assertLess(c.drawn_text_inset('speech', w, h, .40), c.drawn_text_inset('speech', w, h))
        # The text area still clears the rounded corners by at least 5 pt.
        import math
        tx, ty, tw, th = measured['rect_pt']
        self.assertGreaterEqual(shape['radius_pt'] - math.dist((tx, ty), (x + shape['radius_pt'], y + shape['radius_pt'])), 5.0 - 1e-6)
        self.assertLess(c.drawn_box_size('Short.', 'speech', 60.0, corner=.40)['shape_pt'][0],
                        c.drawn_box_size('Short.', 'speech', 60.0)['shape_pt'][0] + 1e-9)

    def test_corner_is_validated(self):
        import compositor as c
        rows, script, geometry = drawn_fixture(self.directory, 'Short.', SPEECH)
        for good in (.40, .45, .5):
            rows[0]['reserves'][0]['corner'] = good
            c.validate_copy_runs(script, rows)
        for bad in (.39, .51, 0, 'x', True, None, [.4]):
            rows[0]['reserves'][0]['corner'] = bad
            with self.subTest(corner=bad), self.assertRaisesRegex(ValueError, 'corner'):
                c.validate_copy_runs(script, rows)
        rows, script, geometry = drawn_fixture(self.directory, 'Short.', dict(CAPTION, corner=.4))
        with self.assertRaisesRegex(ValueError, 'corner'):
            c.validate_copy_runs(script, rows)

    def test_an_explicit_default_corner_draws_exactly_what_no_corner_draws(self):
        import compositor as c
        outputs = []
        for index, reserve in enumerate((SPEECH, dict(SPEECH, corner=.45))):
            rows, script, geometry = drawn_fixture(self.directory, 'Look at his hands.', reserve)
            path = self.directory / f'corner{index}.pdf'
            c.compose(rows, script, geometry, path)
            outputs.append(path.read_bytes())
        self.assertEqual(outputs[0], outputs[1])

    def test_scaling_a_row_keeps_the_corner(self):
        import compositor as c
        rows, script, geometry = drawn_fixture(self.directory, 'Short.', dict(SPEECH, corner=.4))
        self.assertEqual(c.scaled_row(rows[0], 3200, 1600)['reserves'][0]['corner'], .4)

    def render_page(self, name, rows, script, geometry, dpi=200):
        import subprocess
        import numpy as np
        import compositor as c
        import shutil
        from pathlib import Path
        from PIL import Image
        tool = shutil.which('pdftoppm') or str(Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm')
        if not Path(tool).exists():
            self.skipTest('pdftoppm is not available')
        pdf = self.directory / f'{name}.pdf'
        c.compose(rows, script, geometry, pdf)
        subprocess.run([tool, '-png', '-singlefile', '-r', str(dpi), str(pdf), str(self.directory / name)], check=True)
        with Image.open(self.directory / f'{name}.png') as image:
            return np.asarray(image.convert('RGB')).astype(int)

    def test_a_balloon_may_bleed_past_the_visible_edge_while_its_padded_text_area_stays_inside(self):
        import compositor as c
        # The visible top edge is at page y = 300 + 184.5. The balloon's corner clearance is about 7.3 pt.
        bleeding = dict(SPEECH, rect=[500, -20, 1300, 220])            # 20 px = 4.6 pt above the frame
        rows, script, geometry = drawn_fixture(self.directory, 'Look at his hands.', bleeding)
        measured = self.measure(rows, script, geometry)[0]
        x, y, w, h = measured['drawn']['rect_pt']
        self.assertGreater(y + h, 484.5)                               # the shape runs past the visible edge
        tx, ty, tw, th = measured['rect_pt']
        self.assertLessEqual(ty + th + c.DRAW_PAD_PT, 484.5 + 1e-6)    # the text area and its padding do not
        too_far = dict(SPEECH, rect=[500, -60, 1300, 220])             # 13.8 pt: the padded text area would leave
        rows, script, geometry = drawn_fixture(self.directory, 'Look at his hands.', too_far)
        with self.assertRaisesRegex(ValueError, 'visible'):
            self.measure(rows, script, geometry)

    def test_a_text_area_outside_the_visible_art_still_fails(self):
        for rect in ([1500, 100, 2300, 400], [-900, 100, 100, 400], [200, 700, 1000, 1200]):
            with self.subTest(rect=rect):
                rows, script, geometry = drawn_fixture(self.directory, 'Look.', dict(SPEECH, rect=rect, tail=[800, 790]))
                with self.assertRaisesRegex(ValueError, 'visible'):
                    self.measure(rows, script, geometry)

    def test_a_caption_has_no_spare_room_to_bleed(self):
        # A caption's text area plus its padding is the whole rectangle, so it cannot run off an edge.
        rows, script, geometry = drawn_fixture(self.directory, 'Short.', dict(CAPTION, rect=[100, -10, 900, 220]))
        with self.assertRaisesRegex(ValueError, 'visible'):
            self.measure(rows, script, geometry)
        rows, script, geometry = drawn_fixture(self.directory, 'Short.', dict(CAPTION, rect=[0, 0, 900, 220]))
        self.measure(rows, script, geometry)                            # flush with the edge is fine

    def test_the_clipped_balloon_is_cut_at_the_panel_edge_and_the_border_is_drawn_over_it(self):
        import numpy as np
        bleeding = dict(SPEECH, rect=[500, -20, 1300, 220])
        rows, script, geometry = drawn_fixture(self.directory, 'Look at his hands.', bleeding)
        page = self.render_page('bleed', rows, script, geometry)
        scale = 200 / 72
        top = int(round((666 - 484.5) * scale))                        # the panel's top edge, in page pixels
        column = int(round((36 + 369 * .5) * scale))                   # the middle of the balloon
        background = np.array([247, 240, 222])
        above = page[top - 8:top - 3, column]
        self.assertTrue((np.abs(above - background).max(axis=1) <= 4).all())     # nothing painted outside the panel
        border = page[top - 2:top + 3, column]
        self.assertTrue((border.max(axis=1) < 90).any())                         # the border stroke is drawn over the cut
        below = page[top + 6:top + 12, column]
        self.assertGreater(below.min(), 200)                                     # the balloon's white fill just inside

    def test_a_page_whose_shapes_are_inside_the_frame_is_byte_identical_to_the_previous_compositor(self):
        import compositor as c
        from importlib.machinery import SourceFileLoader
        from importlib.util import module_from_spec, spec_from_loader
        from pathlib import Path
        backup = Path(c.__file__).parent / 'review/compositor.py.backup-pre-edge-bleed'
        loader = SourceFileLoader('pre_edge_bleed_compositor', str(backup))
        old = module_from_spec(spec_from_loader(loader.name, loader))
        loader.exec_module(old)
        for index, reserve in enumerate((SPEECH, CAPTION, dict(SPEECH, corner=.40), dict(SPEECH, rect=[0, 0, 900, 240]))):
            with self.subTest(reserve=reserve):
                rows, script, geometry = drawn_fixture(self.directory, 'Look at his hands.', reserve)
                before, after = self.directory / f'pre{index}.pdf', self.directory / f'post{index}.pdf'
                old.compose(rows, script, geometry, before)
                c.compose(rows, script, geometry, after)
                self.assertEqual(before.read_bytes(), after.read_bytes())

    def test_drawn_shapes_are_clipped_to_the_panel(self):
        # A balloon that reaches the panel edge must not paint outside the panel clip.
        rows, script, geometry, result, path, reader = self.compose(
            'Short.', {'kind': 'speech', 'draw': 'speech', 'rect': [0, 0, 800, 240], 'copy_indices': [0],
                       'tail': [1590, 790]})
        operations = self.operations(reader)
        ops = [op for _, op in operations]
        first_shape = next(i for i, (args, op) in enumerate(operations) if op == b'c')
        clipped_before = [op for op in ops[:first_shape] if op == b'W' or op == b'W*']
        self.assertGreaterEqual(len(clipped_before), 2)   # the image clip, then the drawn-shape clip


if __name__ == '__main__':
    unittest.main()
