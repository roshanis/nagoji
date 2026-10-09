export const meta = {
  name: 'v15-identity-verify',
  description: 'Compare each identity-fix candidate with the audited frame: is the identity fault gone, and did nothing else break?',
  phases: [{ title: 'Verify', detail: 'one checker per group of up to six panels' }],
}

const V15 = '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo'
const PY = '/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python'
const RULES = `Read-only task: do not edit, create, move or delete any project file; you may save zoom crops under $TMPDIR with Python and Pillow (${PY}) and Read them. No em dashes or en dashes in your output.`
const STANDARD = `Bible: ${V15}/CONTINUITY.md (the Nagoji Sawant / Ananthan Pillai table and its row for this chapter, and the Marthanda Varma line). Each panel's script is ${V15}/scripts/CHAPTER-NN-SCRIPT.md (panel "**P.N**" blocks).
Hard identity rules. NAGOJI: one tiny flat gold stud flush on the earlobe and nothing hanging below it; clean-shaven chin outside captivity; thick curled moustache; the old brand only as a pale blurred scar patch on the inner LEFT forearm (never a symbol, letters, cross, star or wheel, never on the right arm or back of the hand); hair as the chapter row says; no grey before chapter 16. VARMA (chapters 1 to 27): straight, sleek jet-black hair, never curly, never grey; bare-headed only with one small knot on the left side just above the left ear (never on the crown or at the back); thin waxed upturned moustache; white namam with a red centre line; pearl drop earrings; he must never read as a double of Nagoji. ANYONE: no unnamed man drawn as a near double of a principal.
Also hard faults in any candidate: painted text, letters or pseudo-text; extra, missing or detached limbs or broken hands; blood or gore; a changed face for any other named character; for an EDIT, any change to composition, framing, setting or other figures beyond what the correction asked.`

const ITEM = {type: 'object', properties: {
  id: {type: 'string'},
  fault_fixed: {type: 'boolean', description: 'the audited identity fault is gone in the new candidate'},
  new_faults: {type: 'string', description: 'every hard fault present in the NEW candidate that the old frame did not have, naming where; empty if none'},
  remaining: {type: 'string', description: 'any part of the audited fault still visible in the new candidate; empty if none'},
  verdict: {type: 'string', enum: ['accept_new', 'keep_old', 'retry'], description: 'accept_new: the new candidate is clean of hard faults (or strictly better with only NOTE-level drift). keep_old: the new candidate is worse than the old frame. retry: not fixed or newly broken, and one more targeted correction should fix it'},
  correction: {type: 'string', description: 'for retry: one precise paragraph for an edit of the NEW candidate (or of the old frame if the new one is unusable, and say which) that fixes what remains and keeps everything else; empty otherwise'},
  retry_from: {type: 'string', enum: ['new', 'old', 'none']},
  tails: {type: 'array', description: 'ONLY for a regenerated (mode generate) panel you accept: one entry per SPEECH lettering line (not captions): the speaker mouth as fractions of the NEW frame width and height; for an off-panel speaker the frame-edge point nearest them. Empty for edits.', items: {type: 'object', properties: {copy_index: {type: 'integer'}, x: {type: 'number'}, y: {type: 'number'}}, required: ['copy_index', 'x', 'y']}},
  notes: {type: 'string', description: 'NOTE-level drift worth listing for the author; empty if none'},
}, required: ['id', 'fault_fixed', 'new_faults', 'remaining', 'verdict', 'correction', 'retry_from', 'tails', 'notes']}
const OUT = {type: 'object', properties: {items: {type: 'array', items: ITEM}}, required: ['items']}

phase('Verify')
const results = await pipeline(args.groups, g => agent(`${RULES}
You verify identity fixes in finished panels of the graphic novel "Horse of the Servant" (Travancore and Goa, 1738 to 1753). The image generator kept drawing King Marthanda Varma as a double of Nagoji and giving Nagoji a hanging earring; an audit found the faults and each panel was edited (or regenerated) once. First Read ${g.file}: chapter ${g.chapter}, package ${g.package}, ${g.count} panel(s), each with the audited OLD frame, the NEW candidate, the mode, the confirmed fault, the correction that was sent, the cast, the character sheets and the lettering lines. Read each sheet once. For each panel Read the OLD and the NEW frame and zoom into every principal's head, ears, hair, chin and forearms, and into hands and the area the correction touched.
${STANDARD}
Be a skeptic about the fix: say fault_fixed only if the fault is clearly gone at zoom. Be fair about regressions: list only real hard faults the NEW candidate has that the OLD did not. Choose accept_new when the new candidate is free of hard faults, keep_old when it is worse than the old frame, retry otherwise. Return one item per panel.`,
  {label: `verify ${g.package} #${g.n}`, phase: 'Verify', schema: OUT}).then(r => r && {group: g, items: r.items}))
const done = results.filter(Boolean)
const all = done.flatMap(r => r.items.map(x => ({package: r.group.package, chapter: r.group.chapter, ...x})))
log(`${all.length} panels: ${all.filter(x => x.verdict === 'accept_new').length} accept, ${all.filter(x => x.verdict === 'retry').length} retry, ${all.filter(x => x.verdict === 'keep_old').length} keep old; ${args.groups.length - done.length} groups failed`)
return {items: all, failedGroups: args.groups.filter((g, i) => !results[i]).map(g => g.n)}
