import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_answer_api(client: AsyncClient):
    """Тест создания ответа через API"""

    # Сначала создаем вопрос
    question_response = await client.post(
        "/api/questions/",
        json={"text": "What is Python?"}
    )
    question_id = question_response.json()["id"]
    
    # Создаем ответ
    response = await client.post(
        f"/api/questions/{question_id}/answers/",
        json={"text": "Python is a programming language", "user_id": "user-123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Python is a programming language"
    assert data["user_id"] == "user-123"
    assert data["question_id"] == question_id
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_answer_nonexistent_question_api(client: AsyncClient):
    """Тест создания ответа к несуществующему вопросу через API"""
    response = await client.post(
        "/api/questions/999/answers/",
        json={"text": "Some answer", "user_id": "user-123"}
    )
    
    assert response.status_code == 404
    assert "Question not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_answer_api(client: AsyncClient):
    """Тест получения ответа через API"""

    # Создаем вопрос и ответ
    question_response = await client.post(
        "/api/questions/",
        json={"text": "What is Python?"}
    )
    question_id = question_response.json()["id"]
    
    answer_response = await client.post(
        f"/api/questions/{question_id}/answers/",
        json={"text": "Python is a programming language", "user_id": "user-123"}
    )
    answer_id = answer_response.json()["id"]
    
    # Получаем ответ
    response = await client.get(f"/api/answers/{answer_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == answer_id
    assert data["text"] == "Python is a programming language"
    assert data["user_id"] == "user-123"
    assert data["question_id"] == question_id


@pytest.mark.asyncio
async def test_get_answer_not_found_api(client: AsyncClient):
    """Тест получения несуществующего ответа через API"""
    response = await client.get("/api/answers/999")
    
    assert response.status_code == 404
    assert "Answer not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_answer_api(client: AsyncClient):
    """Тест удаления ответа через API"""
    # Создаем вопрос и ответ
    question_response = await client.post(
        "/api/questions/",
        json={"text": "What is Python?"}
    )
    question_id = question_response.json()["id"]
    
    answer_response = await client.post(
        f"/api/questions/{question_id}/answers/",
        json={"text": "Python is a programming language", "user_id": "user-123"}
    )
    answer_id = answer_response.json()["id"]
    
    # Удаляем ответ
    delete_response = await client.delete(f"/api/answers/{answer_id}")
    assert delete_response.status_code == 200
    
    # Проверяем, что ответ удален
    get_response = await client.get(f"/api/answers/{answer_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_multiple_answers_same_user_api(client: AsyncClient):
    """Тест создания нескольких ответов от одного пользователя на один вопрос"""

    # Создаем вопрос
    question_response = await client.post(
        "/api/questions/",
        json={"text": "What is Python?"}
    )
    question_id = question_response.json()["id"]
    
    # Создаем несколько ответов от одного пользователя
    user_id = "user-123"
    answer1_response = await client.post(
        f"/api/questions/{question_id}/answers/",
        json={"text": "Answer 1", "user_id": user_id}
    )
    answer2_response = await client.post(
        f"/api/questions/{question_id}/answers/",
        json={"text": "Answer 2", "user_id": user_id}
    )
    
    assert answer1_response.status_code == 200
    assert answer2_response.status_code == 200
    
    answer1_id = answer1_response.json()["id"]
    answer2_id = answer2_response.json()["id"]
    
    assert answer1_id != answer2_id
    assert answer1_response.json()["user_id"] == user_id
    assert answer2_response.json()["user_id"] == user_id


@pytest.mark.asyncio
async def test_get_question_with_answers_api(client: AsyncClient):
    """Тест получения вопроса со всеми ответами через API"""

    # Создаем вопрос
    question_response = await client.post(
        "/api/questions/",
        json={"text": "What is Python?"}
    )
    question_id = question_response.json()["id"]
    
    # Создаем несколько ответов
    await client.post(
        f"/api/questions/{question_id}/answers/",
        json={"text": "Answer 1", "user_id": "user-123"}
    )
    await client.post(
        f"/api/questions/{question_id}/answers/",
        json={"text": "Answer 2", "user_id": "user-456"}
    )
    
    # Получаем вопрос со всеми ответами
    response = await client.get(f"/api/questions/{question_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == question_id
    assert len(data["answers"]) == 2
    assert all("id" in answer for answer in data["answers"])
    assert all("text" in answer for answer in data["answers"])


@pytest.mark.asyncio
async def test_create_answer_validation(client: AsyncClient):
    """Тест валидации при создании ответа"""

    # Создаем вопрос
    question_response = await client.post(
        "/api/questions/",
        json={"text": "What is Python?"}
    )
    question_id = question_response.json()["id"]
    
    # Попытка создать ответ без обязательных полей
    response = await client.post(
        f"/api/questions/{question_id}/answers/",
        json={}
    )
    
    assert response.status_code == 422  # Validation error



