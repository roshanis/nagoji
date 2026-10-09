export const meta = {
  name: 'v15-tail-identity-review',
  description: 'Check every speech tail lands on the named speaker, and Nagoji and Varma read as different men, from tail check sheets',
  phases: [{ title: 'Review', detail: 'one reader per chapter group reads every tail check sheet' }],
}
const V15 = '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo'
const SH = `${V15}/pipeline/review/tail-sheets-2026-10-09`
const pad = n => String(n).padStart(2, '0')
const GROUPS = args.groups
const FIND = {type: 'object', properties: {
  checked: {type: 'array', items: {type: 'object', properties: {chapter: {type: 'integer'}, balloons: {type: 'integer'}}, required: ['chapter', 'balloons']}},
  problems: {type: 'array', items: {type: 'object', properties: {
    chapter: {type: 'integer'}, panel: {type: 'string', description: 'as printed on the tile, e.g. p02.05'}, balloon: {type: 'integer'},
    kind: {type: 'string', enum: ['tail_to_wrong_person', 'tail_to_nothing', 'visible_speaker_but_tail_to_edge', 'speaker_drawn_as_someone_else', 'nagoji_varma_lookalike', 'other']},
    description: {type: 'string'}, who_the_tail_points_at: {type: 'string'}, where_the_speaker_is: {type: 'string'},
    confidence: {type: 'string', enum: ['high', 'medium']}},
    required: ['chapter', 'panel', 'kind', 'description', 'confidence']}}},
  required: ['checked', 'problems']}
const ruleText = `You are checking the lettering of the V15 graphic novel "Horse of the Servant" (Kerala and Goa, 1738 to 1753). Do not edit any file.
First read these three approved character sheets with the Read tool, so you know the two men who must never be confused:
- Nagoji as commander (ch5 to ch17 page 10): ${V15}/concepts/21-nagoji-commander-v15.png . A THICK curled moustache, long CURLY black hair, a small gold ear stud, clean-shaven chin; rust-red turban, cream tunic, broad red sash.
- Nagoji as Ananthan Pillai (from ch17 page 11): ${V15}/concepts/22-nagoji-ananthan-pillai-v15.png . Same face; Kerala topknot high on the crown, no turban, cream mundu and shoulder cloth.
- Marthanda Varma, the king (every chapter): ${V15}/concepts/23-marthanda-varma-v15.png . A THIN neatly waxed moustache with sharp upturned points, straight SLEEK hair (never curly), the white namam with a red centre line on his forehead, a pearl drop from each earlobe; a cream-and-gold turban with a jewelled peacock-feather crest at court, or bare-headed with a small knot of hair on the left side of his head; often bare-chested with gold necklaces.
Then read EVERY tail check sheet listed below (each is a PNG of up to six tiles). Each tile is one comic panel cut from the finished page. Above it: the panel id (p02.05 = page 2, panel 5), the visible cast from the cast file, and one numbered, coloured line per speech balloon ("2. PADMINI: ..."). On the art: a coloured numbered badge just left of each balloon, and a ring of the same colour and number at that balloon's tail point (where its tail aims: the speaker's mouth). A tailless box (voice-over or memory) has no ring and is correct.
For every balloon decide whether the ring and the drawn tail land on the speaker the line names. Report a problem only when you can see it:
- tail_to_wrong_person: the ring sits on a different person than the named speaker (for example the line is VARMA's but the ring is on Nagoji).
- tail_to_nothing: the ring sits on scenery, a body part far from any head, or empty space, while the speaker is visible.
- visible_speaker_but_tail_to_edge: the ring is on the panel edge (an off-panel speaker) though the named speaker is clearly visible in the panel.
- speaker_drawn_as_someone_else: the person the ring correctly marks does not look like the named speaker (above all: VARMA drawn with Nagoji's thick curly moustache, curly hair or red turban and sash, or NAGOJI drawn as the king).
- nagoji_varma_lookalike: a panel showing both men where they read as the same face or costume.
Group or unnamed speakers (CROWD, GUARD, SOLDIER, HEADMAN, a voice): the ring on any plausible member of that group, or on the edge when none is visible, is fine. A ring on the right person but at the chin, cheek or forehead is fine. If two balloons by one speaker share one ring, that is fine. If you are not sure, do not report it. Use medium confidence when the art is ambiguous.
Count the balloons you checked per chapter (the numbered lines under the tiles) and return them in "checked".`
phase('Review')
const results = await parallel(GROUPS.map(g => () => {
  const list = g.chapters.map(c => `Chapter ${c.ch}: ${c.sheets.map(n => `${SH}/ch${pad(c.ch)}-tails-${pad(n)}.png`).join(', ')}`).join('\n')
  return agent(`${ruleText}\n\nSHEETS TO READ (every one):\n${list}`, {label: `tails ch${g.chapters.map(c => c.ch).join('+')}`, phase: 'Review', schema: FIND})
}))
return results
