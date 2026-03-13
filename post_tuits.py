from connect_DB import get_mongo_collection
from connect_Twitter import connect_to_twitter
from create_tweet import create_tweet
import logging
import os
import sys
from datetime import datetime

log_file = os.path.join(os.path.dirname(__file__), "chuchu_bot.log")
# file_path = os.path.join(os.path.dirname(__file__), "data.json")
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
today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"***** ***** ***** {today} ***** ***** *****")


def get_one_document(collection, x_client, x_api):
    logger.info("Iniciando búsqueda de tuit...")
    intentos = 0
    max_intentos = 10

    while intentos < max_intentos:
        try:
            pipeline = [{"$match": {"enviado": {"$lt": 3}}}, {"$sample": {"size": 1}}]
            random_item = list(collection.aggregate(pipeline))

            if not random_item:
                logger.warning(
                    "Consulta a MongoDB vacía. Revisa si quedan documentos con enviado < 3."
                )
                return None

            item = random_item[0]
            # Logueamos ID para rastrearlo
            logger.info(
                f"Candidato hallado: ID {item.get('_id')} | Intentos: {intentos + 1}"
            )

            # Cálculo de longitud (ajusta según formato de string en create_tweet)
            longitud_texto = len(item.get("texto", "")) + len(item.get("libro", "")) + 6

            if longitud_texto < 280:
                logger.info(f"✅ Tuit válido: {item['texto'][:40]}...")
                create_tweet(item, x_client, x_api)
                # Actualización en db
                collection.update_one(
                    {"_id": item["_id"]},
                    {"$set": {"publicado": True}, "$inc": {"enviado": 1}},
                )
                return item
            else:
                logger.info(f"❌ Descartado por largo ({longitud_texto} chars).")

        except Exception as e:
            logger.error(f"Error crítico: {e}")
            break

        intentos += 1
    return None


def get_one_documents():
    max_intentos = 10
    intentos = 0

    while intentos < max_intentos:
        # Filtramos directamente en la base de datos por los que no han superado el límite de envíos
        pipeline = [{"$match": {"enviado": {"$lt": 3}}}, {"$sample": {"size": 1}}]
        random_item = list(collection.aggregate(pipeline))

        if not random_item:
            logger.warning(
                "No quedan ítems disponibles para publicar (todos enviados 3 veces)."
            )
            return None

        item = random_item[0]
        # Cálculo de longitud (ajusta según tu formato de string en create_tweet)
        longitud_texto = len(item.get("texto", "")) + len(item.get("libro", "")) + 6

        if longitud_texto < 280:
            try:
                logger.info(f"(TEST)Publicando: {item['texto'][:30]}...")
                # create_tweet(item, x_client, x_api)

                # # Actualización atómica
                # collection.update_one(
                #     {"_id": item["_id"]},
                #     {"$set": {"publicado": True}, "$inc": {"enviado": 1}},
                # )
                return item
            except Exception as e:
                logger.error(f"Fallo en la comunicación con X: {e}")
                break  # Salimos para evitar bucles de error de red

        intentos += 1
        logger.info(f"Documento muy largo, reintentando... (Intento {intentos})")

    logger.error("Se alcanzó el máximo de intentos sin encontrar un tuit válido.")
    return None


if __name__ == "__main__":
    try:
        # Ahora el log se iniciará ANTES de intentar conectar
        logger.info("--- INICIANDO PROCESO DEL BOT ---")

        # Conectamos dentro del try para capturar errores en el log
        collection = get_mongo_collection()
        x_client, x_api = connect_to_twitter()

        if collection is not None and x_client is not None:
            get_one_document(collection, x_client, x_api)
        else:
            logger.error("No se pudo establecer conexión con los servicios.")

    except Exception as e:
        # Esto guardará cualquier error de conexión en el log
        logger.critical(f"--- EL BOT NO PUDO ARRANCAR: {e}", exc_info=True)
    finally:
        logger.info("--- FIN DE LA EJECUCIÓN ---")
