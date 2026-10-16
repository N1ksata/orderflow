# Database Design

## General Conventions

- All prices are in EUR and use exact decimal values.
- All timestamps include a time zone.
- All columns are required unless explicitly marked nullable.
- Each table's identifier is its primary key.

## products

Stores the products available in the store.

| Column          | Data type | Purpose                              |
| --------------- | --------- | ------------------------------------ |
| id              | integer   | Unique identifier for each product   |
| name            | text      | Product name                         |
| price           | decimal   | Current price of one unit in EUR     |
| available_stock | integer   | Number of units available to reserve |

### Rules

- Each product has a unique ID.
- Name is required and must not be empty.
- Price must be greater than zero.
- Available stock must be zero or greater.

## users

Stores customer and administrator accounts.

| Column        | Data type | Purpose                            |
| ------------- | --------- | ---------------------------------- |
| id            | integer   | Unique identifier for each user    |
| name          | text      | User's display name                |
| email         | text      | User's email address               |
| password_hash | text      | Password hash used to verify login |
| role          | text      | Either customer or admin           |

### Rules

- Each user has a unique ID.
- Name and email are required and must not be empty.
- Each email address must be unique.
- Passwords are stored as hashes, never as plain text.
- Role allows only customer or admin.
- New users receive the customer role.
- Users cannot assign themselves the admin role.

## orders

Stores purchase requests and their processing status.

| Column           | Data type                | Purpose                                     |
| ---------------- | ------------------------ | ------------------------------------------- |
| id               | integer                  | Unique identifier for each order            |
| user_id          | integer                  | Identifies the user who placed the order    |
| status           | text                     | Current order processing status             |
| idempotency_key  | text                     | Identifies a purchase attempt for this user |
| rejection_reason | text, nullable           | Explains why an order was rejected          |
| created_at       | timestamp with time zone | Records when the order was created          |

### Rules

- Each order has a unique ID.
- user_id must reference an existing user.
- Status starts as pending.
- Status allows only pending, confirmed, or rejected.
- Confirmed and rejected are final statuses within the initial scope.
- Rejected orders require a rejection reason.
- Pending and confirmed orders leave rejection_reason empty.
- idempotency_key is required and must not be empty.
- The backend automatically sets created_at.
- The combination of user_id and idempotency_key must be unique.
- Different users may use the same idempotency key.
- Retrying the same request with the same user_id and idempotency_key returns the existing order.
- Reusing that combination with different products or quantities returns an error.
- Each order must contain at least one order item.

## order_items

Stores the products requested in each order.

| Column     | Data type | Purpose                                    |
| ---------- | --------- | ------------------------------------------ |
| id         | integer   | Uniquely identifies an order-item row      |
| order_id   | integer   | References the order containing this item  |
| product_id | integer   | References the product being purchased     |
| quantity   | integer   | Number of units requested                  |
| unit_price | decimal   | Price of one unit in EUR at order creation |

### Rules

- Each order item has a unique ID.
- order_id must reference an existing order.
- product_id must reference an existing product.
- Quantity must be a positive whole number.
- Unit price must be greater than zero.
- The backend reads unit_price from the product's database price.
- The combination of order_id and product_id must be unique.
- Changing a product's current price must not change an existing order item's unit price.

## outbox_events

Stores events waiting to be published to RabbitMQ.

| Column       | Data type                          | Purpose                                |
| ------------ | ---------------------------------- | -------------------------------------- |
| event_id     | integer                            | Uniquely identifies this event record  |
| event_type   | text                               | Names the event, such as OrderCreated  |
| order_id     | integer                            | Identifies the related order           |
| created_at   | timestamp with time zone           | Records when the event was created     |
| published_at | timestamp with time zone, nullable | Records when publication was confirmed |

### Rules

- Each event has a unique event ID.
- order_id must reference an existing order.
- event_type is required and must not be empty.
- The backend automatically sets created_at.
- published_at starts empty.
- The publisher sets published_at only after RabbitMQ confirms publication.
- Events with an empty published_at remain eligible for retry.
- Repeated publication of the same event must retain its event ID.

## inventory_reservations

Records the stock reserved for each product in a confirmed order.

| Column     | Data type                | Purpose                                  |
| ---------- | ------------------------ | ---------------------------------------- |
| id         | integer                  | Uniquely identifies the reservation      |
| order_id   | integer                  | References the order receiving the stock |
| product_id | integer                  | References the reserved product          |
| quantity   | integer                  | Number of units reserved                 |
| created_at | timestamp with time zone | Records when the reservation was created |

### Rules

- Each reservation has a unique ID.
- order_id must reference an existing order.
- product_id must reference an existing product.
- The product must belong to that order's order_items.
- Quantity must be a positive whole number matching the order item's quantity.
- The combination of order_id and product_id must be unique.
- Confirmed orders have reservations for every order item.
- Pending and rejected orders have no committed reservations.
- Creating reservations reduces products.available_stock by the reserved quantities.
- Available stock must never become negative.
- Reprocessing an already confirmed or rejected order must not change inventory.
- Releasing reservations is outside the initial scope.

## Relationships

- One user can have many orders.
- One order contains one or more order items.
- Each order item references one product.
- One order can have multiple outbox events.
- One confirmed order has one reservation for each order item.
- One product can appear in many orders and reservations.

## Transaction Boundaries

### Creating an order

- Requests containing unknown product IDs return a validation error; no order is created.
- The order, order items, and OrderCreated outbox event must commit together.
- If any part fails, none of these records are saved.
- Concurrent requests with the same user_id and idempotency_key cannot create separate orders.
- A retry compares the submitted products and quantities with the existing order.
- Matching requests return the existing order; different requests return an error.

### Processing an order

- Workers must coordinate through the database before changing the same order or product stock.
- Stock checks must remain valid until the reservation transaction commits.
- All reservations, stock reductions, and the confirmed status must commit together.
- If any product has insufficient stock, the order becomes rejected with a reason and no inventory changes.
- Temporary infrastructure failures roll back incomplete changes and permit retry.
- The worker acknowledges the message after the database transaction commits.
- Repeated delivery for a confirmed or rejected order must not repeat inventory changes.

### Publishing events

- The publisher sends unpublished outbox events to RabbitMQ.
- published_at is set only after RabbitMQ confirms publication.
- A crash before recording published_at can cause the event to be published again.
- Workers must safely handle repeated delivery of the same event.
