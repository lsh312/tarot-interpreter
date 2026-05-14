"""
Adds an image_filename field to every card in tarot_cards.json.
Naming convention: {card_id}.jpg  e.g. major_00.jpg, wands_01.jpg
Run from the project root: python ingest/update_json_images.py
"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "tarot_cards.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for card in data["cards"]:
    card["image_filename"] = f"{card['id']}.jpg"

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated {len(data['cards'])} cards with image_filename fields.")
print(f"Saved to {DATA_FILE}")
