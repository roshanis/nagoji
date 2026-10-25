export const meta = {
  name: 'v15-select-zones-file',
  description: 'Select candidates (one reviewer per page, reading that page from a file) then mark face and keep zones for the picks',
  phases: [{ title: 'Select', detail: 'one reviewer per page' }, { title: 'Zones', detail: 'faces and keep zones for every pick' }],
}
const V15 = '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo'
const S = '/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad'
const pad = n => String(n).padStart(2, '0')
const ch = args.chapter
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


phase('Select')
const results = await pipeline(args.pages, pg => agent(
`You are choosing finished art for page ${pg.page} of Chapter ${ch} of the graphic novel "Horse of the Servant" (Travancore and Goa, 1738 to 1753). First Read ${args.pagesDir}/page-${pad(pg.page)}.txt: it lists the character sheets for this page and the ${pg.panels} panel(s) to decide, each with its script label, cast, contact sheet (every candidate the image generator produced, labelled v01, v02, ...), candidate versions, frame paths and lettering lines. For each panel, Read its contact sheet and pick the best ACCEPTABLE candidate. Zoom with crops if needed (Python with Pillow: /Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python; save crops under $TMPDIR and Read them).

Script: ${V15}/scripts/CHAPTER-${pad(ch)}-SCRIPT.md (panel "**${pg.page}.N**" blocks: art direction plus "> " lettering lines). Continuity bible: ${V15}/CONTINUITY.md (base lines plus the rows for chapter ${ch}; Nagoji's table row for chapter ${ch}). Each panel's own prompt is at ${V15}/chapters/${args.package || 'ch' + pad(ch)}/prompts/<panel id>.txt (LOOKS and MUST MATCH lines say what each principal must show in this chapter).

A candidate is ACCEPTABLE only if: every drawn principal matches their sheet and the chapter's bible row (Nagoji: thick curled moustache, CLEAN-SHAVEN chin, small gold ear stud); the panel shows the script beat (who is present, action, framing); there is no text, letters or pseudo-text painted in the art, no noose, no blood or gore, no anachronism; hands and anatomy are sound; and there is clear, low-detail space (sky, wall, floor, shadow) where each lettering line can sit without covering a face, a hand doing something important or the key action. BALLOONS AND CAPTIONS ARE DRAWN BY THE LETTERER, NOT THE ART: any painted blank balloon or box in a candidate will be covered by a drawn one, so do NOT reject a candidate for painted balloon count, size, order or a missing tail. Reject for a painted balloon only if a painted TAIL sticks out well beyond its balloon toward the wrong character (it would stay visible), or if painted boxes cover faces or the key action. The setting must match the script and the neighbouring panels (a closed hold is never open to the sky; a storm only heard is not shown as rain indoors). Prefer consistency with neighbouring panels on the page (same room, lighting, costume). If nothing is acceptable, set pick to null and write a correction: one precise paragraph to append to the image prompt that fixes the specific failure while keeping what worked.

Only choose among the candidate versions the page file lists for a panel. For tail points and faces, Read the chosen frame itself (listed under frames) so the fractions refer to that exact image. Do not edit any file. Return one decision per listed panel.`,
  {label: `select ch${ch} p${pg.page}`, phase: 'Select', schema: DECISION}))
const decisions = results.filter(Boolean).flatMap(r => r.decisions)
log(`chapter ${ch}: ${decisions.filter(d => d.pick).length} picked, ${decisions.filter(d => !d.pick).length} need regeneration; ${results.filter(r => !r).length} page reviewers failed`)
phase('Zones')
const byPage = {}
for (const d of decisions) {
  if (!d.pick) continue
  const m = d.id.match(/page-(\d+)-panel-(\d+)/)
  if (!m) continue
  ;(byPage[Number(m[1])] = byPage[Number(m[1])] || []).push([m[2], d.pick])
}
const zargs = {chapter: ch, framesRoot: args.framesRoot, pages: Object.entries(byPage).map(([page, frames]) => ({page: Number(page), frames}))}
const [faces, keep] = zargs.pages.length ? await parallel([
  () => workflow({scriptPath: `${S}/v15-faces2.js`}, zargs),
  () => workflow({scriptPath: `${S}/v15-keep.js`}, zargs),
]) : [null, null]
return {selections: [{chapter: ch, decisions, failedPages: args.pages.filter((p, i) => !results[i]).map(p => p.page)}], zones: [{kind: 'faces', chapter: ch, result: faces}, {kind: 'keep', chapter: ch, result: keep}]}
