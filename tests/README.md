# Main roll regression checks

Read `TESTING_REQUIREMENTS.md` for the owner's test contract. Every `browser*check.py` file is an executable Playwright/Chromium test, following the existing standalone repository style. Assertions cover scene geometry, rendered pixels and editor state. No test is a screenshot-only approval.

Run the complete regression set from the repository root:

```sh
.venv/bin/python tests/run_regression.py /tmp/main-roll-regression
```

The runner executes the exact unit-test discovery command requested by the owner and every browser check, with bounded concurrency and per-process deadlines. It preserves command exit codes and writes a JSON report distinguishing passed, failed, skipped and unrun checks. A timeout is a failure. Demonstration generation is separate and runs only after the complete set passes.

`browser_support.py` provides a real local importer HTTP server and range-served deterministic video fixtures through `Handler._send_media`, plus explicit decoder readiness. New tests save failure screenshots/errors under `/tmp/ze-browser-evidence`. Existing tests retain their geometry, pixel, motion and playback assertions. `browser_final_adjustments_check.py` uses temporary evidence by default; set `ZE_FINAL_EVIDENCE_DIR` only after validation to publish versioned screenshots.

| Requirement | Focused test file |
| --- | --- |
| Painted header gap and TV/Live clearance | `browser_header_anchor_check.py` |
| Capacity-based grouping, blank lines, timing, final page | `browser_bullet_grouping_check.py` |
| Independent bulletin text; Whole automatic hide/Main restore | `browser_bullet_persistence_check.py` |
| Text-only centering and retained media geometry | `browser_text_only_recenter_check.py` |
| Whole fixed right media / shared below-text roll | `browser_whole_shared_scroll_check.py` |
| Reflow at different Whole frame sizes | `browser_whole_resize_check.py` |
| Joining-safe kashida, final lines and source immutability | `browser_post_justification_check.py` |
| Native account containment, padding, pinning and side platform | `browser_native_account_check.py` |
| Asymmetric red/blue mask wipes, Flip, final hold, optional grid | `browser_media_sequence_check.py` |
| Real video playback, local time, audio weights and held frames | `browser_video_sequence_check.py` |
| Media-only centering, Fill/Fit, all shapes, URL cleanup, no blur | `browser_media_only_layout_check.py` |
| Mandatory text boundary and strict/flexible movable geometry | `browser_safe_area_check.py` |
| Desktop/mobile controls, Advanced details and working listeners | `browser_workspace_cleanup_check.py` |
| Individual/group dragging and exact button/keyboard history | `browser_drag_undo_check.py` |
| Download/load JSON, sequence slots, duration and manual holds | `browser_project_roundtrip_check.py` |
| Real URL API import and disconnected-helper preservation | `browser_importer_connection_check.py` |
| Staggered paragraph overlap, directions, pixel mask and final hold | `browser_handoff_check.py`, `browser_paragraph_check.py` |
| V0.7 frame-sampled entrance and safe-band pixel fidelity | `browser_motion_check.py` |
| Real helper process, port conflicts and connected launcher | `test_launcher.py` |
| Complete ZIP, exact source hashes and connected default launcher | `test_windows_package.py` |

Existing capture/import/media, portrait, native account, reference-size, solo-text, palette, clean-media, layout, editing and workspace suites are retained and run alongside these focused checks.

Intentional expectation changes are limited to documented product changes: automatic bulletin-off when choosing Whole; one history transaction for that selection; returning to Main restores prior visibility; Advanced control relocation; explicit Grid/speaker or hidden-video audio choices; and preserving media geometry in Text-only mode. Additional replacement-behavior tests cover each change. Other assertions are retained.

Unit mocks and controlled local URL responses are identified as fixtures. Passing them does not prove that a live X/Facebook/Instagram URL is anonymously accessible. Native Windows batch execution and unavailable external broadcast references are not validated by Linux/Chromium checks.

### October 30 owner examples

`browser_owner_adjustments_check.py` tests Main media-only/Fit import defaults, shared movement selection, sentence/numbered-point preservation, stationary title pixels in both flips, normal-bullet reset without source edits, actual background-driven panel color and manual locking. `browser_mouse_resize_check.py` uses real pointer handles to resize each group, verifies width/height independently, reflow, native-account containment, mandatory text safety, Undo/Redo/reset and JSON round trips. Existing auto-post/reference/post-layout checks deliberately replace old roll-text/Fill defaults with bullet/Fit; optional fixed-media and Fill assertions remain.

Owner continuation acceptance: `browser_pending_adjustments_check.py` covers 384 combinations of retained layout, flip, media shape, allocation size, Fit/Fill and text toggle. `test_telegram.py` verifies full text extraction and profile/media separation without live network access.

Development dependency installation: `.venv/bin/python -m pip install -r requirements-dev.txt`. Telegram browser capture separation is also exercised by `browser_telegram_capture_check.py`.

Latest post-review: `browser_owner_post_review_check.py` checks actual strap-safe text pixels, complete Main posts, independent account toggles that do not affect Whole, natural media proportions and overflow-only scrolling. `browser_screenshot_import_check.py` runs the bundled Arabic/English recognition in Chromium with no external requests, then reviews/imports separate profile and post-media crops. `test_offline_assets.py` verifies local model/engine/logo integrity.
