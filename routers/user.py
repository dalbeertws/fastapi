from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sql_app.database import get_db
from sql_app.models import User

from sql_app.schemas import UserCreate, UserBase, UserToken
from sql_app.crud import create_user, save_user_token
from utils import get_password_hash, check_user_exists, create_jwt_token, verify_password


router = APIRouter(prefix='/users', tags=['user'])


@router.post('/signup', response_model=UserToken, status_code=status.HTTP_201_CREATED)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    user_exists = check_user_exists(db, user.email)
    if user_exists:
        raise HTTPException(status_code=400, detail="User with the email already exists")
    hashed_password =  get_password_hash(user.password)
    new_user = create_user( user.email,
                            hashed_password,
                            db)
    access_token = create_jwt_token(user.email, timedelta(minutes=15))
    save_user_token(new_user, access_token, db)
    return {"access_token": access_token}


@router.get('/user', response_model=UserBase)
def get_user(user: UserBase, db: Session = Depends(get_db)):
    return db.query(UserBase).filter(UserBase.email == user.email).first()
    

@router.post('/login', summary="Create access and refresh tokens for user")
async def login(user: UserCreate, db: Session = Depends(get_db)):
    user_exists = check_user_exists(db, user.email)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    user_obj = db.query(User).filter(User.email == user.email).first()
    if not verify_password(user.password, user_obj.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_jwt_token(user.email),
    }
