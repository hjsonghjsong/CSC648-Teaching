from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from questions_bank.services.question_service import QuestionService

router = APIRouter(prefix="/questions", tags=["questions"])
service = QuestionService()


@router.get("/")
def get_questions(tag: Optional[str] = None, n: Optional[int] = None):
    return service.get_questions(tag=tag, n=n)


@router.get("/random")
def get_random_questions(n: int = Query(1, ge=1)):
    return service.get_random_questions(n=n)


@router.get("/{question_id}")
def get_question(question_id: int):
    q = service.get_question(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@router.post("/")
def create_question(body: dict):
    return service.create_question(body)


@router.put("/{question_id}")
def modify_question(question_id: int, body: dict):
    q = service.modify_question(question_id, body)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@router.delete("/{question_id}")
def delete_question(question_id: int):
    deleted = service.delete_question(question_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"status": "deleted"}
