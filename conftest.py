import pytest

from pages.todo_page import TodoPage


@pytest.fixture
def todo(page) -> TodoPage:
    """A fresh, empty TodoMVC page. pytest-playwright gives every test its own browser context."""
    return TodoPage(page).open()


@pytest.fixture
def three_todos(todo) -> TodoPage:
    todo.add("Buy milk", "Walk the dog", "Pay rent")
    return todo
