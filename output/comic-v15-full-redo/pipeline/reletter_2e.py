#!/usr/bin/env python3
"""Re-letter the V15 chapters to the 2e text: the panel-approved lettering list of 2026-10-21 (round 1 and 2), less
items 19, 21, 22 and 26, which wait for the chapter 14 and 15 redraws.

The art is unchanged. Per chapter, from the repository root on the author's Mac, with the V15 Python:

  1. freeze the package's prepared script as SCRIPT-SOURCE.md (if the package has none) and edit the live script;
  2. accept-script-revision --allow-lettering --allow-balloons --allow-delivery;
  3. reletter the final selection manifest (cut captions lose their reserves);
  4. build at the chapter's final folio as revision r2e1, then verify.

Usage: reletter_2e.py [--chapters 1,2,...] [--panel-geometry page-NN-panel-NN=path.json ...] [--dry-run]
A chapter whose panel gains a balloon (chapter 11 pages 2.3 and 2.4) needs --panel-geometry for that panel from
auto-geometry --draw; without it the chapter stops after step 2, and later runs resume from there.
Nothing is overwritten: every pipeline output is written once, and a finished chapter is skipped.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

PIPELINE=Path(__file__).resolve().parent
V15=PIPELINE.parent
RUN=PIPELINE/'run_chapter.py'
REVISION='r2e1'
REASON='2e text sync (author 2026-10-28, lettering list approved by the review panel 2026-10-21)'

C='> CAPTION: '
EDITS={
 '01':[ # 1, 2, 11, 12, 30
  (C+'This was where the Portuguese forged information.','> *No text.*'),
  (C+'Ships meant movement. Movement meant chances.\n\n'+C+'They had taken my name. They had tried to break my body.\n\n'+C+'They had forgotten the simplest lesson of the Deccan monsoon.\n\n> CAPTION (separate, weighted): Storms do not ask permission.','> *No text.*'),
  ('> JOÃO: Este. This one is stubborn.','> JOÃO: *Este*. This one is stubborn.'),
  ('our language, senhor marata?','our language, *senhor marata*?'),
  ('Twenty-five. Huzurat cavalry,','Twenty-five. *Huzurat* cavalry,'),
  ('you were huzurat cavalry under','you were *huzurat* cavalry under'),
 ],
 '02':[ # 3, 4, 5, 13, 14
  ('\n\n'+C+'Someday, I thought, that hesitation might matter.',''),
  (C+'The words settled over me heavier than iron.\n\n',''),
  ('\n\n'+C+'Neither of us mentioned that promises made in chains are the easiest to break.',''),
  ('On your feet, marata. The Viceroy','On your feet, *marata*. The Viceroy'),
  ('Not even maratas.','Not even *maratas*.'),
 ],
 '04':[ # 6, 28
  ('\n\n'+C+'Storms on land were different from storms at sea. They did not roar and crash; they crept in on quiet feet, through conversations and calculations.',''),
  (C+'I had escaped the Portuguese dungeon and the drowning ship by chance and stubbornness.\n\n'+C+'If I was to survive whatever came next, I would need more than that.','> *No text.*'),
 ],
 '05':[ # 7, 29
  (C+'Somewhere to the south a king I had not yet met considered maps covered in salt stains and ink.\n\n'+C+'The road that had begun in a Goan dungeon now pointed toward him.\n\n'+C+'Horses. Guns. Storms.\n\n',''),
  (C+"The fishermen had spoken the name Travancore. I wanted to hear it from this man's mouth.\n\n",''),
 ],
 '06':[ # 8
  (C+'Storms had tried to kill me. Now I would learn whether I could become one.\n\n',''),
 ],
 '07':[ # 9, 10
  ('\n\n'+C+'But it was honest.',''),
  (C+'On Deccan soil, I had thought I knew the limits of what a horse could do against a gun. Here, those limits shifted.\n\n'+C+'Storms did not ask permission.\n\n> CAPTION (separate, weighted): Perhaps horses, taught well, did not either.',
   '> CAPTION (separate, weighted): On Deccan soil, I had thought I knew the limits of what a horse could do against a gun. Here, those limits shifted.'),
 ],
 '10':[ # 30
  ('Silver chuckrams. Pepper by the candi,','Silver *chuckrams*. Pepper by the *candi*,'),
  ('And hundis, that could','And *hundis*, that could'),
  ('> CAPTION: A madampi near Attingal','> CAPTION: A *madampi* near Attingal'),
 ],
 '11':[ # 16, 17, 18
  ('> BOY (off): When he turns, the men move. When he scratches his nose, they move slower.',
   '> BOY (off): When he turns, the men move. When he scratches his nose, they move slower.\n\n> NAGOJI (off): He has a name?'),
  ('> NAGOJI: Keep watching. Count how many days they hover.',
   '> BOY (from above): They shout something. Hard to hear over the wind. Lannoy. Lannu. Something like that.\n\n> NAGOJI: Keep watching. Count how many days they hover.'),
  ('> NAGOJI: The same tall officer on the quarterdeck. Pale hair, stiff back. He drills them hard.',
   '> NAGOJI: The watch boy says the same tall officer stands on the quarterdeck. He calls him Lannoy, though the wind may have changed the name.'),
  (C+'Somewhere on the largest hull, the pale-haired officer stood or slept or paced. I did not yet know his name.\n\n'+C+'That would come later, when he surrendered at Colachel and chose a different flag.',
   C+'Somewhere out there, on that largest hull, the pale-haired officer, Lannoy, Lannu, whatever his men called him, stood or slept or paced.'),
 ],
 '13':[ # 30
  ('> PADMINI: This is the Sarpa Kavu.','> PADMINI: This is the *Sarpa Kavu*.'),
  ("of Padmini Amma's tharavadu may walk","of Padmini Amma's *tharavadu* may walk"),
 ],
 '16':[ # 23, 24, 25, 30
  ('> LANNOY: A Catholic city in Flanders.','> LANNOY: A Catholic city in Artois.'),
  ('No. But seventeen years of watching','No. But eight years of watching'),
  ('> LANNOY: I am forty-three.','> LANNOY: I am twenty-five.'),
  ('> CAPTION: A kanikka for a victory','> CAPTION: A *kanikka* for a victory'),
 ],
 '19':[ # 30
  ('Even if you have a tharavadu now,','Even if you have a *tharavadu* now,'),
  ('It travels by your hundi.','It travels by your *hundi*.'),
 ],
 '24':[ # 15, 27
  ('> DUARTE: Senhor... I... that is...','> DUARTE: *Senhor*... I... that is...'),
  ('In Zeeland, where I was born, there','In Zeeland, where I first took ship, there'),
 ],
}

# Final V15 builds (pipeline/review/V15-FINAL-SOURCES-2026-10-10.json) and folios (V15-IMPOSITION-2026-10-10.json).
FINAL={'01':('ch01-v2','d9t-b','LAYOUT-fitted-d9.json',1),'02':('ch02','d6t-b','LAYOUT-fitted-d6.json',10),
       '04':('ch04','s13t-b','LAYOUT-fitted-s13.json',27),'05':('ch05-split2','u1-b','LAYOUT-solved-s1.json',34),
       '06':('ch06-split','u1-b','LAYOUT-solved-s1.json',44),'07':('ch07-turn','s1-b','LAYOUT-solved-s1.json',57),
       '10':('ch10-split2','u1-b','LAYOUT-solved-s1c.json',100),'11':('ch11-split2','u1-b','LAYOUT-solved-s1c.json',114),
       '13':('ch13-split','u1-b','LAYOUT-solved-s1.json',151),'16':('ch16-split3','s1-b','LAYOUT-solved-s1.json',203),
       '19':('ch19','s3-b','LAYOUT-solved-s3.json',260),'24':('ch24-split2','s1-b','LAYOUT-solved-s1.json',342)}
# Which old reserve a surviving chunk keeps where matching by text cannot say (lettering list items 10 and 18).
CHUNK_MAP={'07':['page-13-panel-05=0:2'],'11':['page-24-panel-01=0:0']}


def sha256(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(chapter,package,*argv,dry=False):
    command=[sys.executable,str(RUN),argv[0],'--chapter',str(int(chapter)),'--package-dir',str(package),*argv[1:]]
    print('  $',' '.join(command[2:]),flush=True)
    if dry:return None
    done=subprocess.run(command,capture_output=True,text=True)
    if done.returncode:raise SystemExit(f'ch{chapter} {argv[0]} failed:\n{done.stderr.strip() or done.stdout.strip()}')
    return json.loads(done.stdout) if done.stdout.strip() else None


def edited(text,chapter):
    for old,new in EDITS[chapter]:
        if text.count(old)!=1:raise SystemExit(f'ch{chapter}: expected one match for {old[:70]!r}, found {text.count(old)}')
        text=text.replace(old,new)
    if chr(0x2014) in text or chr(0x2013) in text:raise SystemExit(f'ch{chapter}: the edit leaves a dash')
    return text


def chapter_run(chapter,geometries,dry):
    name,tag,layout,folio=FINAL[chapter];package=V15/'chapters'/name
    job=json.loads((package/'IMAGEGEN-JOBS.json').read_text());script=Path(job['script']['path'])
    source=package/'SCRIPT-SOURCE.md'
    pdf=package/'pdf'/f'Horse-of-the-Servant-V15-Chapter-{chapter}-{REVISION}.pdf'
    if pdf.exists():
        print(f'ch{chapter}: {REVISION} already built, skipped');return {'chapter':chapter,'pdf':str(pdf),'skipped':True}
    print(f'ch{chapter}: {name} {tag}',flush=True)
    revisions=package/'SCRIPT-REVISIONS.json'
    accepted=revisions.is_file() and any(REASON==entry.get('reason') for entry in json.loads(revisions.read_text()))
    if not accepted:
        if not source.exists():
            if sha256(script)!=job['script']['sha256']:raise SystemExit(f'ch{chapter}: the live script is not the prepared one')
            if not dry:source.write_bytes(script.read_bytes())
        current=script.read_text(encoding='utf-8')
        if not dry:script.write_text(edited(current,chapter),encoding='utf-8')
        else:edited(current,chapter)
        run(chapter,package,'accept-script-revision','--reason',REASON,'--allow-lettering','--allow-balloons',
            '--allow-delivery',dry=dry)
    manifest=package/f'SELECTION-INPUT-{tag}.json';relettered=package/f'SELECTION-INPUT-{tag}-2e.json'
    if not relettered.exists():
        extra=[x for value in CHUNK_MAP.get(chapter,[]) for x in ('--chunk-map',value)]
        extra+=[x for panel,path in geometries.get(chapter,{}).items() for x in ('--panel-geometry',f'{panel}={path}')]
        run(chapter,package,'reletter','--manifest',str(manifest),'--manifest-out',str(relettered),*extra,dry=dry)
    run(chapter,package,'build','--manifest',str(relettered),'--layout',str(package/layout),'--first-folio',str(folio),
        '--revision',REVISION,dry=dry)
    run(chapter,package,'verify','--first-folio',str(folio),'--revision',REVISION,dry=dry)
    return {'chapter':chapter,'pdf':str(pdf),'renders':str(package/'renders'/REVISION),
            'final_build':f'{name}:{REVISION}:{tag}-2e'}


def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--chapters',default=','.join(FINAL))
    p.add_argument('--panel-geometry',action='append',default=[],help='CH:page-NN-panel-NN=path.json, e.g. 11:page-02-panel-03=g.json')
    p.add_argument('--dry-run',action='store_true')
    args=p.parse_args()
    geometries={}
    for value in args.panel_geometry:
        chapter,_,rest=value.partition(':');panel,_,path=rest.partition('=')
        geometries.setdefault(f'{int(chapter):02d}',{})[panel]=path
    results=[]
    for chapter in [f'{int(x):02d}' for x in args.chapters.split(',')]:
        if chapter not in FINAL:raise SystemExit(f'ch{chapter} has no 2e lettering changes')
        try:results.append(chapter_run(chapter,geometries,args.dry_run))
        except SystemExit as error:
            print(error,file=sys.stderr);results.append({'chapter':chapter,'stopped':str(error)})
    print(json.dumps(results,indent=2,ensure_ascii=False))


if __name__=='__main__':main()
