# On-air guide calibration

Source: the user's 1920×1080 guide image supplied in this conversation. Coordinates are read from that image, not an official machine-readable specification.

- Visible lower-third assembly: top approximately 847 px; ticker is below it.
- Foreground bottom limit: 823 px, leaving a 24 px gap above the assembly.
- Channel bug: approximately x=100–244, y=38–135 px. Global top clearance defaults to 152 px so either flipped layout clears it.
- Symmetric foreground side margins: 79 px. The illustrated lower-third spans approximately x=79–1844.
- The supplied image does not show an independently measurable taller breaking-news variant. Both editable presets start at 847 px; the user can enter a higher exclusion for a taller strap.

Protection fits the union of foreground group bounds, with extra paint padding for strokes/shadows. The background remains full-frame. Guide tint/labels are DOM preview overlays and are absent from PNG/WebM output. Animated group bounds and painted lower-third pixels were checked across 151 entrance frames; manual source offsets/scales and centered layouts were exercised.

The updated fitter preserves identity-group dimensions independently of portrait/landscape aspect ratio. Source and bullet content fit the remaining space, and the complete fitted composition can be translated within the protected region. Individual mouse offsets do not rescale unselected groups.
