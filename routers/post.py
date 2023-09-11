from fastapi import APIRouter, Depends, status
from database.schemas import PostBase, PostCreateRes, UserPostsRes
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from database.crud import create_post, delete_post
from utils import get_current_user

router = APIRouter(prefix='/posts', tags=['post'])


@router.post("/", response_model=PostCreateRes, status_code=status.HTTP_201_CREATED)
def addPost(post: PostBase,  user=Depends(get_current_user), db: Session = Depends(get_db)): 
    user = db.query(User).filter(User.email == user).first()
    new_post = create_post(post, user.id, db)
    return {"id": new_post.id}


@router.get("/", response_model=UserPostsRes)
def getPosts(user=Depends(get_current_user),  db: Session=Depends(get_db)):
    user = db.query(User).filter(User.email == user).first()
    posts = db.query(User).filter(User.id == user.id).first().posts
    return {"posts": posts}


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(post_id: int, user=Depends(get_current_user),  db: Session=Depends(get_db),):
    user = db.query(User).filter(User.email == user).first()
    delete_post(post_id, user, db)
