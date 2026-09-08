# Known Gaps & Future Improvements

Notes on what's already working well vs. what's next, kept separate from
`test_design.md` (coverage rationale) and `ai_usage.md` (AI usage) so this can
evolve independently. Nothing here has been applied to the code yet.

1. **`LANDING_PAGE = InventoryPage.URL` alias in `conftest.py`** — a
   single-use alias defined in test infrastructure purely to rename
   `InventoryPage.URL` to "where login redirects." It makes `conftest.py`
   reach into one specific page object just to re-export a constant
   (backwards layering: page objects should be consumed by tests/fixtures,
   not reached into by infra for a name), and creates two names for one
   value that could silently drift apart if a real "landing page" concept
   is ever introduced. It's used once, two lines below a spot that already
   references `InventoryPage.URL` directly — the alias buys no clarity. If
   "successful login lands here" is worth naming, it belongs on `LoginPage`
   (e.g. `LoginPage.SUCCESS_REDIRECT`), not as a bare conftest global.

2. **Duplicated inventory-item accessors across three page objects** —
   `CartPage`, `CheckoutStepTwoPage`, and `InventoryPage`/`InventoryItem`
   each independently implement the same
   `get_by_test_id("inventory-item-price")` → `parse_price()` list
   comprehension. A small mixin or shared "list of inventory-item rows"
   component would remove the triplication.

3. **Inconsistent `URL` constant across page objects** — `LoginPage`,
   `InventoryPage`, `CartPage`, and `CheckoutStepOnePage` each define a
   `URL` class attribute; `CheckoutStepTwoPage` and `CheckoutCompletePage`
   don't.

4. **Unused test users** — `tests/data/users.py` defines `problem`, `perf`,
   `err`, and `visual` accounts (SauceDemo's well-known misbehaving-app
   logins: broken sort/UI, artificial slowness, JS errors, CSS glitches),
   but only `standard` and `locked` are ever referenced in a test. The data
   is wired up; the scenarios that would use it aren't written yet.

5. **`pytest-rerunfailures` is declared but unused** — it's in
   `requirements.txt` but no `--reruns` flag appears anywhere in
   `pytest.ini`. Either drop the dependency or wire it up intentionally.

6. **Single-browser coverage** — CI and local setup only install/run
   Chromium; no Firefox/WebKit matrix.

7. **No accessibility or visual-regression coverage** — the image check
   (`wait_for_image_loaded`) confirms something rendered, not that it's
   visually correct, and there's no `axe-core`-style accessibility pass.

8. **Single fixed environment** — `--base-url` is hardcoded to
   `https://www.saucedemo.com` in `pytest.ini`. It's already an override-able
   CLI flag (chosen over `pytest-playwright`'s own `base_url =` ini key,
   which doesn't propagate to xdist workers), so multi-environment support
   exists mechanically — it's just never exercised or documented.

9. **Testing pyramid is 100% UI** — appropriate here (the assignment
   forbids API-only solutions and SauceDemo has no real API to test
   against), but worth stating explicitly: in a real product, more
   assertions would move down to API/unit tests, keeping UI coverage
   focused on the highest-risk end-to-end journeys — the same
   prioritization already argued in `test_design.md`.

10. **Duplicated timeout setup between `page` and `logged_in_page`** — the
    built-in `page` fixture is overridden at `conftest.py:152` to set a 10s
    default timeout, but `logged_in_page` never depends on that fixture: it
    builds its own `Page` via `new_context().new_page()` in
    `_get_page_for_user`, so the override never applies there. As a result
    `page.set_default_timeout(10000)` is duplicated in `_get_page_for_user`
    at two call sites (`conftest.py:174` and `:185`) instead of coming from
    one shared place.

11. **Session-scoped login cache doesn't mean what it implies under
    `-n=auto`** — `_storage_state_cache` (`conftest.py:158`) is
    `scope="session"`, and its docstring says a user is "logged in for real
    once per user_key." That's only true within a single process.
    `pytest-xdist` runs `-n=auto` as separate worker subprocesses, each with
    its own independent fixture tree, so a `session`-scoped fixture is
    session-scoped *per worker*, not across the whole run. With N workers,
    a given user can be logged in for real up to N times total (once per
    worker that happens to need it), not once. The caching still collapses
    "once per test" down to "once per worker," which is the real win — but
    the docstring overstates the guarantee as if it held run-wide.

12. **`browser_type_launch_args` unconditionally disables the Chromium
    sandbox, not just in CI** — `conftest.py:130` adds
    `["--no-sandbox", "--disable-dev-shm-usage"]` to every launch, with no
    branching on environment. Those flags are the standard workaround for
    running Chromium as root in a container with a small `/dev/shm` —
    exactly what `.github/workflows/tests.yml`'s `ubuntu-latest` runner
    needs — but the fixture applies identically to a local run (e.g. on a
    dev's own Windows machine), which doesn't need it and gets its sandbox
    disabled anyway. There's also no comment recording that the flags are
    CI-motivated, so the reasoning isn't discoverable from the code alone.
