# ZE OS — Mouwajaha V0.7, Test Beta 2.2

V0.7 is the active baseline. This branch contains the testable HTML editor and its local public-post importer.

## Download and test on Windows

1. Download this branch using **Code → Download ZIP**.
2. Right-click the downloaded ZIP and choose **Extract All**.
3. Install Python 3.10 or newer if it is not already installed.
4. Double-click `START_ZE_OS.bat` inside the extracted folder. First startup installs the helper dependencies and opens the editor in your browser.
5. Keep the command window open. In the browser tab it launches, click **Check importer connection**, then paste a public post URL and click **Detect & import post**.

Opening `ZE_OS_Mouwajaha_V07.html` directly works for offline editing. It does not start the importer. Facebook and other platforms can restrict public post access; a connected importer cannot guarantee access to every post.

## Beta changes and validation

- Name straps size to the text and stay beside the portrait when flipped.
- Supplied STV Regular/Bold fonts are embedded in this beta.
- Enhanced Motion uses smoother easing while retaining the V0.7 staged entrance.
- Share-link redirects are validated before fetching the actual post.
- Importer connection checks distinguish a disconnected helper from a platform error. Failed imports preserve the existing scene.

Eleven importer tests passed. Browser checks covered STV loading, English/Arabic long names, flipping, representative entrance frames, centered layouts, and disconnected, denied, and successful imports with controlled responses. An approximately eight-second WebM export was verified. The actual Facebook post could not be tested through the cloud proxy; live import remains unverified for that post.

The AEP was inspected structurally. Native AE easing was not recovered, and full-resolution frame-by-frame fidelity remains unverified. This is a reconstruction beta, not a broadcast-approved master.

See `README_BETA.txt` for additional setup instructions and limitations. Original supplied HTML is preserved in `baseline/`.

## Public-post capture update (Beta 2.1)

Close the old helper window before starting this version. The launcher checks the capture browser and installs Playwright Chromium if no working browser is found. Capture waits for a visible post and its images. Errors now distinguish a missing browser, HTTP rejection, login redirection, timeout, and an unsupported page layout; valid metadata remains usable when capture fails. A successful screenshot is retained even if author extraction fails.

The supplied Facebook test URL is `https://www.facebook.com/share/p/1GVmqHPmx5/`. Its live content remains unverified because Facebook is outside this cloud instance's enforced network allowlist. Browser capture checks use controlled public-post, HTTP 400, and login-page fixtures. If a share link fails, open it normally, click the post date/time, and try that direct post URL. Posts that require signing in may need a manually imported screenshot.

## Interface categories (Beta 2.2)

The editor sidebar now groups controls into Post import, Source & bulletin, Layout & positioning, Media assets, Arabic typography, Animation, Colors & palette, and Guides & safe areas. Each titled panel has a fold/unfold arrow and supports Enter/Space keyboard toggling. Post import opens by default. The reference sidebar has Project export, AEP reference, Reference timing, and About this reconstruction; export opens by default. Folding preserves edits. Mobile controls wrap within the viewport.

Browser validation covered every panel, keyboard toggling without triggering playback, retained edits, layout controls, mobile horizontal overflow, and existing font/name/import behavior. Canvas images matched the preceding beta exactly at 1.2, 2.12, and 4 seconds; this verifies the interface regrouping did not change those rendered frames. The Facebook-access limitations above still apply.
