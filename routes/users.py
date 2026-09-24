from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from auth import verify_api_key
from database import get_session
from exceptions import BadRequestException, NotFoundException
from models.users import User, UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, description="Create a new user")
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session),
    _: str = Depends(verify_api_key),
):
    existing_user = session.exec(
        select(User).where(User.email == user.email)
    ).first()
    if existing_user:
        raise BadRequestException(f"User with email '{user.email}' already exists")

    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/", response_model=list[UserResponse], description="List all users")
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    if not users:
        raise NotFoundException("No users found in the database")
    return users


@router.get("/{user_id}", response_model=UserResponse, description="Get user by ID")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise NotFoundException(f"User with ID {user_id} not found")
    return user