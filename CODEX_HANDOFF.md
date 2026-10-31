# Latest owner post-review instructions (October 31, 2026)

The owner authorized the accumulated screenshot-reported corrections, then clarified that Main defaults to the entire editable post as though captured from the source: profile/name row, original text, then media aligned to the post width. Main retains Media only / Text only plus independent profile-picture and account-name toggles. These new account toggles DO NOT control Whole frame. The external bulletin stays independent.

Current changes also protect all post text below the decorative strap/account viewport, use proportional full-width media below text, and scroll only the document overflow. Whole retains stationary right media and shared below-text document motion, with its external platform tile enlarged from 66 to 76 base units. Preserve the original V0.7 entrance, Flip orientation and manual controls.

Profile extraction handles Telegram's nested CSS avatar and identity-scoped avatar nodes on other platforms. Missing profiles get Unicode account initials. X/Facebook/Instagram/Telegram/Threads logos are bundled from Simple Icons 16.36.0, with brand-source references and integrity information in assets/vendor-sources.json. Threads recognizes both threads.net and threads.com.

Screenshot import appears below URL import. It uses the bundled Tesseract.js 7.0.0 plus matching core 7.0.0 and English/Arabic models, locally in the browser. Review/correct the detected platform/name/handle/text and profile/media crop outlines before applying. This is best-effort recognition and crop proposal, not guaranteed semantic reconstruction of any screenshot. Video/audio cannot be recovered. Automatic reading needs the HTTP editor opened by START_ZE_OS.bat; file:// mode supports manual review/cropping. Never upload screenshots to an external recognition service.

New acceptance checks: tests/browser_owner_post_review_check.py (actual painted strap clearance, Main-only independent account controls, natural media overflow, bundled logos and initials), tests/browser_screenshot_import_check.py (real offline Arabic/English recognition, crop review and import), and tests/test_offline_assets.py. The full runner is tests/run_regression.py. Windows ZIP builder includes all assets and licenses. Source remains on ze-os-v07-beta278-recovery; main must remain untouched. Earlier sections below are historical.

# Latest owner continuation from c4b0bbd

The owner explicitly authorized the pending corrections after checking GitHub. The remote recovery branch was verified at `c4b0bbd74ce02c42aad2577e61c0bcf20729c76d` before editing. Work stays on `ze-os-v07-beta278-recovery`; main is untouched.

Implemented: visible **Show post text inside the roll** toggle; independent external bulletin retained on import, toggle and post edits; explicit one-time copy remains available. Main, Adaptive, Whole and Dedicated 9:16 are retained; Balanced/Beside are removed from selection and old projects migrate them to Adaptive. All retained structured renderers use disjoint bounded text/media allocations with Fit/Fill and manual framing. Whole right-side media is stationary; below-text media shares document travel without the old recentering endpoint. Existing right/below selection survives entering Whole. Arrangement determines Whole motion, so conflicting speaker/scroll controls are disabled there.

Telegram metadata and Chromium capture both use the public embed widget. The full original body (including line breaks) is extracted; profile imagery is excluded from actual post attachments, including large avatars and nested profile image elements. Original post text is inside the roll; editorial bullets stay independent. The real example `https://t.me/alichoeib1970/19404` is blocked by this cloud proxy (CONNECT 403); live retrieval is unverified. Controlled metadata and actual Chromium widget fixtures exercise both paths.

Install development/test dependencies with `.venv/bin/python -m pip install -r requirements-dev.txt`. The standalone regression runner remains `tests/run_regression.py`. `browser_pending_adjustments_check.py` adds 384 layout/flip/shape/size/Fit-Fill/toggle cases and representative entrance captures. `browser_telegram_capture_check.py` covers actual Chromium extraction from controlled widget HTML. Validation evidence is recorded in `validation/owner-continuation.json` after completion. Do not treat the historical sections below as the latest UI/motion policy.

Build the Windows package using `.venv/bin/python tools/build_windows_package.py downloads/Main_roll_test.zip`. The archive contains the connected launcher and exact current editor/importer files, with per-file SHA256 checksums. Users should extract all files into a new folder, close old helper windows, and run `TEST_MAIN_ROLL.bat`. Windows execution itself is not verified on this Linux host.

# Current continuation — Beta 2.7.8 recovery

The owner supplied the Universal Main roll continuation on October 29, 2026, authorizing reconstruction and implementation beyond the historical scope below. Read [RECOVERY_BETA278.md](RECOVERY_BETA278.md) first. Work is on `ze-os-v07-beta278-recovery`, from `e1e4830ef214a93a6c823b18543349791b4f9f3f`; keep main untouched. The failed environment was not recovered. Compare and preserve any subsequently supplied recovery files before further work. V0.7 alone remains approved. The older “wait for edits” text below records historical context and is superseded by this continuation.

# ZE OS / Mouwajaha V0.7 — Codex Handoff

## Current user decision
- Active project: one **Mouwajaha roll**.
- Main version: **V0.7**, including its newer focused workflow features; do not revive V0.8 or V0.9 multi-template Atlas as the base.
- The user intends to list more corrections in Codex. First inspect the code and source AEP, verify the existing app, and wait for specific edits.

## What the app is meant to do
A browser-based, offline-first editable TV-roll graphics tool: an animated social post or web article frame with optional Arabic bullet/paragraph panel; a program identity and background loop; branded account name, platform logo, profile picture; resize/reposition/flip, preview, and eventual standalone rendering plus After Effects export. Current V0.7 remains a beta; do not represent it as broadcast-certified or pixel-exact.

## Accepted behavior from previous review
- Professional multi-stage animated entrance, including layered square/logo construction, roll-frame/mask reveal, source scroll, accent/panel motion, and staggered Arabic text.
- Two-column layout with bullet enabled.
- Bullet disabled: panel and text disappear; roll recenters automatically and may widen based on content shape; header follows.
- Flip: swap source and bullet side **without reversing lettering**; move account header with the source. Header order from outside edge inward: logo, profile, name/handle.
- STV for Arabic, editable justified/kashida text; maintain last-line alignment.
- Import local media and URL/source metadata when obtainable; user can replace any sample pictures and loops.
- Sample media can replace missing original assets; original motion geometry and design are priority.
- Program loop color adaptation with manual/identity palette override.
- Safe area must be respected, eventually with custom on-air exclusion zones.

## Important distinctions
- `ali.aep` reveals project structure, but references may be missing. The linked `blame roll.mp4` is the finished TV reference, and should be copied into this folder for frame-by-frame comparison.
- No source STV font is included or should be redistributed; the user can import their licensed local font.
- Public social platforms often restrict scraping; the URL importer is best effort with a screenshot/manual fallback.
- Previous frame-by-frame studies used estimated motion, not authoritative native AE easing/keyframes; only verify fidelity after source comparison.

## Codex starting task to paste
> We are continuing ZE OS from the ChatGPT design session. Read AGENTS.md and CODEX_HANDOFF.md, inspect the current ZE_OS_Mouwajaha_V07.html and ali.aep, and find the original blame roll.mp4 reference in this folder. Treat V0.7 as the sole approved baseline. Do not start coding yet: first summarize the architecture, describe current controls and limits, and be ready for my specific corrections. Preserve the original broadcast identity, editability, and professional animation. Never revert to the V0.8/V0.9 Atlas experiments.
