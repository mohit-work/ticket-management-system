from sqlalchemy.orm import Session
from app.db.models import Ticket, TicketUpdate


def create_ticket(db: Session, ticket: Ticket) -> Ticket:
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def get_ticket(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def get_tickets(
    db: Session,
    status: str | None = None,
    priority: str | None = None,
    category: str | None = None
):
    query = db.query(Ticket)

    if status is not None:
        query = query.filter(Ticket.status == status)

    if priority is not None:
        query = query.filter(Ticket.priority == priority)

    if category is not None:
        query = query.filter(Ticket.category == category)

    return query.all()


def update_ticket(db: Session, ticket: Ticket) -> Ticket:
    db.commit()
    db.refresh(ticket)
    return ticket


def create_ticket_update(
    db: Session,
    ticket_update: TicketUpdate
) -> TicketUpdate:
    db.add(ticket_update)
    db.commit()
    db.refresh(ticket_update)
    return ticket_update


def get_ticket_updates(db: Session, ticket_id: int):
    return (
        db.query(TicketUpdate)
        .filter(TicketUpdate.ticket_id == ticket_id)
        .order_by(TicketUpdate.created_at)
        .all()
    )