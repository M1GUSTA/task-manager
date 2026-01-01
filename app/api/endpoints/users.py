from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schemas.user import UserCreate
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hash, verify_password
from app.dependencies.dependecies import get_user_service
from app.exceptions.exceptions import UsernameAlreadyExists
from app.services.user_service import UserService

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post("/sign_up")
async def sign_up_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    try:
        user = {"username": user.username, "email": user.email, "password": get_password_hash(user.password)}
        user = UserCreate(**user)

        if await user_service.add(user):
            return {"success": "User was created"}

    except UsernameAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username is already taken") from e


@user_router.post("/login")
async def login(
    user_service: UserService = Depends(get_user_service), form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        user = await user_service.find_by_username(form_data.username)
        if user:
            if verify_password(form_data.password, user.password):
                access_token = create_access_token(
                    data={"sub": form_data.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                )

                return {"access_token": access_token, "token_type": "bearer"}

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}") from e
