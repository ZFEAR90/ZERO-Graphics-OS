ZE OS — Mouwajaha V0.7 / Test Beta 2.4

QUICK VISUAL TEST
Open ZE_OS_Mouwajaha_V07.html in Chrome or Edge for offline editing. Live post import requires the helper; opening the HTML does not start it.
The supplied STV Regular/Bold fonts and sample media are embedded for your local testing.
Reference Match now uses proxy-sampled timing and is the default. Enhanced Motion remains an optional treatment.
Test Flip with short/long English and Arabic names. The straps measure the text, remain attached to the profile, and fit the available header space. Very long names reduce slightly and then truncate with an ellipsis; the original editable field retains the full name.

LIVE POST IMPORT ON WINDOWS
Extract the complete ZIP into a folder. Install Python 3.10 or newer if needed.
Double-click START_ZE_OS.bat. On first use it installs the Python dependencies in .venv (Internet needed), starts the helper, and opens the editor.
Keep the helper window open. Paste the Facebook share link or another public post URL, then click Detect & import post.
The helper tries public metadata, validates share-link redirects, retrieves available author/profile/media, and optionally captures the actual post in a browser.
Chrome/Edge or an installed Playwright Chromium is needed for screenshot capture. For Playwright Chromium, run:
.venv\Scripts\python.exe -m playwright install chromium

MAC / LINUX
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python ze_local_importer.py

IMPORT LIMITS
Opening the HTML alone supports editing and offline platform recognition. Live import needs the local helper.
Facebook/Instagram/X can withhold public content or require login. The helper does not sign into accounts or bypass access restrictions. Unavailable profile photos/captures must be imported manually.
When a real screenshot is unavailable but post text/images are obtainable, the roll displays an explicitly marked imported content card. It is not a screenshot of the original site.
The original sample portrait/article is cleared on new import so old content cannot be mistaken for the new post.

VALIDATION
Browser checks: embedded STV faces, eight English/Arabic long-name + flip cases, centered roll, reference seeking, and post/name/avatar/logo replacement using controlled response data. No JavaScript exceptions.
Importer regression tests cover X author/photos, Telegram author/avatar, Facebook share redirects, blocked redirects, denied posts, URL validation, and localhost API response.
The user's Facebook example could not be fetched from the cloud: the configured outbound proxy denies Facebook. Its real content and capture remain unverified. The required social hosts were saved to the environment configuration draft, not applied or published.

MOTION / AEP
ali.aep was inspected as a RIFX project. Roll/mask/stroke structures and transform/effect property records are present. The revised V0.7 enhanced entrance uses smooth zero-velocity/acceleration endpoints and retains independently staged logo squares, frame/masks, article reveal, and paragraphs.
Native AE temporal Bezier curves were not recovered. This is a reconstruction beta, not a pixel-exact or broadcast-approved master.
The unmodified supplied HTML is retained in baseline/ in the development checkout.

BETA 2 CONNECTION FIX
Use Check importer connection before importing. Run START_ZE_OS.bat from the extracted Beta 2 folder, keep the command window open, and use the tab it launches. An unreachable importer and a platform refusal now produce distinct messages. Failed imports keep your previous scene. Eight importer tests and browser checks for disconnected/denied/successful imports passed. The actual Facebook post remains unverified from this cloud.

BETA 2.1 CAPTURE FIX
Close the previous command window before starting the new helper. The launcher now checks the capture browser and installs Chromium if needed. Browser fallback waits for a visible post/images and reports why it fails. Check importer connection should show version 0.7-beta2.1. Facebook can still refuse public access; try the direct URL reached by clicking the post timestamp. The real Facebook example remains unverified in the cloud.

BETA 2.2 INTERFACE
Click any category title or its arrow to fold/unfold its controls. Post import and Project export are open initially; other categories are folded. Changes remain when a panel is folded. Enter/Space work on focused headers. On small screens, categories stack below the preview.

BETA 2.3 POST MEDIA AND AUDIO
Open Post photos, video & audio. Choose text + selected media, media only or text only. Include/exclude photos/videos or individual items; unchecking retains an item for restoration. Add originals locally if the platform restricts access. The roll, bullet panel and account header adapt together; bullets off centers the group.
Include post audio starts OFF. Enable it for preview and WebM recording, and adjust volume. Audio may remain when video is hidden; uncheck an individual item to remove its picture and audio. Flattened screenshots cannot provide removable media or sound. Only public downloadable media can be fetched automatically; remote attachments are limited to 40 MiB each. The real Facebook post is still unverified.

BETA 2.4 MOTION / SAFE AREA / COLORS
Gray masks grow independently with smooth interpolation. Reference timing was measured from the 25 fps proxy; full-resolution/native-AE exactness is not yet verified.
Guides & safe areas uses y=847 from your guide, a 24 px lower-third gap, and 152 px channel-logo top clearance. Adjust the breaking-news top edge upward if that strap is taller. Protection is on by default. Guides are preview-only.
Changing the background loop selects three main colors automatically. Edit Accent, Panel and Text, or unfold Individual element colors for per-element overrides. Overrides remain when the loop changes until unchecked/reset. The full uploaded reference exceeds the 32 MiB transfer limit; the existing proxy was used.

BETA 2.4 GROUP EDITING / PREVIEW / DEMO
Layout & positioning: drag Account group, Roll + account, or Bullet panel. Shift-click adds a group. Select all moves the full composition. Whole-composition Up/Down moves all groups; Reset restores that offset. Safe protection limits movement to the available on-air area. Header/logo/profile sizes remain stable across 9:16 and landscape sources.
The last complete preview/background is retained during missing decoded frames. Intentional black video frames remain part of the original media.
The demo folder contains a 40-second MP4 walkthrough, an actual eight-second WebM export, and original synthetic demo media. Live social extraction is not demonstrated as successful. Exact full-resolution/native-AE fidelity remains unverified.
