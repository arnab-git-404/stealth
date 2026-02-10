from fastapi import APIRouter, Response, Depends, status
from utils.jwt_helper import verify_csrf, get_current_user

router = APIRouter()


@router.post(
    "/logout",
    summary="Log out the user",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_csrf)],
)
def logout(
    response: Response,
    _: str = Depends(get_current_user),
):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/auth/refresh")
    response.delete_cookie("csrf_token", path="/")

    return {"message": "Logged out successfully"}
