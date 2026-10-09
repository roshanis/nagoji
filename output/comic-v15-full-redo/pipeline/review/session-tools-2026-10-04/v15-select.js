export const meta = {
  name: 'v15-select',
  description: 'Pick the best existing candidate for every panel of a chapter, or write a precise correction for Codex',
  phases: [{ title: 'Select', detail: 'one reviewer per page reads each panel contact sheet' }],
}

const V15 = '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo'
const pad = n => String(n).padStart(2, '0')
const ch = args.chapter
const PAGES = args.sheetsRoot ? args.pages.map(pg => ({page: pg.page, panels: pg.panels.map(([n, cast, versions]) => {
  const id = `page-${pad(pg.page)}-panel-${n}`
  return {id, label: `${pg.page}.${Number(n)}`, cast, versions, sheet: `${args.sheetsRoot}${id}.png`}
})})) : args.pages
const SHEETS = args.sheets.map(s => `${s.key}: ${s.path}`).join('\n')
const DECISION = {type: 'object', properties: {decisions: {type: 'array', items: {type: 'object', properties: {
  id: {type: 'string'},
  pick: {type: ['string', 'null'], description: 'best acceptable candidate version such as v03, or null if none is acceptable'},
  backup: {type: ['string', 'null'], description: 'second acceptable version, or null'},
  issues: {type: 'string', description: 'what is wrong with the pick or with all candidates; empty if the pick is clean'},
  correction: {type: 'string', description: 'if pick is null: one precise paragraph to append to the image prompt so the next generation fixes the problem; else empty'},
}, required: ['id', 'pick', 'backup', 'issues', 'correction']}}}, required: ['decisions']}

const results = await pipeline(PAGES, page => agent(
`You are choosing finished art for page ${page.page} of Chapter ${ch} of the graphic novel "Horse of the Servant" (Travancore and Goa, 1738 to 1753). For each panel below, Read its contact sheet (every candidate the image generator produced, labelled v01, v02, ...) and pick the best ACCEPTABLE candidate. Zoom with crops if needed (Python with Pillow: /Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python; save crops under $TMPDIR and Read them).

Script: ${V15}/scripts/CHAPTER-${pad(ch)}-SCRIPT.md (panel "**${page.page}.N**" blocks: art direction plus "> " lettering lines). Continuity bible: ${V15}/CONTINUITY.md (base lines plus the rows for chapter ${ch}; Nagoji's table row for chapter ${ch}). Character sheets (Read the ones for each panel's cast):
${SHEETS}

A candidate is ACCEPTABLE only if: every drawn principal matches their sheet and the chapter's bible row (Nagoji: thick curled moustache, CLEAN-SHAVEN chin, small gold ear stud); the panel shows the script beat (who is present, action, framing); there is no text, letters or pseudo-text painted in the art, no noose, no blood or gore, no anachronism; hands and anatomy are sound; and it has the right number of BLANK outlined text areas (balloons or caption boxes, one per lettering line of that panel) placed clear of faces and the key action; the blank areas run in the script's reading order (top to bottom, then left to right) and every speech balloon's tail points visibly to the mouth of the character who speaks that line (captions have no tail); the setting matches the script and the neighbouring panels (for example a closed hold is never open to the sky; a storm only heard is not shown as rain indoors). Prefer consistency with neighbouring panels on the page (same room, lighting, costume). If nothing is acceptable, set pick to null and write a correction: one precise paragraph to append to the image prompt that fixes the specific failure while keeping what worked.

PANELS:
${page.panels.map(p => `${p.id} (script ${p.label}); cast: [${p.cast.join(', ')}]; contact sheet: ${p.sheet}; candidates: ${p.versions.join(', ')}`).join('\n')}

Do not edit any file. Return one decision per panel.`,
  {label: `select ch${ch} p${page.page}`, phase: 'Select', schema: DECISION}))

const decisions = results.filter(Boolean).flatMap(r => r.decisions)
const missing = PAGES.flatMap(p => p.panels.map(x => x.id)).filter(id => !decisions.some(d => d.id === id))
log(`chapter ${ch}: ${decisions.filter(d => d.pick).length} picked, ${decisions.filter(d => !d.pick).length} need regeneration, ${missing.length} without a decision`)
return {chapter: ch, decisions, missing}
