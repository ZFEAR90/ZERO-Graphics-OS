# Main roll — Beta 2.7.8 recovery

Recovery branch: `ze-os-v07-beta278-recovery`.
Starting commit: `e1e4830ef214a93a6c823b18543349791b4f9f3f` (published Beta 2.7.7).
Date: October 29, 2026.

This work reconstructs the supplied continuation handoff. No files from the failed environment were available. The starting checkout was clean; it contained neither the confirmed Phase 1/2 changes nor `zeUniversalWorkspace()`. Phase 3 was implemented here, not assumed recovered. The approved Mouwajaha V0.7 assets, reference motion and compatibility HTML filename are retained. No V0.8/V0.9/Atlas material was used. Main was not modified; nothing was pushed or published.

## Implemented continuation

- Beta 2.7.8 editor and importer health version.
- Auto bullet grouping keeps short paragraphs together even with blank lines; explicit blank-line grouping remains available. Pagination measures the actual safe text box, font and line height. Manual timing matches survive compatible edits and regrouping. Each paragraph's final line remains naturally aligned. The final page persists through the endpoint.
- Moving post text into the roll preserves the independent bulletin. The latest owner correction makes choosing Whole automatically turn the external bulletin off without erasing its text; returning to Main restores the prior visibility. Ordinary post-text placement remains independent of bulletin visibility. Text-only/media-hidden choices retain media geometry metadata.
- Post Arabic uses the existing joining-safe kashida renderer without modifying editable source text. Space justification and natural alignment are alternatives. Right-only characters and lam–alef ligatures are excluded from insertion slots.
- Main keeps the approved reference frame and automatic portrait-right / wide-below arrangement. Whole defaults to shared text/media motion, with pinned native account and an enlarged external platform tile. Fixed/speaker-safe media remains selectable. Both presentations honor the manual scroll selection.
- Sequence is the multiple-media default; optional grid remains in Advanced. A configurable eased directional reveal covers the outgoing picture without antialiasing gaps. Flip reverses the reveal without reflecting media. Framing uses the first selected item and stays stable during the sequence. The final item holds.
- Playback uses slot-local time, pre-seeks the next video, pauses inactive clips, crossfades clip gain during overlaps, and retains Hold/Loop plus decoded-frame fallback. Hidden-video audio requires an explicit switch; disabled items remain excluded.
- Header anchoring uses painted component bounds, keeping the 24 scene-unit bulletin gap and TV/Live clearance. Native account scaling is bounded by its frame. Bulletin text always respects the breaking-news boundary, including with roll protection off.
- `zeUniversalWorkspace()` removes the permanent right sidebar, moves export and primary colors into Main, collapses reference/metadata and detailed timing under Advanced, adds Render Video next to the preview, fits its height, and puts preview before controls on narrow screens. Undo/Redo and keyboard movement history remain available.

## Validation and reproduction

Run from this checkout with `.venv/bin/python`. The local importer starts with `BROWSER=true .venv/bin/python ze_local_importer.py` (port 8765 unless `ZE_OS_PORT` overrides it). Its `/api/health` response identifies `ze-os-importer`, version `0.7-beta2.7.8`. Each cloud task is isolated; use the existing checkout and do not create a worktree unless requested.

Core checks:

```sh
.venv/bin/python -m unittest discover -s tests -p test_importer.py
.venv/bin/python tests/browser_recovery_check.py
.venv/bin/python tests/browser_native_account_check.py
.venv/bin/python tests/browser_motion_check.py
.venv/bin/python tests/browser_paragraph_check.py
```

Additional focused checks cover reference dimensions, clean media, media toggles, painted header anchors, post routing, shared below-text movement, handoff, palette and editing. Older assertions were deliberately updated for retained bulletin text, actual painted header bounds, shared Whole movement, enabled manual overrides and the new control locations. Pixel, mask, source orientation and timing assertions remain.

The source-width reference metric remains 0.142857 proxy pixels mean error; 151-frame entrance/safe-band checks use the repository's existing embedded proxy. This is not a full-scene or full-resolution fidelity claim.

Generate the walkthrough and actual 50-second browser output with:

```sh
PLAYWRIGHT_BROWSERS_PATH=/workspace/.cache/ms-playwright \
  .venv/bin/python tests/create_beta278_demo.py
```

Playwright recording reuses system FFmpeg via the workspace helper path. Generated demonstration fixtures are explicitly identified; no live platform extraction is claimed. The demonstration includes import, both presentations, portrait/square/wide media, Fill/Fit, text placement, bullet visibility, Flip, actual drag/undo/redo, masks, paragraph transitions, safe-area switching, automatic/manual palette changes, and the full browser recording.

Artifacts:

- `demo/ZE_OS_V07_Beta278_Demo.mp4`: editor walkthrough (screen capture; silent).
- `demo/ZE_OS_V07_Beta278_50s.webm`: actual opaque browser output, 1920×1080 VP9/Opus, 50.000 seconds.
- `demo/ZE_OS_V07_Beta278_Main.png` and `demo/ZE_OS_V07_Beta278_Whole.png`.
- `demo/ZE_OS_V07_Beta278_Walkthrough.webm`: original UI screen recording.

All 16 importer tests and 15 focused browser suites passed; inline JavaScript passed Node syntax checking. The WebM was decoded and checked for full-black intervals and audible audio. `demo/ZE_OS_V07_Beta278_Validation.json` records the evidence. Browser recording is real time and may drop frames; it is not deterministic 25-fps broadcast rendering. Transparent PNG is real alpha. Browser WebM remains disabled in transparent mode. Native MOV/ProRes 4444 and native After Effects export remain deferred.

## Recovery and reference limits

The failed task's uncommitted files, `X Roll ArmedForcesJO.mp4`, a full original broadcast render and additional approved screenshot references were not available here. If supplied later, compare and preserve any recovered work before further changes. The included proxy and written direction support current testing, not a claim of matching unavailable reference footage. Live social access still depends on the platform and environment network settings; manual file import remains available.

The onboarding draft stores tested install/start instructions; saving it does not publish the environment. Review environment settings separately before publishing a snapshot. No credentials are required for the local workflow.

## Final owner-adjustment audit

The owner subsequently supplied the final pre-failure requests, retained verbatim in `FINAL_ADJUSTMENTS.md`. Most behavior was present in recovery commit `47fd3f7`; this follow-up closes the remaining gaps:

- Composition offsets and the media-overlap override now live in Advanced. Per-item face/framing, Hold/Loop and speaker controls also live there; Main keeps per-item inclusion and an **Advanced media controls** shortcut. Palette strength is an Advanced detail. Export, Render Video, primary timing/colors and Undo/Redo remain accessible.
- The speaker checkbox refreshes on presentation changes. Disabling it restores shared movement in Main/Whole structured layouts. Clicking the already active presentation preserves its manual choices.
- Roll text and bullet text share the stricter breaking-news/current-guide boundary. Text-only content remains protected with regular guides selected and roll protection off.
- Hidden-text/media-only content uses the clean centered renderer even in retained Advanced layout treatments; it does not acquire duplicate blur.

Run `.venv/bin/python tests/browser_final_adjustments_check.py` for the final acceptance matrix. It checks Main/Advanced placement through actual controls, speaker on/off, ten hidden-media layout/flip combinations, sixteen Text-only geometry combinations, painted text safety in Main/Whole and both flips, and the 24-unit painted header gap. Browser evidence is in `demo/final-adjustments/`. The existing recovery, header-anchor, social-layout, whole-below, clean-media, native-account, media-toggle, palette and motion checks were also rerun. JavaScript syntax and all 16 importer tests passed. The demonstration and real 50-second browser output were refreshed for this interface.

This audit still uses generated fixture media and the available V0.7 proxy. No recovered failed-task files or unavailable external references are implied. Changes remain on the recovery branch; no remote or environment publication was performed.


## Connected importer and latest owner requests

The quick test launcher previously opened the offline HTML only, which explains the reported “Local importer is not reachable” message. `TEST_MAIN_ROLL.bat` now runs `START_ZE_OS.bat` and opens the connected local editor. `OFFLINE_MAIN_ROLL.bat` is the explicit manual-media alternative. Setup writes `STARTUP_LOG.txt`; Python 3.10+ and dependencies are checked before starting. Screenshot-browser installation is a separate optional action, so a large browser download no longer delays the metadata importer. An identical running helper can reopen its editor; another/older server produces a clear port-conflict diagnostic.

Choosing Whole now automatically hides the external bullet and retains its contents. Main restores the prior visibility. The larger/resized frame reflows post text and media; long post bodies roll inside the mask with the account pinned. Safe geometry leaves space for upward movement where applicable.

The uploaded `TESTING_REQUIREMENTS.md` adds dedicated executable checks, a complete regression runner, and portable project-settings round trips. Project JSON now includes explicit sequence slots and editor settings; Load project JSON restores grouping, justification, sequence choices, layout, colors, duration and manual paragraph holds. Original media bytes remain local and must be reattached on another computer; their settings remain in the project while absent.

All test files were inspected before adding the focused checks. See `tests/README.md` for coverage mapping and deliberate legacy expectation updates. The Windows archive builder verifies every packaged source file and excludes environments/logs.

The owner's linked X post is `https://x.com/AB4_Ali3/status/2115886714602631173`. Its live content could not be verified from this cloud instance: the proxy rejected the X endpoint with CONNECT HTTP 403. Required X hosts were saved in the environment-settings draft; saving that draft is separate from applying it. Local importer/API/fixture tests do not establish live platform access. No credentials were requested or bypassed.


Final automated verification for the connected-importer update: **20 unit tests and all 39 browser check files passed**. Failed: 0; skipped: 0; unrun automated checks: 0. The extracted Windows ZIP was separately smoke-tested with its own packaged helper and a controlled local URL response. The actual refreshed WebM is 50.000 seconds, has audible Opus audio and no detected full-black interval. The updated demonstration includes real playback of the long Whole post and a resize/reflow example. Reports and logs are in `demo/validation/Beta278/`; no Beta 2.7.7 artifacts were overwritten. Native Windows batch execution remains unrun, and the requested live X URL remains blocked by the cloud proxy.


Automatic Whole bulletin hiding also retains the last visible bullet capacity. This keeps grouping and manual holds stable while the panel is hidden, including export/load on a fresh page; the persistence and round-trip tests cover that case. The complete release suite was rerun after this fix and passed all 20 unit tests and 39 browser files. The ZIP, preview evidence and demonstration were then rebuilt from that exact source.

## October 30 owner testing continuation

Main media imports now default to post text in the external bullet and centered media only in the roll, with Fit rather than Fill. Whole retains the complete-post treatment; including text in Main defaults to shared movement. Optional fixed media and Fill remain. Post import is expanded. Pagination prioritizes whole paragraphs, numbered points and sentences, with clause/word fallback for oversized content; a numbered marker stays with its text. Long numbered lists infer a pinned introductory heading on a colored strap, with editable title and normal-bullet reset. This uses structural/language boundaries, not a full semantic AI model.

The panel follows loop colors more visibly, including neutral images. Manual Panel edits lock the color across loop changes; unlocking resumes automatic matching. Temporary right/bottom/corner mouse handles resize roll/bullet dimensions independently; contents reflow/scale/refit, headers remain grouped, safe text capacity is retained, and Undo/Redo/reset/Project JSON preserve dimensions. The testing switch hides the handles.

Final automated validation: 20 unit cases and 41 browser files passed, zero failures/skips/unrun. New owner and pointer-resize checks cover geometry, title pixels, sentence/list boundaries, default uncropped media, normal/flipped layouts, palette, Undo and project round trips. Existing optional fixed-media and Fill coverage remains. The real URL API test now includes a photo and verifies new Main defaults; the extracted Windows ZIP also passes its packaged helper/editor test with controlled post metadata. Live platform access remains separate; native Windows batch execution remains unrun in this Linux executor. Results/logs: `demo/validation/Beta278-Oct30/`.
