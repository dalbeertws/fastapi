from typing import List
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserToken(BaseModel):
    access_token: str
    

class PostBase(BaseModel):
    name: str
    description: str


class PostCreateRes(BaseModel):
    id: int


class Posts(BaseModel):
    id: int
    name: str
    description: str


class UserPostsRes(BaseModel):
    posts: List[Posts]


class UserSignupRes(BaseModel):
    id: int
    email: EmailStr
