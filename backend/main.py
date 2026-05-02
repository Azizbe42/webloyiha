from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.security import OAuth2PasswordBearer
import jwt
import datetime

# ====== CONFIG ======
SECRET_KEY = "secret123"
ALGORITHM = "HS256"

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ====== FAKE DATABASE ======
users_db = {}
results_db = []

correct_answers = ["A", "C", "B", "D"]

# ====== MODELS ======
class User(BaseModel):
    username: str
    password: str

class ExamSubmit(BaseModel):
    answers: List[str]

class TextAnswer(BaseModel):
    text: str

# ====== AUTH ======
def create_token(username):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# ====== REGISTER ======
@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User exists")
    
    users_db[user.username] = user.password
    return {"message": "Registered"}

# ====== LOGIN ======
@app.post("/login")
def login(user: User):
    if users_db.get(user.username) != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.username)
    return {"access_token": token}

# ====== EXAM ======
@app.post("/submit")
def submit_exam(data: ExamSubmit, user=Depends(get_current_user)):
    score = 0

    for i in range(len(correct_answers)):
        if i < len(data.answers) and data.answers[i] == correct_answers[i]:
            score += 1

    result = {
        "user": user,
        "score": score,
        "total": len(correct_answers)
    }

    results_db.append(result)

    return result

# ====== ADMIN PANEL ======
@app.get("/admin/results")
def admin_results(user=Depends(get_current_user)):
    if user != "admin":
        raise HTTPException(status_code=403, detail="Not admin")

    return {"results": results_db}

# ====== AI MODULE (REAL OPENAI) ======
from openai import OpenAI
client = OpenAI()

@app.post("/ai-check")
def ai_check(data: TextAnswer):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": data.text}]
    )

    return {
        "ai_response": res.choices[0].message.content
    }

# ====== HOME ======
@app.get("/")
def home():
    return {"status": "working"}
