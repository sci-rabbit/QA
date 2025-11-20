from fastapi import APIRouter


from api.dependencies import db_session
from core.schemas.question_schema import (
    QuestionSchema,
    CreateQuestionSchema,
    QuestionSchemaWithAnswers,
)
from core.services.question_service import QuestionService

router = APIRouter(prefix="/api", tags=["Question CRUD"])


@router.get("/questions/")
async def get_questions(
    session: db_session,
) -> list[QuestionSchema]:
    question_service = QuestionService(session=session)
    return await question_service.get_questions()


@router.post("/questions/")
async def create_question(
    question_data: CreateQuestionSchema,
    session: db_session,
) -> QuestionSchema:
    question_service = QuestionService(session=session)
    return await question_service.create_question(question_data=question_data)


@router.get("/questions/{id}")
async def get_question(
    id: int,
    session: db_session,
) -> QuestionSchemaWithAnswers:
    question_service = QuestionService(session=session)
    return await question_service.get_question(question_id=id)


@router.delete("/questions/{id}")
async def delete_question(
    id: int,
    session: db_session,
) -> None:
    question_service = QuestionService(session=session)
    await question_service.delete_question(question_id=id)
