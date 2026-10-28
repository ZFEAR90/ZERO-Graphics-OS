ZE OS — Mouwajaha V0.7 / Test Beta 2

QUICK VISUAL TEST
Open ZE_OS_Mouwajaha_V07.html in Chrome or Edge for offline editing. Live post import requires the helper; opening the HTML does not start it.
The supplied STV Regular/Bold fonts and sample media are embedded for your local testing.
Use Enhanced Motion for the revised smooth entrance, or Reference Match for the earlier timing treatment.
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
