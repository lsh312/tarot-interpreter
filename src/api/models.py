from pydantic import BaseModel
from typing import Optional


class QuestionRequest(BaseModel):
    question: str


class CardResponse(BaseModel):
    position: str
    name: str
    orientation: str
    keywords: list[str]
    meaning: str
    image_filename: str


class ReadingResponse(BaseModel):
    spread_type: str
    question: Optional[str]
    cards: list[CardResponse]
    interpretation: str
