from sqlalchemy.orm import Session
from sql_app.models import User, UserToken, Post
from fastapi import HTTPException



# def create_user(email: str, hashed_password: str, db: Session):
def create_user(email:str,hashed_password: str, db: Session):
    print('$$$$$'*50)
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def get_user(token: str, db: Session):
    return db.query(UserToken).filter(UserToken.token == token).first().user

def save_user_token(user: User, access_token: str, db: Session):
    user_token = UserToken(
        access_token=access_token, 
        user=user)
    db.add(user_token)
    db.commit()
    db.refresh(user_token)
    return user_token

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

