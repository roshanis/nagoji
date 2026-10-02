# Chapter 1 r7 production handoff

24 redraws and 17 exact r6 reused selections are complete. All new selected frames were reviewed at native resolution; critical identities, cast, restraints and setting also passed independent review. Failed candidates and exact prompts are retained. Every selected image is inside this package.

Full preflight passes all 41 frames, 49 reserves and 58 script chunks. Page 6 rows are full-width 369pt with uniform 2pt gaps. The additive review/SELECTION-INPUT-r7.json tightens the 6.1 viewport to remove white canvas without overwriting its earlier selection file. All other final selection geometry comes from selections/.

The r7 build is running, with results to be saved to review/BUILD-COMMAND-r7.json. PDF creation has begun; final acceptance is pending command completion, verify, personal inspection of all nine 300 DPI renders, final REVIEW.md and one append-only root build-log entry. No build-log append has been made by this task yet.

All 336 baseline protected file hashes match. Old ch01, prepared prompts, scripts, bible and approved sheet files remain unchanged. Shared compositor is concurrently maintained by another task and is read-only here.

Remaining work: collect successful build output, run verify with explicit ch01-v2 package and r7, inspect all nine renders, record PDF hash/PPI/fonts/text counts, write issue-by-issue REVIEW.md and final integrity/rejection records, append one build-log entry, report paths and all required figures. Never overwrite or delete. Never prepare again.
