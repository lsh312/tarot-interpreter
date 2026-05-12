from fastapi import APIRouter, HTTPException, Request

from src.agents import ReadingResult
from .models import CardResponse, QuestionRequest, ReadingResponse

router = APIRouter(prefix="/reading", tags=["reading"])


def _to_response(result: ReadingResult) -> ReadingResponse:
    return ReadingResponse(
        spread_type=result.spread_type,
        question=result.question,
        cards=[
            CardResponse(
                position=pos,
                name=card.name,
                orientation=card.orientation,
                keywords=card.keywords,
                meaning=card.active_meaning,
                image_filename=card.image_filename,
            )
            for pos, card in result.cards
        ],
        interpretation=result.interpretation,
    )


@router.post("/daily", response_model=ReadingResponse)
def daily_reading(request: Request):
    try:
        return _to_response(request.app.state.agent.daily_reading())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/three-card", response_model=ReadingResponse)
def three_card_reading(body: QuestionRequest, request: Request):
    try:
        return _to_response(request.app.state.agent.three_card_reading(body.question))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/celtic-cross", response_model=ReadingResponse)
def celtic_cross_reading(body: QuestionRequest, request: Request):
    try:
        return _to_response(
            request.app.state.agent.celtic_cross_reading(body.question)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
