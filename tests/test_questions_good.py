# tests/test_questions_api.py
import pytest
from fastapi.testclient import TestClient

from questions_bank.main import app
from questions_bank.repos import question_repo

@pytest.fixture(autouse=True)
def fresh_repo():
    """
    Ensure a clean in-memory repo before each test.
    """
    question_repo.repo._db.clear()
    question_repo.repo._id_counter = 1
    yield
    question_repo.repo._db.clear()
    question_repo.repo._id_counter = 1


@pytest.fixture
def client():
    return TestClient(app)


def _create(client, text="Q?", choices=("A", "B"), answer="A", tags=None):
    payload = {
        "text": text,
        "choices": list(choices),
        "answer": answer,
    }
    if tags is not None:
        payload["tags"] = list(tags)
    resp = client.post("/questions/", json=payload)
    assert resp.status_code == 200
    return resp.json()


# ---------- Edge-case: empty repo ----------
def test_empty_repo_returns_empty_lists(client):
    # GET /questions/ (no data)
    resp = client.get("/questions/")
    assert resp.status_code == 200
    assert resp.json() == []

    # GET /questions/random?n=1 (no data → empty list)
    resp = client.get("/questions/random", params={"n": 1})
    assert resp.status_code == 200
    assert resp.json() == []


# ---------- Typical: create / list / get ----------
def test_create_question_assigns_id_and_persists(client):
    created = _create(client, text="Capital?", choices=("SF", "SAC"), answer="SAC", tags=("geo",))
    assert {"id", "text", "choices", "answer", "tags"} <= set(created.keys())
    assert created["id"] == 1
    assert created["tags"] == ["geo"]

    # List should include it
    resp = client.get("/questions/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["id"] == created["id"]

    # Get by id
    resp = client.get(f"/questions/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["text"] == "Capital?"

    # Missing id → 404 per controller contract
    resp = client.get("/questions/9999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Question not found"


# ---------- Filtering & limits (per get_questions contract) ----------
def test_list_questions_filters_by_tag_excludes_untagged(client):
    _create(client, text="Tagged", tags=("math",))
    _create(client, text="Untagged", tags=None)

    # Tag=math should only return items that include 'math'
    resp = client.get("/questions/", params={"tag": "math"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["text"] == "Tagged"
    assert "math" in data[0]["tags"]
    # Ensure untagged item is not present
    assert all("math" in q.get("tags", []) for q in data)


def test_list_questions_limits_by_n(client):
    for i in range(5):
        _create(client, text=f"Q{i}", tags=("t",))

    resp = client.get("/questions/", params={"n": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3  # service slices results by n


# ---------- Random selection (per get_random_questions contract) ----------
def test_get_random_questions_respects_n_and_truncates(client):
    for i in range(4):
        _create(client, text=f"R{i}", tags=("r",))

    # n within bounds
    resp = client.get("/questions/random", params={"n": 2})
    assert resp.status_code == 200
    two = resp.json()
    assert isinstance(two, list) and len(two) == 2

    # n greater than count → truncated to total size
    resp = client.get("/questions/random", params={"n": 10})
    assert resp.status_code == 200
    many = resp.json()
    assert len(many) == 4  # truncated to available


def test_get_random_questions_invalid_n_returns_422(client):
    # FastAPI Query enforces n >= 1
    resp = client.get("/questions/random", params={"n": 0})
    assert resp.status_code == 422


# ---------- Update (per modify_question contract) ----------
def test_update_question_replaces_fields_and_missing_returns_404(client):
    created = _create(client, text="Old", choices=("A", "B"), answer="A", tags=("x",))
    qid = created["id"]

    payload = {
        "text": "New",
        "choices": ["C", "D"],
        "answer": "C",
        "tags": ["y"],
    }
    resp = client.put(f"/questions/{qid}", json=payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["text"] == "New"
    assert updated["choices"] == ["C", "D"]
    assert updated["answer"] == "C"
    assert updated["tags"] == ["y"]

    # Missing id → 404
    resp = client.put("/questions/9999", json=payload)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Question not found"


# ---------- Delete (per delete_question contract) ----------
def test_delete_question_then_get_returns_404(client):
    created = _create(client, text="To delete")
    qid = created["id"]

    resp = client.delete(f"/questions/{qid}")
    assert resp.status_code == 200
    assert resp.json() == {"status": "deleted"}

    # Subsequent GET should 404
    resp = client.get(f"/questions/{qid}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Question not found"

    # Deleting a missing id → 404
    resp = client.delete("/questions/9999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Question not found"


# ---------- Large dataset + “no tags” edge ----------
def test_large_insert_then_filter_and_slice_and_untagged_behavior(client):
    # 50 tagged + 50 untagged
    for i in range(50):
        _create(client, text=f"T{i}", tags=("keep",))
    for i in range(50):
        _create(client, text=f"U{i}", tags=None)

    # Tag filter should exclude untagged
    resp = client.get("/questions/", params={"tag": "keep"})
    assert resp.status_code == 200
    tagged_only = resp.json()
    assert len(tagged_only) == 50
    assert all("keep" in q.get("tags", []) for q in tagged_only)

    # n slicing correctness on large list
    resp = client.get("/questions/", params={"n": 30})
    assert resp.status_code == 200
    sliced = resp.json()
    assert len(sliced) == 30
