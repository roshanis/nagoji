#!/usr/bin/env python3
"""Prepare a reproducible V15 chapter art job from an approved script.

This module only parses and prepares prompts. It never calls image generation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
V15 = ROOT / "output" / "comic-v15-full-redo"
SCRIPTS = V15 / "scripts"
CONTINUITY = V15 / "CONTINUITY.md"
CONCEPT_ROOT = ROOT / "output" / "comic-v13-reference-redesign-v1" / "concepts"
LOCK_PATH = ROOT / "output" / "comic-v13-reference-redesign-v1" / "CHARACTER-LOCK-v1.json"

NO_DASHES = ("\u2014", "\u2013")
SPEAKERS = {"CAPTION", "JOÃO", "JOAO", "DUARTE", "NAGOJI", "PRISONER"}
CHARACTER_ALIASES = {
    "nagoji": ("nagoji", "ananthan", "sawant", "horseman"),
    "varma": ("marthanda varma", "varma"),
    "duarte": ("duarte", "father duarte"),
    "joao": ("joão", "joao", "gaoler"),
    "ramayyan": ("ramayyan",),
    "padmini": ("padmini",),
    "revathi": ("revathi",),
    "ibrahim": ("ibrahim", "kapitan"),
    "eustachius": ("eustachius", "de lannoy", "lannoy"),
    "raza": ("raza khan", "raza"),
    "ponnan": ("ponnan", "ponnam pandya"),
    "dhanaji": ("dhanaji",),
    "keshavrao": ("keshavrao",),
    "senior_rani": ("senior rani", "rani of attingal", "attingal"),
    "prince": ("prince", "heir"),
    "savitri": ("savitri", "kottarakkara"),
    "thoma": ("thoma ittyerah", "ittyerah"),
    "avraham": ("avraham ben ephraim", "avraham", "ephraim"),
    "nandini": ("nandini",),
    "mathoo": ("mathoo tharakan", "mathoo"),
    "karl": ("karl august", "karl"),
}
CONCEPTS = {
    "nagoji": "nagoji-v2.png",
    "varma": "varma-v1.png",
    "temple_priest": "temple-priest-v1.png",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _reject_dashes(value: str, where: str) -> None:
    if any(mark in value for mark in NO_DASHES):
        raise ValueError(f"em dash or en dash in {where}")


def _copy_line(line: str, panel_id: str) -> dict[str, str] | None:
    if not line.startswith("> "):
        return None
    value = line[2:]
    if re.fullmatch(r"\*No text(?:\..*)?\*", value.strip(), re.IGNORECASE):
        return None
    match = re.match(r"^([^:]+): (.*)$", value)
    if not match:
        raise ValueError(f"unparsed quoted line in {panel_id}: {value}")
    speaker, text = match.groups()
    base = speaker.split(" (")[0].strip().upper()
    if base not in SPEAKERS:
        # Permit future named speakers while still requiring an explicit label.
        if not re.fullmatch(r"[A-Z][A-Z0-9À-ÖØ-Ý ]+", base):
            raise ValueError(f"invalid speaker in {panel_id}: {speaker}")
    _reject_dashes(text, f"{panel_id} copy")
    return {"speaker": speaker, "text": text}


def parse_script(path: Path) -> dict[str, Any]:
    """Parse every page and panel while preserving exact quoted copy."""
    path = Path(path)
    raw = path.read_text(encoding="utf-8")
    _reject_dashes(raw, str(path))
    pages: dict[int, dict[str, Any]] = {}
    current_page: int | None = None
    current_panel: dict[str, Any] | None = None
    for line in raw.splitlines():
        page_match = re.match(r"^## PAGE (\d+)(?:\s*\([^)]*\))?\s*$", line)
        if page_match:
            current_page = int(page_match.group(1))
            if current_page in pages:
                raise ValueError(f"duplicate page {current_page}")
            pages[current_page] = {"page": current_page, "panels": []}
            current_panel = None
            continue
        if re.match(r"^#{1,6}\s+", line):
            current_panel = None
            continue
        panel_match = re.match(r"^\*\*(\d+)\.(\d+)\*\*\s+(.*)$", line)
        if panel_match:
            if current_page is None:
                raise ValueError("panel before page heading")
            page_number, panel_number = map(int, panel_match.groups()[:2])
            if page_number != current_page:
                raise ValueError(f"panel page differs from heading: {line}")
            expected = len(pages[current_page]["panels"]) + 1
            if panel_number != expected:
                raise ValueError(f"non-contiguous panel number on page {current_page}: {panel_number}")
            current_panel = {
                "id": f"page-{page_number:02d}-panel-{panel_number:02d}",
                "page": page_number,
                "panel": panel_number,
                "description": panel_match.group(3),
                "copy": [],
            }
            _reject_dashes(current_panel["description"], current_panel["id"])
            pages[current_page]["panels"].append(current_panel)
            continue
        if line.startswith(">") and not line.startswith("> "):
            raise ValueError(f"malformed quoted line: {line}")
        if line.strip() == "---":
            current_panel = None
            continue
        if line.startswith(">") and current_panel is None:
            raise ValueError(f"unattached quoted line: {line}")
        if current_panel is not None and re.match(r"^\s*\*[^*]+\*\s*$", line):
            if re.fullmatch(r"\*Page turn\.\*", line.strip(), re.IGNORECASE):
                current_panel = None
            else:
                current_panel.setdefault('directions', []).append(line.strip().strip('*'))
            continue
        if current_panel is not None and line.startswith("> "):
            item = _copy_line(line, current_panel["id"])
            if item is not None:
                current_panel["copy"].append(item)
            else:
                current_panel.setdefault('directions', []).append(line[2:].strip().strip('*'))
        elif current_panel is not None and line.strip():
            # Script writers may wrap a panel description over several plain lines.
            if current_panel['copy']:
                raise ValueError(f"Unattached prose after panel copy: {line}")
            current_panel["description"] += " " + line.strip()
            _reject_dashes(current_panel["description"], current_panel["id"])
    if not pages:
        raise ValueError("script contains no page headings")
    expected_pages = list(range(min(pages), max(pages) + 1))
    if sorted(pages) != expected_pages:
        raise ValueError(f"page numbers are not contiguous: {sorted(pages)}")
    panels = [panel for page in pages.values() for panel in page["panels"]]
    if not panels:
        raise ValueError("script contains no panels")
    title = _title_from_script(raw)
    return {
        "path": str(path),
        "sha256": sha256(path),
        "title": title,
        "page_count": len(pages),
        "panel_count": len(panels),
        "pages": {str(number): page for number, page in pages.items()},
    }


def _title_from_script(raw: str) -> str:
    match = re.search(r"^## (Chapter\s+\d+\s*:\s*.+)$", raw, re.MULTILINE | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"^# (.+)$", raw, re.MULTILINE)
    return match.group(1).strip() if match else "V15 Chapter"


def _continuity_blocks(raw: str) -> dict[str, str]:
    blocks: dict[str, list[str]] = {}
    current: str | None = None
    for line in raw.splitlines():
        heading = re.match(r"^##\s+(.+)$", line)
        bullet = re.match(r"^-\s+\*\*(.+?)\*\*:\s*(.*)$", line)
        if heading:
            current = heading.group(1).strip().lower()
            blocks.setdefault(current, []).append(line)
        elif bullet:
            current = bullet.group(1).strip().lower()
            blocks[current] = [line]
        elif current is not None and line.strip():
            blocks[current].append(line)
    return {key: "\n".join(value).strip() for key, value in blocks.items()}


def load_continuity(path: Path = CONTINUITY) -> dict[str, Any]:
    path = Path(path)
    raw = path.read_text(encoding="utf-8")
    _reject_dashes(raw, str(path))
    blocks = _continuity_blocks(raw)
    return {"path": str(path), "sha256": sha256(path), "raw": raw, "blocks": blocks}


def _nagoji_look(continuity: dict[str, Any], chapter: int) -> str:
    blocks = continuity["blocks"]
    block = blocks.get("nagoji sawant / ananthan pillai", "")
    constant = "strong cheekbones, straight nose, thick curled moustache, CLEAN-SHAVEN CHIN with light stubble at most, long curly black hair, small gold ear stud, lean cavalryman build"
    rows = re.findall(r"\|\s*(\d+)(?:-(\d+))?(?:\s+epilogue)?\s*\|\s*([^\n]+)", block, re.IGNORECASE)
    for low, high, look in rows:
        if int(low) <= chapter <= int(high or low):
            return constant + "; " + look.strip()
    return constant + "; " + block


def _character_look(continuity: dict[str, Any], key: str, chapter: int) -> str:
    if key == "nagoji":
        return _nagoji_look(continuity, chapter)
    aliases = CHARACTER_ALIASES.get(key, (key,))
    for name, block in continuity["blocks"].items():
        if any(alias in name for alias in aliases):
            return block
    return "No dedicated continuity block found. Use only the script description and standing rules."


def _mentioned(text: str, key: str) -> bool:
    low = text.lower()
    return any(re.search(r"\b" + re.escape(alias) + r"\b", low) for alias in CHARACTER_ALIASES.get(key, (key,)))


def infer_cast(panel: dict[str, Any], chapter: int, overrides: dict[str, Any] | None = None) -> list[str]:
    overrides = overrides or {}
    if panel["id"] in overrides:
        return sorted({str(item).lower() for item in overrides[panel["id"]]})
    if "default" in overrides:
        return sorted({str(item).lower() for item in overrides["default"]})
    text = panel["description"] + " " + " ".join(item["text"] for item in panel["copy"])
    cast = [key for key in CHARACTER_ALIASES if _mentioned(text, key)]
    # First-person narration is a conservative narrator inference for Nagoji.
    if re.search(r"\b(my|i|me|we|us)\b", text.lower()) and "nagoji" not in cast:
        cast.append("nagoji")
    # Chapter 1 is entirely Nagoji's captivity sequence; descriptions often use pronouns.
    if chapter == 1 and re.search(r"\b(his|him|he|man|prisoner|horseman)\b", text.lower()):
        cast.append("nagoji")
    return sorted(set(cast))


def _references(cast: list[str], description: str = "") -> list[str]:
    refs: list[str] = []
    for key in cast:
        if key in CONCEPTS:
            refs.append(str((CONCEPT_ROOT / CONCEPTS[key]).resolve()))
        elif key == "temple_priest":
            refs.append(str((CONCEPT_ROOT / CONCEPTS["temple_priest"]).resolve()))
    return refs


def _reference_hashes(paths: list[str]) -> dict[str, str | None]:
    return {path: sha256(Path(path)) for path in paths}


def assemble_prompt(panel: dict[str, Any], chapter: int, continuity: dict[str, Any], cast: list[str]) -> str:
    looks = [f"{key}: {_character_look(continuity, key, chapter)}" for key in cast]
    standing = continuity["raw"].split("## Standing rules for generated art", 1)[-1].strip()
    copy = panel.get("copy", [])
    copy_lines = [f"{item['speaker']}: {item['text']}" for item in copy]
    copy_rule = (
        "No text of any kind in generated art. Do not render the following exact copy; it is composited later:\n"
        + ("\n".join(copy_lines) if copy_lines else "[no copy]") +
        f"\nReserve exactly {len(copy)} blank outlined text area(s), one per copy chunk, with enough clear space for the exact characters above."
        " Keep faces, hands, and important action outside those reserves."
    )
    prompt = (
        f"V15 graphic novel panel {panel['id']} for chapter {chapter}. {panel['description']}\n\n"
        + ("SCRIPT DIRECTIONS (never render as lettering): " + " ".join(panel.get('directions', [])) + "\n\n" if panel.get('directions') else "") +
        "AUTHORITATIVE CONTINUITY, which overrides the script on appearance:\n" + "\n".join(looks) +
        "\n\nSTANDING CONTINUITY RULES:\n" + standing +
        "\n\n" + copy_rule +
        "\nNo invented lettering, pseudo-writing, logos, watermark, gore, or anachronistic costume."
    )
    _reject_dashes(prompt, f"prompt {panel['id']}")
    return prompt


def _safe_write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text(encoding="utf-8") != data:
            raise FileExistsError(f"refusing to overwrite conflicting file: {path}")
        return
    path.write_text(data, encoding="utf-8")


def default_layout(page_count: int) -> dict[str, Any]:
    return {"page_width_pt": 441.0, "page_height_pt": 666.0, "bleed_pt": 0.125 * 72,
            "art_x_pt": 36.0, "art_y_pt": 56.25, "art_width_pt": 369.0,
            "story_height_pt": 523.5, "title_band_pt": 30.0, "gap_pt": 2.0,
            "page_count": page_count, "policy": "compositor assigns rows from panel counts"}


def prepare(chapter: int, out_dir: Path, *, scripts_dir: Path = SCRIPTS,
            continuity_path: Path = CONTINUITY, cast_overrides_path: Path | None = None) -> dict[str, Any]:
    script_path = Path(scripts_dir) / f"CHAPTER-{chapter:02d}-SCRIPT.md"
    script = parse_script(script_path)
    continuity = load_continuity(continuity_path)
    overrides: dict[str, Any] = {}
    if cast_overrides_path:
        overrides = json.loads(Path(cast_overrides_path).read_text(encoding="utf-8"))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = out_dir / "SCRIPT-SNAPSHOT.json"
    snapshot = {"source": script, "captured_sha256": script["sha256"], "drift_policy": "refuse if source hash changes"}
    _safe_write(snapshot_path, json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    prompts_dir = out_dir / "prompts"
    jobs = []
    for page in script["pages"].values():
        for panel in page["panels"]:
            cast = infer_cast(panel, chapter, overrides)
            refs = _references(cast, panel["description"])
            prompt = assemble_prompt(panel, chapter, continuity, cast)
            prompt_path = prompts_dir / f"{panel['id']}.txt"
            _safe_write(prompt_path, prompt + "\n")
            refs_hashes = _reference_hashes(refs)
            lock_hash = sha256(LOCK_PATH) if LOCK_PATH.is_file() else None
            jobs.append({"id": panel["id"], "page": panel["page"], "panel": panel["panel"],
                         "cast": cast, "reference_images": refs,
                         "reference_image_sha256": refs_hashes,
                         "continuity_authority": {"path": continuity["path"], "sha256": continuity["sha256"],
                                                   "v13_lock_path": str(LOCK_PATH), "v13_lock_sha256": lock_hash},
                         "prompt_path": str(prompt_path), "prompt_sha256": sha256(prompt_path),
                         "image_gen": {"tool": "image_gen__imagegen", "args": {
                             "prompt": prompt, "referenced_image_paths": refs}},
                         "status": "awaiting_author_cast_review_and_selected_frame_ledger"})
    job = {"schema_version": 1, "chapter": chapter, "script": script,
           "continuity": {"path": continuity["path"], "sha256": continuity["sha256"]},
           "character_lock": {"path": str(LOCK_PATH), "sha256": sha256(LOCK_PATH)},
           "layout": default_layout(script["page_count"]), "jobs": jobs,
           "generation_policy": "prepare only; no image generation API calls"}
    job_path = out_dir / "IMAGEGEN-JOBS.json"
    _safe_write(job_path, json.dumps(job, indent=2, ensure_ascii=False) + "\n")
    return {"script_snapshot": str(snapshot_path), "job_json": str(job_path), "job_count": len(jobs)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prepare", nargs="?", default="prepare")
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scripts-dir", type=Path, default=SCRIPTS)
    parser.add_argument("--continuity", type=Path, default=CONTINUITY)
    parser.add_argument("--cast-overrides", type=Path)
    args = parser.parse_args(argv)
    print(json.dumps(prepare(args.chapter, args.out, scripts_dir=args.scripts_dir,
                             continuity_path=args.continuity, cast_overrides_path=args.cast_overrides), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
