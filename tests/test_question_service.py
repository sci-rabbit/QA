import pytest
from fastapi import HTTPException
from core.services.question_service import QuestionService
from core.schemas.question_schema import CreateQuestionSchema


@pytest.mark.asyncio
async def test_create_question_service(db_session):
    """Тест создания вопроса через сервис"""
    service = QuestionService(session=db_session)
    
    question_data = CreateQuestionSchema(text="What is Python?")
    question = await service.create_question(question_data)
    
    assert question.id is not None
    assert question.text == "What is Python?"
    assert question.created_at is not None


@pytest.mark.asyncio
async def test_get_question_service(db_session):
    """Тест получения вопроса через сервис"""
    service = QuestionService(session=db_session)
    
    # Создаем вопрос
    question_data = CreateQuestionSchema(text="What is Python?")
    created_question = await service.create_question(question_data)
    
    # Получаем вопрос
    retrieved_question = await service.get_question(question_id=created_question.id)
    
    assert retrieved_question.id == created_question.id
    assert retrieved_question.text == "What is Python?"
    assert retrieved_question.answers == []


@pytest.mark.asyncio
async def test_get_question_not_found_service(db_session):
    """Тест получения несуществующего вопроса через сервис"""
    service = QuestionService(session=db_session)
    
    with pytest.raises(HTTPException) as exc_info:
        await service.get_question(question_id=999)
    
    assert exc_info.value.status_code == 404
    assert "Question not found" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_all_questions_service(db_session):
    """Тест получения всех вопросов через сервис"""
    service = QuestionService(session=db_session)
    
    # Создаем несколько вопросов
    question1 = await service.create_question(CreateQuestionSchema(text="Question 1"))
    question2 = await service.create_question(CreateQuestionSchema(text="Question 2"))
    
    # Получаем все вопросы
    questions = await service.get_questions()
    
    assert len(questions) >= 2
    question_ids = [q.id for q in questions]
    assert question1.id in question_ids
    assert question2.id in question_ids


@pytest.mark.asyncio
async def test_delete_question_service(db_session):
    """Тест удаления вопроса через сервис"""
    service = QuestionService(session=db_session)
    
    # Создаем вопрос
    question = await service.create_question(CreateQuestionSchema(text="Question to delete"))
    question_id = question.id
    
    # Удаляем вопрос
    await service.delete_question(question_id=question_id)
    
    # Проверяем, что вопрос удален
    with pytest.raises(HTTPException) as exc_info:
        await service.get_question(question_id=question_id)
    
    assert exc_info.value.status_code == 404



