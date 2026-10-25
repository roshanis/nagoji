import json, re, html
from pathlib import Path
import markdown

ROOT = Path('/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo')
SP = Path('/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad')
meta = json.load(open(SP / 'review-meta.json'))

LETTER = re.compile(r'<blockquote>\s*<p>(.*?)</p>\s*</blockquote>', re.S)
PANEL = re.compile(r'<p><strong>(\d+\.\d+[^<]{0,24})</strong>\s*(.*?)</p>', re.S)
H2 = re.compile(r'<h2>(.*?)</h2>')

def letter(m):
    body = m.group(1).strip()
    mm = re.match(r'^([^:<]{1,70}):\s*(.*)$', body, re.S)
    if mm and mm.group(1).upper() == mm.group(1) and any(c.isalpha() for c in mm.group(1)):
        spk, txt = mm.group(1).strip(), mm.group(2)
        kind = 'cap' if spk.startswith('CAPTION') else ('sfx' if spk.startswith(('SFX', 'SOUND')) else 'say')
        return f'<div class="letter {kind}"><span class="spk">{spk}</span><span class="txt">{txt}</span></div>'
    return f'<div class="letter none">{body}</div>'

def render(n, md):
    md = md.replace('<', '&lt;')
    out = markdown.markdown(md, extensions=['tables', 'fenced_code', 'sane_lists'])
    out = re.sub(r'<h1>.*?</h1>', '', out, count=1)
    out = re.sub(r'<h2>Chapter[^<]*</h2>', '', out, count=1)
    out = LETTER.sub(letter, out)
    out = PANEL.sub(lambda m: f'<div class="panel"><span class="pn">{m.group(1).strip()}</span><p>{m.group(2)}</p></div>', out)
    out = re.sub(r'<hr\s*/?>', '', out)
    # split into head (before first PAGE), pages, and trailing notes (first non-PAGE h2 after pages)
    parts = H2.split(out)
    head, body, notes, seen_page = parts[0], [], [], False
    for i in range(1, len(parts), 2):
        title, chunk = parts[i], parts[i + 1]
        pm = re.match(r'PAGE\s+(\d+)(.*)', title)
        if pm and not notes:
            seen_page = True
            extra = pm.group(2).strip()
            body.append(f'<section class="page" id="ch{n:02d}-p{pm.group(1)}"><h3 class="pageh"><span>Page {pm.group(1)}</span>'
                        + (f'<em>{extra}</em>' if extra else '') + f'</h3>{chunk}</section>')
        elif seen_page:
            notes.append(f'<h3>{title}</h3>{chunk}')
        else:
            head += f'<h3>{title}</h3>{chunk}'
    notes_html = (f'<details class="notes"><summary>Adaptation notes and review changes</summary><div class="notesbody">{"".join(notes)}</div></details>' if notes else '')
    return f'<div class="shead">{head}</div>' + ''.join(body) + notes_html

chapters = []
for m in meta:
    md = (ROOT / f'scripts/CHAPTER-{m["n"]:02d}-SCRIPT.md').read_text()
    chapters.append((m, render(m['n'], md)))

tpl = (SP / 'review_template.html').read_text()
nav = ''.join(f'<a class="navi" href="#ch{m["n"]:02d}" data-ch="ch{m["n"]:02d}"><span class="dot" data-dot="ch{m["n"]:02d}"></span><span class="nn">{m["n"]}</span><span class="nt">{html.escape(m["title"].split(": ",1)[-1])}</span></a>' for m, _ in chapters)
opts = ''.join(f'<option value="ch{m["n"]:02d}">{m["n"]}. {html.escape(m["title"].split(": ",1)[-1])}</option>' for m, _ in chapters)
rows = ''
for m, _ in chapters:
    lo, hi = m['range']
    rows += (f'<tr><td class="num">{m["n"]}</td><td><a href="#ch{m["n"]:02d}">{html.escape(m["title"].split(": ",1)[-1])}</a></td>'
             f'<td class="num">{m["pages"]}</td><td class="num muted">{m["target"]} <small>({lo} to {hi})</small></td><td class="num">{m["panels"]}</td>'
             f'<td class="num">{m["words"]:,}</td><td><span class="chip" data-chip="ch{m["n"]:02d}">Not reviewed</span></td></tr>')
secs = ''
for m, body in chapters:
    n = m['n']; lo, hi = m['range']
    ch1 = n == 1
    stat = ('<span class="drawn">Approved and drawn (r6)</span>' if ch1 else '')
    rev = ('Approved by you on 2026-09-26; art drawn.' if ch1 else f'Written, then revised against three blind reviews ({m["findings"]} findings).')
    secs += f'''<section class="chapter" id="ch{n:02d}" hidden>
<header class="chead"><p class="eyebrow">Chapter {n} of 28</p><h2>{html.escape(m["title"].split(": ",1)[-1])}</h2>{stat}
<dl class="stats"><div><dt>Pages</dt><dd>{m["pages"]}<small> target {m["target"]}, range {lo} to {hi}</small></dd></div><div><dt>Panels</dt><dd>{m["panels"]}</dd></div><div><dt>Lettered lines</dt><dd>{m["lettering"]}</dd></div><div><dt>Novel chapter</dt><dd>{m["words"]:,}<small> words</small></dd></div></dl>
<p class="revline">{rev}</p>
<div class="review" data-review="ch{n:02d}">
<div class="seg" role="group" aria-label="Review status for chapter {n}">
<button type="button" id="st-ch{n:02d}-unread" data-status="unread">Not reviewed</button>
<button type="button" id="st-ch{n:02d}-approved" data-status="approved">Approved</button>
<button type="button" id="st-ch{n:02d}-changes" data-status="changes">Needs changes</button></div>
<label for="note-ch{n:02d}">Your notes for this chapter (name the page and panel, for example 3.2)</label>
<textarea id="note-ch{n:02d}" rows="4" placeholder="Changes you want, lines to restore, anything that reads wrong."></textarea>
<div class="saverow"><button type="button" class="save" id="save-ch{n:02d}">Save</button><span class="savemsg" aria-live="polite"></span></div>
</div></header>
<div class="script">{body}</div>
<p class="backtop"><a href="#overview">Back to all chapters</a></p>
</section>'''
out = tpl.replace('{{NAV}}', nav).replace('{{OPTS}}', opts).replace('{{ROWS}}', rows).replace('{{SECTIONS}}', secs)
out = out.replace('{{TOTALPAGES}}', str(sum(m['pages'] for m, _ in chapters))).replace('{{TOTALPANELS}}', f"{sum(m['panels'] for m, _ in chapters):,}")
assert '—' not in out and '–' not in out, 'dash'
(SP / 'script-review' / 'script-review.html').write_text(out)
print(len(out) // 1024, 'KB')
