Project Path: /home/varun/Code/School/SFSU/AITestExample/questions_bank

Source Tree:

```
questions_bank
├── controllers
│   ├── __init__.py
│   └── question_controller.py
├── __init__.py
├── services
│   ├── __init__.py
│   └── question_service.py
├── main.py
└── repos
    ├── question_repo.py
    └── __init__.py

```

`/home/varun/Code/School/SFSU/AITestExample/questions_bank/controllers/question_controller.py`:

```py
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



```

`/home/varun/Code/School/SFSU/AITestExample/questions_bank/services/question_service.py`:

```py
from typing import Optional
from questions_bank.repos.question_repo import repo


class QuestionService:
    def get_questions(self, tag: Optional[str] = None, n: Optional[int] = None):
        questions = repo.find_all()
        if tag:
            questions = [q for q in questions if tag in q["tags"]]
        if n:
            questions = questions[:n]
        return questions

    def get_question(self, question_id: int):
        return repo.find_by_id(question_id)

    def get_random_questions(self, n: int):
        return repo.find_random(n)

    def create_question(self, data: dict):
        return repo.save(data)

    def modify_question(self, question_id: int, data: dict):
        return repo.update(question_id, data)

    def delete_question(self, question_id: int):
        return repo.delete(question_id)

```

`/home/varun/Code/School/SFSU/AITestExample/questions_bank/main.py`:

```py
from fastapi import FastAPI
import uvicorn
from questions_bank.controllers import question_controller

app = FastAPI()
app.include_router(question_controller.router)


def main():
    # TODO: add reload param
    uvicorn.run("questions_bank.main:app", host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()

```

`/home/varun/Code/School/SFSU/AITestExample/questions_bank/repos/question_repo.py`:

```py
import random


class QuestionRepository:
    def __init__(self):
        self._db = {}
        self._id_counter = 1

    def find_all(self):
        return list(self._db.values())

    def find_by_id(self, question_id: int):
        return self._db.get(question_id)

    def find_random(self, n: int):
        questions = list(self._db.values())
        return random.sample(questions, min(n, len(questions)))

    def save(self, data: dict):
        q = {
            "id": self._id_counter,
            "text": data["text"],
            "choices": data["choices"],
            "answer": data["answer"],
            "tags": data.get("tags", []),
        }
        self._db[self._id_counter] = q
        self._id_counter += 1
        return q

    def update(self, question_id: int, data: dict):
        if question_id not in self._db:
            return None
        q = self._db[question_id]
        q.update(
            {
                "text": data["text"],
                "choices": data["choices"],
                "answer": data["answer"],
                "tags": data.get("tags", []),
            }
        )
        return q

    def delete(self, question_id: int):
        return self._db.pop(question_id, None)


repo = QuestionRepository()

```
