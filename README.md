# ZE OS — Mouwajaha V0.7, Test Beta 2.4

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

Sixteen importer tests passed. Browser checks covered STV loading, English/Arabic long names, flipping, representative entrance frames, centered layouts, and disconnected, denied, and successful imports with controlled responses. An approximately eight-second WebM export was verified. The actual Facebook post could not be tested through the cloud proxy; live import remains unverified for that post.

The AEP was inspected structurally. Native AE easing was not recovered, and full-resolution frame-by-frame fidelity remains unverified. This is a reconstruction beta, not a broadcast-approved master.

See `README_BETA.txt` for additional setup instructions and limitations. Original supplied HTML is preserved in `baseline/`.

## Public-post capture update (Beta 2.1)

Close the old helper window before starting this version. The launcher checks the capture browser and installs Playwright Chromium if no working browser is found. Capture waits for a visible post and its images. Errors now distinguish a missing browser, HTTP rejection, login redirection, timeout, and an unsupported page layout; valid metadata remains usable when capture fails. A successful screenshot is retained even if author extraction fails.

The supplied Facebook test URL is `https://www.facebook.com/share/p/1GVmqHPmx5/`. Its live content remains unverified because Facebook is outside this cloud instance's enforced network allowlist. Browser capture checks use controlled public-post, HTTP 400, and login-page fixtures. If a share link fails, open it normally, click the post date/time, and try that direct post URL. Posts that require signing in may need a manually imported screenshot.

## Interface categories (Beta 2.2)

The editor sidebar now groups controls into Post import, Source & bulletin, Layout & positioning, Media assets, Arabic typography, Animation, Colors & palette, and Guides & safe areas. Each titled panel has a fold/unfold arrow and supports Enter/Space keyboard toggling. Post import opens by default. The reference sidebar has Project export, AEP reference, Reference timing, and About this reconstruction; export opens by default. Folding preserves edits. Mobile controls wrap within the viewport.

Browser validation covered every panel, keyboard toggling without triggering playback, retained edits, layout controls, mobile horizontal overflow, and existing font/name/import behavior. Canvas images matched the preceding beta exactly at 1.2, 2.12, and 4 seconds; this verifies the interface regrouping did not change those rendered frames. The Facebook-access limitations above still apply.

## Post photos, video and audio (Beta 2.3)

Open **Post photos, video & audio** after importing. Available original attachments are listed individually; uncheck an item to remove it from the roll and check it again to restore it. Use **Include photos**, **Include videos**, and **Roll content** to choose text plus media, media only, or text only. Text remains editable. Add original local image/video/audio files when the source platform does not expose its media publicly.

The roll adapts to the selected visual media's aspect ratio within the broadcast canvas. The bullet panel changes width/height and reflows its Arabic text; the logo, profile photo and name follow the source as one group. Flip changes positions without mirroring text. With bullets off, the roll and header center. Single-media-only display contains the complete image/video; a longer post or multiple media items scroll inside the mask without stretching.

**Include post audio** is off initially. Enable it and use the volume slider for preview and WebM recording. Sound can remain when the video picture is hidden; uncheck the individual item to remove both picture and sound. Playback, pause, and seeking follow the timeline. This adds audio to the existing entrance WebM recorder; it does not implement a full MP4 export.

Public MP4/WebM and supported audio downloads are cached locally in ignored `.ze_media/`, limited to 40 MiB per remote attachment, and served with byte ranges for seeking. Local files can be added directly through the browser. A flattened screenshot cannot provide separately editable photos/video or recover its audio. Media that requires login, a blob-only stream, an unavailable codec, or a non-downloadable player requires the original file; no private content is fetched.

Validated with controlled post responses and generated photo/portrait/video/tone fixtures: keep/remove/restore, linked sizing and flip, bullet centering, portrait reflow, multi-file uploads, video playback/pause/seeking, separate audio and hidden-video audio. The recorded WebM contained audible audio with sound enabled and no audio track when disabled. Sixteen importer tests passed, including media caching, file limits and byte-range responses. Existing font/name/import checks passed. The actual Facebook post remains unverified because of the cloud network restriction.

Developer media smoke test: `python tests/browser_media_check.py` (requires Playwright, Chromium and FFmpeg/ffprobe). Fixtures are generated colored frames and synthetic sine tones, not user media.

## Reference motion, safe area, and colors (Beta 2.4)

Reference Match is now the default. The nested source frame uses frame-sampled monotone Hermite curves from the embedded 960×540, 25 fps proxy. Logo/avatar construction and handle timing were recalibrated, and Arabic line-reveal windows were measured from the reference. Every gray/white mask grows independently rather than switching a full rectangle on.

The measured source outer-width mean absolute error over frames 17–30 improved from 15.36 proxy pixels in the preceding renderer to 0.14 pixels. This is a single source-geometry metric; it is not a full-scene pixel-match score. Content scale between sampled frames, native AE interpolation, fonts/layout under edited content, original background motion, and full-resolution fidelity are not fully verified. The newly uploaded full reference exceeded the tool's 32 MiB transfer limit, so validation used the existing proxy. Observations and measured results are in `references/motion_observations_25fps.json` and `references/motion_validation.json`.

The user's 1920×1080 on-air guide shows the lower third beginning at approximately y=847. Protection is on by default with a 24 px gap, 152 px top clearance below the channel bug, and symmetric 79 px side margins. **Guides & safe areas** exposes the regular and breaking-news top edges, top clearance, and gap. Both presets initially use the supplied guide boundary; set the breaking-news edge higher if its strap is taller. Foreground groups fit together inside the available area, including when dragged/scaled, flipped, or centered. The safe-area overlay is preview-only and does not burn into exports. Background loops remain full frame.

Changing the loop automatically selects three main colors: Accent, Panel, and Text. These are editable. **Colors & palette → Individual element colors** provides twelve overrides for frame, inner mask, roll border/ribbon, bullet ribbon/panel/text, name strap/text, account strap/text, and identity borders. Changing a color enables its override. Unticking it resumes palette following; reset restores all links. Bright saturated loop colors are included in sampling, and video intros are sampled for up to three seconds if their initial frame has no usable color. Brand logos and imported photos/video retain their original pixels.

Browser validation covered automatic palette selection from two real file inputs, master edits, persistent overrides, reset, preview-only guides, continuous gray scaling, 151 frames per safety preset, rendered-pixel exclusion of the lower-third band/gap, manual offsets/scales, and the existing font/name/import controls. Media playback, seeking, portrait reflow and audio-enabled/disabled recording checks passed with the revised timing and safe area. The Facebook access limitations remain.

### Mouse editing, fixed header size and preview stability

**Layout & positioning** now includes whole-composition Up/Down/Reset controls and group selection: Account group, Roll + account, Bullet panel, and Select all. Drag a selected group in the preview. Shift-click adds a group; selected subsets move only those groups, and Select all translates the full composition. Roll dragging includes its linked account header. Selection outlines are preview-only and hide during playback/recording. Safe protection clamps movement to the on-air area; switching it off permits unrestricted positioning.

Portrait media no longer scales down the header: the normal identity group remains 432×94 scene units (with its original logo/profile/text sizes) across portrait and landscape sources unless explicitly resized. Within protected layouts, source/bullet content fits the available space separately from the header. Per-group mouse offsets and whole-composition offsets are included in scene JSON.

The renderer retains the last decoded background during decoder starvation and paints a complete scene into a staging canvas before publishing it to the visible/compare canvases. If rendering is interrupted, the prior complete preview is retained with a waiting message. Intentional black frames encoded into a media file are not removed. Tests simulated an unavailable background frame and an interrupted scene render and verified that the visible frame remained unchanged. Layout computation is cached between edits to avoid repeated fitting work during playback.

Paused frame stepping now seeks the reference on every 25 fps step, and frame buttons pause reference playback. This removes the prior multi-frame comparison tolerance while paused.

### Demonstration

- [41-second editor demonstration, with actual post-demo audio (MP4)](demo/ZE_OS_V07_Beta24_Demo.mp4?raw=true)
- [Actual approximately eight-second editor export, with audio (WebM)](demo/ZE_OS_V07_Beta24_Preview.webm?raw=true)

The demonstration uses generated local gradient/video assets and synthetic tone audio, not a successful live Facebook extraction. It shows category panels, loop-driven palette selection, individual overrides, editable text/media, portrait/landscape layouts, fixed header sizing, flip, bullet hiding, mouse grouping, on-air protection, audio controls and an actual WebM export. The MP4 is 1440×900 H.264/AAC; the actual exported preview is 1920×1080 VP9/Opus. Both have non-silent audio. No full-black preview interval was detected in the demonstration.

Developer checks: the editor/importer browser tests require Playwright and Chromium; media checks also use FFmpeg/ffprobe. Motion-calibration checks additionally require NumPy, SciPy and Pillow. These are development checks, not extra requirements for running the standalone HTML.
