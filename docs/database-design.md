# Database Design

## products

Stores the products available in the store.

| Column          | Data type | Purpose                                |
| --------------- | --------- | -------------------------------------- |
| id              | integer   | Unique identifier for each product     |
| name            | text      | Product name                           |
| price           | decimal   | Price of one unit in EUR               |
| available_stock | integer   | Number of units available in the store |

### Rules

- Each product has a unique id.
- Name is required.
- Price must be greater than 0.
- Available stock must be zero or greater.

## Users

| Column        | Data type | Purpose                              |
| ------------- | --------- | ------------------------------------ |
| id            | integer   | Unique identifier for each user      |
| name          | text      | User’s display name.                 |
| email         | text      | User's email                         |
| password_hash | text      | Hashed password used to verify login |
| role          | text      | Either customer or admin             |

### Rules

- Each user has a unique id.
- Name and email are required.
- Each email address must be unique.
- Passwords are stored as hashes, never as plain text.
- New users receive the customer role.
- Users cannot assign themselves the admin role.

## Orders

| Column          | Data type | Purpose                                   |
| --------------- | --------- | ----------------------------------------- |
| id              | integer   | Unique identifier for each order          |
| user_id         | integer   | Identifies the user who placed the order. |
| status          | text      | Current order processing status.          |
| idempotency_key | text      | idempotency key                           |
| created_at      | timestamp | includes a time zone                      |

### Rules

- Each order has a unique ID.
- user_id is required and must reference an existing user.
- Status starts as pending and allows only pending, confirmed, or rejected.
- idempotency_key is required.
- The backend automatically sets created_at.
- The combination of user_id and idempotency_key must be unique.
- Different users may use the same idempotency key.
- Retrying the same request with the same user_id and idempotency_key returns the existing order.
- Reusing that combination with different products or quantities returns an error.

## Order items

| Column     | Data type | Purpose                                               |
| ---------- | --------- | ----------------------------------------------------- |
| id         | integer   | Uniquely identifies an order-item row                 |
| order_id   | integer   | References the order containing this item             |
| product_id | integer   | references the product being purchased                |
| quantity   | integer   | The quantity of the product                           |
| unit_price | decimal   | stores the price of one unit in EUR at order creation |

### Rules

- Each order item has a unique ID.
- order_id is required and must reference an existing order.
- product_id is required and must reference an existing product.
- quantity is positive whole number and it must be greater than 0.
- unit_price is required and must be greater than 0.
- The combination of order_id and product_id must be unique, so each product appears once per order.
- Changing the product’s current price must not change an existing order item’s unit price.

## Outbox Events

| Column       | Data type | Purpose                               |
| ------------ | --------- | ------------------------------------- |
| event_id     | integer   | identifies this event record          |
| event_type   | text      | Names the event, such as OrderCreated |
| order_id     | integer   | identifies the related order          |
| created_at   | timestamp | when the event is created             |
| published_at | timestamp | when the publisher sents the event    |

### Rules

- each event has a unique event ID.It must reference to an existing order.
- published_at stays empty until the event is successfully sent.
- if sending fails ,published_at will remain empty and retry the event.
