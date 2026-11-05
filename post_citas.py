"""Punto de entrada del bot: elige una cita de MongoDB y la publica en las
redes activas (ENABLED_PLATFORMS). Sustituye a post_tuits.py."""

import logging
import os
import random
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv

from formatter import alt_text, base_text, choose_style, compose
from images import load_cover
from publishers import PublisherUnavailable, build_publishers

load_dotenv()

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chuchu_bot.log")
logging.basicConfig(
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)
# Silenciar el ruido HTTP de las librerías
for noisy in ("httpx", "httpcore", "urllib3"):
    logging.getLogger(noisy).setLevel(logging.WARNING)

PIPELINE = [
    {"$match": {"enviado": {"$lt": 2}}},  # enviado < 2
    {"$sort": {"enviado": 1}},            # prioridad a los menos enviados
    {"$limit": 20},
    {"$sample": {"size": 1}},
]


def pick_quote(collection, style, max_len: int, max_intentos: int = 10):
    """Devuelve un documento cuya cita (sin hashtags) quepa en todas las redes activas."""
    for intento in range(1, max_intentos + 1):
        candidatos = list(collection.aggregate(PIPELINE))
        if not candidatos:
            logger.warning("Consulta a MongoDB vacía. ¿Quedan documentos con enviado < 2?")
            return None
        item = candidatos[0]
        largo = len(base_text(item, style))
        logger.info(f"Candidato ID {item.get('_id')} | intento {intento} | {largo} chars")
        if largo <= max_len:
            return item
        logger.info(f"❌ Descartado por largo ({largo} > {max_len}).")
    logger.warning(f"Ninguna cita válida tras {max_intentos} intentos.")
    return None


def run(collection, publishers, dry_run: bool = False) -> dict[str, str]:
    style = choose_style()  # mismo estilo (emojis) en todas las redes
    max_len = min(p.MAX_CHARS for p in publishers)
    item = pick_quote(collection, style, max_len)
    if item is None:
        return {}

    media = None
    prob = float(os.getenv("PROB_IMAGEN", "0.1"))
    if item.get("portada") and random.random() < prob:
        media = load_cover(item["portada"], alt=alt_text(item))

    resultados: dict[str, str] = {}
    for p in publishers:
        try:
            texto = compose(item, style, p.MAX_CHARS, p.MAX_TAGS)
            resultados[p.name] = p.publish(texto, media)
        except PublisherUnavailable as e:
            logger.warning(f"⚠️ [{p.name}] omitido: {e}")
        except Exception:
            logger.exception(f"Error publicando en {p.name}")

    if dry_run:
        logger.info("DRY-RUN: no se actualiza MongoDB.")
    elif resultados:
        ahora = datetime.now(timezone.utc)
        set_fields = {"publicado": True}
        for red, post_id in resultados.items():
            set_fields[f"publicaciones.{red}"] = {"id": post_id, "fecha": ahora}
        collection.update_one(
            {"_id": item["_id"]},
            {
                "$set": set_fields,
                "$inc": {"enviado": 1},
                "$currentDate": {"fecha_ultimo_post": True},
            },
        )
        logger.info(f"MongoDB actualizado: {item['_id']} → {list(resultados)}")
    else:
        logger.error("No se publicó en ninguna red; MongoDB sin cambios.")
    return resultados


def main() -> int:
    logger.info(f"***** {datetime.now():%Y-%m-%d %H:%M:%S} — INICIANDO BOT *****")
    dry_run = os.getenv("DRY_RUN", "0") == "1" or "--dry-run" in sys.argv
    redes = [r.strip().lower() for r in os.getenv("ENABLED_PLATFORMS", "bluesky").split(",") if r.strip()]
    logger.info(f"Redes activas: {redes}{' (DRY-RUN)' if dry_run else ''}")

    try:
        publishers = build_publishers(redes, dry_run=dry_run)
        if not publishers:
            logger.error("Ninguna red disponible. Revisa ENABLED_PLATFORMS y credenciales.")
            return 1

        from connect_DB import get_mongo_collection
        collection = get_mongo_collection()
        if collection is None:
            logger.error("No se pudo conectar a MongoDB.")
            return 1

        return 0 if run(collection, publishers, dry_run) else 1
    except Exception as e:
        logger.critical(f"--- EL BOT NO PUDO ARRANCAR: {e}", exc_info=True)
        return 1
    finally:
        logger.info("--- FIN DE LA EJECUCIÓN ---")


if __name__ == "__main__":
    sys.exit(main())
