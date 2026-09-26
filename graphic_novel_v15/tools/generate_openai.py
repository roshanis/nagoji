#!/usr/bin/env python3
"""Generate V15 art with OpenAI image models from prompts/<script>.openai.jsonl.

Same two passes as the Qwen script:

  sheets  one character model sheet per character and costume phase -> refs/<id>.png
          Review these and regenerate any you do not like before running panels.
  panels  one image per panel -> art/<panel id>.png. Panels with characters are sent
          to the edit endpoint with those characters' sheets attached as references.

Then run `python tools/build.py pages` to letter and assemble the pages.

Setup:
  python tools/build.py openai      # writes the JSONL this script reads
  export OPENAI_API_KEY=sk-...
  pip install requests pillow

Examples:
  python tools/generate_openai.py sheets
  python tools/generate_openai.py panels --only 01-1
  python tools/generate_openai.py panels --pages 1-6 --quality high
  python tools/generate_openai.py panels --dry-run

NOTE: written against the OpenAI Images API (generations and edits, base64 output).
It has not been run yet: the environment it was written in blocks api.openai.com.
Run a single panel with --only first and check the output.
"""
import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.openai.com/v1/images"


def parse_pages(spec):
    if not spec:
        return None
    pages = set()
    for part in spec.split(","):
        a, _, b = part.partition("-")
        pages.update(range(int(a), int(b or a) + 1))
    return pages


def request(args, job, ref_files):
    fields = {"model": args.model, "prompt": job["prompt"], "size": job["size"],
              "quality": args.quality, "n": "1"}
    if args.dry_run:
        print(json.dumps({"endpoint": "edits" if ref_files else "generations",
                          "refs": [p.name for p in ref_files], **fields}, indent=1)[:1200])
        return None
    import requests
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY is not set")
    headers = {"Authorization": f"Bearer {key}"}
    for attempt in range(4):
        if ref_files:
            files = [("image[]", (p.name, p.read_bytes(), "image/png")) for p in ref_files]
            r = requests.post(f"{API}/edits", headers=headers, data=fields, files=files, timeout=600)
        else:
            body = dict(fields, n=1)
            r = requests.post(f"{API}/generations", headers=headers, json=body, timeout=600)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(2 ** (attempt + 2))
            continue
        if r.status_code != 200:
            raise RuntimeError(f"{r.status_code}: {r.text[:500]}")
        return base64.b64decode(r.json()["data"][0]["b64_json"])
    raise RuntimeError("gave up after retries")


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(data)
    from PIL import Image
    Image.open(tmp).convert("RGB").save(path)
    tmp.unlink()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["sheets", "panels"])
    ap.add_argument("--script", default="script_ch01-05.yaml")
    ap.add_argument("--pages", help="e.g. 1-6 or 1,3,5-7")
    ap.add_argument("--only", nargs="*", help="panel or sheet ids")
    ap.add_argument("--force", action="store_true", help="regenerate files that exist")
    ap.add_argument("--no-refs", action="store_true", help="ignore character sheets")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--model", default="gpt-image-1")
    ap.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    args = ap.parse_args()

    src = ROOT / "prompts" / (Path(args.script).stem + ".openai.jsonl")
    if not src.exists():
        sys.exit(f"{src} not found; run tools/build.py openai first")
    kind = "sheet" if args.command == "sheets" else "panel"
    pages, only = parse_pages(args.pages), set(args.only or [])
    for line in src.read_text().splitlines():
        job = json.loads(line)
        if job["kind"] != kind or (only and job["id"] not in only):
            continue
        if pages and job.get("page") not in pages:
            continue
        out = ROOT / ("refs" if kind == "sheet" else "art") / f"{job['id']}.png"
        if out.exists() and not args.force:
            continue
        refs = [] if args.no_refs else [ROOT / "refs" / f"{r}.png" for r in job.get("refs", [])]
        refs = [p for p in refs if p.exists()]
        print(kind, job["id"], "refs:", [p.stem for p in refs])
        data = request(args, job, refs)
        if data:
            save(out, data)


if __name__ == "__main__":
    main()
