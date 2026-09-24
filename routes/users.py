from fastapi import APIRouter, Request, Depends
from models.users import User, UserCreate, UserResponse
from database import get_session
from sqlmodel import Session, select
from auth import verify_api_key
from exceptions import NotFoundException, BadRequestException, InternalServerException

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    # make sure api key is valid
    if api_key != "my_api_key":
        raise BadRequestException("Invalid API key")

    # make sure the user doesn't already exist
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise BadRequestException("User with this email already exists")
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/", response_model=list[UserResponse])
def list_users(session: Session = Depends(get_session), description="List all users"):
    # get all users
    users = session.exec(select(User)).all()
    if not users:
        raise NotFoundException("No users found")
    return users
