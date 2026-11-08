"""Page Object for the React TodoMVC app.

Tests talk to this class, never to raw selectors, so a markup change is fixed in one place.
"""
from __future__ import annotations

import re

from playwright.sync_api import Locator, Page, expect


class TodoPage:
    PATH = "/examples/react/dist/"

    def __init__(self, page: Page) -> None:
        self.page = page
        # The edit field reuses data-testid="text-input", so scope the new-todo field to the header.
        self.new_todo_input: Locator = page.get_by_test_id("header").get_by_placeholder("What needs to be done?")
        self.main: Locator = page.get_by_test_id("main")
        self.footer: Locator = page.get_by_test_id("footer")
        self.items: Locator = page.get_by_test_id("todo-item")
        self.labels: Locator = page.get_by_test_id("todo-item-label")
        self.toggle_all_checkbox: Locator = page.get_by_test_id("toggle-all")
        self.counter: Locator = page.locator(".todo-count")
        self.clear_completed_button: Locator = page.get_by_role("button", name="Clear completed")

    # ---------- navigation ----------
    def open(self, route: str = "") -> "TodoPage":
        self.page.goto(f"{self.PATH}{route}")
        expect(self.new_todo_input).to_be_visible()
        return self

    def filter_link(self, name: str) -> Locator:
        return self.page.get_by_test_id("footer-navigation").get_by_role("link", name=name, exact=True)

    def show(self, name: str) -> None:
        self.filter_link(name).click()

    # ---------- actions ----------
    def add(self, *titles: str) -> None:
        for title in titles:
            self.new_todo_input.fill(title)
            self.new_todo_input.press("Enter")

    def item(self, title: str) -> Locator:
        return self.items.filter(has=self.page.get_by_test_id("todo-item-label").get_by_text(title, exact=True))

    def toggle(self, title: str) -> None:
        self.item(title).get_by_test_id("todo-item-toggle").click()

    def delete(self, title: str) -> None:
        row = self.item(title)
        row.hover()  # the destroy button only shows on hover
        row.get_by_role("button", name="Delete todo").click()

    def start_edit(self, title: str) -> Locator:
        row = self.item(title)
        row.get_by_test_id("todo-item-label").dblclick()
        return row.get_by_role("textbox", name="Edit todo")

    def edit(self, title: str, new_title: str, commit_key: str | None = "Enter") -> None:
        field = self.start_edit(title)
        field.fill(new_title)
        if commit_key:
            field.press(commit_key)

    def toggle_all(self) -> None:
        self.toggle_all_checkbox.click()

    def clear_completed(self) -> None:
        self.clear_completed_button.click()

    # ---------- assertions ----------
    def expect_titles(self, *titles: str) -> None:
        expect(self.labels).to_have_text(list(titles))

    def expect_count_text(self, n: int) -> None:
        word = "item" if n == 1 else "items"
        # This build prints "1 item left!" — tolerate the trailing "!" but not a wrong number or plural.
        expect(self.counter).to_have_text(re.compile(rf"^{n} {word} left!?$"))
