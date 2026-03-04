from fastapi import APIRouter, HTTPException, Query
from db.mongo_client import patients_collection, visits_collection
from schemas.schema import PatientListItem
from typing import List

router = APIRouter()

@router.get("/", response_model=List[PatientListItem])
def get_all_patients(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    try:
        cursor = (
            patients_collection
            .find({}, {"_id": 1, "name": 1, "age": 1, "gender": 1, "phone": 1, "status": 1, "patientId": 1})
            .skip(offset)
            .limit(limit)
        )
        patients = list(cursor)
        result = []
        for p in patients:
            patient_id = p.get("patientId")
            # Count visits
            visits_count = visits_collection.count_documents({"patientId": patient_id})
            # Get last visit date
            last_visit_doc = visits_collection.find({"patientId": patient_id}).sort("date", -1).limit(1)
            last_visit = None
            for v in last_visit_doc:
                last_visit = v.get("date")
            result.append({
                "id": str(p["_id"]),
                "name": p.get("name", ""),
                "age": p.get("age", 0),
                "gender": p.get("gender", ""),
                "phone": p.get("phone"),
                "visits": visits_count,
                "lastVisit": last_visit,
                "status": p.get("status", "review"),
            })
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve patients: {str(e)}"
        )