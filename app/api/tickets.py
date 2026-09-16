from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.ticket import (
    TicketCreate,
    TicketResponse,
    TicketUpdateRequest,
    TicketUpdateResponse
)
from app.services import ticket_service

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    return ticket_service.create_ticket(
        db,
        ticket.employee_id,
        ticket.engineer_id,
        ticket.title,
        ticket.description,
        ticket.category,
        ticket.priority
    )


@router.get("/", response_model=list[TicketResponse])
def get_tickets(
    status: str | None = None,
    priority: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db)
):
    return ticket_service.get_tickets(
        db,
        status,
        priority,
        category
    )


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return ticket_service.get_ticket(db, ticket_id)


@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdateRequest,
    db: Session = Depends(get_db)
):
    return ticket_service.update_ticket(
        db,
        ticket_id,
        ticket.engineer_id,
        ticket.title,
        ticket.description,
        ticket.category,
        ticket.priority,
        ticket.status
    )


@router.get(
    "/{ticket_id}/updates",
    response_model=list[TicketUpdateResponse]
)
def get_ticket_updates(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    return ticket_service.get_ticket_updates(db, ticket_id)