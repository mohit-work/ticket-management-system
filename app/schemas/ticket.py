from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class TicketCategory(str, Enum):
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    NETWORK = "Network"
    ACCESS = "Access"
    OTHER = "Other"


class TicketCreate(BaseModel):
    employee_id: int
    engineer_id: int | None = None
    title: str
    description: str
    category: TicketCategory
    priority: TicketPriority


class TicketResponse(BaseModel):
    id: int
    employee_id: int
    engineer_id: int | None
    title: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketUpdateRequest(BaseModel):
    engineer_id: int | None = None
    title: str | None = None
    description: str | None = None
    category: TicketCategory | None = None
    priority: TicketPriority | None = None
    status: TicketStatus | None = None


class TicketUpdateResponse(BaseModel):
    id: int
    ticket_id: int
    engineer_id: int
    comment: str
    old_status: TicketStatus | None
    new_status: TicketStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)