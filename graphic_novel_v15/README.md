# Horse of the Servant: Graphic Novel V15

A rebuild of the graphic novel adaptation after the V13 review (`v13_review.md`).
This folder currently covers **Chapters 1 to 5 (pages 1 to 23)**, as a pilot for the
approach before the remaining chapters are redone.

## What is here

| File | Purpose |
|---|---|
| `v13_review.md` | What was wrong with V13 and how V15 answers each point |
| `characters.yaml` | Locked character designs, costume phases, style and palettes. Source of truth. |
| `character_bible.md` | Readable version of the above (generated) |
| `script_ch01-05.yaml` | Page-by-page script: layout, art direction, captions, balloons. Source of truth. |
| `script_ch01-05.md` | Readable version of the script (generated) |
| `prompts/script_ch01-05.jsonl` | One Qwen request per panel (generated) |
| `style_guide.md` | Look, storytelling rules, page template, workflow |
| `tools/build.py` | Validate, generate docs and prompts, letter and assemble pages |
| `tools/generate_qwen.py` | Generate character sheets and panel art with Qwen image models |
| `fonts/` | Comic Neue and Cinzel (SIL Open Font License) |

Generated at build time and not committed: `out/` (lettered pages and PDF), `refs/`
(character sheets) and `art/` (panel images) until they have been reviewed.

## Status

- Script, character bible, prompts and lettering pipeline: done for Chapters 1 to 5.
- Art: **not generated yet.** The environment this was built in cannot reach the Qwen
  API (its network policy blocks `dashscope.aliyuncs.com` and `huggingface.co`), so
  `tools/generate_qwen.py` has only been dry-run. Its first real run should be a single
  panel, checked by eye.

## Quick start

```bash
pip install pyyaml pillow requests
python tools/build.py check          # validate
python tools/build.py pages          # placeholder pages to read the pacing
export DASHSCOPE_API_KEY=sk-...
python tools/generate_qwen.py refs   # character sheets; review them
python tools/generate_qwen.py panels --only 01-1   # one panel first
python tools/generate_qwen.py panels --pages 1-23
python tools/build.py pages          # final lettered pages and PDF in out/
```
