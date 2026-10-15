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
| name          | text      | Username                             |
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
