from sqlalchemy.orm import Session

from app.db.models import Employee
from app.repositories import employee_repository
from app.core.exceptions import (
    DuplicateEmailException,
    EmployeeNotFoundException
)


def create_employee(
    db: Session,
    name: str,
    email: str,
    department: str
) -> Employee:
    existing_employee = db.query(Employee).filter(
        Employee.email == email
    ).first()

    if existing_employee is not None:
        raise DuplicateEmailException("Email already exists")

    employee = Employee(
        name=name,
        email=email,
        department=department
    )

    return employee_repository.create_employee(db, employee)


def get_employee(db: Session, employee_id: int):
    employee = employee_repository.get_employee(db, employee_id)

    if employee is None:
        raise EmployeeNotFoundException("Employee not found")

    return employee


def get_employees(db: Session):
    return employee_repository.get_employees(db)