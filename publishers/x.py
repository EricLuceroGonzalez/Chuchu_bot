"""Publisher de X. DESACTIVADO por defecto: la API de X es de pago por uso.
Para reactivarlo: `uv sync --extra x` y añadir "x" a ENABLED_PLATFORMS."""

import io
import logging
import os

from .base import Media, Publisher, PublisherUnavailable

logger = logging.getLogger(__name__)


def _cred(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Falta la variable de entorno {name}")
    return value


class XPublisher(Publisher):
    name = "x"
    MAX_CHARS = 280

    def connect(self) -> None:
        import tweepy

        self.client = tweepy.Client(
            consumer_key=_cred("X_API_KEY"),
            consumer_secret=_cred("X_API_KEY_SECRET"),
            access_token=_cred("X_ACCESS_TOKEN"),
            access_token_secret=_cred("X_ACCESS_TOKEN_SECRET"),
        )
        auth = tweepy.OAuth1UserHandler(
            _cred("X_API_KEY"),
            _cred("X_API_KEY_SECRET"),
            _cred("X_ACCESS_TOKEN"),
            _cred("X_ACCESS_TOKEN_SECRET"),
        )
        self.api = tweepy.API(auth)  # v1.1, solo para subir imágenes

    def _post(self, text: str, media: Media | None) -> str:
        import tweepy

        try:
            media_ids = None
            if media:
                up = self.api.media_upload(filename="portada.jpg", file=io.BytesIO(media.data))
                media_ids = [up.media_id]
            r = self.client.create_tweet(text=text, media_ids=media_ids)
        except tweepy.errors.HTTPException as e:
            status = getattr(e.response, "status_code", None)
            if status == 402:
                raise PublisherUnavailable("X sin créditos (402 Payment Required)") from e
            if status == 429:
                raise PublisherUnavailable("X rate limit (429)") from e
            raise
        return str(r.data["id"])
