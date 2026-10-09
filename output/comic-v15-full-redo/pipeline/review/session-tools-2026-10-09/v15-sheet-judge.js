export const meta = {
  name: 'v15-sheet-judge',
  description: 'Judge new Nagoji and Varma model-sheet candidates (two independent judges per sheet), then test whether the chosen sheets keep the two men apart',
  phases: [
    { title: 'Judge', detail: 'two independent judges score every candidate of each sheet' },
    { title: 'Distinctness', detail: 'one skeptic tries to confuse the chosen Nagoji and Varma sheets' },
  ],
}

const V = '/Users/roshanvenugopal/Documents/github/nagoji/output'
const PY = '/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python'
const RULES = `Read-only task: do not edit, create, move or delete any project file; you may save zoom crops under $TMPDIR with Python and Pillow (${PY}) and Read them. No em dashes or en dashes in your output.`
const BIBLE = `${V}/comic-v15-full-redo/CONTINUITY.md (the Nagoji Sawant / Ananthan Pillai table near the top, and the Marthanda Varma line further down)`

const SCORE = {type: 'object', properties: {
  candidates: {type: 'array', items: {type: 'object', properties: {
    candidate: {type: 'string'},
    identity_fidelity: {type: 'integer', description: '1 to 10: same face as the approved V13 sheet (bone structure, nose, eyes, moustache shape, age)'},
    rule_compliance: {type: 'integer', description: '1 to 10: every rule in the sheet prompt holds in EVERY view'},
    text_quality: {type: 'integer', description: '1 to 10: only the requested labels, spelled exactly, no garbled or extra text'},
    failures: {type: 'array', items: {type: 'string'}, description: 'each concrete failure, naming the view (for example "LEFT PROFILE: gold drop hangs below the lobe")'},
  }, required: ['candidate', 'identity_fidelity', 'rule_compliance', 'text_quality', 'failures']}},
  best: {type: 'string', description: 'candidate id to adopt, or "none" if every candidate has a failure that would mislead the panel generator'},
  why: {type: 'string'},
}, required: ['candidates', 'best', 'why']}

const DISTINCT = {type: 'object', properties: {
  confusable: {type: 'boolean', description: 'true if a reader could take one man for the other in a panel where costume is not decisive'},
  shared_features: {type: 'array', items: {type: 'string'}},
  distinguishing_features: {type: 'array', items: {type: 'string'}, description: 'features that tell them apart at small panel size, strongest first'},
  prompt_lines: {type: 'object', properties: {nagoji: {type: 'string'}, varma: {type: 'string'}},
    required: ['nagoji', 'varma'], description: 'one sentence each, for panel prompts, that states the visible differences'},
  verdict: {type: 'string'},
}, required: ['confusable', 'shared_features', 'distinguishing_features', 'prompt_lines', 'verdict']}

phase('Judge')
const judged = await parallel(args.sheets.flatMap(s => ['identity', 'rules'].map(lens => () => agent(
`${RULES}
You judge candidates for a character model sheet of the graphic novel "Horse of the Servant" (Travancore and Goa, 1738 to 1753). Sheet: ${s.name}.
The prompt the generator was given (its rules are the acceptance test): ${s.prompt}
The approved V13 sheet it was edited from (the identity reference): ${s.source}
Bible: ${BIBLE}
Candidates (Read each image; zoom into every head, ear, hairline, forearm and label):
${s.candidates.map(c => `${c.id}: ${c.path}`).join('\n')}
Your lens is ${lens === 'identity'
  ? 'IDENTITY: compare every face on each candidate with the approved V13 sheet. Is it the same man (bone structure, nose, eyes, moustache shape, apparent age)? Are all the views on one candidate the same man?'
  : 'RULES: check every rule in the prompt in EVERY view: ear ornament (a flush stud for Nagoji, never a hanging drop; pearl drops for Varma), hair (Varma never grey and never curly, knot above the LEFT ear when bare-headed; Nagoji topknot only on the Ananthan Pillai sheet), moustache, clean chin, forearm brand drawn only as a blurred pale scar patch with no symbol, costume, background, and the exact label text.'}
Score every candidate, list concrete failures with the view they are in, and name the candidate to adopt (or "none").`,
  {label: `${lens} ${s.name}`, phase: 'Judge', schema: SCORE}).then(r => r && {sheet: s.name, lens, ...r}))))

const results = judged.filter(Boolean)
const chosen = {}
for (const s of args.sheets) {
  const votes = results.filter(r => r.sheet === s.name)
  const total = {}
  for (const v of votes) for (const c of v.candidates) {
    const fatal = c.failures.length && v.best !== c.candidate ? 1 : 0
    total[c.candidate] = (total[c.candidate] || 0) + c.identity_fidelity + c.rule_compliance + c.text_quality - fatal
  }
  const ranked = Object.entries(total).sort((a, b) => b[1] - a[1])
  chosen[s.name] = {pick: ranked.length ? ranked[0][0] : null, totals: total, judges_best: votes.map(v => v.best)}
  log(`${s.name}: totals ${JSON.stringify(total)}; judges picked ${votes.map(v => v.best).join(', ')}`)
}

phase('Distinctness')
const pathOf = (name) => {
  const s = args.sheets.find(x => x.name === name); const id = chosen[name] && chosen[name].pick
  const c = s && s.candidates.find(x => x.id === id); return c ? c.path : null
}
const distinct = await agent(
`${RULES}
Try hard to CONFUSE these two men; default to "confusable" if you are unsure. Nagoji (a Maratha cavalry commander who later serves Travancore as Ananthan Pillai) and King Marthanda Varma of Travancore appear together in many panels; the image generator has repeatedly drawn Varma as a double of Nagoji (grey temples, crown topknot, the same heavy curled moustache).
Nagoji sheets: ${pathOf('21-nagoji-commander-v15')} and ${pathOf('22-nagoji-ananthan-pillai-v15')}
Varma sheet: ${pathOf('23-marthanda-varma-v15')}
Bible: ${BIBLE}
Compare the heads at the size a face takes in a medium panel (crop each head and shrink it to about 80 pixels tall). Judge them with costume hidden: face shape, nose, moustache, hair texture and how it is worn, ear ornament, forehead mark, build. Say whether a reader could take one man for the other, list the shared and the distinguishing features, and write one sentence for each man that panel prompts should carry so the generator keeps them apart.`,
  {label: 'distinctness skeptic', phase: 'Distinctness', schema: DISTINCT})

return {chosen, judgements: results, distinctness: distinct}
