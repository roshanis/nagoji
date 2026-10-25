# What can be deleted: disk audit, 2026-10-10

The disk had under 1 GB free (926 GB). Seven independent read-only audits each tried to prove its category was NOT safe to delete, hashing files and searching every V15 record for references. Nothing has been deleted. Full evidence: `pipeline/review/DISK-CLEANUP-AUDIT-2026-10-10.json`.

## Safe to delete: about 194 GB, nothing lost

| What | GB | Why it is safe |
|---|---|---|
| `.git/objects/pack/tmp_pack_*` (21 files, 15 to 25 Sept) | 108.3 | Half-written packs from interrupted `git add` runs. Git never reads them. Their contents are copies of old V10 preview PDFs that are still on disk. |
| `output/ltx-local-test-v1`: model weights, runtime, caches | 35.0 | Finished video-model trial. Its notes, QA and renders stay. |
| Superseded V15 builds: old chapter PDFs, page renders, and half-written outputs of failed builds | 39.8 | Every revision except each chapter's final one. All can be rebuilt from the recorded data. |
| Codex's original images (`~/.codex/generated_images`) whose byte-identical copy is a frame in a final package | 5.1 | Duplicates. The copies in the packages are the ones the book uses. |
| 2x upscales inside superseded packages | 1.9 | No final build reads them. |
| `output/arcreel-trial-v1`: installs and frontend build | 1.7 | Clean clone of a public app. The trial produced nothing. |
| Byte-identical duplicate PDFs (inside `output/pdf` and copies elsewhere) | 1.4 | Each has an identical copy that stays. |
| `chapters/ch16-split2` frames (unused package) | 0.3 | Identical copies are in the final `ch16-split3`. |
| Scratch images and temp folders from these sessions | 0.3 | Review crops and leftovers. |

## Your call: about 120 GB of past work

| What | GB | What you would lose |
|---|---|---|
| Git cruft pack `pack-71a0b3c2…` (only via `git gc --prune=now`, never by hand) | 14.2 | Unreachable copies of files still on disk, plus 131 small provenance files (old build-log snapshots, about 2 MB). |
| V14 working set (`comic-v14-chapter-quality-v1`, keeping `complete-book-r2` and the 12 chapter PDFs in Git LFS) | 17.8 | The superseded V14 build folders. |
| V10 workspaces (`comic-v10-user-corrections-v1`, `comic-v10-copyedit-v1`) | 13.5 | Intermediate previews and geometry PDFs. |
| `output/pdf` archive of V7 to V13 reading proofs | 10.6 | Past deliverables. |
| Yesterday's delivered PDFs (now replaced by today's builds) | 8.8 | The 2026-10-09 versions of 19 chapters. |
| Superseded V15 frames (7.0 GB are duplicates of final frames, 2.7 GB rejected attempts that exist only there) | 9.7 | Rejected generations and their history. |
| Codex originals whose only copy is in old projects or superseded packages | 9.2 | Originals of older art. |
| Book 2 (`book2-graphic-full-v1`) | 5.7 | The only copy of the Dutchman's Son comic art: keep unless it is backed up. |
| Other old edition workspaces (v8, v11, v12, lettering) and V13 working files | 6.9 | Superseded workspaces. Each has its deliverable PDF in `output/pdf`. |
| Old Codex worktree `nagoji-comic-codex-worktree` | 3.5 | Three early full-book PDFs and book-1 illustrations that exist nowhere else. |
| 2x upscales of the final packages | 3.8 | The next rebuild would re-upscale them, about a minute per frame. |
| Past video deliverables | 1.3 | Chapter 13 videos and movie review cuts. |

## Keep

- The final build of every chapter (14.9 GB), all V15 records, prompts and decisions, and the frames the final packages use.
- Git history (3.0 GB of reachable packs) and Git LFS (2.7 GB).
- `comic-v13-reference-redesign-v1/concepts/`: the V13 reference sheets that V15 prompts still use.
- `arcreel-trial-v1/native-app/runtime/` holds app login files. Remove them separately if you want, but never share them.

## Why the git leftovers appeared

The repository's `.gitignore` lists only `.DS_Store`, so any whole-tree `git add` sweeps the hundreds of gigabytes in `output/` into git. When such a run is interrupted it leaves a `tmp_pack` behind, and git's automatic cleanup never removes those. Adding `output/` (or at least `*.pdf`, `*.png`, `*.mp4`) to `.git/info/exclude` would stop it. That is a config change, so it is yours to approve.
