# Final owner adjustments

These are the final adjustments requested immediately before the original Codex environment stopped working:

1. Universal naming and interface
- The project is now a universal social-media roll.
- Rename the primary layout everywhere to “Main roll.”
- Keep “Whole roll frame” as the alternate full-post presentation.
- Remove or collapse unwanted panels.
- Keep essential controls in Main and place detailed controls under Advanced options.

2. Flipped account header
- When the composition is flipped, the account header must remain as close to the bullet panel as it is when unflipped.
- Measure the actual visible profile/name/platform bounds rather than the larger invisible group box.
- When the bullet is visible, the header always belongs above the bullet, never above the roll.
- Compensate for the TV-logo area and Live area without leaving a large empty gap.

3. Whole roll frame default
- Default presentation: post text on the left and media on the right.
- Text and media must scroll/move together by default.
- Do not let only the post text move while the media remains behind.
- Keep an optional “Keep media visible” mode for speaker/face protection.
- For the wide arrangement, allow post text above and media below as an optional layout.
- Wide media should remain centered while moving with its text.

4. Whole-roll account treatment
- Do not show the external account header straps in Whole roll frame.
- Put the profile picture, display name and handle inside the roll at the top-left.
- Keep them pinned while post content moves.
- Add enough internal padding so the profile picture and labels never cross the roll edge.
- Keep the social-platform logo beside the roll.
- Make the platform logo slightly larger than its previous size.

5. Arabic post text
- Arabic post text inside Whole roll frame should use kashida justification by default.
- Use joining-safe kashida; never stretch or distort glyphs.
- Do not modify the stored source text.
- The final line of each paragraph should remain naturally aligned.

6. Text-only mode
- Selecting Text only must not move the roll upward or into the wrong position.
- Recenter the roll using the normal approved composition.
- Keep roll text above the breaking-news/lower-third safe line.
- Changing to Text only must not permanently alter the saved media geometry.

7. Bullet independence
- Choosing “Post text inside the roll” must never delete, empty or hide the external bullet text.
- The bullet panel disappears only when “Show bullet panel” is turned off.
- Post-text placement and bullet-panel visibility are separate controls.

8. Bullet grouping
- If all supplied bullet text fits safely in one panel, keep it as one bullet even when the source contains blank lines.
- Default mode: automatically keep text together when it fits and paginate only when necessary.
- Add an optional “Split at blank lines” mode for users who want blank lines to create additional bullets.
- Base automatic pagination on the real panel size, font size, line height and lower-third safe limit.

9. Multiple media
- When a post contains multiple images or videos, show one media item at a time by default.
- The first item exits through a smooth mask while the next item reveals through a complementary mask.
- Do not show a stacked grid by default.
- Do not leave a blank frame between items.
- Hold the final media item at the end.
- Flip mode reverses the wipe direction but must never mirror the media.
- Keep Grid/Together as an optional Advanced presentation.

10. Hidden post text and media-only layout
- When “Hide post text” is selected, center the media inside the roll.
- Do not add a blurred duplicate background.
- Default media fitting is Fill, with a Fit option.
- Preserve face-safe cropping where possible.
- Never place imported post links beneath the media or anywhere inside the roll.

11. Safe-area behavior
- The roll may cross the lower-third region when necessary for large media and when safe-area protection is disabled.
- Bullet text must always remain above the breaking-news safe line.
- Text inside a text-only roll must also remain safe and readable.
- Keep the Respect safe area On/Off control.

12. Final editor cleanup
- Main should contain the controls needed for normal use:
  post import, Main/Whole layout, bullet visibility/text, media selection, post-text placement, Fill/Fit, account details, safe-area toggle, primary timing, primary colors and Undo/Redo.
- Move typography details, kashida options, media sequence controls, face protection, manual geometry, detailed colors, guides and reference tools into Advanced options.
- Collapse optional AEP/reference/timing/about information.
- Keep Export and Render full video easy to reach.
- Preserve all working controls while removing unnecessary permanent panels.

Do not publish until these final adjustments are verified in a real browser in normal and flipped layouts.

## Owner testing corrections — October 30, 2026

Authorized implementation after owner testing: prioritize sentence/paragraph/list-point boundaries when paginating; pin an inferred introductory heading above long numbered lists using a colored strap, with editable title and Return to normal bullet; Main with visible bullets imports text to the external bullet and media only to the roll; Fit is the new import default (superseding Fill), with Fill retained; shared text/media movement when text is included, speaker-safe override retained; automatic loop-derived panel color and persistent manual override; temporary mouse width/height resizing for roll and bullet, responsive contents, Undo/Redo, reset, portable geometry. Post import starts expanded. No external AI service is used for semantic interpretation: pagination uses document structure and language-aware sentence boundaries, then clause/word fallback only for oversized units.
