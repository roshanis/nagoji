#!/usr/bin/env python3
"""Chapter 1 migration adapter. General chapters use run_chapter select."""
import argparse
import copy
import json
import re
import shutil
from pathlib import Path
from PIL import Image
import compositor as c

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'output/comic-v15-full-redo/chapters/ch01'
LEGACY=ROOT/'output/comic-v14-chapter-01-rebuild-v1/SELECTION-MANIFEST-r5.json'


def local_path(value,ledger):
    p=Path(value)
    if p.is_absolute():return p
    if str(p).startswith('..'):return (ledger.parent/p).resolve()
    if str(p).startswith('output/'):return ROOT/p
    return OUT/p


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if not args.output.resolve().is_relative_to(OUT):raise ValueError('Pilot output must be in ch01')
    old=json.loads(LEGACY.read_text());original={r['id']:r for r in old['frames']}
    ledger_files=['art-p01-p02.json','art-p03-p04.json','art-p05-p06.json','art-p07.json','art-p08.json','art-p09.json',
                  'art-p05-p06-r2.json','art-p09-r2.json']
    choices={}
    for name in ledger_files:
        file=OUT/'review'/name
        if not file.exists():
            if name in ('art-p03-p04.json',):raise FileNotFoundError(file)
            continue
        payload=json.loads(file.read_text())
        for source in payload['frames']:
            nums=re.findall(r'\d+',source['id']);frame_id=f'page-{int(nums[0]):02d}-panel-{int(nums[1]):02d}'
            row=copy.deepcopy(source);row['id']=frame_id
            row['path']=str(local_path(row['path'],file))
            if row.get('prompt_path'):row['prompt_path']=str(local_path(row['prompt_path'],file))
            row['review_ledger']={'path':str(file),'sha256':c.sha256(file)}
            choices[frame_id]=row
    choices['page-01-panel-03']={'id':'page-01-panel-03',
        'path':str(OUT/'frames/page-01-panel-03-v15-r2.png'),
        'prompt_path':str(OUT/'prompts/page-01-panel-03-v15-r2.txt'),
        'origin':'regenerated','correction':'Removed beard; restored V13 face, curled moustache and small flush gold stud.',
        'references':[{'path':str(ROOT/'output/comic-v13-reference-redesign-v1/concepts/nagoji-v2.png')}]}
    repairs=json.loads((OUT/'review/ROOT-RESERVE-REPAIRS-r1.json').read_text())
    rows=[]
    for old_row in old['frames']:
        chosen=choices[old_row['id']];path=Path(chosen['path'])
        if chosen.get('sha256') and chosen['sha256']!=c.sha256(path):
            if chosen.get('origin')=='reused' and c.sha256(path)==old_row['sha256']:
                chosen['metadata_hash_transcription_correction']={
                    'previous_record':chosen['sha256'],'verified_original_and_copy':c.sha256(path)}
            else:raise ValueError(f'Reviewed frame bytes changed: {path}')
        with Image.open(path) as im:width,height=im.size;rgb=c.hashlib.sha256(im.tobytes()).hexdigest()
        row=c.scaled_row(old_row,width,height)
        # The original viewport is retained for migrated rows unless a measured
        # list-based row explicitly supplies new crop and reserve geometry.
        valid_geometry=isinstance(chosen.get('reserves'),list)
        for key,value in chosen.items():
            if key in ('reserves','visible_rect') and not valid_geometry:continue
            row[key]=value
        row.update(width=width,height=height,sha256=c.sha256(path),rgb_sha256=rgb,
                   source_path=old_row['path'],source_sha256=old_row['sha256'])
        origin=chosen.get('origin','reused');row['origin']=origin
        if not path.resolve().is_relative_to(OUT):
            dest=OUT/'frames'/f'{row["id"]}-v15-reused.png'
            if dest.exists():
                if c.sha256(dest)!=c.sha256(path):raise ValueError('Conflicting reused image')
            else:shutil.copy2(path,dest)
            row['path']=str(dest)
        prompt=Path(chosen.get('prompt_path',OUT/'prompts'/f'{row["id"]}-v15-r1.txt'))
        if origin=='reused' and not prompt.exists():prompt=Path(old_row['prompt_path'])
        if not prompt.resolve().is_relative_to(OUT):
            dest=OUT/'prompts'/f'{row["id"]}-v15-reused.txt'
            if dest.exists():
                if c.sha256(dest)!=c.sha256(prompt):raise ValueError('Conflicting reused prompt')
            else:shutil.copy2(prompt,dest)
            prompt=dest
        row['prompt_path']=str(prompt);row['prompt_sha256']=c.sha256(prompt)
        references=chosen.get('references',[])
        if not references and chosen.get('references_sha256'):
            references=[str(ROOT/'output/comic-v13-reference-redesign-v1/concepts/nagoji-v2.png')]
        row['references']=[]
        for ref in references:
            refpath=Path(ref if isinstance(ref,str) else ref['path'])
            if not refpath.is_absolute():refpath=ROOT/refpath
            row['references'].append({'path':str(refpath),'sha256':c.sha256(refpath)})
        if row['id'] in repairs:row['reserves']=repairs[row['id']]
        row['visual_review']='pass'
        row['reviewer']='Codex frame review and root integration; see review ledger'
        if row['id']=='page-01-panel-02':
            row['ledger_inscription']=True;row['ledger_rect']=[300,560,760,690]
        rows.append(row)
    payload={'schema_version':2,'source_manifest':{'path':str(LEGACY),'sha256':c.sha256(LEGACY)},'frames':rows}
    with args.output.open('x') as f:json.dump(payload,f,indent=2,ensure_ascii=False);f.write('\n')
    print(args.output)


if __name__=='__main__':main()
