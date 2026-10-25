"""Save a finished selection workflow output and merge it into the package's newest decisions round (any naming scheme).
Usage (from output/comic-v15-full-redo): merge_latest.py TASK_ID PACKAGE LABEL"""
import subprocess, sys, shutil
from pathlib import Path
S = Path('/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad')
T = Path('/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/tasks')
PY = '/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python'
sys.path.insert(0, str(S)); from apply_identity_latest import latest
task, pkg, label = sys.argv[1:4]
out = Path(f'review-sheets/SELECT-ZONES-{pkg}-{label}-2026-10-08.json')
if out.exists(): sys.exit(f'{out} exists')
shutil.copy(T / f'{task}.output', out)
d_in, f_in, k_in, d_out, f_out, k_out = latest(pkg)
env = {'PYTHONDONTWRITEBYTECODE': '1', 'PATH': '/usr/bin:/bin'}
r = subprocess.run([PY, 'pipeline/review/session-tools-2026-10-04/merge_round.py', str(out), pkg, d_in, d_out, f_in, f_out, k_in, k_out], capture_output=True, text=True, env=env)
print(r.stdout.strip() or r.stderr.strip()[-500:])
R = f'chapters/{pkg}/review'
r = subprocess.run([PY, str(S / 'norm_versions.py'), f'{R}/{k_out}', f'{R}/{f_out}'], capture_output=True, text=True, env=env)
print(r.stdout.strip() or r.stderr.strip()[-300:])
