import hashlib
import os
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


def _media_slide(kind: str, href: str, active: bool) -> str:
    style = f"width:100%;height:100%;object-fit:cover;{'' if active else 'display:none'}"
    if kind == "image":
        return (
            f'<a href="{href}" target="_blank">'
            f'<img class="rr-slide" src="{href}" style="{style}"></a>'
        )
    return f'<video class="rr-slide" controls style="{style}" src="{href}"></video>'


def _move_js(direction: int, n: int) -> str:
    """Cycles .rr-slide children by `direction`, tracking position in the box's own data-idx --
    no external <script> needed: inline onclick attributes execute fine even in HTML inserted via
    insertAdjacentHTML (confirmed in-browser), unlike an inserted <script> tag, which wouldn't."""
    return (
        "var b=this.closest('.rr-media');"
        "var s=b.querySelectorAll('.rr-slide');"
        f"var i=(parseInt(b.dataset.idx||'0')+({direction})+{n})%{n};"
        "b.dataset.idx=i;"
        "s.forEach(function(el,j){"
        "if(j===i){el.style.display=''}else{el.style.display='none';"
        "if(el.tagName==='VIDEO')el.pause();}"
        "});"
        f"b.querySelector('.rr-cnt').textContent=(i+1)+' / {n}';"
    )


def _media_box_html(slides: list[tuple[str, str]]) -> str:
    """One small box (pytest-html's own div.media footprint: bordered, floated right, 320x240)
    cycling through every failure screenshot/video with </>, like its native carousel -- can't
    reuse that carousel because its <video> slot hardcodes <source type="video/mp4"> and rejects
    a real .webm outright (see the per-format loop in pytest_runtest_makereport)."""
    if not slides:
        return ""
    n = len(slides)
    viewport = "".join(
        _media_slide(kind, href, active=(i == 0)) for i, (kind, href) in enumerate(slides)
    )
    if n == 1:
        return (
            '<div style="border:1px solid #e6e6e6;float:right;height:240px;'
            f'margin:0 5px;width:320px;overflow:hidden">{viewport}</div>'
        )
    return (
        '<div class="rr-media" data-idx="0" style="border:1px solid #e6e6e6;float:right;'
        'height:240px;margin:0 5px;width:320px;overflow:hidden">'
        '<div style="display:grid;grid-template-columns:25px auto 25px;'
        'align-items:center;height:200px">'
        f'<div style="cursor:pointer;text-align:center" onclick="{_move_js(-1, n)}">&lt;</div>'
        f'<div style="height:inherit">{viewport}</div>'
        f'<div style="cursor:pointer;text-align:center" onclick="{_move_js(1, n)}">&gt;</div>'
        "</div>"
        f'<div class="rr-cnt" style="text-align:center">1 / {n}</div>'
        "</div>"
    )


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

    html_dir = Path(item.config.getoption("htmlpath")).resolve().parent

    def _rel_href(path: Path) -> str:
        return Path(os.path.relpath(path.resolve(), html_dir)).as_posix()

    extra = list(getattr(report, "extras", []))
    slides = [("image", _rel_href(p)) for p in sorted(folder.glob("*.png"))]
    slides += [("video", _rel_href(p)) for p in sorted(folder.glob("*.webm"))]
    media_html = _media_box_html(slides)
    if media_html:
        extra.append(html_extras.html(media_html))
    for trace in sorted(folder.glob("*.zip")):
        # A plain relative link, not extras.url(): with --self-contained-html this would need
        # to be a data: URI, and a plain `target="_blank"` link to one gets blocked by browsers
        # (top-level navigation to data: is treated as a phishing risk) and lands on
        # about:blank -- open the downloaded file at https://trace.playwright.dev.
        extra.append(
            html_extras.html(
                f'<a download="{trace.name}" href="{_rel_href(trace)}">'
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
