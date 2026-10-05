#!/usr/bin/env python3
"""V15 per-chapter production entry point. Built-in imagegen runs in Codex."""
from __future__ import annotations
import argparse
import concurrent.futures
import copy
import functools
import json
import multiprocessing
import os
import re
import shutil
from pathlib import Path
import compositor as c
import script_pipeline as s

V15=Path(__file__).resolve().parent.parent


def write_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    text=json.dumps(data,indent=2,ensure_ascii=False)+'\n'
    if chr(0x2014) in text:raise ValueError('Em dash forbidden')
    with path.open('x',encoding='utf-8') as f:f.write(text)


SNAPSHOTS={'CONTINUITY.md':'CONTINUITY-SNAPSHOT.md'}
SCRIPT_SOURCE='SCRIPT-SOURCE.md'          # the package's frozen copy of the script it was prepared from
SCRIPT_REVISIONS='SCRIPT-REVISIONS.json'  # script versions accepted since: directions changed, lettering untouched


def _snapshot_name(path):
    """Return the package snapshot filename for a recorded input, if one exists."""
    name=Path(path).name
    if name.endswith('-ART-DIRECTION.json'):
        return 'ART-DIRECTION-SNAPSHOT.json'
    return SNAPSHOTS.get(name)


def check_recorded_input(item,out,snapshot_name=None):
    """The recorded input must be unchanged, or frozen in the package's own snapshot."""
    source_path=Path(item['path'])
    if source_path.is_file() and c.sha256(source_path)==item['sha256']:return
    snapshot_name=snapshot_name or _snapshot_name(item['path'])
    snapshot=Path(out)/snapshot_name if snapshot_name else None
    if snapshot is not None and snapshot.is_file() and c.sha256(snapshot)==item['sha256']:return
    revisions,source=Path(out)/SCRIPT_REVISIONS,Path(out)/SCRIPT_SOURCE
    if revisions.is_file() and source.is_file() and c.sha256(source)==item['sha256']:
        accepted={entry['sha256'] for entry in json.loads(revisions.read_text()) if entry.get('source')==item['path']}
        if c.sha256(Path(item['path'])) in accepted:return
    raise ValueError(f'Input changed since preparation: {item["path"]}')


def _lettering(script):
    """The parts of a script a package's frames and lettering depend on: its panels, in order, with their copy."""
    return [(panel['id'],[(chunk['speaker'],chunk['text']) for chunk in panel['copy']])
            for page in script['pages'].values() for panel in page['panels']]


def _lettering_changes(before,after):
    """The text-only changes between two _lettering lists, or None when the panels, balloons or speakers differ."""
    if [(panel,[speaker for speaker,_ in copy]) for panel,copy in before]!=[(panel,[speaker for speaker,_ in copy]) for panel,copy in after]:
        return None
    return [{'panel':panel,'chunk':i,'speaker':a[0],'before':a[1],'after':b[1]}
            for (panel,old),(_,new) in zip(before,after) for i,(a,b) in enumerate(zip(old,new)) if a!=b]


def accept_script_revision(args,out):
    """Accept the package's script as revised by the author: directions may change, and with --allow-lettering the
    text of existing balloons and captions, never the panels, the balloons or their speakers.

    The package must hold SCRIPT-SOURCE.md, a copy of the script it was prepared from (frozen before the edit); the
    live script must parse to the same panels with the same speakers (and, without --allow-lettering, the same text).
    The accepted hash is appended to SCRIPT-REVISIONS.json with the reason and any text changes, and load_job then
    accepts the revised script. A text change needs a new fit and build, since the balloons are sized from the text.
    """
    if not args.reason:raise ValueError('accept-script-revision needs --reason')
    job=json.loads((out/'IMAGEGEN-JOBS.json').read_text());item=job['script']
    source=out/SCRIPT_SOURCE
    if not source.is_file():raise ValueError(f'{SCRIPT_SOURCE} is missing: copy the script into the package before editing it')
    if c.sha256(source)!=item['sha256']:raise ValueError(f'{SCRIPT_SOURCE} does not match the script the package was prepared from')
    live=Path(item['path'])
    before,after=_lettering(s.parse_script(source)),_lettering(s.parse_script(live))
    changes=[]
    if before!=after:
        changed=', '.join(sorted({panel for panel,_ in before}.symmetric_difference({panel for panel,_ in after})
                                 |{a[0] for a,b in zip(before,after) if a!=b}) or ['panel order'])
        changes=_lettering_changes(before,after)
        if changes is None:
            raise ValueError(f'the revised script changes the panels, balloons or speakers, not only the lettering ({changed})')
        if not args.allow_lettering:
            raise ValueError(f'the revised script changes the lettering ({changed}); pass --allow-lettering to accept text-only changes')
        for change in changes:
            if chr(0x2014) in change['after'] or chr(0x2013) in change['after']:
                raise ValueError(f"{change['panel']}: the new text has an em or en dash")
    revisions=out/SCRIPT_REVISIONS
    entries=json.loads(revisions.read_text()) if revisions.is_file() else []
    from datetime import datetime,timezone
    entry={'source':item['path'],'sha256':c.sha256(live),'reason':args.reason,
           'accepted_at':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    if changes:entry['lettering_changes']=changes
    entries.append(entry)
    if revisions.is_file():
        # An append-only log: every earlier entry is kept, and the file is replaced in one step.
        text=json.dumps(entries,indent=2,ensure_ascii=False)+'\n'
        if chr(0x2014) in text:raise ValueError('Em dash forbidden')
        partial=revisions.with_name(revisions.name+'.partial')
        with partial.open('x',encoding='utf-8') as f:f.write(text)
        os.replace(partial,revisions)
    else:write_json(revisions,entries)
    return {'accepted':c.sha256(live),'revisions':len(entries),'lettering_changes':len(changes)}


def load_job(out):
    job=json.loads((out/'IMAGEGEN-JOBS.json').read_text())
    profile=job.get('prompt_profile')
    if profile not in (None,'v1','v2'):
        raise ValueError(f'Unknown prompt_profile: {profile}')
    for item in [job['script'],job['continuity'],job['character_lock']]:
        check_recorded_input(item,out)
    if profile=='v2' and 'art_direction' not in job:
        raise ValueError('v2 job requires art_direction')
    if 'art_direction' in job:
        check_recorded_input(job['art_direction'],out,'ART-DIRECTION-SNAPSHOT.json')
    for item in job['jobs']:
        if c.sha256(Path(item['prompt_path']))!=item['prompt_sha256']:
            raise ValueError(f'Prepared prompt changed: {item["id"]}')
        for path,digest in item['reference_image_sha256'].items():
            if c.sha256(Path(path))!=digest:
                raise ValueError(f'Prepared reference changed: {path}')
    return job


def package(chapter,override=None):
    if not 1<=chapter<=28:raise ValueError('Chapter must be 1 through 28')
    name=f'ch{chapter:02d}'
    if override is None:return V15/'chapters'/name
    # A sibling package (for example ch01-v2) rebuilds a chapter without touching the original.
    resolved=Path(override).resolve()
    if resolved.parent!=(V15/'chapters').resolve() or not re.fullmatch(name+r'(-[A-Za-z0-9]+)?',resolved.name):
        raise ValueError(f'Package must be chapters/{name} or chapters/{name}-<suffix>')
    return V15/'chapters'/resolved.name


def selected_rows(out,job):
    rows=[]
    for item in job['jobs']:
        p=out/'selections'/f'{item["id"]}.json'
        if not p.exists():raise ValueError(f'No reviewed selection: {item["id"]}')
        rows.append(json.loads(p.read_text()))
    return rows


def audit_reserve_pixels(rows,geometry,measurements):
    """Check actual glyph ink rectangles against blank native reserve pixels."""
    from PIL import Image
    import numpy as np
    row_map={r['id']:r for r in rows}
    panel_map={p['id']:p for ps in geometry['pages'].values() for p in ps}
    results=[]
    for m in measurements:
        if m.get('drawn'):continue     # text on a drawn shape sits on the shape's own white fill
        row=row_map[m['frame_id']];clip,_=c.fit_clip_contain(row,panel_map[row['id']])
        matrix=c.measure([row['width'],row['height']],row['visible_rect'],clip)['matrix']
        a,_,_,d,e,f=matrix
        def source(x,y):return (row['width']*(x-e)/a,row['height']*(1-(y-f)/d))
        with Image.open(row['path']) as image:
            for text,base,bounds in zip(m['lines'],m['baselines_pt'],m['actual_line_bounds_pt']):
                x,y,w,h=m['rect_pt'];bx0,by0,bx1,by1=bounds
                left,bottom=source(x+2+bx0,y+base+by0)
                right,top=source(x+2+bx1,y+base+by1)
                rect=[round(left),round(top),round(right),round(bottom)]
                vx0,vy0,vx1,vy1=row['visible_rect']
                if not (vx0<=rect[0]<rect[2]<=vx1 and vy0<=rect[1]<rect[3]<=vy1):
                    raise ValueError(f'Glyph lies outside visible art: {row["id"]}')
                pix=np.asarray(image.crop(rect),dtype=float)
                fraction=float((pix.mean(axis=2)>190).mean())
                results.append({'frame_id':row['id'],'text':text,'source_pixel_rect':rect,'light_fraction':fraction})
                if fraction<.99:raise ValueError(f'Lettering crosses nonblank art: {row["id"]}: {text} ({fraction:.3f})')
    return {'status':'pass','minimum_light_fraction':min((x['light_fraction'] for x in results),default=1),
            'line_count':len(results),'lines':results}


class AutoGeometryError(ValueError):
    """auto-geometry could not produce a geometry that is safe to select."""


_MALAYALAM=re.compile(r"\([^)]*\bmalayalam\b[^)]*\)",re.I)


def lettered_script(path):
    """The script as it is lettered: parse_script, with every line tagged (Malayalam) inside angle brackets.

    Angle brackets mark speech Nagoji cannot follow, translated for the reader (the chapter 4 convention); a line
    already bracketed is left as it is. The script file and parse_script, which the image prompts use, are unchanged.
    """
    script=s.parse_script(path)
    for page in script['pages'].values():
        for panel in page['panels']:
            for chunk in panel.get('copy') or []:
                if _MALAYALAM.search(chunk['speaker']) and not chunk['text'].lstrip().startswith('<'):
                    chunk['text']='<'+chunk['text']+'>'
    return script


def frame_file(record,out):
    """A record's frame: absolute, or relative to the working directory, repository root or package."""
    path=Path(record['path'])
    options=[path] if path.is_absolute() else [Path.cwd()/path,V15.parent.parent/path,out/path]
    for option in options:
        if option.is_file():return option.resolve()
    raise FileNotFoundError(f'candidate frame not found: {record["path"]}')


def _recorded_script(job,out):
    """Recover source-package lettering independently of a later split of its live script."""
    item=job['script'];source=out/SCRIPT_SOURCE;revisions=out/SCRIPT_REVISIONS
    entries=json.loads(revisions.read_text()) if revisions.is_file() else []
    entries=[entry for entry in entries if entry.get('source')==item['path']]
    if source.exists():
        if not source.is_file() or c.sha256(source)!=item['sha256']:
            raise ValueError(f'{SCRIPT_SOURCE} does not match the script the package was prepared from')
        script=s.parse_script(source)
        panels={panel['id']:panel for page in script['pages'].values() for panel in page['panels']}
        for entry in entries:
            # accept_script_revision records text changes against the frozen original,
            # so later entries replace earlier text, even when their "before" is the original.
            for change in entry.get('lettering_changes',[]):
                panel=panels.get(change['panel']);index=change['chunk']
                if (panel is None or type(index) is not int or not 0<=index<len(panel['copy'])
                        or panel['copy'][index]['speaker']!=change['speaker']):
                    raise ValueError(f'Invalid recorded lettering change: {change["panel"]} chunk {index}')
                s._reject_dashes(change['after'], f'recorded lettering {change["panel"]}')
                panel['copy'][index]['text']=change['after']
        return script
    live=Path(item['path'])
    accepted={item['sha256']}|{entry['sha256'] for entry in entries}
    if live.is_file() and c.sha256(live) in accepted:return s.parse_script(live)
    raise ValueError(f'Recorded source script is unavailable or its hash changed: {item["path"]}; '
                     f'{SCRIPT_SOURCE} is missing and the live hash must be recorded or accepted')


def import_frame(args,out):
    """Copy an unchanged candidate to a new panel ID, preserving its generating provenance."""
    from hashlib import sha256
    from io import BytesIO
    from PIL import Image
    job=load_job(out)
    if not all((args.from_package,args.source,args.frame_id)):
        raise ValueError('import-frame needs --from-package --source --frame-id')
    source_out=args.from_package.resolve()
    if source_out==out.resolve():raise ValueError('Cannot import from the same package')
    if not any(item['id']==args.frame_id for item in job['jobs']):
        raise ValueError(f'Unknown target frame: {args.frame_id}')
    stem=re.fullmatch(r'(page-\d+-panel-\d+)-v\d+',args.source)
    if stem is None:raise ValueError('--source must be a source frame stem, such as page-08-panel-04-v03')
    record_path=source_out/'candidates'/f'{args.source}.json'
    record_bytes=record_path.read_bytes();record=json.loads(record_bytes)
    source_job=json.loads((source_out/'IMAGEGEN-JOBS.json').read_text(encoding='utf-8'))
    source_id=record['id']
    if source_id!=stem[1] or not any(item['id']==source_id for item in source_job['jobs']):
        raise ValueError(f'Unknown or mismatched source panel: {source_id}')
    source_copy=dict(_lettering(_recorded_script(source_job,source_out)))
    target_script=job['script']
    if 'pages' not in target_script:target_script=s.parse_script(Path(target_script['path']))
    target_copy=dict(_lettering(target_script))
    if source_id not in source_copy or args.frame_id not in target_copy:
        raise ValueError('Source or target panel is missing from its recorded script')
    if source_copy[source_id]!=target_copy[args.frame_id]:
        raise ValueError(f'Panel lettering differs: {source_id} -> {args.frame_id}')
    source_frame=frame_file(record,source_out)
    frame_bytes=source_frame.read_bytes();digest=sha256(frame_bytes).hexdigest()
    if digest!=record['sha256']:raise ValueError(f'Source frame sha256 mismatch: {source_id}')
    with Image.open(BytesIO(frame_bytes)) as im:width,height=im.size;mode=im.mode
    if mode!='RGB' or (width,height)!=(record['width'],record['height']):
        raise ValueError(f'Source frame RGB/dimensions mismatch: {source_id}')
    candidates=out/'candidates';frames=out/'frames'
    index=1
    while (candidates/f'{args.frame_id}-v{index:02d}.json').exists() or (frames/f'{args.frame_id}-v{index:02d}.png').exists():index+=1
    frame=frames/f'{args.frame_id}-v{index:02d}.png'
    result={'id':args.frame_id,'path':str(frame),'sha256':digest,'width':width,'height':height,
            'generation_tool':record['generation_tool'],'origin':'imported',
            'prompt_path':record['prompt_path'],'prompt_sha256':record['prompt_sha256'],
            'references':record.get('references',[]),'visual_review':'pending',
            'original_generated_path':record.get('original_generated_path',str(source_frame)),
            'imported_from':{'package':str(source_out),'record':str(record_path),
                             'record_sha256':sha256(record_bytes).hexdigest(),'frame_id':source_id}}
    for key in ('base_prompt_path','base_prompt_sha256','moderated_rewrite'):
        if key in record:result[key]=record[key]
    frames.mkdir(parents=True,exist_ok=True)
    with frame.open('xb') as output:output.write(frame_bytes)
    write_json(candidates/f'{args.frame_id}-v{index:02d}.json',result)
    return result


def _draw_kind(speaker):
    return 'caption' if speaker.strip().upper().startswith('CAPTION') else 'speech'


def parse_styles(raw,copy):
    """Per-chunk lettering styles from {copy index: style}: a list with one style or None per chunk."""
    styles=[None]*len(copy)
    if raw is None:return styles
    if not isinstance(raw,dict):raise AutoGeometryError('--styles must be a JSON object of {copy index: style}')
    for key,style in raw.items():
        try:index=int(key)
        except ValueError:raise AutoGeometryError(f'--styles: {key!r} is not a copy index') from None
        if not 0<=index<len(copy):raise AutoGeometryError(f'--styles: copy index {index} is out of range (0 to {len(copy)-1})')
        if style!='unreadable':raise AutoGeometryError(f'--styles: unknown style {style!r} for copy index {index}')
        styles[index]=style
    return styles


def parse_tails(raw,copy,width,height):
    """Each chunk's tail point in source pixels, or None for a caption.

    `raw` is a list (one [x_frac, y_frac] or null per copy index) or a map from copy index
    to [x_frac, y_frac]: the speaker's mouth as fractions of the source image. Every speech
    chunk must have one; a tail point is never guessed.
    """
    if raw is None:raw={}
    if isinstance(raw,list):entries={i:v for i,v in enumerate(raw) if v is not None}
    elif isinstance(raw,dict):
        try:entries={int(k):v for k,v in raw.items()}
        except ValueError:raise AutoGeometryError('--tails map keys must be copy indices') from None
    else:raise AutoGeometryError('--tails must hold a list or a map of [x_frac, y_frac] points')
    points=[None]*len(copy)
    for index,value in entries.items():
        if not 0<=index<len(copy):
            raise AutoGeometryError(f'--tails names chunk {index}, but the panel has {len(copy)} chunk(s)')
        if not(isinstance(value,list) and len(value)==2 and all(isinstance(v,(int,float)) and not isinstance(v,bool) for v in value)):
            raise AutoGeometryError(f'tail for chunk {index} must be [x_frac, y_frac]')
        if not all(0<=v<=1 for v in value):
            raise AutoGeometryError(f'tail for chunk {index} must have fractions between 0 and 1')
        if _draw_kind(copy[index]['speaker'])=='caption':
            raise AutoGeometryError(f'chunk {index} is a caption and takes no tail')
        points[index]=(value[0]*width,value[1]*height)
    for index,chunk in enumerate(copy):
        if _draw_kind(chunk['speaker'])=='speech' and points[index] is None:
            raise AutoGeometryError(f'chunk {index} is speech by {chunk["speaker"]!r} and needs a tail point in --tails '
                '([x_frac, y_frac] of its speaker\'s mouth); the tool never guesses one')
    return points


def parse_keep(raw,width,height):
    """Keep zones as [x0, y0, x1, y1] rectangles in source pixels.

    `raw` is a list of {"x0": frac, "y0": frac, "x1": frac, "y1": frac}: story-critical areas (a gripping hand, a prop, a
    brand) as fractions of the frame's width (x) and height (y). Other keys, such as "what", are ignored. The cover crop keeps
    each zone whole, as it keeps faces; the placer keeps boxes off a zone where it can (reserves.place_boxes `keep`, a soft
    obstacle: a balloon that has no other place covers it, and the plan reports it in "keep_overlaps").
    """
    if raw is None:return []
    if not isinstance(raw,list):
        raise AutoGeometryError('--keep must hold a list of zones, each {"x0": frac, "y0": frac, "x1": frac, "y1": frac}')
    zones=[]
    for index,entry in enumerate(raw):
        numbers=isinstance(entry,dict) and all(isinstance(entry.get(key),(int,float)) and not isinstance(entry.get(key),bool)
                                               for key in ('x0','y0','x1','y1'))
        if not numbers:raise AutoGeometryError(f'keep zone {index} must be {{"x0": frac, "y0": frac, "x1": frac, "y1": frac}}')
        if not(0<=entry['x0']<entry['x1']<=1 and 0<=entry['y0']<entry['y1']<=1):
            raise AutoGeometryError(f'keep zone {index}: fractions must be between 0 and 1, with x0 below x1 and y0 below y1')
        zones.append([entry['x0']*width,entry['y0']*height,entry['x1']*width,entry['y1']*height])
    return zones


def keep_coverage(boxes,keep_px,visible_rect):
    """Share of each keep zone's visible area covered by nonoverlapping box rectangles in source pixels."""
    shares=[]
    for x0,y0,x1,y1 in keep_px:
        x0=max(x0,visible_rect[0]);y0=max(y0,visible_rect[1])
        x1=min(x1,visible_rect[2]);y1=min(y1,visible_rect[3])
        area=max(0,x1-x0)*max(0,y1-y0)
        covered=sum(max(0,min(x1,bx1)-max(x0,bx0))*max(0,min(y1,by1)-max(y0,by0))
                    for bx0,by0,bx1,by1 in boxes)
        shares.append(covered/area if area else 0.0)
    return shares


HEAD_RADIUS=.09      # an implied head zone's radius, as a share of the frame height


def parse_faces(raw,width,height):
    """Face zones as (x, y, radius, name) in source pixels.

    `raw` is a list of {"x": frac, "y": frac, "r": frac} (optionally "name"): a face's centre
    as fractions of the frame, and its radius as a fraction of the frame HEIGHT.
    """
    if raw is None:return []
    if not isinstance(raw,list):
        raise AutoGeometryError('--faces must hold a list of faces, each {"x": frac, "y": frac, "r": frac}')
    faces=[]
    for index,entry in enumerate(raw):
        numbers=isinstance(entry,dict) and all(isinstance(entry.get(key),(int,float)) and not isinstance(entry.get(key),bool)
                                               for key in ('x','y','r'))
        if not numbers:raise AutoGeometryError(f'face {index} must be {{"x": frac, "y": frac, "r": frac}}')
        if not(0<=entry['x']<=1 and 0<=entry['y']<=1 and 0<entry['r']<=1):
            raise AutoGeometryError(f'face {index}: x and y must be between 0 and 1, and r above 0 and at most 1')
        name=entry.get('name') if isinstance(entry.get('name'),str) and entry['name'] else f'face {index}'
        faces.append((entry['x']*width,entry['y']*height,entry['r']*height,name))
    return faces


def head_zones(tails,faces,bounds,height):
    """The head every tail point implies: a zone centred half a radius above the mouth.

    The radius is 0.09 of the frame height. A tail point on the frame's edge is an off-frame
    speaker with no head in the frame, and one that a given face already covers needs no extra zone.
    """
    import math
    import reserves as rv
    zones=[];radius=HEAD_RADIUS*height
    for index,point in enumerate(tails):
        if point is None or rv.on_frame_edge(point,bounds):continue
        if any(math.hypot(point[0]-face[0],point[1]-face[1])<=face[2] for face in faces):continue
        if any(math.hypot(point[0]-zone[0],point[1]-(zone[1]+.5*radius))<=.5*radius for zone in zones):continue   # same speaker
        zones.append((point[0],point[1]-.5*radius,radius,f"head of chunk {index}'s speaker"))
    return zones


def _painted_extent(region):
    """The [x0, y0, x1, y1] rectangle holding a painted region's pixels: its blank shape plus its outline."""
    (x,y),(h,w)=region['painted']['origin'],region['painted']['mask'].shape;return [x,y,x+w,y+h]


def _crop_keep(faces,heads,tails,regions,art,zones=()):
    """What the cover crop must hold, as [x0, y0, x1, y1] source rectangles.

    The bounding box of every face and head zone, the pixels of every painted region (its blank shape plus its
    outline), every keep zone (see parse_keep), and a small square around each tail point that is not on the art's
    edge. A tail point on the edge is an off-frame speaker and is not kept (see _pin_tails).
    """
    import reserves as rv
    keep=[[x-radius,y-radius,x+radius,y+radius] for x,y,radius,_ in list(faces)+list(heads)]
    keep+=[_painted_extent(region) for region in regions]
    keep+=[list(zone) for zone in zones]
    for point in tails:
        if point is not None and not rv.on_frame_edge(point,art):
            m=rv.TAIL_MARGIN_PX;keep.append([point[0]-m,point[1]-m,point[0]+m,point[1]+m])
    return keep


def _pin_tails(tails,art,crop):
    """Tail points on the art's edge belong to off-frame speakers: where the crop cut that edge away, move them onto the crop's."""
    import reserves as rv
    pinned=[]
    for point in tails:
        if point is not None and rv.on_frame_edge(point,art):
            x,y=point
            if crop[0]>art[0]:x=max(x,crop[0])
            if crop[2]<art[2]:x=min(x,crop[2])
            if crop[1]>art[1]:y=max(y,crop[1])
            if crop[3]<art[3]:y=min(y,crop[3])
            point=(x,y)
        pinned.append(point)
    return pinned


def _widener(interior_pt,scale):
    """need(height_px, corner ratio) -> px: the width a balloon of that height needs to keep `interior_pt` of text width.

    A balloon's text area is inset by its padding plus a corner clearance that grows with its shorter
    side (compositor.drawn_text_inset), so a box made taller than the text needs, by the painted region
    it covers, has a narrower text area and the copy would re-wrap. The width comes from the same corner
    rule, exactly (a fixed point, as in compositor.drawn_box_size). drawn_box_size adds .05 pt of slack
    to the interior; the fit check needs only the widest line plus 4 pt, so that slack is not asked for
    and a box that passed the fit check without it stays as it was.
    """
    from math import ceil
    required=interior_pt-.05
    def need(height_px,ratio):
        height=height_px*scale;width=required+2*c.DRAW_PAD_PT
        for _ in range(12):width=required+2*c.drawn_text_inset('speech',width,height,ratio)
        return ceil(width/scale)
    return need


UNPAINTED=False   # --unpainted: the chapter's art has no painted balloons, so drawn_geometry and fit_inputs find no painted regions


def drawn_geometry(frame,copy,slot,tails,faces=None,styles=None,keep=None,unpainted=None):
    """Boxes for the compositor to draw, one per chunk, sized for the text at the panel's placed size.

    Each box holds its wrapped text plus padding. Where a painted blank region exists in
    reading order the box is centred on it and covers its bounding box plus 8 px; otherwise
    it goes in the quietest clear space. A box never covers a tail point (its own or another
    chunk's) or comes within 3 pt of one: it is grown away from the point, narrower wraps are
    tried when that is not enough, and a painted region that itself contains a tail point is
    only partly covered (reported as "partly_covered"). A tail point on the frame's edge is an
    off-frame speaker and never blocks anything. When neighbouring boxes collide, narrower
    wraps are tried too. The wrap width starts at the larger of the painted region's width and
    36 percent of the visible width, and is never narrower than the longest word. A balloon over
    a painted region also hides every painted pixel at its rounded corners: its box grows, or its
    corner radius drops (reserve "corner", never below 40 percent of the shorter side), whichever
    keeps it smaller. Where its painted region touches a frame edge (within 6 pt) and that is not
    enough, the balloon may run off that edge (clipped at the panel), by no more than needed and
    never so far that its text area and padding leave the frame; "bleeds" reports those chunks and
    the pixels past the frame on each side. A box never covers a face: `faces` (see parse_faces) and
    the head every tail point implies (see head_zones) are kept clear of the balloon's rounded shape
    and any bleed, for painted and unpainted chunks alike, and a chunk that cannot be placed
    without covering one fails saying it "would cover a face". A balloon that must cover a painted
    region taller than its text needs is widened so its text area keeps the width its wrap was sized
    for (a taller rounded shape has more corner clearance); the widened box is checked like any other. "face_clearance" reports, for each
    box, the distance to the nearest face. A balloon's tail reads as pointing at its own speaker: it never crosses another
    balloon or a face that is not the speaker's, a balloon with no painted region goes near its speaker, and the boxes read in
    script order (see reserves.place_boxes). When none of this works the chunk fails. A balloon's tail reads as pointing at
    whoever its drawn tip lands nearest, so the tip never ends nearer another face than its speaker's.

    Two soft wishes are met where any position allows and dropped, as they always were, where none does. A balloon for a
    voice off frame (a tail point on the frame's edge) keeps TAIL_MIN_PT plus the stroke between it and that edge so the
    compositor draws a tail ("edge_voice_no_tail" lists the chunks that could not). The `keep` zones are avoided by
    every box (a tenth of a zone may be covered; "keep_overlaps" maps the chunks that cover more to the zones' indexes).

    Before any of that the frame is cover-cropped toward the slot's shape (reserves.cover_crop): the crop
    keeps every face, every head a tail implies, every painted region, every `keep` zone (source-pixel rectangles,
    see parse_keep: a prop or a gripping hand; boxes keep off them where they can, see above) and every on-frame
    tail point, and at least reserves.MIN_KEEP of the art's height or width, and everything above works inside it. The result's
    "visible_rect" is the crop and "art_rect" the uncropped art. A tail point on the art's edge (an off-frame
    speaker) is not kept; where the crop cut that edge away the point is moved onto the crop's edge.
    With `unpainted` (default: the module's UNPAINTED, set by --unpainted) the frame has no painted regions: art generated
    with no balloons can still hold a pale outlined area (open sky between a pillar and a roof), which is space for
    lettering, not a painted blank a balloon must cover.
    """
    import reserves as rv
    from math import ceil
    unpainted=UNPAINTED if unpainted is None else unpainted
    aspect=slot['rect_pt'][2]/slot['rect_pt'][3]
    if not copy:
        base=rv.detect_reserves(frame,0,[]);art=base['visible_rect']
        return {**base,'visible_rect':rv.cover_crop(art,aspect,_crop_keep(faces or [],[],[],[],art,keep or [])),'art_rect':art,
                'painted':[],'partly_covered':[],'bleeds':{},'face_clearance':{},'head_zones':[],'keep_overlaps':{},
                'edge_voice_no_tail':[]}
    found=rv.find_regions(frame,0 if unpainted else len(copy))
    width,height=found['size'];art=found['visible_rect'];faces=list(faces or [])
    crop=rv.cover_crop(art,aspect,_crop_keep(faces,head_zones(tails,faces,art,height),tails,found['regions'],art,keep or []))
    tails=_pin_tails(tails,art,crop);found['visible_rect']=bounds=crop
    row={'width':width,'height':height,'visible_rect':bounds}
    clip,_=c.fit_clip_contain(row,slot)
    scale=c.measure([width,height],bounds,clip)['matrix'][0]/width        # points per source pixel
    options,widen=[],[]
    for index,chunk in enumerate(copy):
        region=found['regions'][index] if index<len(found['regions']) else None
        wrap=max((region['bbox'][2]-region['bbox'][0]) if region else 0,.36*(bounds[2]-bounds[0]))*scale
        kind=_draw_kind(chunk['speaker'])
        sizes,needs=[],[]
        for _ in range(14):
            box=c.drawn_box_size(chunk['text'],kind,wrap,style=(styles or [None]*len(copy))[index])
            size=(ceil(box['shape_pt'][0]/scale)+1,ceil(box['shape_pt'][1]/scale)+1)
            if size not in sizes:
                sizes.append(size);needs.append(_widener(box['interior_pt'][0],scale) if kind=='speech' else None)
            wrap*=.85
        options.append(sizes);widen.append(needs)
    margin=max(6,ceil(3.0/scale))         # a visible tail needs about 3 pt between the box and the mouth
    # A balloon is rounded, so over a painted region its box grows (or its corner radius shrinks) until no
    # painted pixel shows at a corner; a caption is a rectangle and needs nothing.
    rounded=[(c.BALLOON_RADIUS_RATIO,c.BALLOON_MIN_RATIO) if _draw_kind(chunk['speaker'])=='speech' else None for chunk in copy]
    touch=ceil(6.0/scale)                 # a painted region within 6 pt of a frame edge touches it, for bleed
    heads=head_zones(tails,faces,bounds,height)
    try:plan=rv.place_boxes(frame,found,options,tails,tail_margin=margin,rounded=rounded,bleed=touch,
                            faces=faces+heads,face_margin=ceil(1.5/scale),widen=widen,scale=scale,keep=keep)
    except rv.PlacementError as error:raise AutoGeometryError(str(error)) from error
    reserves=[]
    for index,(chunk,box) in enumerate(zip(copy,plan['boxes'])):
        kind=_draw_kind(chunk['speaker'])
        reserve={'kind':kind,'draw':kind,'rect':[int(v) for v in box],'copy_indices':[index]}
        if styles and styles[index]:reserve['style']=styles[index]
        ratio=plan['corner'][index]
        if ratio is not None and ratio<c.BALLOON_RADIUS_RATIO-1e-9:reserve['corner']=round(ratio,3)
        if tails[index] is not None:
            tx,ty=tails[index]
            if not rv.on_frame_edge((tx,ty),bounds) and box[0]<=tx<=box[2] and box[1]<=ty<=box[3]:
                raise AutoGeometryError(f'chunk {index}: its tail point lies inside its box, so the balloon would cover the '
                    'speaker\'s mouth; move the tail point outside the space the balloon needs')
            reserve['tail']=[round(tx),round(ty)]
        reserves.append(reserve)
    return {'visible_rect':plan['visible_rect'],'art_rect':art,'reserves':reserves,'painted':plan['painted'],
            'partly_covered':[index for index,cut in enumerate(plan['partial']) if cut],
            'bleeds':{index:amounts for index,amounts in enumerate(plan['bleed']) if any(amounts)},
            'face_clearance':{index:{'px':round(gap,1),'pt':round(gap*scale,2),'face':name}
                              for index,near in enumerate(plan['face_clearance']) if near for gap,name in [near]},
            'head_zones':[zone[3] for zone in heads],'keep_overlaps':plan['keep_overlaps'],
            'edge_voice_no_tail':plan['edge_voice_no_tail']}


def auto_geometry(args,out):
    """Measure a candidate's blank reserves and write geometry only if every chunk fits.

    Detects one blank outlined area per copy chunk, then applies the compositor's own fit
    measurement at the panel's placed size (LAYOUT.json page_rows if present, else the
    default rows) and the native light-pixel audit the build performs.
    """
    import reserves as rv
    from types import SimpleNamespace
    if not args.candidate or not args.geometry_out:
        raise AutoGeometryError('auto-geometry needs --candidate and --geometry-out')
    if args.geometry_out.exists():
        raise AutoGeometryError(f'geometry file already exists: {args.geometry_out}')
    job=load_job(out);script=lettered_script(Path(job['script']['path']))
    record=json.loads(args.candidate.read_text())
    panel={p['id']:p for page in script['pages'].values() for p in page['panels']}.get(record.get('id'))
    if panel is None:
        raise AutoGeometryError(f'{record.get("id")} is not a panel of chapter {args.chapter}')
    copy=panel['copy'];frame=frame_file(record,out)
    if getattr(args,'layout',None):layout=json.loads(args.layout.read_text())     # rows to try, instead of LAYOUT.json
    else:
        layout_path=out/'LAYOUT.json'
        layout=json.loads(layout_path.read_text()) if layout_path.exists() else {}
    geometry=c.geometry_for_script(script,layout.get('page_rows'))
    inset=args.inset if getattr(args,'inset',None) is not None else rv.INSET_PX
    painted=partly=bleeds=clearance=heads=keeps=voices=None
    coverage={}
    if getattr(args,'draw',False):
        if getattr(args,'inset',None) is not None:raise AutoGeometryError('--inset does not apply with --draw')
        from PIL import Image
        with Image.open(frame) as image:width,height=image.size
        raw=json.loads(args.tails.read_text()) if getattr(args,'tails',None) else None
        faces=parse_faces(json.loads(args.faces.read_text()) if getattr(args,'faces',None) else None,width,height)
        slot=next(p for p in geometry['pages'][str(panel['page'])] if p['id']==panel['id'])
        styles=parse_styles(json.loads(args.styles.read_text()) if getattr(args,'styles',None) else None,copy)
        keep=parse_keep(json.loads(args.keep.read_text()) if getattr(args,'keep',None) else None,width,height)
        try:plan=drawn_geometry(frame,copy,slot,parse_tails(raw,copy,width,height),faces,styles,keep)
        except AutoGeometryError as error:raise AutoGeometryError(f'{panel["id"]}: {error}') from error
        found={'visible_rect':plan['visible_rect'],'art_rect':plan['art_rect'],'reserves':plan['reserves']}
        painted=plan['painted'];inset=None
        partly=plan['partly_covered'];bleeds=plan['bleeds'];clearance=plan['face_clearance'];heads=plan['head_zones']
        keeps=plan['keep_overlaps'];voices=plan['edge_voice_no_tail']
        coverage={'keep_coverage':keep_coverage([reserve['rect'] for reserve in plan['reserves']],keep,plan['visible_rect'])}
    else:
        if getattr(args,'tails',None):raise AutoGeometryError('--tails needs --draw')
        if getattr(args,'faces',None):raise AutoGeometryError('--faces needs --draw')
        if getattr(args,'styles',None):raise AutoGeometryError('--styles needs --draw')
        if getattr(args,'keep',None):raise AutoGeometryError('--keep needs --draw')
        try:found=rv.detect_reserves(frame,len(copy),[chunk['speaker'] for chunk in copy],inset=inset)
        except rv.ReserveError as error:raise AutoGeometryError(f'{panel["id"]}: {error}') from error
    row=dict(record);row['path']=str(frame);row.update(found)
    measurements=c.copy_fit_measurements([row],script,geometry,
        SimpleNamespace(B=SimpleNamespace(measure=c.measure)),reject_failures=False)
    for m in measurements:
        if not m['fits']:
            index=m['copy_indices'][0];_,_,w,h=m['rect_pt']
            raise AutoGeometryError(
                f'copy does not fit its reserve in {panel["id"]}: chunk {index} needs {len(m["lines"])} line(s) '
                f'but the reserve is {w:.0f} x {h:.0f} pt at the placed size: {copy[index]["text"][:60]!r}')
    try:pixels=audit_reserve_pixels([row],geometry,measurements)
    except ValueError as error:raise AutoGeometryError(f'{panel["id"]}: {error}') from error
    write_json(args.geometry_out,found)
    return {'geometry_out':str(args.geometry_out),'panel':panel['id'],'frame':str(frame),
            'visible_rect':found['visible_rect'],'inset_px':inset,'reserves':found['reserves'],
            'draw':painted is not None,'painted':painted,'partly_covered':partly,'bleeds':bleeds,
            'face_clearance':clearance,'head_zones':heads,'keep_overlaps':keeps,**coverage,'edge_voice_no_tail':voices,
            'tightest_ink_margin_pt':min((min(m['ink_margins_pt'].values()) for m in measurements),default=None),
            'minimum_light_fraction':pixels['minimum_light_fraction']}


FACE_SCALE=1.0      # <stem>-faces.json radii are already scaled by the assembler (0.55 of whole-head zones)


class LayoutFitError(ValueError):
    """fit-layout could not read its inputs or write its layout."""


@functools.lru_cache(maxsize=None)
def _painted_extents(path,mtime,size,count):
    import reserves as rv
    return tuple(tuple(_painted_extent(region)) for region in rv.find_regions(path,count)['regions'])


def painted_keep(frame,count):
    """The rectangles the planner keeps in the crop for a frame's painted regions: [x0, y0, x1, y1] source pixels.

    The extent of each painted region find_regions finds for `count` copy chunks, as _crop_keep takes it. find_regions is
    slow, so the answer is kept per frame file (by its path, modification time and size) and chunk count.
    """
    info=Path(frame).stat()
    return [list(rect) for rect in _painted_extents(str(frame),info.st_mtime_ns,info.st_size,count)]


def fit_inputs(out,manifest,decisions=None,faces_dir=None,face_scale=FACE_SCALE,script=None,unpainted=None):
    """The frames, face zones, painted regions and keep zones layout_fit needs, per panel id.

    A selection manifest's `frames` come first. `decisions` (a file with a `decisions` list, or a
    manifest that holds one) supplies the picked candidate for panels the manifest lacks; its frame
    is measured with the same art_bounds the planner uses. A frame's "visible_rect" here is the
    uncropped art: a row or candidate record written by the cover-cropping planner carries the crop
    for one slot as its visible_rect, so its "art_rect" is preferred when it has one. A face file
    `<frame stem>-faces.json` in `faces_dir` gives that panel's faces, with every radius multiplied
    by `face_scale`; a `<frame stem>-keep.json` there gives its keep zones (see parse_keep).
    With the parsed `script`, each panel that has copy also gets the painted regions the planner would keep in
    its crop (painted_keep of its frame for its number of chunks), since its balloons must hide them; a silent
    panel has none, and without a script none are measured. With `unpainted` (default: the module's UNPAINTED) no panel has any.
    Returns {"frames", "faces", "painted", "keep", "sources", "stems"}, each of faces, painted and keep mapping a panel
    id to [x0, y0, x1, y1] (painted, keep) or (x, y, r) (faces) as fractions of its frame; a panel with no frame is absent
    from "frames".
    """
    import numpy as np
    import reserves as rv
    from PIL import Image
    payload=json.loads(Path(manifest).read_text())
    frames,sources,stems={},{},{}
    for row in payload.get('frames') or []:
        frames[row['id']]={'visible_rect':row.get('art_rect') or row['visible_rect'],'width':row['width'],'height':row['height'],
                           'path':str(frame_file(row,out))}
        sources[row['id']]='manifest';stems[row['id']]=Path(row['path']).stem
    picks=list(payload.get('decisions') or [])
    if decisions is not None:picks+=json.loads(Path(decisions).read_text()).get('decisions') or []
    for decision in picks:
        panel_id,pick=decision.get('id'),decision.get('pick')
        if not pick or panel_id in frames:continue
        record_path=out/'candidates'/f'{panel_id}-{pick}.json'
        if not record_path.is_file():raise LayoutFitError(f'{panel_id}: picked {pick} has no candidate record {record_path}')
        record=json.loads(record_path.read_text());path=frame_file(record,out)
        with Image.open(path) as image:
            width,height=image.size
            visible=record.get('art_rect') or record.get('visible_rect') or rv.art_bounds(np.asarray(image.convert('RGB')))
        frames[panel_id]={'visible_rect':list(visible),'width':width,'height':height,'path':str(path)}
        sources[panel_id]=f'pick {pick}';stems[panel_id]=f'{panel_id}-{pick}'
    faces={}
    if faces_dir is not None:
        for panel_id,stem in stems.items():
            path=Path(faces_dir)/f'{stem}-faces.json'
            if path.is_file():
                try:zones=[(x,y,radius*face_scale) for x,y,radius,_ in parse_faces(json.loads(path.read_text()),1,1)]
                except AutoGeometryError as error:raise LayoutFitError(f'{path}: {error}') from error
                if zones:faces[panel_id]=zones
    keep={}
    if faces_dir is not None:
        for panel_id,stem in stems.items():
            path=Path(faces_dir)/f'{stem}-keep.json'
            if path.is_file():
                try:zones=parse_keep(json.loads(path.read_text()),1,1)
                except AutoGeometryError as error:raise LayoutFitError(f'{path}: {error}') from error
                if zones:keep[panel_id]=zones
    painted={}
    if UNPAINTED if unpainted is None else unpainted:script=None
    chunks={p['id']:len(p.get('copy') or []) for page in (script or {'pages':{}})['pages'].values() for p in page['panels']}
    for panel_id,frame in frames.items():
        if not chunks.get(panel_id):continue
        rects=painted_keep(frame['path'],chunks[panel_id])
        if rects:painted[panel_id]=[[x0/frame['width'],y0/frame['height'],x1/frame['width'],y1/frame['height']] for x0,y0,x1,y1 in rects]
    return {'frames':frames,'faces':faces,'painted':painted,'keep':keep,'sources':sources,'stems':stems}


def drawn_fits(row,panel,slot,tails,faces,script,keep_max=None):
    """Whether the drawn-balloon planner places `panel`'s copy in `slot` and the fit check passes.

    This is auto-geometry's own plan, fit measurement and pixel audit, without writing a file.
    `row` holds the frame's id, path, width and height, and optionally "keep", the panel's keep zones in source pixels.
    With `keep_max`, no zone's visible area may be covered beyond that share by the placed boxes.
    """
    from types import SimpleNamespace
    geometry={'pages':{str(panel['page']):[slot]}}
    try:plan=drawn_geometry(Path(row['path']),panel['copy'],slot,tails,faces,keep=row.get('keep'))
    except AutoGeometryError:return False
    if keep_max is not None and row.get('keep'):
        shares=keep_coverage([reserve['rect'] for reserve in plan['reserves']],row['keep'],plan['visible_rect'])
        if any(share>keep_max for share in shares):return False
    found=dict(row);found.update({'visible_rect':plan['visible_rect'],'reserves':plan['reserves']})
    try:
        measured=c.copy_fit_measurements([found],script,geometry,SimpleNamespace(B=SimpleNamespace(measure=c.measure)),
                                         reject_failures=False)
        if not all(m['fits'] for m in measured):return False
        audit_reserve_pixels([found],geometry,measured)
    except ValueError:return False
    return True


PROBE_STEP_PT=5.0
PROBE_ROUNDS=6


class SlotProbe:
    """Asks the planner whether a panel's copy can be placed at a row height. Answers are cached."""

    def __init__(self,script,inputs,tails_dir,keep_max=None):
        self.script=script;self.keep_max=keep_max
        self.panels={p['id']:p for page in script['pages'].values() for p in page['panels']}
        self.frames=inputs['frames'];self.faces=inputs['faces'];self.keep=inputs.get('keep') or {};self.cache={};self.calls=0;self.tails={}
        for panel_id,stem in inputs['stems'].items():
            path=Path(tails_dir)/f'{stem}-tails.json'
            if path.is_file() and self.panels.get(panel_id,{}).get('copy'):self.tails[panel_id]=json.loads(path.read_text())

    def probed(self,panel_id):return panel_id in self.tails

    def fits(self,panel_id,width_pt,height_pt):
        key=(panel_id,round(width_pt,3),round(height_pt,3))
        if key not in self.cache:
            self.calls+=1
            panel=self.panels[panel_id];frame=self.frames[panel_id]
            row={'id':panel_id,'path':frame['path'],'width':frame['width'],'height':frame['height']}
            if panel_id in self.keep:row['keep']=[[x0*frame['width'],y0*frame['height'],x1*frame['width'],y1*frame['height']]
                                                  for x0,y0,x1,y1 in self.keep[panel_id]]
            tails=parse_tails(self.tails[panel_id],panel['copy'],frame['width'],frame['height'])
            faces=parse_faces([{'x':x,'y':y,'r':radius} for x,y,radius in self.faces.get(panel_id,[])],
                              frame['width'],frame['height'])
            slot={'id':panel_id,'rect_pt':[c.ART_X_PT,c.ART_Y_PT,width_pt,height_pt]}
            options={} if self.keep_max is None else {'keep_max':self.keep_max}
            self.cache[key]=drawn_fits(row,panel,slot,tails,faces,self.script,**options)
        return self.cache[key]

    def first_fit(self,panel_id,width_pt,low_pt,high_pt,step_pt=PROBE_STEP_PT):
        """The smallest height on a grid from `low_pt` (and `high_pt` itself) at which the panel is placed, or None."""
        height=low_pt
        while height<high_pt:
            if self.fits(panel_id,width_pt,height):return height
            height+=step_pt
        return high_pt if self.fits(panel_id,width_pt,high_pt) else None

    def nearest_fit(self,panel_id,width_pt,around_pt,low_pt,high_pt,step_pt=1.0):
        """The height within bounds closest to `around_pt` (upward first) at which the panel is placed, or None."""
        for offset in range(1,int((high_pt-low_pt)/step_pt)+2):
            for height in (around_pt+offset*step_pt,around_pt-offset*step_pt):
                if low_pt<=height<=high_pt and self.fits(panel_id,width_pt,round(height,1)):return round(height,1)
        return None


def probe_fit(lf,script,prior,inputs,tails_dir,margin,step_pt=PROBE_STEP_PT,probe=None,minimums=None,keep_max=None):
    """Fit with planner-proved floors: each row is given at least the height its panels need, then verified.

    Each probed panel is scanned upward from its row's lower bound, in `step_pt` steps, for the first
    height the planner places it at (its floor). The fit is then verified at the heights it chose; a
    panel that fails there (placement is not monotone in height, and a window can fall between scan
    steps) is pinned to the nearest height that works, searching 1 pt at a time, and the fit repeated.
    A panel that no height within its bounds places is left to the ratio fit and reported.
    `minimums` maps a panel id to a height a script size cue asks of its row: the scan starts there and
    layout_fit.fit_layout gives the row at least that. `probe` is a SlotProbe to reuse, so that fits of
    several candidate structures share the planner's answers (its `calls` then counts all of them).
    """
    probe=probe or SlotProbe(script,inputs,tails_dir,keep_max=keep_max)
    minimums=minimums or {}
    layout=lf.structure(script,prior)
    rows=[(page,row) for page,rows_ in layout.items() for row in rows_]

    def lowest(row):
        return min(max([row['min_pt']]+[minimums.get(panel_id,0) for panel_id in row['panels']]),row['max_pt'])

    floors,ceilings,pins,off_grid,gave_up={},{},{},set(),set()
    for _,row in rows:
        for panel_id in row['panels']:
            if not probe.probed(panel_id):continue
            found=probe.first_fit(panel_id,row['width_pt'],lowest(row),row['max_pt'],step_pt)
            if found is None:off_grid.add(panel_id)
            else:floors[panel_id]=found
    initial=dict(floors)

    def chosen(fitted,page,row):
        height=fitted['page_rows'][page][layout[page].index(row)]
        return height[0] if isinstance(height,list) else height

    for round_number in range(1,PROBE_ROUNDS+1):
        fitted=lf.fit_layout(script,prior,inputs['frames'],inputs['faces'],margin=margin,floors=floors,ceilings=ceilings,
                             painted=inputs.get('painted'),keep=inputs.get('keep'),minimums=minimums)
        failed=[(panel_id,row,chosen(fitted,page,row)) for page,row in rows for panel_id in row['panels']
                if probe.probed(panel_id) and panel_id not in gave_up
                and not probe.fits(panel_id,row['width_pt'],chosen(fitted,page,row))]
        if not failed or round_number==PROBE_ROUNDS:break
        for panel_id,row,height in failed:
            pin=probe.nearest_fit(panel_id,row['width_pt'],height,lowest(row),row['max_pt'])
            if pin is None:
                gave_up.add(panel_id);floors.pop(panel_id,None);ceilings.pop(panel_id,None)
            else:floors[panel_id]=ceilings[panel_id]=pins[panel_id]=pin
    verified={panel_id:probe.fits(panel_id,row['width_pt'],chosen(fitted,page,row))
              for page,row in rows for panel_id in row['panels'] if probe.probed(panel_id)}
    fitted['report']['probe']={'step_pt':step_pt,'planner_calls':probe.calls,'rounds':round_number,
        'floors':initial,'pins':pins,'verified':verified,
        'unplaceable':sorted(panel_id for panel_id,ok in verified.items() if not ok),
        'off_grid':sorted(panel_id for panel_id in off_grid if verified.get(panel_id)),
        'unprobed':sorted(panel_id for _,row in rows for panel_id in row['panels']
                          if not probe.probed(panel_id) and probe.panels[panel_id]['copy'])}
    return fitted


def _structure_page(page_no,page,prior,inputs,tails_dir,margin,unpainted,keep_max=None):
    """Spawn worker: return one page's rows, structure report, probe reports and total planner calls."""
    import layout_fit as lf
    global UNPAINTED
    UNPAINTED=unpainted
    script={'pages':{page_no:page}}
    probe=SlotProbe(script,inputs,tails_dir,keep_max=keep_max);probed={}

    def refine(page_no,page,entry,minimums):
        fitted=probe_fit(lf,{'pages':{page_no:page}},{page_no:entry},inputs,tails_dir,margin,probe=probe,minimums=minimums,
                         keep_max=keep_max)
        sizes=tuple(len(row) if isinstance(row,list) else 1 for row in fitted['page_rows'][page_no])
        probed[(page_no,sizes)]=fitted['report']['probe']
        return fitted,all(fitted['report']['probe']['verified'].values())

    fitted=lf.fit_structures(script,{page_no:prior},inputs['frames'],inputs['faces'],margin=margin,
                             painted=inputs['painted'],keep=inputs['keep'],refine=refine)
    return fitted['page_rows'][page_no],fitted['report']['pages'][page_no],probed,probe.calls


def structure_fit(lf,script,prior,inputs,tails_dir,margin,probing,jobs=1,keep_max=None):
    """fit-layout --structures: choose each page's rows (which panels share a row) as well as their heights.

    With `probing`, the planner is asked about the top candidates of each page (layout_fit.PROBE_TOP): each is
    probe_fit at its own widths, sharing a SlotProbe within each page, and the best one the planner verifies is chosen. The report's
    "probe" section is then the chosen candidates' (floors, pins, verified, ...), with the planner calls of all.
    With probing and `jobs > 1`, pages run in spawned processes, capped at the number of pages, and results are
    assembled in script order. `jobs <= 1` keeps the in-process shared probe; without probing `jobs` has no effect.
    """
    frames,faces,painted,keep=inputs['frames'],inputs['faces'],inputs['painted'],inputs['keep']
    if not probing:return lf.fit_structures(script,prior,frames,faces,margin=margin,painted=painted,keep=keep)
    if jobs>1:
        page_rows,pages,probed={},{},{};planner_calls=0
        if script['pages']:
            with concurrent.futures.ProcessPoolExecutor(max_workers=min(jobs,len(script['pages'])),
                                                       mp_context=multiprocessing.get_context('spawn')) as pool:
                futures=[(str(page_no),pool.submit(_structure_page,str(page_no),page,(prior or {}).get(str(page_no)),
                                                   inputs,tails_dir,margin,UNPAINTED,keep_max))
                         for page_no,page in script['pages'].items()]
                for page_no,future in futures:
                    page_rows[page_no],pages[page_no],found,calls=future.result()
                    probed.update(found);planner_calls+=calls
        fitted=lf.assemble_structures(page_rows,pages,margin,lf.PROBE_TOP)
    else:
        probe=SlotProbe(script,inputs,tails_dir,keep_max=keep_max);probed={}

        def refine(page_no,page,entry,minimums):
            fitted=probe_fit(lf,{'pages':{page_no:page}},{page_no:entry},inputs,tails_dir,margin,probe=probe,minimums=minimums,
                             keep_max=keep_max)
            sizes=tuple(len(row) if isinstance(row,list) else 1 for row in fitted['page_rows'][page_no])
            probed[(page_no,sizes)]=fitted['report']['probe']
            return fitted,all(fitted['report']['probe']['verified'].values())

        fitted=lf.fit_structures(script,prior,frames,faces,margin=margin,painted=painted,keep=keep,refine=refine)
        planner_calls=probe.calls
    chosen=[probed[(page_no,tuple(page['structure']['chosen']))] for page_no,page in fitted['report']['pages'].items()]
    merged={'step_pt':PROBE_STEP_PT,'planner_calls':planner_calls,'rounds':max((found['rounds'] for found in chosen),default=0),
            'floors':{},'pins':{},'verified':{},'unplaceable':[],'off_grid':[],'unprobed':[]}
    for found in chosen:
        for key in ('floors','pins','verified'):merged[key].update(found[key])
        for key in ('unplaceable','off_grid','unprobed'):merged[key]+=found[key]
    for key in ('unplaceable','off_grid','unprobed'):merged[key].sort()
    fitted['report']['probe']=merged
    return fitted


def fit_layout_command(args,out):
    """Re-balance the prior layout's row heights for the lettering each panel carries; write a new layout file."""
    import layout_fit as lf
    missing=[flag for flag,value in (('--manifest',args.manifest),('--layout',args.layout),('--layout-out',args.layout_out))
             if value is None]
    if missing:raise LayoutFitError('fit-layout needs '+', '.join(missing))
    if args.layout_out.exists():raise LayoutFitError(f'layout file already exists: {args.layout_out}')
    prior=json.loads(args.layout.read_text()).get('page_rows')
    if not isinstance(prior,dict):raise LayoutFitError(f'{args.layout} has no page_rows')
    job=load_job(out);script=lettered_script(Path(job['script']['path']))
    face_scale=FACE_SCALE if args.face_scale is None else args.face_scale
    margin=lf.MARGIN if args.margin is None else args.margin
    if not(face_scale>0 and margin>0):raise LayoutFitError('--face-scale and --margin must be above 0')
    if args.probe and args.faces_dir is None:
        raise LayoutFitError('--probe needs --faces-dir, which holds each frame\'s <stem>-tails.json and -faces.json')
    inputs=fit_inputs(out,args.manifest,args.decisions,args.faces_dir,face_scale,script)
    keep_max=getattr(args,'keep_max',None)
    if args.structures:fitted=structure_fit(lf,script,prior,inputs,args.faces_dir,margin,args.probe,jobs=args.jobs,keep_max=keep_max)
    elif args.probe:fitted=probe_fit(lf,script,prior,inputs,args.faces_dir,margin,keep_max=keep_max)
    else:fitted=lf.fit_layout(script,prior,inputs['frames'],inputs['faces'],margin=margin,painted=inputs['painted'],keep=inputs['keep'])
    source={'layout':str(args.layout),'layout_sha256':c.sha256(args.layout),'manifest':str(args.manifest),
            'margin':margin,'face_scale':face_scale}
    if args.structures:source['structures']=True
    tolerance={} if keep_max is None else {'keep_max':keep_max}
    source.update(tolerance)
    write_json(args.layout_out,{'page_rows':fitted['page_rows'],'fitted_from':source})
    return {'layout_out':str(args.layout_out),**fitted['report'],'face_scale':face_scale,'sources':inputs['sources'],
            'faces':sorted(inputs['faces']),'painted':sorted(inputs['painted']),'keep':sorted(inputs['keep']),**tolerance}


def build(args,out):
    job=load_job(out);script=lettered_script(Path(job['script']['path']))
    if args.manifest:
        payload=json.loads(args.manifest.read_text());rows=payload['frames']
    else:rows=selected_rows(out,job)
    c.validate_selection(rows,script,out)
    layout=json.loads(args.layout.read_text()) if args.layout else {}
    geometry=c.geometry_for_script(script,layout.get('page_rows'))
    rows,upscales=c.dpi_gate(rows,geometry,out,args.upscale_python,args.upscale_script)
    upscales=[action for row in rows for action in row.get('transforms',[])]
    c.validate_selection(rows,script,out)
    from types import SimpleNamespace
    measurements=c.copy_fit_measurements(rows,script,geometry,SimpleNamespace(B=SimpleNamespace(measure=c.measure)))
    pixels=audit_reserve_pixels(rows,geometry,measurements)
    manifest={'schema_version':2,'chapter':args.chapter,'generation_tool':'built-in imagegen',
        'status':'selected_for_verified_pdf_assembly','script':job['script'],
        'continuity':job['continuity'],'character_lock':job['character_lock'],
        'page_count':script['page_count'],'frame_count':len(rows),'frames':rows,
        'geometry':geometry,'upscales':upscales}
    final_manifest=out/f'SELECTION-MANIFEST-{args.revision}.json'
    write_json(final_manifest,manifest)
    pdf=out/'pdf'/f'Horse-of-the-Servant-V15-Chapter-{args.chapter:02d}-{args.revision}.pdf'
    composition=c.compose(rows,script,geometry,pdf,first_folio=args.first_folio,chapter=args.chapter)
    report=c.verify_pdf(pdf,rows,script,composition['placements'],args.first_folio)
    report['upscales']=upscales
    report['manifest_path']=str(final_manifest);report['manifest_sha256']=c.sha256(final_manifest)
    renders=c.render_pdf(pdf,out/'renders'/args.revision)
    write_json(out/'review'/f'DPI-REPORT-{args.revision}.json',report)
    canonical=out/'DPI-REPORT.json'
    if canonical.exists():
        # Preserve the previous delivery report before updating this stable pointer.
        backup=out/'review'/f'DPI-REPORT-before-{args.revision}-{c.sha256(canonical)[:12]}.json'
        if not backup.exists():shutil.copy2(canonical,backup)
        canonical.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    else:write_json(canonical,report)
    write_json(out/'review'/f'COMPOSITION-{args.revision}.json',composition)
    write_json(out/'review'/f'RESERVE-PIXELS-{args.revision}.json',pixels)
    write_json(out/'review'/f'RENDERS-{args.revision}.json',renders)
    write_json(out/'review'/f'TEXT-CHECK-{args.revision}.json',{
        'status':'pass','script_sha256':script['sha256'],'pdf_sha256':c.sha256(pdf),
        'verified_chunks':report['script_chunks_verified'],
        'expected_chunks':sum(len(p['copy']) for page in script['pages'].values() for p in page['panels']),
        'comparison':'Exact words and punctuation once in script order on correct page, normalising whitespace only.'})
    return {'pdf':str(pdf),'sha256':c.sha256(pdf),'minimum_ppi':report['minimum_effective_ppi'],
            'median_ppi':report['median_effective_ppi'],'script_chunks':report['script_chunks_verified']}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['prepare','next-job','capture','import-frame','select','build','verify','auto-geometry','fit-layout',
                                      'accept-script-revision'])
    p.add_argument('--reason',help='accept-script-revision: why the author changed the script')
    p.add_argument('--allow-lettering',action='store_true',
                   help='accept-script-revision: also accept text-only changes to existing balloons and captions')
    p.add_argument('--chapter',type=int,required=True)
    p.add_argument('--cast-overrides',type=Path)
    p.add_argument('--art-direction',type=Path,help='prepare: v2 art-direction sidecar JSON')
    p.add_argument('--allow-draft',action='store_true',help='prepare: permit a draft art-direction sidecar')
    p.add_argument('--frame-id');p.add_argument('--generated',type=Path)
    p.add_argument('--from-package',type=Path,help='import-frame: source package directory')
    p.add_argument('--source',help='import-frame: source candidate stem, e.g. page-08-panel-04-v03')
    p.add_argument('--candidate',type=Path);p.add_argument('--geometry',type=Path)
    p.add_argument('--reviewer');p.add_argument('--review-note')
    p.add_argument('--manifest',type=Path);p.add_argument('--layout',type=Path)
    p.add_argument('--revision',default='r1');p.add_argument('--first-folio',type=int,default=1)
    p.add_argument('--upscale-python',type=Path,default=Path.home()/'AI/qwen-image-2.1-lab/.venv/bin/python')
    p.add_argument('--upscale-script',type=Path,default=Path.home()/'AI/upscalers/upscale2x.py')
    p.add_argument('--package-dir',type=Path)
    p.add_argument('--geometry-out',type=Path,help='auto-geometry: new geometry JSON to write')
    p.add_argument('--prompt',type=Path,help='capture: the exact revised prompt sent to the generator')
    p.add_argument('--moderated',action='store_true',help='capture: --prompt is a softened rewrite after a moderation refusal')
    p.add_argument('--inset',type=int,help='auto-geometry: pixels to inset each reserve (default 6)')
    p.add_argument('--draw',action='store_true',help='auto-geometry: place boxes the compositor draws, not painted reserves')
    p.add_argument('--tails',type=Path,help='auto-geometry --draw: JSON of speaker mouth points, [x_frac, y_frac] per copy index')
    p.add_argument('--styles',type=Path,help='auto-geometry --draw: JSON {copy index: style} for chunks lettered in a style, e.g. {"0": "unreadable"}')
    p.add_argument('--faces',type=Path,help='auto-geometry --draw: JSON list of faces {"x","y","r"} as fractions of the frame (r of its height)')
    p.add_argument('--keep',type=Path,help='auto-geometry --draw: JSON list of zones {"x0","y0","x1","y1"} as fractions of the frame that the crop must keep')
    p.add_argument('--layout-out',type=Path,help='fit-layout: new layout file to write (LAYOUT.json format)')
    p.add_argument('--decisions',type=Path,help='fit-layout: reviewer decisions; their picks supply frames the manifest lacks')
    p.add_argument('--faces-dir',type=Path,help='fit-layout: folder of <frame stem>-faces.json files')
    p.add_argument('--face-scale',type=float,help='fit-layout: multiply face radii by this (default 1: the assembler already wrote scaled radii)')
    p.add_argument('--margin',type=float,help='fit-layout: usable-to-needed lettering area to aim for (default 3)')
    p.add_argument('--probe',action='store_true',
                   help='fit-layout: also ask the planner, per panel, what height places its copy (needs --faces-dir)')
    p.add_argument('--keep-max',type=float,
                   help='fit-layout --probe: maximum share of each visible keep zone covered by boxes (above 0, at most 1)')
    p.add_argument('--unpainted',action='store_true',
                   help='auto-geometry --draw and fit-layout: the art has no painted balloons, so no painted regions are measured or covered')
    p.add_argument('--structures',action='store_true',
                   help='fit-layout: also choose each page\'s row structure (which panels share a row) from the script layout cues and the fit')
    p.add_argument('--jobs',type=int,
                   help='fit-layout --structures --probe: page workers (default: CPU count minus 2, at least 1; <=1 runs in process)')
    args=p.parse_args(argv)
    for flag,value in (('--from-package',args.from_package),('--source',args.source)):
        if value is not None and args.command!='import-frame':p.error(f'{flag} applies only to import-frame')
    if args.prompt is not None and args.command!='capture':p.error('--prompt applies only to capture')
    if args.art_direction is not None and args.command!='prepare':p.error('--art-direction applies only to prepare')
    if args.allow_draft and args.command!='prepare':p.error('--allow-draft applies only to prepare')
    if args.allow_lettering and args.command!='accept-script-revision':
        p.error('--allow-lettering applies only to accept-script-revision')
    if args.geometry_out is not None and args.command!='auto-geometry':p.error('--geometry-out applies only to auto-geometry')
    if args.inset is not None and args.command!='auto-geometry':p.error('--inset applies only to auto-geometry')
    if args.draw and args.command!='auto-geometry':p.error('--draw applies only to auto-geometry')
    if args.tails is not None and args.command!='auto-geometry':p.error('--tails applies only to auto-geometry')
    if args.faces is not None and args.command!='auto-geometry':p.error('--faces applies only to auto-geometry')
    if args.keep is not None and args.command!='auto-geometry':p.error('--keep applies only to auto-geometry')
    if args.probe and args.command!='fit-layout':p.error('--probe applies only to fit-layout')
    if args.keep_max is not None:
        if not (args.command=='fit-layout' and args.probe):p.error('--keep-max applies only to fit-layout --probe')
        if not (0<args.keep_max<=1):p.error('--keep-max must be above 0 and at most 1')
    if args.structures and args.command!='fit-layout':p.error('--structures applies only to fit-layout')
    if args.jobs is not None and not (args.command=='fit-layout' and args.structures and args.probe):
        p.error('--jobs applies only to fit-layout --structures --probe')
    if args.jobs is None:args.jobs=max(1,(os.cpu_count() or 1)-2)
    if args.unpainted and not (args.command=='fit-layout' or (args.command=='auto-geometry' and args.draw)):
        p.error('--unpainted applies only to auto-geometry --draw and fit-layout')
    global UNPAINTED
    UNPAINTED=args.unpainted
    for flag,value in (('--layout-out',args.layout_out),('--decisions',args.decisions),('--faces-dir',args.faces_dir),
                       ('--face-scale',args.face_scale),('--margin',args.margin)):
        if value is not None and args.command!='fit-layout':p.error(f'{flag} applies only to fit-layout')
    out=package(args.chapter,args.package_dir)
    if args.command=='prepare':
        result=s.prepare(args.chapter,out,cast_overrides_path=args.cast_overrides,
                         art_direction_path=args.art_direction,allow_draft=args.allow_draft)
    elif args.command=='next-job':
        job=load_job(out)
        result=next((j for j in job['jobs'] if not list((out/'candidates').glob(j['id']+'-*.json'))),None)
    elif args.command=='capture':
        from PIL import Image
        job=load_job(out)
        item=next(j for j in job['jobs'] if j['id']==args.frame_id)
        if not args.generated:raise ValueError('--generated is required')
        revised={}
        if args.prompt is not None:
            # A correction may only append to the prepared prompt. Refuse before anything is written.
            if not args.prompt.is_file():raise ValueError(f'--prompt file does not exist: {args.prompt}')
            base=Path(item['prompt_path']).read_bytes().rstrip()
            sent=args.prompt.read_bytes()
            # v2 also takes a correction set in just before the prepared final SETTING paragraph, which must stay last
            # (checked below); everything before that paragraph is the prepared text, unchanged.
            inserted=job.get('prompt_profile')=='v2' and b'\n\n' in base and sent.startswith(base.rsplit(b'\n\n',1)[0]+b'\n\n')
            if not args.moderated and not sent.startswith(base) and not inserted:
                raise ValueError(f'--prompt must begin with the prepared prompt {item["prompt_path"]}; a correction can only be appended'
                                 + (' or set in before its final SETTING paragraph' if job.get('prompt_profile')=='v2' else ''))
            base_text=base.decode('utf-8')
            final_block=base_text.rstrip().split('\n\n')[-1]
            if job.get('prompt_profile')=='v2':
                if not final_block.startswith('SETTING (this panel):'):
                    raise ValueError('v2 prepared prompt must end with a SETTING paragraph')
                revised_text=args.prompt.read_text(encoding='utf-8').rstrip()
                if any(mark in revised_text for mark in ('\u2014','\u2013')):
                    raise ValueError('em dash or en dash in revised prompt')
                if revised_text.split('\n\n')[-1] != final_block:
                    raise ValueError('revised prompt must end by repeating the prepared SETTING paragraph')
            revised={'prompt_path':str(args.prompt.resolve()),'prompt_sha256':c.sha256(args.prompt),
                     'base_prompt_path':item['prompt_path'],'base_prompt_sha256':item['prompt_sha256']}
            # A softened rewrite after a moderation refusal is allowed only when declared, and is recorded as such.
            if args.moderated:revised['moderated_rewrite']=True
        candidates=out/'candidates';candidates.mkdir(parents=True,exist_ok=True)
        index=1
        # Skip versions taken by a record or by an orphan frame an earlier run left behind.
        while (candidates/f'{args.frame_id}-v{index:02d}.json').exists() or (out/'frames'/f'{args.frame_id}-v{index:02d}.png').exists():index+=1
        frame=out/'frames'/f'{args.frame_id}-v{index:02d}.png';frame.parent.mkdir(parents=True,exist_ok=True)
        if frame.exists():raise FileExistsError(frame)
        shutil.copy2(args.generated,frame)
        with Image.open(frame) as im:width,height=im.size;mode=im.mode
        if mode!='RGB':raise ValueError('Candidate must be RGB; regeneration required')
        result={'id':args.frame_id,'path':str(frame),'sha256':c.sha256(frame),'width':width,'height':height,
            'generation_tool':'built-in imagegen','origin':'generated','prompt_path':item['prompt_path'],
            'prompt_sha256':item['prompt_sha256'],
            'references':[{'path':path,'sha256':digest} for path,digest in item['reference_image_sha256'].items()],
            'visual_review':'pending','original_generated_path':str(args.generated)}
        result.update(revised)
        write_json(candidates/f'{args.frame_id}-v{index:02d}.json',result)
    elif args.command=='import-frame':result=import_frame(args,out)
    elif args.command=='select':
        if not all([args.candidate,args.geometry,args.reviewer,args.review_note]):
            raise ValueError('select needs --candidate --geometry --reviewer --review-note')
        result=json.loads(args.candidate.read_text());coords=json.loads(args.geometry.read_text())
        result.update(coords);result['visual_review']='pass';result['reviewer']=args.reviewer
        result['review_note']=args.review_note
        write_json(out/'selections'/f'{result["id"]}.json',result)
    elif args.command=='auto-geometry':
        try:result=auto_geometry(args,out)
        except (AutoGeometryError,ValueError,FileNotFoundError) as error:
            raise SystemExit(f'auto-geometry failed: {error}')
    elif args.command=='fit-layout':
        try:result=fit_layout_command(args,out)
        except (LayoutFitError,ValueError,OSError) as error:
            raise SystemExit(f'fit-layout failed: {error}')
    elif args.command=='build':result=build(args,out)
    elif args.command=='accept-script-revision':
        try:result=accept_script_revision(args,out)
        except (ValueError,OSError) as error:
            raise SystemExit(f'accept-script-revision failed: {error}')
    else:
        job=load_job(out);script=lettered_script(Path(job['script']['path']))
        manifest=json.loads((out/f'SELECTION-MANIFEST-{args.revision}.json').read_text())
        composition=json.loads((out/'review'/f'COMPOSITION-{args.revision}.json').read_text())
        pdf=out/'pdf'/f'Horse-of-the-Servant-V15-Chapter-{args.chapter:02d}-{args.revision}.pdf'
        c.validate_selection(manifest['frames'],script,out)
        result=c.verify_pdf(pdf,manifest['frames'],script,composition['placements'],args.first_folio)
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=='__main__':main()
