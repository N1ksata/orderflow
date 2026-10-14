# OrderFlow Requirements

## Purpose

OrderFlow is a backend for an online store. It accepts orders,
reserves stock, and lets customers check their order status.

## Creating an order

- Only signed-in users can create orders.
- An order must contain at least one product.
- Customers send product IDs and quantities.
- Requests containing unknown product IDs return a validation error;
  no order is created.
- Quantities must be positive whole numbers.
- Product prices come from the database.
- Each order item stores its price at the time of purchase.

## Inventory

- An order must reserve all requested items or none of them.
- If any item has insufficient stock, the entire order is rejected.
- A rejected order reserves no stock and includes a rejection reason.
- When customers compete for the last unit, the first order to successfully reserve it in the database gets it.
- Available stock must never become negative.

## Duplicate requests

- Customers send a unique idempotency key for each purchase attempt.
- Retrying the same request with the same key returns the existing order.
- Reusing the same key with different products or quantities returns an error.
- Idempotency keys are scoped to the customer.

## Order status

- New orders start as pending.
- A background worker processes pending orders.
- Orders become confirmed when all items are successfully reserved.
- Orders become rejected when any requested product has insufficient stock.
- A temporary system failure must not be treated as an insufficient stock.

## Access

- Customers can view only their own orders.
- Administrators can view all orders.

## Initial Scope

- Payments, shipping, cancellations, and a storefront are excluded.
