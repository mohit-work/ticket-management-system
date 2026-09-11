from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from .database import Base
from datetime import datetime


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False)

class Engineer(Base):
    __tablename__ = "engineers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    specialization = Column(String(100), nullable=False)

from sqlalchemy import ForeignKey, DateTime
from datetime import datetime


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    engineer_id = Column(Integer, ForeignKey("engineers.id"), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    category = Column(String(50), nullable=False)
    priority = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class TicketUpdate(Base):
    __tablename__ = "ticket_updates"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    engineer_id = Column(Integer, ForeignKey("engineers.id"), nullable=False)
    comment = Column(String(1000), nullable=False)
    old_status = Column(String(20), nullable=True)
    new_status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)