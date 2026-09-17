# Pharmacy FEFO Manager

A full-stack pharmacy inventory management application built with FastAPI, SQLite, SQLAlchemy, JWT authentication, and a simple HTML/CSS/JavaScript frontend.

The application follows **FEFO (First-Expiry-First-Out)**. When medicine is dispensed, the batch with the earliest expiry date is used first. Expired and quarantined batches are never dispensed.

## Features

- User registration and login
- JWT-based authentication
- Medicine management
- Batch management
- FEFO dispensing
- Sellable in-date stock calculation
- Medicine search
- Pagination
- Sorting by name and stock
- Expiry alerts
- Daily expiry automation using `POST /clock`
- Automatic quarantine of expired batches
- Flagging batches expiring within 7 days
- Messy batch import
- Duplicate detection
- Invalid row rejection
- Re-order thresholds
- Re-order notification outbox
- Responsive dashboard
- Persistent SQLite database
- Swagger API documentation

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Authentication:** JWT
- **Password Hashing:** bcrypt
- **Frontend:** HTML, CSS, JavaScript
- **Templates:** Jinja2
- **Development Environment:** GitHub Codespaces

---

## Project Structure

```text
pharmacy-fefo/
│
├── README.md
├── REASONING.md
├── AI_LOGS.md
├── requirements.txt
├── pharmacy.db
├── .env
├── .gitignore
│
└── app/
    ├── __init__.py
    ├── auth.py
    ├── auth_routes.py
    ├── automation_routes.py
    ├── database.py
    ├── import_routes.py
    ├── main.py
    ├── medicine_routes.py
    ├── models.py
    ├── notification_routes.py
    ├── notification_service.py
    ├── schemas.py
    │
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   └── js/
    │       └── app.js
    │
    └── templates/
        └── index.html