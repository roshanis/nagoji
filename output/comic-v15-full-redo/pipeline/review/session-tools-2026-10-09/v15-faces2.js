export const meta = {
  name: 'v15-faces2',
  description: 'Mark every face as a zone over its features (brows to chin), check each zone on an overlay, for balloon placement',
  phases: [{ title: 'Mark', detail: 'one reader per page marks face zones and checks them on an overlay' },
           { title: 'Check', detail: 'a second reader redraws the overlay and corrects misses and misplaced zones' }],
}
const FACES = {type: 'object', properties: {panels: {type: 'array', items: {type: 'object', properties: {
  id: {type: 'string'}, version: {type: 'string'},
  faces: {type: 'array', items: {type: 'object', properties: {x: {type: 'number'}, y: {type: 'number'}, r: {type: 'number'}, who: {type: 'string'}},
    required: ['x', 'y', 'r', 'who']}},
}, required: ['id', 'version', 'faces']}}}, required: ['panels']}
const pad = n => String(n).padStart(2, '0')
const PY = '/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python'
const SPEC = `A FACE ZONE is a circle that covers one person's facial features so that no speech balloon or caption is ever placed over them. Its centre (x, y) is the middle of the features (roughly the bridge of the nose, between the eyes and the mouth), NOT the centre of the head: for a face in profile or three-quarter view, put it on the face, not over the hair or the back of the skull. Its radius r reaches from that centre to the brow line above and to the bottom of the chin below (include a moustache and beard), and not much further: it should not swallow the whole head of hair. x is a fraction of the frame WIDTH, y and r are fractions of the frame HEIGHT. Mark EVERY readable face, including background figures and faces cut by the frame edge, but skip faces whose features span less than about 2 percent of the frame height. A figure seen from behind with no face showing gets no zone. Give each a short "who" (for example "Nagoji, profile, centre", "grey-bearded fisherman at left").`
const OVERLAY = (path, label) => `To check, draw the circles onto a copy with Pillow and look at it: ${PY} -c "from PIL import Image,ImageDraw;import json,sys;im=Image.open('${path}').convert('RGB');W,H=im.size;d=ImageDraw.Draw(im);[d.ellipse([(f['x'])*W-f['r']*H,f['y']*H-f['r']*H,f['x']*W+f['r']*H,f['y']*H+f['r']*H],outline=(255,0,0),width=max(3,H//200)) for f in json.loads(sys.argv[1])];im.save(sys.argv[2])" '<faces json>' $TMPDIR/${label}.png then Read that PNG. Every circle must sit on a face's features (brows to chin) and every readable face must have one.`
const PAGES = args.pages.map(pg => ({page: pg.page, frames: pg.frames.map(([n, v]) => ({
  id: `page-${pad(pg.page)}-panel-${n}`, version: v, path: `${args.framesRoot}page-${pad(pg.page)}-panel-${n}-${v}.png`}))}))
const results = await pipeline(PAGES,
  page => agent(`${SPEC}

Mark the face zones in each frame below (read each with the Read tool; crop and zoom with Pillow under $TMPDIR as needed). ${OVERLAY('<frame path>', 'faces-<id>')} Adjust until right. Report every frame, even one with no faces (empty list). Do not edit any file in the project.

FRAMES:
${page.frames.map(f => `${f.id} ${f.version}: ${f.path}`).join('\n')}`, {label: `mark ch${args.chapter} p${page.page}`, phase: 'Mark', schema: FACES}),
  (marked, page) => marked ? agent(`${SPEC}

Another reader marked these face zones. For each frame, draw them on a copy and look closely (${OVERLAY('<frame path>', 'check-<id>')}). Correct any circle that sits on hair or the back of the head instead of the features, any radius that is far too large or too small, and add any readable face that was missed; remove zones on figures whose face does not show. Return the corrected list for every frame. Do not edit any file in the project.

MARKED:
${JSON.stringify(marked.panels)}
FRAMES:
${page.frames.map(f => `${f.id} ${f.version}: ${f.path}`).join('\n')}`, {label: `check ch${args.chapter} p${page.page}`, phase: 'Check', schema: FACES}) : null)
const panels = results.filter(Boolean).flatMap(r => r.panels)
log(`chapter ${args.chapter}: face zones for ${panels.length} frames, ${panels.reduce((n, p) => n + p.faces.length, 0)} faces`)
return {chapter: args.chapter, panels}
