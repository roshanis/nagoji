"""Render a small review Markdown file (headings, lists, paragraphs, one diff fence) to a themed HTML page.
Usage: [PAGE_TITLE=...] md_review_html.py SRC.md OUT.html [DIFF_FILE]   (DIFF_FILE fills a {DIFF} placeholder in SRC, rewritten in place)"""
import html, os, re, sys
from pathlib import Path
src, out = Path(sys.argv[1]), Path(sys.argv[2])
text = src.read_text()
if len(sys.argv) > 3 and '{DIFF}' in text:
    text = text.replace('{DIFF}', Path(sys.argv[3]).read_text().rstrip('\n'))
    src.write_text(text)
def inline(s):
    s = html.escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return re.sub(r'`(.+?)`', r'<code>\1</code>', s)
body, para, lists, fence = [], [], [], None
def flush():
    if para: body.append('<p>' + inline(' '.join(para)) + '</p>'); para.clear()
def close(depth=0):
    while len(lists) > depth: body.append('</li></%s>' % lists.pop())
title = 'Review'
for line in text.splitlines():
    if fence is not None:
        if line.startswith('```'):
            body.append('<pre class="diff">' + ''.join(fence) + '</pre>'); fence = None
        else:
            cls = 'add' if line.startswith('+') else 'del' if line.startswith('-') else 'hunk' if line.startswith('@@') else ''
            fence.append(f'<span class="{cls}">{html.escape(line)}</span>\n')
        continue
    if line.startswith('```'): flush(); close(); fence = []; continue
    m = re.match(r'^(#+) (.*)', line)
    if m:
        flush(); close()
        if len(m.group(1)) == 1: title = m.group(2)
        body.append(f'<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>'); continue
    m = re.match(r'^( *)(\d+\.|-) (.*)', line)
    if m:
        flush(); depth = len(m.group(1)) // 2 + 1; tag = 'ol' if m.group(2)[0].isdigit() else 'ul'
        if depth > len(lists): lists.append(tag); body.append(f'<{tag}><li>')
        else: close(depth); body.append('</li><li>')
        body.append(inline(m.group(3))); continue
    if not line.strip(): flush(); continue
    if lists: body.append(' ' + inline(line.strip()))
    else: para.append(line.strip())
flush(); close()
css = """:root{--bg:#faf7f0;--fg:#1d1b17;--muted:#6b645a;--card:#fff;--line:#e3dccd;--accent:#8a3b12;--add:#e5f3e1;--addfg:#1f5a17;--del:#fbe6e3;--delfg:#8a1f12}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#171513;--fg:#ece6da;--muted:#a59d90;--card:#211e1a;--line:#3a352e;--accent:#e08a5a;--add:#1d2e1a;--addfg:#a8d99c;--del:#3a1d19;--delfg:#f0a598}}
:root[data-theme="dark"]{--bg:#171513;--fg:#ece6da;--muted:#a59d90;--card:#211e1a;--line:#3a352e;--accent:#e08a5a;--add:#1d2e1a;--addfg:#a8d99c;--del:#3a1d19;--delfg:#f0a598}
body{background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif;margin:0;padding:24px 16px}main{max-width:900px;margin:0 auto}
h2{color:var(--accent);border-bottom:1px solid var(--line);padding-bottom:4px;margin-top:1.8em}li{margin:.4em 0}code{font-size:.9em}
pre.diff{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px;overflow-x:auto;font:12.5px/1.45 Menlo,monospace;white-space:pre-wrap;word-break:break-word}
.add{background:var(--add);color:var(--addfg);display:block}.del{background:var(--del);color:var(--delfg);display:block}.hunk{color:var(--muted);display:block}"""
out.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
               f'<title>{html.escape(os.environ.get("PAGE_TITLE", "Continuity v2 Review"))}</title><style>{css}</style></head><body><main>' + '\n'.join(body) + '</main></body></html>\n')
print('wrote', out)
