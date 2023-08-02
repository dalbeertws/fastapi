from fastapi import APIRouter, Depends, status
from sql_app.schemas import PostBase, PostCreateRes, UserPostsRes
from sqlalchemy.orm import Session
from sql_app.database import get_db
from sql_app.models import User
from sql_app.crud import create_post
from utils import get_current_user


router = APIRouter(prefix='/posts', tags=['post'])


@router.post("/", response_model=PostCreateRes, status_code=status.HTTP_201_CREATED)
def add_post(post: PostBase,  user = Depends(get_current_user),  db: Session  = Depends(get_db)): 
    user = db.query(User).filter(User.email == user).first()
    new_post = create_post(post, user.id, db)
    return {"id": new_post.id}


@router.get("/", response_model=UserPostsRes)
def get_posts( user = Depends(get_current_user),  db: Session  = Depends(get_db)):
   user = db.query(User).filter(User.email == user).first()
   posts =  db.query(User).filter(User.id == user.id).first().posts
   return {"posts": posts}
