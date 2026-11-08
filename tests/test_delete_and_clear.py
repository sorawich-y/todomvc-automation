"""TC-DEL: deleting todos and Clear completed."""
import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_delete_todo(three_todos):
    three_todos.delete("Walk the dog")
    three_todos.expect_titles("Buy milk", "Pay rent")
    three_todos.expect_count_text(2)


def test_delete_last_todo_hides_main_and_footer(todo):
    todo.add("Buy milk")
    todo.delete("Buy milk")
    expect(todo.items).to_have_count(0)
    expect(todo.main).to_be_hidden()
    expect(todo.footer).to_be_hidden()


def test_clear_completed_hidden_when_nothing_completed(three_todos):
    expect(three_todos.clear_completed_button).to_be_hidden()


def test_clear_completed_removes_only_completed(three_todos):
    three_todos.toggle("Buy milk")
    three_todos.toggle("Pay rent")
    expect(three_todos.clear_completed_button).to_be_visible()
    three_todos.clear_completed()
    three_todos.expect_titles("Walk the dog")
    expect(three_todos.clear_completed_button).to_be_hidden()
