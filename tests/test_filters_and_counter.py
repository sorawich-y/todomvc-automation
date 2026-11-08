"""TC-FLT / TC-CNT: filters, routing and the items-left counter."""
import re

import pytest
from playwright.sync_api import expect


def test_main_and_footer_hidden_with_no_todos(todo):
    expect(todo.main).to_be_hidden()
    expect(todo.footer).to_be_hidden()


@pytest.mark.parametrize("n", [1, 2, 5])
def test_counter_pluralises(todo, n):
    todo.add(*[f"task {i}" for i in range(n)])
    todo.expect_count_text(n)


@pytest.mark.smoke
def test_active_filter(three_todos, page):
    three_todos.toggle("Walk the dog")
    three_todos.show("Active")
    expect(page).to_have_url(re.compile(r"#/active$"))
    three_todos.expect_titles("Buy milk", "Pay rent")


def test_completed_filter(three_todos, page):
    three_todos.toggle("Walk the dog")
    three_todos.show("Completed")
    expect(page).to_have_url(re.compile(r"#/completed$"))
    three_todos.expect_titles("Walk the dog")


def test_all_filter_shows_everything(three_todos):
    three_todos.toggle("Walk the dog")
    three_todos.show("Completed")
    three_todos.show("All")
    three_todos.expect_titles("Buy milk", "Walk the dog", "Pay rent")


def test_selected_filter_is_highlighted(three_todos):
    three_todos.show("Active")
    expect(three_todos.filter_link("Active")).to_have_class(re.compile(r"\bselected\b"))
    expect(three_todos.filter_link("All")).not_to_have_class(re.compile(r"\bselected\b"))


def test_completing_item_inside_active_filter_hides_it(three_todos):
    three_todos.show("Active")
    three_todos.toggle("Buy milk")
    three_todos.expect_titles("Walk the dog", "Pay rent")


def test_browser_back_returns_to_previous_filter(three_todos, page):
    three_todos.toggle("Walk the dog")
    three_todos.show("Active")
    three_todos.show("Completed")
    page.go_back()
    expect(page).to_have_url(re.compile(r"#/active$"))
    three_todos.expect_titles("Buy milk", "Pay rent")
