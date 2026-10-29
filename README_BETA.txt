ZE OS — Mouwajaha V0.7 / Test Beta 2.7.3

BETA 2.7.3 — CURRENT CORRECTION
Reference size is the default under Main → Roll & account → Roll frame layout. The same V0.7 cadre is retained for 9:16, square and wide media: 804 × 796 pixels at 100% source scale with bullets on. Fit/Fill and post text placement do not resize it. The older adaptive treatments remain optional.
Main → Post photos, video & audio → Media fitting: Fill frame (crop edges) covers the frame by default. Fit whole image (no crop) shows the full picture/video inside it, with space when aspect ratios differ.
Post text placement is independent: Bullet panel / Inside the roll / Hide post text. Media posts default to editable bullets and no text inside the roll. Inside-roll text and media can scroll together or keep selected media fixed.
Fill crops edges. A manual face region can limit that crop when Protect manual face region is enabled; Fit shows the whole image and ignores zoom. There is no automatic face tracking.
The header stays above bullets when enabled. Reference-size solo cards anchor it inside the top strip, including portrait media. The whole bullet panel and text always remain above the lower third. Strict safe-area fitting can shorten the roll viewport; user scaling still applies.
Text-only solo rolls retain their existing larger size. Their editable text scrolls only above the selected lower-third boundary and gap, even with safe-area protection Off. The frame may still extend below it; baked-in screenshot lettering is not independently editable.
Close the old helper, extract this ZIP, and run START_ZE_OS.bat. Connection version: 0.7-beta2.7.3. demo/ZE_OS_V07_Beta273_Layouts.mp4 is a 14-second still comparison. Previous real animation recordings remain. Default duration remains 50 seconds; MOV/alpha is deferred to the final renderer.

BETA 2.7.2 — PREVIOUS WORKFLOW
The entire black bulletin panel and text now stay above the lower-third safe line, even with protection Off, after moving/scaling/flipping. Only the roll may use extra lower space.
Successful media-post imports copy the cleaned post text into the editable bullet field, replacing the sample text. Edited bullets remain independent. Main → Post photos, video & audio has Post text placement: Bullet panel / Inside the roll / Hide post text, plus Use post text in bullets.
Returning an unchanged copied bullet to the roll clears that duplicate; custom bullet edits are preserved. Inside the roll defaults to scrolling text and media together. Keep selected media visible is available when a speaker should remain fixed instead. Text-only imports retain their text inside the roll.
Media fitting defaults to Fill frame, with Fit whole image selectable. Single-media frames match media proportions to remove unintended white margins. Fit shows the whole image and ignores zoom. A protected crop region still limits Fill; soft duplicate background fills an uncovered edge when protection prevents a crop.
Wider two-column media are positioned lower for balance, with a small permitted roll overlap below the lower third. With bullets off, a wide card puts the profile/name/account inside its top strip and the platform tile across the top-right corner. The attached header moves with the card. Portrait solo remains its own layout.
Connection version is 0.7-beta2.7.2. Close the old helper before running this folder's START_ZE_OS.bat. The app still defaults to 50 seconds. A 24-second comparison and actual 8-second browser scroll export are in demo/. MOV/alpha belongs to the final renderer.

BETA 2.7.1 — EARLIER CORRECTIONS
The account/profile/logo header stays above the bullet column whenever bullets are enabled. Move the bulletin to move its header; the roll moves independently. With bullets off, the header sits above the roll.
Large centered portrait centers the whole assembly and gives the roll more height. Its header uses the bullet column instead of the space above the media.
Bullet TEXT always stays above the selected lower-third safe line, including the breaking-news preset and gap. This is mandatory even with Respect safe area Off. The black panel may extend below the line; wrapping/scrolling and a fixed mask keep the text above it.
Wider photo/video cards and Balanced put post text above the picture. Beside retains its separate columns. Original editable post URLs are removed from import/rendered text; source URL metadata remains. Baked-in links in screenshots/images are not automatically erased.
Each visual attachment has Framing / protect face. Default: full image protected, zoom 100%. For a closer crop, set a percentage rectangle including the entire face throughout the clip, then increase zoom, up to 140%. The crop keeps that rectangle visible. This is manual framing, not face detection or tracking.
Project JSON saves headerAnchor, mandatory bulletin text protection and per-media framing. Duration remains 50 s by default. MOV/alpha still belongs to the final renderer.
Connection version is 0.7-beta2.7.1. Close the old helper before running this folder's START_ZE_OS.bat. New layout stills and a 16-second comparison are in demo/.

BETA 2.7 — EARLIER CHANGES
Main has Respect safe area: On/Off. It defaults Off for the taller composition requested: bullets and roll may cross the lower third; movement is unrestricted. On enables strict protection and turns off the media-only exception. The separate media checkbox can selectively allow the roll below the lower third with protection still on. Guides remain visible. Automatic initial placement still compensates for the TV-logo side; the Live reservation ends above the green top-safe line.
Header size now defaults to 85%, plus the existing TV-side reduction; the centered portrait treatment has its own additional reduction. Imported bullets retain more height with protection off. A single photo stays fully visible while its caption scrolls separately.
Lines leave in an overlapping wave, and the next paragraph starts entering during that exit. Text widths, wrapping and font metrics control the handoff masks so lines do not touch. Flip reverses the motion. The final paragraph stays through the end; its manual hold is a minimum.
Solo roll: larger and centered; normal layouts stay constrained to the on-air region. The centered header can use the clear top-middle space. Moving into the middle or onto the Live side releases the taller TV-logo limit. The Live reservation now ends at the green top-safe line (68 px); the TV-logo clearance remains 152 px.
Roll language / reading direction is in Main → Roll & account: Auto, Arabic / RTL, or Latin / LTR. Editable Arabic uses STV. Original media pixels are never mirrored.
Post photos, video & audio now has After video ends → Hold last frame (default) or Loop per clip. Enabled source audio follows that choice. Keep video visible (speaker-safe) is on by default: complete video pictures remain fixed while other post content scrolls separately. Turn it off for normal post scrolling. This does not use a face detector.
Main → Roll & account → 9:16 photo / video layout has three choices for one selected portrait:
1. Large centered portrait (default): taller centered roll, compact readable header, smaller side bullets. Flip swaps the bullet side. The roll may cross the lower third, to 1016 px; bullets and header follow the Main safe-area switch.
2. Balanced card · soft sides: wider card, uncropped portrait over blurred duplicate side fill, independently scrolling caption. Its default viewport fits above the lower third.
3. Portrait beside post text: full-height picture beside separately scrolling editable text, with RTL/LTR ordering. Its default viewport fits above the lower third. Without text, media-only uses the soft-side card.
These choices work for photos or videos selected independently; flattened screenshots cannot be split. Multiple attachments use the combined post layout. The guide labels the permitted media-roll overlap. Allow large post photos/videos below lower third is enabled by default, for any independently selected media. With protection on, only the roll gains extra height/downward movement, up to 1016 px; turn it off to restore the usual source limit. Single landscape posts now use balanced source/bullet widths rather than squeezing bullets beside a wide roll. Choosing text-only or removing portrait media restores normal protection immediately.
The video choices, portrait treatment, overlap policy and language override are included in Project JSON. MOV alpha remains for the final renderer; the existing transparent PNG/background-off option is unchanged.
Connection version is 0.7-beta2.7. Close the old helper before starting the new folder's START_ZE_OS.bat.

BETA 2.6 — EARLIER CHANGES
Main → Bullet text → Paragraph timing & output contains the video length (default 50 s), transition duration, and individual Auto / Hold seconds / Preview controls.
Auto estimates reading time from paragraph length and shares available time accordingly. Manual holds are preserved when video length changes. Hold excludes entry and exit. A warning appears if the schedule cannot fit; full recording is blocked instead of silently truncating the text.
Text exits opposite its entry, then the next appears. Flip reverses both directions. Text is clipped inside the black panel throughout entry and exit.
Render full video (WebM) in Project export records the selected duration; the short preview remains separate. Keep the tab visible. Cancel discards the recording.
Transparent background removes the loop and solid fill. The preview uses a checkerboard; PNG exports have real alpha. MOV / ProRes 4444 alpha belongs to the final render engine and is saved as the output intent in scene JSON. Browser video recording is disabled in transparent mode; this beta does not export MOV alpha.
Connection version is 0.7-beta2.6. Close the old helper before starting START_ZE_OS.bat from this folder.

BETA 2.5 — EARLIER CHANGES
Main contains Roll & account, Bullet text, Post import, selected post media/audio and composition Up/Down. Advanced options holds the remaining detailed categories. Fold the category titles as needed.
Roll and bullet widths/text are restored: protection no longer scales down the composition. Tall viewing windows shorten only when necessary to fit above the lower third; content keeps its proportions and scrolls. Disable protection to use the original unrestricted height.
The logo/profile/name group defaults to 90%, stays consistent for 9:16 and landscape, and is a further 5% smaller on the TV-logo side. It clears both top corners after flipping. Change its group size in Advanced → Detailed layout & selection.
The current lower-third shaded guide is kept. Top/bottom/side lines from the older guide are restored, with TV/Live corner outlines. Guides are not rendered into exports.
Undo or Ctrl+Z restores each mouse drag as one step, including multi-group moves. Redo is Ctrl+Shift+Z / Ctrl+Y. Numeric position and Up/Down edits are undoable. Text fields keep native text undo. History lasts for the current session, up to 100 edits.
Close the previous helper and run START_ZE_OS.bat from this new folder; connection version should be 0.7-beta2.5.

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
