import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .db.database import engine, Base
from .db import models
from .api import employees
from .api import engineers
from .api import tickets
from .core.exceptions import (
    DuplicateEmailException,
    EmployeeNotFoundException,
    EngineerNotFoundException,
    TicketNotFoundException
)
from .core.logging import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="IT Ticket Management System")

app.include_router(employees.router)
app.include_router(engineers.router)
app.include_router(tickets.router)


@app.exception_handler(EmployeeNotFoundException)
async def employee_not_found_handler(
    request: Request,
    exc: EmployeeNotFoundException
):
    logger.warning(
        "Employee not found: %s",
        str(exc)
    )

    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(EngineerNotFoundException)
async def engineer_not_found_handler(
    request: Request,
    exc: EngineerNotFoundException
):
    logger.warning(
        "Engineer not found: %s",
        str(exc)
    )

    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(DuplicateEmailException)
async def duplicate_email_handler(
    request: Request,
    exc: DuplicateEmailException
):
    logger.warning(
        "Duplicate email: %s",
        str(exc)
    )

    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )

@app.exception_handler(TicketNotFoundException)
async def ticket_not_found_handler(
    request: Request,
    exc: TicketNotFoundException
):
    logger.warning(
        "Ticket not found: %s",
        str(exc)
    )

    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


@app.exception_handler(ValueError)
async def value_error_handler(
    request: Request,
    exc: ValueError
):
    logger.warning(
        "Validation error: %s",
        str(exc)
    )

    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {"message": "IT Ticket Management System API is running"}