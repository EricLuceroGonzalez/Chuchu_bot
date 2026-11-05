"""Interfaz común para todas las redes sociales."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Media:
    data: bytes
    mime_type: str = "image/jpeg"
    alt: str = ""
    width: int | None = None
    height: int | None = None


class PublisherUnavailable(Exception):
    """La red no está disponible ahora (sin créditos, rate limit, etc.).
    Se registra como aviso y el bot sigue con las demás redes."""


class Publisher(ABC):
    name: str = "base"
    MAX_CHARS: int = 280

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        if not dry_run:
            self.connect()

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def _post(self, text: str, media: Media | None) -> str:
        """Publica y devuelve un identificador (id o URI) del post."""

    def fits(self, text: str) -> bool:
        return len(text) <= self.MAX_CHARS

    def publish(self, text: str, media: Media | None = None) -> str:
        if not self.fits(text):
            raise ValueError(f"[{self.name}] texto demasiado largo ({len(text)}/{self.MAX_CHARS})")
        if self.dry_run:
            extra = f" + imagen ({len(media.data) // 1024} KB)" if media else ""
            logger.info(f"[DRY-RUN][{self.name}] Publicaría{extra}:\n{text}")
            return "dry-run"
        post_id = self._post(text, media)
        logger.info(f"✅ [{self.name}] publicado: {post_id}")
        return post_id
