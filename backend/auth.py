import jwt
import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
import backend.models as models

SECRET = "secret"

def register(user, db: Session):
    db_user = models.User(
        username=user.username,
        password=user.password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    return {"msg": "registered"}

def login(user, db: Session):
    db_user = db.query(models.User).filter_by(username=user.username).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401)

    token = jwt.encode({"sub": user.username}, SECRET, algorithm="HS256")
    return {"access_token": token}

def get_current_user(token, db):
    data = jwt.decode(token, SECRET, algorithms=["HS256"])
    return db.query(models.User).filter_by(username=data["sub"]).first()

def submit_exam(user, data, db):
    correct = ["A","C","B","D"]

    score = sum(
        1 for i, a in enumerate(data.answers)
        if i < len(correct) and a == correct[i]
    )

    res = models.Result(user_id=user.id, score=score)
    db.add(res)
    db.commit()

    return {"score": score}
    
