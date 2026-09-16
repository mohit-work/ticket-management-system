from pydantic import BaseModel, ConfigDict, EmailStr


class EngineerCreate(BaseModel):
    name: str
    email: EmailStr
    specialization: str


class EngineerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    specialization: str

    model_config = ConfigDict(from_attributes=True)