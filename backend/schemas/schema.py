from pydantic import BaseModel, Field
from typing import Literal

class Doctor(BaseModel):
    email: str
    name: str = Field(..., min_length=2)
    specialty: str
    years_of_experience: int = Field(..., ge=0, le=60)
    organisation: str
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=8)


class Patient(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=0, le=120)
    gender: Literal["Male", "Female", "Other"]
    phone: str = Field(..., min_length=10, max_length=15)
    transcript: dict[str, str]
