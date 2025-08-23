from questions_bank.repos.question_repo import QuestionRepository


def test_save_and_find():
    repo = QuestionRepository()
    q = repo.save(
        {"text": "What is 2+2?", "choices": ["3", "4"], "answer": "4", "tags": ["math"]}
    )
    assert q["id"] == 1
    assert repo.find_by_id(1)["answer"] == "4"
