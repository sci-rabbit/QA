import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_question_api(client: AsyncClient):
    """Тест создания вопроса через API"""
    response = await client.post(
        "/api/questions/",
        json={"text": "What is Python?"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "What is Python?"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_question_api(client: AsyncClient):
    """Тест получения вопроса через API"""

    # Создаем вопрос
    create_response = await client.post(
        "/api/questions/",
        json={"text": "What is Python?"}
    )
    question_id = create_response.json()["id"]
    
    # Получаем вопрос
    response = await client.get(f"/api/questions/{question_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == question_id
    assert data["text"] == "What is Python?"
    assert "answers" in data
    assert isinstance(data["answers"], list)


@pytest.mark.asyncio
async def test_get_question_not_found_api(client: AsyncClient):
    """Тест получения несуществующего вопроса через API"""
    response = await client.get("/api/questions/999")
    
    assert response.status_code == 404
    assert "Question not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_all_questions_api(client: AsyncClient):
    """Тест получения всех вопросов через API"""

    # Создаем несколько вопросов
    await client.post("/api/questions/", json={"text": "Question 1"})
    await client.post("/api/questions/", json={"text": "Question 2"})
    
    # Получаем все вопросы
    response = await client.get("/api/questions/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_delete_question_api(client: AsyncClient):
    """Тест удаления вопроса через API"""

    # Создаем вопрос
    create_response = await client.post(
        "/api/questions/",
        json={"text": "Question to delete"}
    )
    question_id = create_response.json()["id"]
    
    # Удаляем вопрос
    delete_response = await client.delete(f"/api/questions/{question_id}")
    assert delete_response.status_code == 200
    
    # Проверяем, что вопрос удален
    get_response = await client.get(f"/api/questions/{question_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_question_with_answers_cascade(client: AsyncClient):
    """Тест каскадного удаления ответов при удалении вопроса"""

    # Создаем вопрос
    question_response = await client.post(
        "/api/questions/",
        json={"text": "Question with answers"}
    )
    question_id = question_response.json()["id"]
    
    # Создаем несколько ответов
    answer1_response = await client.post(
        f"/api/questions/{question_id}/answers/",
        json={"text": "Answer 1", "user_id": "user-123"}
    )
    answer2_response = await client.post(
        f"/api/questions/{question_id}/answers/",
        json={"text": "Answer 2", "user_id": "user-456"}
    )
    answer1_id = answer1_response.json()["id"]
    answer2_id = answer2_response.json()["id"]
    
    # Удаляем вопрос
    delete_response = await client.delete(f"/api/questions/{question_id}")
    assert delete_response.status_code == 200
    
    # Проверяем, что ответы тоже удалены
    answer1_get = await client.get(f"/api/answers/{answer1_id}")
    answer2_get = await client.get(f"/api/answers/{answer2_id}")
    
    assert answer1_get.status_code == 404
    assert answer2_get.status_code == 404


@pytest.mark.asyncio
async def test_create_question_validation(client: AsyncClient):
    """Тест валидации при создании вопроса"""

    # Попытка создать вопрос без текста
    response = await client.post("/api/questions/", json={})
    
    assert response.status_code == 422  # Validation error


