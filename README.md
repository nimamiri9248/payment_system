# Payment & Product Management System with Real-Time Notifications

This is a Django-based Payment and Product Management System featuring:

- **JWT Authentication** for secure user management.
- **CRUD APIs** for Products, Invoices, and Transactions.
- **MinIO** for scalable product image storage.
- **Django Channels & WebSockets** for real-time transaction status notifications.
- Basic unit tests for key functionalities.
- **PostgreSQL** as the database.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [WebSocket Usage](#websocket-usage)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [License](#license)

---

## Features

- User registration, login, profile management using JWT.
- Admin and user-level product management with image uploads to MinIO.
- Invoice and transaction management with permissions.
- Real-time notifications using WebSockets for transaction status updates.
- Basic unit tests for core functionalities.

---

## Requirements

- Python 3.12
- PostgreSQL
- Redis (for Channels layer)
- MinIO server

---

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nimamiri9248/payment_system.git
   cd payment_system
   ```

2. **Create a virtual environment** and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   # For Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**:
   - Create a database (e.g., `payment_db`) and update `core/settings.py` with your DB credentials.

5. **Apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Set up MinIO**:
   - Install and run MinIO, create a bucket as specified in `core/settings.py`.
   - Update `core/settings.py` with your MinIO credentials and bucket information.

8. **Ensure Redis is running**:
   - Install and run Redis on `localhost:6379` or update settings accordingly.

9. **Collect static files** (if needed):
   ```bash
   python manage.py collectstatic
   ```

---

## Configuration

- **JWT Settings**: Configured in `core/settings.py`. Adjust token lifetimes and refresh strategies as needed.
- **Channels & WebSockets**: Configured in `core/asgi.py`, `core/routing.py`, and `CHANNEL_LAYERS` in settings.
- **MinIO**: Configured via `django-storages` settings in `core/settings.py`.

---

## Running the Application

### Development with WebSockets Support

You can use the Django development server for **HTTP** requests and basic WebSocket testing:

```bash
python manage.py runserver
```

However, for more reliable WebSocket support, run using an ASGI server like **Daphne** or **Uvicorn**:

**Using Daphne:**
```bash
daphne -b 0.0.0.0 -p 8000 core.asgi:application
```

**Using Uvicorn:**
```bash
uvicorn core.asgi:application --host 0.0.0.0 --port 8000
```

Access the application at `http://localhost:8000/`.

---

## WebSocket Usage

To connect to real-time transaction updates for a user:

```js
const userId = 1; 
const socketUrl = `ws://${window.location.host}/ws/transactions/user/${userId}/`;
const socket = new WebSocket(socketUrl);

socket.onopen = () => console.log("Connected");
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Transaction update:", data);
};
socket.onerror = (error) => console.error("WebSocket error:", error);
socket.onclose = () => console.log("Disconnected");
```

Ensure that your server is running an ASGI server to handle WebSocket connections.

---

## API Endpoints

### Authentication (under `/accounts/`):
- `POST /accounts/register/` — Register a new user.
- `POST /accounts/login/` — Obtain JWT tokens.
- `GET /accounts/profile/` — Get user profile.
- `PATCH /accounts/profile/` — Update profile.
- `POST /accounts/logout/` — Logout and blacklist tokens (if configured).

### Products (under `/products/`):
- CRUD endpoints for products. Admin-only for create/update/delete.

### Invoices (under `/invoices/`):
- `GET /invoices/` — List invoices.
- `POST /invoices/` — Create a new invoice.
- CRUD operations on individual invoices at `/invoices/<id>/`.

### Transactions (under `/transactions/`):
- `POST /transactions/create/` — Register a transaction.
- `GET /transactions/` — List transaction history.
CRUD operations on individual transcations for admins at `/transactions/<id>/`.

---

## Running Tests

To run all tests:

```bash
python manage.py test
```

To run tests for a specific app:

```bash
python manage.py test accounts
python manage.py test products
python manage.py test invoices
python manage.py test transactions
```

---