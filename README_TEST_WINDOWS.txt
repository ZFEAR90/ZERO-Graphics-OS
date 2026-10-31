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

LATEST POST-REVIEW ADJUSTMENTS
Main imports the complete editable post inside the roll: account row,
post text, then media aligned to the same post width. Media only / Text only
remain available. Profile picture and account name have independent switches
for Main; these switches do not change Whole frame mode.
Post text is kept below the decorative top strap and pinned account area.
Text-above media uses its full natural width and proportions. Text and media
move together only when the complete document exceeds the visible roll.
Whole keeps stationary right-side media and shared below-text scrolling;
its side platform tile is about 15 percent larger.
Missing account photos show a name initial instead of a blank circle.
Current platform vector logos are bundled locally; links identify the platform.

SCREENSHOT IMPORT
Below URL import, choose Import post screenshot. The local reader extracts
English/Arabic text and proposes platform, account and image crops. Review
and correct these fields, drag the profile/post-image crops as necessary,
then choose Import reviewed screenshot post. External bullets are preserved.
Use the connected editor opened by TEST_MAIN_ROLL.bat for automatic reading.
The models and logos are bundled in assets; screenshots are not uploaded.
Automatic detection is best effort: check the text, identity and crop borders.
A screenshot cannot recover original video/audio. The offline HTML supports
manual text/crop review; automatic reading needs the local editor connection.

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
