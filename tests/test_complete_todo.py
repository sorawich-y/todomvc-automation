"""TC-CMP: completing todos and toggle-all."""
import re

import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_mark_todo_completed(three_todos):
    three_todos.toggle("Walk the dog")
    expect(three_todos.item("Walk the dog")).to_have_class(re.compile(r"\bcompleted\b"))
    three_todos.expect_count_text(2)


def test_unmark_completed_todo(three_todos):
    three_todos.toggle("Walk the dog")
    three_todos.toggle("Walk the dog")
    expect(three_todos.item("Walk the dog")).not_to_have_class(re.compile(r"\bcompleted\b"))
    three_todos.expect_count_text(3)


def test_toggle_all_marks_every_todo_completed(three_todos):
    three_todos.toggle_all()
    for row in three_todos.items.all():
        expect(row).to_have_class(re.compile(r"\bcompleted\b"))
    three_todos.expect_count_text(0)


def test_toggle_all_again_clears_every_todo(three_todos):
    three_todos.toggle_all()
    three_todos.toggle_all()
    for row in three_todos.items.all():
        expect(row).not_to_have_class(re.compile(r"\bcompleted\b"))
    three_todos.expect_count_text(3)


def test_toggle_all_checkbox_follows_individual_items(three_todos):
    for title in ("Buy milk", "Walk the dog", "Pay rent"):
        three_todos.toggle(title)
    expect(three_todos.toggle_all_checkbox).to_be_checked()
    three_todos.toggle("Pay rent")
    expect(three_todos.toggle_all_checkbox).not_to_be_checked()
