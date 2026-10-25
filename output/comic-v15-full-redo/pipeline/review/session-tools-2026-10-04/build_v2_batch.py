"""Write one v2 generation batch from a prepared package: the prepared prompt unchanged, its reference sheets in order.
Usage: build_v2_batch.py PACKAGE BATCH_NUMBER ID [ID ...]   (ids as page.panel, e.g. 1.5; never overwrites a batch)"""
import json, sys
from pathlib import Path
R = Path('/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo')
package, number, wanted = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
job = json.loads((R / 'chapters' / package / 'IMAGEGEN-JOBS.json').read_text())
assert job.get('prompt_profile') == 'v2', 'not a v2 package'
jobs = {x['id']: x for x in job['jobs']}
batch = []
for want in wanted:
    page, panel = (int(x) for x in want.split('.'))
    item = jobs[f'page-{page:02d}-panel-{panel:02d}']
    prompt = R / 'chapters' / package / 'prompts' / f"{item['id']}.txt"
    assert prompt.is_file(), prompt
    batch.append({'chapter': job['chapter'], 'package': f'output/comic-v15-full-redo/chapters/{package}', 'id': item['id'],
                  'prompt_file': f'output/comic-v15-full-redo/chapters/{package}/prompts/{item["id"]}.txt',
                  'references': item['reference_images']})
name = R / 'review-sheets' / f'LEAN-BATCH-{number}.json'
with name.open('x') as f:
    json.dump(batch, f, indent=1)
print(name, len(batch), 'entries;', sum(len(x['references']) for x in batch), 'reference attachments')
