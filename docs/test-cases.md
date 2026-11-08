# Test case design — React TodoMVC

App under test: https://todomvc.com/examples/react/dist/
Oracle: the [TodoMVC app spec](https://github.com/tastejs/todomvc/blob/master/app-spec.md) plus observed behaviour of this build.

Techniques: equivalence partitioning (blank / valid / special input), boundary values (1 char, 500 chars,
0 / 1 / many items for the plural counter), state transitions (active ⇄ completed ⇄ deleted, view ⇄ edit),
and negative tests (blank input, HTML injection).

Priority: **P1** = smoke (`-m smoke`, run on every commit), **P2** = regression.

| ID | Area | Scenario | Expected | Pri | Automated in |
|---|---|---|---|---|---|
| ADD-01 | Add | Type title, press Enter | Item appears, counter "1 item left" | P1 | `test_add_single_todo` |
| ADD-02 | Add | After adding | Input is cleared | P1 | `test_input_is_cleared_after_adding` |
| ADD-03 | Add | Page load | New-todo input has focus | P2 | `test_new_todo_input_is_focused_on_load` |
| ADD-04 | Add | Add 3 items | Shown in insertion order | P2 | `test_todos_keep_insertion_order` |
| ADD-05 | Add | Leading/trailing spaces | Title trimmed | P2 | `test_title_is_trimmed` |
| ADD-06 | Add | Empty / spaces only | Nothing added | P2 | `test_blank_title_is_not_added` ×3 |
| ADD-07 | Add | 1-character title (lower bound) | Added | P2 | `test_single_character_title_is_accepted` |
| ADD-08 | Add | Same title twice | Both kept | P2 | `test_duplicate_titles_are_allowed` |
| ADD-09 | Add | Thai, CJK+emoji, `<script>`, `& ' "` | Rendered literally, no script runs | P2 | `test_unicode_and_special_characters_render_as_text` ×4 |
| ADD-10 | Add | 500-character title | Added intact | P2 | `test_long_title` |
| CMP-01 | Complete | Tick an item | Gets `completed`, counter −1 | P1 | `test_mark_todo_completed` |
| CMP-02 | Complete | Untick it | Back to active, counter +1 | P2 | `test_unmark_completed_todo` |
| CMP-03 | Complete | Toggle-all | All completed, counter 0 | P2 | `test_toggle_all_marks_every_todo_completed` |
| CMP-04 | Complete | Toggle-all twice | All active again | P2 | `test_toggle_all_again_clears_every_todo` |
| CMP-05 | Complete | Tick every item / untick one | Toggle-all checkbox follows | P2 | `test_toggle_all_checkbox_follows_individual_items` |
| EDT-01 | Edit | Double-click, change, Enter | Title saved | P1 | `test_edit_with_enter_saves` |
| EDT-02 | Edit | Double-click | Edit field focused, prefilled | P2 | `test_double_click_opens_edit_field_with_current_title` |
| EDT-03 | Edit | While editing | Checkbox and label hidden | P2 | `test_toggle_and_delete_hidden_while_editing` |
| EDT-04 | Edit | Spaces around new title | Trimmed | P2 | `test_edit_is_trimmed` |
| EDT-05 | Edit | Clear title, Enter | Item deleted | P2 | `test_edit_to_empty_deletes_todo` |
| EDT-06 | Edit | Change, press Escape | Original title kept | P2 | `test_escape_cancels_edit` |
| EDT-07 | Edit | Change, click elsewhere | Saved on blur | P2 | `test_blur_saves_edit` |
| EDT-08 | Edit | Edit a completed item | Stays completed | P2 | `test_edit_keeps_completed_state` |
| DEL-01 | Delete | Hover, click × | Item removed, counter −1 | P1 | `test_delete_todo` |
| DEL-02 | Delete | Delete last item | Main list and footer hidden | P2 | `test_delete_last_todo_hides_main_and_footer` |
| DEL-03 | Clear | No completed items | "Clear completed" hidden | P2 | `test_clear_completed_hidden_when_nothing_completed` |
| DEL-04 | Clear | 2 of 3 completed, clear | Only active item left, button hides | P2 | `test_clear_completed_removes_only_completed` |
| FLT-01 | Layout | No todos | Main and footer hidden | P2 | `test_main_and_footer_hidden_with_no_todos` |
| CNT-01 | Counter | 1 / 2 / 5 items | "item" vs "items" | P2 | `test_counter_pluralises` ×3 |
| FLT-02 | Filter | Active | Only active, URL `#/active` | P1 | `test_active_filter` |
| FLT-03 | Filter | Completed | Only completed, URL `#/completed` | P2 | `test_completed_filter` |
| FLT-04 | Filter | All | Everything | P2 | `test_all_filter_shows_everything` |
| FLT-05 | Filter | Selected link | Highlighted | P2 | `test_selected_filter_is_highlighted` |
| FLT-06 | Filter | Complete item while on Active | Disappears from view | P2 | `test_completing_item_inside_active_filter_hides_it` |
| FLT-07 | Routing | Browser Back | Returns to previous filter | P2 | `test_browser_back_returns_to_previous_filter` |
| PER-01 | Persist | Reload page | Todos and state survive | P2 | `test_todos_survive_reload` — **xfail, see finding F-1** |

## Findings from the run

| ID | Finding | Severity | Evidence |
|---|---|---|---|
| F-1 | Todos are lost on page reload. The spec requires persistence (localStorage); this build stores nothing. | Medium | `test_persistence.py` (strict xfail — turns red the day it's fixed, so the test gets promoted) |
| F-2 | Counter reads "1 item left**!**" — spec text is "1 item left". | Low (cosmetic) | Locator in `TodoPage.expect_count_text` tolerates it explicitly |
| F-3 | New-todo input and edit input share `data-testid="text-input"` — ambiguous test hook. | Low (testability) | `TodoPage.new_todo_input` scopes it to the header |

## Not automated (manual / out of scope)

- Visual layout and responsive breakpoints (would use screenshot comparison, e.g. `expect(page).to_have_screenshot` via Playwright Test or Percy).
- Accessibility audit (axe-core via `axe-playwright-python`).
- Performance with thousands of items.
