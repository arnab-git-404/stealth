from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Literal, Optional, List
from enum import Enum

class PatientStatus(str, Enum):
    review = "review"
    billing = "billing"
    completed = "completed"

class Patient(BaseModel):
    patientId: str = Field(..., description="Unique patient identifier")
    doctorEmail: str = Field(..., description="Doctor's email")
    name: str
    age: int
    gender: str
    phone: Optional[str] = None
    history: List[str] = Field(default_factory=list, description="List of visit IDs")
    status: PatientStatus = Field(..., description="Patient status")
    created_at: datetime

    class Config:
        orm_mode = True

class Doctor(BaseModel):
    fullName: str = Field(..., min_length=2)
    email: str
    speciality: str
    practiceType: str
    yearsOfExperience: int = Field(..., ge=0, le=60)
    organizationName: str
    phoneNumber: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=8)

class ConsultationRequest(BaseModel):
    patientId: Optional[str] = None  
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=0, le=120)
    gender: Literal["Male", "Female", "Other"]
    phone: str = Field(..., min_length=10, max_length=15)
    audioUrl: str
    doctorEmail: str = Field(..., min_length=2)

class PatientResponse(BaseModel):
    id: Optional[str] 
    name: str
    age: int
    gender: str
    phone: str

    class Config:
        populate_by_name = True
        from_attributes = True
    
class CompleteProfileRequest(BaseModel):
    doctor: Doctor
    token : str

class VisitUpdate(BaseModel):
    transcript: Dict[str, str]

class VisitListItem(BaseModel):
    id: str
    date: datetime

class VisitResponse(BaseModel):
    id: str
    patientId: str
    date: datetime
    notes: list[str]
    transcription: list[str]

class PatientWithVisitsResponse(BaseModel):
    patient: PatientResponse
    visits: list[VisitListItem]

class PatientListItem(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    phone: Optional[str] = None
    visits: int
    lastVisit: Optional[datetime] = None
    status: PatientStatus

    class Config:
        orm_mode = True
