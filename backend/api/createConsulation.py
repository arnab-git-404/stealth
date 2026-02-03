from fastapi import APIRouter, HTTPException, status, Depends
from schemas.schema import Patient
from db.mongo_client import patients_collection, visits_collection
from utils.uniqueid import generate_patient_id
from datetime import datetime, timezone
from utils.jwt_helper import verify_csrf, get_current_user
from stt.transcribe import transcribe_audio_from_url
from stt.parse_transcription import parse_transcription_response
from llm.soap_generator import generate_soap_note
import logging

router = APIRouter(prefix="/visits", tags=["visits"])
logger = logging.getLogger(__name__)


@router.post(
    "/create-consultation",
    status_code=status.HTTP_201_CREATED,
    summary="Create patient and visit record",
    dependencies=[Depends(verify_csrf)],
)
def create_consultation(
    payload: Patient,
    user_email: str = Depends(get_current_user),
):
    try:
        existing_patient = patients_collection.find_one(
            {"patientId": payload.patientId, "doctorEmail": user_email}
        )

        if existing_patient:
            patient_id = existing_patient["patientId"]
            patient_mongo_id = existing_patient["_id"]
        else:
            patient_id = generate_patient_id()
            patient_doc = {
                "patientId": patient_id,
                "doctorEmail": user_email,
                "name": payload.name,
                "age": payload.age,
                "gender": payload.gender,
                "phone": payload.phone,
                "history": [],
                "created_at": datetime.now(timezone.utc),
            }
            patient_result = patients_collection.insert_one(patient_doc)
            patient_mongo_id = patient_result.inserted_id

        transcription_raw = transcribe_audio_from_url(
            audio_url=payload.audioUrl,
            language_code="eng",
            diarize=True,
            num_speakers=2,
        )

        full_text, parsed_transcription = parse_transcription_response(
            transcription_raw
        )
        notes = generate_soap_note(parsed_transcription)

        visit_doc = {
            "patientId": patient_id,
            "date": datetime.now(timezone.utc),
            "notes": notes,
            "transcription": parsed_transcription,
        }

        visit_result = visits_collection.insert_one(visit_doc)
        visit_id = visit_result.inserted_id
        patients_collection.update_one(
            {"_id": patient_mongo_id},
            {"$push": {"history": visit_id}},
        )

        logger.info(
            f"Visit created for patient {patient_id} by doctor {user_email}"
        )

        return {
            "message": "Patient and visit created successfully",
            "patientId": patient_id,
            "visitId": str(visit_id),
            "patient": patient_doc if not existing_patient else existing_patient,
            "visit": visit_doc,
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Failed to create visit")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create visit",
        )
