from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseAnswerSchema(BaseModel):
    text: str
    user_id: str


class CreateAnswerSchema(BaseAnswerSchema):
    pass


class AnswerSchema(BaseAnswerSchema):
    id: int
    question_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

