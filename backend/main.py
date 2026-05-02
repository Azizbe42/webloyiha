from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Fake database
correct_answers = ["A", "C", "B", "D"]

class ExamSubmit(BaseModel):
    answers: List[str]

@app.get("/")
def home():
    return {"message": "Exam system working"}

@app.post("/submit")
def submit_exam(data: ExamSubmit):
    score = 0

    for i in range(len(correct_answers)):
        if i < len(data.answers) and data.answers[i] == correct_answers[i]:
            score += 1

    return {
        "score": score,
        "total": len(correct_answers),
        "percentage": int(score / len(correct_answers) * 100)
    }
