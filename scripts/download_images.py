"""
Downloads all 78 Rider-Waite-Smith tarot card images (public domain) into data/images/.
Source: Sacred Texts (https://www.sacred-texts.com/tarot/pkt/img/)
URL pattern: ar01.jpg (major arcana), wa01.jpg / cu01.jpg / sw01.jpg / pe01.jpg (minor arcana)

Run from the project root: python scripts/download_images.py
Requires: pip install requests
"""

import json
import time
from pathlib import Path

import requests

DATA_FILE = Path(__file__).parent.parent / "data" / "tarot_cards.json"
IMAGES_DIR = Path(__file__).parent.parent / "data" / "images"
BASE_URL = "https://www.sacred-texts.com/tarot/pkt/img"

SUIT_ABBREV = {
    "wands": "wa",
    "cups": "cu",
    "swords": "sw",
    "pentacles": "pe",
}

# Court cards and aces use letter codes; numbered cards use zero-padded digits
NUMBER_SUFFIX = {
    1: "ac",   # Ace
    11: "pa",  # Page
    12: "kn",  # Knight
    13: "qu",  # Queen
    14: "ki",  # King
}

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

downloaded = 0
skipped = 0
failed = []

for card in data["cards"]:
    if card["arcana"] == "major":
        suffix = str(card["number"]).zfill(2)
        source_url = f"{BASE_URL}/ar{suffix}.jpg"
    else:
        abbrev = SUIT_ABBREV[card["suit"]]
        suffix = NUMBER_SUFFIX.get(card["number"], str(card["number"]).zfill(2))
        source_url = f"{BASE_URL}/{abbrev}{suffix}.jpg"

    save_path = IMAGES_DIR / card["image_filename"]

    if save_path.exists():
        print(f"  Skipped (already exists): {card['image_filename']}")
        skipped += 1
        continue

    try:
        response = requests.get(source_url, timeout=10)
        if response.status_code == 200:
            save_path.write_bytes(response.content)
            print(f"  Downloaded: {card['image_filename']}")
            downloaded += 1
        else:
            print(f"  FAILED [{response.status_code}]: {card['name']} — {source_url}")
            failed.append(card["name"])
    except requests.RequestException as e:
        print(f"  ERROR: {card['name']} — {e}")
        failed.append(card["name"])

    time.sleep(0.5)

print(f"\nDone. {downloaded} downloaded, {skipped} skipped, {len(failed)} failed.")
if failed:
    print(f"Failed: {', '.join(failed)}")
    print("Check URLs manually at https://www.sacred-texts.com/tarot/pkt/img/")
