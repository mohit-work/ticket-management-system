from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.engineer import EngineerCreate, EngineerResponse
from app.services import engineer_service

router = APIRouter(prefix="/engineers", tags=["Engineers"])


@router.post("/", response_model=EngineerResponse)
def create_engineer(engineer: EngineerCreate, db: Session = Depends(get_db)):
    return engineer_service.create_engineer(
        db,
        engineer.name,
        engineer.email,
        engineer.specialization
    )


@router.get("/", response_model=list[EngineerResponse])
def get_engineers(db: Session = Depends(get_db)):
    return engineer_service.get_engineers(db)


@router.get("/{engineer_id}", response_model=EngineerResponse)
def get_engineer(engineer_id: int, db: Session = Depends(get_db)):
    return engineer_service.get_engineer(db, engineer_id)