import datetime
from fastapi import status, HTTPException, Depends, APIRouter
from ..schemas import UserCreate, UserLogin, UserOut
from sqlalchemy.orm import Session, query
from ..models import User
from ..database import get_db
from ..utils import hash_password, verify_password
from ..oauth2 import create_access_token, get_current_user
from ..db import add_blacklist_token


router = APIRouter()

# Create User


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash Password
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# User Login
# [Todos]
  # Locked user after 10 failed attempts


@router.post("/login")
def login(user_credentails: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username == user_credentails.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            "message": "unauthorized", "description": "invalid credentails"})
    is_valid = verify_password(user_credentails.password, user.password)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            "message": "unauthorized", "description": "invalid credentails"})
    # Create Token
    access_token = create_access_token(data={"user_id": user.id})
    # Return token
    return {"access_token": access_token, "token_type": "bearer"}

# User Checkin


@router.put("/checkin", status_code=status.HTTP_200_OK)
async def checkin(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    db.query(User).filter(User.id == user_id.id).update(
        {"checkin": datetime.datetime.now()})
    db.commit()
    return
# Check User Status


@router.get('/active/{id}', status_code=status.HTTP_200_OK)
async def get_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    user = db.query(User).filter(
        User.id == id).first()

    day = user.checkin.day
    total_seconds = user.checkin.second + \
        (user.checkin.minute * 60) + ((user.checkin.hour * 60) * 60)

    time_now = datetime.datetime.now()
    time_now_day = time_now.day
    diff_day = time_now_day - day

    time_now_total_seconds = time_now.second + \
        (time_now.minute * 60) + ((time_now.hour * 60) * 60) + \
        (diff_day * 24 * 60 * 60)
    diff_time = round((time_now_total_seconds - total_seconds) / 60)
    print(diff_time)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": "user id not found"})
    if diff_time > 5:
        return {"is_active": False}
    return {"is_active": "true"}


# Log out user
@ router.post('/logout')
def logout(token: str = Depends(get_current_user)):
    if add_blacklist_token(token):
        return {"log out"}
