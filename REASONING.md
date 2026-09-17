# REASONING

## How I Approached the Problem

I started by breaking the pharmacy problem into its main business requirements instead of trying to build everything at once.

The most important requirement was FEFO, or **First-Expiry-First-Out**. The pharmacy should always dispense the batch that expires soonest, while making sure that expired medicine can never be dispensed.

I therefore built the inventory and batch logic first and then added authentication, search, expiry automation, import handling, notifications, and the frontend around it.

---

## 1. Technology Choices

I used **FastAPI** for the backend because it makes it easy to create REST APIs and also provides Swagger documentation automatically.

For persistence, I chose **SQLite with SQLAlchemy**. SQLite was suitable for this project because it provides a real persistent database without requiring a separate database server. It also works well inside GitHub Codespaces.

For the frontend, I used regular **HTML, CSS, and JavaScript** rather than React. The application does not require a large frontend framework, and keeping the frontend simple allowed me to focus more on getting the inventory logic correct.

---

## 2. Database Design

I separated the application data into different tables.

### Users

The `users` table stores:

- User name
- Email
- Hashed password
- Account creation time

### Medicines

The `medicines` table stores:

- Medicine name
- Generic name
- Manufacturer
- Re-order threshold

### Batches

The `batches` table stores:

- Medicine ID
- Batch number
- Quantity
- Expiry date
- Batch status
- Expiry flag

A medicine can have multiple batches.

### Outbox

The `outbox` table stores re-order notification events.

This gives the application a simple structure:

```text
Medicine
   |
   └── Multiple Batches
          |
          ├── Quantity
          ├── Expiry Date
          └── Status