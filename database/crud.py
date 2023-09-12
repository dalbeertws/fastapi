from sqlalchemy.orm import Session
from database.models import User, Post
from fastapi import HTTPException


def create_new_user(email: str, hashed_password: str, db: Session):
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def create_post(post: Post, user_id: int, db: Session):
    created_post = Post(
        name=post.name,
        description=post.description,
        user_id=user_id
    )
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post


def delete_post(post_id: Post, user: User, db: Session):
    post = db.query(Post).filter(Post.id == post_id).first()
    # Check if the post belongs to the user
    if not post or post.user_id != user.id:
        raise HTTPException(status_code=404, detail="Post not found or does not belong to the user")
    db.delete(post)
    db.commit()
    db.close()
