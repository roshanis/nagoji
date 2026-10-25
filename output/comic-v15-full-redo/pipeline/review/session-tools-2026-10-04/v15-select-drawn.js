export const meta = {
  name: 'v15-select-drawn',
  description: 'Pick the best candidate per panel for compositor-drawn balloons, with speaker mouth points for every speech line',
  phases: [{ title: 'Select', detail: 'one reviewer per page reads each panel contact sheet' }],
}

const V15 = '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo'
const pad = n => String(n).padStart(2, '0')
const ch = args.chapter
const PAGES = args.sheetsRoot ? args.pages.map(pg => ({page: pg.page, panels: pg.panels.map(([n, cast, versions]) => {
  const id = `page-${pad(pg.page)}-panel-${n}`
  return {id, label: `${pg.page}.${Number(n)}`, cast, versions, sheet: `${args.sheetsRoot}${id}.png`, frames: versions.map(v => `${v}=${args.framesRoot}${id}-${v}.png`).join(' '), copy: (args.copy && args.copy[id]) || ''}
})})) : args.pages
const SHEETS = args.sheets.map(s => `${s.key}: ${s.path}`).join('\n')
const DECISION = {type: 'object', properties: {decisions: {type: 'array', items: {type: 'object', properties: {
  id: {type: 'string'},
  pick: {type: ['string', 'null'], description: 'best acceptable candidate version such as v03, or null if none is acceptable'},
  backup: {type: ['string', 'null'], description: 'second acceptable version, or null'},
  tails: {type: 'array', description: 'for the PICK: one entry per SPEECH line (not captions): the speaker mouth position as fractions of the pick frame width and height; if the speaker is off-panel, the point on the frame edge nearest to where they are', items: {type: 'object', properties: {copy_index: {type: 'integer'}, x: {type: 'number'}, y: {type: 'number'}}, required: ['copy_index', 'x', 'y']}},
  faces: {type: 'array', description: 'for the PICK: every visible readable human face (any character): centre x, y as fractions of width and height, radius r as a fraction of frame HEIGHT enclosing the whole head with hair and headwear', items: {type: 'object', properties: {x: {type: 'number'}, y: {type: 'number'}, r: {type: 'number'}}, required: ['x', 'y', 'r']}},
  backup_faces: {type: 'array', description: 'same for the BACKUP, or empty', items: {type: 'object', properties: {x: {type: 'number'}, y: {type: 'number'}, r: {type: 'number'}}, required: ['x', 'y', 'r']}},
  backup_tails: {type: 'array', description: 'same for the BACKUP, or empty', items: {type: 'object', properties: {copy_index: {type: 'integer'}, x: {type: 'number'}, y: {type: 'number'}}, required: ['copy_index', 'x', 'y']}},
  issues: {type: 'string', description: 'what is wrong with the pick or with all candidates; empty if the pick is clean'},
  correction: {type: 'string', description: 'if pick is null: one precise paragraph to append to the image prompt so the next generation fixes the problem; else empty'},
}, required: ['id', 'pick', 'backup', 'tails', 'backup_tails', 'faces', 'backup_faces', 'issues', 'correction']}}}, required: ['decisions']}

const results = await pipeline(PAGES, page => agent(
`You are choosing finished art for page ${page.page} of Chapter ${ch} of the graphic novel "Horse of the Servant" (Travancore and Goa, 1738 to 1753). For each panel below, Read its contact sheet (every candidate the image generator produced, labelled v01, v02, ...) and pick the best ACCEPTABLE candidate. Zoom with crops if needed (Python with Pillow: /Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python; save crops under $TMPDIR and Read them).

Script: ${V15}/scripts/CHAPTER-${pad(ch)}-SCRIPT.md (panel "**${page.page}.N**" blocks: art direction plus "> " lettering lines). Continuity bible: ${V15}/CONTINUITY.md (base lines plus the rows for chapter ${ch}; Nagoji's table row for chapter ${ch}). Character sheets (Read the ones for each panel's cast):
${SHEETS}

A candidate is ACCEPTABLE only if: every drawn principal matches their sheet and the chapter's bible row (Nagoji: thick curled moustache, CLEAN-SHAVEN chin, small gold ear stud); the panel shows the script beat (who is present, action, framing); there is no text, letters or pseudo-text painted in the art, no noose, no blood or gore, no anachronism; hands and anatomy are sound; and there is clear, low-detail space (sky, wall, floor, shadow) where each lettering line can sit without covering a face, a hand doing something important or the key action. BALLOONS AND CAPTIONS ARE DRAWN BY THE LETTERER, NOT THE ART: any painted blank balloon or box in a candidate will be covered by a drawn one, so do NOT reject a candidate for painted balloon count, size, order or a missing tail. Reject for a painted balloon only if a painted TAIL sticks out well beyond its balloon toward the wrong character (it would stay visible), or if painted boxes cover faces or the key action. The setting must match the script and the neighbouring panels (a closed hold is never open to the sky; a storm only heard is not shown as rain indoors). Prefer consistency with neighbouring panels on the page (same room, lighting, costume). If nothing is acceptable, set pick to null and write a correction: one precise paragraph to append to the image prompt that fixes the specific failure while keeping what worked.${args.preference ? '\n\n' + args.preference : ''}

PANELS:
${page.panels.map(p => `${p.id} (script ${p.label}); cast: [${p.cast.join(', ')}]; contact sheet: ${p.sheet}; candidates: ${p.versions.join(', ')}; frames: ${p.frames || 'see contact sheet'}; lettering lines (copy_index: speaker): ${p.copy || 'none'}`).join('\n')}

For tail points and faces, Read the chosen frame itself (listed under frames) so the fractions refer to that exact image. Do not edit any file. Return one decision per panel.`,
  {label: `select ch${ch} p${page.page}`, phase: 'Select', schema: DECISION}))

const decisions = results.filter(Boolean).flatMap(r => r.decisions)
const missing = PAGES.flatMap(p => p.panels.map(x => x.id)).filter(id => !decisions.some(d => d.id === id))
log(`chapter ${ch}: ${decisions.filter(d => d.pick).length} picked, ${decisions.filter(d => !d.pick).length} need regeneration, ${missing.length} without a decision`)
return {chapter: ch, decisions, missing}
