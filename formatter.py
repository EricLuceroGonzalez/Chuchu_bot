"""Construye el texto de cada post a partir de un documento de MongoDB.

Formato:
    "texto de la cita"

    — Autor, Libro (año)

    #citas #Autor
"""

import random
import re
from dataclasses import dataclass

EMOJIS = {
    "opener": ["🎞️", "👀", "💾", "🌟", "🎯", "📌", "🌀"],
    "libro": ["📚", "🧾", "📕", "🔖", "📓", "📗", "📖", "👓", "📝"],
}
PROB_EMOJIS = 0.2
MAX_TAG_LEN = 30


@dataclass
class Style:
    """Se decide una vez por ejecución para que todas las redes lleven el mismo estilo."""
    opener: str = ""
    book: str = ""


def choose_style() -> Style:
    if random.random() < PROB_EMOJIS:
        return Style(random.choice(EMOJIS["opener"]), random.choice(EMOJIS["libro"]))
    return Style()


def _clean(value) -> str:
    return str(value).strip() if value not in (None, "") else ""


def to_hashtag(value: str) -> str:
    """'Gabriel García Márquez' → 'GabrielGarcíaMárquez'. Conserva tildes y ñ."""
    words = re.findall(r"\w+", value)
    return "".join(w[0].upper() + w[1:] for w in words if w)


def source_line(item: dict, style: Style) -> str:
    autor, libro, año = (_clean(item.get(k)) for k in ("autor", "libro", "año"))
    obra = f"{libro} ({año})" if libro and año else libro or año
    partes = ", ".join(p for p in (autor, obra) if p)
    if not partes:
        return ""
    return f"{style.book} {partes}" if style.book else f"— {partes}"


def base_text(item: dict, style: Style) -> str:
    texto = _clean(item.get("texto"))
    cita = f'{style.opener} "{texto}"' if style.opener else f'"{texto}"'
    fuente = source_line(item, style)
    return f"{cita}\n\n{fuente}" if fuente else cita


def candidate_tags(item: dict) -> list[str]:
    """Hashtags por orden de prioridad."""
    tags = ["citas"]
    for campo in ("autor",):
        if (t := to_hashtag(_clean(item.get(campo)))) and len(t) <= MAX_TAG_LEN:
            tags.append(t)
    tags.append("libros")
    if (t := to_hashtag(_clean(item.get("libro")))) and len(t) <= MAX_TAG_LEN:
        tags.append(t)
    tags.append("literatura")
    # sin duplicados (sin distinguir mayúsculas)
    vistos, unicos = set(), []
    for t in tags:
        if t.lower() not in vistos:
            vistos.add(t.lower())
            unicos.append(t)
    return unicos


def compose(item: dict, style: Style, max_chars: int, max_tags: int) -> str:
    """Texto final para una red: base + todos los hashtags que quepan."""
    base = base_text(item, style)
    tags: list[str] = []
    for t in candidate_tags(item)[:max_tags]:
        prueba = f"{base}\n\n" + " ".join(f"#{x}" for x in [*tags, t])
        if len(prueba) <= max_chars:
            tags.append(t)
        else:
            break
    return f"{base}\n\n" + " ".join(f"#{t}" for t in tags) if tags else base


def alt_text(item: dict) -> str:
    libro, autor, año = (_clean(item.get(k)) for k in ("libro", "autor", "año"))
    alt = f"Portada del libro «{libro}»" if libro else "Portada del libro"
    if autor:
        alt += f", de {autor}"
    if año:
        alt += f" ({año})"
    return alt + "."
