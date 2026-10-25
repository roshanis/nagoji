export const meta = {
  name: 'v15-chapter-review',
  description: 'Five-lens visual review of a built V15 chapter, with skeptic verification of serious findings',
  phases: [
    { title: 'Review', detail: 'five lenses read every page render' },
    { title: 'Verify', detail: 'a skeptic tries to refute each blocker or major finding' },
  ],
}

const V15 = '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo'
const pad = n => String(n).padStart(2, '0')
const ch = args.chapter
const pages = Array.from({length: args.pages}, (_, i) => `${args.renders}/page-${pad(i + 1)}.png`)
const pageList = pages.map((p, i) => `page ${i + 1}: ${p}`).join('\n')
const COMMON = `You are reviewing Chapter ${ch} of the V15 graphic novel "Horse of the Servant" (Travancore and Goa, 1738 to 1753). Look at EVERY page render below with the Read tool (they are 300 DPI PNGs; zoom by reading crops if you need to: you may use the Bash tool with the Python at /Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python and Pillow to save crops under $TMPDIR, then Read them).
Script: ${V15}/scripts/CHAPTER-${pad(ch)}-SCRIPT.md. Continuity bible: ${V15}/CONTINUITY.md (a character's base line plus the rows for chapter ${ch}; Nagoji's table row for chapter ${ch}). ${args.noCastFile ? 'This chapter has no cast file; take the visible cast from the script.' : 'Visible cast per panel: ' + V15 + '/scripts/CHAPTER-' + pad(ch) + '-CAST-OVERRIDES.json.'} Approved character sheets: ${V15}/concepts/APPROVED-SHEETS.json (files in ${V15}/concepts/), plus Nagoji ${'/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v13-reference-redesign-v1/concepts/nagoji-v2.png'} and Varma .../concepts/varma-v1.png in the same V13 folder.
PAGES:
${pageList}
Do not edit any file. Report only real problems you can point to on a specific page and panel (panel numbers follow the script: page P, panel N from top-left in reading order). Severity: blocker (must be redrawn before publication: wrong identity, forbidden content, wrong or unreadable lettering, missing beat), major (clearly wrong but localized: costume error, anachronism, wrong speaker tail, awkward crop hiding the action), minor (polish). If a page is clean, say nothing about it.`
const LENSES = [
  {key: 'identity', text: 'LENS: character identity. Compare every drawn principal with their approved sheet and the bible base line. Nagoji: thick curled moustache, CLEAN-SHAVEN chin, small gold ear stud, long curly black hair, never a beard. Check each named character is recognisably the same person across panels and matches the sheet; flag look-alikes (for example Keshavrao drawn like Nagoji), wrong age, wrong facial hair, missing scars that the bible requires (Ibrahim LEFT ear to jaw, Raza LEFT cheek).'},
  {key: 'continuity', text: 'LENS: costume and continuity for this chapter. Check every principal against the bible rows for this chapter (chains, rags, turbans, coats, brand on the inner LEFT forearm drawn as ridges and never a cross, injuries, jewellery, tali, horses by colour). Check props and settings stay consistent across panels on the same page.'},
  {key: 'rules', text: 'LENS: standing rules. Flag any letters, words, numerals or pseudo-text painted into the art (outside the lettered balloons and captions), any noose, any blood or gore, anachronisms for 1738 to 1753 (glass lanterns in Kerala settings, modern objects, 19th-century Roman collars), Portuguese guards that read as British redcoats or Dutch blue-coats, lettered flags or banners.'},
  {key: 'lettering', text: 'LENS: lettering and page layout. Every balloon and caption readable and inside its panel, not covering a face or the key action, tails pointing to the correct speaker, reading order clear, no clipped or overlapping text, panel borders and gutters clean, the page reads as a coherent comic page like the approved Chapter 1 (see ' + V15 + '/chapters/ch01/renders/r6/page-01.png for the standard).'},
  {key: 'fidelity', text: 'LENS: fidelity to the script. For each page, check each panel shows the script panel beat (who is present, the action, the framing: wide, close, insert), that panel count and order match the script, and that silent beats stay silent. Flag panels whose art tells a different story from the script or loses a must-keep beat.'},
]
const FIND = {type: 'object', properties: {findings: {type: 'array', items: {type: 'object', properties: {
  page: {type: 'integer'}, panel: {type: 'string'}, severity: {type: 'string', enum: ['blocker', 'major', 'minor']},
  description: {type: 'string'}, evidence: {type: 'string'}}, required: ['page', 'severity', 'description', 'evidence']}}}, required: ['findings']}
const VERDICT = {type: 'object', properties: {refuted: {type: 'boolean'}, severity: {type: 'string', enum: ['blocker', 'major', 'minor', 'none']}, reason: {type: 'string'}}, required: ['refuted', 'severity', 'reason']}

phase('Review')
const byLens = await pipeline(
  LENSES,
  lens => agent(`${COMMON}\n\n${lens.text}`, {label: `review ch${ch} ${lens.key}`, phase: 'Review', schema: FIND})
    .then(r => (r ? r.findings : []).map(f => ({...f, lens: lens.key}))),
  findings => parallel(findings.filter(f => f.severity !== 'minor').map(f => () =>
    agent(`${COMMON}\n\nA reviewer (${f.lens} lens) reported this ${f.severity} problem on page ${f.page}${f.panel ? ', panel ' + f.panel : ''}: "${f.description}" Evidence given: "${f.evidence}". Look at that page closely (crop and zoom) and try to REFUTE it. It is refuted if the art does not show the problem, if the bible or script allows it, or if it is too slight to matter at print size. If uncertain, refute. Otherwise confirm and give the right severity.`,
      {label: `verify ch${ch} p${f.page} ${f.lens}`, phase: 'Verify', schema: VERDICT})
      .then(v => ({...f, verdict: v})))).then(verified => ({verified, minors: findings.filter(f => f.severity === 'minor')}))
)
const all = byLens.filter(Boolean)
const confirmed = all.flatMap(x => x.verified.filter(Boolean)).filter(f => f.verdict && !f.verdict.refuted)
const refuted = all.flatMap(x => x.verified.filter(Boolean)).filter(f => f.verdict && f.verdict.refuted)
const minors = all.flatMap(x => x.minors)
log(`chapter ${ch}: ${confirmed.length} confirmed, ${refuted.length} refuted, ${minors.length} minor`)
return {chapter: ch, confirmed, refuted: refuted.map(f => ({page: f.page, panel: f.panel, lens: f.lens, description: f.description, reason: f.verdict.reason})), minors}
