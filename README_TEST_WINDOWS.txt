MAIN ROLL - BETA 2.7.8 - WINDOWS URL-IMPORT TEST

1. Extract the ENTIRE ZIP to a NEW folder.
2. Close older Main roll importer windows and offline browser tabs.
3. Double-click TEST_MAIN_ROLL.bat (or START_ZE_OS.bat).
4. Keep the command window open. Use the browser tab it opens.
5. Paste the public post URL and click Detect & import post.

REQUIREMENTS
Python 3.10 or newer is required for URL importing. Install it from
https://www.python.org/downloads/windows/ and enable the Python launcher.
The first run installs Python dependencies and needs Internet access.
The launcher opens a connected local editor, not the offline HTML file.

IF STARTUP FAILS
Read the command window and STARTUP_LOG.txt in this folder.
If a port is occupied, close the older helper window before retrying.
If Python is missing, install it and run the launcher again.
If post screenshots are unavailable, run INSTALL_CAPTURE_BROWSER.bat,
then restart START_ZE_OS.bat. Installed Chrome/Edge may also be used.
Social platforms may deny anonymous access. That is different from an
unreachable local importer. Upload original media manually when needed.

OFFLINE MODE
OFFLINE_MAIN_ROLL.bat opens the editor without Python. It supports manual
photos/video, editing and browser rendering. It does NOT start URL importing.

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
