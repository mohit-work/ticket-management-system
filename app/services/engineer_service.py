from sqlalchemy.orm import Session

from app.db.models import Engineer
from app.repositories import engineer_repository
from app.core.exceptions import (
    DuplicateEmailException,
    EngineerNotFoundException
)


def create_engineer(
    db: Session,
    name: str,
    email: str,
    specialization: str
) -> Engineer:
    existing_engineer = db.query(Engineer).filter(
        Engineer.email == email
    ).first()

    if existing_engineer is not None:
        raise DuplicateEmailException("Email already exists")

    engineer = Engineer(
        name=name,
        email=email,
        specialization=specialization
    )

    return engineer_repository.create_engineer(db, engineer)


def get_engineer(db: Session, engineer_id: int):
    engineer = engineer_repository.get_engineer(db, engineer_id)

    if engineer is None:
        raise EngineerNotFoundException("Engineer not found")

    return engineer


def get_engineers(db: Session):
    return engineer_repository.get_engineers(db)