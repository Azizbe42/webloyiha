from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
import backend.models as models
import backend.schemas as schemas
import backend.auth as auth
import backend.ai as ai

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== REGISTER =====
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth.register(user, db)

# ===== LOGIN =====
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return auth.login(user, db)

# ===== SUBMIT =====
@app.post("/submit")
def submit_exam(
    data: schemas.ExamSubmit,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = auth.get_current_user(token, db)
    return auth.submit_exam(user, data, db)

# ===== ADMIN =====
@app.get("/admin/results")
def admin_results(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = auth.get_current_user(token, db)

    if user.role != "teacher":
        raise HTTPException(status_code=403)

    return db.query(models.Result).all()

# ===== AI =====
@app.post("/ai-check")
def ai_check(data: schemas.TextAnswer):
    return {"response": ai.check(data.text)}

# ===== ROOT =====
@app.get("/")
def home():
    return {"status": "working 🚀"}
