"""TC-ADD: creating todos."""
import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_add_single_todo(todo):
    todo.add("Buy milk")
    todo.expect_titles("Buy milk")
    todo.expect_count_text(1)


@pytest.mark.smoke
def test_input_is_cleared_after_adding(todo):
    todo.add("Buy milk")
    expect(todo.new_todo_input).to_have_value("")


def test_new_todo_input_is_focused_on_load(todo):
    expect(todo.new_todo_input).to_be_focused()


def test_todos_keep_insertion_order(todo):
    todo.add("first", "second", "third")
    todo.expect_titles("first", "second", "third")


def test_title_is_trimmed(todo):
    todo.add("   Buy milk   ")
    todo.expect_titles("Buy milk")


@pytest.mark.parametrize("blank", ["", " ", "     "])
def test_blank_title_is_not_added(todo, blank):
    todo.add(blank)
    expect(todo.items).to_have_count(0)


def test_single_character_title_is_accepted(todo):
    """Lower boundary: the shortest non-blank title."""
    todo.add("a")
    todo.expect_titles("a")


def test_duplicate_titles_are_allowed(todo):
    todo.add("Buy milk", "Buy milk")
    expect(todo.items).to_have_count(2)


@pytest.mark.parametrize(
    "title",
    [
        "ซื้อนม",  # Thai
        "買牛奶 🥛",  # CJK + emoji
        "<script>alert(1)</script>",  # must render as text, not execute
        "Tom & Jerry's \"quote\"",
    ],
    ids=["thai", "cjk-emoji", "html-injection", "special-chars"],
)
def test_unicode_and_special_characters_render_as_text(todo, title, page):
    dialogs = []
    page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))
    todo.add(title)
    todo.expect_titles(title)
    assert dialogs == [], "HTML in a title must not execute"


def test_long_title(todo):
    title = "x" * 500
    todo.add(title)
    todo.expect_titles(title)
