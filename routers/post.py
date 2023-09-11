from fastapi import APIRouter, Depends, status
from database.schemas import PostBase, PostCreateRes, UserPostsRes
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from database.crud import create_post, delete_post
from utils import get_current_user
from cachetools import TTLCache


router = APIRouter(prefix='/posts', tags=['post'])
cache = TTLCache(maxsize=100, ttl=300)


@router.post("/", response_model=PostCreateRes, status_code=status.HTTP_201_CREATED)
def addPost(post: PostBase,  user=Depends(get_current_user), db: Session=Depends(get_db)): 
    new_post = create_post(post, user.id, db)
    cache_key = f"getPosts_{user.id}"
    if cache_key in cache:
        del cache[cache_key]
    return {"id": new_post.id}


@router.get("/", response_model=UserPostsRes)
def getPosts(user=Depends(get_current_user), db: Session = Depends(get_db)):
    cache_key = f"getPosts_{user.id}"
    # Check if the response is already cached
    cached_response = cache.get(cache_key)
    if cached_response:
        print('CACHEEEEEEEEEEEEEE')
        return cached_response
    print('NOTTTTTTTTTTTTTTTT')
    # If not cached, retrieve the data and cache it
    posts = db.query(User).filter(User.id == user.id).first().posts
    response = {"posts": posts}
    cache[cache_key] = response
    return response


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(post_id: int, user=Depends(get_current_user),  db: Session=Depends(get_db)):
    delete_post(post_id, user, db)
