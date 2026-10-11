"""Append five automatically generated lines once per India calendar day."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import random


INDIA_TIME = timezone(timedelta(hours=5, minutes=30))
NOTES = (
    "A tiny paper boat drifts across a quiet pond.",
    "The evening sky carries a soft ribbon of orange.",
    "A curious sparrow pauses beside an open window.",
    "Fresh rain leaves silver beads on the garden leaves.",
    "An old notebook waits for a brand new idea.",
    "A cup of tea warms a peaceful corner of the room.",
    "The moon rises slowly above the sleeping rooftops.",
    "A winding path disappears between tall green trees.",
    "A gentle breeze turns the pages of a forgotten book.",
    "Small lanterns glow along the riverside walkway.",
    "A bright kite dances above the crowded marketplace.",
    "Morning sunlight paints golden squares on the floor.",
    "The distant hills fade into a pale blue horizon.",
    "A bicycle bell rings down the narrow cobbled lane.",
    "Clouds gather like soft pillows over the valley.",
    "A little stream hums beneath a wooden bridge.",
    "The first star appears before the streetlights glow.",
    "A quiet library holds a thousand possible adventures.",
    "A sunflower leans toward the last light of the day.",
    "The smell of fresh bread floats through the morning air.",
)


def append_daily_notes(path: Path, now: datetime | None = None) -> bool:
    day = (now or datetime.now(INDIA_TIME)).astimezone(INDIA_TIME).date()
    prefix = f"{day.isoformat()} | "
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if any(line.startswith(prefix) for line in existing.splitlines()):
        print(f"An entry for {day} already exists; skipping.")
        return False

    lines = [prefix + note for note in random.sample(NOTES, 5)]
    separator = "\n" if existing and not existing.endswith("\n") else ""
    with path.open("a", encoding="utf-8", newline="\n") as log:
        log.write(separator + "\n".join(lines) + "\n")
    print(f"Added five automatically generated lines for {day}.")
    return True


if __name__ == "__main__":
    append_daily_notes(Path(__file__).resolve().parents[2] / "daily-notes.txt")
