from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, auth, ai

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

# ===== SUBMIT EXAM =====
@app.post("/submit")
def submit_exam(data: schemas.ExamSubmit, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = auth.get_current_user(token, db)
    return auth.submit_exam(user, data, db)

# ===== ADMIN =====
@app.get("/admin/results")
def admin_results(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = auth.get_current_user(token, db)
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Not allowed")
    return db.query(models.Result).all()

# ===== AI =====
@app.post("/ai-check")
def ai_check(data: schemas.TextAnswer):
    return {"response": ai.check(data.text)}
    
