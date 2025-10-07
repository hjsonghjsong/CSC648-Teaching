from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from questions_bank.services.question_service import QuestionService

router = APIRouter(prefix="/questions", tags=["questions"])
service = QuestionService()


@router.get("/")
def get_questions(tag: Optional[str] = None, n: Optional[int] = None):
    """
    Get all questions with optional filtering.
    
    Input:
        tag (Optional[str]): Filter questions by tag. If provided, only questions containing this tag will be returned.
        n (Optional[int]): Limit the number of questions returned.
    
    Output:
        list: List of question dictionaries matching the criteria.
    """
    return service.get_questions(tag=tag, n=n)


@router.get("/random")
def get_random_questions(n: int = Query(1, ge=1)):
    """
    Get random questions from the database.
    
    Input:
        n (int): Number of random questions to retrieve. Must be >= 1. Defaults to 1.
    
    Output:
        list: List of randomly selected question dictionaries.
    """
    return service.get_random_questions(n=n)


@router.get("/{question_id}")
def get_question(question_id: int):
    """
    Get a specific question by ID.
    
    Input:
        question_id (int): The unique identifier of the question to retrieve.
    
    Output:
        dict: Question dictionary containing id, text, choices, answer, and tags.
    
    Raises:
        HTTPException: 404 error if question with the given ID is not found.
    """
    q = service.get_question(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@router.post("/")
def create_question(body: dict):
    """
    Create a new question.
    
    Input:
        body (dict): Question data containing:
            - text (str): The question text
            - choices (list): List of answer choices
            - answer (str): The correct answer
            - tags (list, optional): List of tags for categorization
    
    Output:
        dict: Newly created question with auto-generated ID.
    """
    return service.create_question(body)


@router.put("/{question_id}")
def modify_question(question_id: int, body: dict):
    """
    Modify an existing question.
    
    Input:
        question_id (int): The unique identifier of the question to modify.
        body (dict): Updated question data containing:
            - text (str): The question text
            - choices (list): List of answer choices
            - answer (str): The correct answer
            - tags (list, optional): List of tags for categorization
    
    Output:
        dict: Updated question dictionary.
    
    Raises:
        HTTPException: 404 error if question with the given ID is not found.
    """
    q = service.modify_question(question_id, body)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@router.delete("/{question_id}")
def delete_question(question_id: int):
    """
    Delete a question by ID.
    
    Input:
        question_id (int): The unique identifier of the question to delete.
    
    Output:
        dict: Status message confirming deletion {"status": "deleted"}.
    
    Raises:
        HTTPException: 404 error if question with the given ID is not found.
    """
    deleted = service.delete_question(question_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"status": "deleted"}
