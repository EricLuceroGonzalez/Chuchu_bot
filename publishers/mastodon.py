"""Publisher de Mastodon. Gratis: token de acceso creado en
Preferencias → Desarrollo → Nueva aplicación (permiso write:statuses y write:media)."""

import io
import logging
import os

from .base import Media, Publisher, PublisherUnavailable

logger = logging.getLogger(__name__)


class MastodonPublisher(Publisher):
    name = "mastodon"
    MAX_CHARS = 500  # valor por defecto; algunas instancias permiten más

    def connect(self) -> None:
        from mastodon import Mastodon

        base_url = os.getenv("MASTODON_BASE_URL")
        token = os.getenv("MASTODON_ACCESS_TOKEN")
        if not base_url or not token:
            raise ValueError("Faltan MASTODON_BASE_URL o MASTODON_ACCESS_TOKEN en el .env")
        self.client = Mastodon(access_token=token, api_base_url=base_url)
        if os.getenv("MASTODON_MAX_CHARS"):
            self.MAX_CHARS = int(os.environ["MASTODON_MAX_CHARS"])
        logger.info(f"Mastodon: conectado a {base_url}.")

    def _post(self, text: str, media: Media | None) -> str:
        from mastodon import MastodonRatelimitError

        try:
            media_ids = None
            if media:
                m = self.client.media_post(
                    io.BytesIO(media.data),
                    mime_type=media.mime_type,
                    description=media.alt,
                    file_name="portada.jpg",
                )
                media_ids = [m["id"]]
            status = self.client.status_post(
                text, media_ids=media_ids, language="es", visibility="public"
            )
        except MastodonRatelimitError as e:
            raise PublisherUnavailable("Mastodon rate limit") from e
        return status["url"] or str(status["id"])
