"""A correction batch for a chapter 1 to 8 package (prompt profile v1): the panel's prepared prompt, then the edit or
regeneration instruction, then the lettering update the earlier v1 fix prompts end with (as chapters/ch05/prompts/
*-fix-f5.txt). Never overwrites a prompt or a batch.
Usage: build_v1_fix_batch.py PACKAGE BATCH_NUMBER TAG FIXES.json
FIXES.json: {"fixes": [{"id": "page-03-panel-04", "mode": "edit" | "generate", "edit_from": "v01", "correction": "..."}]}"""
import json, sys
from pathlib import Path
R = Path('/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo')
package, number, tag, fixes = sys.argv[1], int(sys.argv[2]), sys.argv[3], json.loads(Path(sys.argv[4]).read_text())['fixes']
job = json.loads((R / 'chapters' / package / 'IMAGEGEN-JOBS.json').read_text())
assert job.get('prompt_profile') in (None, 'v1'), 'not a v1 package'
jobs = {x['id']: x for x in job['jobs']}
LETTERING = ('LETTERING UPDATE (overrides any earlier instruction about blank text areas): draw NO balloons, caption boxes, '
             'frames, outlines or text of any kind anywhere in the image; leave clear, low-detail space where lettering will go.')
batch = []
for fix in fixes:
    item = jobs[fix['id']]
    base = (R / 'chapters' / package / 'prompts' / f"{fix['id']}.txt").read_text().strip()
    for dash in ('—', '–'):
        assert dash not in fix['correction'], f"{fix['id']}: dash in correction"
    if fix['mode'] == 'edit':
        note = ('EDIT INSTRUCTION (this job is an edit of the attached image): Keep everything that is right in the attached '
                'image (composition, setting, figures, faces, costumes and light); change only what this correction '
                f"describes: {fix['correction']}")
        entry = {'mode': 'edit', 'edit_source': str(R / 'chapters' / package / 'frames' / f"{fix['id']}-{fix['edit_from']}.png")}
        assert Path(entry['edit_source']).is_file(), entry['edit_source']
    else:
        note = f"REVIEW CORRECTION (an earlier image of this panel was rejected): {fix['correction']}"
        entry = {'mode': 'generate', 'references': item.get('reference_images', [])}
    out = R / 'chapters' / package / 'prompts' / f"{fix['id']}-{tag}.txt"
    with out.open('x') as f:
        f.write(f'{base}\n\n{note}\n\n{LETTERING}\n')
    batch.append({'chapter': job['chapter'], 'package': f'output/comic-v15-full-redo/chapters/{package}', 'id': fix['id'],
                  'prompt_file': f'output/comic-v15-full-redo/chapters/{package}/prompts/{out.name}', **entry})
name = R / 'review-sheets' / f'LEAN-BATCH-{number}.json'
with name.open('x') as f:
    json.dump(batch, f, indent=1)
print(name.name + ':', len(batch), 'jobs,', sum(1 for b in batch if b['mode'] == 'edit'), 'edits')
