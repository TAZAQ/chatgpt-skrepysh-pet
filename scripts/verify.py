"""Verify the distributable pet package without third-party dependencies."""

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FILES = {
    "spritesheet.png",
    "skrepysh/spritesheet.webp",
    "skrepysh/pet.json",
    "demo.gif",
}


def verify():
    checksums = json.loads((ROOT / "checksums.json").read_text(encoding="utf-8"))
    if set(checksums) != REQUIRED_FILES:
        raise ValueError("checksums.json must cover exactly the four distributable files")

    for name, expected in checksums.items():
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError(f"Invalid SHA-256 digest: {name}")
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"SHA-256 mismatch: {name}")
        print(f"OK  {name}")

    pet = json.loads((ROOT / "skrepysh/pet.json").read_text(encoding="utf-8"))
    if pet.get("id") != "skrepysh":
        raise ValueError("Pet ID must match the skrepysh directory")
    if type(pet.get("spriteVersionNumber")) is not int or pet["spriteVersionNumber"] != 2:
        raise ValueError("Expected spriteVersionNumber 2")
    if pet.get("spritesheetPath") != "spritesheet.webp":
        raise ValueError("Expected the bundled spritesheet.webp")
    for key in ("displayName", "description"):
        if not isinstance(pet.get(key), str) or not pet[key].strip():
            raise ValueError(f"Missing or empty pet {key}")
    print("OK  pet manifest")


if __name__ == "__main__":
    try:
        verify()
    except (OSError, ValueError, TypeError, AttributeError) as error:
        print(f"ERROR  {error}", file=sys.stderr)
        sys.exit(1)
    print("Package integrity verified.")
