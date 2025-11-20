import pytest
from fastapi import HTTPException
from core.services.answer_service import AnswerService
from core.services.question_service import QuestionService
from core.schemas.answer_schema import CreateAnswerSchema
from core.schemas.question_schema import CreateQuestionSchema


@pytest.mark.asyncio
async def test_create_answer_service(db_session):
    """Тест создания ответа через сервис"""

    # Сначала создаем вопрос
    question_service = QuestionService(session=db_session)
    question = await question_service.create_question(
        CreateQuestionSchema(text="What is Python?")
    )
    
    # Создаем ответ
    answer_service = AnswerService(session=db_session)
    answer_data = CreateAnswerSchema(
        text="Python is a programming language",
        user_id="user-123"
    )
    answer = await answer_service.create_answer(
        question_id=question.id,
        answer_data=answer_data
    )
    
    assert answer.id is not None
    assert answer.question_id == question.id
    assert answer.user_id == "user-123"
    assert answer.text == "Python is a programming language"
    assert answer.created_at is not None


@pytest.mark.asyncio
async def test_create_answer_nonexistent_question(db_session):
    """Тест создания ответа к несуществующему вопросу"""
    answer_service = AnswerService(session=db_session)
    answer_data = CreateAnswerSchema(
        text="Some answer",
        user_id="user-123"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await answer_service.create_answer(
            question_id=999,
            answer_data=answer_data
        )
    
    assert exc_info.value.status_code == 404
    assert "Question not found" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_answer_service(db_session):
    """Тест получения ответа через сервис"""

    # Создаем вопрос и ответ
    question_service = QuestionService(session=db_session)
    question = await question_service.create_question(
        CreateQuestionSchema(text="What is Python?")
    )
    
    answer_service = AnswerService(session=db_session)
    answer_data = CreateAnswerSchema(
        text="Python is a programming language",
        user_id="user-123"
    )
    created_answer = await answer_service.create_answer(
        question_id=question.id,
        answer_data=answer_data
    )
    
    # Получаем ответ
    retrieved_answer = await answer_service.get_answer(answer_id=created_answer.id)
    
    assert retrieved_answer.id == created_answer.id
    assert retrieved_answer.text == "Python is a programming language"
    assert retrieved_answer.user_id == "user-123"


@pytest.mark.asyncio
async def test_get_answer_not_found_service(db_session):
    """Тест получения несуществующего ответа через сервис"""
    answer_service = AnswerService(session=db_session)
    
    with pytest.raises(HTTPException) as exc_info:
        await answer_service.get_answer(answer_id=999)
    
    assert exc_info.value.status_code == 404
    assert "Answer not found" in exc_info.value.detail


@pytest.mark.asyncio
async def test_delete_answer_service(db_session):
    """Тест удаления ответа через сервис"""

    # Создаем вопрос и ответ
    question_service = QuestionService(session=db_session)
    question = await question_service.create_question(
        CreateQuestionSchema(text="What is Python?")
    )
    
    answer_service = AnswerService(session=db_session)
    answer_data = CreateAnswerSchema(
        text="Python is a programming language",
        user_id="user-123"
    )
    answer = await answer_service.create_answer(
        question_id=question.id,
        answer_data=answer_data
    )
    answer_id = answer.id
    
    # Удаляем ответ
    await answer_service.delete_answer(answer_id=answer_id)
    
    # Проверяем, что ответ удален
    with pytest.raises(HTTPException) as exc_info:
        await answer_service.get_answer(answer_id=answer_id)
    
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_multiple_answers_from_same_user(db_session):
    """Тест создания нескольких ответов от одного пользователя на один вопрос"""

    # Создаем вопрос
    question_service = QuestionService(session=db_session)
    question = await question_service.create_question(
        CreateQuestionSchema(text="What is Python?")
    )
    
    # Создаем несколько ответов от одного пользователя
    answer_service = AnswerService(session=db_session)
    user_id = "user-123"
    
    answer1 = await answer_service.create_answer(
        question_id=question.id,
        answer_data=CreateAnswerSchema(text="Answer 1", user_id=user_id)
    )
    
    answer2 = await answer_service.create_answer(
        question_id=question.id,
        answer_data=CreateAnswerSchema(text="Answer 2", user_id=user_id)
    )
    
    assert answer1.id != answer2.id
    assert answer1.user_id == answer2.user_id == user_id
    assert answer1.question_id == answer2.question_id == question.id



