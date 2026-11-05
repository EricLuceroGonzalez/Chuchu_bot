"""Construye el texto del post a partir de un documento de MongoDB."""

import random

EMOJIS = {
    "opener": ["🎞️", "👀", "💾", "🌟", "🎯", "📌", "🌀"],
    "libro": ["📚", "🧾", "📕", "🔖", "📓", "📗", "📖", "👓", "📝"],
}


def build_text(item: dict) -> str:
    texto = item.get("texto", "").strip()
    libro = item.get("libro", "").strip()
    año = item.get("año")
    fuente = f"{libro} ({año})" if año else libro

    if random.random() < 0.2:
        opener = random.choice(EMOJIS["opener"])
        book = random.choice(EMOJIS["libro"])
        return f'{opener}"{texto}"\n{book}{fuente}.'
    return f'"{texto}"\n{fuente}'
