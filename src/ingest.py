"""
Ingest tarot card data into the Chroma vector store.

Run from project root:
    python -m src.ingest
"""
import json
import yaml
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

PROJECT_ROOT = Path(__file__).parent.parent


def load_config() -> dict:
    with open(PROJECT_ROOT / "config.yaml") as f:
        return yaml.safe_load(f)


def load_cards(cards_file: str) -> list[dict]:
    with open(PROJECT_ROOT / cards_file) as f:
        return json.load(f)["cards"]


def card_to_document(card: dict) -> Document:
    keywords = ", ".join(card.get("keywords", []))
    suit = card.get("suit") or "N/A"

    element = card.get("element") or ""
    astrological = card.get("astrological") or ""
    symbolism = card.get("symbolism") or ""

    parts = [
        f"Card: {card['name']}",
        f"Arcana: {card['arcana']} | Suit: {suit}",
    ]
    if element:
        parts.append(f"Element: {element}")
    if astrological:
        parts.append(f"Astrological: {astrological}")
    parts += [
        f"Keywords: {keywords}",
        f"Upright: {card['upright_meaning']}",
        f"Reversed: {card['reversed_meaning']}",
    ]
    if symbolism:
        parts.append(f"Symbolism: {symbolism}")

    text = "\n".join(parts)

    metadata = {
        "id": card["id"],
        "name": card["name"],
        "arcana": card["arcana"],
        "suit": suit,
        "number": card.get("number") if card.get("number") is not None else -1,
        "element": card.get("element") or "",
        "astrological": card.get("astrological") or "",
        "keywords": keywords,
        "image_filename": card.get("image_filename") or "",
    }

    return Document(page_content=text, metadata=metadata)


def ingest(reset: bool = False) -> Chroma:
    config = load_config()

    cards = load_cards(config["data"]["cards_file"])
    print(f"Loaded {len(cards)} cards")

    documents = [card_to_document(card) for card in cards]

    persist_dir = str(PROJECT_ROOT / config["vector_db"]["persist_dir"])
    collection_name = config["vector_db"]["collection_name"]

    if reset and Path(persist_dir).exists():
        import shutil
        shutil.rmtree(persist_dir)
        print(f"Cleared existing collection at {persist_dir}")

    print(f"Loading embedding model: {config['embeddings']['model']}")
    embeddings = HuggingFaceEmbeddings(
        model_name=config["embeddings"]["model"],
        model_kwargs={"device": "cpu"},
    )

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_dir,
    )

    print(f"Ingested {len(documents)} cards into '{collection_name}'")
    print(f"Persisted at: {persist_dir}")

    return vectorstore


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Ingest tarot cards into Chroma"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing DB before ingesting",
    )
    args = parser.parse_args()

    ingest(reset=args.reset)
