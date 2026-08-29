import base64
import hashlib
from pathlib import Path

import pytest
from playwright.sync_api import expect
from pytest_html import extras as html_extras
from slugify import slugify

import config
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.data.users import USERS

# Where a successful login redirects to.
LANDING_PAGE = InventoryPage.URL


def _artifact_test_folder(item: pytest.Item) -> Path:
    """Where pytest-playwright saves this test's screenshot/video/trace (mirrors its own
    `output_path` fixture, which isn't public API but is the exact logic it uses internally)."""
    output_dir = Path(item.config.getoption("--output")).absolute()
    file_name = slugify(item.nodeid)
    if len(file_name) >= 256:
        digest = hashlib.sha256(file_name.encode()).hexdigest()[:7]
        file_name = f"{file_name[:100]}-{digest}-{file_name[-100:]}"
    return output_dir / file_name


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach pytest-playwright's failure screenshot/video/trace to the pytest-html report.

    Must run at the "teardown" phase, not "call": pytest-playwright doesn't save these
    artifacts to disk until its own fixture teardown runs, which happens after the call
    phase (and its report) is already finalized.
    """
    outcome = yield
    report = outcome.get_result()
    if report.when != "teardown":
        return

    folder = _artifact_test_folder(item)
    if not folder.is_dir():
        return

    extra = list(getattr(report, "extras", []))
    for screenshot in sorted(folder.glob("*.png")):
        extra.append(html_extras.image(base64.b64encode(screenshot.read_bytes()).decode()))
    for video in sorted(folder.glob("*.webm")):
        extra.append(
            html_extras.video(
                base64.b64encode(video.read_bytes()).decode(),
                mime_type="video/webm",
                extension="webm",
            )
        )
    for trace in sorted(folder.glob("*.zip")):
        # Not extras.url(): a plain `target="_blank"` link to a data: URI gets blocked by
        # browsers (top-level navigation to data: is treated as a phishing risk) and lands on
        # about:blank. `download` exempts the click from that, since it saves rather than
        # navigates -- open the saved file at https://trace.playwright.dev.
        data = base64.b64encode(trace.read_bytes()).decode()
        extra.append(
            html_extras.html(
                f'<a download="{trace.name}" href="data:application/zip;base64,{data}">'
                f"Download {trace.name} (open at trace.playwright.dev)</a>"
            )
        )
    if extra:
        report.extras = extra


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--no-sandbox", "--disable-dev-shm-usage"],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 900},
    }


@pytest.fixture(scope="session", autouse=True)
def _configure_test_id_attribute(playwright):
    # App uses data-test, not Playwright's default data-testid.
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def page(page):
    page.set_default_timeout(10000)
    return page


@pytest.fixture(scope="session")
def _storage_state_cache():
    """{user_key: storage_state}, populated lazily by logged_in_page."""
    return {}


def _get_page_for_user(new_context, storage_state_cache, user_key: str):
    """Returns (context, page) authenticated as `user_key`, landed on the inventory page.

    Logs in for real once per user_key, then replays the cached storage_state into a fresh
    context on every call after that.
    """
    if user_key not in storage_state_cache:
        bootstrap_context = new_context()
        try:
            bootstrap_page = bootstrap_context.new_page()
            bootstrap_page.set_default_timeout(10000)
            login_page = LoginPage(bootstrap_page)
            login_page.open()
            login_page.login(USERS[user_key], config.PASSWORD)
            expect(bootstrap_page).to_have_url(LANDING_PAGE)
            storage_state_cache[user_key] = bootstrap_context.storage_state()
        finally:
            bootstrap_context.close()

    context = new_context(storage_state=storage_state_cache[user_key])
    page = context.new_page()
    page.set_default_timeout(10000)
    page.goto(InventoryPage.URL)
    expect(page).to_have_url(InventoryPage.URL)
    return context, page


@pytest.fixture
def logged_in_page(new_context, request, _storage_state_cache):
    """Page authenticated and landed on the inventory page, logged in as `request.param`
    (default: "standard"). Use `@pytest.mark.parametrize("logged_in_page", ["problem"],
    indirect=True)` to log in as a different user.
    """
    user_key = getattr(request, "param", "standard")
    context, page = _get_page_for_user(new_context, _storage_state_cache, user_key)
    try:
        yield page
    finally:
        context.close()
