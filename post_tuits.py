from connect_DB import get_mongo_collection
from connect_Twitter import connect_to_twitter
from create_tweet import create_tweet
import logging
import os
from datetime import datetime


# file_path = os.path.join(os.path.dirname(__file__), "data.json")
logging.basicConfig(
    filename=f"{os.path.dirname(__file__)}/chuchu_bot.log",
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"***** ***** ***** {today} ***** ***** *****")

# Connect to MongoDB and Twitter
collection = get_mongo_collection()
x_client, x_api = connect_to_twitter()

# ... (imports igual)


def get_one_document():
    logger.info("Iniciando búsqueda de tuit...")  # Para saber que la función arrancó
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
            # Logueamos qué ID hemos pescado para rastrearlo
            logger.info(
                f"Candidato hallado: ID {item.get('_id')} | Intentos: {intentos + 1}"
            )

            # Cálculo de longitud (ajusta según tu formato de string en create_tweet)
            longitud_texto = len(item.get("texto", "")) + len(item.get("libro", "")) + 6

            if longitud_texto < 280:
                logger.info(f"✅ Tuit válido: {item['texto'][:40]}...")
                # DESCOMENTA ESTO PARA QUE FUNCIONE
                # create_tweet(item, x_client, x_api)
                return item
            else:
                logger.info(f"❌ Descartado por largo ({longitud_texto} chars).")

        except Exception as e:
            logger.error(f"Error crítico dentro del bucle: {e}")
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
        logger.info("--- EJECUCIÓN INICIADA ---")
        get_one_document()
        logger.info("--- EJECUCIÓN FINALIZADA ---")
    except Exception as e:
        logger.critical(f"EL BOT SE HA CAÍDO ANTES DE EMPEZAR: {e}", exc_info=True)
