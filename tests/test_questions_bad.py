import pytest
from httpx import AsyncClient
from main import app  # import your FastAPI app


@pytest.mark.asyncio
async def test_create_question():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/questions/", json={"title": "What is 2+2?", "answer": "4"}
        )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "What is 2+2?"
    assert data["answer"] == "4"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_question():
    # First create a question
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_res = await ac.post(
            "/questions/", json={"title": "Capital of France?", "answer": "Paris"}
        )
        qid = create_res.json()["id"]

        # Retrieve it
        get_res = await ac.get(f"/questions/{qid}")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["title"] == "Capital of France?"
    assert data["answer"] == "Paris"


@pytest.mark.asyncio
async def test_update_question():
    # Create first
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_res = await ac.post(
            "/questions/", json={"title": "Largest planet?", "answer": "Saturn"}
        )
        qid = create_res.json()["id"]

        # Update
        update_res = await ac.put(
            f"/questions/{qid}", json={"title": "Largest planet?", "answer": "Jupiter"}
        )

    assert update_res.status_code == 200
    data = update_res.json()
    assert data["answer"] == "Jupiter"


@pytest.mark.asyncio
async def test_delete_question():
    # Create first
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_res = await ac.post(
            "/questions/", json={"title": "Temp question?", "answer": "Delete me"}
        )
        qid = create_res.json()["id"]

        # Delete
        delete_res = await ac.delete(f"/questions/{qid}")
        assert delete_res.status_code == 204

        # Confirm deletion
        get_res = await ac.get(f"/questions/{qid}")
        assert get_res.status_code == 404
