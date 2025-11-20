import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.answer_repository import AnswerRepository
from core.repositories.question_repository import QuestionRepository

from core.schemas.answer_schema import CreateAnswerSchema, AnswerSchema


logger = logging.getLogger(__name__)


class AnswerService:
    def __init__(self, session: AsyncSession) -> None:
        self.answer_repository = AnswerRepository(session=session)
        self.question_repository = QuestionRepository(session=session)

    async def create_answer(
        self,
        question_id: int,
        answer_data: CreateAnswerSchema,
    ) -> AnswerSchema:
        question = await self.question_repository.get(q_id=question_id)

        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )

        logger.info(
            "Creating answer, text=%s",
            answer_data.text,
        )
        answer_data_dict = answer_data.model_dump()
        answer_data_dict["question_id"] = question_id

        answer = await self.answer_repository.create(
            answer_data=answer_data_dict,
        )
        logger.info(
            "Answer created successfully",
        )

        return AnswerSchema.model_validate(answer)

    async def get_answer(
        self,
        answer_id: int,
    ) -> AnswerSchema:
        answer = await self.answer_repository.get(a_id=answer_id)

        if answer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Answer not found",
            )

        return AnswerSchema.model_validate(answer)

    async def delete_answer(
        self,
        answer_id: int,
    ) -> None:
        logger.warning("Deleting answer, answer_id=%s", answer_id)
        await self.answer_repository.delete(a_id=answer_id)
        logger.info("Answer deleted")
