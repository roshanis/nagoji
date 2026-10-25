#!/usr/bin/env python3
"""Turn v15-select decisions into a build manifest plus a Codex regeneration list.

Usage: lean_assemble.py --chapter N --package DIR --decisions decisions.json --tag lean-r1
  [--style ID:INDEX=unreadable ...]
Writes DIR/SELECTION-INPUT-<tag>.json (manifest rows) and DIR/review/REGEN-<tag>.json
(panels without an acceptable candidate or whose reserves could not be fitted).
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

REPO = Path('/Users/roshanvenugopal/Documents/github/nagoji')
PY = '/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python'
RUN = REPO / 'output/comic-v15-full-redo/pipeline/run_chapter.py'
FACE_SCALE = 1.0
CARRY = ('ledger_inscription', 'ledger_rect', 'sound_origin', 'sound_gray', 'sound_scale')
LAYOUT = None
UNPAINTED = False   # pass --unpainted to auto-geometry (art with no painted balloons)


def geometry(chapter, package, record, out, default_pkg, tails=None, faces=None, styles=None, keep=None):
    if tails is not None:
        target = out.with_name(f'{out.stem}-drawn.json')
        if target.exists():
            return json.loads(target.read_text()), 'drawn'
        tails_file = out.with_name(f'{out.stem}-tails.json')
        if not tails_file.exists():
            tails_file.write_text(json.dumps({str(t['copy_index']): [t['x'], t['y']] for t in tails}))
        cmd = [PY, str(RUN), 'auto-geometry', '--chapter', str(chapter), '--candidate', str(record),
               '--geometry-out', str(target), '--draw', '--tails', str(tails_file)]
        if faces is not None:
            faces_file = out.with_name(f'{out.stem}-faces.json')
            if not faces_file.exists():
                faces_file.write_text(json.dumps([{'x': f['x'], 'y': f['y'], 'r': round(f['r'] * FACE_SCALE, 4)} for f in faces]))
            cmd += ['--faces', str(faces_file)]
        if keep:
            keep_file = out.with_name(f'{out.stem}-keep.json')
            if not keep_file.exists():
                keep_file.write_text(json.dumps(keep))
            cmd += ['--keep', str(keep_file)]
        if styles:
            styles_file = out.with_name(f'{out.stem}-styles.json')
            if not styles_file.exists():
                styles_file.write_text(json.dumps(styles))
            cmd += ['--styles', str(styles_file)]
        if LAYOUT is not None:
            cmd += ['--layout', str(LAYOUT)]
        if UNPAINTED:
            cmd += ['--unpainted']
        if not default_pkg:
            cmd[3:3] = ['--package-dir', str(package)]      # before --chapter, not between it and its value
        r = subprocess.run(cmd, capture_output=True, text=True, env={'PYTHONDONTWRITEBYTECODE': '1', 'PATH': '/usr/bin:/bin'})
        if r.returncode == 0 and target.exists():
            return json.loads(target.read_text()), 'drawn'
        return None, ((r.stderr or r.stdout).strip().splitlines()[-1:] or ['no output'])[0]
    for inset in (6, 2, 0):
        target = out.with_name(f'{out.stem}-inset{inset}.json')
        if target.exists():
            return json.loads(target.read_text()), inset
        cmd = [PY, str(RUN), 'auto-geometry', '--chapter', str(chapter), '--candidate', str(record),
               '--geometry-out', str(target), '--inset', str(inset)]
        if not default_pkg:
            cmd[3:3] = ['--package-dir', str(package)]      # before --chapter, not between it and its value
        r = subprocess.run(cmd, capture_output=True, text=True, env={'PYTHONDONTWRITEBYTECODE': '1', 'PATH': '/usr/bin:/bin'})
        if r.returncode == 0 and target.exists():
            return json.loads(target.read_text()), inset
        last = (r.stderr or r.stdout).strip().splitlines()[-1:] or ['no output']
    return None, last[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chapter', type=int, required=True)
    ap.add_argument('--package', type=Path, required=True)
    ap.add_argument('--decisions', type=Path, required=True)
    ap.add_argument('--tag', required=True)
    ap.add_argument('--style', action='append', default=[])
    ap.add_argument('--draw', action='store_true')
    ap.add_argument('--faces-file', type=Path, help='v15-faces result: panels [{id, version, faces}]')
    ap.add_argument('--face-scale', type=float, default=1.0, help='scale whole-head radii down to the facial features')
    ap.add_argument('--carry-from', type=Path, help='earlier build manifest whose native lettering fields (ledger, sound marks) carry over')
    ap.add_argument('--carry-sources', type=Path, help='JSON {panel id: {version: source frame file name}}: edits that keep a source frame\'s geometry')
    ap.add_argument('--no-backup', action='store_true', help='never fall back to a backup (the pre-fit pass, so the fitter probes the picks)')
    ap.add_argument('--keep-file', type=Path, help='v15-keep result: panels [{id, version, keep}]')
    ap.add_argument('--layout', type=Path, help='place balloons against this LAYOUT file instead of the package LAYOUT.json')
    ap.add_argument('--unpainted', action='store_true', help='the art has no painted balloons (auto-geometry --unpainted)')
    a = ap.parse_args()
    global FACE_SCALE, LAYOUT, UNPAINTED
    FACE_SCALE = a.face_scale
    LAYOUT = a.layout.resolve() if a.layout else None
    UNPAINTED = a.unpainted
    pkg = a.package.resolve()
    default_pkg = pkg.name == f'ch{a.chapter:02d}'
    job = json.loads((pkg / 'IMAGEGEN-JOBS.json').read_text())
    order = [j['id'] for j in job['jobs']]
    decisions = {d['id']: d for d in json.loads(a.decisions.read_text())['decisions']}
    styles = {}                                   # panel id -> {copy index: style}; --style ID:INDEX=STYLE
    for spec in a.style:
        target, style = spec.split('=', 1)
        pid, _, index = target.partition(':')
        if not index:
            sys.exit(f'--style {spec}: name the chunk, as ID:INDEX=STYLE')
        styles.setdefault(pid, {})[index] = style
    face_map = {}
    if a.faces_file:
        for f in json.loads(a.faces_file.read_text())['panels']:
            face_map[(f['id'], f['version'])] = f['faces']
    keep_map = {}
    if a.keep_file:
        for k in json.loads(a.keep_file.read_text())['panels']:
            keep_map[(k['id'], k['version'])] = [{key: z[key] for key in ('x0', 'y0', 'x1', 'y1')} for z in k['keep']]
    carry = {}
    if a.carry_from:
        sources = json.loads(a.carry_sources.read_text()) if a.carry_sources else {}
        for old in json.loads(a.carry_from.read_text())['frames']:
            fields = {k: old[k] for k in CARRY if k in old}
            if fields:
                name = Path(old['path']).name.replace('-2x.png', '.png')
                carry[old['id']] = (name, old['width'], old['height'], fields, sources.get(old['id'], {}))

    def carry_fields(pid, version, row):
        """Copy native lettering fields from the earlier manifest when this frame is that frame or an edit keeping its geometry."""
        if pid not in carry:
            return []
        name, width, height, fields, edits = carry[pid]
        mine = Path(row['path']).name
        if mine != name and edits.get(version) != name:
            return []
        # An edit may differ by a few pixels, and an upscaled old row is at 2x: scale its coordinates to this frame.
        sx, sy = row['width'] / width, row['height'] / height
        for key, value in fields.items():
            if key in ('ledger_rect',):
                row[key] = [round(value[0] * sx), round(value[1] * sy), round(value[2] * sx), round(value[3] * sy)]
            elif key == 'sound_origin':
                row[key] = [round(value[0] * sx), round(value[1] * sy)]
            else:
                row[key] = value
        return sorted(fields)
    geodir = pkg / 'review' / f'geometry-{a.tag}'
    geodir.mkdir(parents=True, exist_ok=True)
    rows, regen, notes = [], [], []
    for pid in order:
        d = decisions.get(pid)
        if not d:
            regen.append({'id': pid, 'reason': 'no decision', 'correction': ''}); continue
        chosen = None
        tries = [(d.get('pick'), d.get('tails', []), d.get('faces'))]
        if not a.no_backup:
            tries.append((d.get('backup'), d.get('backup_tails', []), d.get('backup_faces')))
        for version, tails, dfaces in tries:
            if not version:
                continue
            record = pkg / 'candidates' / f'{pid}-{version}.json'
            selected = pkg / 'selections' / f'{pid}.json'      # frames carried in from an earlier package have only a selection record
            if not record.exists() and selected.exists() and Path(json.loads(selected.read_text())['path']).name == f'{pid}-{version}.png':
                record = selected
            if not record.exists():
                notes.append(f'{pid}: {version} record missing'); continue
            faces = face_map.get((pid, version), dfaces) if a.draw else None
            if a.draw and faces is None:
                notes.append(f'{pid}: {version} has no face data; refusing to place balloons blind'); continue
            geo, info = geometry(a.chapter, pkg, record, geodir / f'{pid}-{version}.json', default_pkg,
                                 tails if a.draw else None, faces, styles.get(pid) if a.draw else None,
                                 keep_map.get((pid, version)) if a.draw else None)
            if geo is None:
                notes.append(f'{pid}: {version} reserves failed ({info})'); continue
            row = json.loads(record.read_text())
            row.update(geo)
            if pid in styles and not a.draw:
                for reserve in row['reserves']:
                    if str(reserve['copy_indices'][0]) in styles[pid]:
                        reserve['style'] = styles[pid][str(reserve['copy_indices'][0])]
            for ref in row.get('references') or []:          # older captures recorded paths only
                if 'sha256' not in ref:
                    ref['sha256'] = hashlib.sha256(Path(ref['path']).read_bytes()).hexdigest()
                    ref['sha256_filled_at_build'] = True
            if carry:
                carried = carry_fields(pid, version, row)
                if carried:
                    notes.append(f'{pid}: {version} carried {carried}')
            row['visual_review'] = 'pass'
            row['reviewer'] = 'Claude selection workflow, auto-geometry %s' % (('inset %d' % info) if isinstance(info, int) else info)
            row['review_note'] = d.get('issues') or 'Clean against sheets, bible row and script beat.'
            chosen = row; break
        if chosen:
            rows.append(chosen)
        else:
            regen.append({'id': pid, 'reason': 'no acceptable candidate' if not d.get('pick') else 'reserves did not fit',
                          'correction': d.get('correction') or ('Leave clearly blank, outlined text areas, one per lettering line, '
                                                               'large enough for the text, clear of faces and the key action.'),
                          'issues': d.get('issues', '')})
    manifest = {'schema_version': 2, 'chapter': a.chapter, 'status': 'lean_selection', 'tag': a.tag,
                'frames': rows, 'missing': [r['id'] for r in regen]}
    out = pkg / f'SELECTION-INPUT-{a.tag}.json'
    with out.open('x') as f:
        f.write(json.dumps(manifest, indent=1) + '\n')
    rg = pkg / 'review' / f'REGEN-{a.tag}.json'
    with rg.open('x') as f:
        f.write(json.dumps(regen, indent=1) + '\n')
    print(json.dumps({'selected': len(rows), 'regenerate': len(regen), 'manifest': str(out), 'regen': str(rg), 'notes': notes}, indent=1))


if __name__ == '__main__':
    main()
