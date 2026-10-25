export const meta = {
  name: 'v15-identity-audit',
  description: 'Re-check every accepted panel showing Nagoji or Varma against the 2026-10-08 sheets and bible; a skeptic confirms each redo verdict',
  phases: [
    { title: 'Audit', detail: 'one auditor per chunk of about eight panels' },
    { title: 'Verify', detail: 'one skeptic per chunk re-checks every redo verdict' },
  ],
}

const V15 = '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo'
const DIR = '/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/audit'
const PY = '/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python'
const pad3 = n => String(n).padStart(3, '0')
const RULES = `Read-only task: do not edit, create, move or delete any project file; you may save zoom crops under $TMPDIR with Python and Pillow (${PY}) and Read them. No em dashes or en dashes in your output.`
const STANDARD = `Bible: ${V15}/CONTINUITY.md (read the Nagoji Sawant / Ananthan Pillai section and its row for this chapter and page, and the Marthanda Varma line and its rows). Each panel's own prompt is ${V15}/chapters/<package>/prompts/<panel id>.txt.
A panel needs REDO only for a hard identity fault that a reader would notice at print size:
VARMA (chapters 1 to 27): grey or silver in his hair; bare-headed with a knot on top of the crown, or loose curly shoulder-length hair; or he reads as a double of Nagoji in the same book (heavy bushy moustache plus curly hair and no namam or pearls), so a reader could take one for the other; or he wears Nagoji's rust-red turban or Nagoji's costume. In chapter 28 Varma is the aged dedication figure (grey hair, low knot, plain mundu, sacred thread) and that is correct.
NAGOJI: a hanging drop, bead or ring below the earlobe clearly visible (the rule is one tiny flat flush stud); a beard or clear stubble on the chin outside captivity; the old brand drawn as a symbol, letters, cross, star, wheel or dark tattoo, or on the RIGHT forearm, or on the outer forearm or back of the hand; hair wrong for the chapter row (for example a topknot while the row says rust-red turban or loose curls, or loose hair or a turban while the row says Kerala topknot); grey hair before chapter 16.
ANYONE: an unnamed man drawn as a near double of Nagoji or Varma beside them, so the reader cannot tell which is the principal.
Everything else (a slightly high or back-set side knot, a missing namam on a small distant Varma, a medium moustache, small costume drift) is NOTE, not REDO. When unsure, say NOTE.`

const ITEM = {type: 'object', properties: {
  id: {type: 'string'}, version: {type: 'string'},
  verdict: {type: 'string', enum: ['ok', 'note', 'redo']},
  issues: {type: 'string', description: 'what is wrong, naming the character and where in the frame; empty if ok'},
  mode: {type: 'string', enum: ['edit', 'generate', 'none'], description: 'for redo: edit if a local change fixes it (ear, hair, moustache, brand), generate if the panel must be redrawn; none otherwise'},
  correction: {type: 'string', description: 'for redo: one precise paragraph for the image generator that fixes the fault and keeps everything else; empty otherwise'},
}, required: ['id', 'version', 'verdict', 'issues', 'mode', 'correction']}
const AUDIT = {type: 'object', properties: {items: {type: 'array', items: ITEM}}, required: ['items']}
const VERDICT = {type: 'object', properties: {items: {type: 'array', items: {type: 'object', properties: {
  id: {type: 'string'}, confirmed: {type: 'boolean'}, reason: {type: 'string'},
  correction: {type: 'string', description: 'the correction to use if confirmed (improve the auditor\'s if needed); empty if not confirmed'},
  mode: {type: 'string', enum: ['edit', 'generate', 'none']},
}, required: ['id', 'confirmed', 'reason', 'correction', 'mode']}}}, required: ['items']}

const results = await pipeline(args.chunks,
  ch => agent(`${RULES}
You audit finished comic panels of the graphic novel "Horse of the Servant" (Travancore and Goa, 1738 to 1753) for two principals the image generator keeps confusing: Nagoji and King Marthanda Varma. First Read ${DIR}/chunk-${pad3(ch.n)}.json: chapter ${ch.chapter}, package ${ch.package}, and ${ch.count} panels, each with its frame path, cast and the character sheet(s) that apply to it. Read each sheet once, then Read every frame and zoom into each principal's head, ears, hair and forearms.
${STANDARD}
Return one item per panel in the chunk.`,
    {label: `audit ch${ch.chapter} #${ch.n}`, phase: 'Audit', schema: AUDIT}),
  (a, ch) => {
    if (!a) return null
    const redo = a.items.filter(x => x.verdict === 'redo')
    if (!redo.length) return {chunk: ch, audit: a.items, verify: []}
    return agent(`${RULES}
You are a skeptic. Another reviewer marked these panels for REDO because of an identity fault; try to REFUTE each one, defaulting to "not confirmed" when the fault is doubtful or too small to notice at print size. Chunk file: ${DIR}/chunk-${pad3(ch.n)}.json (frame paths and sheets).
${STANDARD}
Panels marked REDO, with the reviewer's reason:
${redo.map(x => `${x.id} ${x.version}: ${x.issues}`).join('\n')}
For each, Read the frame, zoom, and confirm or refute. For a confirmed one, give the correction paragraph to use (keep everything that is right; fix only the fault) and whether an edit of this frame suffices or the panel must be regenerated.`,
      {label: `verify ch${ch.chapter} #${ch.n}`, phase: 'Verify', schema: VERDICT}).then(v => ({chunk: ch, audit: a.items, verify: v ? v.items : null}))
  })

const done = results.filter(Boolean)
const confirmed = done.flatMap(r => (r.verify || []).filter(v => v.confirmed).map(v => ({chapter: r.chunk.chapter, package: r.chunk.package, ...v})))
log(`audited ${done.reduce((n, r) => n + r.audit.length, 0)} panels in ${done.length} of ${args.chunks.length} chunks; ${confirmed.length} confirmed redo`)
return {confirmed, chunks: done, missingChunks: args.chunks.filter((c, i) => !results[i]).map(c => c.n)}
