# Keep tolerance handoff

Scope: only this pipeline worktree. No git commands, commits, source deletions, placement changes or Codex configuration edits. The only authorized main-tree change is one final agents-build-log.md append.

Changed source files: run_chapter.py, test_run_chapter.py, README.md. Backups and original file hashes are in this audit directory. Ten tests were added before implementation. The final red run is tests-red-r2.txt. All ten pass in tests-green.txt.

Implemented clipped keep coverage, opt-in keep_max through drawn_fits, SlotProbe, probe_fit, structure_fit and _structure_page, scoped and bounded --keep-max CLI, optional fitted_from and report metadata, and auto-geometry --draw audit fractions. No placement changes.

Luna reviewer approved both the plan and implementation. Default ratio, probe and structures outputs match the pre-change baseline after normalizing temporary fixture paths; see default-before.json, default-after.json and verification.json. Added text has no en dash, em dash or trailing whitespace. Python parses. No configured lint or security command was found in the pipeline.

Full six-module suite is running through the permitted executor, session 32268, logging to full-suite.txt. The session prohibits sandbox escalation, so this cannot be called an outside-sandbox run, though real spawned workers passed the focused tests. Await the full result. Then prepare and append the single requested main-tree build-log entry if the normal executor permits it; otherwise retain the exact entry here and report the write restriction. Do not use another tool to bypass filesystem restrictions.
