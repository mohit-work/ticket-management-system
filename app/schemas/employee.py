from pydantic import BaseModel, ConfigDict, EmailStr


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str

    model_config = ConfigDict(from_attributes=True)