import pytest
from src.agents import TarotAgent, ReadingResult


@pytest.fixture(scope="module")
def agent():
    return TarotAgent()


def test_daily_reading_structure(agent):
    result = agent.daily_reading()
    assert isinstance(result, ReadingResult)
    assert result.spread_type == "single_card"
    assert result.question is None
    assert len(result.cards) == 1
    assert len(result.interpretation) > 50


def test_three_card_reading_structure(agent):
    result = agent.three_card_reading("Should I pursue this new opportunity?")
    assert result.spread_type == "three_card"
    assert result.question is not None
    assert len(result.cards) == 3
    positions = [pos for pos, _ in result.cards]
    assert positions == ["Past", "Present", "Future"]
    assert len(result.interpretation) > 100


def test_celtic_cross_reading_structure(agent):
    result = agent.celtic_cross_reading("How should I approach my career right now?")
    assert result.spread_type == "celtic_cross"
    assert len(result.cards) == 10
    assert len(result.interpretation) > 200


def test_cards_are_unique_within_reading(agent):
    result = agent.celtic_cross_reading("Will this relationship work out?")
    card_ids = [card.id for _, card in result.cards]
    assert len(card_ids) == len(set(card_ids)), "Duplicate cards drawn in same reading"


def test_card_orientation_in_interpretation(agent):
    result = agent.daily_reading()
    _, card = result.cards[0]
    assert card.orientation in ("Upright", "Reversed")
    assert card.active_meaning == (
        card.reversed_meaning if card.is_reversed else card.upright_meaning
    )
