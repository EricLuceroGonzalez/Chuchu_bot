"""Publisher de Bluesky (AT Protocol). Gratis, sin API key: handle + App Password."""

import logging
import os
import re
from pathlib import Path

from .base import Media, Publisher, PublisherUnavailable

logger = logging.getLogger(__name__)

# La sesión se guarda en disco para no hacer login en cada ejecución
# (Bluesky limita la creación de sesiones: 30 cada 5 min / 300 al día).
SESSION_FILE = Path(__file__).resolve().parent.parent / ".bsky_session"
HASHTAG_RE = re.compile(r"(?<!\w)#(\w+)")


class BlueskyPublisher(Publisher):
    name = "bluesky"
    # El límite real son 300 grafemas. len() cuenta code points, que siempre es
    # >= grafemas (un emoji como 🎞️ son 2 code points), así que es conservador.
    MAX_CHARS = 300
    MAX_BYTES = 3000
    MAX_TAGS = 2

    def connect(self) -> None:
        from atproto import Client

        self.client = Client(base_url=os.getenv("BSKY_SERVICE") or None)

        if SESSION_FILE.exists():
            try:
                self.client.login(session_string=SESSION_FILE.read_text().strip())
                logger.info("Bluesky: sesión reutilizada.")
                self._save_session()
                return
            except Exception as e:
                logger.info(f"Bluesky: sesión guardada inválida ({e}); login de nuevo.")

        handle = os.getenv("BSKY_HANDLE")
        password = os.getenv("BSKY_APP_PASSWORD")
        if not handle or not password:
            raise ValueError("Faltan BSKY_HANDLE o BSKY_APP_PASSWORD en el .env")
        self.client.login(handle, password)
        logger.info(f"Bluesky: conectado como {handle}.")
        self._save_session()

    def _save_session(self) -> None:
        try:
            SESSION_FILE.write_text(self.client.export_session_string())
            SESSION_FILE.chmod(0o600)
        except Exception as e:
            logger.warning(f"Bluesky: no se pudo guardar la sesión: {e}")

    @staticmethod
    def _rich_text(text: str):
        """En Bluesky los #hashtags solo son clicables si van como 'facets'."""
        from atproto import client_utils

        tb = client_utils.TextBuilder()
        pos = 0
        for m in HASHTAG_RE.finditer(text):
            tb.text(text[pos:m.start()])
            tb.tag(m.group(0), m.group(1))
            pos = m.end()
        tb.text(text[pos:])
        return tb

    def fits(self, text: str) -> bool:
        return super().fits(text) and len(text.encode("utf-8")) <= self.MAX_BYTES

    def _post(self, text: str, media: Media | None) -> str:
        from atproto import models
        from atproto_client.exceptions import RequestException

        rich = self._rich_text(text)
        try:
            if media:
                aspect = None
                if media.width and media.height:
                    aspect = models.AppBskyEmbedDefs.AspectRatio(
                        width=media.width, height=media.height
                    )
                r = self.client.send_image(
                    text=rich,
                    image=media.data,
                    image_alt=media.alt,
                    image_aspect_ratio=aspect,
                    langs=["es"],
                )
            else:
                r = self.client.send_post(text=rich, langs=["es"])
        except RequestException as e:
            status = getattr(getattr(e, "response", None), "status_code", None)
            if status == 429:
                raise PublisherUnavailable("Bluesky rate limit (429)") from e
            raise
        self._save_session()  # el token puede haberse refrescado
        return r.uri
