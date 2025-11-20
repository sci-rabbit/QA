import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.question_repository import QuestionRepository
from core.schemas.question_schema import (
    CreateQuestionSchema,
    QuestionSchema,
    QuestionSchemaWithAnswers,
)

logger = logging.getLogger(__name__)


class QuestionService:
    def __init__(self, session: AsyncSession) -> None:
        self.question_repository = QuestionRepository(session=session)

    async def create_question(
        self,
        question_data: CreateQuestionSchema,
    ) -> QuestionSchema:
        logger.info(
            "Creating question text=%s",
            question_data.text,
        )
        question_data_dict = question_data.model_dump()

        question = await self.question_repository.create(
            question_data=question_data_dict,
        )

        logger.info(
            "Question created successfully",
        )
        return QuestionSchema.model_validate(question)

    async def get_question(
        self,
        question_id: int,
    ) -> QuestionSchemaWithAnswers:
        question = await self.question_repository.get(
            q_id=question_id,
        )

        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )

        return QuestionSchemaWithAnswers.model_validate(question)

    async def get_questions(
        self,
    ) -> list[QuestionSchema]:
        questions = await self.question_repository.get_all()
        return [QuestionSchema.model_validate(question) for question in questions]

    async def delete_question(
        self,
        question_id: int,
    ) -> None:
        logger.warning("Deleting question, question_id=%s", question_id)
        await self.question_repository.delete(q_id=question_id)
        logger.info("Question deleted")
