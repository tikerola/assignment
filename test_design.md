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

6. **Inventory — sorting**
   Verifies sorting by product name and price in both ascending and descending order.

## Reasoning

The test suite prioritizes the core business flow and data integrity over simple page-load checks. Particular emphasis is placed on cart and pricing validation because incorrect product selection, cart state, or price calculations directly affect the purchasing experience.

The tests also include negative scenarios to verify that invalid authentication and incomplete checkout information are handled correctly. Together, the six tests provide focused coverage of the application's main user journeys and key functional risks without creating unnecessary duplication.
