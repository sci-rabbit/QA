from fastapi import APIRouter

from core.services.answer_service import AnswerService
from api.dependencies import db_session
from core.schemas.answer_schema import AnswerSchema, CreateAnswerSchema

router = APIRouter(prefix="/api", tags=["Answer CRUD"])


@router.post("/questions/{question_id}/answers/")
async def create_answer(
    question_id: int,
    answer_data: CreateAnswerSchema,
    session: db_session,
) -> AnswerSchema:
    answer_service = AnswerService(session=session)
    return await answer_service.create_answer(
        question_id=question_id,
        answer_data=answer_data,
    )


@router.get("/answers/{answer_id}")
async def get_answer(
    answer_id: int,
    session: db_session,
) -> AnswerSchema:
    answer_service = AnswerService(session=session)
    return await answer_service.get_answer(answer_id=answer_id)


@router.delete("/answers/{answer_id}")
async def delete_answer(
    answer_id: int,
    session: db_session,
) -> None:
    answer_service = AnswerService(session=session)
    await answer_service.delete_answer(answer_id=answer_id)
