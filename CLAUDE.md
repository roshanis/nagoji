# Assistant Notes

This repository is a book manuscript, not an application codebase. For full writing and editing guidance, read `AGENTS.md`.

## Constraints

- No em dashes.
- Keep chapter files self-contained; do not split or merge them.
- Maintain a clear POV and timeline; avoid anachronistic language.

## Files To Keep In Sync

- `book*_chapter*.md`: primary narrative chapters
- `manuscript_v2.md`: composite draft (chapters plus end matter)
- `synopsys.md`, `novel_outline_bhimrao.md`, `glossary.md`, `Author_Historical_Note_nagoji.md`: support documents that should reflect the current manuscript

## Review Panel (required for every change)

Every proposed change to the manuscript or its support documents goes through the six reviewer agents in `.claude/agents/` before it is presented to the author as ready or applied: `reviewer-user-experience`, `reviewer-graphic-design`, `reviewer-story-editing`, `reviewer-general-editing`, `reviewer-history-research`, then `reviewer-adversarial` last with the other five verdicts. Run the first five in parallel. A change survives only if no reviewer blocks it and every requested revision is applied and re-checked. Record the verdicts under each item in the suggestions file. The panel advises; the author still approves every change. Full protocol: `.claude/REVIEW_PANEL.md`.
