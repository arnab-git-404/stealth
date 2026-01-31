from fastapi import APIRouter, HTTPException, status
from schemas.schema import Patient
from db.mongo_client import patients_collection, visits_collection
from utils.uniqueid import generate_patient_id
from datetime import datetime, timezone
from stt.transcribe import transcribe_audio_from_url
from stt.parse_transcription import parse_transcription_response
from llm.soap_generator import generate_soap_note

router = APIRouter(prefix="/visits", tags=["visits"])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create patient and visit record",
)
def create_visit(payload: Patient):
    existing_patient = patients_collection.find_one({"patientId": payload.patientId})

    if existing_patient:
        patient_id = existing_patient["patientId"]
    else:
        patient_id = generate_patient_id()
    
    try:
        patient_doc = {
            "patientId": patient_id,
            "doctorId": payload.doctorId,
            "name": payload.name,
            "age": payload.age,
            "gender": payload.gender,
            "phone": payload.phone,
            "history": [],
            "created_at": datetime.now(timezone.utc),
        }
        patient_result = patients_collection.insert_one(patient_doc)
        patient_mongo_id = patient_result.inserted_id
        transcript_url = payload.transcript
        transcription_raw = transcribe_audio_from_url(
            audio_url=transcript_url,
            language_code="eng",
            diarize=True,
            num_speakers=2,
        )
        full_text, transcription_final = parse_transcription_response(transcription_raw)
        notes = generate_soap_note(transcription_final)
        visit_doc = {
            "patientId": patient_id,
            #"transcript": payload.transcript, (previously used to store audio URL)
            "date": datetime.now(timezone.utc),
            "notes": notes
        }

        visit_result = visits_collection.insert_one(visit_doc)
        visit_id = visit_result.inserted_id

        
        patients_collection.update_one(
            {"_id": patient_mongo_id},
            {"$push": {"history": visit_id}}
        )

        return {
            "message": "Patient and visit created successfully",
            "patientId": patient_id,
            "visitId": str(visit_id),
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create visit: {str(e)}"
        )