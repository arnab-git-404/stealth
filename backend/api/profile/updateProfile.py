from fastapi import APIRouter, Depends, HTTPException, status
from schemas.auth import UpdateProfileRequest
from db.mongo_client import doctors_collection
from utils.jwt_helper import verify_csrf, get_current_user
from utils.security import hash_password
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/update-profile",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_csrf)],
    summary="Update doctor profile"
)
def update_profile(
    payload: UpdateProfileRequest,
    user_email: str = Depends(get_current_user)
):
    existing_doctor = doctors_collection.find_one({"email": user_email})
    if not existing_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    update_data = {}

    if payload.fullName is not None:
        update_data["fullName"] = payload.fullName
    if payload.speciality is not None:
        update_data["speciality"] = payload.speciality
    if payload.practiceType is not None:
        update_data["practiceType"] = payload.practiceType
    if payload.yearsOfExperience is not None:
        update_data["yearsOfExperience"] = payload.yearsOfExperience
    if payload.organizationName is not None:
        update_data["organizationName"] = payload.organizationName
    if payload.phoneNumber is not None:
        update_data["phoneNumber"] = payload.phoneNumber
    if payload.password is not None:
        update_data["password_hash"] = hash_password(payload.password)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    result = doctors_collection.update_one(
        {"email": user_email},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        logger.warning(f"No profile fields updated for {user_email}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )

    logger.info(f"Profile updated successfully for {user_email}")
    return {"message": "Profile updated successfully"}
