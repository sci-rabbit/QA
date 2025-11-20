from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from core.schemas.answer_schema import AnswerSchema


class BaseQuestionSchema(BaseModel):
    text: str = Field(min_length=3)


class CreateQuestionSchema(BaseQuestionSchema):
    pass


class QuestionSchema(BaseQuestionSchema):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionSchemaWithAnswers(QuestionSchema):
    answers: list[AnswerSchema]

