import json
import random
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import anthropic
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent.parent

_SYSTEM_PROMPT = (
    "You are a wise and insightful tarot reader with deep knowledge of the cards' "
    "symbolism, archetypal meanings, and their relevance to everyday life. "
    "Your readings are warm, thoughtful, and practically grounded. "
    "You speak directly to the reader with compassion and clarity. "
    "Never add disclaimers about tarot being 'just for entertainment' — "
    "treat each reading with full seriousness and respect."
)


@dataclass
class CardDraw:
    id: str
    name: str
    arcana: str
    suit: Optional[str]
    keywords: list[str]
    upright_meaning: str
    reversed_meaning: str
    symbolism: str
    image_filename: str
    is_reversed: bool

    @property
    def orientation(self) -> str:
        return "Reversed" if self.is_reversed else "Upright"

    @property
    def active_meaning(self) -> str:
        return self.reversed_meaning if self.is_reversed else self.upright_meaning


@dataclass
class ReadingResult:
    spread_type: str
    question: Optional[str]
    cards: list[tuple[str, CardDraw]]  # (position_name, card)
    interpretation: str


class TarotAgent:
    def __init__(self):
        config = self._load_config()
        self.llm_config = config["llm"]
        self.spreads = config["spreads"]
        self._all_cards = self._load_cards(config["data"]["cards_file"])
        self.client = anthropic.Anthropic()

    def _load_config(self) -> dict:
        with open(PROJECT_ROOT / "config.yaml") as f:
            return yaml.safe_load(f)

    def _load_cards(self, cards_file: str) -> list[dict]:
        with open(PROJECT_ROOT / cards_file) as f:
            return json.load(f)["cards"]

    def _draw(self, n: int) -> list[CardDraw]:
        sample = random.sample(self._all_cards, n)
        return [
            CardDraw(
                id=c["id"],
                name=c["name"],
                arcana=c["arcana"],
                suit=c.get("suit"),
                keywords=c.get("keywords", []),
                upright_meaning=c["upright_meaning"],
                reversed_meaning=c["reversed_meaning"],
                symbolism=c.get("symbolism") or "",
                image_filename=c.get("image_filename") or "",
                is_reversed=random.random() < 0.5,
            )
            for c in sample
        ]

    def _format_card(self, position: str, card: CardDraw) -> str:
        lines = [
            f"**{position}: {card.name}** ({card.orientation})",
            f"Keywords: {', '.join(card.keywords)}",
            f"Meaning: {card.active_meaning}",
        ]
        if card.symbolism:
            lines.append(f"Symbolism: {card.symbolism}")
        return "\n".join(lines)

    def _interpret(self, user_message: str) -> str:
        with self.client.messages.stream(
            model=self.llm_config["model"],
            max_tokens=self.llm_config["max_tokens"],
            system=[
                {
                    "type": "text",
                    "text": _SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            message = stream.get_final_message()

        return next(b.text for b in message.content if b.type == "text")

    def daily_reading(self) -> ReadingResult:
        """Draw one random card and interpret the energy of the day."""
        cards = self._draw(1)
        card = cards[0]
        position = self.spreads["single_card"]["positions"][0]

        prompt = (
            f"Today's daily card has been drawn:\n\n"
            f"{self._format_card(position, card)}\n\n"
            "Interpret this card's energy for today. What themes, awareness, or guidance "
            "does it bring for navigating the day ahead? "
            "Be warm, practical, and around 150-200 words."
        )

        return ReadingResult(
            spread_type="single_card",
            question=None,
            cards=[(position, card)],
            interpretation=self._interpret(prompt),
        )

    def three_card_reading(self, question: str) -> ReadingResult:
        """Draw three cards to give a fast answer to a specific question."""
        cards = self._draw(3)
        positions = self.spreads["three_card"]["positions"]
        pairs = list(zip(positions, cards))

        card_block = "\n\n".join(
            self._format_card(pos, card) for pos, card in pairs
        )

        prompt = (
            f"A three-card spread has been drawn to answer this question:\n\n"
            f"**Question:** {question}\n\n"
            f"The cards:\n\n{card_block}\n\n"
            "Provide a cohesive reading that answers the question through these three cards. "
            "Show how past influences the present, and what guidance the future position offers. "
            "Be specific to the question. Around 250-300 words."
        )

        return ReadingResult(
            spread_type="three_card",
            question=question,
            cards=pairs,
            interpretation=self._interpret(prompt),
        )

    def celtic_cross_reading(self, question: str) -> ReadingResult:
        """Draw ten cards for a detailed Celtic Cross reading on a specific question."""
        cards = self._draw(10)
        positions = self.spreads["celtic_cross"]["positions"]
        pairs = list(zip(positions, cards))

        card_block = "\n\n".join(
            self._format_card(pos, card) for pos, card in pairs
        )

        prompt = (
            f"A Celtic Cross spread has been drawn to answer this question:\n\n"
            f"**Question:** {question}\n\n"
            f"The ten cards:\n\n{card_block}\n\n"
            "Provide a detailed reading that answers the question through all ten cards. "
            "Weave together the story told by each position — present situation, challenge, "
            "past and future influences, internal and external forces, advice, and the outcome. "
            "Be specific to the question. Around 400-500 words."
        )

        return ReadingResult(
            spread_type="celtic_cross",
            question=question,
            cards=pairs,
            interpretation=self._interpret(prompt),
        )
