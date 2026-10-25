export const meta = {
  name: 'v15-keep',
  description: 'Mark the key-action region the crop must keep in each chosen frame, and whether the scripted beat is in the frame at all',
  phases: [{ title: 'Keep', detail: 'one reader per page marks action regions against the script beat' }],
}
const KEEP = {type: 'object', properties: {panels: {type: 'array', items: {type: 'object', properties: {
  id: {type: 'string'}, version: {type: 'string'},
  keep: {type: 'array', items: {type: 'object', properties: {
    x0: {type: 'number'}, y0: {type: 'number'}, x1: {type: 'number'}, y1: {type: 'number'}, what: {type: 'string'}},
    required: ['x0', 'y0', 'x1', 'y1', 'what']}},
  beat_present: {type: 'boolean'},
  missing: {type: 'string'},
}, required: ['id', 'version', 'keep', 'beat_present', 'missing']}}}, required: ['panels']}
const pad = n => String(n).padStart(2, '0')
const V15 = '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo'
const SCRIPT = `${V15}/scripts/CHAPTER-${pad(args.chapter)}-SCRIPT.md`
const PAGES = args.pages.map(pg => ({page: pg.page, frames: pg.frames.map(([n, v]) => ({
  id: `page-${pad(pg.page)}-panel-${n}`, label: `${pg.page}.${Number(n)}`, version: v,
  path: `${args.framesRoot}page-${pad(pg.page)}-panel-${n}-${v}.png`}))}))
const results = await pipeline(PAGES, page => agent(
`These are the chosen full, uncropped frames for page ${page.page} of chapter ${args.chapter} of a graphic novel. When a frame is printed, the layout crops it toward its panel's shape, keeping only the regions it is told to keep, so anything the panel's story needs must be marked or it may be cut away.

Read the script: ${SCRIPT} (the "## PAGE ${page.page}" section; panel N.M is the frame page-..-panel-0M). For EACH frame, read the frame with the Read tool (you may crop and zoom with Python and Pillow: /Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python, crops under $TMPDIR) and:
1. keep: the region(s) that must stay visible for the panel's scripted beat to read: the key action (hands gripping, a prop being handled, a blow, a fall, a brand the script says is seen, a named object the script plants), plus any story-critical object or figure the script names for this panel. Give each as a tight rectangle in fractions of the frame width (x0, x1) and height (y0, y1), with a short "what". Do NOT mark faces for their own sake (faces are handled separately), and do not mark scenery that is merely nice; mark only what the beat needs. A panel whose beat is just a face or a wide establishing view may have an empty list. Keep the total small: a crop may keep as little as 45 percent of the frame's height or width, and every region you mark forces more of the frame to stay.
2. beat_present: true if the scripted beat (the action, the named prop or mark, the figures the script requires) is actually drawn somewhere in this full frame; false if it is missing from the art itself (then no crop can save it and the frame must be redrawn).
3. missing: when beat_present is false, say exactly what the script needs that the art lacks (one or two sentences); otherwise an empty string.
Report every frame, in order. Do not edit any file.

FRAMES:
${page.frames.map(f => `${f.label} (${f.id} ${f.version}): ${f.path}`).join('\n')}`,
  {label: `keep ch${args.chapter} p${page.page}`, phase: 'Keep', schema: KEEP}))
const panels = results.filter(Boolean).flatMap(r => r.panels)
const absent = panels.filter(p => !p.beat_present).map(p => p.id)
log(`chapter ${args.chapter}: keep regions for ${panels.length} frames; beat missing from the art in ${absent.length}: ${absent.join(', ')}`)
return {chapter: args.chapter, panels}
