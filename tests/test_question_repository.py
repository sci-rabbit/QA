import pytest
from core.repositories.question_repository import QuestionRepository

@pytest.mark.asyncio
async def test_create_question(db_session):
    """Тест создания вопроса"""
    repository = QuestionRepository(session=db_session)
    
    question_data = {"text": "What is Python?"}
    question = await repository.create(question_data)
    
    assert question.id is not None
    assert question.text == "What is Python?"
    assert question.created_at is not None


@pytest.mark.asyncio
async def test_get_question(db_session):
    """Тест получения вопроса по ID"""
    repository = QuestionRepository(session=db_session)
    
    # Создаем вопрос
    question_data = {"text": "What is Python?"}
    created_question = await repository.create(question_data)
    
    # Получаем вопрос
    retrieved_question = await repository.get(q_id=created_question.id)
    
    assert retrieved_question is not None
    assert retrieved_question.id == created_question.id
    assert retrieved_question.text == "What is Python?"


@pytest.mark.asyncio
async def test_get_question_not_found(db_session):
    """Тест получения несуществующего вопроса"""
    repository = QuestionRepository(session=db_session)
    
    question = await repository.get(q_id=999)
    
    assert question is None


@pytest.mark.asyncio
async def test_get_all_questions(db_session):
    """Тест получения всех вопросов"""
    repository = QuestionRepository(session=db_session)
    
    # Создаем несколько вопросов
    question1 = await repository.create({"text": "Question 1"})
    question2 = await repository.create({"text": "Question 2"})
    
    # Получаем все вопросы
    questions = await repository.get_all()
    
    assert len(questions) >= 2
    question_ids = [q.id for q in questions]
    assert question1.id in question_ids
    assert question2.id in question_ids


@pytest.mark.asyncio
async def test_delete_question(db_session):
    """Тест удаления вопроса"""
    repository = QuestionRepository(session=db_session)
    
    # Создаем вопрос
    question = await repository.create({"text": "Question to delete"})
    question_id = question.id
    
    # Удаляем вопрос
    await repository.delete(q_id=question_id)
    
    # Проверяем, что вопрос удален
    deleted_question = await repository.get(q_id=question_id)
    assert deleted_question is None


@pytest.mark.asyncio
async def test_delete_nonexistent_question(db_session):
    """Тест удаления несуществующего вопроса (не должно вызывать ошибку)"""
    repository = QuestionRepository(session=db_session)
    
    # Удаление несуществующего вопроса не должно вызывать ошибку
    await repository.delete(q_id=999)



