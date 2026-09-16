import logging

from sqlalchemy.orm import Session

from app.db.models import Ticket, TicketUpdate
from app.repositories import ticket_repository
from app.repositories import employee_repository
from app.repositories import engineer_repository
from app.core.exceptions import (
    EmployeeNotFoundException,
    EngineerNotFoundException,
    TicketNotFoundException
)

logger = logging.getLogger(__name__)


def create_ticket(
    db: Session,
    employee_id: int,
    engineer_id: int | None,
    title: str,
    description: str,
    category: str,
    priority: str
) -> Ticket:
    employee = employee_repository.get_employee(db, employee_id)

    if employee is None:
        raise EmployeeNotFoundException("Employee not found")

    if engineer_id is not None:
        engineer = engineer_repository.get_engineer(db, engineer_id)

        if engineer is None:
            raise EngineerNotFoundException("Engineer not found")

    ticket = Ticket(
        employee_id=employee_id,
        engineer_id=engineer_id,
        title=title,
        description=description,
        category=category,
        priority=priority,
        status="OPEN"
    )

    ticket = ticket_repository.create_ticket(db, ticket)

    logger.info("Ticket created: id=%s", ticket.id)

    return ticket


def get_ticket(db: Session, ticket_id: int):
    ticket = ticket_repository.get_ticket(db, ticket_id)

    if ticket is None:
        raise TicketNotFoundException("Ticket not found")

    logger.info("Ticket retrieved: id=%s", ticket_id)

    return ticket


def get_tickets(
    db: Session,
    status: str | None = None,
    priority: str | None = None,
    category: str | None = None
):
    tickets = ticket_repository.get_tickets(
        db,
        status,
        priority,
        category
    )

    logger.info(
        "Tickets retrieved: count=%s status=%s priority=%s category=%s",
        len(tickets),
        status,
        priority,
        category
    )

    return tickets


def update_ticket(
    db: Session,
    ticket_id: int,
    engineer_id: int | None = None,
    title: str | None = None,
    description: str | None = None,
    category: str | None = None,
    priority: str | None = None,
    status: str | None = None
) -> Ticket:
    ticket = ticket_repository.get_ticket(db, ticket_id)

    if ticket is None:
        raise TicketNotFoundException("Ticket not found")

    old_status = ticket.status

    if engineer_id is not None:
        engineer = engineer_repository.get_engineer(db, engineer_id)

        if engineer is None:
            raise EngineerNotFoundException("Engineer not found")

        ticket.engineer_id = engineer_id

    if title is not None:
        ticket.title = title

    if description is not None:
        ticket.description = description

    if category is not None:
        ticket.category = category

    if priority is not None:
        ticket.priority = priority

    if status is not None:
        allowed_transitions = {
            "OPEN": {"ASSIGNED"},
            "ASSIGNED": {"IN_PROGRESS"},
            "IN_PROGRESS": {"RESOLVED"},
            "RESOLVED": {"CLOSED"},
            "CLOSED": set()
        }

        status = status.value if hasattr(status, "value") else status

        if status not in allowed_transitions:
            raise ValueError("Invalid ticket status")

        if status not in allowed_transitions[ticket.status]:
            raise ValueError(
                f"Cannot change status from {ticket.status} to {status}"
            )

        ticket.status = status

        ticket_update = TicketUpdate(
            ticket_id=ticket.id,
            engineer_id=ticket.engineer_id,
            comment=f"Status changed from {old_status} to {status}",
            old_status=old_status,
            new_status=status
        )

        ticket_repository.create_ticket_update(db, ticket_update)

        logger.info(
            "Ticket status changed: id=%s old_status=%s new_status=%s",
            ticket.id,
            old_status,
            status
        )

    ticket = ticket_repository.update_ticket(db, ticket)

    logger.info("Ticket updated: id=%s", ticket.id)

    return ticket


def get_ticket_updates(db: Session, ticket_id: int):
    ticket = ticket_repository.get_ticket(db, ticket_id)

    if ticket is None:
        raise TicketNotFoundException("Ticket not found")

    updates = ticket_repository.get_ticket_updates(db, ticket_id)

    logger.info(
        "Ticket history retrieved: id=%s count=%s",
        ticket_id,
        len(updates)
    )

    return updates