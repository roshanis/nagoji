#!/usr/bin/env python3
"""scan_slop.py: repetition and tic-density audit for a folder of markdown chapters.

Pure Python 3 standard library. Written for the second edition of
"Horse of the Servant", but it works on any folder of chapter files.

Usage (run from the repository root):

    python3 book1_horse_servant_2e/audit/tools/scan_slop.py book1_horse_servant
    python3 .../scan_slop.py book1_horse_servant_2e/manuscript -b book1_horse_servant
    python3 .../scan_slop.py book1_horse_servant -k as_if,not_but     (every hit, with line)
    python3 .../scan_slop.py book1_horse_servant -k img:storm         (every storm image)
    python3 .../scan_slop.py book1_horse_servant -o report.md

Options:
    -g, --glob PATTERN     files to read inside DIR (default: book*_chapter*.md)
    -b, --baseline DIR     add a before/after section against an earlier draft
    -k, --hits KEYS        print only the hit list for these marker keys ("all" for every marker)
    -o, --out FILE         write the report to FILE instead of stdout
    -p, --preface FILE     insert a markdown file after the report header
    -n, --names-file FILE  extra proper names (one per line) to treat as phrase breaks
    --top N                size of the cross-chapter phrase table (default 40)
    --appendix N           rows in the appendix of other repeated phrases (default 120)
    --json FILE            also dump the numbers as JSON

What it measures:
    (a) repeated word n-grams (5 to 10 words, extended past 10 when longer runs repeat)
    (b) a fixed list of prose tics, per chapter, as counts and per 1000 words,
        plus a density ranking and a check against the style-sheet rations
    (c) repeated images, similes and "as if" continuations across chapters
    (d) sentence length and paragraph rhythm
    (e) dashes and quote-mark consistency
    plus chapter endings and whole sentences repeated across chapters.
"""

import argparse
import bisect
import datetime
import glob as globmod
import json
import math
import os
import re
import statistics
import sys
from collections import Counter, OrderedDict, defaultdict

# ===========================================================================
# Constants
# ===========================================================================

LDQ, RDQ, LSQ, RSQ = "\u201c", "\u201d", "\u2018", "\u2019"
EM_DASH, EN_DASH, HBAR, ELLIPSIS = "\u2014", "\u2013", "\u2015", "\u2026"

HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")
CHAPTER_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s*chapter\s+(\d+)\s*[:.]?\s*(.*?)\s*$", re.I)
PLAIN_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s*(.*?)\s*#*\s*$")
IMAGE_LINE_RE = re.compile(r"^\s*!\[")
RULE_RE = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
TABLE_DELIM_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
FILE_CHAPTER_RE = re.compile(r"chapter[_\s]?0*(\d+)", re.I)

WORD_RE = re.compile(
    r"[^\W\d_]+(?:['\u2019][^\W\d_]+)*(?:-[^\W\d_]+(?:['\u2019][^\W\d_]+)*)*"
    r"|\d+(?:[.,:]\d+)*"
)
SENT_END_RE = re.compile(r"[.!?\u2026]+[\"\u201d\u2019')\]]*")
ABBREVIATIONS = {"mr", "mrs", "dr", "st", "capt", "lt", "col", "gen", "rev", "sr", "jr", "mt", "vs", "fr"}
SPEECH_VERBS = set("""
said asked replied answered murmured whispered called shouted cried added snapped muttered
demanded admitted continued repeated agreed insisted warned told observed remarked laughed
breathed growled barked hissed sighed protested pressed offered echoed conceded corrected
interrupted explained suggested noted declared announced wondered mused returned retorted
countered yelled roared bellowed grunted says asks""".split())

STOPWORDS = set("""
a about above after again against all almost along also am among an and any are around as at
away back be because been before behind being below beneath beside between beyond both but by
can cannot could did do does doing done down during each either else enough even ever every
few for from further had has have having he her here hers herself him himself his how however
i if in into is it its itself just least less like more most much must my myself neither never
no nor not now of off often on once one only onto or other others our ours ourselves out over
own past perhaps quite rather same she should since so some still such than that the their
theirs them themselves then there these they this those though through thus till to too
toward towards under until up upon us very was we were what when where whether which while who
whom whose why will with within without would yet you your yours yourself yourselves
don't didn't doesn't isn't wasn't weren't won't wouldn't couldn't shouldn't can't hadn't
hasn't haven't i'm i'd i'll i've it's he's she's that's there's they're we're you're let's
he'd she'd they'd we'd you'd what's who's s t me across inside outside near amid amidst nothing
something anything everything someone anyone everyone ones whose while
""".split())

MODALS = {"do", "does", "did", "could", "would", "should", "will", "can", "must", "might",
          "may", "shall", "need", "dare", "cannot"}
LIKE_VERB_PREV = {"would", "did", "do", "does", "not", "i", "you", "we", "they", "to", "might",
                  "may", "should", "could", "will", "don't", "didn't", "doesn't", "i'd",
                  "we'd", "you'd", "they'd", "he'd", "she'd"}
NOT_BUT_SKIP_PREV = MODALS | {"have", "has", "had"}
CONCESSIVE_NEXT = {"i", "he", "she", "it", "we", "they", "you", "there", "nobody", "none"}
SUBJECT_PRONOUNS = {"i", "he", "she", "we", "they", "it", "you", "there", "who"}
VERB_HINTS = set("""
am is are was were be been being has have had do does did done can could will would shall should
may might must said says say came come comes went go goes gone took take takes taken made make
makes saw see sees seen knew know knows known thought think told tell gave give given found find
felt feel feels left leave kept keep keeps held hold holds stood stand stands sat sit ran run runs
rode ride rides fell fall falls fallen rose rise rises meant mean means brought bring began begin
begins begun spoke speak speaks broke break breaks wore bore led lead leads lay lie lies sent spent
built caught taught fought sought bought struck hung won lost paid heard hear understood became
become grew grow drew threw shook woke wrote drove hid bit shot slept swept wept crept met set put
let lets cut hit read sang rang sank swam got get gets stuck spun spread lit fed fled bled bent
lent burnt dealt knelt leapt spat slid stole swore tore forgot forgave froze chose sprang strode
dug clung flung swung arose awoke beat blew flew withdrew want wants need needs seem seems look
looks turn turns move moves stay stays wait waits stop stops work works matter matters belong
belongs remain remains end ends
""".split())
NOT_VERBS_ED = {"hundred", "sacred", "naked", "wicked", "kindred", "creed", "breed", "steed", "speed",
                "seed", "weed", "reed", "shed", "sled", "bred", "indeed"}
AS_AS_EXCLUDE = {"soon", "long", "much", "many", "well", "far", "often", "little", "few",
                 "good", "quickly", "near", "early", "late", "fast", "best"}

RATIO_CAP = 3.0  # one marker can pull a chapter's tic index up by at most 3x the book rate

# ===========================================================================
# Parsing
# ===========================================================================


class Sentence(object):
    __slots__ = ("text", "start", "end", "line", "words", "narration")

    def __init__(self, text, start, end, line, words, narration):
        self.text, self.start, self.end = text, start, end
        self.line, self.words, self.narration = line, words, narration


class Paragraph(object):
    __slots__ = ("line", "text", "mask", "sentences", "has_dialogue", "_starts", "_lines", "cache")

    def __init__(self, parts):
        texts, starts, offset = [], [], 0
        for lineno, part in parts:
            starts.append(offset)
            texts.append(part)
            offset += len(part) + 1
        self.text = " ".join(texts)
        self._starts = starts
        self._lines = [lineno for lineno, _ in parts]
        self.line = self._lines[0]
        self.mask = quote_mask(self.text)
        self.has_dialogue = any(m and c.isalpha() for c, m in zip(self.text, self.mask))
        self.cache = {}
        self.sentences = []
        for a, b in split_sentences(self.text):
            chunk = self.text[a:b]
            narration = not any(self.mask[k] and self.text[k].isalpha() for k in range(a, b))
            self.sentences.append(Sentence(chunk, a, b, self.line_at(a), tokenize(chunk), narration))

    def line_at(self, offset):
        idx = bisect.bisect_right(self._starts, offset) - 1
        return self._lines[max(idx, 0)]

    def sentence_at(self, offset):
        for s in self.sentences:
            if s.start <= offset < s.end:
                return s
        return self.sentences[-1] if self.sentences else None


class Chapter(object):
    def __init__(self, name, path, number, title, paragraphs, raw):
        self.name, self.path, self.number, self.title = name, path, number, title
        self.paragraphs, self.raw = paragraphs, raw
        stem = os.path.splitext(os.path.basename(name))[0]
        self.label = "Ch%02d" % number if number is not None else stem
        self.words = sum(len(s.words) for p in paragraphs for s in p.sentences)


def tokenize(text):
    """Lowercased word tokens; curly apostrophes become straight ones."""
    return [w.replace(RSQ, "'").lower() for w in WORD_RE.findall(text)]


def _base(token):
    t = token.replace(RSQ, "'").lower()
    if t.endswith("'s"):
        t = t[:-2]
    return t.rstrip("'")


def quote_mask(text):
    """True for every character inside double quotes (curly or straight), quote marks included."""
    mask, inside = [], False
    for ch in text:
        if ch == LDQ:
            inside = True
            mask.append(True)
        elif ch == RDQ:
            mask.append(True)
            inside = False
        elif ch == '"':
            mask.append(True)
            inside = not inside
        else:
            mask.append(inside)
    return mask


def split_sentences(text):
    """Return (start, end) spans of sentences inside one paragraph."""
    spans, start, n = [], 0, len(text)
    while start < n and text[start].isspace():
        start += 1
    for m in SENT_END_RE.finditer(text):
        end = m.end()
        ws = re.match(r"\s+", text[end:])
        if not ws:
            continue
        nxt = end + ws.end()
        if nxt >= n:
            continue
        c = text[nxt]
        if not (c.isupper() or c.isdigit() or c in (LDQ, '"', LSQ, "(", "[")):
            continue
        punct = m.group(0)
        if punct[0] == ".":
            prev = re.search(r"([A-Za-z]+)$", text[:m.start()])
            if prev and prev.group(1).lower() in ABBREVIATIONS:
                continue
        if ("?" in punct or "!" in punct) and punct[-1] in (RDQ, '"', RSQ):
            follow = [w.lower() for w in re.findall(r"[A-Za-z]+", text[nxt:nxt + 60])][:4]
            if any(w in SPEECH_VERBS for w in follow):
                continue  # "Where?" I asked.  stays one sentence
        if text[start:end].strip():
            spans.append((start, end))
        start = nxt
    tail_end = len(text.rstrip())
    if start < tail_end:
        spans.append((start, tail_end))
    return spans


def _clean_line(line):
    line = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", line)
    line = re.sub(r"\[\^[^\]]+\]", "", line)
    line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"<[^>]+>", "", line)
    line = re.sub(r"^\s*>\s?", "", line)
    line = line.replace("*", "")
    line = re.sub(r"(?<!\w)_+|_+(?!\w)", "", line)
    return line.strip()


def parse_chapter(text, name="chapter.md", path=""):
    """Parse one markdown chapter into paragraphs and sentences. Headings, images,
    horizontal rules, tables and HTML comments are not prose and are skipped."""
    number, title = None, None
    paragraphs, buf = [], []
    in_comment = False

    def flush():
        if buf:
            paragraphs.append(Paragraph(list(buf)))
            del buf[:]

    for lineno, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if in_comment:
            if "-->" in s:
                in_comment = False
            continue
        if s.startswith("<!--"):
            flush()
            in_comment = "-->" not in s
            continue
        if HEADING_RE.match(raw):
            flush()
            m = CHAPTER_HEADING_RE.match(raw)
            if m and number is None:
                number, title = int(m.group(1)), m.group(2).strip() or None
            elif title is None:
                title = PLAIN_HEADING_RE.match(raw).group(1)
            continue
        if not s or IMAGE_LINE_RE.match(raw) or RULE_RE.match(raw) or s.startswith("|"):
            flush()
            continue
        cleaned = _clean_line(raw)
        if not cleaned:
            flush()
            continue
        buf.append((lineno, cleaned))
    flush()
    if number is None:
        m = FILE_CHAPTER_RE.search(os.path.basename(name))
        if m:
            number = int(m.group(1))
    return Chapter(name, path or name, number, title, paragraphs, text)


def load_chapters(directory, pattern):
    files = sorted(globmod.glob(os.path.join(directory, pattern)))
    chapters = []
    for f in files:
        if not os.path.isfile(f):
            continue
        with open(f, encoding="utf-8") as fh:
            chapters.append(parse_chapter(fh.read(), name=os.path.basename(f), path=f))
    chapters.sort(key=lambda c: (c.number is None, c.number or 0, c.name))
    return chapters

# ===========================================================================
# Markers
# ===========================================================================


class Hit(object):
    __slots__ = ("key", "chapter", "line", "snippet", "dialogue", "match")

    def __init__(self, key, chapter, line, snippet, dialogue=False, match=""):
        self.key, self.chapter, self.line = key, chapter, line
        self.snippet, self.dialogue, self.match = snippet, dialogue, match

    @property
    def location(self):
        return "%s:%d" % (self.chapter, self.line)


def _snip(text, start, end, width=55):
    a, b = max(0, start - width), min(len(text), end + width)
    if a > 0:
        sp = text.find(" ", a)
        if -1 < sp < start:
            a = sp + 1
    if b < len(text):
        sp = text.rfind(" ", end, b)
        if sp != -1:
            b = sp
    out = text[a:b]
    if a > 0:
        out = "..." + out
    if b < len(text):
        out += "..."
    return cell(out)


def cell(s):
    """Make text safe for a markdown table cell."""
    return s.replace("|", "/").replace("\n", " ")


def _prev_word(text, idx):
    """The word right before idx when only spaces separate them (no punctuation)."""
    m = re.search(r"([A-Za-z'\u2019]+)\s+$", text[:idx])
    return m.group(1).replace(RSQ, "'").lower() if m else None


class Marker(object):
    def __init__(self, key, short, label, desc, fn, group="core", scope="all text"):
        self.key, self.short, self.label, self.desc = key, short, label, desc
        self.fn, self.group, self.scope = fn, group, scope


def _regex_fn(pattern, flags=re.I):
    rx = re.compile(pattern, flags)

    def fn(ch, key):
        out = []
        for p in ch.paragraphs:
            for m in rx.finditer(p.text):
                out.append(Hit(key, ch.label, p.line_at(m.start()), _snip(p.text, m.start(), m.end()),
                               p.mask[m.start()], m.group(0)))
        return out
    return fn


_NOT_RE = re.compile(r"\bnot\b", re.I)
_NOT_BUT_RE = re.compile(r"\bnot\b([^.!?;:\u201c\u201d\"]{0,90}?)\bbut\b", re.I)


def not_but_spans(p):
    """Spans of 'not X (,) but Y' constructions in a paragraph (cached)."""
    if "not_but" in p.cache:
        return p.cache["not_but"]
    spans, pos = [], 0
    for m in _NOT_RE.finditer(p.text):
        if m.start() < pos or _prev_word(p.text, m.start()) in NOT_BUT_SKIP_PREV:
            continue
        t = _NOT_BUT_RE.match(p.text, m.start())
        if not t or len(tokenize(t.group(1))) > 8:
            continue
        after = tokenize(p.text[t.end():t.end() + 30])[:2]
        if after and (after[0] in CONCESSIVE_NEXT or after == ["no", "one"]):
            continue      # "not young, but no one would call her old" is concession, not correction
        spans.append((m.start(), t.end()))
        pos = t.end()
    p.cache["not_but"] = spans
    return spans


def _in_spans(pos, spans):
    return any(a <= pos < b for a, b in spans)


def _not_but(ch, key):
    return [Hit(key, ch.label, p.line_at(a), _snip(p.text, a, b), p.mask[a], p.text[a:b])
            for p in ch.paragraphs for a, b in not_but_spans(p)]


def _not_opener(ch, key):
    out = []
    for p in ch.paragraphs:
        spans = not_but_spans(p)
        for s in p.sentences:
            lead = len(s.text) - len(s.text.lstrip(LDQ + '"' + LSQ + "( "))
            if re.match(r"Not\b", s.text[lead:]) and not any(a < s.end and b > s.start for a, b in spans):
                out.append(Hit(key, ch.label, s.line, cell(s.text[:120]), p.mask[s.start + lead], "Not"))
    return out


_COMMA_NOT_RE = re.compile(
    r",\s+not\s+(?:a|an|the|in|with|for|by|as|from|to|because|of|on|at|my|his|her|their|our|out|"
    r"me|him|them|us|one|through|into|over|under|merely|just|only|this|those|these)\b", re.I)


def _comma_not(ch, key):
    out = []
    for p in ch.paragraphs:
        spans = not_but_spans(p)
        for m in _COMMA_NOT_RE.finditer(p.text):
            if not _in_spans(m.start() + m.group(0).lower().index("not"), spans):
                out.append(Hit(key, ch.label, p.line_at(m.start()), _snip(p.text, m.start(), m.end()),
                               p.mask[m.start()], m.group(0)))
    return out


_LIKE_A_RE = re.compile(r"\blike\s+(?:a|an|the)\b", re.I)


def _like_a(ch, key):
    out = []
    for p in ch.paragraphs:
        for m in _LIKE_A_RE.finditer(p.text):
            if _prev_word(p.text, m.start()) in LIKE_VERB_PREV:
                continue
            out.append(Hit(key, ch.label, p.line_at(m.start()), _snip(p.text, m.start(), m.end() + 20),
                           p.mask[m.start()], m.group(0)))
    return out


def _triad(ch, key):
    out = []
    for p in ch.paragraphs:
        run = []
        for s in p.sentences + [None]:
            if s is not None and s.narration and 1 <= len(s.words) <= 3:
                run.append(s)
                continue
            if len(run) >= 3:
                out.append(Hit(key, ch.label, run[0].line, cell(" ".join(x.text for x in run)[:120])))
            run = []
    return out


def _one_sentence_para(ch, key):
    return [Hit(key, ch.label, p.line, cell(p.text[:120]))
            for p in ch.paragraphs if not p.has_dialogue and len(p.sentences) == 1]


def _short_para_final(ch, key):
    return [Hit(key, ch.label, p.sentences[-1].line, cell(p.sentences[-1].text[:120]))
            for p in ch.paragraphs
            if not p.has_dialogue and len(p.sentences) >= 2 and len(p.sentences[-1].words) < 8]


def _rhetorical_q(ch, key):
    return [Hit(key, ch.label, s.line, cell(s.text[:140]))
            for p in ch.paragraphs for s in p.sentences
            if s.narration and s.text.rstrip(RDQ + '"' + RSQ + ") ").endswith("?")]


def is_fragment(words):
    """Heuristic verbless sentence: 1 to 8 words, no subject pronoun, no common or -ed verb form."""
    if not 1 <= len(words) <= 8:
        return False
    for w in words:
        if w in SUBJECT_PRONOUNS or w in VERB_HINTS or w.endswith("n't"):
            return False
        if len(w) > 3 and w.endswith("ed") and w not in NOT_VERBS_ED:
            return False
    return True


def _fragment(ch, key):
    return [Hit(key, ch.label, s.line, cell(s.text[:120]))
            for p in ch.paragraphs for s in p.sentences if s.narration and is_fragment(s.words)]


CORE_MARKERS = [
    Marker("not_but", "Not X but Y", "Not X, but Y",
           "'not ... but' within 8 words in one clause; skips 'did/could/would not ... but'", _not_but),
    Marker("not_opener", "Not-opener", "'Not ...' sentence opener",
           "sentence starting with Not that has no 'but' turn (the 'Not X. Y.' fragment)", _not_opener),
    Marker("comma_not", "X, not Y", "'X, not Y' correction",
           "', not a/the/in/for/because...' outside a Not-but span", _comma_not),
    Marker("as_if", "as if", "as if", "every 'as if'", _regex_fn(r"\bas if\b")),
    Marker("as_though", "as though", "as though", "every 'as though'", _regex_fn(r"\bas though\b")),
    Marker("like_a", "like a/the", "like a / like the",
           "'like a/an/the'; skips verb use after would/did/not/I/you/we/they/to", _like_a),
    Marker("soft_adverbs", "soft adv.", "slowly / quietly / softly / carefully",
           "the four soft adverbs", _regex_fn(r"\b(?:slowly|quietly|softly|carefully)\b")),
    Marker("weight_of", "weight of", "the weight of", "'the weight of'", _regex_fn(r"\bthe weight of\b")),
    Marker("something_x", "something X", "something older / deeper / else",
           "'something' + older, deeper, else, larger, greater, heavier, darker, stranger, harder, colder, more",
           _regex_fn(r"\bsomething (?:older|deeper|else|larger|greater|heavier|darker|stranger|harder|colder|more)\b")),
    Marker("first_time", "first time", "for the first time", "'for the first time'",
           _regex_fn(r"\bfor the first time\b")),
    Marker("etched", "etched", "etched", "etch, etched, etching", _regex_fn(r"\betch(?:ed|es|ing)?\b")),
    Marker("somehow", "somehow", "somehow", "'somehow'", _regex_fn(r"\bsomehow\b")),
    Marker("in_that_moment", "that moment", "in that moment",
           "'in that/this moment/instant'", _regex_fn(r"\bin (?:that|this) (?:moment|instant)\b")),
    Marker("sense_of", "a sense of", "a sense of", "'a sense of'", _regex_fn(r"\ba sense of\b")),
    Marker("triad", "triads", "three-fragment list",
           "run of 3+ narration sentences of 1 to 3 words each ('Horses. Guns. Storms.')", _triad,
           scope="narration"),
    Marker("one_sentence_para", "1-sent para", "one-sentence paragraph",
           "narration paragraph (no quoted speech) that is a single sentence", _one_sentence_para,
           scope="narration"),
    Marker("short_para_final", "short final", "short paragraph-final sentence",
           "last sentence under 8 words in a narration paragraph of 2+ sentences (the kicker)",
           _short_para_final, scope="narration"),
    Marker("rhetorical_q", "narr. ?", "rhetorical question in narration",
           "narration sentence (outside quotes) ending in '?'", _rhetorical_q, scope="narration"),
]

EXTENDED_MARKERS = [
    Marker("fragment", "fragments", "verbless fragment",
           "narration sentence of 1 to 8 words with no subject pronoun and no common or -ed verb form "
           "('Together.', 'Fresh men.', 'Not yet.'); heuristic", _fragment, "extended", "narration"),
    Marker("kind_of", "kind/sort of", "the kind of / the sort of", "'the/a kind of', 'the/a sort of'",
           _regex_fn(r"\b(?:the|a)\s+(?:kind|sort)\s+of\b"), "extended"),
    Marker("stock_atmosphere", "stock air", "stock atmosphere",
           "hung in the air, thick with, had nothing to do with, another world, the air was thick/heavy",
           _regex_fn(r"\bhung in the air\b|\bhanging in the air\b|\bthick with\b|\bhad nothing to do with\b"
                     r"|\banother world\b|\bthe air (?:was|grew) (?:thick|heavy)\b"), "extended"),
    Marker("gently_silently", "gently/silently", "gently / silently", "'gently', 'silently'",
           _regex_fn(r"\b(?:gently|silently)\b"), "extended"),
    Marker("somewhere", "somewhere", "somewhere", "vague placing: 'somewhere'",
           _regex_fn(r"\bsomewhere\b"), "extended"),
    Marker("perhaps", "perhaps", "perhaps", "'perhaps'", _regex_fn(r"\bperhaps\b"), "extended"),
    Marker("nodded", "nodded", "nodded", "'nodded', 'nodding'", _regex_fn(r"\bnodd(?:ed|ing)\b"), "extended"),
    Marker("jaw", "jaw", "jaw tightened", "'jaw' + tightened, set, clenched, hardened, worked",
           _regex_fn(r"\bjaws?\s+(?:tightened|tightening|set|clenched|hardened|worked)\b"), "extended"),
    Marker("eyes_verb", "eyes/gaze +verb", "eyes / gaze + motion verb",
           "'eyes/gaze/glance' + narrowed, flicked, moved, lingered, rested, met, held, ...",
           _regex_fn(r"\b(?:eyes|gaze|glance)\s+(?:narrowed|flicked|moved|went|lingered|rested|followed|met|"
                     r"held|drifted|darted|slid|travelled|traveled|swept|fixed|fell|returned|softened|"
                     r"hardened|widened|searched)\b"), "extended"),
    Marker("appraising", "studied me", "appraising look",
           "studied/measured/weighed/considered/regarded + me/him/her/us/them",
           _regex_fn(r"\b(?:studied|studying|measured|measuring|weighed|weighing|appraised|appraising|"
                     r"assessed|assessing|considered|considering|regarded|regarding)\s+(?:me|him|her|us|them)\b"),
           "extended"),
    Marker("long_moment", "long moment", "a long moment", "'a long moment'",
           _regex_fn(r"\ba long moment\b"), "extended"),
    Marker("said_nothing", "said nothing", "said nothing / did not answer",
           "'said nothing', 'did not answer/reply/respond', 'made no answer', 'said no more'",
           _regex_fn(r"\bsaid nothing\b|\bdid not (?:answer|reply|respond)\b|\bmade no (?:answer|reply)\b"
                     r"|\bsaid no more\b"), "extended"),
    Marker("something_in", "something in", "something in his eyes / voice",
           "'something in his/her/their/my eyes, voice, face, manner, tone'",
           _regex_fn(r"\bsomething in (?:his|her|their|my|your|the) (?:eyes|voice|face|manner|tone|gaze|"
                     r"expression)\b"), "extended"),
    Marker("noticing", "the way he", "the way he / she ...", "'the way he/she/they/his/the ...'",
           _regex_fn(r"\bthe way (?:he|she|they|his|her|their|a|an|the|my|it)\b"), "extended"),
    Marker("lesson", "lesson", "narrated lesson", "'I learned/understood/realised', 'the lesson', 'began to understand'",
           _regex_fn(r"\bI (?:had )?(?:learned|learnt|understood|realised|realized)\b|\bthe lesson\b"
                     r"|\bbegan to understand\b"), "extended"),
    Marker("provisional_close", "for now", "for now / that was enough",
           "'for now', 'for the moment', 'that/it was enough'",
           _regex_fn(r"\bfor now\b|\bfor the moment\b|\b(?:that|it) was enough\b"), "extended"),
    Marker("modern_register", "modern words", "modern register",
           "modern management or therapy words the style sheet bans for a 1740s narrator: risk assessment, "
           "leverage, timeline, strategic, navigate, focus, process, journey, priority, okay, feedback ...",
           _regex_fn(r"\b(?:risk assessment|leverage|timelines?|strategic(?:ally)?|navigat\w*|focus(?:ed|ing)?|"
                     r"process(?:es|ed|ing)?|mindset|prioriti[sz]\w*|priorities|optimi[sz]\w*|okay|journeys?|"
                     r"stakeholders?|feedback|deadlines?|logistics?|efficien\w*|trauma\w*|closure)\b"),
           "extended"),
]

ALL_MARKERS = CORE_MARKERS + EXTENDED_MARKERS
MARKERS_BY_KEY = OrderedDict((m.key, m) for m in ALL_MARKERS)

CORE_TABLES = [
    ("Contrast and simile markers", ["not_but", "not_opener", "comma_not", "as_if", "as_though", "like_a"]),
    ("Soft adverbs and vague depth words", ["soft_adverbs", "weight_of", "something_x", "first_time",
                                            "etched", "somehow", "in_that_moment", "sense_of"]),
    ("Structural markers", ["triad", "one_sentence_para", "short_para_final", "rhetorical_q"]),
]
EXTENDED_TABLES = [
    ("Extended markers: stock beats and gestures", ["nodded", "jaw", "eyes_verb", "appraising",
                                                    "long_moment", "said_nothing", "something_in", "noticing"]),
    ("Extended markers: vague, summary and modern words", ["fragment", "kind_of", "stock_atmosphere",
                                                           "gently_silently", "somewhere", "perhaps", "lesson",
                                                           "provisional_close", "modern_register"]),
]


def count_markers(chapter, markers=None):
    """Return an ordered dict: marker key -> list of Hit."""
    markers = ALL_MARKERS if markers is None else markers
    return OrderedDict((m.key, m.fn(chapter, m.key)) for m in markers)


def _rate(count, words):
    return count * 1000.0 / words if words else 0.0


def chapter_marker_table(chapters, markers=None):
    rows = []
    for ch in chapters:
        hits = count_markers(ch, markers)
        counts = OrderedDict((k, len(v)) for k, v in hits.items())
        rows.append({"label": ch.label, "title": ch.title, "number": ch.number, "words": ch.words,
                     "counts": counts, "rates": OrderedDict((k, _rate(c, ch.words)) for k, c in counts.items()),
                     "hits": hits})
    return rows


def book_rates(rows, keys):
    words = sum(r["words"] for r in rows)
    return OrderedDict((k, _rate(sum(r["counts"][k] for r in rows), words)) for k in keys)


def density_ranking(chapters, reference_rates=None, rows=None):
    """Rank chapters by combined density of the core markers.

    per_1000: all core hits per 1000 words (raw, dominated by the common markers).
    index:    mean over markers of (hits + 1) / (expected hits + 1), expected = reference rate x
              chapter length, each ratio capped at RATIO_CAP, so every marker weighs the same and a
              single stray hit of a rare marker cannot dominate. 1.00 = book average."""
    keys = [m.key for m in CORE_MARKERS]
    rows = rows if rows is not None else chapter_marker_table(chapters, CORE_MARKERS)
    ref = reference_rates or book_rates(rows, keys)
    active = [k for k in keys if ref.get(k, 0) > 0]
    out = []
    for r in rows:
        ratios = OrderedDict((k, min((r["counts"][k] + 1.0) / (ref[k] * r["words"] / 1000.0 + 1.0), RATIO_CAP))
                             for k in active)
        total = sum(r["counts"][k] for k in keys)
        drivers = sorted(((v, k) for k, v in ratios.items() if v >= 1.5), reverse=True)[:3]
        out.append({"label": r["label"], "title": r["title"], "words": r["words"], "hits": total,
                    "per_1000": _rate(total, r["words"]),
                    "index": statistics.mean(ratios.values()) if ratios else 0.0,
                    "drivers": [(k, v) for v, k in drivers]})
    raw_order = sorted(out, key=lambda x: -x["per_1000"])
    for i, x in enumerate(raw_order, 1):
        x["raw_rank"] = i
    out.sort(key=lambda x: (-x["index"], -x["per_1000"]))
    for i, x in enumerate(out, 1):
        x["rank"] = i
    return out

HOTSPOT_SKIP = {"one_sentence_para"}   # paragraph shape, not a phrase to fix


def hot_spots(chapters, limit=None):
    """Paragraphs ranked by marker hits inside them (core and extended markers).
    score = distinct marker kinds + 0.5 per repeat of a kind already counted."""
    spots = []
    for ch in chapters:
        line_to_para = {}
        for i, p in enumerate(ch.paragraphs):
            for ln in p._lines:
                line_to_para[ln] = i
        per = defaultdict(list)
        for key, hits in count_markers(ch).items():
            if key in HOTSPOT_SKIP:
                continue
            for h in hits:
                idx = line_to_para.get(h.line)
                if idx is not None:
                    per[idx].append(key)
        for idx, keys in per.items():
            p = ch.paragraphs[idx]
            kinds = len(set(keys))
            spots.append({"location": "%s:%d" % (ch.label, p.line), "hits": len(keys), "kinds": kinds,
                          "score": kinds + 0.5 * (len(keys) - kinds),
                          "words": sum(len(s.words) for s in p.sentences), "markers": Counter(keys),
                          "text": p.text})
    spots.sort(key=lambda x: (-x["score"], x["words"], x["location"]))
    return spots[:limit] if limit else spots


# Style-sheet rations (STYLE_SHEET.md sections 1 and 2). limit None = special rule.
RATIONS = [
    ("Not-but family", "1, dialogue only", ("not_but", "not_opener", "comma_not"), None),
    ("as if / as though", "1", ("as_if", "as_though"), 1),
    ("like a / the", "2", ("like_a",), 2),
    ("slowly / quietly / softly", "2", ("soft_adverbs",), 2),
    ("narration questions", "1", ("rhetorical_q",), 1),
    ("verbless fragments", "3", ("fragment",), 3),
    ("triads", "0", ("triad",), 0),
    ("vague depth words", "0", ("weight_of", "something_x", "etched", "somehow", "in_that_moment",
                                "sense_of", "first_time", "stock_atmosphere"), 0),
]


def ration_check(rows):
    out = []
    for r in rows:
        cells, total = [], 0
        for name, _, keys, limit in RATIONS:
            hits = [h for k in keys for h in r["hits"][k]]
            if name.startswith("slowly"):
                hits = [h for h in hits if h.match.lower() != "carefully"]
            n = len(hits)
            if limit is None:
                dialogue = sum(1 for h in hits if h.dialogue)
                over = (n - dialogue) + max(0, dialogue - 1)
            else:
                over = max(0, n - limit)
            total += over
            cells.append((n, over))
        out.append({"label": r["label"], "cells": cells, "excess": total})
    return out

# ===========================================================================
# (a) Repeated n-grams
# ===========================================================================


class Repeat(object):
    def __init__(self, tokens, occurrences, score):
        self.tokens = tuple(tokens)
        self.phrase = " ".join(tokens)
        self.length = len(tokens)
        self.occurrences = occurrences          # sorted [(label, line, dialogue)]
        self.chapters = sorted(set(o[0] for o in occurrences))
        self.score = score

    @property
    def count(self):
        return len(self.occurrences)


def _sentence_tokens(p, s):
    """(token, offset, is_sentence_initial, original) for one sentence."""
    out, prev_end = [], s.start
    for i, m in enumerate(WORD_RE.finditer(p.text, s.start, s.end)):
        gap = p.text[prev_end:m.start()]
        opens = LDQ in gap or LSQ in gap or "(" in gap
        if not opens and '"' in gap:
            k = prev_end + gap.index('"')
            opens = p.mask[k] and (k == 0 or not p.mask[k - 1])
        out.append((m.group(0).replace(RSQ, "'").lower(), m.start(), i == 0 or opens, m.group(0)))
        prev_end = m.end()
    return out


def detect_names(chapters):
    """Proper names: words capitalised away from sentence starts and (almost) never lowercase."""
    cap_mid, lower = Counter(), Counter()
    for ch in chapters:
        for p in ch.paragraphs:
            for s in p.sentences:
                for tok, _, initial, orig in _sentence_tokens(p, s):
                    base = _base(tok)
                    if not base or base == "i" or base.startswith("i'") or not orig[0].isalpha():
                        continue
                    if orig[0].isupper():
                        if not initial:
                            cap_mid[base] += 1
                    else:
                        lower[base] += 1
    return {b for b, c in cap_mid.items() if lower[b] == 0 or (c >= 3 and c >= 4 * lower[b])}


def _content(tokens):
    return [t for t in tokens if t not in STOPWORDS and (len(t) > 1 or t.isdigit())]


def repeated_ngrams(chapters, nmin=5, nmax=10, min_chapters=2, min_total=3, names=None):
    """Maximal repeated word runs of nmin..nmax words (runs longer than nmax are merged).

    A phrase qualifies when it appears in >= min_chapters chapters or >= min_total times.
    Sentences and proper names (auto-detected, or the given set) break phrases, headings are
    never prose, and a phrase needs at least two content (non-function) words."""
    names = detect_names(chapters) if names is None else {_base(n) for n in names}
    runs, meta = [], []           # runs[r] = tokens, meta[r] = (chapter index, [(line, dialogue)])
    df = Counter()
    for ci, ch in enumerate(chapters):
        seen = set()
        for p in ch.paragraphs:
            for s in p.sentences:
                cur, cur_meta = [], []
                for tok, off, _, _ in _sentence_tokens(p, s) + [(None, None, None, None)]:
                    if tok is None or _base(tok) in names:
                        if len(cur) >= nmin:
                            runs.append(cur)
                            meta.append((ci, cur_meta))
                        cur, cur_meta = [], []
                        continue
                    seen.add(tok)
                    cur.append(tok)
                    cur_meta.append((p.line_at(off), p.mask[off]))
        df.update(seen)
    occ = defaultdict(list)
    for r, toks in enumerate(runs):
        for n in range(nmin, nmax + 1):
            for i in range(len(toks) - n + 1):
                occ[tuple(toks[i:i + n])].append((r, i))
    passing = {}
    for g, occs in occ.items():
        if len(occs) < 2:
            continue
        chs = set(meta[r][0] for r, _ in occs)
        if (len(chs) >= min_chapters or len(occs) >= min_total) and len(_content(g)) >= 2:
            passing[g] = occs
    starts = defaultdict(set)
    for g, occs in passing.items():
        starts[len(g)].update(occs)
    n_ch = max(len(chapters), 1)

    def build(tokens, occs):
        occurrences = sorted(((chapters[meta[r][0]].label,) + meta[r][1][i]) for r, i in occs)
        weight = sum(math.log(1 + float(n_ch) / max(df[t], 1)) for t in set(_content(tokens)))
        spread = math.sqrt(len(set(o[0] for o in occurrences)))
        return Repeat(tokens, occurrences, weight * len(occurrences) * spread)

    result = []
    top_at = {}
    for g, occs in passing.items():
        n = len(g)
        if n < nmax:
            longer = starts.get(n + 1, set())
            if all((r, i) in longer or (r, i - 1) in longer for r, i in occs):
                continue
            result.append(build(g, occs))
        else:
            for o in occs:
                top_at[o] = g
    for g, occs in passing.items():   # merge overlapping nmax-grams into longer phrases
        if len(g) != nmax:
            continue
        key = sorted(occs)
        r0, i0 = key[0]
        prev = top_at.get((r0, i0 - 1))
        if prev is not None and sorted((r, i + 1) for r, i in passing[prev]) == key:
            continue          # continuation of an earlier chain
        tokens, cur = list(g), g
        while True:
            r1, i1 = sorted(passing[cur])[0]
            nxt = top_at.get((r1, i1 + 1))
            if nxt is None or sorted((r, i + 1) for r, i in passing[cur]) != sorted(passing[nxt]):
                break
            tokens.append(nxt[-1])
            cur = nxt
        result.append(build(tokens, occs))
    result.sort(key=lambda x: (-x.score, -len(x.chapters), -x.count, x.phrase))
    return result


def _locations(occurrences, limit=None, dialogue_mark=True):
    grouped = OrderedDict()
    for label, line, dialogue in occurrences:
        grouped.setdefault(label, []).append("%d%s" % (line, "d" if (dialogue and dialogue_mark) else ""))
    parts = ["%s:%s" % (k, ",".join(v)) for k, v in grouped.items()]
    if limit and len(parts) > limit:
        return "; ".join(parts[:limit]) + "; +%d more" % (len(parts) - limit)
    return "; ".join(parts)

# ===========================================================================
# (c) Images, similes, "as if" continuations
# ===========================================================================

IMAGE_FAMILIES = [
    ("storm", r"storm\w*|tempest\w*|squalls?|gales?|thunder\w*|lightning"),
    ("forge / anvil", r"forg(?:e|es|ed|ing)|anvils?|smith\w*|hammer\w*|smelt\w*|furnace\w*"),
    ("blade / steel", r"blades?|steel|knife|knives|razor\w*"),
    ("tiger", r"tiger\w*|tigress\w*"),
    ("river / current", r"rivers?|currents?|streams?|flood\w*"),
    ("tide", r"tides?|tidal"),
    ("ledger / debt", r"ledgers?|tall(?:y|ied|ies)|reckon\w*|debts?"),
    ("weigh / balance", r"weigh\w*|weights?|scales?|balanc\w*"),
    ("fire / ember / ash", r"embers?|ash|ashes|smoulder\w*|smolder\w*|flames?|sparks?|kindl\w*"),
    ("chain / iron", r"chain\w*|shackle\w*|fetter\w*|irons?"),
    ("thread / web / knot", r"threads?|webs?|knots?|weav\w*|woven|fabric"),
    ("shadow", r"shadow\w*"),
    ("monsoon / rain", r"monsoon\w*|rain|rains|rained|raining|rainy"),
    ("wolf / snake / hawk", r"wol(?:f|ves)|jackals?|hawks?|snakes?|serpents?|cobras?|vultures?|kites?"),
    ("game / chess / dice", r"chess\w*|dice|gambl\w*|games?|gambit\w*|wager\w*"),
    ("cage / trap / net", r"cages?|caged|traps?|trapped|snares?|nets?"),
    ("root / seed", r"roots?|rooted|seeds?"),
    ("wound / scar", r"wounds?|wounded|scars?|scarred"),
    ("salt", r"salt\w*"),
    ("ghost / mask", r"ghosts?|ghostly|masks?|masked"),
]
_FAMILY_RES = [(name, re.compile(r"\b(?:%s)\b" % pat, re.I)) for name, pat in IMAGE_FAMILIES]
_TRIGGER_RE = re.compile(r"\blike\b|\bas\s+(?:if|though)\b|\bas\s+([A-Za-z]+)\s+as\b", re.I)


def _simile_zones(p):
    """Character spans covered by a simile clause: the 8 words after like / as if / as X as."""
    if "zones" in p.cache:
        return p.cache["zones"]
    zones = []
    for m in _TRIGGER_RE.finditer(p.text):
        word = m.group(0).lower()
        if word == "like" and _prev_word(p.text, m.start()) in LIKE_VERB_PREV:
            continue
        if m.group(1) and m.group(1).lower() in AS_AS_EXCLUDE:
            continue
        s = p.sentence_at(m.start())
        words = list(WORD_RE.finditer(p.text, m.end(), s.end if s else len(p.text)))[:8]
        if words:
            zones.append((m.end(), words[-1].end()))
    p.cache["zones"] = zones
    return zones


def image_report(chapters):
    out = []
    for name, rx in _FAMILY_RES:
        hits, fig, per = [], [], Counter()
        for ch in chapters:
            for p in ch.paragraphs:
                zones = _simile_zones(p)
                for m in rx.finditer(p.text):
                    h = Hit("img:" + name, ch.label, p.line_at(m.start()), _snip(p.text, m.start(), m.end(), 45),
                            p.mask[m.start()], m.group(0))
                    hits.append(h)
                    per[ch.label] += 1
                    if _in_spans(m.start(), zones) or re.match(r"\s+of\b", p.text[m.end():]):
                        fig.append(h)
        out.append({"family": name, "total": len(hits), "chapters": per, "figurative": fig, "hits": hits})
    return out


_LIKE_VEH_RE = re.compile(r"\blike\s+(?:(?:a|an|the|some)\s+)?", re.I)
_AS_AS_VEH_RE = re.compile(r"\bas\s+([A-Za-z]+)\s+as\s+(?:(?:a|an|the|some)\s+)?", re.I)


def _singular(w):
    if len(w) > 3 and w.endswith("s") and not w.endswith(("ss", "us", "is")):
        return w[:-1]
    return w


def simile_vehicles(chapters):
    """vehicle word -> hits, for 'like (a/the) X' and 'as ADJ as (a) X' similes."""
    out = defaultdict(list)
    for ch in chapters:
        for p in ch.paragraphs:
            for rx in (_LIKE_VEH_RE, _AS_AS_VEH_RE):
                for m in rx.finditer(p.text):
                    if rx is _LIKE_VEH_RE and _prev_word(p.text, m.start()) in LIKE_VERB_PREV:
                        continue
                    if rx is _AS_AS_VEH_RE and m.group(1).lower() in AS_AS_EXCLUDE:
                        continue
                    s = p.sentence_at(m.start())
                    seg = p.text[m.end():s.end if s else len(p.text)]
                    seg = re.split(r"[,.;:!?()\"\u201c\u201d]", seg, maxsplit=1)[0]
                    run = []
                    for w in list(WORD_RE.finditer(seg))[:3]:
                        if w.group(0).replace(RSQ, "'").lower() in STOPWORDS:
                            break
                        run.append(w)
                    if not run or run[0].group(0)[0].isupper():
                        continue
                    while len(run) > 1 and re.search(r"(?:ing|ed)$", run[-1].group(0).lower()):
                        run.pop()
                    key = _singular(_base(run[-1].group(0)))
                    end = m.end() + run[-1].end()
                    out[key].append(Hit("simile", ch.label, p.line_at(m.start()), cell(p.text[m.start():end]),
                                        p.mask[m.start()], key))
    return out


_ASIF_RE = re.compile(r"\bas\s+(?:if|though)\b", re.I)


def as_if_continuations(chapters):
    """first content word after 'as if/as though' -> hits."""
    out = defaultdict(list)
    for ch in chapters:
        for p in ch.paragraphs:
            for m in _ASIF_RE.finditer(p.text):
                s = p.sentence_at(m.start())
                seg = p.text[m.end():s.end if s else len(p.text)]
                words = list(WORD_RE.finditer(seg))[:5]
                key = next((_base(w.group(0)) for w in words if _base(w.group(0)) not in STOPWORDS), None)
                if key:
                    tail = seg[:words[-1].end()] if words else ""
                    out[key].append(Hit("as_if_cont", ch.label, p.line_at(m.start()),
                                        cell(m.group(0) + tail), p.mask[m.start()], key))
    return out

# ===========================================================================
# (d) Rhythm, (e) typography, endings, repeated sentences
# ===========================================================================


def sentence_stats(ch):
    lens = [len(s.words) for p in ch.paragraphs for s in p.sentences if s.words]
    paras = ch.paragraphs
    narr = [p for p in paras if not p.has_dialogue]
    standalone = sum(1 for i, p in enumerate(paras)
                     if not p.has_dialogue and len(p.sentences) == 1
                     and not (i > 0 and paras[i - 1].has_dialogue)
                     and not (i + 1 < len(paras) and paras[i + 1].has_dialogue))
    one = sum(1 for p in paras if len(p.sentences) == 1)
    one_narr = sum(1 for p in narr if len(p.sentences) == 1)
    dialogue_words = sum(1 for p in paras for m in WORD_RE.finditer(p.text) if p.mask[m.start()])
    mean = statistics.mean(lens) if lens else 0.0
    stdev = statistics.stdev(lens) if len(lens) > 1 else 0.0
    return {
        "words": ch.words, "sentences": len(lens), "mean": mean,
        "median": statistics.median(lens) if lens else 0.0, "stdev": stdev,
        "cv": stdev / mean if mean else 0.0,
        "short_share": 100.0 * sum(1 for n in lens if n < 8) / len(lens) if lens else 0.0,
        "long_share": 100.0 * sum(1 for n in lens if n > 30) / len(lens) if lens else 0.0,
        "paragraphs": len(paras), "one_sentence": one,
        "one_sentence_share": 100.0 * one / len(paras) if paras else 0.0,
        "narr_paragraphs": len(narr),
        "narr_one_share": 100.0 * one_narr / len(narr) if narr else 0.0,
        "standalone_one": standalone,
        "dialogue_share": 100.0 * dialogue_words / ch.words if ch.words else 0.0,
    }


def typography(text):
    prose = "\n".join(l for l in text.splitlines() if not RULE_RE.match(l) and not TABLE_DELIM_RE.match(l))
    return OrderedDict([
        ("em_dash", text.count(EM_DASH)),
        ("en_dash", text.count(EN_DASH) + text.count(HBAR)),
        ("double_hyphen", len(re.findall(r"-{2,}", prose))),
        ("curly_double", text.count(LDQ) + text.count(RDQ)),
        ("straight_double", text.count('"')),
        ("curly_apostrophe", text.count(RSQ)),
        ("straight_apostrophe", text.count("'")),
        ("ellipsis", text.count(ELLIPSIS) + len(re.findall(r"\.\.\.", text))),
    ])


ENDING_OPENERS = ("For the moment", "For now", "And some", "Perhaps", "But")
SUMMARY_WORDS_RE = re.compile(
    r"\b(enough|lesson|learn\w*|together|truth|history|future|forever|always|home|begin\w*|began|"
    r"remain\w*|carry|carried|storm\w*)\b", re.I)


def chapter_endings(chapters):
    rows = []
    for ch in chapters:
        if not ch.paragraphs:
            continue
        p = ch.paragraphs[-1]
        last = p.sentences[-1] if p.sentences else None
        flags, words = [], []
        body = p.text.lstrip(LDQ + '"' + " ")
        for op in ENDING_OPENERS:
            if body.startswith(op + " ") or body.startswith(op + ","):
                flags.append("opens '%s'" % op)
                break
        if len(p.sentences) == 1:
            flags.append("one-sentence")
        if last and len(last.words) < 8:
            flags.append("short (<8 words)")
        words = sorted(set(w.lower() for w in SUMMARY_WORDS_RE.findall(p.text)))
        if words:
            flags.append("summary word")
        stub = _single_para_chapter(ch, p)
        tics = [m.key for m in CORE_MARKERS
                if m.key not in ("one_sentence_para", "short_para_final") and m.fn(stub, m.key)]
        rows.append({"label": ch.label, "line": p.line, "text": p.text, "last": last.text if last else "",
                     "flags": flags, "summary_words": words, "tics": tics})
    return rows


def _single_para_chapter(ch, p):
    stub = Chapter(ch.name, ch.path, ch.number, ch.title, [p], "")
    stub.label = ch.label
    return stub


def ending_echoes(chapters, names, min_chapters=3):
    """Content words shared by the final two paragraphs of >= min_chapters chapters."""
    per = defaultdict(list)
    for ch in chapters:
        seen = set()
        for p in ch.paragraphs[-2:]:
            for t in tokenize(p.text):
                b = _base(t)
                if b not in STOPWORDS and b not in names and len(b) > 2:
                    seen.add(_singular(b))
        for w in seen:
            per[w].append(ch.label)
    return sorted(((w, labs) for w, labs in per.items() if len(labs) >= min_chapters),
                  key=lambda x: (-len(x[1]), x[0]))


def repeated_sentences(chapters, min_chapters=2, min_total=3, names=None):
    """Narration sentences repeated word for word; sentences made only of names are skipped."""
    names = names or set()
    groups = defaultdict(list)
    for ch in chapters:
        for p in ch.paragraphs:
            for s in p.sentences:
                if s.narration and s.words and not all(_base(w) in names for w in s.words):
                    groups[" ".join(s.words)].append((ch.label, s.line))
    out = []
    for key, locs in groups.items():
        chs = set(l for l, _ in locs)
        if len(chs) >= min_chapters or len(locs) >= min_total:
            out.append({"sentence": key, "locations": locs, "chapters": len(chs)})
    out.sort(key=lambda x: (-x["chapters"], -len(x["locations"]), x["sentence"]))
    return out

# ===========================================================================
# Report
# ===========================================================================


def md_table(headers, rows, align=None):
    if not rows:
        return "_None found._"
    align = align or ["l"] + ["r"] * (len(headers) - 1)
    sep = {"l": "---", "r": "---:", "c": ":---:"}
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(sep[a] for a in align) + "|"]
    for r in rows:
        lines.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(lines)


def _f(x, nd=1):
    return ("%." + str(nd) + "f") % x


def _cr(count, rate):
    return "%d (%s)" % (count, _f(rate)) if count else "0"


def _chapter_title(ch_or_row):
    t = ch_or_row["title"] if isinstance(ch_or_row, dict) else ch_or_row.title
    return cell(t or "")


def _display_dir(directory):
    rel = os.path.relpath(directory)
    return directory if rel.startswith("..") else rel


def render_report(chapters, directory, pattern, top=40, appendix=120, names=None, baseline=None,
                  preface=None, title=None):
    names = detect_names(chapters) if names is None else names
    rows = chapter_marker_table(chapters, ALL_MARKERS)
    core_keys = [m.key for m in CORE_MARKERS]
    ext_keys = [m.key for m in EXTENDED_MARKERS]
    total_words = sum(ch.words for ch in chapters)
    ranking = density_ranking(chapters, rows=rows)
    reps = repeated_ngrams(chapters, names=names)
    cross = [r for r in reps if len(r.chapters) >= 2]
    within = [r for r in reps if len(r.chapters) < 2]
    by_label = {ch.label: ch for ch in chapters}
    out = []
    w = out.append

    w("# %s" % (title or "Repetition and Tic Density Audit"))
    w("")
    w("Source: `%s` (files matching `%s`): %d chapters, %s words. Generated %s by "
      "`book1_horse_servant_2e/audit/tools/scan_slop.py`." % (
          _display_dir(directory), pattern, len(chapters), "{:,}".format(total_words),
          datetime.date.today().isoformat()))
    w("")
    w("Locations are `ChNN:line` (line numbers in the source file). A `d` after a line number "
      "means that occurrence sits inside quoted speech. Rates are per 1000 words.")
    w("")
    if preface:
        w(preface.rstrip())
        w("")
    w("## Contents")
    w("")
    for i, sec in enumerate(["Density ranking", "Style-sheet ration check", "Hot-spot paragraphs",
                             "Top cross-chapter repeated phrases", "Tic markers per chapter",
                             "Repeated images and similes", "Sentence rhythm", "Dashes and quote marks",
                             "Chapter endings", "Repeated whole sentences", "Appendix: other repeated phrases"],
                            1):
        w("%d. %s" % (i, sec))
    w("")

    # 1. density ranking
    w("## 1. Density ranking")
    w("")
    w("Core markers only (the %d in section 5). **Tic index** gives every marker equal weight: for each "
      "marker, (hits + 1) / (expected hits + 1), where expected = book rate x chapter length, capped at "
      "%.0fx, then averaged over the markers. 1.00 is the book average; the +1 stops one stray 'somehow' "
      "from dominating a short chapter. **Hits/1000** is the plain sum, which the common markers "
      "(one-sentence paragraphs, short kickers, soft adverbs) dominate. **Drivers** are markers at 1.5x "
      "expected or more." % (len(CORE_MARKERS), RATIO_CAP))
    w("")
    w(md_table(["Rank", "Chapter", "Title", "Words", "Core hits", "Hits/1000", "Raw rank", "Tic index",
                "Drivers (x book rate)"],
               [[x["rank"], x["label"], cell(x["title"] or ""), x["words"], x["hits"], _f(x["per_1000"]),
                 x["raw_rank"], _f(x["index"], 2),
                 ", ".join("%s %.1f" % (MARKERS_BY_KEY[k].short, v) for k, v in x["drivers"])]
                for x in ranking],
               ["r", "l", "l", "r", "r", "r", "r", "r", "l"]))
    w("")

    # 2. ration check
    w("## 2. Style-sheet ration check")
    w("")
    w("Counts against the per-chapter limits in `STYLE_SHEET.md` (sections 1 and 2). `n (+k)` means n "
      "found, k over the limit. The Not-but family is allowed once, in dialogue only, so every narration "
      "use is over. 'Vague depth words' groups the weight of, something X, etched, somehow, in that "
      "moment, a sense of, for the first time and the stock atmosphere phrases (some 'first time' uses "
      "may be literal and allowed). 'Verbless fragments' is a heuristic (narration sentences of up to 8 "
      "words with no subject pronoun and no common verb form), so treat it as a pointer, not a verdict. "
      "**Excess** is the minimum number of edits that chapter needs to meet the sheet.")
    w("")
    rc = ration_check(rows)
    heads = ["Chapter"] + ["%s (%s)" % (n, lim) for n, lim, _, _ in RATIONS] + ["Excess"]
    trows = []
    for r in rc:
        trows.append([r["label"]] + [("%d (+%d)" % (n, o) if o else str(n)) for n, o in r["cells"]]
                     + ["**%d**" % r["excess"]])
    totals = [sum(r["cells"][i][0] for r in rc) for i in range(len(RATIONS))]
    overs = [sum(r["cells"][i][1] for r in rc) for i in range(len(RATIONS))]
    trows.append(["**Book**"] + ["%d (+%d)" % (t, o) for t, o in zip(totals, overs)]
                 + ["**%d**" % sum(r["excess"] for r in rc)])
    w(md_table(heads, trows))
    w("")

    # 3. hot spots
    w("## 3. Hot-spot paragraphs")
    w("")
    w("The 30 paragraphs where marker hits (core and extended, excluding the one-sentence paragraph "
      "count) cluster most: a worklist for the line edit. **Score** = distinct marker kinds + 0.5 for "
      "each repeat of a kind, so a paragraph mixing several tics outranks one long fragment list. Ties "
      "go to the shorter paragraph.")
    w("")
    spots = hot_spots(chapters, 30)
    w(md_table(["Where", "Score", "Hits", "Words", "Markers", "Opening"],
               [[x["location"], _f(x["score"]), x["hits"], x["words"],
                 ", ".join("%s%s" % (MARKERS_BY_KEY[k].short, " x%d" % n if n > 1 else "")
                           for k, n in x["markers"].most_common()),
                 cell(x["text"][:90] + ("..." if len(x["text"]) > 90 else ""))] for x in spots],
               ["l", "r", "r", "r", "l", "l"]))
    w("")

    # 4. top cross-chapter phrases
    w("## 4. Top %d cross-chapter repeated phrases" % top)
    w("")
    w("Maximal repeated word runs of 5 to 10 words (longer runs are merged and shown whole), found in 2 or "
      "more chapters. Sentence ends and proper names break a phrase, headings are excluded, and a phrase "
      "needs at least two content words. Ranked by **score** = uses x distinctiveness x sqrt(chapters), "
      "where distinctiveness sums ln(1 + chapters / chapters-containing-word) over the phrase's content "
      "words, so rare, specific wording and wide spread both push a phrase up while common filler sinks. "
      "%d phrases qualify overall: %d cross-chapter, %d "
      "repeated 3+ times inside one chapter only. %d words were treated as names."
      % (len(reps), len(cross), len(within), len(names)))
    w("")
    w(md_table(["#", "Phrase", "Words", "Uses", "Chapters", "In speech", "Score", "Locations"],
               [[i, cell(r.phrase), r.length, r.count, len(r.chapters), sum(1 for o in r.occurrences if o[2]),
                 _f(r.score), _locations(r.occurrences)] for i, r in enumerate(cross[:top], 1)],
               ["r", "l", "r", "r", "r", "r", "r", "l"]))
    w("")
    if within:
        w("**Repeated 3+ times inside a single chapter:**")
        w("")
        w(md_table(["Phrase", "Uses", "Locations"],
                   [[cell(r.phrase), r.count, _locations(r.occurrences)] for r in within[:25]],
                   ["l", "r", "l"]))
        w("")

    # 4. markers
    w("## 5. Tic markers per chapter")
    w("")
    w("### 5.1 Marker definitions")
    w("")
    w(md_table(["Key", "Column", "Marker", "What counts", "Scope"],
               [[m.key, m.short, m.label, cell(m.desc), m.scope] for m in CORE_MARKERS],
               ["l", "l", "l", "l", "l"]))
    w("")
    w("### 5.2 Book totals")
    w("")
    brow = []
    for m in ALL_MARKERS:
        hits = [h for r in rows for h in r["hits"][m.key]]
        chs = sum(1 for r in rows if r["counts"][m.key])
        peak = max(rows, key=lambda r: r["counts"][m.key]) if rows else None
        brow.append([m.label + (" (ext.)" if m.group == "extended" else ""), len(hits),
                     _f(_rate(len(hits), total_words), 2), "%d/%d" % (chs, len(rows)),
                     "%s (%d)" % (peak["label"], peak["counts"][m.key]) if peak and peak["counts"][m.key] else "",
                     "%d%%" % round(100.0 * sum(1 for h in hits if h.dialogue) / len(hits)) if hits else ""])
    w(md_table(["Marker", "Total", "Per 1000", "Chapters", "Peak chapter", "In speech"], brow,
               ["l", "r", "r", "r", "l", "r"]))
    w("")
    soft = Counter(h.match.lower() for r in rows for h in r["hits"]["soft_adverbs"])
    w("Soft adverb breakdown: " + ", ".join("%s %d" % (k, soft.get(k, 0))
                                             for k in ("slowly", "quietly", "softly", "carefully")) + ".")
    w("")
    sub = 3
    for heading, keys in CORE_TABLES + EXTENDED_TABLES:
        w("### 5.%d %s" % (sub, heading))
        sub += 1
        w("")
        w("Each cell: count (per 1000 words).")
        w("")
        trows = [[r["label"], r["words"]] + [_cr(r["counts"][k], r["rates"][k]) for k in keys] for r in rows]
        tot = [sum(r["counts"][k] for r in rows) for k in keys]
        trows.append(["**Book**", total_words] + [_cr(t, _rate(t, total_words)) for t in tot])
        w(md_table(["Chapter", "Words"] + [MARKERS_BY_KEY[k].short for k in keys], trows))
        w("")
    w("Extended marker definitions: " + "; ".join("`%s` = %s" % (m.key, m.desc) for m in EXTENDED_MARKERS) + ".")
    w("")

    # 5. images
    w("## 6. Repeated images and similes")
    w("")
    w("### 6.1 Image families")
    w("")
    w("All uses of each word family, literal or not. **Figurative** = inside a simile clause (the 8 words "
      "after like / as if / as though / as X as) or followed directly by 'of' (a tide of men, the weight of "
      "years). Spread lists chapter:count.")
    w("")
    imgs = image_report(chapters)
    for f in imgs:
        f["fig_places"] = list(OrderedDict((h.location, h) for h in f["figurative"]).values())
    w(md_table(["Family", "Uses", "Chapters", "Figurative", "Spread", "Figurative locations"],
               [[f["family"], f["total"], len(f["chapters"]), len(f["figurative"]),
                 ", ".join("%s:%d" % (k.replace("Ch", ""), v) for k, v in sorted(f["chapters"].items())),
                 ", ".join(h.location for h in f["fig_places"][:14]) + (
                     " +%d" % (len(f["fig_places"]) - 14) if len(f["fig_places"]) > 14 else "")]
                for f in sorted(imgs, key=lambda f: -len(f["figurative"]))],
               ["l", "r", "r", "r", "l", "l"]))
    w("")
    w("### 6.2 Figurative uses in context")
    w("")
    w("Up to 8 per family, for the families that recur figuratively in 3 or more chapters.")
    w("")
    ctx = []
    for f in sorted(imgs, key=lambda f: -len(f["figurative"])):
        if len(set(h.chapter for h in f["figurative"])) >= 3:
            for h in f["fig_places"][:8]:
                ctx.append([f["family"], h.location, h.snippet])
    w(md_table(["Family", "Where", "Context"], ctx, ["l", "l", "l"]))
    w("")
    veh = simile_vehicles(chapters)
    vrows = sorted(((k, v) for k, v in veh.items() if len(set(h.chapter for h in v)) >= 2),
                   key=lambda kv: (-len(set(h.chapter for h in kv[1])), -len(kv[1]), kv[0]))
    w("### 6.3 Simile vehicles used in more than one chapter")
    w("")
    w("From 'like (a/the) X' and 'as ADJ as (a) X'. %d distinct vehicles, %d of them reused across chapters."
      % (len(veh), len(vrows)))
    w("")
    w(md_table(["Vehicle", "Uses", "Chapters", "Examples"],
               [[k, len(v), len(set(h.chapter for h in v)),
                 "; ".join("%s %s" % (h.location, h.snippet) for h in v[:5]) + (" +%d" % (len(v) - 5) if len(v) > 5 else "")]
                for k, v in vrows[:40]], ["l", "r", "r", "l"]))
    w("")
    conts = as_if_continuations(chapters)
    crows = sorted(((k, v) for k, v in conts.items() if len(set(h.chapter for h in v)) >= 2 or len(v) >= 3),
                   key=lambda kv: (-len(kv[1]), kv[0]))
    w("### 6.4 What follows 'as if' / 'as though'")
    w("")
    w("First content word after the phrase, when it recurs (2+ chapters or 3+ uses).")
    w("")
    w(md_table(["Next word", "Uses", "Chapters", "Examples"],
               [[k, len(v), len(set(h.chapter for h in v)),
                 "; ".join("%s %s" % (h.location, h.snippet) for h in v[:4]) + (" +%d" % (len(v) - 4) if len(v) > 4 else "")]
                for k, v in crows[:30]], ["l", "r", "r", "l"]))
    w("")

    # 6. rhythm
    w("## 7. Sentence rhythm")
    w("")
    w("Sentence length in words. CV = stdev / mean (higher = more varied). Short = under 8 words, "
      "long = over 30. **1-sent paras** counts every paragraph that is a single sentence (dialogue lines "
      "included); **narr. 1-sent** is the share among paragraphs with no quoted speech. **Standalone** "
      "counts one-sentence narration paragraphs with no speech on either side: the one-line kicker "
      "paragraphs inside narrative passages, as opposed to beats between lines of dialogue. **Speech** "
      "is the share of words inside quotation marks.")
    w("")
    srows, all_lens = [], []
    for ch in chapters:
        st = sentence_stats(ch)
        srows.append([ch.label, st["words"], st["sentences"], _f(st["mean"]), _f(st["median"], 0),
                      _f(st["stdev"]), _f(st["cv"], 2), "%s%%" % _f(st["short_share"], 0),
                      "%s%%" % _f(st["long_share"], 0), st["paragraphs"],
                      "%d (%s%%)" % (st["one_sentence"], _f(st["one_sentence_share"], 0)),
                      "%s%%" % _f(st["narr_one_share"], 0), st["standalone_one"],
                      "%s%%" % _f(st["dialogue_share"], 0)])
        all_lens.extend(len(s.words) for p in ch.paragraphs for s in p.sentences if s.words)
    if all_lens:
        paras = [p for ch in chapters for p in ch.paragraphs]
        one = sum(1 for p in paras if len(p.sentences) == 1)
        narr = [p for p in paras if not p.has_dialogue]
        mean = statistics.mean(all_lens)
        sd = statistics.stdev(all_lens) if len(all_lens) > 1 else 0.0
        srows.append(["**Book**", total_words, len(all_lens), _f(mean), _f(statistics.median(all_lens), 0),
                      _f(sd), _f(sd / mean if mean else 0, 2),
                      "%s%%" % _f(100.0 * sum(1 for n in all_lens if n < 8) / len(all_lens), 0),
                      "%s%%" % _f(100.0 * sum(1 for n in all_lens if n > 30) / len(all_lens), 0), len(paras),
                      "%d (%s%%)" % (one, _f(100.0 * one / len(paras), 0)),
                      "%s%%" % _f(100.0 * sum(1 for p in narr if len(p.sentences) == 1) / max(len(narr), 1), 0),
                      sum(sentence_stats(ch)["standalone_one"] for ch in chapters), ""])
    w(md_table(["Chapter", "Words", "Sentences", "Mean", "Median", "Stdev", "CV", "Short", "Long",
                "Paras", "1-sent paras", "Narr. 1-sent", "Standalone", "Speech"], srows))
    w("")

    # 7. typography
    w("## 8. Dashes and quote marks")
    w("")
    w("Em dash and double hyphen must both be zero (style sheet). Double hyphens are counted in prose "
      "lines only; horizontal rules and table rules are ignored. Mixed straight and curly quotes or "
      "apostrophes in one chapter are flagged for the copy edit (curly apostrophes also count closing "
      "single quotes).")
    w("")
    trows, tsum = [], Counter()
    for ch in chapters:
        t = typography(ch.raw)
        tsum.update(t)
        flag = "mixed quotes" if t["straight_double"] and t["curly_double"] else ""
        if t["straight_double"] and not t["curly_double"]:
            flag = "straight quotes only"
        if t["curly_apostrophe"] and t["straight_apostrophe"]:
            flag = (flag + "; " if flag else "") + "mixed apostrophes"
        if t["em_dash"] or t["double_hyphen"]:
            flag = (flag + "; " if flag else "") + "DASHES"
        trows.append([ch.label] + list(t.values()) + [flag])
    trows.append(["**Book**"] + [tsum[k] for k in typography("").keys()] + [""])
    w(md_table(["Chapter", "Em dash", "En dash", "Double hyphen", "Curly \u201c\u201d", "Straight \"",
                "Curly \u2019", "Straight '", "Ellipses", "Flag"], trows,
               ["l", "r", "r", "r", "r", "r", "r", "r", "r", "l"]))
    w("")

    # 8. endings
    w("## 9. Chapter endings")
    w("")
    w("The last paragraph of each chapter. The style sheet asks for endings on an action, an image or a "
      "line of dialogue, not a summary or moral, and bans final paragraphs opening with But, For now, For "
      "the moment, And some or Perhaps. **Tics** lists core markers firing inside that final paragraph.")
    w("")
    ends = chapter_endings(chapters)
    w(md_table(["Chapter", "Line", "Final paragraph", "Flags", "Tics"],
               [[e["label"], e["line"], cell(e["text"] if len(e["text"]) <= 160 else "..." + e["text"][-157:]),
                 ", ".join(f if f != "summary word" else "summary word (%s)" % ", ".join(e["summary_words"])
                           for f in e["flags"]),
                 ", ".join(MARKERS_BY_KEY[k].short for k in e["tics"])] for e in ends],
               ["l", "r", "l", "l", "l"]))
    w("")
    flagged = sum(1 for e in ends if e["flags"])
    w("%d of %d endings carry at least one flag." % (flagged, len(ends)))
    w("")
    echoes = ending_echoes(chapters, names)
    if echoes:
        w("**Words shared by the closing two paragraphs of 3+ chapters** (possible repeated closing ideas): "
          + "; ".join("%s (%s)" % (wd, ", ".join(l.replace("Ch", "") for l in labs)) for wd, labs in echoes[:25])
          + ".")
        w("")

    # 9. repeated sentences
    w("## 10. Repeated whole sentences")
    w("")
    w("Narration sentences (any length) that recur word for word in 2+ chapters or 3+ times. Short "
      "motif lines and stock beats that the n-gram scan is too long to catch show up here.")
    w("")
    rs = repeated_sentences(chapters, names=names)
    w(md_table(["Sentence", "Uses", "Chapters", "Locations"],
               [[cell(r["sentence"]), len(r["locations"]), r["chapters"],
                 _locations([(l, n, False) for l, n in r["locations"]], 10)] for r in rs[:40]],
               ["l", "r", "r", "l"]))
    w("")

    # baseline
    if baseline:
        w(render_baseline(chapters, baseline[1], baseline[0]))

    # appendix
    w("## 11. Appendix: other repeated phrases")
    w("")
    rest = cross[top:]
    w("Cross-chapter phrases ranked %d onward (showing %d of %d), same columns as section 4."
      % (top + 1, min(appendix, len(rest)), len(rest)))
    w("")
    w(md_table(["#", "Phrase", "Uses", "Chapters", "Score", "Locations"],
               [[i, cell(r.phrase), r.count, len(r.chapters), _f(r.score), _locations(r.occurrences)]
                for i, r in enumerate(rest[:appendix], top + 1)], ["r", "l", "r", "r", "r", "l"]))
    w("")
    return "\n".join(out)


def render_baseline(chapters, before, before_dir):
    keys = [m.key for m in CORE_MARKERS]
    after_rows = chapter_marker_table(chapters, ALL_MARKERS)
    before_rows = chapter_marker_table(before, ALL_MARKERS)
    ref = book_rates(before_rows, keys)
    after_rank = {x["label"]: x for x in density_ranking(chapters, reference_rates=ref, rows=after_rows)}
    before_rank = {x["label"]: x for x in density_ranking(before, reference_rates=ref, rows=before_rows)}
    bmap = {r["label"]: r for r in before_rows}
    out = ["## Before and after", "",
           "This draft against the baseline `%s`. Tic index here uses the baseline's book rates, so 1.00 "
           "means 'as dense as the baseline average' and lower is better. **Gained** lists core markers "
           "whose count went up in that chapter (the plan requires none)." % _display_dir(before_dir), ""]
    rows = []
    for r in after_rows:
        b = bmap.get(r["label"])
        if not b:
            rows.append([r["label"], "new", r["words"], "", "", sum(r["counts"][k] for k in keys), "", "", "", ""])
            continue
        ha, hb = sum(r["counts"][k] for k in keys), sum(b["counts"][k] for k in keys)
        gained = [MARKERS_BY_KEY[k].short for k in keys if r["counts"][k] > b["counts"][k]]
        rows.append([r["label"], b["words"], r["words"],
                     "%+.1f%%" % (100.0 * (r["words"] - b["words"]) / b["words"]) if b["words"] else "",
                     hb, ha, "%+d" % (ha - hb), _f(before_rank[r["label"]]["index"], 2),
                     _f(after_rank[r["label"]]["index"], 2), ", ".join(gained)])
    out.append(md_table(["Chapter", "Words before", "Words after", "Change", "Core hits before",
                         "Core hits after", "Delta", "Index before", "Index after", "Gained"], rows))
    out.append("")
    trows = []
    for m in ALL_MARKERS:
        tb = sum(r["counts"][m.key] for r in before_rows)
        ta = sum(r["counts"][m.key] for r in after_rows)
        trows.append([m.label, tb, ta, "%+d" % (ta - tb)])
    out.append(md_table(["Marker", "Before", "After", "Delta"], trows))
    out.append("")
    return "\n".join(out)


def render_hits(chapters, keys):
    """Plain hit listing for the requested marker keys (or img:<family>)."""
    rows_by_key = OrderedDict()
    want = [k.strip() for k in keys.split(",") if k.strip()]
    if want == ["all"]:
        want = list(MARKERS_BY_KEY)
    imgs = None
    for k in want:
        if k.startswith("img:"):
            imgs = imgs or {f["family"].split(" ")[0]: f for f in image_report(chapters)}
            fam = imgs.get(k[4:].split(" ")[0])
            rows_by_key[k] = fam["hits"] if fam else None
        elif k in MARKERS_BY_KEY:
            rows_by_key[k] = [h for ch in chapters for h in MARKERS_BY_KEY[k].fn(ch, k)]
        else:
            rows_by_key[k] = None
    out = []
    for k, hits in rows_by_key.items():
        if hits is None:
            out.append("## %s: unknown key (markers: %s; images: %s)\n" % (
                k, ", ".join(MARKERS_BY_KEY), ", ".join("img:" + n.split(" ")[0] for n, _ in IMAGE_FAMILIES)))
            continue
        out.append("## %s (%d hits)\n" % (k, len(hits)))
        out.append(md_table(["Where", "Speech", "Text"],
                            [[h.location, "yes" if h.dialogue else "", h.snippet] for h in hits], ["l", "l", "l"]))
        out.append("")
    return "\n".join(out)


def to_json(chapters):
    rows = chapter_marker_table(chapters, ALL_MARKERS)
    return {
        "chapters": [{"label": r["label"], "title": r["title"], "words": r["words"],
                      "counts": r["counts"], "rates": r["rates"],
                      "stats": sentence_stats(ch), "typography": typography(ch.raw)}
                     for r, ch in zip(rows, chapters)],
        "ranking": density_ranking(chapters, rows=rows),
        "repeats": [{"phrase": r.phrase, "uses": r.count, "chapters": r.chapters, "score": r.score,
                     "locations": r.occurrences} for r in repeated_ngrams(chapters)],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Repetition and tic-density audit for markdown chapters.")
    ap.add_argument("directory", help="folder holding the chapter files")
    ap.add_argument("-g", "--glob", default="book*_chapter*.md", help="file pattern (default: %(default)s)")
    ap.add_argument("-b", "--baseline", help="earlier draft folder to compare against")
    ap.add_argument("-k", "--hits", help="comma-separated marker keys (or img:<family>, or all): list every hit")
    ap.add_argument("-o", "--out", help="write the report here instead of stdout")
    ap.add_argument("-p", "--preface", help="markdown file inserted after the report header")
    ap.add_argument("-n", "--names-file", help="extra proper names, one per line")
    ap.add_argument("--top", type=int, default=40, help="rows in the cross-chapter phrase table")
    ap.add_argument("--appendix", type=int, default=120, help="rows in the phrase appendix")
    ap.add_argument("--json", help="also write the numbers as JSON to this file")
    ap.add_argument("--title", help="report title")
    args = ap.parse_args(argv)

    chapters = load_chapters(args.directory, args.glob)
    if not chapters:
        sys.stderr.write("No files matching %r in %s\n" % (args.glob, args.directory))
        return 2
    if args.hits:
        text = render_hits(chapters, args.hits)
    else:
        names = detect_names(chapters)
        if args.names_file:
            with open(args.names_file, encoding="utf-8") as fh:
                names |= {_base(l.strip()) for l in fh if l.strip()}
        before = (args.baseline, load_chapters(args.baseline, args.glob)) if args.baseline else None
        preface = None
        if args.preface:
            with open(args.preface, encoding="utf-8") as fh:
                preface = fh.read()
        text = render_report(chapters, args.directory, args.glob, top=args.top, appendix=args.appendix,
                             names=names, baseline=before, preface=preface, title=args.title)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(to_json(chapters), fh, indent=1, default=list)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    else:
        sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
