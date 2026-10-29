# ZE OS — Mouwajaha V0.7, Test Beta 2.7.1

V0.7 is the active baseline. This branch contains the testable HTML editor and its local public-post importer.

## Latest corrections — Beta 2.7.1

- **Header above bullets:** with bullets enabled, the account/logo/profile group anchors to the bulletin column in every layout and Flip direction. Moving the bullet panel moves its header; moving the roll leaves the header in place. Independent header offsets stay within that column. With bullets off, the header moves above the roll.
- **Centered portrait assembly:** Large centered portrait now centers the complete visible group, with a larger roll (436 scene-unit target height when the permitted space allows it). The roll can use the lower-third overlap permission; its header no longer takes space above it when bullets are on.
- **Mandatory bulletin text protection:** the black panel may extend below the guide with protection off, but its text is always measured, wrapped/scrolled and clipped above the lower-third safe line, including transitions and mouse movement. This rule remains active with **Respect safe area: Off**. The current selected regular/breaking-news boundary and gap define the line.
- **Post text first:** wider photo/video cards and the Balanced portrait treatment put their independently scrolling caption above the fixed picture. The explicit Beside treatment retains its separate text/media columns.
- **No copied URLs in roll text:** import and rendering remove HTTP/HTTPS, `www`, shortened `t.co` links and common bare domains from editable post text. The original source URL remains in the import controls/project metadata. Existing screenshot/image pixels are not OCR-edited; links baked into a supplied bitmap require a replacement or manual framing.
- **Optional protected crop:** under each visual attachment, unfold **Framing / protect face**. Full-frame protection and 100% zoom are the defaults. For a closer crop, enter a percentage rectangle containing the whole face throughout the clip, then increase zoom (up to 140%). The crop is limited/repositioned to keep that rectangle visible. This is a manual region, not automatic face detection/tracking. Framing and the header/text policies are saved in JSON.

The default duration remains 50 seconds. The existing line handoff, Hold/Loop, audio, palette and background-alpha controls remain. The native MOV/alpha renderer is still deferred.

[Current layout comparison](demo/ZE_OS_V07_Beta271_Layouts.mp4) · [Wide](demo/ZE_OS_V07_Beta271_Wide.png) · [Portrait](demo/ZE_OS_V07_Beta271_Portrait.png) · [Flipped](demo/ZE_OS_V07_Beta271_Flipped.png). This 16-second comparison uses four real editor stills; the earlier animation demos remain separately labeled.

Focused browser checks compare bulletin text pixels with/without the renderer across reference/imported layouts, flips, offsets and protection states; no changed text pixels may enter the lower-third region. They also verify caption positions, imported URL cleanup, complete-group centering, header grouping, solo placement, protected crop bounds and saved settings. Media/audio recordings, line handoffs, undo and the 151-frame reference entrance check remain covered.

## Download and test on Windows

1. Download this branch using **Code → Download ZIP**.
2. Right-click the downloaded ZIP and choose **Extract All**.
3. Install Python 3.10 or newer if it is not already installed.
4. Double-click `START_ZE_OS.bat` inside the extracted folder. First startup installs the helper dependencies and opens the editor in your browser.
5. Keep the command window open. In the browser tab it launches, click **Check importer connection**, then paste a public post URL and click **Detect & import post**.

Opening `ZE_OS_Mouwajaha_V07.html` directly works for offline editing. It does not start the importer. Facebook and other platforms can restrict public post access; a connected importer cannot guarantee access to every post.

## Current composition controls (Beta 2.7)

**Main → Respect safe area: On/Off** switches between strict fitting and the requested full-height composition. It defaults **Off**: taller bullets and roll may cross the lower-third guide, and movement is unrestricted. Automatic initial placement still accounts for the TV-logo side. **On** enables protection and clears the media exception, fitting source/bullets to the guides. The separate media checkbox can grant only the roll an exception when protection is on; the button then says “On · media exception.” Guides remain visible in every mode. The account group now defaults to **85%** (with the existing extra TV-side compensation); centered portrait headers are further reduced for readability within that layout.

A single landscape post uses comparable roll/bullet widths. With flexible placement, its bullet panel keeps the taller viewport instead of shortening at the lower third. A single photo remains fully visible in contain mode while its caption scrolls independently; it is not scrolled/cropped out of the frame. A video is similarly fixed unless its speaker-safe option is explicitly disabled. Multi-attachment posts retain their combined layout.

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

The editor opens in **Main**, with Post import, Roll & account, Bullet text, Post photos/video/audio, and Composition position. Roll/account and bullet text open initially; replacement pickers are nested under Roll & account. **Advanced options** contains detailed layout/selection, typography, animation, background loop, palette, and guides. Categories still fold without losing edits; both tabs support keyboard navigation. Undo/Redo remain visible above either tab. The reference/export sidebar is unchanged.

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

The user's 1920×1080 on-air guide shows the lower third beginning at approximately y=847. Protection defaults to a 24 px gap, 152 px top clearance for the TV logo and right-hand Live sign, and symmetric 79 px side margins. **Advanced options → Guides & safe areas** exposes both regular/breaking boundaries and clearance. The current lower-third tint/edge remains; the earlier top, bottom and side outline is restored, with corner reservations added. All guides are preview-only.

Beta 2.5 removes the uniform safety fitter that made the design small. Source and bullet widths and text sizes stay at their requested values. Protection repositions them upward; if a tall source or panel cannot fit between the top exclusion and the lower third, only its viewing height is shortened. Source content keeps its proportions and scrolls inside its window. Disable protection for the original unrestricted height. The account group defaults to 90% of its original size, consistently across media ratios, with a further 5% reduction on the TV-logo side, and clears both top corners after flipping. Its group-size control and per-element controls are under Advanced → Detailed layout & selection. Explicit extreme sizes can exceed a guide; a warning appears rather than silently scaling the composition down.

Changing the loop automatically selects three main colors: Accent, Panel, and Text. These are editable. **Colors & palette → Individual element colors** provides twelve overrides for frame, inner mask, roll border/ribbon, bullet ribbon/panel/text, name strap/text, account strap/text, and identity borders. Changing a color enables its override. Unticking it resumes palette following; reset restores all links. Bright saturated loop colors are included in sampling, and video intros are sampled for up to three seconds if their initial frame has no usable color. Brand logos and imported photos/video retain their original pixels.

Browser validation covered automatic palette selection from two real file inputs, master edits, persistent overrides, reset, preview-only guides, continuous gray scaling, 151 frames per safety preset, rendered-pixel exclusion of the lower-third band/gap, manual offsets/scales, and the existing font/name/import controls. Media playback, seeking, portrait reflow and audio-enabled/disabled recording checks passed with the revised timing and safe area. The Facebook access limitations remain.

### Mouse editing, fixed header size and preview stability

**Layout & positioning** now includes whole-composition Up/Down/Reset controls and group selection: Account group, Roll + account, Bullet panel, and Select all. Drag a selected group in the preview. Shift-click adds a group; selected subsets move only those groups, and Select all translates the full composition. Roll dragging includes its linked account header. Selection outlines are preview-only and hide during playback/recording. Safe protection clamps movement to the on-air area; switching it off permits unrestricted positioning.

Portrait media no longer scales down the header: the identity group uses the same base size across portrait and landscape sources. Beta 2.5 sets it to 90% of the original 432×94 scene units, with a further 5% reduction on the TV-logo side, unless explicitly resized. Within protected layouts, source/bullet content fits the available space separately from the header. Per-group mouse offsets and whole-composition offsets are included in scene JSON.

The renderer retains the last decoded background during decoder starvation and paints a complete scene into a staging canvas before publishing it to the visible/compare canvases. If rendering is interrupted, the prior complete preview is retained with a waiting message. Intentional black frames encoded into a media file are not removed. Tests simulated an unavailable background frame and an interrupted scene render and verified that the visible frame remained unchanged. Layout computation is cached between edits to avoid repeated fitting work during playback.

Paused frame stepping now seeks the reference on every 25 fps step, and frame buttons pause reference playback. This removes the prior multi-frame comparison tolerance while paused.

### Demonstration

- [41-second editor demonstration, with actual post-demo audio (MP4)](demo/ZE_OS_V07_Beta24_Demo.mp4?raw=true)
- [Actual approximately eight-second editor export, with audio (WebM)](demo/ZE_OS_V07_Beta24_Preview.webm?raw=true)

The demonstration uses generated local gradient/video assets and synthetic tone audio, not a successful live Facebook extraction. It shows category panels, loop-driven palette selection, individual overrides, editable text/media, portrait/landscape layouts, fixed header sizing, flip, bullet hiding, mouse grouping, on-air protection, audio controls and an actual WebM export. The MP4 is 1440×900 H.264/AAC; the actual exported preview is 1920×1080 VP9/Opus. Both have non-silent audio. No full-black preview interval was detected in the demonstration.

Developer checks: the editor/importer browser tests require Playwright and Chromium; media checks also use FFmpeg/ffprobe. Motion-calibration checks additionally require NumPy, SciPy and Pillow. These are development checks, not extra requirements for running the standalone HTML.

## Movement history (Beta 2.5)

Drag a group or use Shift-click / Select all for a selection. **Undo / Ctrl+Z** restores a whole drag in one step; **Redo / Ctrl+Shift+Z or Ctrl+Y** reapplies it. Whole-composition Up/Down, numeric offsets, sizes and layout toggles are also undoable. Ctrl+Z in a text input stays the browser's native text undo. History is local to the current editor session (100 edits); it is not a project/media undo system.

The new browser workspace check covers actual tab navigation, unchanged source/bullet widths, the smaller header, both flip directions clearing the TV/Live exclusion, protected upward movement, per-drag and grouped undo/redo, numeric edits, guide visibility and mobile width. Existing animation, imports, media/audio and palette checks remain.

[Beta 2.5 update demonstration](demo/ZE_OS_V07_Beta25_Demo.mp4) shows the current full-width layout, tabs, guides, TV-side header compensation, mouse movements and undo. The earlier Beta 2.4 video and actual WebM/audio recording are retained separately.

## Paragraph timing and transparent output (Beta 2.6)

Under **Main → Bullet text → Paragraph timing & output**, set the overall length (default **50 seconds**) and paragraph exit/slide time (default **0.64 seconds**). Each paragraph has a Preview button, an Auto checkbox and an editable Hold duration. Hold starts after its entrance/type reveal and excludes the exit. Auto estimates reading length from word/character counts, then distributes the available video time by those estimates. Manual holds remain unchanged when video length changes. Editing the same paragraph retains its manual setting; reordering exact paragraphs carries their timing with them.

Text enters from the right and exits left; Beta 2.7 overlaps the next paragraph line by line. Flip reverses those directions without mirroring glyphs. A fixed rounded mask clips the animated text inside the black panel in reference, protected, and imported layouts. The panel/frame entrance staging remains; Beta 2.7 uses the line-based text entrance described below. Long paragraphs scroll inside the same mask rather than losing lines. The timeline shows paragraph segments; Preview seeks to the chosen entrance. **Reset holds to Auto** clears overrides; **Use estimated total** sets a natural reading-length total. If paragraphs cannot fit, a warning preserves manual settings and prevents a full recording from silently cutting them off. If all holds are manual and finish early, Beta 2.7 keeps the final paragraph visible for the remaining time.

**Project export → Render full video (WebM)** records the selected duration in real time, with post audio if enabled. The short preview recorder remains available. Keep the browser tab visible; Cancel discards a recording. Browser recording runs in real time and can drop frames on a busy computer; deterministic broadcast rendering belongs to the final engine. Controls are locked while recording. The downloaded WebM receives finite duration metadata. A final offline render engine and native MP4/MOV encoding are not implemented in this beta.

**Transparent background (no loop)** removes both the loop and the background fill. The checkerboard is preview-only; PNG export contains real alpha. Project JSON records the transparent-output request and a target MOV / ProRes 4444 alpha setting for the final renderer. Browser WebM export is disabled in transparency mode because it does not provide reliable alpha. This beta does not claim to export a MOV alpha video.

Validation includes reading-length weighting, preserved manual holds, edited/reordered/duplicate paragraphs, overflow handling, motion-speed independence of hold seconds, both masked flip directions, pixel comparisons across imported/reference/protected layouts, transparent PNG alpha, saved timing/output settings, real full-duration WebM output and cancellation. Existing media/audio, safe-area, palette, typography/import and movement-history checks remain.

[50-second paragraph-transition example](demo/ZE_OS_V07_Beta26_50s.mp4) · [actual WebM export](demo/ZE_OS_V07_Beta26_50s.webm) · [transparent PNG example](demo/ZE_OS_V07_Beta26_Transparent.png). The MP4 viewing copy was converted externally, not generated by an in-app final render engine.

## Current line handoff, solo layout and post video (Beta 2.7)

Paragraphs now leave in a staggered top-to-bottom wave: each line starts before the previous line finishes. The next paragraph starts during that wave, also line by line. The renderer measures wrapped text, font metrics and each line's width. It gives incoming glyphs only the horizontal space already cleared by outgoing glyphs in the same vertical area. This retains the panel mask, supports different line counts/fonts and reverses correctly with Flip. The final paragraph has no exit and remains visible through the exact video end. A manual hold on the final paragraph is a minimum, rather than an instruction to clear the panel early. Full browser recording now leaves the editor at its final frame.

With bullets off, the source recenters and uses a larger viewport (720 scene units for the sample article; 760 for editable post text, with media-specific/compact/wide choices). Its header may occupy the clear upper-middle region so the source gets more height. With protection on, the bounds below apply; with it off, taller viewports and unrestricted movement are available. Top constraints use the group's destination bounds. The TV-logo side keeps its 152 px clearance; the shortened Live reservation ends at the green title-safe line (68 px). Moving into the middle or onto the Live side releases the taller TV clearance; a group that still spans the TV logo remains constrained there.

**Main → Roll & account → Roll language / reading direction** provides Auto, Arabic/RTL and Latin/LTR. Auto uses editable post text; each paragraph is wrapped and aligned in its direction, with STV for Arabic. Media and screenshot pixels are never mirrored or OCR-rewritten. The centered header's order follows the solo roll language.

**Main → Roll & account → 9:16 photo / video layout** offers three treatments for one selected portrait photo/video (including imported posts and local media):

| Choice | Behavior |
| --- | --- |
| **Large centered portrait** (default) | Tall, centered roll; compact readable account header; smaller bullet panel beside it. Flip moves bullets to the other side. The roll may cross the lower third, down to 1016 px, as explicitly requested. Header and bullets obey the Main safe-area switch. |
| **Balanced card · soft sides** | A wider card with a full, uncropped portrait over blurred duplicate side fill; a caption strip scrolls independently. Source and bullets have comparable widths; its default viewport fits above the lower third. |
| **Portrait beside post text** | Full-height portrait beside separately scrolling post text, ordered by Arabic/Latin reading direction. The default viewport fits above the lower third; the roll can use the optional extra-height permission. Without editable text, media-only uses the soft-side card. |

**Allow large post photos/videos below lower third** is on by default, following the latest user correction. It grants only the source roll extra height or downward movement, up to 1016 px, for independently selected photos/videos of any aspect ratio. Disable it to restore the usual limit. Header and bullet text stay protected when protection is enabled. Single landscape posts now use a 432-unit roll beside a comparable-width bullet panel, rather than squeezing bullets next to a 560-unit roll.

The menu applies to a single independently selected portrait (aspect ratio 0.42–0.72); multiple attachments use the existing combined layout. Screenshots cannot be split into editable media/text. Focus works with text + media and media-only; hiding the media or choosing text-only immediately restores normal safe-area limits. The lower-third guide remains visible and labels the media-roll permission. The header defaults to about 66% of original size for this centered treatment and stays independent of media dimensions. All three choices retain full-media contain rendering, without cropping or mirroring. The safe-area switch, layout and overlap policy are saved in JSON. Speaker-safe video can be unpinned explicitly; it then uses ordinary post scrolling.

Each video under **Post photos, video & audio** has **After video ends → Hold last frame / Loop**. Hold is the default. Loop repeats that clip, including its sound when post audio is enabled. Choices affect paused seeking, preview and browser recording and are written to project JSON. A last-decoded-picture cache prevents missing decoded frames at a loop boundary from replacing the visible video.

**Keep video visible (speaker-safe)** defaults on for every attached video. Selected videos remain in fixed, full-frame contain cells while text and other post media scroll below them. This is a conservative video-protection layout, not a face detector; it prevents scrolling/cropping from losing a speaker's face without requiring AI. Multiple selected videos share the fixed region. Uncheck the option to put a video back into the ordinary scrolling post. A single media-only video uses the complete source window. Flattened screenshots cannot supply independently pinnable videos.

Focused checks sample Arabic/Latin and mixed-length paragraph handoffs in both flip directions for simultaneous outgoing/incoming text, stagger order, empty frames and intersecting glyph bounds. They also verify final text at the exact end, larger solo layouts, language overrides, destination-aware top constraints, independent video end behavior, retained decoded frames, pinned-video geometry and saved choices. The previous media/audio, safe-area, typography/import, palette and undo checks remain applicable.

[Beta 2.7 demonstration](demo/ZE_OS_V07_Beta27_Demo.mp4) shows normal/flipped line handoffs and all three portrait options. The actual browser WebM exports and full-size comparison screenshots are in `demo/`; see `demo/README.txt` for durations and capture limits.
