"""TC-EDT: editing todos."""
import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_edit_with_enter_saves(three_todos):
    three_todos.edit("Walk the dog", "Walk the cat")
    three_todos.expect_titles("Buy milk", "Walk the cat", "Pay rent")


def test_double_click_opens_edit_field_with_current_title(three_todos):
    field = three_todos.start_edit("Walk the dog")
    expect(field).to_be_visible()
    expect(field).to_be_focused()
    expect(field).to_have_value("Walk the dog")


def test_toggle_and_delete_hidden_while_editing(three_todos):
    three_todos.start_edit("Walk the dog")
    row = three_todos.item("Walk the dog")
    expect(row.get_by_test_id("todo-item-toggle")).to_be_hidden()
    expect(row.get_by_test_id("todo-item-label")).to_be_hidden()


def test_edit_is_trimmed(three_todos):
    three_todos.edit("Walk the dog", "   Walk the cat   ")
    three_todos.expect_titles("Buy milk", "Walk the cat", "Pay rent")


def test_edit_to_empty_deletes_todo(three_todos):
    three_todos.edit("Walk the dog", "")
    three_todos.expect_titles("Buy milk", "Pay rent")


def test_escape_cancels_edit(three_todos):
    three_todos.edit("Walk the dog", "Something else", commit_key="Escape")
    three_todos.expect_titles("Buy milk", "Walk the dog", "Pay rent")


def test_blur_saves_edit(three_todos):
    three_todos.edit("Walk the dog", "Walk the cat", commit_key=None)
    three_todos.new_todo_input.click()  # move focus away
    three_todos.expect_titles("Buy milk", "Walk the cat", "Pay rent")


def test_edit_keeps_completed_state(three_todos):
    three_todos.toggle("Walk the dog")
    three_todos.edit("Walk the dog", "Walk the cat")
    three_todos.expect_count_text(2)
