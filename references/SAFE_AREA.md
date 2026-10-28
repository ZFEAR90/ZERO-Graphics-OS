# On-air guide calibration

Source: the user's 1920×1080 guide image supplied in this conversation. Coordinates are read from that image, not an official machine-readable specification.

- Visible lower-third assembly: top approximately 847 px; ticker is below it.
- Foreground bottom limit: 823 px, leaving a 24 px gap above the assembly.
- Channel bug: approximately x=100–244, y=38–135 px. Global top clearance defaults to 152 px so either flipped layout clears it.
- Symmetric foreground side margins: 79 px. The illustrated lower-third spans approximately x=79–1844.
- The supplied image does not show an independently measurable taller breaking-news variant. Both editable presets start at 847 px; the user can enter a higher exclusion for a taller strap.

Beta 2.5 preserves requested foreground widths and typography instead of uniformly scaling the composition. It moves groups into the protected area, avoiding both the TV logo and top-right Live reservation when flipped. A source that is taller than the available vertical span gets a shorter scrolling viewport; its content is not stretched. Bullet panels can shorten their visible height while retaining text size. The default account group is 90% of the original, independent of source aspect ratio, with a further 5% reduction on the TV-logo side; its own size setting can override the base size.

The lower-third tint and edge from Beta 2.4 remain. The earlier mint title-safe outline (top/bottom/sides) and orange lower guide are restored, with separate TV/Live corner outlines. Guide DOM overlays are absent from PNG/WebM output. Painted lower-third pixels are checked over 151 entrance frames, separately from raw crop/selection rectangles, which include historical blank margins.

The safety band is finite: the original tall source plus an account header cannot both fit at their full height between 152 and 823 px. Shortening the viewing window avoids reducing widths, text and account graphics. Turning protection off restores the unrestricted height. Explicit extreme sizes warn instead of triggering an automatic whole-composition scale. Whole-composition offsets and per-group movement clamp at the on-air limits, with an undoable edit for each drag.
