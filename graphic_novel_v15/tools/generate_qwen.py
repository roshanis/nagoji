#!/usr/bin/env python3
"""Generate V15 art with Qwen image models through Alibaba Cloud Model Studio (DashScope).

Two passes, run in this order:

  1. refs    One character sheet per character and costume phase, made with the
             text-to-image model. Review these by eye and regenerate any you do not
             like (--force --only nagoji:B_prisoner) before moving on. They are what
             keeps faces consistent across panels.
  2. panels  One image per panel from prompts/<script>.jsonl. Panels that show
             characters are sent to the image-edit model together with those
             characters' sheets as reference images (up to 3). Panels with no
             characters use text-to-image.

Then run `python tools/build.py pages` to letter and assemble the pages.

Setup:
  export DASHSCOPE_API_KEY=sk-...
  # Optional. Default is the international endpoint; use
  # https://dashscope.aliyuncs.com for the mainland China region.
  export DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com
  pip install requests pyyaml pillow

Examples:
  python tools/generate_qwen.py refs
  python tools/generate_qwen.py panels --pages 1-6
  python tools/generate_qwen.py panels --only 03-2 04-5 --force
  python tools/generate_qwen.py panels --dry-run      # print requests, call nothing

Model names are flags so you can switch without editing code:
  --t2i-model qwen-image-plus     (text to image)
  --edit-model qwen-image-edit-plus (reference-guided edit, multiple images)

NOTE: written against the DashScope multimodal-generation API as documented for
Qwen-Image. It has not been run yet: the environment it was written in blocks
dashscope hosts. Run a single panel with --only first and check the output.
"""
import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = "/api/v1/services/aigc/multimodal-generation/generation"
REF_SIZE = "1664*928"


def parse_pages(spec):
    if not spec:
        return None
    pages = set()
    for part in spec.split(","):
        a, _, b = part.partition("-")
        pages.update(range(int(a), int(b or a) + 1))
    return pages


def data_uri(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def call(args, model, content, parameters):
    body = {
        "model": model,
        "input": {"messages": [{"role": "user", "content": content}]},
        "parameters": parameters,
    }
    if args.dry_run:
        shown = [{"image": c["image"][:48] + "..."} if "image" in c else c for c in content]
        print(json.dumps({"model": model, "content": shown, "parameters": parameters},
                         ensure_ascii=False, indent=1)[:1500])
        return None
    import requests
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        sys.exit("DASHSCOPE_API_KEY is not set")
    base = os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope-intl.aliyuncs.com")
    for attempt in range(4):
        r = requests.post(base + ENDPOINT, json=body, timeout=300,
                          headers={"Authorization": f"Bearer {key}",
                                   "Content-Type": "application/json"})
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(2 ** (attempt + 1))
            continue
        if r.status_code != 200:
            raise RuntimeError(f"{r.status_code}: {r.text[:500]}")
        out = r.json()
        try:
            url = out["output"]["choices"][0]["message"]["content"][0]["image"]
        except (KeyError, IndexError):
            raise RuntimeError(f"unexpected response: {json.dumps(out)[:500]}")
        img = requests.get(url, timeout=120)
        img.raise_for_status()
        return img.content
    raise RuntimeError("gave up after retries")


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(data)
    # Normalise whatever format came back to PNG.
    from PIL import Image
    Image.open(tmp).convert("RGB").save(path)
    tmp.unlink()


def ref_path(ref):
    return ROOT / "refs" / (ref.replace(":", "__") + ".png")


def cmd_refs(args):
    chars = yaml.safe_load((ROOT / "characters.yaml").read_text())
    style = chars["style"]
    wanted = set(args.only or [])
    for cid, c in chars["characters"].items():
        phases = c.get("phases") or {None: None}
        for phase, costume in phases.items():
            ref = f"{cid}:{phase}" if phase else cid
            if wanted and ref not in wanted and cid not in wanted:
                continue
            out = ref_path(ref)
            if out.exists() and not args.force:
                continue
            subject = c["prompt"].strip()
            if costume:
                subject += f", wearing: {costume['wear'].strip()}"
            is_horse = "horse" in c.get("role", "").lower() or "mare" in c.get("role", "").lower()
            views = ("side view, three-quarter view and head close-up" if is_horse else
                     "full-body front view, three-quarter view, profile view and a head close-up")
            prompt = (f"{style['prompt'].strip().rstrip('.')}. Character model sheet on a plain warm paper background, "
                      f"{views} of the same {'animal' if is_horse else 'person'}, consistent design "
                      f"across every view, even neutral lighting. {subject}.")
            params = {"size": REF_SIZE, "negative_prompt": style["negative"], "prompt_extend": False,
                      "watermark": False, "seed": args.seed}
            print("ref", ref)
            data = call(args, args.t2i_model, [{"text": prompt}], params)
            if data:
                save(out, data)


def cmd_panels(args):
    src = ROOT / "prompts" / (Path(args.script).stem + ".jsonl")
    if not src.exists():
        sys.exit(f"{src} not found; run tools/build.py prompts first")
    chars = yaml.safe_load((ROOT / "characters.yaml").read_text())
    script = yaml.safe_load((ROOT / args.script).read_text())
    panel_refs = {p["id"]: p.get("chars", []) for pg in script["pages"] for p in pg["panels"]}
    pages = parse_pages(args.pages)
    only = set(args.only or [])
    for line in src.read_text().splitlines():
        job = json.loads(line)
        if pages and job["page"] not in pages:
            continue
        if only and job["id"] not in only:
            continue
        out = ROOT / "art" / f"{job['id']}.png"
        if out.exists() and not args.force:
            continue
        ref_files = [ref_path(r) for r in panel_refs[job["id"]] if ref_path(r).exists()][:3]
        print("panel", job["id"], "refs:", [p.stem for p in ref_files])
        if ref_files and not args.no_refs:
            content = [{"image": data_uri(p)} for p in ref_files]
            names = ", ".join(p.stem.split("__")[0] for p in ref_files)
            content.append({"text": (
                f"Draw a new graphic novel panel. The reference images are character model "
                f"sheets for: {names}. Keep each character's face, build, hair and costume "
                f"exactly as in their sheet. Do not copy the sheet layout. {job['prompt']}")})
            params = {"negative_prompt": job["negative_prompt"], "watermark": False,
                      "seed": args.seed}
            data = call(args, args.edit_model, content, params)
        else:
            params = {"size": job["size"], "negative_prompt": job["negative_prompt"],
                      "prompt_extend": False, "watermark": False, "seed": args.seed}
            data = call(args, args.t2i_model, [{"text": job["prompt"]}], params)
        if data:
            save(out, data)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["refs", "panels"])
    ap.add_argument("--script", default="script_ch01-05.yaml")
    ap.add_argument("--pages", help="e.g. 1-6 or 1,3,5-7")
    ap.add_argument("--only", nargs="*", help="panel ids, or character ids for refs")
    ap.add_argument("--force", action="store_true", help="regenerate files that exist")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-refs", action="store_true", help="text-to-image only, ignore sheets")
    ap.add_argument("--seed", type=int, default=1738)
    ap.add_argument("--t2i-model", default="qwen-image-plus")
    ap.add_argument("--edit-model", default="qwen-image-edit-plus")
    args = ap.parse_args()
    {"refs": cmd_refs, "panels": cmd_panels}[args.command](args)


if __name__ == "__main__":
    main()
