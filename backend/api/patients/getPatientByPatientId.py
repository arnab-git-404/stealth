from fastapi import APIRouter, HTTPException
from db.mongo_client import patients_collection, visits_collection
from schemas.schema import PatientWithVisitsResponse


router = APIRouter()


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

    visits_cursor = visits_collection.find(
        {"patientId": patient_id},
        {"date": 1}   
    )

    visits = []
    for v in visits_cursor:
        visits.append({
            "id": str(v["_id"]),
            "date": v.get("date")
        })

    return {"patient": patient_payload, "visits": visits}