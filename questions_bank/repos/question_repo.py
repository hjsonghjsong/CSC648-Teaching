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
