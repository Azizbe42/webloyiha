from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # student / teacher

class UserLogin(BaseModel):
    username: str
    password: str

class ExamSubmit(BaseModel):
    answers: List[str]

class TextAnswer(BaseModel):
    text: str
