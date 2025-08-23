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
