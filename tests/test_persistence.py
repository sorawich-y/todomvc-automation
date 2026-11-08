"""TC-PER: the TodoMVC spec says todos must survive a page reload (localStorage)."""
import pytest
from playwright.sync_api import expect


@pytest.mark.xfail(
    reason="Known gap: this React build keeps todos in memory only; reload loses them (spec requires localStorage)",
    strict=True,
)
def test_todos_survive_reload(three_todos, page):
    three_todos.toggle("Walk the dog")
    page.reload()
    three_todos.expect_titles("Buy milk", "Walk the dog", "Pay rent")
    three_todos.expect_count_text(2)
