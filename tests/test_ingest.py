import pytest
from pathlib import Path
from src.ingest import load_config, load_cards, card_to_document, ingest


def test_load_cards():
    config = load_config()
    cards = load_cards(config["data"]["cards_file"])
    assert len(cards) == 78


def test_card_to_document_no_none_metadata():
    config = load_config()
    cards = load_cards(config["data"]["cards_file"])
    for card in cards:
        doc = card_to_document(card)
        for key, value in doc.metadata.items():
            assert value is not None, f"None metadata on '{card['name']}' field '{key}'"


def test_card_to_document_text_contains_name():
    config = load_config()
    cards = load_cards(config["data"]["cards_file"])
    for card in cards:
        doc = card_to_document(card)
        assert card["name"] in doc.page_content


@pytest.fixture(scope="module")
def vectorstore():
    return ingest()


def test_vectorstore_card_count(vectorstore):
    assert vectorstore._collection.count() == 78


def test_similarity_search_returns_results(vectorstore):
    results = vectorstore.similarity_search("new beginnings and adventure", k=3)
    assert len(results) == 3
    names = [r.metadata["name"] for r in results]
    assert any(name for name in names), "Expected at least one result"


def test_similarity_search_fool(vectorstore):
    results = vectorstore.similarity_search("new beginnings and adventure", k=5)
    names = [r.metadata["name"] for r in results]
    assert "The Fool" in names, f"Expected The Fool in top 5, got: {names}"
