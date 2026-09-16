from sqlalchemy.orm import Session
from app.db.models import Engineer


def create_engineer(db: Session, engineer: Engineer) -> Engineer:
    db.add(engineer)
    db.commit()
    db.refresh(engineer)
    return engineer


def get_engineer(db: Session, engineer_id: int):
    return db.query(Engineer).filter(Engineer.id == engineer_id).first()


def get_engineers(db: Session):
    return db.query(Engineer).all()