#!/usr/bin/env python3
"""Contact sheets for reviewing every candidate frame of a V15 chapter package.

make_review_sheets() writes one PNG per panel in IMAGEGEN-JOBS.json, showing all of that
panel's candidate frames, labelled by version under a header with the panel id and cast,
plus an INDEX.json that maps each panel to its sheet and candidates. It only reads the
package and only writes into a new output directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[3]
SHEET_WIDTH = 1600
MARGIN = 16
GAP = 16
HEADER_HEIGHT = 84
LABEL_HEIGHT = 34
MAX_TILE_HEIGHT = 1100
MAX_SHEET_HEIGHT = 2600
BACKGROUND = (44, 44, 48)
PLATE = (70, 70, 76)
TEXT = (238, 238, 240)
MUTED = (170, 170, 178)


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _font(size, bold=False):
    names = ['/System/Library/Fonts/Helvetica.ttc', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
             if bold else '/System/Library/Fonts/Supplemental/Arial.ttf']
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def _frame_path(recorded, package):
    """Records hold absolute paths, or paths relative to the repository root or the working directory."""
    path = Path(recorded)
    options = [path] if path.is_absolute() else [Path.cwd() / path, REPO_ROOT / path, package / path]
    for option in options:
        if option.is_file():
            return option.resolve()
    raise FileNotFoundError(f'candidate frame not found: {recorded}')


def _candidates(package, panel):
    """Candidate records for one panel, in version order.

    A candidate is candidates/<panel>-vNN.json. Provenance files sit beside them and are
    not candidates. Other <panel>-<label>.json records (an import such as r7-a01) are
    listed only when they hold a frame path and add a frame no earlier record shows.
    """
    found = []
    for path in (package / 'candidates').glob(f'{panel}-*.json'):
        label = path.name[len(panel) + 1:-len('.json')]
        if 'provenance' in label:
            continue
        version = re.fullmatch(r'v(\d+)', label)
        record = json.loads(path.read_text(encoding='utf-8'))
        is_record = isinstance(record, dict) and 'path' in record and 'sha256' in record \
            and record.get('id', panel) == panel
        if version and not is_record:
            raise ValueError(f'candidate record is unreadable: {path.name}')
        if is_record:
            key = (0, int(version.group(1)), label) if version else (1, 0, label)
            found.append((key, label, path, record))
    entries, seen = [], set()
    for _, label, path, record in sorted(found, key=lambda item: item[0]):
        frame = _frame_path(record['path'], package)
        if frame in seen:
            continue
        seen.add(frame)
        actual = _sha256(frame)
        if actual != record['sha256']:
            raise ValueError(f'frame differs from its record: {path.name} ({frame.name})')
        entries.append({'version': label, 'record': str(path.resolve()), 'frame': str(frame), 'sha256': actual})
    return entries


def _tile_sizes(sizes, columns):
    """(cell width, per-frame tile sizes, sheet height) when laid out in this many columns."""
    cell = (SHEET_WIDTH - 2 * MARGIN - (columns - 1) * GAP) // columns
    tiles = []
    for width, height in sizes:
        scale = min(1.0, cell / width, MAX_TILE_HEIGHT / height)
        tiles.append((max(1, round(width * scale)), max(1, round(height * scale))))
    rows = [tiles[i:i + columns] for i in range(0, len(tiles), columns)]
    total = HEADER_HEIGHT + sum(max(h for _, h in row) + LABEL_HEIGHT + GAP for row in rows) + MARGIN
    return cell, tiles, total


def _columns(sizes):
    """Columns for a sheet: wide strips start one per row, squarer frames two, portrait three.

    More columns are added, up to three, while the sheet would be taller than
    MAX_SHEET_HEIGHT, because a viewer shrinks a very tall image until it is unreadable.
    """
    aspect = statistics.median(w / h for w, h in sizes)
    columns = 1 if aspect >= 2 else 2 if aspect >= .9 else 3
    columns = min(columns, len(sizes))
    while columns < min(3, len(sizes)) and _tile_sizes(sizes, columns)[2] > MAX_SHEET_HEIGHT:
        columns += 1
    return columns


def _draw_sheet(panel, cast, entries, path):
    frames = []
    for entry in entries:
        with Image.open(entry['frame']) as image:
            frames.append(image.convert('RGB'))
    if frames:
        columns = _columns([f.size for f in frames])
        cell, sizes, height = _tile_sizes([f.size for f in frames], columns)
        tiles = [frame.resize(size, Image.LANCZOS) for frame, size in zip(frames, sizes)]
        rows = [tiles[i:i + columns] for i in range(0, len(tiles), columns)]
    else:
        cell, rows, height = SHEET_WIDTH - 2 * MARGIN, [], HEADER_HEIGHT + 60
    sheet = Image.new('RGB', (SHEET_WIDTH, height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    draw.text((MARGIN, 12), panel, fill=TEXT, font=_font(34, bold=True))
    cast_text = 'cast: ' + (', '.join(cast) if cast else 'none')
    draw.text((MARGIN, 54), f'{cast_text}      {len(entries)} candidate(s)', fill=MUTED, font=_font(22))
    if not entries:
        draw.text((MARGIN, HEADER_HEIGHT + 12), 'no candidates yet', fill=MUTED, font=_font(26))
    y, index = HEADER_HEIGHT, 0
    for row in rows:
        row_height = max(t.height for t in row)
        for column, tile in enumerate(row):
            x = MARGIN + column * (cell + GAP) + (cell - tile.width) // 2
            entry = entries[index]
            draw.rectangle([x - 2, y - 2 + LABEL_HEIGHT, x + tile.width + 1, y + LABEL_HEIGHT + tile.height + 1],
                           outline=PLATE, width=2)
            draw.text((x, y + 2), entry['version'], fill=TEXT, font=_font(26, bold=True))
            draw.text((x + 120, y + 6), f'{frames[index].width} x {frames[index].height}   {entry["sha256"][:10]}',
                      fill=MUTED, font=_font(18))
            sheet.paste(tile, (x, y + LABEL_HEIGHT))
            index += 1
        y += row_height + LABEL_HEIGHT + GAP
    sheet.save(path)


def make_review_sheets(package_dir, out_dir):
    """Write one contact sheet per panel and INDEX.json into a new out_dir; return the index."""
    package = Path(package_dir).resolve()
    out = Path(out_dir).resolve()
    jobs = json.loads((package / 'IMAGEGEN-JOBS.json').read_text(encoding='utf-8'))['jobs']
    if out == package or package in out.parents:
        raise ValueError(f'out_dir must be outside the package: {out}')
    if out.exists():
        raise FileExistsError(f'out_dir already exists: {out}')
    # Read and verify everything before creating anything.
    plan = [(job['id'], list(job.get('cast', [])), _candidates(package, job['id'])) for job in jobs]
    out.mkdir(parents=True)
    index = {}
    for panel, cast, entries in plan:
        sheet = out / f'{panel}.png'
        _draw_sheet(panel, cast, entries, sheet)
        index[panel] = {'sheet': str(sheet), 'cast': cast, 'candidates': entries}
    (out / 'INDEX.json').write_text(json.dumps(index, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return index


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package-dir', type=Path, required=True, help='chapter package, for example chapters/ch03')
    parser.add_argument('--out', type=Path, required=True, help='new directory for the sheets and INDEX.json')
    args = parser.parse_args(argv)
    try:
        index = make_review_sheets(args.package_dir, args.out)
    except (ValueError, FileExistsError, FileNotFoundError) as error:
        sys.exit(f'review_sheets: {error}')
    print(json.dumps({'out_dir': str(args.out.resolve()), 'sheets': len(index),
                      'candidates': sum(len(v['candidates']) for v in index.values())}, indent=2))


if __name__ == '__main__':
    main()
