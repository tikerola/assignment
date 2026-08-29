# Test Design

## Scope

The test suite focuses on the application's core shopping journey and the highest-risk areas: authentication, cart state, pricing, checkout validation, product interactions, and inventory sorting.

## Test Coverage

1. **Happy path — full product and price verification**
   Covers the complete purchase flow from login through order confirmation. Selected products, individual prices, item totals, tax, and final totals are verified at the cart and checkout overview stages, with the successful order confirmation verified at the end.

2. **Login — negative cases**
   Verifies that invalid and locked-out users cannot log in and receive the expected error feedback.

3. **Cart — state integrity**
   Verifies that adding and removing products correctly updates cart contents and the cart badge count.

4. **Checkout — form validation**
   Verifies that required customer information is validated and incomplete checkout information prevents the user from proceeding.

5. **Product details — cart state persistence**
   Verifies that a product added from its details page is correctly reflected in the cart and that the selected product state is preserved.

6. **Checkout — empty cart guard (known gap)**
   Documents that the application does not block checkout when the cart holds zero items — clicking "Checkout" proceeds straight to the customer-information step with an empty order. Treating the application as if it had real business consequences (invoicing, fulfillment, reporting), an empty order reaching confirmation is a risk worth flagging. The corresponding test asserts the desired behavior (checkout is blocked) and is marked `xfail(strict=True)`, so it fails loudly — turning into an unexpected pass — if the application is ever fixed or changes in a way that resolves this gap, rather than silently reporting green against a real defect.

## Bonus coverage

- **Inventory — sorting**
  Verifies sorting by product name and price in both ascending and descending order. Kept out of the prioritized list above: it's a cosmetic list-ordering feature rather than a core purchase-flow risk, so it's included as supplementary coverage rather than displacing higher-risk scenarios.

## Reasoning

The test suite prioritizes the core business flow and data integrity over simple page-load checks. Particular emphasis is placed on cart and pricing validation because incorrect product selection, cart state, or price calculations directly affect the purchasing experience.

The tests also include negative scenarios to verify that invalid authentication and incomplete checkout information are handled correctly, and a known-gap scenario (empty-cart checkout) recorded as an expected failure rather than left unverified. Together, the prioritized scenarios provide focused coverage of the application's main user journeys and key functional risks without creating unnecessary duplication; inventory sorting is retained as bonus coverage rather than core risk coverage.
