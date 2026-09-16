# IT Ticket Management System

A modular backend service for managing IT helpdesk tickets using FastAPI, PostgreSQL, SQLAlchemy, Pydantic, and pytest.

## Features

* Employee management
* Engineer management
* IT ticket creation and retrieval
* Ticket updates
* Ticket status workflow
* Ticket update history
* Ticket filtering by status, priority, and category
* Request and response validation
* Foreign-key validation
* Duplicate email handling
* Consistent HTTP error responses
* Structured application logging
* Automated API tests
* PostgreSQL test database
* SQL schema and example queries
* OpenAPI API documentation

## Technology Stack

* Python 3.14
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* pytest
* pytest-cov
* Uvicorn

## Project Structure

```text
ticket-management-system/
├── app/
│   ├── api/
│   │   ├── employees.py
│   │   ├── engineers.py
│   │   └── tickets.py
│   ├── core/
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   ├── repositories/
│   │   ├── employee_repository.py
│   │   ├── engineer_repository.py
│   │   └── ticket_repository.py
│   ├── schemas/
│   │   ├── employee.py
│   │   ├── engineer.py
│   │   └── ticket.py
│   ├── services/
│   │   ├── employee_service.py
│   │   ├── engineer_service.py
│   │   └── ticket_service.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   └── test_tickets.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Architecture

The application follows a layered backend architecture:

```text
Client
   ↓
FastAPI API Layer
   ↓
Service Layer
   ↓
Repository Layer
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

### API Layer

Handles HTTP requests, dependency injection, request validation, and response models.

### Service Layer

Contains business logic such as ticket status transitions, foreign-key validation, and duplicate-email checks.

### Repository Layer

Handles database operations and keeps database-access logic separate from business logic.

### Database Layer

Contains SQLAlchemy models and PostgreSQL database configuration.

### Core Layer

Contains application exceptions and structured logging configuration.

## Database Model

The system contains four main tables:

### Employees

Stores employees who create IT tickets.

### Engineers

Stores engineers who handle tickets.

### Tickets

Stores the main IT helpdesk tickets.

Ticket lifecycle:

```text
OPEN
  ↓
ASSIGNED
  ↓
IN_PROGRESS
  ↓
RESOLVED
  ↓
CLOSED
```

### Ticket Updates

Stores the history of ticket status changes and engineer comments.

Relationships:

```text
Employee 1 ──── N Ticket

Engineer 1 ──── N Ticket

Ticket 1 ──── N TicketUpdate
```

## Configuration

Create a `.env` file in the project root.

Example:

```text
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ticket_management
TEST_DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ticket_management_test
```

Do not commit `.env` because it contains database credentials.

Use `.env.example` as the configuration template.

## Installation

Create and activate the virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

## API Endpoints

### Employees

| Method | Endpoint          | Description        |
| ------ | ----------------- | ------------------ |
| POST   | `/employees/`     | Create an employee |
| GET    | `/employees/`     | Get all employees  |
| GET    | `/employees/{id}` | Get an employee    |

### Engineers

| Method | Endpoint          | Description        |
| ------ | ----------------- | ------------------ |
| POST   | `/engineers/`     | Create an engineer |
| GET    | `/engineers/`     | Get all engineers  |
| GET    | `/engineers/{id}` | Get an engineer    |

### Tickets

| Method | Endpoint                | Description        |
| ------ | ----------------------- | ------------------ |
| POST   | `/tickets/`             | Create a ticket    |
| GET    | `/tickets/`             | Get tickets        |
| GET    | `/tickets/{id}`         | Get a ticket       |
| PUT    | `/tickets/{id}`         | Update a ticket    |
| GET    | `/tickets/{id}/updates` | Get ticket history |

Tickets can be filtered using query parameters:

```text
/tickets/?status=OPEN
/tickets/?priority=HIGH
/tickets/?category=Network
/tickets/?status=OPEN&priority=HIGH
```

## Validation and Error Handling

The API validates request data using Pydantic.

Examples:

* Invalid enum values → HTTP 422
* Missing employee → HTTP 404
* Missing engineer → HTTP 404
* Missing ticket → HTTP 404
* Invalid ticket status transition → HTTP 400
* Duplicate employee/engineer email → HTTP 409

Errors use a consistent response structure:

```json
{
  "detail": "Error message"
}
```

## Testing

Run the complete test suite:

```powershell
pytest -v
```

Current test suite:

```text
22+ automated tests
```

Run tests with coverage:

```powershell
pytest --cov=app --cov-report=term-missing
```

The current test suite achieves approximately **95% application coverage**.

## SQL Scripts

`sql/schema.sql` contains the relational database schema.

`sql/queries.sql` contains examples of:

* JOIN queries
* Common Table Expressions (CTEs)
* Window functions
* Transactions

## Development Workflow

The project uses a feature-branch workflow.

Example:

```text
master
   ↓
feature/complete-ticket-management
   ↓
development and testing
   ↓
commit
   ↓
pull request
   ↓
merge
```

Current feature branch:

```text
feature/complete-ticket-management
```

## Security and Configuration

Database credentials are stored in `.env` and excluded from source control.

The repository contains `.env.example` so another developer can configure the application without exposing credentials.

## Current Test Result

The application currently passes the complete automated test suite:

```text
23 passed
95% coverage
```
