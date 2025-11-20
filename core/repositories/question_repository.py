import logging
from typing import Dict, Any

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models.question import Question


logger = logging.getLogger(__name__)


class QuestionRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def get_all(self) -> list[Question]:
        query = select(Question)
        result = await self.session.execute(query)

        return list(result.scalars().all())

    async def get(self, q_id: int) -> Question | None:
        query = (
            select(Question)
            .options(selectinload(Question.answers))
            .where(Question.id == q_id)
        )
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def create(self, question_data: Dict[str, Any]) -> Question:
        question_model = Question(**question_data)
        self.session.add(question_model)
        await self.session.commit()
        return question_model

    async def delete(self, q_id: int) -> None:
        query = delete(Question).where(Question.id == q_id)
        await self.session.execute(query)
        await self.session.commit()
