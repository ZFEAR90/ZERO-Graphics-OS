ZE OS V0.7 Beta 2.7 — current demonstration

ZE_OS_V07_Beta27_Demo.mp4: 52-second silent H.264 viewing copy, 1920x1080, 25 fps.
0–18 s: actual normal-direction line-by-line paragraph handoffs.
18–36 s: actual flipped handoffs. The final paragraph stays visible at the end of each recording.
36–40 s: Large centered portrait, compact header and smaller side bullets, roll crossing lower third.
40–44 s: Balanced card with soft duplicate side fill and independently scrolling caption.
44–48 s: Portrait beside editable post text.
48–52 s: balanced-width landscape post, taller bullet panel and shortened Live reservation.
The last four sections are still screenshots from the real editor. Guides are preview overlays; they are not exported graphics.

ZE_OS_V07_Beta27_Normal.webm and ZE_OS_V07_Beta27_Flipped.webm are the actual 18-second browser recordings. The app still defaults to 50 seconds; only these concise demonstrations use 18. The matching *_Timing.json files contain their schedules; DefaultTiming.json records the unchanged 50-second default.
The MP4 was composed/converted externally with FFmpeg, adding section captions. It duplicates/holds frames where real-time capture dropped frames; this does not provide deterministic 25 fps broadcast rendering or an in-app MP4 engine.
The Portrait_Centered / Portrait_Balanced / Portrait_Beside / Landscape PNG files show full preview compositions. Editor.png shows the current interface. All Beta27 screenshots include the shorter Live guide above the green top-safe line. Respect safe area defaults Off for the requested taller layout: roll and bullets may cross the lower third. On fits both within the guides. The optional roll-only exception can be used with protection enabled. The header default is 85%, with the portrait treatment reduced further. Single landscape media now has balanced column widths.
The portrait/landscape source clips are generated demo graphics, not successful social-platform imports and not face-detection examples. Source audio is disabled in this silent demonstration; independent audio and Hold/Loop are checked separately in browser tests.

Earlier demonstration files retained below:

ZE OS V0.7 Beta 2.6 timing / transparent-output examples

ZE_OS_V07_Beta26_50s.webm: actual default 50-second browser export, 1920x1080, silent. Contains the three editable sample paragraphs, reading-length-weighted automatic holds, masked exits and following entrances. Rendered from the normal editor, with the background enabled.
ZE_OS_V07_Beta26_50s.mp4: H.264 viewing copy converted externally with FFmpeg, 25 fps (duplicated frames where the real-time browser capture drops frames). This conversion is not an in-app MP4 renderer.
ZE_OS_V07_Beta26_Timing.json: the actual default schedule and hold durations used by that recording.
ZE_OS_V07_Beta26_Editor.png: current timing controls and the editor.
ZE_OS_V07_Beta26_Transparent.png: actual PNG export with real alpha and the background disabled. The preview checkerboard and safe-area guides are not baked in.

Browser capture is real time and can drop frames; it is not the future deterministic broadcast render engine. MOV / ProRes 4444 with alpha is deferred to that final engine. The beta does not export alpha MOV or claim reliable alpha WebM.

Earlier demonstration files retained below:

ZE OS V0.7 Beta 2.5 update demonstration

ZE_OS_V07_Beta25_Demo.mp4: 40.48-second real-editor walkthrough, H.264, 1440x900, silent.
Shows full-width panels, the Main/Advanced tabs, retained lower-third guide plus restored outline/corner guides, a 90% account header with a further 5% reduction on the TV-logo side, mouse group moves, Undo/Redo, and local portrait media. It does not demonstrate successful live social extraction.

Earlier Beta 2.4 feature demonstration (retained):

ZE_OS_V07_Beta24_Demo.mp4: 41.0-second editor walkthrough, H.264/AAC, 1440x900.
ZE_OS_V07_Beta24_Preview.webm: actual approximately eight-second editor recording, VP9/Opus, 1920x1080.
Both contain actual demo post audio captured from the editor audio mixer.

The included loop/landscape/portrait clips are generated local gradient graphics and synthetic tone audio. They demonstrate editing without claiming live extraction from Facebook or another platform.
The user-supplied fonts/reference media in the editor retain their existing provenance. This is a reconstruction beta and is not broadcast approved or verified as pixel-exact.
