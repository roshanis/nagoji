// @exec: {"yield_time_ms": 120000, "max_output_tokens": 1000}
// Run this source in Codex functions.exec, not node. Set chapter for the job.
// This bridge uses the actual built-in tool; Python never substitutes an API.
const chapter = 1;
const py = '/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python';
const entry = '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/run_chapter.py';
const quote = value => "'" + String(value).replaceAll("'", "'\\''") + "'";
const next = await tools.exec_command({cmd: `PYTHONDONTWRITEBYTECODE=1 ${quote(py)} ${quote(entry)} next-job --chapter ${chapter}`, max_output_tokens: 10000});
if (next.exit_code !== 0) throw new Error(next.output);
const job = JSON.parse(next.output);
if (!job) { text('All jobs have captured candidates. Review and select them before build.'); exit(); }
for (const path of job.reference_images) image((await tools.view_image({path})).image_url);
const args = {...job.image_gen.args};
if (!args.referenced_image_paths?.length) delete args.referenced_image_paths;
const result = await tools.image_gen__imagegen(args);
generatedImage(result);
const matches = (result.output_hint || '').match(/as (\/[^\n]+\.png) by default/);
if (!matches) throw new Error('Generation did not return a saved PNG path. Stop; do not substitute another model.');
const saved = await tools.exec_command({cmd: `PYTHONDONTWRITEBYTECODE=1 ${quote(py)} ${quote(entry)} capture --chapter ${chapter} --frame-id ${quote(job.id)} --generated ${quote(matches[1])}`, max_output_tokens: 1500});
if (saved.exit_code !== 0) throw new Error(saved.output);
text(saved.output);
