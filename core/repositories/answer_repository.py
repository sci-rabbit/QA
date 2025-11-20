import logging
from typing import Dict, Any

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.answer import Answer

logger = logging.getLogger(__name__)


class AnswerRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def get(self, a_id: int) -> Answer | None:
        return await self.session.get(Answer, a_id)

    async def create(self, answer_data: Dict[str, Any]) -> Answer:
        question_model = Answer(**answer_data)
        self.session.add(question_model)
        await self.session.commit()
        return question_model

    async def delete(self, a_id: int) -> None:
        query = delete(Answer).where(Answer.id == a_id)
        await self.session.execute(query)
        await self.session.commit()
