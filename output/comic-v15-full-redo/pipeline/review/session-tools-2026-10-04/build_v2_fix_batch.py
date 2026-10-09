"""A v2 correction batch: each correction goes in before the prompt's final SETTING paragraph, which stays last
(the v2 capture gate requires it). Usage: build_v2_fix_batch.py PACKAGE BATCH_NUMBER TAG FIXES.json
FIXES.json: {"fixes": [{"id": "page-02-panel-02", "mode": "edit" | "generate", "edit_from": "v01", "correction": "..."}]}
Never overwrites a prompt or a batch."""
import json, sys
from pathlib import Path
R = Path('/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo')
package, number, tag, fixes = sys.argv[1], int(sys.argv[2]), sys.argv[3], json.loads(Path(sys.argv[4]).read_text())['fixes']
job = json.loads((R / 'chapters' / package / 'IMAGEGEN-JOBS.json').read_text())
assert job.get('prompt_profile') == 'v2', 'not a v2 package'
jobs = {x['id']: x for x in job['jobs']}
batch = []
for fix in fixes:
    item = jobs[fix['id']]
    base = (R / 'chapters' / package / 'prompts' / f"{fix['id']}.txt").read_text().strip()
    body, setting = base.rsplit('\n\n', 1)
    assert setting.startswith('SETTING (this panel):'), fix['id']
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
        entry = {'mode': 'generate', 'references': item['reference_images']}
    text = f'{body}\n\n{note}\n\n{setting}\n'
    out = R / 'chapters' / package / 'prompts' / f"{fix['id']}-{tag}.txt"
    with out.open('x') as f:
        f.write(text)
    batch.append({'chapter': job['chapter'], 'package': f'output/comic-v15-full-redo/chapters/{package}', 'id': fix['id'],
                  'prompt_file': f'output/comic-v15-full-redo/chapters/{package}/prompts/{fix["id"]}-{tag}.txt', **entry})
with (R / 'review-sheets' / f'LEAN-BATCH-{number}.json').open('x') as f:
    json.dump(batch, f, indent=1)
print(f'LEAN-BATCH-{number}: {len(batch)} jobs,', sum(e["mode"] == "edit" for e in batch), 'edits')
