from fastapi import APIRouter, HTTPException
from db.mongo_client import patients_collection, visits_collection
from schemas.schema import PatientWithVisitsResponse


router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/{patient_id}", response_model=PatientWithVisitsResponse)
def get_patient(patient_id: str):
    patient = patients_collection.find_one({"patientId": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient["id"] = str(patient.pop("_id"))

    patient_payload = {
        "id": patient.get("id"),
        "name": patient.get("name"),
        "age": patient.get("age"),
        "gender": patient.get("gender"),
        "phone": patient.get("phone"),
    }

    visits_cursor = visits_collection.find({
        "$or": [
            {"patientId": patient_id},
        ]
    })

    visits = list(visits_cursor)

    for v in visits:
        v["id"] = str(v.pop("_id"))

    return {"patient": patient_payload, "visits": visits}


