# AI Usage

- Used Claude Code (Anthropic) as a pair-programmer throughout: implementing page objects and test scenarios from `test_design.md`, and iterating on structure/readability.
- Every test and page-object change was run against the live site (not assumed) before being accepted, including probing actual app behavior (e.g. empty-cart checkout) before writing assertions.
- AI suggested and applied refactors on request: extracting a shared `parse_price()` helper to remove duplicated price-parsing logic, and moving product-selection logic out of tests into page-object methods.
- AI proposed documenting a known application gap (checkout not blocked on an empty cart) as an `xfail(strict=True)` test rather than skipping it, and updated `test_design.md` accordingly.
- All suggestions were reviewed and confirmed by the author before being committed.
