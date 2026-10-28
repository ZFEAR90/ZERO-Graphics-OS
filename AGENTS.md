# ZE OS / Codex working instructions

## Product and current scope
This repository is the focused **Zero Graphics OS (ZE OS)** beta for **Mouwajaha's Source Roll** only. The user is a television motion-graphics designer. **V0.7 is the approved baseline for ongoing iteration**; previous all-project V0.8/V0.9 atlas experiments were rejected. Do not merge their motion or generic templates into V0.7. Do not begin work on other projects or build the full ZE OS or local AI without explicit instruction.

## Files
- `ZE_OS_Mouwajaha_V07.html`: active browser beta, preserve its existing professional motion design until the user approves changes.
- `ze_local_importer.py`, `START_ZE_OS.bat`: optional public-post URL import helper.
- `ali.aep`: original After Effects project, supplied to study layer relationships, effects, timing, and motion; media may be missing.
- Original broadcast reference: `blame roll.mp4` (provided separately; place beside these files). It is the authority for appearance and the original entrance motion.
- No copyrighted STV fonts are bundled. Load a licensed copy from the user's PC; STV is the Arabic broadcast typeface used in the designs.

## Ground rules
1. One template at a time. Perfect Mouwajaha roll before proceeding to the next.
2. Fidelity first: compare original and browser reconstruction at matching timestamps, preferably each 25-fps frame, and quantify discrepancies. Do not call a scene pixel-exact without verifying it. Build independently editable layers, **not** a flattened playback of the original footage.
3. Motion should feel professionally staged: independently animated logo squares, scale and position, source-frame construction, roll mask reveal/scroll, bullet-panel expansion, text staging, natural ease-in/out, and *subtle* overshoot. Do not add distracting gratuitous effects. V0.7 motion language is the preferred baseline.
4. **Flipping must reposition groups, not mirror them.** Keep Arabic/English text and images in their normal orientation. The account header must move with its source, with platform logo at the outer edge, then profile photo, then account name/handle towards the inside.
5. When bullets are disabled, hide both the bullet container and text; center the source roll and intelligently size it based on its content aspect ratio and safe-area constraints. Header follows the source. Re-enabling bullets restores the two-column layout.
6. Make each element replaceable: background loop, source image/tall webpage screenshot, account/platform icon, profile photo, display name/handle, editorial title/bullets, borders/colors, sizes, positions, timing.
7. Tall webpage captures must scroll inside a masked source frame without deformation or stretching. Article screenshots should be clean and source-faithful.
8. Recognize post URL platforms (X, Facebook, Instagram, Telegram, Threads), and populate source name, icon/profile, and post media when publicly accessible. APIs/website restrictions mean import can fail; provide manual override rather than fabricate content.
9. Match accent palette to an imported local image/video loop *with* explicit overrides and the ability to restore approved program colors. Keep broadcast safe zones editable.
10. Arabic shaping, right-to-left text, STV font, justified lines/kashida and correct non-justified final line are important. Never horizontally mirror or rearrange Arabic letter order.
11. Output a playable preview inside the editor and maintain a clear reference-vs-reconstruction comparison.
12. When changing code, test the specific user-reported behavior, inspect at least representative entrance frames, and report any remaining fidelity gaps honestly. Preserve a working version before a major rewrite.

## Scope boundary
The user has asked to move the discussion from ordinary ChatGPT to Codex and has **not yet supplied their next adjustment requests**. Do not proactively redesign, implement new features, overwrite this baseline, or claim full functionality before they describe the next changes.
