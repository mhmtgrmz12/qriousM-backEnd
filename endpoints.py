from fastapi import APIRouter, HTTPException, Query
import queries
from typing import Optional

router = APIRouter()

@router.get("/getQuestion")
def get_question(
    id: Optional[int] = Query(default=None),
    category: Optional[str] = Query(default=None),
    difficulty: Optional[str] = Query(default=None),
    type: Optional[str] = Query(default=None)
):

    type = type.strip() if type else None
    category = category.strip() if category else None
    difficulty = difficulty.strip() if difficulty else None

    question = queries.fetch_question(id, category, difficulty, type)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    response = {
        "id": question["id"],
        "type": question["type"],
        "question": question["question"],
        "choices": None
    }

    if question["type"] == "multipleChoice":
        choices = [question["choice1"], question["choice2"], question["choice3"], question["choice4"]]
        response["choices"] = [c for c in choices if c is not None]

    elif question["type"] == "true/false":
        response["choices"] = ["True", "False"]

    return response



@router.post("/checkAnswer")
def check_answer(id: int, answer: str):
    correct_answer = queries.get_correct_answer(id)
    if correct_answer is None:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = correct_answer.strip().lower() == answer.strip().lower()

    return {
        "correct": is_correct,
        "correctAnswer": correct_answer
    }
