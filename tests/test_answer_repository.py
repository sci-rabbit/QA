import pytest
from core.repositories.answer_repository import AnswerRepository
from core.repositories.question_repository import QuestionRepository


@pytest.mark.asyncio
async def test_create_answer(db_session):
    """Тест создания ответа"""

    # Сначала создаем вопрос
    question_repo = QuestionRepository(session=db_session)
    question = await question_repo.create({"text": "What is Python?"})
    
    # Создаем ответ
    answer_repo = AnswerRepository(session=db_session)
    answer_data = {
        "question_id": question.id,
        "user_id": "user-123",
        "text": "Python is a programming language"
    }
    answer = await answer_repo.create(answer_data)
    
    assert answer.id is not None
    assert answer.question_id == question.id
    assert answer.user_id == "user-123"
    assert answer.text == "Python is a programming language"
    assert answer.created_at is not None


@pytest.mark.asyncio
async def test_get_answer(db_session):
    """Тест получения ответа по ID"""

    # Создаем вопрос и ответ
    question_repo = QuestionRepository(session=db_session)
    question = await question_repo.create({"text": "What is Python?"})
    
    answer_repo = AnswerRepository(session=db_session)
    answer_data = {
        "question_id": question.id,
        "user_id": "user-123",
        "text": "Python is a programming language"
    }
    created_answer = await answer_repo.create(answer_data)

    retrieved_answer = await answer_repo.get(a_id=created_answer.id)
    
    assert retrieved_answer is not None
    assert retrieved_answer.id == created_answer.id
    assert retrieved_answer.text == "Python is a programming language"
    assert retrieved_answer.user_id == "user-123"


@pytest.mark.asyncio
async def test_get_answer_not_found(db_session):
    """Тест получения несуществующего ответа"""
    answer_repo = AnswerRepository(session=db_session)
    
    answer = await answer_repo.get(a_id=999)
    
    assert answer is None


@pytest.mark.asyncio
async def test_delete_answer(db_session):
    """Тест удаления ответа"""

    # Создаем вопрос и ответ
    question_repo = QuestionRepository(session=db_session)
    question = await question_repo.create({"text": "What is Python?"})
    
    answer_repo = AnswerRepository(session=db_session)
    answer_data = {
        "question_id": question.id,
        "user_id": "user-123",
        "text": "Python is a programming language"
    }
    answer = await answer_repo.create(answer_data)
    answer_id = answer.id
    
    # Удаляем ответ
    await answer_repo.delete(a_id=answer_id)
    
    # Проверяем, что ответ удален
    deleted_answer = await answer_repo.get(a_id=answer_id)
    assert deleted_answer is None


@pytest.mark.asyncio
async def test_delete_nonexistent_answer(db_session):
    """Тест удаления несуществующего ответа (не должно вызывать ошибку)"""
    answer_repo = AnswerRepository(session=db_session)
    
    # Удаление несуществующего ответа не должно вызывать ошибку
    await answer_repo.delete(a_id=999)



