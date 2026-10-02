#!/usr/bin/env python3
"""Re-balance a chapter's row heights for the lettering each panel carries.

LAYOUT.json row heights are drawn before any text is measured, so a strip that carries two
or three speech lines can be left with no clear area for its balloons. fit_layout keeps the
prior layout's row STRUCTURE (which panels share a row) and moves height between the rows of
each page so that, in this order of priority:

1. every page still totals exactly 523.5 pt including the 2 pt gaps, in whole tenths of a point;
2. each row's lettering load fits with margin: the ratio of a panel's usable area (its placed
   clip, minus its face zones) to the area of the padded balloons and captions its chunks need at
   the real 8.5 pt DIN wrap. The placed clip models the planner: the frame's art (its visible_rect
   here, the uncropped art rect) is first cropped toward the slot's shape by reserves.cover_crop,
   keeping every face zone, every painted region the balloons must hide, every story keep zone and
   at least MIN_KEEP of the art's height or width, and what remains is aspect-fitted in the slot.
   The page's minimum ratio is maximised, and pursued only up to `margin`;
3. rows whose art cannot span the column (a height-limited frame, or one the crop could not reach)
   are given the smallest height at which the cropped art spans the column, where the page budget
   allows, evening out the fill (the share of each slot's area that its art covers: a panel letterboxed above
   and below in a tall slot counts as under-filled, as one with bars at the sides does);
4. any budget left goes to the lowest ratios that can still improve, then is spread over the
   rows that have headroom.

Bounds: a row never drops below 55 pt or below 60 percent of its prior height (a silent row may
drop to 55 pt), and never grows beyond twice its prior height. A page whose load cannot fit
inside the bounds is reported (status "cannot_fit" or "tight"); the bounds are never violated.

The ratio is an area proxy: it cannot see tail keep-outs, painted regions or how a face sits in
the clip. `floors` and `ceilings` let a caller that has asked the placement planner (see
run_chapter.probe_fit) add what it proved: a row is never given less than its floor or more than
its ceiling (within the bounds above), and the ratio fit works in the room that is left.

fit_structures goes one step further and chooses each page's row STRUCTURE too (see its docstring): every way to
group the page's panels, in reading order, into rows of one or two is fitted as above, filtered by the layout cues in
the panels' script descriptions (layout_cues), and ranked by lettering, then by how well the art fills its slots (by area, see _Panel.fill).
"""
from __future__ import annotations
import bisect
import functools
import math
import re
import compositor as c
from reserves import MIN_KEEP, cover_crop     # MIN_KEEP (the crop's floor) is re-exported for callers and reports

MIN_ROW_PT = 55.0
MIN_SHARE = 0.6
MAX_GROWTH = 2.0
MARGIN = 3.0            # usable area over needed area that a row is fitted to reach
WRAP_SHARE = 0.36       # the planner's first wrap width, as a share of the clip width
WRAP_STEP_PT = 2.0      # wrap widths are quantised to this for the cached box measurements
TENTHS = 10
PAGE_TENTHS = round(c.STORY_HEIGHT_PT * TENTHS)
GAP_TENTHS = round(c.GAP_PT * TENTHS)
FACE_CAP = 0.9          # faces never take more than this share of a frame
ROW_SIZES = (1, 2)      # panels per row that the structure search tries (rows of three are not tried)
PROBE_TOP = 3           # candidates per page that fit_structures hands to its refine hook (the planner probe)
CUE_SHARE = 0.9         # a size cue floors its row at this fraction of the share of the page it names
CUE_HEAD_WORDS = 6      # strip, tier and splash are layout cues only among a description's first words
SPAN_SHARE = 0.95       # a full-width cue floors its row where the art spans this share of the column


def _draw_kind(speaker):
    return 'caption' if speaker.strip().upper().startswith('CAPTION') else 'speech'


@functools.lru_cache(maxsize=None)
def _box_area(text, kind, wrap_pt):
    width, height = c.drawn_box_size(text, kind, wrap_pt)['shape_pt']
    return width * height


def _disc_in_rect(cx, cy, radius, rect, slices=48):
    """Area of a disc inside a rectangle, by thin vertical slices."""
    x0, y0, x1, y1 = rect
    left, right = max(cx - radius, x0), min(cx + radius, x1)
    if right <= left:
        return 0.0
    step = (right - left) / slices
    area = 0.0
    for index in range(slices):
        x = left + (index + .5) * step
        half = math.sqrt(max(0.0, radius * radius - (x - cx) ** 2))
        top, bottom = min(cy + half, y1), max(cy - half, y0)
        if top > bottom:
            area += (top - bottom) * step
    return area


class _Panel:
    """One panel's usable area and lettering need as a function of its row height."""

    def __init__(self, panel, width_pt, frame, faces, painted=None, keep=None):
        self.id = panel['id']
        self.width = width_pt
        self.chunks = [(chunk['text'], _draw_kind(chunk['speaker'])) for chunk in panel.get('copy') or []]
        self.silent = not self.chunks
        self.aspect = None
        self.face_share = 0.0
        self.face_area = 0.0
        self.visible = None
        self.keep = []                 # the crop must keep each face zone's bounding box, painted region and keep zone
        self._shapes = {}
        if frame:
            x0, y0, x1, y1 = frame['visible_rect']
            self.visible = [x0, y0, x1, y1]
            self.aspect = (x1 - x0) / (y1 - y0)
            zones = [(x * frame['width'], y * frame['height'], r * frame['height']) for x, y, r in faces or []]
            self.face_area = sum(_disc_in_rect(cx, cy, radius, (x0, y0, x1, y1)) for cx, cy, radius in zones)
            self.face_share = min(FACE_CAP, self.face_area / ((x1 - x0) * (y1 - y0)))
            self.keep = [[cx - radius, cy - radius, cx + radius, cy + radius] for cx, cy, radius in zones]
            self.keep += [[fx0 * frame['width'], fy0 * frame['height'], fx1 * frame['width'], fy1 * frame['height']]
                          for fx0, fy0, fx1, fy1 in list(painted or []) + list(keep or [])]

    def _shape(self, height_pt):
        """(clip width, clip height, face share of what the crop shows) at a row height, for a panel with a frame."""
        shape = self._shapes.get(height_pt)
        if shape is None:
            width = self.width
            slot = width / height_pt
            x0, y0, x1, y1 = cover_crop(self.visible, slot, self.keep)
            art = (x1 - x0) / (y1 - y0)
            if abs(art / slot - 1.0) <= .02:
                clip = (width, height_pt)
            elif art > slot:
                clip = (width, width / art)
            else:
                clip = (height_pt * art, height_pt)
            shape = self._shapes[height_pt] = (*clip, min(FACE_CAP, self.face_area / ((x1 - x0) * (y1 - y0))))
        return shape

    def clip(self, height_pt):
        """The placed clip (width, height): the art cropped toward the slot (reserves.cover_crop, which keeps every
        face zone and MIN_KEEP of the art), then compositor.fit_clip_contain's aspect-fit of that, without distortion."""
        if self.aspect is None:
            return self.width, height_pt
        return self._shape(height_pt)[:2]

    def fill(self, height_pt):
        """Share of the slot's area (the column's width times the row's height) that the placed clip covers, or None when
        there is no frame. A clip that spans the column but is shorter than the row (a 3:2 frame that cannot be narrowed,
        in a tall half-width slot) leaves cream above and below, and counts for less than 1."""
        if self.aspect is None:
            return None
        clip_w, clip_h = self.clip(height_pt)
        return (clip_w / self.width) * (clip_h / height_pt)

    def fill_width(self, height_pt):
        """Share of the column width the art spans, or None when there is no frame (what fill was before it counted area)."""
        return None if self.aspect is None else self.clip(height_pt)[0] / self.width

    def fill_height(self):
        """The smallest row height (pt) at which the cropped art spans the column, or 0 when there is no frame."""
        if self.aspect is None:
            return 0.0
        x0, y0, x1, y1 = cover_crop(self.visible, math.inf, self.keep)     # the tightest crop the keep rects allow
        return self.width * (y1 - y0) / (x1 - x0)

    def usable(self, height_pt):
        clip_w, clip_h = self.clip(height_pt)
        share = self.face_share if self.aspect is None else self._shape(height_pt)[2]
        return clip_w * clip_h * (1.0 - share)

    def need(self, height_pt):
        clip_w, _ = self.clip(height_pt)
        wrap = max(WRAP_STEP_PT, round(WRAP_SHARE * clip_w / WRAP_STEP_PT) * WRAP_STEP_PT)
        return sum(_box_area(text, kind, wrap) for text, kind in self.chunks)

    def ratio(self, height_pt):
        return math.inf if self.silent else self.usable(height_pt) / self.need(height_pt)


class _Row:
    def __init__(self, panels, prior_tenths, floor_tenths=0, ceiling_tenths=None, cue_tenths=0):
        self.panels = panels
        self.prior = prior_tenths
        self.silent = all(panel.silent for panel in panels)
        prior_pt = prior_tenths / TENTHS
        bound_pt = min(MIN_ROW_PT, prior_pt) if self.silent else max(MIN_SHARE * prior_pt, min(MIN_ROW_PT, prior_pt))
        self.bound = min(prior_tenths, math.ceil(round(bound_pt * TENTHS, 6)))     # the lower bound of the brief
        self.hi = math.floor(round(MAX_GROWTH * prior_tenths, 6))
        if ceiling_tenths is not None:
            self.hi = max(self.bound, min(self.hi, ceiling_tenths))               # a probed height it must not pass
        self.floor = floor_tenths                                                # a height a planner probe has proved
        self.cue = cue_tenths                                                    # a height the script's size cue asks for
        self.lo = self.wanted = min(self.hi, max(self.bound, floor_tenths, cue_tenths))
        self.fill_tenths = math.ceil(round(max(p.fill_height() for p in panels) * TENTHS, 6))
        self._curve = None

    def raw(self, tenths):
        return min(panel.ratio(tenths / TENTHS) for panel in self.panels)

    @property
    def curve(self):
        """Best ratio reached at or below each height from lo to hi (non-decreasing)."""
        if self._curve is None:
            best, curve = 0.0, []
            for tenths in range(self.lo, self.hi + 1):
                best = max(best, self.raw(tenths))
                curve.append(best)
            self._curve = curve
        return self._curve

    def level(self, tenths):
        return math.inf if self.silent else self.curve[tenths - self.lo]

    def minimal(self, target):
        """The smallest height within the bounds whose ratio reaches `target`, or None."""
        if self.silent or target <= self.curve[0]:
            return self.lo
        index = bisect.bisect_left(self.curve, target)
        return None if index == len(self.curve) else self.lo + index


def _ceil_div(numerator, denominator):
    return -(-numerator // denominator)


def _raise_to_ratio(rows, budget, margin):
    """Smallest heights reaching the highest feasible ratio up to `margin`: (heights, ratio)."""
    def heights_for(target):
        chosen = [row.minimal(target) for row in rows]
        return None if None in chosen or sum(chosen) > budget else chosen
    if (chosen := heights_for(margin)) is not None:
        return chosen, margin
    low, high = 0.0, margin
    best = heights_for(low)
    for _ in range(60):
        middle = (low + high) / 2
        attempt = heights_for(middle)
        if attempt is None:
            high = middle
        else:
            low, best = middle, attempt
    return best, low


def _fill_columns(rows, heights, budget):
    """Raise rows toward the height that makes their art span the column, evenly, within the budget."""
    def heights_for(share):
        return [max(h, min(row.hi, _ceil_div(round(share * row.fill_tenths * 1000), 1000)))
                if row.fill_tenths else h for row, h in zip(rows, heights)]
    if sum(heights_for(1.0)) <= budget:
        return heights_for(1.0)
    low, high = 0.0, 1.0
    for _ in range(40):
        middle = (low + high) / 2
        if sum(heights_for(middle)) <= budget:
            low = middle
        else:
            high = middle
    return heights_for(low)


def _spend_on_ratio(rows, heights, leftover, below=math.inf):
    """Give leftover height to the lowest ratios (under `below`) whose ratio it can still improve."""
    while leftover > 0:
        for index in sorted(range(len(rows)), key=lambda i: (rows[i].level(heights[i]), i)):
            row, h = rows[index], heights[index]
            if row.silent or h >= row.hi or row.level(h) >= below:
                continue
            current = row.level(h)
            reach = min(row.hi, h + leftover)
            target = next((t for t in range(h + 1, reach + 1) if row.level(t) > current + 1e-12), None)
            if target is not None:
                leftover -= target - h
                heights[index] = target
                break
        else:
            break
    return leftover


def _spread(rows, heights, leftover):
    """Spread what is left over the rows with headroom, in proportion to their prior heights."""
    while leftover > 0:
        room = [i for i, row in enumerate(rows) if heights[i] < row.hi]
        if not room:
            break
        total = sum(rows[i].prior for i in room)
        gave = 0
        for i in room:
            share = min(rows[i].hi - heights[i], leftover * rows[i].prior // total)
            heights[i] += share
            gave += share
        if gave == 0:                       # fewer tenths than rows: one each, largest prior first
            for i in sorted(room, key=lambda i: (-rows[i].prior, i))[:leftover]:
                heights[i] += 1
                gave += 1
        leftover -= gave
    return leftover


def _fit_heights(rows, budget, margin):
    heights, _ = _raise_to_ratio(rows, budget, margin)
    # A ratio that a wrap breakpoint holds flat is climbed first, with what the maximin left over.
    _spend_on_ratio(rows, heights, budget - sum(heights), below=margin)
    heights = _fill_columns(rows, heights, budget)
    leftover = _spend_on_ratio(rows, heights, budget - sum(heights))
    _spread(rows, heights, leftover)
    return heights


def _relax_floors(rows, budget):
    """Floors that total more than the page: give each row back a share of what it holds above its bound."""
    excess = sum(row.lo for row in rows) - budget
    if excess <= 0:
        return
    held = [row.lo - row.bound for row in rows]
    cuts = [excess * h // sum(held) for h in held]
    for index in sorted(range(len(rows)), key=lambda i: (-(held[i] - cuts[i]), i))[:excess - sum(cuts)]:
        cuts[index] += 1
    for row, cut in zip(rows, cuts):
        row.lo -= cut


def _number(tenths):
    return tenths // TENTHS if tenths % TENTHS == 0 else tenths / TENTHS


def _prior_structure(page_no, panel_ids, raw):
    """Rows as lists of panel indexes and heights in tenths, refusing a layout geometry_for_script would."""
    count = len(panel_ids)
    if raw is None:                                        # no prior rows: one full-width row per panel
        budget = PAGE_TENTHS - GAP_TENTHS * (count - 1)
        base, extra = divmod(budget, count)
        return [[index] for index in range(count)], [base + (1 if index < extra else 0) for index in range(count)]
    expanded = [row if isinstance(row, (list, tuple)) else [row] for row in raw]
    if sum(len(row) for row in expanded) != count:
        raise ValueError(f'Layout panel count differs on page {page_no}')
    if any(not row or min(row) <= 0 or len(set(row)) != 1 for row in expanded):
        raise ValueError(f'Page {page_no}: each row must have a positive common height')
    total = sum(row[0] for row in expanded) + c.GAP_PT * (len(expanded) - 1)
    if abs(total - c.STORY_HEIGHT_PT) > 0.01:
        raise ValueError(f'Layout heights do not fill page {page_no}')
    structure, cursor = [], 0
    for row in expanded:
        structure.append(list(range(cursor, cursor + len(row))))
        cursor += len(row)
    return structure, [round(row[0] * TENTHS) for row in expanded]


def _round(value):
    return None if value is None or math.isinf(value) else round(value, 2)


def _build_rows(page_no, page, raw, frames, faces, floors, ceilings=None, painted=None, keep=None, minimums=None, cache=None):
    """The page's rows as _Row objects, their prior heights in tenths, and the page budget in tenths.

    `minimums` maps a panel id to a height in points its row should have (a script size cue, not a proved floor).
    `cache`, a dict the caller keeps, holds each panel at each slot width so that candidate structures share their work.
    """
    structure, prior = _prior_structure(page_no, [panel['id'] for panel in page['panels']], raw)
    rows = []
    for members, height in zip(structure, prior):
        width = (c.ART_WIDTH_PT - c.GAP_PT * (len(members) - 1)) / len(members)
        panels = []
        for index in members:
            panel = None if cache is None else cache.get((index, width))
            if panel is None:
                spec = page['panels'][index]
                panel = _Panel(spec, width, frames.get(spec['id']), faces.get(spec['id']),
                               (painted or {}).get(spec['id']), (keep or {}).get(spec['id']))
                if cache is not None:
                    cache[(index, width)] = panel
            panels.append(panel)
        floor = max((floors.get(panel.id, 0) for panel in panels), default=0)
        cue = max((minimums.get(panel.id, 0) for panel in panels), default=0) if minimums else 0
        caps = [ceilings[panel.id] for panel in panels if panel.id in (ceilings or {})]
        rows.append(_Row(panels, height, math.ceil(round(floor * TENTHS, 6)),
                         math.floor(round(min(caps) * TENTHS, 6)) if caps else None, math.ceil(round(cue * TENTHS, 6))))
    return rows, prior, PAGE_TENTHS - GAP_TENTHS * (len(rows) - 1)


def structure(script, prior_rows):
    """Each page's rows with their panels, slot width and bounds in points, as fit_layout would fit them."""
    layout = {}
    for page_no, page in script['pages'].items():
        rows, _, _ = _build_rows(page_no, page, (prior_rows or {}).get(str(page_no)), {}, {}, {})
        layout[str(page_no)] = [{'panels': [panel.id for panel in row.panels], 'width_pt': row.panels[0].width,
                                 'prior_pt': _number(row.prior), 'min_pt': _number(row.bound),
                                 'max_pt': _number(row.hi), 'silent': row.silent} for row in rows]
    return layout


def _page_report(rows, prior, new, margin, dense, budget):
    """Per panel and per row ratios and fills before and after, plus the page's status."""
    by_panel = {}
    row_reports = []
    for row, before, after in zip(rows, prior, new):
        for panel in row.panels:
            by_panel[panel.id] = {
                'frame': 'none' if panel.aspect is None else 'given',
                'faces_share': round(panel.face_share, 3),
                'ratio_before': _round(panel.ratio(before / TENTHS)),
                'ratio_after': _round(panel.ratio(after / TENTHS)),
                'fill_before': _round(panel.fill(before / TENTHS)),
                'fill_after': _round(panel.fill(after / TENTHS)),
                'fill_width_before': _round(panel.fill_width(before / TENTHS)),
                'fill_width_after': _round(panel.fill_width(after / TENTHS)),
                'usable_pt2_after': round(panel.usable(after / TENTHS)),
                'needed_pt2_after': round(panel.need(after / TENTHS))}
        report = {'panels': [panel.id for panel in row.panels], 'silent': row.silent,
                  'prior_pt': _number(before), 'new_pt': _number(after),
                  'min_pt': _number(row.bound), 'max_pt': _number(row.hi),
                  'ratio_before': _round(row.raw(before)), 'ratio_after': _round(row.raw(after))}
        if row.floor:
            report.update({'floor_pt': _number(row.floor), 'floor_met': after >= row.floor})
        if row.cue:
            report.update({'cue_min_pt': _number(row.cue), 'cue_met': after >= row.cue})
        row_reports.append(report)
    before = min(row.raw(h) for row, h in zip(rows, prior))
    after_values = [row.raw(h) for row, h in zip(rows, new)]
    after = min(after_values)
    status, reason = 'ok', None
    short = [i for i, row in enumerate(rows) if row.floor and new[i] < row.floor]
    if short:                                                # a probed floor the page cannot give
        status = 'cannot_fit'
        names = '; '.join(f'{" and ".join(panel.id for panel in rows[i].panels)} needs {_number(rows[i].floor)} pt, '
                          f'gets {_number(new[i])} pt' for i in short)
        why = ('above the most its row may grow' if any(rows[i].floor > rows[i].hi for i in short)
               else f'the floors total {_number(sum(row.wanted for row in rows))} pt against {_number(budget)} pt to share')
        reason = f'probed floor not met: {names} ({why})'
    else:
        judged = [value for row, value in zip(rows, after_values) if not row.floor]    # a met floor is proof enough
        worst_value = min(judged, default=math.inf)
        if not math.isinf(worst_value) and worst_value < margin:
            worst = next(i for i, row in enumerate(rows) if not row.floor and after_values[i] == worst_value)
            row = rows[worst]
            status = 'cannot_fit' if worst_value < 1.0 else 'tight'
            reason = (f'{" and ".join(panel.id for panel in row.panels)}: ratio {worst_value:.2f} at {_number(new[worst])} pt'
                      f' ({"its upper bound" if new[worst] >= row.hi else "all the height this page can spare"}),'
                      f' below the margin {margin:g}'
                      + ('; its lettering needs more area than the panel has' if status == 'cannot_fit' else ''))
    page = {'status': status, 'min_ratio_before': _round(before), 'min_ratio_after': _round(after),
            'rows': row_reports, 'panels': by_panel}
    if dense:
        page['default_rows'] = True
    if reason:
        page['reason'] = reason
    return page


def _solve(page_no, rows, budget, margin):
    """The heights in tenths that fit_layout gives built rows, with its checks."""
    if sum(row.bound for row in rows) > budget or sum(row.hi for row in rows) < budget:
        raise ValueError(f'Page {page_no}: the bounds leave no way to fill the page')
    _relax_floors(rows, budget)
    new = _fit_heights(rows, budget, margin)
    if sum(new) != budget or any(not row.lo <= h <= row.hi for row, h in zip(rows, new)):
        raise ValueError(f'Page {page_no}: the fit broke its own bounds')
    return new


def _entry(lengths, heights):
    """A page_rows entry: each row's height in points, as a list of that height once per panel where panels share a row."""
    return [_number(h) if length == 1 else [_number(h)] * length for length, h in zip(lengths, heights)]


def _summary(pages, margin):
    return {'margin': margin, 'min_row_pt': MIN_ROW_PT, 'min_share_of_prior': MIN_SHARE,
            'max_growth_of_prior': MAX_GROWTH, 'wrap_share_of_clip_width': WRAP_SHARE,
            'statuses': {status: sum(1 for page in pages.values() if page['status'] == status)
                         for status in ('ok', 'tight', 'cannot_fit')}}


def fit_layout(script, prior_rows, frames, faces=None, margin=MARGIN, floors=None, ceilings=None, painted=None, keep=None,
               minimums=None):
    """Fit every page of `script`: {"page_rows": {...}, "report": {...}}.

    `prior_rows` is LAYOUT.json's page_rows; `frames` maps a panel id to its frame
    ({"visible_rect", "width", "height"}, where visible_rect is the uncropped art rect); `faces` maps a panel id to (x, y, r) fractions of the frame,
    r of its height, at the radii to keep clear. `painted` and `keep` likewise map a panel id to
    [x0, y0, x1, y1] fractions of the frame (x of its width, y of its height): the painted regions its
    balloons must hide (run_chapter.fit_inputs measures them as the planner does) and the story keep zones
    (a gripping hand, a prop). The crop keeps each of them whole, as it keeps the face zones, so a frame
    whose painted regions span its width is shown letterboxed in a tall slot, as the planner will show it.
    A panel with no frame is treated as art that fills its slot. A page missing from `prior_rows` gets one
    full-width row per panel to start from.
    `floors` maps a panel id to a height in points that a planner probe has proved it needs: its row
    is never given less, within the upper bound, and the ratio fit works above those floors.
    `ceilings` likewise caps a row (a floor equal to a ceiling pins it). A floor the page cannot give
    (above the upper bound or a ceiling, or floors that together exceed the page) is reported as
    "cannot_fit"; the bounds are still never violated.
    `minimums` maps a panel id to a height in points its row is given at least (within the upper bound), as a floor
    does, but it is not proof that the lettering fits: the row is still judged against the margin, and the report
    lists it as "cue_min_pt" and "cue_met". fit_structures uses it for the size cues of the script.
    """
    faces, floors = faces or {}, floors or {}
    page_rows, pages = {}, {}
    for page_no, page in script['pages'].items():
        raw = (prior_rows or {}).get(str(page_no))
        rows, prior, budget = _build_rows(page_no, page, raw, frames, faces, floors, ceilings, painted, keep, minimums)
        new = _solve(page_no, rows, budget, margin)
        page_rows[str(page_no)] = _entry([len(row.panels) for row in rows], new)
        pages[str(page_no)] = _page_report(rows, prior, new, margin, raw is None, budget)
    return {'page_rows': page_rows, 'report': {**_summary(pages, margin), 'pages': pages}}


# What a panel's script description asks of its row. A cue is read from the opening of the description (its first two
# sentences; the strip, tier and splash words only from its first few words), because the script writers state the
# layout first and then describe the scene, which has "a leather strip" and "the strip of beach" in it.
_FULL_WIDTH = re.compile(r'\bfull[- ](?:page[- ])?width\b', re.IGNORECASE)
_ROW_WORD = re.compile(r'\b(?:strip|tier|splash)\b(?!\s+of\b)', re.IGNORECASE)
_SIDE_BY_SIDE = re.compile(r'side by side|\b(?:left|right) half\b|\bsplit\b', re.IGNORECASE)
_PERCENT = re.compile(r'(\d+(?:\.\d+)?)\s*(?:percent\b|%)', re.IGNORECASE)
_FRACTION = re.compile(r'\b(?:(a|an|one|two|three|four)[\s-]+)?(?:full\s+)?'
                       r'(half|halves|thirds?|quarters?|fourths?|fifths?|sixths?)\s+(?:of\s+)?the\s+page\b', re.IGNORECASE)
_NUMERATORS = {'a': 1, 'an': 1, 'one': 1, 'two': 2, 'three': 3, 'four': 4}
_DENOMINATORS = {'half': 2, 'halves': 2, 'third': 3, 'thirds': 3, 'quarter': 4, 'quarters': 4, 'fourth': 4, 'fourths': 4,
                 'fifth': 5, 'fifths': 5, 'sixth': 6, 'sixths': 6}


def layout_cues(panel):
    """What a panel's script description asks of its row: {"solo": bool, "min_share": float or None}.

    "solo": the panel is alone in its row. "Full width", "full-width" and "full page width" ask for it, in the first
    two sentences; so do the words strip, tier and splash among the first CUE_HEAD_WORDS words ("Narrow strip.", "Bottom
    strip.", "Large, most of a tier."), unless the first sentence asks for panels side by side ("Split tier, two narrow
    panels side by side.", "Left half of the third tier.", which ask for the opposite) or the word begins "strip of".
    "min_share": the share of the page the panel's row should have at least, from "about a third of the page",
    "two thirds of the page", "top half of the page", "half the page", "a quarter of the page", "a fifth", "a sixth",
    "about the bottom 40 percent of the page", "45%" or "about 40 percent" in the first two sentences (the largest
    if there are several); a share outside 0 to 1 is ignored. Insets, inserts and "small" panels, and camera words
    like "wide", ask for nothing: they may share a row freely.
    """
    text = ' '.join((panel.get('description') or '').split())
    sentences = re.split(r'(?<=[.!?])\s+', text)
    opening, first = ' '.join(sentences[:2]), sentences[0]
    solo = bool(_FULL_WIDTH.search(opening))
    if not solo and not _SIDE_BY_SIDE.search(first):
        word = _ROW_WORD.search(first)
        solo = bool(word and len(first[:word.start()].split()) < CUE_HEAD_WORDS)
    shares = [float(m.group(1)) / 100 for m in _PERCENT.finditer(opening)]
    shares += [_NUMERATORS.get((m.group(1) or 'a').lower(), 1) / _DENOMINATORS[m.group(2).lower()]
               for m in _FRACTION.finditer(opening)]
    return {'solo': solo, 'min_share': max((share for share in shares if 0 < share <= 1), default=None)}


def cue_floor_pt(share):
    """The row height in points that a size cue naming `share` of the page asks for: CUE_SHARE of that share."""
    return CUE_SHARE * share * c.STORY_HEIGHT_PT


@functools.lru_cache(maxsize=None)
def row_sizes(count, sizes=ROW_SIZES):
    """Every way to cut `count` panels, in reading order, into consecutive rows of `sizes` panels: tuples of row sizes."""
    if count == 0:
        return [()]
    return [(size,) + rest for size in sizes if size <= count for rest in row_sizes(count - size, sizes)]


def rows_of(sizes):
    """The panel indexes of each row of a structure given as row sizes."""
    rows, cursor = [], 0
    for size in sizes:
        rows.append(list(range(cursor, cursor + size)))
        cursor += size
    return rows


def _respects(sizes, solo):
    return all(len(row) == 1 or not any(solo[index] for index in row) for row in rows_of(sizes))


def structure_candidates(count, solo, prior_sizes):
    """The structures to try for a page of `count` panels: the prior's own first, then every grouping into rows of one
    or two that keeps each panel flagged in `solo` alone. The prior is a candidate even when it has a row of three or
    pairs a solo panel (it is then flagged, not dropped)."""
    found = [tuple(prior_sizes)]
    found += [sizes for sizes in row_sizes(count) if sizes != found[0] and _respects(sizes, solo)]
    return found


def _spread_prior(weights, floors, budget):
    """Row heights in tenths in proportion to `weights`, each at least its floor, totalling `budget`; None if the floors
    cannot be met. A candidate structure is fitted from these heights, as the prior layout's heights start its own fit."""
    fixed, free = {}, set(range(len(weights)))
    while free:
        room, weight = budget - sum(fixed.values()), sum(weights[i] for i in free)
        short = [i for i in free if room * weights[i] / weight < floors[i]]
        if not short:
            break
        for i in short:
            fixed[i] = floors[i]
            free.discard(i)
    room = budget - sum(fixed.values())
    if room < 0 or (not free and room):
        return None
    shares = {i: room * weights[i] / sum(weights[j] for j in free) for i in free}
    heights = {i: math.floor(shares[i]) for i in free}
    for i in sorted(free, key=lambda i: (heights[i] - shares[i], i))[:room - sum(heights.values())]:
        heights[i] += 1
    return [fixed[i] if i in fixed else heights[i] for i in range(len(weights))]


def rank_key(score, order):
    """Sort key for a scored candidate, larger is better: the script's cues respected, every lettered panel's ratio at
    least 1, then the page's minimum fill, its mean fill (the share of each slot's area the art covers, see _Panel.fill)
    and its minimum lettering ratio (fills to three places), then the earlier candidate (the prior structure is first)."""
    return (score['cues_ok'], score['min_ratio'] >= 1.0, round(score['min_fill'], 3), round(score['mean_fill'], 3),
            round(score['min_ratio'], 3), -order)


def _score(rows, heights, cues_ok):
    """A page's fills (a panel with no frame fills its slot) and lettering ratios at the given heights."""
    fills = [1.0 if (fill := panel.fill(h / TENTHS)) is None else fill
             for row, h in zip(rows, heights) for panel in row.panels]
    ratios = [panel.ratio(h / TENTHS) for row, h in zip(rows, heights) for panel in row.panels if not panel.silent]
    return {'cues_ok': cues_ok, 'min_fill': min(fills), 'mean_fill': sum(fills) / len(fills),
            'min_ratio': min(ratios, default=math.inf)}


def _prior_report(report, before_rows):
    """Point a page report's before numbers at the prior layout, not at the start the structure was fitted from."""
    by_panel = {panel.id: (panel, row.prior / TENTHS) for row in before_rows for panel in row.panels}
    by_row = {tuple(panel.id for panel in row.panels): row for row in before_rows}
    for panel_id, info in report['panels'].items():
        panel, height = by_panel[panel_id]
        info['ratio_before'], info['fill_before'] = _round(panel.ratio(height)), _round(panel.fill(height))
        info['fill_width_before'] = _round(panel.fill_width(height))
    for info in report['rows']:
        row = by_row.get(tuple(info['panels']))                            # a row the prior did not have has no before
        info['prior_pt'] = None if row is None else _number(row.prior)
        info['ratio_before'] = None if row is None else _round(row.raw(row.prior))
    report['min_ratio_before'] = _round(min(row.raw(row.prior) for row in before_rows))


def _choose_structure(page_no, page, raw, frames, faces, margin, painted, keep, refine, top):
    """One page: (page_rows entry, page report) for the best structure."""
    panels = page['panels']
    ids = [panel['id'] for panel in panels]
    cues = {panel['id']: layout_cues(panel) for panel in panels}
    minimums = {panel_id: cue_floor_pt(cue['min_share']) for panel_id, cue in cues.items() if cue['min_share']}
    for spec in panels:
        # "Full width" asks for art across the column, not a narrow strip: its row is floored where the crop spans it.
        if cues[spec['id']]['solo'] and frames.get(spec['id']):
            span = SPAN_SHARE * _Panel(spec, c.ART_WIDTH_PT, frames[spec['id']], (faces or {}).get(spec['id']),
                                       (painted or {}).get(spec['id']), (keep or {}).get(spec['id'])).fill_height()
            if span > minimums.get(spec['id'], 0):
                minimums[spec['id']] = span
    solo = [cues[panel_id]['solo'] for panel_id in ids]
    cache = {}
    groups, tenths = _prior_structure(page_no, ids, raw)
    prior_sizes = tuple(len(group) for group in groups)
    prior_entry = raw if raw is not None else _entry(prior_sizes, tenths)
    before_rows, _, _ = _build_rows(page_no, page, raw, frames, faces, {}, None, painted, keep, None, cache)
    height_of = {panel.id: row.prior / TENTHS for row in before_rows for panel in row.panels}
    total = len(set(row_sizes(len(ids))) | {prior_sizes})
    candidates = []
    for order, sizes in enumerate(structure_candidates(len(ids), solo, prior_sizes)):
        if sizes == prior_sizes:
            entry = prior_entry
        else:
            members = rows_of(sizes)
            floors = [max([round(MIN_ROW_PT * TENTHS)] + [math.ceil(round(minimums.get(ids[i], 0) * TENTHS, 6)) for i in row])
                      for row in members]
            heights = _spread_prior([sum(height_of[ids[i]] for i in row) / len(row) for row in members], floors,
                                    PAGE_TENTHS - GAP_TENTHS * (len(members) - 1))
            if heights is None:                                            # the cues' floors cannot all be met
                continue
            entry = _entry(sizes, heights)
        rows, prior, budget = _build_rows(page_no, page, entry, frames, faces, {}, None, painted, keep, minimums, cache)
        cues_ok = (_respects(sizes, solo) and all(row.cue <= row.hi for row in rows)
                   and sum(max(row.bound, row.cue) for row in rows) <= budget)
        if not cues_ok and sizes != prior_sizes:
            continue
        new = _solve(page_no, rows, budget, margin)
        score = _score(rows, new, cues_ok)
        candidates.append({'sizes': sizes, 'order': order, 'entry': entry, 'rows': rows, 'prior': prior, 'budget': budget,
                           'new': new, 'score': score, 'key': rank_key(score, order), 'verified': None})
    ranked = sorted(candidates, key=lambda cand: cand['key'], reverse=True)
    chosen = ranked[0]
    if refine is not None:
        # The top `top` are always asked; if none verifies, the rest are asked in rank order until one does.
        for index, cand in enumerate(ranked):
            if index >= top and any(asked['verified'] for asked in ranked[:index]):
                break
            fitted, cand['verified'] = refine(page_no, page, cand['entry'], minimums)
            cand['fitted'] = fitted
            final, _, _ = _build_rows(page_no, page, fitted['page_rows'][page_no], frames, faces, {}, None, painted, keep,
                                      minimums, cache)
            cand['final_rows'] = [_number(row.prior) for row in final]
            cand['score'] = _score(final, [row.prior for row in final], cand['score']['cues_ok'])
            cand['key'] = rank_key(cand['score'], cand['order'])
        verified = [cand for cand in ranked if cand['verified']]
        chosen = max(verified or ranked[:1], key=lambda cand: cand['key'])
    if 'fitted' in chosen:
        entry, report = chosen['fitted']['page_rows'][page_no], chosen['fitted']['report']['pages'][page_no]
        if raw is None:
            report['default_rows'] = True
    else:
        entry = _entry(chosen['sizes'], chosen['new'])
        report = _page_report(chosen['rows'], chosen['prior'], chosen['new'], margin, raw is None, chosen['budget'])
    _prior_report(report, before_rows)
    ordered = [chosen] + sorted((cand for cand in ranked if cand is not chosen), key=lambda cand: cand['key'], reverse=True)
    report['structure'] = {
        'chosen': list(chosen['sizes']), 'prior': list(prior_sizes),
        'min_fill': round(chosen['score']['min_fill'], 3), 'mean_fill': round(chosen['score']['mean_fill'], 3),
        'min_ratio': _round(chosen['score']['min_ratio']), 'verified': chosen['verified'],
        'candidates': total, 'excluded': total - len(candidates),
        'cues': {panel_id: {**cue, 'min_pt': None if panel_id not in minimums else
                            _number(math.ceil(round(minimums[panel_id] * TENTHS, 6)))}
                 for panel_id, cue in cues.items() if cue['solo'] or cue['min_share']},
        'alternatives': [{'structure': list(cand['sizes']),
                          'rows_pt': cand.get('final_rows') or [_number(h) for h in cand['new']],
                          'min_fill': round(cand['score']['min_fill'], 3), 'mean_fill': round(cand['score']['mean_fill'], 3),
                          'min_ratio': _round(cand['score']['min_ratio']), 'cues_ok': cand['score']['cues_ok'],
                          'verified': cand['verified'], 'prior': cand['sizes'] == prior_sizes,
                          'chosen': cand is chosen} for cand in ordered]}
    return entry, report


def fit_structures(script, prior_rows, frames, faces=None, margin=MARGIN, painted=None, keep=None, refine=None,
                   top=PROBE_TOP):
    """Fit every page of `script` like fit_layout, choosing each page's row structure as well as its heights.

    Every way to group the page's panels, in reading order, into rows of one or two (ROW_SIZES; rows of three are not
    tried) is a candidate, and so is the prior layout's own structure (`prior_rows`, as for fit_layout; a missing page
    has one equal full-width row per panel). A candidate that pairs a panel whose script description asks to be alone
    is dropped, and so is one that cannot give every size cue its floor (layout_cues, cue_floor_pt); the prior is
    kept and flagged "cues_ok": false instead. A candidate starts from rows in proportion to its panels' prior heights
    and is fitted as fit_layout fits them, each size cue as a minimum. Candidates are ranked by rank_key: every lettered
    panel's ratio at least 1, then the page's minimum fill (the share of the slot's area the placed art covers: a frame
    that cannot be narrowed and sits letterboxed in a tall half-width slot counts for little), its mean fill, and its
    minimum ratio; a tie goes to the prior structure, then to the earlier grouping.
    `refine(page_no, page, entry, minimums)`, if given, is asked about the top `top` candidates of each page (for the
    planner probe), and then about the next ones in rank order, one at a time, until one verifies if none of those did: it fits the candidate's `entry` (a page_rows entry to start from) and returns (fitted, verified),
    `fitted` being fit_layout's result for that one page. The verified candidates are ranked again on the heights they
    came back with and the best is chosen; if none verifies, the best candidate by the analytic fit stands, unverified.
    The result is fit_layout's, and each page's report gains "structure": the chosen row sizes, the prior's, the minimum
    and mean fill, the script cues, and every scored alternative with its scores and whether it verified. The page's
    "before" numbers are the prior layout's own; a row the prior did not have has no prior height.
    """
    faces = faces or {}
    page_rows, pages = {}, {}
    for page_no, page in script['pages'].items():
        key = str(page_no)
        page_rows[key], pages[key] = _choose_structure(key, page, (prior_rows or {}).get(key), frames, faces, margin,
                                                       painted, keep, refine, top)
    changed = sum(1 for page in pages.values() if page['structure']['chosen'] != page['structure']['prior'])
    search = {'row_sizes': list(ROW_SIZES), 'pages_changed': changed, 'probe_top': top if refine is not None else None}
    return {'page_rows': page_rows, 'report': {**_summary(pages, margin), 'structure_search': search, 'pages': pages}}
