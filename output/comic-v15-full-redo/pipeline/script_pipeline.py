#!/usr/bin/env python3
"""Prepare a reproducible V15 chapter art job from an approved script.

This module only parses and prepares prompts. It never calls image generation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
V15 = ROOT / "output" / "comic-v15-full-redo"
SCRIPTS = V15 / "scripts"
CONTINUITY = V15 / "CONTINUITY.md"
CONCEPT_ROOT = ROOT / "output" / "comic-v13-reference-redesign-v1" / "concepts"
V15_CONCEPTS = V15 / "concepts"
APPROVED_SHEETS = V15_CONCEPTS / "APPROVED-SHEETS.json"
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
    "van_imhoff": ("van imhoff",),
    "dutch_envoys": ("dutch envoys", "dutch envoy"),
    "yusuf": ("yusuf",),
    "nagoji_father": ("nagoji's father",),
    "nagoji_mother": ("nagoji's mother",),
    "bhalerao": ("bhalerao",),
    "sowcar": ("sowcar",),
    "donnadi": ("donnadi",),
    "madurai_troop": ("madurai troop", "madurai lancers", "madurai riders", "madurai horse"),
    "kollamkara": ("kollamkara",),
    "chanda_sahib": ("chanda sahib",),
    "kanka": ("kanka",),
    "kayal": ("kayal",),
    "grey_gelding": ("grey gelding",),
    "megha": ("megha",),
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
        bullet = re.match(r"^-\s+\*\*(.+?)\*\*(?:\s*\([^)]*\))?:\s*(.*)$", line)
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
    constant = " ".join(line.strip() for line in block.split('|', 1)[0].splitlines()
                        if line.strip() and not line.startswith('#'))
    rows = re.findall(r"\|\s*(\d+)(?:-(\d+))?(?:\s+epilogue)?\s*\|\s*([^\n]+)", block, re.IGNORECASE)
    for low, high, look in rows:
        if int(low) <= chapter <= int(high or low):
            return (constant + "; " if constant else "") + look.strip().rstrip('|').strip()
    return constant + "; " + block


def _character_look(continuity: dict[str, Any], key: str, chapter: int) -> str:
    if key == "nagoji":
        return _nagoji_look(continuity, chapter)
    aliases = CHARACTER_ALIASES.get(key, (key.replace('_', ' '),))
    for name, block in continuity["blocks"].items():
        if any(alias in name for alias in aliases):
            return _look_for_chapter(block, chapter)
    return "No dedicated continuity block found. Use only the script description and standing rules."


_CHAPTER_ROW = re.compile(r"^\s*\|\s*(\d[\d,\s-]*?)\s*\|\s*(.+?)\s*\|?\s*$")
_SPAN_ROW = re.compile(r"^\s*\|\s*\d[\d,\s-]*?\s+@")


def _chapters(spec: str) -> set[int]:
    chapters: set[int] = set()
    for part in spec.split(","):
        low, _, high = part.strip().partition("-")
        chapters.update(range(int(low), int(high or low) + 1))
    return chapters


def _look_for_chapter(block: str, chapter: int) -> str:
    """Keep a bullet's base look plus only the "| chapters | look |" rows for this chapter."""
    base, looks = [], []
    for line in block.splitlines():
        if _SPAN_ROW.match(line):
            continue
        row = _CHAPTER_ROW.match(line)
        if row is None:
            base.append(line)
        elif chapter in _chapters(row.group(1)):
            looks.append(row.group(2).strip())
    if not looks:
        return "\n".join(base)
    return "\n".join(base) + "\nThis chapter: " + "; ".join(looks)


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


def _concept_sheets() -> dict[str, Path]:
    """V13 sheets plus the V15 sheets the author approved, verified byte-for-byte."""
    sheets = {key: CONCEPT_ROOT / name for key, name in CONCEPTS.items()}
    if not APPROVED_SHEETS.is_file():
        return sheets
    for key, entry in json.loads(APPROVED_SHEETS.read_text(encoding="utf-8")).items():
        if key in CONCEPTS:
            raise ValueError(f"{key} keeps its V13 sheet; remove it from {APPROVED_SHEETS.name}")
        path = APPROVED_SHEETS.parent / entry["file"]
        if sha256(path) != entry["sha256"]:
            raise ValueError(f"Approved sheet changed since approval: {path}")
        sheets[key] = path
    return sheets


def _references(cast: list[str], description: str = "") -> list[str]:
    sheets = _concept_sheets()
    return [str(sheets[key].resolve()) for key in cast if key in sheets]


def _reference_hashes(paths: list[str]) -> dict[str, str | None]:
    return {path: sha256(Path(path)) for path in paths}


def assemble_prompt(panel: dict[str, Any], chapter: int, continuity: dict[str, Any], cast: list[str]) -> str:
    looks = [f"{key}: {_character_look(continuity, key, chapter)}" for key in cast]
    standing = continuity["raw"].split("## Standing rules for generated art", 1)[-1].strip()
    copy = panel.get("copy", [])
    copy_lines = [f"{item['speaker']}: {item['text']}" for item in copy]
    # The compositor draws every balloon and caption itself, so the generator only leaves room for them.
    if copy:
        space_rule = (
            f"\nLeave clear, low-detail space (sky, wall, floor or shadow) for exactly {len(copy)} lettering area(s), "
            "one per copy chunk, preferably in the upper part of the frame, with enough room for the exact characters above. "
            "Draw NO balloons, boxes, frames, outlines, banners or text of any kind in those areas or anywhere else; "
            "the lettering is added afterwards. This replaces any earlier mention of blank balloon or caption reserves. "
            "Keep faces, hands, and important action outside those areas."
        )
    else:
        space_rule = ("\nNo lettering areas are needed. Draw NO balloons, boxes, frames or text of any kind. "
                      "This replaces any earlier mention of blank balloon or caption reserves.")
    copy_rule = (
        "No text of any kind in generated art. Do not render the following exact copy; it is composited later:\n"
        + ("\n".join(copy_lines) if copy_lines else "[no copy]") + space_rule
    )
    # The generator takes the frame's shape from the prompt (3:2 unless told); a panel the script sets alone in a
    # full-width row asks for a strip, so the layout need not crop it hard or show it with bars.
    from layout_fit import layout_cues
    shape = ("FRAME SHAPE: a wide horizontal strip, about 3 to 1 (width to height), filling the whole width; keep faces "
             "and the key action inside the middle half of the height.\n\n") if layout_cues(panel)["solo"] else ""
    prompt = (
        f"V15 graphic novel panel {panel['id']} for chapter {chapter}. {panel['description']}\n\n" + shape
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


CAST_KEYS = frozenset(CHARACTER_ALIASES) | {"temple_priest"}

V2_FIRST_CHAPTER = 9
SETTING_SCOPES = frozenset(('kerala', 'court', 'coast', 'travancore_camp', 'dutch',
                            'portuguese', 'deccan', 'carnatic', 'sea'))
FOREIGN_CAST = frozenset(('duarte', 'joao', 'eustachius', 'karl', 'van_imhoff', 'dutch_envoys', 'donnadi'))
NON_PEOPLE = frozenset(('kanka', 'kayal', 'grey_gelding', 'megha', 'madurai_troop', 'dutch_envoys'))
FEMALE_CAST = frozenset(('padmini', 'revathi', 'senior_rani', 'savitri', 'nandini', 'nagoji_mother'))
MALE_CAST = CAST_KEYS - NON_PEOPLE - FEMALE_CAST
DISPLAY_NAMES = {
    'nagoji': 'Nagoji', 'varma': 'Marthanda Varma', 'padmini': 'Padmini Amma', 'revathi': 'Revathi Bayi',
    'ibrahim': 'Ibrahim Marakkar', 'duarte': 'Father Duarte', 'ramayyan': 'Ramayyan Dalawa',
    'eustachius': 'Eustachius De Lannoy', 'senior_rani': 'The Senior Rani of Attingal',
    'mathoo': 'Mathoo Tharakan', 'thoma': 'Thoma Ittyerah', 'dutch_envoys': 'Dutch envoys',
}
# Speaker-only aliases never participate in v1 cast inference.
SPEAKER_ALIASES = {alias: key for key, aliases in CHARACTER_ALIASES.items() for alias in aliases}
SPEAKER_ALIASES.update({'rani': 'senior_rani', 'tharakan': 'mathoo', 'thoma': 'thoma',
                        'envoy': 'dutch_envoys', 'senior envoy': 'dutch_envoys', 'dutch scribe': 'dutch_envoys'})
SHEET_CAVEATS = {
    'nagoji': {'sha256': 'bc270c0540427de10c753c9a8a6cc3eaa293c0aaba5e4d6e468c2b99134e2be0',
               'text': 'The hilltop fort, stone cell and fort wall behind the figures on the Nagoji sheet are not part of this panel. His ear ornament is a tiny flush gold stud on the lobe, not the hanging drop drawn on the sheet.'},
    'ibrahim': {'sha256': '20bf1a3a6baf18a66686c847243b4417df4b5dea5ebe1e8b9210ce9b82188470',
                'text': "Ibrahim's scar is a thin pale line from his LEFT ear to the jaw, not red as drawn on his sheet."},
    'padmini': {'sha256': 'f43457565bbadb7dd81d7bc27d9e469b55968449d9919667a6c595017aba6142',
                'text': "Padmini's hair is thick and BLACK; ignore the grey strands on the sheet."},
}
NO_TEXT_V2 = ('Draw NO balloons, caption boxes, panel borders or a border line around the picture, '
              'and no written characters, numerals, pseudo-writing, logos or watermark anywhere, '
              'including on banners, flags, cloth, walls and documents.')
LOOKS_HEADER_V2 = ('LOOKS (face, build, hair, facial hair, scars, marks and ear ornament always follow these lines; '
                  'footwear, sleeves, headwear, props in hand and pose follow the panel description above '
                  'wherever it is more specific):')
_V2_ROW = re.compile(r'^\s*\|\s*(\d[\d,\s-]*?)(?:\s+epilogue)?(?:\s+@([\d.-]+))?\s*\|\s*(.+?)\s*\|?\s*$', re.I)
_FOREIGN_TERMS = re.compile(r'\b(portuguese|dutch|voc|goa|european|british|redcoats?|church|chapel|jesuit|ships?|harbour|forts?|castle)\b', re.I)


def _known_fields(value, allowed, required, where):
    if not isinstance(value, dict):
        raise ValueError(f'{where} must be an object')
    unknown, missing = set(value) - set(allowed), set(required) - set(value)
    if unknown or missing:
        raise ValueError(f'{where}: unknown keys {sorted(unknown)}, missing keys {sorted(missing)}')


def _nonempty(value, where):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{where} must be non-empty text')


def load_art_direction(path, script, chapter):
    """Validate a complete sidecar without mutating the file or the parsed script."""
    path = Path(path)
    raw = path.read_text(encoding='utf-8')
    _reject_dashes(raw, str(path))
    direction = json.loads(raw)
    # Escaped Unicode dashes must not bypass the text check.
    _reject_dashes(json.dumps(direction, ensure_ascii=False), str(path))
    _known_fields(direction, ('prompt_profile', 'chapter', 'status', 'settings', 'pages', 'panels',
                             'character_notes', 'not_shown'), ('prompt_profile', 'chapter', 'status', 'settings'), 'art direction')
    if direction['prompt_profile'] != 'v2':
        raise ValueError('Unknown prompt_profile; expected v2')
    if type(direction['chapter']) is not int or direction['chapter'] != chapter:
        raise ValueError('Art direction chapter mismatch')
    if direction['status'] not in ('draft', 'approved'):
        raise ValueError('Art direction status must be draft or approved')
    settings = direction['settings']
    if not isinstance(settings, dict) or not settings:
        raise ValueError('settings must be a non-empty object')
    for key, setting in settings.items():
        _nonempty(key, 'setting id')
        _known_fields(setting, ('label', 'scopes', 'anchor', 'absent', 'time', 'allow_terms'),
                      ('label', 'scopes', 'anchor', 'absent'), f'setting {key}')
        for field in ('label', 'anchor', 'absent', 'time'):
            if field in setting:
                _nonempty(setting[field], f'{key}.{field}')
        scopes = setting['scopes']
        if not isinstance(scopes, list) or not all(isinstance(x, str) and x in SETTING_SCOPES for x in scopes):
            raise ValueError(f'Unknown setting scopes in {key}: {scopes}')
        terms = setting.get('allow_terms', [])
        if not isinstance(terms, list) or not all(isinstance(x, str) and _FOREIGN_TERMS.fullmatch(x) for x in terms):
            raise ValueError(f'Invalid allow_terms in {key}')
    panels = {x['id']: x for page in script['pages'].values() for x in page['panels']}
    for field in ('pages', 'panels', 'character_notes', 'not_shown'):
        if not isinstance(direction.get(field, {}), dict):
            raise ValueError(f'{field} must be an object')
    for page, setting in direction.get('pages', {}).items():
        if page not in script['pages'] or not isinstance(setting, str) or setting not in settings:
            raise ValueError(f'Unknown page or setting: {page}: {setting}')
    for panel_id, override in direction.get('panels', {}).items():
        if panel_id not in panels:
            raise ValueError(f'Unknown panel {panel_id}')
        _known_fields(override, ('setting', 'time', 'frame', 'distant', 'lettering_space', 'bleed', 'sheets'), (), panel_id)
        for field in ('setting', 'time', 'lettering_space', 'bleed'):
            if field in override:
                _nonempty(override[field], f'{panel_id}.{field}')
        if 'setting' in override and override['setting'] not in settings:
            raise ValueError(f'Unknown setting for {panel_id}')
        if 'frame' in override and override['frame'] not in ('standard', 'strip', 'tall'):
            raise ValueError(f'Invalid frame for {panel_id}')
        for field in ('distant', 'sheets'):
            if field in override and type(override[field]) is not bool:
                raise ValueError(f'{panel_id}.{field} must be a boolean')
    for key, note in direction.get('character_notes', {}).items():
        if key not in CAST_KEYS:
            raise ValueError(f'Unknown character_notes key {key}')
        _nonempty(note, f'character_notes.{key}')
    for panel_id, keys in direction.get('not_shown', {}).items():
        if panel_id not in panels or not isinstance(keys, list) or not all(isinstance(x, str) and x in CAST_KEYS for x in keys):
            raise ValueError(f'Invalid not_shown entry: {panel_id}')
    for panel in panels.values():
        resolved = _panel_direction(direction, panel)
        if resolved.get('setting') not in settings:
            raise ValueError(f'No setting for {panel["id"]}')
        _frame_v2(panel, resolved)
    return {**direction, 'path': str(path), 'sha256': sha256(path), 'raw': raw}


def _panel_direction(direction, panel):
    resolved = {}
    if str(panel['page']) in direction.get('pages', {}):
        resolved['setting'] = direction['pages'][str(panel['page'])]
    resolved.update(direction.get('panels', {}).get(panel['id'], {}))
    return resolved


def _span_bounds(span):
    match = re.fullmatch(r'@?(\d+)(?:\.(\d+))?(?:-(?:(\d+)(?:\.(\d+))?)?)?', span)
    if not match:
        raise ValueError(f'Invalid span {span}')
    page, panel, end_page, end_panel = match.groups()
    start = (int(page), int(panel or 1))
    if '-' not in span:
        end = (int(page), int(panel or 999))
    elif end_page:
        end = (int(end_page), int(end_panel or 999))
    else:
        end = (999, 999)
    if min(start + end) < 1 or end < start:
        raise ValueError(f'Invalid span {span}')
    return start, end


def _span_contains(span, page, panel):
    start, end = _span_bounds(span)
    return start <= (page, panel) <= end


def _rows_v2(block, chapter, page, panel):
    rows = []
    for line in block.splitlines():
        row = _V2_ROW.match(line)
        if not row:
            if '@' in line and line.lstrip().startswith('|'):
                raise ValueError(f'Invalid span row: {line}')
            continue
        chapters, span, look = row.groups()
        numbers = _chapters(chapters)
        if not numbers:
            raise ValueError(f'Invalid chapter range {chapters}')
        if span:
            _span_bounds(span)
            if len(numbers) != 1:
                raise ValueError('A span row must name exactly one chapter')
            if min(numbers) < V2_FIRST_CHAPTER:
                raise ValueError('Span rows are restricted to chapter 9 onward')
        if chapter in numbers and (not span or _span_contains(span, page, panel)):
            rows.append(look.strip())
    return rows


def _validate_spans(continuity, script, chapter):
    for name, block in continuity['blocks'].items():
        _rows_v2(block, chapter, 1, 1)
        # Chapter rows may layer (a ch20-28 tali under a ch27 funeral sari); span rows split a chapter, so they may not.
        spans = sorted(_span_bounds(row.group(2)) for row in map(_V2_ROW.match, block.splitlines())
                       if row and row.group(2) and chapter in _chapters(row.group(1)))
        for (_, end), (start, _) in zip(spans, spans[1:]):
            if start <= end:
                raise ValueError(f'{name}: chapter {chapter} span rows overlap at page {start[0]} panel {start[1]}')
        for line in block.splitlines():
            row = _V2_ROW.match(line)
            if not row or not row.group(2) or chapter not in _chapters(row.group(1)):
                continue
            span = row.group(2)
            start, end = _span_bounds(span)
            endpoints = [start] + ([] if span.endswith('-') else [end])
            for page, panel in endpoints:
                page_data = script['pages'].get(str(page))
                if page_data is None or (panel != 999 and panel > len(page_data['panels'])):
                    raise ValueError(f'Span @{span} exceeds chapter {chapter} page or panel count')


def _clean_base(text):
    match = re.match(r'^\s*-\s*\*\*(.+?)\*\*(?:\s*\([^)]*\))?:\s*(.*)$', text, re.S)
    display, base = (match.group(1), match.group(2)) if match else ('', text)
    display = re.sub(r'\s*\([^)]*\)', '', display).strip()
    base = re.sub(r'\s*\([^)]*\bch\d[^)]*\)', '', base, flags=re.I)
    clauses = re.split(r'(?<=[.;])\s+', base.strip())
    base = ' '.join(x for x in clauses if not re.search(r'\bch\d|\bchapters?\s+\d', x, re.I))
    return display, base


def _lint_look(key, base, rows):
    checks = [(base, r'\b(?:later|at first|going grey|dies|died)\b')]
    checks.extend((row, r'\b(?:until|afterwards)\b|\bafter (?:he|she|the)\b') for row in rows)
    checks.extend((text, r'\b(?:pages?|panels?)\s+\d|\bepilogue\b|\bfrom (?:the )?(?:page|panel)\b')
                  for text in [base] + rows)
    for text, pattern in checks:
        match = re.search(pattern, text, re.I)
        if match:
            raise ValueError(f'{key} look contains unresolved scope: {match.group(0)}')


def _nagoji_parts_v2(continuity, chapter, page, panel):
    block = continuity['blocks'].get('nagoji sawant / ananthan pillai', '')
    rows = _rows_v2(block, chapter, page, panel)
    if len(rows) != 1:
        raise ValueError(f'nagoji needs exactly one matching row at {chapter}:{page}.{panel}; found {len(rows)}')
    constant = ' '.join(x.strip() for x in block.split('|', 1)[0].splitlines() if x.strip() and not x.startswith('#'))
    if not rows[0].lower().startswith('captivity sheet'):
        constant = re.sub(r'\s*\([^)]*captivity only[^)]*\)', '', constant, flags=re.I)
    _, constant = _clean_base(constant)
    _lint_look('nagoji', constant, rows)
    return constant, rows[0]


def _nagoji_look_v2(continuity, chapter, page, panel):
    constant, row = _nagoji_parts_v2(continuity, chapter, page, panel)
    return '; '.join(x for x in (constant, row) if x)


def _character_block(continuity, key):
    aliases = CHARACTER_ALIASES.get(key, (key.replace('_', ' '),))
    return next((block for name, block in continuity['blocks'].items()
                 if any(alias in name for alias in aliases)), '')


def _character_look_v2(continuity, key, chapter, page, panel):
    if key == 'nagoji':
        return _nagoji_look_v2(continuity, chapter, page, panel)
    block = _character_block(continuity, key)
    if not block:
        return 'Use the panel description for this character.'
    # Base identity precedes the table; editorial notes after tables never become looks.
    _, base = _clean_base(block.split('|', 1)[0].strip())
    rows = _rows_v2(block, chapter, page, panel)
    _lint_look(key, base, rows)
    return ' '.join(x for x in [base] + rows if x)


def _display_name(key, continuity):
    if key in DISPLAY_NAMES:
        return DISPLAY_NAMES[key]
    name, _ = _clean_base(_character_block(continuity, key).split('|', 1)[0])
    return name or key.replace('_', ' ').title()


def _scoped_rules(continuity, scopes):
    heading = '## Scoped art rules (prompt profile v2)'
    if heading not in continuity['raw']:
        raise ValueError(f'Missing {heading}')
    section = re.split(r'^##\s+', continuity['raw'].split(heading, 1)[1], maxsplit=1, flags=re.M)[0]
    rules = []
    for line in section.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r'\s*- \[([^]]+)\] (.+)', line)
        if not match:
            raise ValueError(f'Invalid scoped art rule: {line}')
        tags = {x.strip() for x in match.group(1).split(',')}
        if not tags <= SETTING_SCOPES | {'all'}:
            raise ValueError(f'Unknown scope tag: {sorted(tags - SETTING_SCOPES - {"all"})}')
        if 'all' in tags or tags.intersection(scopes):
            rules.append(match.group(2))
    return rules


def _lettering_v2(copy, continuity, lettering_space=None):
    if not copy:
        return 'LETTERING: none in this panel. ' + NO_TEXT_V2
    items, object_count = [], 0
    for item in copy:
        speaker = item['speaker']
        base = speaker.split(' (', 1)[0].strip().lower()
        parenthetical = ' '.join(re.findall(r'\(([^)]*)\)', speaker)).lower()
        on_object = base in ('leaf', 'ledger') or bool(re.search(r'\b(leaf|stitched|on (?:the )?(?:left |right )?page)\b', parenthetical))
        if on_object:
            kind = 'lettering on an object'
            object_count += 1
        elif base == 'caption' or re.search(r'\bletter\b', parenthetical):
            kind = 'a caption'
        else:
            key = SPEAKER_ALIASES.get(base)
            kind = 'a speech balloon for ' + (_display_name(key, continuity) if key else 'another speaker')
            if re.search(r'\boff\b|voice-over', parenthetical):
                kind += ', speaking from off panel'
        length = len(item['text'].replace('*', ''))
        kind += ' (' + ('short' if length <= 40 else 'medium' if length <= 100 else 'long') + ')'
        hints = re.findall(r'\b(?:left|right) (?:half|page)|\binset\b', parenthetical)
        if hints:
            kind += ', placement: ' + ', '.join(hints)
        items.append(kind)
    block = (f'LETTERING: the letterer adds it afterwards, so draw none of it. This panel will carry exactly {len(copy)} '
             'lettering area(s): ' + '; '.join(items) + '. ')
    if lettering_space:
        block += 'Leave clear, low-detail space: ' + lettering_space + ' '
    elif object_count:
        block += 'Leave the described object surfaces blank for their lettering; reserve clear space for any other areas. '
    else:
        block += 'Leave clear, low-detail space (sky, wall, floor or shadow) for them, preferably in the upper part of the frame. '
    return block + 'Keep faces, hands and important action outside that space. ' + NO_TEXT_V2


def _foreign_findings(panel_id, setting, sources):
    if set(setting['scopes']) & {'dutch', 'portuguese', 'sea'}:
        return []
    allowed = {x.lower() for x in setting.get('allow_terms', [])}
    return [{'panel': panel_id, 'term': match.group(0).lower(), 'source': source}
            for source, text in sources for match in _FOREIGN_TERMS.finditer(text)
            if match.group(0).lower() not in allowed]


def _guard_foreign_terms(panel_id, setting, sources):
    findings = _foreign_findings(panel_id, setting, sources)
    if findings:
        raise ValueError('; '.join(f"{x['panel']}: {x['term']} in {x['source']}" for x in findings))


def _lint_cast_v2(panels, casts, direction):
    errors = []
    for panel in panels:
        cast = set(casts[panel['id']])
        absent = set(direction.get('not_shown', {}).get(panel['id'], []))
        if cast & absent:
            errors.append(f"{panel['id']}: cast and not_shown overlap {sorted(cast & absent)}")
        declared = cast | absent
        missing = {key for key in CAST_KEYS if _mentioned(panel['description'], key) and key not in declared}
        for pattern, key in ((r'\b(?:the king|maharaja)\b', 'varma'), (r'\b(?:diwan|dalawa)\b', 'ramayyan')):
            if re.search(pattern, panel['description'], re.I) and key not in declared:
                missing.add(key)
        if re.search(r'\b(?:him|his|he)\b', panel['description'], re.I) and not declared & MALE_CAST:
            missing.add('male principal for he/him/his (cast or not_shown)')
        if missing:
            errors.append(f"{panel['id']}: {', '.join(sorted(missing))}")
    if errors:
        raise ValueError('Cast lint: ' + '; '.join(errors))


def _frame_v2(panel, resolved):
    from layout_fit import layout_cues
    solo = layout_cues(panel)['solo']
    tall = bool(re.search(r'^tall(?:er)?\b', panel['description'].strip(), re.I))
    frame = resolved.get('frame', 'strip' if solo else 'tall' if tall else 'standard')
    # The compositor still reads script cues; reject conflicts instead of silently changing its layout.
    if (frame == 'strip') != solo or (frame == 'tall' and not tall) or (tall and frame != 'tall'):
        raise ValueError(f"{panel['id']}: frame override conflicts with script layout cues")
    if frame == 'tall':
        return 'FRAME SHAPE: a tall vertical panel, taller than it is wide; keep the described action inside the frame.'
    if frame == 'strip':
        focus = 'the key action' if resolved.get('distant') else 'faces and the key action'
        return ('FRAME SHAPE: a wide horizontal strip, about 3 to 1 (width to height), filling the whole width; '
                f'keep {focus} inside the middle half of the height.')
    return ''


def assemble_prompt_v2(panel, chapter, continuity, cast, direction, sheet_keys):
    resolved = _panel_direction(direction, panel)
    setting = direction['settings'][resolved['setting']]
    parts = [f"V15 graphic novel panel {panel['id']} for chapter {chapter}. Drawn in the book's inked graphic-novel style: "
             f"clean ink line and painted colour, never photorealistic. Place: {setting['label']}.", panel['description']]
    if re.match(r'^\s*Insert\b', panel['description'], re.I):
        parts.append('INSERT: frame only what the description names, cropped tight; no full figure and no portrait unless the description asks for a face.')
    shape = _frame_v2(panel, resolved)
    if shape:
        parts.append(shape)
    directions = [x for x in panel.get('directions', []) if not re.search(r'\b(letter|lettered|lettering|letterer|balloons?|captions?)\b', x, re.I)]
    if directions:
        parts.append('SCRIPT DIRECTIONS: ' + ' '.join(directions))
    people = [_display_name(key, continuity) for key in cast if key not in NON_PEOPLE]
    parts.append('PEOPLE IN THIS PANEL: ' + (', '.join(people) + '. Draw each named person once, with no doubles.' if people else 'no principal characters.'))
    absent = direction.get('not_shown', {}).get(panel['id'], [])
    if absent:
        parts.append('NOT SHOWN: ' + ' '.join(_display_name(key, continuity) + ' is outside the frame.' for key in absent))
    looks = {key: _character_look_v2(continuity, key, chapter, panel['page'], panel['panel']) for key in cast}
    if looks:
        parts.append(LOOKS_HEADER_V2 + '\n' + '\n'.join(_display_name(key, continuity) + ': ' + look for key, look in looks.items()))
    if sheet_keys:
        if len(set(sheet_keys)) != len(sheet_keys) or not set(sheet_keys) <= set(cast):
            raise ValueError(f"{panel['id']}: sheet_keys must be unique cast members")
        line = (f'REFERENCE SHEETS: {len(sheet_keys)} attached image(s), in this order: ' +
                ', '.join(f'{i}) {_display_name(key, continuity)}' for i, key in enumerate(sheet_keys, 1)) +
                '. They are character model sheets: use them only for faces, build, hair and costume. '
                'Ignore everything else on them: backgrounds, scenery, insets, labels, extra poses and props.')
        if 'nagoji' in sheet_keys:
            row = _nagoji_parts_v2(continuity, chapter, panel['page'], panel['panel'])[1].lower()
            if row.startswith('commander sheet'):
                line += ' For Nagoji use only the large full-length commander figure; his sleeves and footwear follow the text, not the sheet.'
            elif row.startswith('captivity sheet'):
                line += ' For Nagoji use only the captivity figure.'
            elif row.startswith('later-life sheet'):
                line += ' For Nagoji use only the later-life figure.'
            else:
                line += ' For Nagoji take only the face and build from the sheet; his costume comes from the text.'
        for key in sheet_keys:
            if key in SHEET_CAVEATS:
                line += ' ' + SHEET_CAVEATS[key]['text']
        parts.append(line)
    rules = _scoped_rules(continuity, setting['scopes'])
    parts.append('ART RULES:\n' + '\n'.join('- ' + rule for rule in rules))
    lettering = _lettering_v2(panel.get('copy', []), continuity, resolved.get('lettering_space'))
    lettering += ' Any balloon, caption or letterer wording in the description means space only, never painted lettering.'
    parts.append(lettering)
    notes = {key: direction.get('character_notes', {})[key] for key in cast if key in direction.get('character_notes', {})}
    if notes:
        parts.append('MUST MATCH:\n' + '\n'.join('- ' + _display_name(key, continuity) + ': ' + note for key, note in notes.items()))
    if resolved.get('bleed'):
        parts.append('MEMORY BLEED: ' + resolved['bleed'])
    time = resolved.get('time', setting.get('time'))
    parts.append('SETTING (this panel): ' + setting['anchor'] + (' Light: ' + time.rstrip('.') + '.' if time else '') + ' ' + setting['absent'])
    sources = [(f'look {key}', text) for key, text in looks.items() if key not in FOREIGN_CAST]
    sources += [('rules', ' '.join(rules)), ('must match', ' '.join(notes.values())), ('lettering', lettering)]
    _guard_foreign_terms(panel['id'], setting, sources)
    prompt = '\n\n'.join(parts)
    _reject_dashes(prompt, f"prompt {panel['id']}")
    return prompt


def validate_cast_overrides(overrides: dict[str, Any], script: dict[str, Any]) -> None:
    """Every panel listed exactly by id, every entry a list of known character keys."""
    ids = [panel["id"] for page in script["pages"].values() for panel in page["panels"]]
    missing = [panel_id for panel_id in ids if panel_id not in overrides]
    unknown_ids = sorted(set(overrides) - set(ids))
    if missing or unknown_ids:
        raise ValueError(f"Cast overrides must list every panel: missing {missing[:5]}, unknown {unknown_ids[:5]}")
    for panel_id, cast in overrides.items():
        if not isinstance(cast, list) or not set(cast) <= CAST_KEYS:
            raise ValueError(f"Cast for {panel_id} must be a list of known keys: {cast}")


def prepare(chapter: int, out_dir: Path, *, scripts_dir: Path = SCRIPTS,
            continuity_path: Path = CONTINUITY, cast_overrides_path: Path | None = None,
            art_direction_path: Path | None = None, allow_draft: bool = False) -> dict[str, Any]:
    if chapter >= V2_FIRST_CHAPTER and art_direction_path is None:
        raise ValueError(f'Chapter {chapter} needs an art direction file (--art-direction); prompt profile v2 applies from chapter 9')
    if art_direction_path is not None:
        if chapter < V2_FIRST_CHAPTER and Path(out_dir).resolve() == (V15 / 'chapters' / f'ch{chapter:02d}').resolve():
            raise ValueError('Cannot prepare v2 in a canonical chapter 1 to 8 package; use a sibling package')
        return _prepare_v2(chapter, Path(out_dir), Path(scripts_dir), Path(continuity_path),
                           cast_overrides_path, art_direction_path, allow_draft)
    script_path = Path(scripts_dir) / f"CHAPTER-{chapter:02d}-SCRIPT.md"
    script = parse_script(script_path)
    continuity = load_continuity(continuity_path)
    overrides: dict[str, Any] = {}
    if cast_overrides_path:
        overrides = json.loads(Path(cast_overrides_path).read_text(encoding="utf-8"))
        validate_cast_overrides(overrides, script)
    elif chapter > 1:
        raise ValueError(f"Chapter {chapter} needs a verified cast overrides file (--cast-overrides)")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    _safe_write(out_dir / "CONTINUITY-SNAPSHOT.md", continuity["raw"])
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


def _prepare_v2(chapter, out_dir, scripts_dir, continuity_path, cast_overrides_path, art_direction_path, allow_draft):
    """Plan every output and lint all panels before touching the destination."""
    script = parse_script(scripts_dir / f'CHAPTER-{chapter:02d}-SCRIPT.md')
    continuity = load_continuity(continuity_path)
    direction = load_art_direction(art_direction_path, script, chapter)
    if direction['status'] == 'draft' and not allow_draft:
        raise ValueError('Draft art direction requires --allow-draft')
    if cast_overrides_path is None:
        raise ValueError(f'Chapter {chapter} needs a verified cast overrides file (--cast-overrides)')
    overrides = json.loads(Path(cast_overrides_path).read_text(encoding='utf-8'))
    validate_cast_overrides(overrides, script)
    panels = [panel for page in script['pages'].values() for panel in page['panels']]
    casts = {panel['id']: infer_cast(panel, chapter, overrides) for panel in panels}
    _lint_cast_v2(panels, casts, direction)
    _validate_spans(continuity, script, chapter)
    # The untouched live bible is the pre-v2 A/B source, even when preparing with a proposal.
    baseline = load_continuity(CONTINUITY)
    sheets = _concept_sheets()
    lock_hash = sha256(LOCK_PATH)
    snapshot_path = out_dir / 'SCRIPT-SNAPSHOT.json'
    snapshot = {'source': script, 'captured_sha256': script['sha256'], 'drift_policy': 'refuse if source hash changes'}
    writes = [(out_dir / 'CONTINUITY-SNAPSHOT.md', continuity['raw']),
              (snapshot_path, json.dumps(snapshot, indent=2, ensure_ascii=False) + '\n'),
              (out_dir / 'ART-DIRECTION-SNAPSHOT.json', direction['raw'])]
    jobs = []
    for panel in panels:
        cast = casts[panel['id']]
        resolved = _panel_direction(direction, panel)
        sheet_keys = [key for key in cast if key in sheets] if resolved.get('sheets', True) else []
        refs = [str(sheets[key].resolve()) for key in sheet_keys]
        refs_hashes = _reference_hashes(refs)
        for key, ref in zip(sheet_keys, refs):
            if key in SHEET_CAVEATS and refs_hashes[ref] != SHEET_CAVEATS[key]['sha256']:
                raise ValueError(f'{panel["id"]}: {key} sheet caveat hash is stale; review the caveat')
        prompt = assemble_prompt_v2(panel, chapter, continuity, cast, direction, sheet_keys)
        prompt_path = out_dir / 'prompts' / f'{panel["id"]}.txt'
        writes.append((prompt_path, prompt + '\n'))
        jobs.append({'id': panel['id'], 'page': panel['page'], 'panel': panel['panel'], 'cast': cast,
                     'setting': resolved['setting'], 'sheet_keys': sheet_keys, 'reference_images': refs,
                     'reference_image_sha256': refs_hashes,
                     'continuity_authority': {'path': continuity['path'], 'sha256': continuity['sha256'],
                                             'v13_lock_path': str(LOCK_PATH), 'v13_lock_sha256': lock_hash},
                     'prompt_path': str(prompt_path), 'prompt_sha256': hashlib.sha256((prompt + '\n').encode('utf-8')).hexdigest(),
                     'v1_prompt_length': len(assemble_prompt(panel, chapter, baseline, cast)),
                     'image_gen': {'tool': 'image_gen__imagegen', 'args': {'prompt': prompt, 'referenced_image_paths': refs}},
                     'status': 'awaiting_author_cast_review_and_selected_frame_ledger'})
    job = {'schema_version': 1, 'chapter': chapter, 'prompt_profile': 'v2', 'script': script,
           'art_direction': {'path': direction['path'], 'sha256': direction['sha256']},
           'continuity': {'path': continuity['path'], 'sha256': continuity['sha256']},
           'v1_baseline': {'path': baseline['path'], 'sha256': baseline['sha256']},
           'character_lock': {'path': str(LOCK_PATH), 'sha256': lock_hash},
           'layout': default_layout(script['page_count']), 'jobs': jobs,
           'generation_policy': 'prepare only; no image generation API calls'}
    job_path = out_dir / 'IMAGEGEN-JOBS.json'
    writes.append((job_path, json.dumps(job, indent=2, ensure_ascii=False) + '\n'))
    # A conflicting old file must not leave new snapshots alongside a frozen partial package.
    for path, data in writes:
        if path.exists() and (not path.is_file() or path.read_text(encoding='utf-8') != data):
            raise FileExistsError(f'refusing to overwrite conflicting file: {path}')
    for path, data in writes:
        _safe_write(path, data)
    return {'script_snapshot': str(snapshot_path), 'job_json': str(job_path), 'job_count': len(jobs)}


def _audit_foreign_sources(prompt, panel, item, direction, continuity, expected):
    """Audit assembled and appended content, exempting only identified author and sheet text."""
    resolved = _panel_direction(direction, panel)
    authored = [panel['description'], resolved.get('bleed', ''), resolved.get('lettering_space', '')]
    authored += [x for x in panel.get('directions', []) if not re.search(r'\b(letter|lettered|lettering|letterer|balloons?|captions?)\b', x, re.I)]
    exempt_sections = {section for section in expected.split('\n\n')
                       if section.startswith(('V15 graphic novel panel ', 'SETTING (this panel):',
                                              'REFERENCE SHEETS:', 'MEMORY BLEED:', 'NOT SHOWN:'))}
    sources = []
    for section in prompt.split('\n\n'):
        if section in exempt_sections:
            continue
        if section in authored:
            continue
        if section.startswith('LOOKS ('):
            section = '\n'.join(line for line in section.splitlines()[1:]
                                if not any(line.startswith(_display_name(key, continuity) + ':') for key in FOREIGN_CAST))
        elif section.startswith('SCRIPT DIRECTIONS:'):
            section = section.removeprefix('SCRIPT DIRECTIONS: ')
            for text in authored:
                if text:
                    section = section.replace(text, '', 1)
        elif section.startswith('LETTERING:') and resolved.get('lettering_space'):
            section = section.replace(resolved['lettering_space'], '', 1)
        sources.append(('prompt text', section))
    return sources


def audit_prompts(job_json_path):
    """Read-only audit of prepared prompts and every distinct recorded sent prompt."""
    job_json_path = Path(job_json_path)
    out = job_json_path.parent
    job = json.loads(job_json_path.read_text(encoding='utf-8'))
    if job.get('prompt_profile') != 'v2':
        raise ValueError('Prompt audit requires a v2 package')
    script = json.loads((out / 'SCRIPT-SNAPSHOT.json').read_text(encoding='utf-8'))['source']
    panels = {x['id']: x for page in script['pages'].values() for x in page['panels']}
    direction = load_art_direction(out / 'ART-DIRECTION-SNAPSHOT.json', script, job['chapter'])
    if direction['sha256'] != job['art_direction']['sha256']:
        raise ValueError('Art direction snapshot hash mismatch')
    continuity = load_continuity(out / 'CONTINUITY-SNAPSHOT.md')
    if continuity['sha256'] != job['continuity']['sha256']:
        raise ValueError('Continuity snapshot hash mismatch')
    if script != job['script']:
        raise ValueError('Script snapshot differs from recorded job')
    entries, seen = [], set()
    items = {item['id']: item for item in job['jobs']}
    for item in job['jobs']:
        refs = item['reference_images']
        if set(refs) != set(item['reference_image_sha256']):
            raise ValueError(f"{item['id']}: reference paths differ from recorded hashes")
        for ref in refs:
            if not Path(ref).is_file() or sha256(Path(ref)) != item['reference_image_sha256'][ref]:
                raise ValueError(f"{item['id']}: reference image hash mismatch: {ref}")
        path = out / 'prompts' / f'{item["id"]}.txt'
        entries.append((item, path, item['prompt_sha256'], False))
        seen.add((item['id'], str(path.resolve()), item['prompt_sha256']))
    for folder in ('candidates', 'selections'):
        for record_path in sorted((out / folder).glob('*.json')):
            record = json.loads(record_path.read_text(encoding='utf-8'))
            panel_id = record.get('id')
            if panel_id not in items or 'prompt_path' not in record or 'prompt_sha256' not in record:
                raise ValueError(f'Invalid prompt provenance in {record_path}')
            path = Path(record['prompt_path'])
            if not path.is_absolute():
                path = out / path
            identity = (panel_id, str(path.resolve()), record['prompt_sha256'])
            if identity not in seen:
                entries.append((items[panel_id], path, record['prompt_sha256'], True))
                seen.add(identity)
    counts = {'prompt_count': len(entries), 'prepared_prompt_count': len(job['jobs']),
              'sent_prompt_count': sum(sent for _, _, _, sent in entries), 'setting_last': 0,
              'copy_leaks': 0, 'foreign_terms': 0, 'draw_no_once': 0, 'sheet_order_matches': 0,
              'rules_under_10_percent': 0, 'footwear_checks': 0, 'footwear_matches': 0}
    lengths, fractions, details = [], [], []
    for item, path, digest, sent in entries:
        if sha256(path) != digest:
            raise ValueError(f'Prompt hash mismatch: {path}')
        prompt = path.read_text(encoding='utf-8').strip()
        panel = panels[item['id']]
        resolved = _panel_direction(direction, panel)
        setting = direction['settings'][resolved['setting']]
        expected = assemble_prompt_v2(panel, job['chapter'], continuity, item['cast'], direction, item['sheet_keys'])
        ending = expected.split('\n\n')[-1]
        counts['setting_last'] += prompt.split('\n\n')[-1] == ending
        leaks = [chunk['text'] for chunk in panel['copy'] if len(chunk['text'].replace('*', '')) >= 10
                 and (chunk['text'] in prompt or chunk['text'].replace('*', '') in prompt)]
        findings = _foreign_findings(item['id'], setting, _audit_foreign_sources(prompt, panel, item, direction, continuity, expected))
        counts['copy_leaks'] += len(leaks)
        counts['foreign_terms'] += len(findings)
        counts['draw_no_once'] += prompt.count('Draw NO') == 1
        refs = [section for section in prompt.split('\n\n') if section.startswith('REFERENCE SHEETS:')]
        sheet_keys = item['sheet_keys']
        order = ', '.join(f'{i}) {_display_name(key, continuity)}' for i, key in enumerate(sheet_keys, 1))
        expected_paths = item['reference_images']
        order_ok = len(sheet_keys) == len(expected_paths) and len(set(expected_paths)) == len(expected_paths)
        order_ok = order_ok and (not refs if not sheet_keys else len(refs) == 1 and
                                refs[0].startswith(f'REFERENCE SHEETS: {len(sheet_keys)} attached image(s), in this order: {order}.'))
        # Check each path against its stable sheet filename, so swapping paths is detectable.
        approved = json.loads(APPROVED_SHEETS.read_text()) if APPROVED_SHEETS.is_file() else {}
        for key, ref in zip(sheet_keys, expected_paths):
            filename = CONCEPTS.get(key) or approved.get(key, {}).get('file')
            if filename and Path(ref).name != filename:
                order_ok = False
        counts['sheet_order_matches'] += bool(order_ok)
        rules = '\n\n'.join(section for section in prompt.split('\n\n') if section.startswith('ART RULES:'))
        fraction = len(rules) / len(prompt)
        fractions.append(fraction); lengths.append(len(prompt))
        counts['rules_under_10_percent'] += fraction < 0.1
        footwear_ok = None
        if job['chapter'] == 9 and 'nagoji' in item['cast']:
            counts['footwear_checks'] += 1
            look_line = next((line for line in prompt.splitlines() if line.startswith('Nagoji: ')), '')
            footwear = 'boots' if (panel['page'], panel['panel']) <= (2, 3) else 'barefoot'
            footwear_ok = footwear in look_line and ('barefoot' if footwear == 'boots' else 'boots') not in look_line
            counts['footwear_matches'] += footwear_ok
        details.append({'id': item['id'], 'path': str(path), 'sent': sent, 'characters': len(prompt),
                        'rules_fraction': round(fraction, 6), 'copy_leaks': len(leaks), 'foreign_terms': findings,
                        'footwear_matches': footwear_ok})
    baseline_lengths = [item['v1_prompt_length'] for item in job['jobs']]
    counts.update({'median_length': statistics.median(lengths) if lengths else 0,
                   'v1_median_length': statistics.median(baseline_lengths) if baseline_lengths else 0,
                   'max_rules_percent': round(max(fractions, default=0) * 100, 4), 'details': details})
    counts['median_at_or_below_v1'] = counts['median_length'] <= counts['v1_median_length']
    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", default="prepare", choices=('prepare', 'audit'))
    parser.add_argument("--chapter", type=int)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scripts-dir", type=Path, default=SCRIPTS)
    parser.add_argument("--continuity", type=Path, default=CONTINUITY)
    parser.add_argument("--cast-overrides", type=Path)
    parser.add_argument("--art-direction", type=Path)
    parser.add_argument("--allow-draft", action='store_true')
    args = parser.parse_args(argv)
    if args.command == 'audit':
        result = audit_prompts(args.out / 'IMAGEGEN-JOBS.json')
    else:
        if args.chapter is None:
            parser.error('prepare requires --chapter')
        result = prepare(args.chapter, args.out, scripts_dir=args.scripts_dir, continuity_path=args.continuity,
                         cast_overrides_path=args.cast_overrides, art_direction_path=args.art_direction, allow_draft=args.allow_draft)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
