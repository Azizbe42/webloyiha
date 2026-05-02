from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import jwt
import datetime

# ===== CONFIG =====
SECRET_KEY = "secret123"
ALGORITHM = "HS256"

# ===== DB (SQLITE - BEPUL) =====
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ===== MODELS =====
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)  # student / teacher

class ResultDB(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer)

Base.metadata.create_all(bind=engine)

# ===== APP =====
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ===== SCHEMAS =====
class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class ExamSubmit(BaseModel):
    answers: List[str]

class TextAnswer(BaseModel):
    text: str

# ===== DEPENDENCY =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== AUTH =====
def create_token(username):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str, db: Session):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(UserDB).filter(UserDB.username == data["sub"]).first()
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# ===== REGISTER =====
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(UserDB).filter(UserDB.username == user.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="User exists")

    db_user = UserDB(
        username=user.username,
        password=user.password,
        role=user.role
    )
    db.add(db_user)
    db.commit()

    return {"message": "Registered"}

# ===== LOGIN =====
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.username)

    return {"access_token": token}

# ===== EXAM =====
correct_answers = ["A", "C", "B", "D"]

@app.post("/submit")
def submit_exam(
    data: ExamSubmit,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    score = 0
    for i in range(len(correct_answers)):
        if i < len(data.answers) and data.answers[i] == correct_answers[i]:
            score += 1

    result = ResultDB(user_id=user.id, score=score)
    db.add(result)
    db.commit()

    return {"score": score, "total": len(correct_answers)}

# ===== ADMIN (TEACHER) =====
@app.get("/admin/results")
def admin_results(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Not allowed")

    results = db.query(ResultDB).all()

    return [{"user_id": r.user_id, "score": r.score} for r in results]

# ===== AI (BEPUL FAKE) =====
@app.post("/ai-check")
def ai_check(data: TextAnswer):
    keywords = ["ai", "python", "data", "machine"]
    score = sum(1 for k in keywords if k in data.text.lower())

    return {"response": f"AI baho: {score}/4"}

# ===== ROOT =====
@app.get("/")
def home():
    return {"status": "working 🚀"}
