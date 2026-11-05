"""Carga la portada (URL o ruta local) y la comprime para que quepa en
todas las redes (Bluesky limita cada imagen a ~1 MB)."""

import io
import logging
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

from publishers import Media

logger = logging.getLogger(__name__)

MAX_BYTES = 950_000
MAX_SIDE = 2000


def _read(src: str) -> bytes:
    if src.startswith(("http://", "https://")):
        req = urllib.request.Request(src, headers={"User-Agent": "chuchu-bot/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read()
    return Path(src).read_bytes()


def load_cover(src: str, alt: str = "") -> Media | None:
    try:
        img = Image.open(io.BytesIO(_read(src)))
        img = ImageOps.exif_transpose(img).convert("RGB")
        img.thumbnail((MAX_SIDE, MAX_SIDE))

        while True:
            for quality in (85, 75, 65, 55, 45):
                buf = io.BytesIO()
                img.save(buf, "JPEG", quality=quality, optimize=True)  # sin EXIF
                if buf.tell() <= MAX_BYTES:
                    return Media(buf.getvalue(), "image/jpeg", alt, img.width, img.height)
            img = img.resize((int(img.width * 0.8), int(img.height * 0.8)))
    except Exception as e:
        logger.warning(f"No se pudo preparar la portada ({src}): {e}")
        return None
