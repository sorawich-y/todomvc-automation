# TodoMVC (React) — end-to-end tests

Automated UI tests for https://todomvc.com/examples/react/dist/ using **Python + pytest + Playwright**.

- 43 tests: add, complete, toggle-all, edit, delete, clear completed, filters, routing, counter, persistence
- Page Object Model, smoke/regression markers, parallel runs, HTML report, screenshot + video + trace on failure
- CI on GitHub Actions across Chromium, Firefox and WebKit

Test case design and the bugs found: [`docs/test-cases.md`](docs/test-cases.md).

## Why these tools

| Choice | Why | Over |
|---|---|---|
| **Playwright** | Auto-waits on every action and assertion (no `sleep`), one API for Chromium/Firefox/WebKit, built-in trace viewer for debugging failures | Selenium: needs explicit waits and separate drivers per browser, so tests are slower and flakier |
| **pytest** | Fixtures for setup, `parametrize` for data-driven cases, markers, huge plugin ecosystem (`pytest-xdist`, `pytest-html`) | unittest: more boilerplate, no fixtures |
| **Page Object Model** | Selectors live in one file (`pages/todo_page.py`); a markup change is a one-line fix, tests read like the spec | Raw selectors in each test |

## Set up (macOS / Linux / Windows)

Needs **Python 3.10+** and git. Check with `python3 --version`.

```bash
git clone https://github.com/sorawich-y/todomvc-automation.git
cd todomvc-automation

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium        # or: playwright install   (all three browsers)
# Linux CI box without browser libs: playwright install --with-deps chromium
```

## Run

```bash
pytest                              # whole suite, headless Chromium
pytest -m smoke                     # 6 critical-path tests
pytest -n auto                      # parallel, one worker per CPU
pytest --headed --slowmo 300        # watch it run
pytest --browser firefox            # or webkit; repeat the flag for several
pytest tests/test_edit_todo.py -k escape   # one test
```

Expected result: `42 passed, 1 xfailed`. The xfail is a real bug (todos lost on reload) — see findings.

## Reports and debugging

- `reports/report.html` — self-contained HTML report, opened in any browser.
- `reports/artifacts/<test>/` — screenshot, video and `trace.zip` for every **failed** test.
- Replay a failure step by step: `playwright show-trace reports/artifacts/<test>/trace.zip`

## Project layout

```
pages/todo_page.py      Page Object: selectors + user actions + reusable assertions
conftest.py             fixtures: `todo` (fresh empty app), `three_todos` (seeded)
tests/                  one file per feature area
docs/test-cases.md      test case table, traceability to test functions, findings
pytest.ini              base URL, browser, report and artifact settings, markers
.github/workflows/      CI: push, PR and nightly, 3-browser matrix
```

## Design notes

- **Isolation** — each test gets a new browser context (pytest-playwright default), so no test depends on another and the suite runs in parallel safely.
- **Stable selectors** — `data-testid` and accessible roles/names first, CSS classes only where nothing else exists.
- **No sleeps** — every wait is a Playwright web-first assertion (`expect(...)`), which retries until timeout.
- **Known bugs as strict xfail** — the test documents the expected behaviour; when the bug is fixed it turns red (XPASS) so someone removes the marker.
- **Config, not code** — base URL and browser come from `pytest.ini` / CLI, so the same suite runs against a staging URL with `--base-url`.
