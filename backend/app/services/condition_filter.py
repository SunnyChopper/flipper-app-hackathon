from __future__ import annotations

import re

from app.models.listing import Listing

BROKEN_LABELS = (
    "for parts",
    "not working",
    "parts only",
    "damaged",
    "broken",
    "poor",
    "fair",
    "defective",
    "faulty",
)

BROKEN_PHRASES = (
    "for parts",
    "parts only",
    "not working",
    "doesn't work",
    "does not work",
    "dont work",
    "won't turn on",
    "wont turn on",
    "won't power",
    "wont power",
    "no power",
    "no picture",
    "no video",
    "no display",
    "water damage",
    "liquid damage",
    "cracked",
    "cracked screen",
    "shattered",
    "smashed",
    "broken",
    "dented",
    "spidered",
    "swollen",
    "battery swollen",
    "dead",
    "faulty",
    "defective",
    "as-is for repair",
    "as is for repair",
    "needs repair",
    "needs fixing",
    "sold for parts",
)

NEW_OR_GOOD_PHRASES = (
    "brand new",
    "new in box",
    "never used",
    "like new",
    "mint",
    "excellent condition",
    "open box",
    "refurbished",
)


def looks_broken_or_poor(listing: Listing) -> bool:
    """Keep listings that are broken, for parts, or clearly in bad condition."""
    label = (listing.condition_label or "").lower()
    blob = f"{listing.title} {listing.description} {label}"
    normalized = _normalize(blob)

    if any(phrase in normalized for phrase in NEW_OR_GOOD_PHRASES) and not _has_breakage(normalized, label):
        return False
    return _has_breakage(normalized, label)


def _has_breakage(normalized: str, label: str) -> bool:
    if any(token in label for token in BROKEN_LABELS):
        return True
    return any(phrase in normalized for phrase in BROKEN_PHRASES)


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
