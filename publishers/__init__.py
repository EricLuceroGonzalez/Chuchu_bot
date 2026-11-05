import logging

from .base import Media, Publisher, PublisherUnavailable

logger = logging.getLogger(__name__)

__all__ = ["Media", "Publisher", "PublisherUnavailable", "build_publishers"]


def _registry() -> dict[str, type[Publisher]]:
    # Imports perezosos: si una librería no está instalada (p. ej. tweepy),
    # solo falla esa red, no el bot entero.
    reg: dict[str, type[Publisher]] = {}
    try:
        from .bluesky import BlueskyPublisher
        reg["bluesky"] = BlueskyPublisher
    except ImportError as e:
        logger.debug(f"bluesky no disponible: {e}")
    try:
        from .mastodon import MastodonPublisher
        reg["mastodon"] = MastodonPublisher
    except ImportError as e:
        logger.debug(f"mastodon no disponible: {e}")
    try:
        from .x import XPublisher
        reg["x"] = XPublisher
    except ImportError as e:
        logger.debug(f"x no disponible: {e}")
    return reg


def build_publishers(names: list[str], dry_run: bool = False) -> list[Publisher]:
    reg = _registry()
    publishers: list[Publisher] = []
    for name in names:
        cls = reg.get(name)
        if cls is None:
            logger.error(f"Red '{name}' desconocida o su librería no está instalada.")
            continue
        try:
            publishers.append(cls(dry_run=dry_run))
        except Exception as e:
            logger.error(f"No se pudo conectar a {name}: {e}")
    return publishers
