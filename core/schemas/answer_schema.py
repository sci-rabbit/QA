from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BaseAnswerSchema(BaseModel):
    text: str = Field(min_length=1)
    user_id: str = Field(min_length=1)


class CreateAnswerSchema(BaseAnswerSchema):
    pass


class AnswerSchema(BaseAnswerSchema):
    id: int
    question_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

