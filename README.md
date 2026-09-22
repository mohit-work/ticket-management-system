# IT Ticket Management System

A modular enterprise-style IT helpdesk backend and data pipeline built with FastAPI, PostgreSQL, SQLAlchemy, Pandas, PySpark, pytest, and Docker.

The project was developed in two stages:

- Week 1: REST backend and relational data layer
- Week 2: Repeatable enterprise data pipeline

## Features

### Backend

- Employee management
- Engineer management
- IT ticket creation and retrieval
- Ticket updates
- Ticket status workflow
- Ticket update history
- Ticket filtering by status, priority, and category
- Request and response validation
- Foreign-key validation
- Duplicate email handling
- Consistent HTTP error responses
- Structured application logging
- OpenAPI documentation
- PostgreSQL persistence
- Automated API tests

### Data Pipeline

- CSV ingestion
- JSON ingestion
- Parquet ingestion
- PostgreSQL table ingestion
- REST API ingestion
- Source schema/data contracts
- Schema versioning
- Data profiling
- Completeness checks
- Uniqueness checks
- Validity checks
- Referential integrity validation
- Rejected-record quarantine
- Source-to-target reconciliation
- Raw, standardized, and curated layers
- Batch audit manifest
- Content-based batch identification
- Incremental processing
- Idempotent reruns
- Pandas transformations
- PySpark transformations
- Dockerized execution

## Technology Stack

- Python 3.12+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Pandas
- PySpark
- PyArrow
- pytest
- pytest-cov
- Uvicorn
- Docker

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
│   ├── pipeline/
│   │   ├── cli.py
│   │   ├── contracts.py
│   │   ├── quality.py
│   │   ├── runner.py
│   │   ├── sources.py
│   │   ├── spark_transform.py
│   │   └── transform.py
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
├── data/
│   └── input/
├── tests/
│   ├── conftest.py
│   ├── test_tickets.py
│   └── test_pipeline.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
## Architecture
Backend Architecture
Client
   |
   v
FastAPI API Layer
   |
   v
Service Layer
   |
   v
Repository Layer
   |
   v
SQLAlchemy
   |
   v
PostgreSQL
Data Pipeline Architecture
CSV / JSON / Parquet / PostgreSQL / REST API
                    |
                    v
                  Raw
                    |
                    v
        Schema validation + profiling
                    |
                    v
             Standardized
                    |
                    v
       Transform + join + validation
                    |
             +------+------+
             |             |
             v             v
          Curated       Rejected
             |             |
             +------+------+
                    |
                    v
             Audit Manifest
## Database Model

The system contains four main tables:

Employees

Stores employees who create IT tickets.

Engineers

Stores engineers who handle IT tickets.

Tickets

Stores the main IT helpdesk tickets.

Ticket lifecycle:

OPEN
  |
  v
ASSIGNED
  |
  v
IN_PROGRESS
  |
  v
RESOLVED
  |
  v
CLOSED
### Ticket Updates

Stores ticket status-change history and engineer comments.

Relationships:

Employee 1 ───── N Ticket

Engineer 1 ───── N Ticket

Ticket 1 ─────── N TicketUpdate
## Configuration

Create a .env file in the project root.

Example:

DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ticket_management

Do not commit .env because it contains database credentials.

Use `.env.example` as the configuration template.

## Installation

Create and activate the virtual environment:

python -m venv .venv
.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
## Running the Backend

Start the FastAPI server:

uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000
## API Documentation

FastAPI automatically generates interactive documentation.

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

OpenAPI specification:

http://127.0.0.1:8000/openapi.json
## API Endpoints
### Employees
Method	Endpoint	Description
POST	/employees/	Create an employee
GET	/employees/	Get all employees
GET	/employees/{id}	Get an employee
### Engineers
Method	Endpoint	Description
POST	/engineers/	Create an engineer
GET	/engineers/	Get all engineers
GET	/engineers/{id}	Get an engineer
### Tickets
Method	Endpoint	Description
POST	/tickets/	Create a ticket
GET	/tickets/	Get tickets
GET	/tickets/{id}	Get a ticket
PUT	/tickets/{id}	Update a ticket
GET	/tickets/{id}/updates	Get ticket history

Tickets can be filtered using query parameters:

/tickets/?status=OPEN
/tickets/?priority=HIGH
/tickets/?category=Network
/tickets/?status=OPEN&priority=HIGH
## Validation and Error Handling

The API validates request data using Pydantic.

Examples:

Invalid enum values → HTTP 422
Missing employee → HTTP 404
Missing engineer → HTTP 404
Missing ticket → HTTP 404
Invalid ticket status transition → HTTP 400
Duplicate employee/engineer email → HTTP 409

Errors use a consistent response structure:

{
  "detail": "Error message"
}
## Enterprise Data Pipeline

The Week 2 pipeline ingests case records, employee reference data, and policy metadata from heterogeneous sources.

The default run reads cases from `cases.csv`, employees from `employees.json`, and policies from `policies.csv`. Individual sources can also be read from the following formats:

CSV
JSON
Parquet
- PostgreSQL `tickets` table for the cases source
- REST API for the policies source
## Data Contracts

Data contracts are defined in:

app/pipeline/contracts.py

The contracts define:

Required columns
Unique keys
Contract name
Contract version

Current contract version:

1.0
## Data Quality

The pipeline performs:

Completeness checks
Required-value validation
Duplicate-key detection
Priority validity checks
Status validity checks
Referential integrity validation
Distribution profiling

Invalid records are written to:

data/output/<batch_id>/rejected/records.csv

Each rejected record includes a rejection reason.

## Pipeline Outputs

For each batch:

data/output/<batch_id>/
├── raw/
│   ├── cases.csv
│   ├── employees.csv
│   └── policies.csv
├── standardized/
│   ├── cases.csv
│   ├── employees.csv
│   └── policies.csv
├── curated/
│   └── cases.csv
├── rejected/
│   └── records.csv
└── manifest.json

The manifest contains:

Batch ID
Start and finish timestamps
Source row counts
Standardized row counts
Curated row count
Rejected row count
Skipped row count
Reconciliation result
Contract versions
Data-quality metrics
## Running the Pipeline Locally

Run the default file-based pipeline:

python -m app.pipeline.cli
### REST API ingestion

The policy source can be replaced with a REST endpoint returning either a JSON array or:

{
  "data": []
}

Example using an external policy endpoint:

python -m app.pipeline.cli --api-url http://localhost:8000/policies_api.json
### PostgreSQL ingestion

The cases source can be read from the PostgreSQL tickets table:

python -m app.pipeline.cli --database-url "postgresql://postgres:postgres@localhost:5432/ticket_management"
### Incremental processing

Incremental mode tracks previously processed case IDs:

python -m app.pipeline.cli --incremental

Repeated execution of the same input skips previously processed cases.

The state is maintained in:

data/output/state/processed_cases.csv
## PySpark Transformations

Reusable PySpark transformations are implemented in:

app/pipeline/spark_transform.py

The module demonstrates:

Filtering
Joins
Aggregation
Window functions
Deduplication
Null handling
## Docker

Build the image:
docker build -t ticket-management-pipeline .
Run the pipeline:
docker run --rm -v "${PWD}/data:/app/data" ticket-management-pipeline

The container uses:

INPUT_DIR=data/input
OUTPUT_DIR=data/output

The data directory is mounted so pipeline outputs remain available on the host.

## Testing

Run the complete test suite:

pytest -q

Run tests with coverage:

pytest --cov=app --cov-report=term-missing

The test suite covers:

REST API behavior
Validation
Error handling
Repository and service logic
Pipeline ingestion
Data-quality validation
Transformations
Incremental processing
PostgreSQL ingestion
PySpark transformations
## SQL Scripts

sql/schema.sql contains the relational database schema.

sql/queries.sql contains examples of:

JOIN queries
Common Table Expressions (CTEs)
Window functions
Transactions
## Development Workflow

The project uses a feature-branch workflow:

master
   |
   v
feature/complete-ticket-management
   |
   v
Development and testing
   |
   v
Commit
   |
   v
Pull Request
   |
   v
Merge

Current development branch:

feature/complete-ticket-management
## Security and Configuration

Database credentials are stored in .env and excluded from source control.

The repository contains .env.example so another developer can configure the application without exposing credentials.

.dockerignore excludes:

.env
.venv
.git
__pycache__
.pytest_cache
.coverage
data/output