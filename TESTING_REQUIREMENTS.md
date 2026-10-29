Create and maintain real test files for every Main roll adjustment. Follow the existing repository test style and inspect all current tests before adding new ones.

Testing requirements:

1. Do not rely only on screenshots or visual claims.
- Use Playwright/Chromium browser tests with geometry, pixel and state assertions.
- Save screenshots as supporting evidence, especially on failures.
- Use deterministic fixtures and fixed timeline positions.

2. Keep existing tests.
- Do not delete or weaken existing tests merely because behavior changed.
- Update an old expectation only when the product requirement intentionally changed.
- Add new regression coverage for the replacement behavior.
- Keep unrelated tests unchanged.

3. Add focused browser test files for:

- `browser_header_anchor_check.py`
  - Check the actual painted bottom of the profile/name/platform header.
  - Verify the visible header remains close to the bullet in normal and flipped modes.
  - Verify clearance from the TV-logo and Live protected areas.
  - Do not test only the larger invisible group box.

- `browser_bullet_grouping_check.py`
  - Short text containing blank lines remains one bullet in Auto mode when it fits.
  - “Split at blank lines” creates separate bullets.
  - Long text paginates according to the real safe panel capacity.
  - The final bullet remains visible until the end.
  - Existing manual paragraph timing is preserved where content still matches.

- `browser_bullet_persistence_check.py`
  - Selecting “Inside the roll” does not empty or hide bullet text.
  - Bullet text survives switches among Inside roll, Hide post text and Bullet panel.
  - The bullet disappears only when Show bullet panel is disabled.

- `browser_text_only_recenter_check.py`
  - Text-only mode keeps/recenters the approved roll position.
  - It does not jump upward.
  - Text stays above the breaking-news safe line.
  - Source/media geometry is not permanently changed solely by hiding media.

- `browser_whole_shared_scroll_check.py`
  - Whole roll frame defaults to text-left/media-right.
  - Text and media move together.
  - Their relative spacing remains constant while scrolling.
  - The optional Keep media visible mode pins media.
  - Wide text-above/media-below mode moves the complete content group.

- `browser_post_justification_check.py`
  - Arabic non-final lines use joining-safe kashida by default.
  - Prepared non-final lines fill the intended width within tolerance.
  - Final paragraph lines remain naturally aligned.
  - Words and glyph order are not reversed.
  - The stored original post text remains unchanged.

- `browser_native_account_check.py`
  - Whole roll account avatar, name and handle remain completely inside the roll.
  - Verify internal padding at large requested scales.
  - Account row remains pinned while body content moves.
  - External name/profile straps are absent in Whole mode.
  - The platform logo is slightly larger and remains beside the roll.

- `browser_media_sequence_check.py`
  - Multiple media show one item at a time by default.
  - Test the transition before, during and after the mask wipe.
  - Use solid red/blue images with an asymmetric marker so mirroring can be detected.
  - Verify no blank interval during the transition.
  - Verify Flip reverses wipe direction but does not mirror pixels.
  - Verify the final item is held.
  - Verify Grid mode still works only when selected.

- `browser_video_sequence_check.py`
  - Use real short video fixtures.
  - Only active/transitioning videos play.
  - Incoming video begins at the correct local time.
  - Hold last frame and Loop work.
  - No black frames occur while seeking or after a short video ends.
  - Audio weights crossfade during sequence overlap.

- `browser_media_only_layout_check.py`
  - Hide post text centers media.
  - No editor-created blurred background appears.
  - Fill covers the frame and Fit shows the entire image.
  - Portrait, square and wide media keep the approved roll frame size.
  - Imported links never appear inside or beneath the roll.

- `browser_safe_area_check.py`
  - Bullet text never crosses the breaking-news safe line.
  - Text-only roll content remains safe.
  - Respect safe area On constrains applicable geometry.
  - Safe area Off may let the roll/media cross the lower third, while bullet text remains protected.
  - A centered roll can still be moved upward.

- `browser_workspace_cleanup_check.py`
  - Main contains essential controls.
  - Advanced contains detailed controls.
  - Optional reference panels are collapsed.
  - Export and Render full video remain accessible.
  - Removing permanent panels does not break their controls or event listeners.
  - Test both desktop and narrow/mobile layouts.

- `browser_drag_undo_check.py`
  - Drag roll, bullet, header and all-elements groups separately.
  - Ctrl+Z, Ctrl+Shift+Z, Undo and Redo restore exact positions.
  - Verify logical grouping is preserved.

4. Test paragraph animation:
- First paragraph exits line by line.
- Lines overlap rather than waiting for the previous line to finish.
- The next paragraph enters while the previous one finishes exiting.
- Exit direction is opposite entry direction.
- Flip reverses directions correctly.
- The black bullet mask prevents text from appearing outside the panel.
- The final paragraph stays visible to the end.

5. Test exports and state:
- Project JSON includes bullet-grouping mode, justification mode, media-sequence settings, transition duration and sequence slots.
- Export/import round-trip preserves these settings.
- Default overall duration is 50 seconds.
- Manual paragraph durations survive a round trip.
- Render controls use the chosen duration.

6. Importer tests:
- Preserve all existing importer tests.
- Update the expected version to `0.7-beta2.7.8`.
- Run:
  `.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -q`

7. JavaScript validation:
- Extract the inline JavaScript from the HTML.
- Run `node --check` on the extracted script after every significant edit.
- A syntax check alone is not sufficient; browser tests must also run.

8. Media test server:
- For video tests, use the repository importer/media handler with HTTP Range support, such as `ze_local_importer.Handler._send_media`.
- Do not rely on a basic server that breaks browser video seeking.
- Wait for explicit readiness instead of using arbitrary long sleeps.

9. Test artifacts:
- Create versioned Beta 2.7.8 preview screenshots and a demonstration video only after tests pass.
- Do not overwrite Beta 2.7.7 artifacts.
- Report exact passed, failed, skipped and unrun checks.
- Never claim a test passed unless it actually executed and completed.

Run focused tests after each feature, then run the complete importer and browser regression suite before publishing.
