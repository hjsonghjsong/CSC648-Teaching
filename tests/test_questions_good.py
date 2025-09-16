import pytest
from fastapi.testclient import TestClient
from questions_bank.main import app
from questions_bank.repos import question_repo

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_repo():
    # Reset repo state before each test
    question_repo.repo._db.clear()
    question_repo.repo._id_counter = 1


def make_question(text="What is 2+2?", choices=None, answer="4", tags=None):
    return {
        "text": text,
        "choices": choices or ["1", "2", "3", "4"],
        "answer": answer,
        "tags": tags or ["math"],
    }


def test_create_and_get_question():
    # Create a question
    resp = client.post("/questions/", json=make_question())
    assert resp.status_code == 200
    q = resp.json()
    assert q["id"] == 1
    assert q["answer"] == "4"

    # Retrieve the same question
    resp = client.get("/questions/1")
    assert resp.status_code == 200
    q2 = resp.json()
    assert q2["id"] == 1
    assert q2["text"] == "What is 2+2?"


def test_get_nonexistent_question():
    resp = client.get("/questions/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Question not found"


def test_modify_question():
    q = client.post("/questions/", json=make_question()).json()
    resp = client.put(
        f"/questions/{q['id']}",
        json=make_question(text="Updated?", answer="42", tags=["logic"]),
    )
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["text"] == "Updated?"
    assert updated["answer"] == "42"
    assert updated["tags"] == ["logic"]


def test_modify_nonexistent_question():
    resp = client.put("/questions/123", json=make_question())
    assert resp.status_code == 404


def test_delete_question():
    q = client.post("/questions/", json=make_question()).json()
    resp = client.delete(f"/questions/{q['id']}")
    assert resp.status_code == 200
    assert resp.json() == {"status": "deleted"}

    # Verify it's gone
    resp = client.get(f"/questions/{q['id']}")
    assert resp.status_code == 404


def test_delete_nonexistent_question():
    resp = client.delete("/questions/999")
    assert resp.status_code == 404


def test_get_questions_filter_and_limit():
    # Add some questions
    client.post("/questions/", json=make_question(tags=["math"]))
    client.post("/questions/", json=make_question(text="Q2", tags=["science"]))
    client.post("/questions/", json=make_question(text="Q3", tags=["math"]))

    # Filter by tag
    resp = client.get("/questions/?tag=math")
    results = resp.json()
    assert all("math" in q["tags"] for q in results)
    assert len(results) == 2

    # Limit results
    resp = client.get("/questions/?n=2")
    results = resp.json()
    assert len(results) == 2


def test_get_random_questions():
    for i in range(5):
        client.post("/questions/", json=make_question(text=f"Q{i}"))
    resp = client.get("/questions/random?n=3")
    results = resp.json()
    assert len(results) == 3
    assert all("id" in q for q in results)


def test_get_random_questions_with_no_questions():
    resp = client.get("/questions/random?n=2")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_question_without_tags():
    q = make_question(tags=None)
    q.pop("tags", None)
    resp = client.post("/questions/", json=q)
    assert resp.status_code == 200
    saved = resp.json()
    assert saved["tags"] == []


def test_large_number_of_questions():
    for i in range(50):
        client.post("/questions/", json=make_question(text=f"Q{i}"))
    resp = client.get("/questions/")
    results = resp.json()
    assert len(results) == 50
