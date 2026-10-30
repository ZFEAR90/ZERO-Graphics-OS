MAIN ROLL - BETA 2.7.8 - WINDOWS URL-IMPORT TEST

1. Extract the ENTIRE ZIP to a NEW folder.
2. Close older Main roll importer windows and offline browser tabs.
3. Double-click TEST_MAIN_ROLL.bat (or START_ZE_OS.bat).
4. Keep the command window open. Use the browser tab it opens.
5. Post import is open at the top of Main. Paste the public post URL and click Detect & import post.

REQUIREMENTS
Python 3.10 or newer is required for URL importing. Install it from
https://www.python.org/downloads/windows/ and enable the Python launcher.
The first run installs Python dependencies and needs Internet access.
The launcher opens a connected local editor, not the offline HTML file.

IF STARTUP FAILS
Read the command window and STARTUP_LOG.txt in this folder.
If a port is occupied, close the older helper window before retrying.
If Python is missing, install it and run the launcher again.
Missing pip in an existing .venv is now repaired automatically with Python
ensurepip. If that fails, use the official Python installer to Modify/Repair
Python with pip enabled, then rerun START_ZE_OS.bat.
If post screenshots are unavailable, run INSTALL_CAPTURE_BROWSER.bat,
then restart START_ZE_OS.bat. Installed Chrome/Edge may also be used.
Social platforms may deny anonymous access. That is different from an
unreachable local importer. Upload original media manually when needed.

OFFLINE MODE
OFFLINE_MAIN_ROLL.bat opens the editor without Python. It supports manual
photos/video, editing and browser rendering. It does NOT start URL importing.

LATEST TESTING ADJUSTMENTS
Imported original post text is shown inside the roll. Use Show post text
inside the roll to hide/show it without changing external bulletin text.
Use post text in bullets is an explicit one-time copy only.
Fit sizes media to its allocated area; Fill and manual framing remain.
Main, Adaptive, Whole frame and Dedicated 9:16 are retained. Balanced card
and Portrait beside post text have been removed.
Whole: right-side media stays stationary while text scrolls. Below-text
media scrolls with the text, with no automatic centering/repositioning.
Switching to Whole preserves your selected right/below arrangement.
Telegram text-only posts use the original body inside the roll. The channel
photo is a profile image, not a post attachment. Live access remains subject
to Telegram and local network restrictions.
Bullet pages prefer complete paragraphs, numbered points and sentences.
Oversized sentences may still need clause/word splits to fit safely.
Long numbered lists automatically pin their introductory heading on a
colored strap. Edit the title or click Return to normal bullet to reset it.
Changing the loop adapts the panel color. Editing Panel locks your manual
choice; untick Keep my manual panel color to follow the loop again.
Temporary mouse resizing: pause, click a roll or bullet panel, then drag
its right/bottom/corner handle. Text scales/reflows and media refits.
Undo/Redo and Project JSON retain sizes. Reset mouse sizes restores defaults.
The temporary feature can be disabled using its checkbox in Main.

WHOLE ROLL
Choosing Whole roll frame turns the external bullet off automatically.
Its text is retained; Main roll restores its previous visibility.
The complete post reflows inside the larger/resized frame. Long posts scroll
inside the mask; the account row stays pinned. Speaker-safe mode is optional.

PROJECTS AND EXPORT
Project JSON saves editor settings, sequence slots and manual paragraph holds.
Load project JSON restores those settings. Original media files stay local:
reattach them when loading on another computer. Default video length: 50 s.
PNG supports real alpha. Browser video is opaque WebM. Native MOV alpha is
not implemented. Use Edge or Chrome for testing.

The importer process and editor are tested in Chromium on the cloud machine.
The .bat scripts have not been run on a native Windows machine here.
