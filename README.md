# SauceDemo UI Test Automation

Playwright + pytest test suite covering the core shopping journey on
[saucedemo.com](https://www.saucedemo.com/): login, cart, checkout, and
inventory sorting. See `test_design.md` for what's covered and why.

## Requirements

- Python 3.10+
- Git

## Setup

Clone the repo, then from its root:

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows (PowerShell)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install dependencies and the Playwright browser:

```bash
pip install -r requirements.txt
playwright install chromium
```

Create a `.env` file in the project root with the SauceDemo test password
(published on the site's own login page):

```
TEST_PASSWORD=<password from the SauceDemo login page>
```

## Running the tests

Run the full suite with a single command (parallelized across CPU cores).
An HTML report is written to `results/report.html` on every run (along with
its `results/assets/` folder, so keep the two together when sharing it); any
failing test also gets a screenshot, video, and downloadable Playwright trace
attached directly to its report row -- click the screenshot to view it full
size, or download the trace and open it at
[trace.playwright.dev](https://trace.playwright.dev):

```bash
pytest -n=auto
```

Run only the curated smoke subset:

```bash
pytest -m smoke
```

Run the full regression suite explicitly:

```bash
pytest -m regression -n=auto
```

## Project structure

- `pages/` — Page Object classes, one per SauceDemo page
- `tests/` — the test suite
- `test_design.md` — what's tested and why
- `ai_usage.md` — how AI was used in this assignment
