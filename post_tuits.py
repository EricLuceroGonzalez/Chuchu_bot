from connect_DB import get_mongo_collection
from connect_Twitter import connect_to_twitter
from create_tweet import create_tweet
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

# file_path = os.path.join(os.path.dirname(__file__), "data.json")
logging.basicConfig(
    filename=f"{os.path.dirname(__file__)}/chuchu_bot.log",
    encoding="utf-8",
    format="%(levelname)s:%(message)s",
    level=logging.INFO,
)
today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.info(f"***** ***** ***** {today} ***** ***** *****")

# Connect to MongoDB and Twitter
collection = get_mongo_collection()
x_client, x_api = connect_to_twitter()


def get_one_document():
    while True:
        # Get one random document from the collection
        random_item = collection.aggregate([{"$sample": {"size": 1}}])
        random_item = list(random_item)  # Convert cursor to list

        if not random_item:
            logging.error("No items found in the collection.")
            return None
        # Check the length of characters in tweet text (< 280)
        lengt_text = len(random_item[0]["texto"]) + len(random_item[0]["libro"]) + 6
        if (
            (random_item[0].get("publicado") is not True)
            and (random_item[0].get("enviado", 0) < 3)
            and (lengt_text < 280)
        ):
            # Create a tweet with the random item
            create_tweet(random_item[0], x_client, x_api)

            # Update the document to set "publicado" to True and +1 to "enviado"
            # collection.update_one(
            #     {"_id": random_item[0]["_id"]},
            #     {"$set": {"publicado": True}, "$inc": {"enviado": 1}},
            # )
            logging.info(f"id/_id:{random_item[0]["id"]}/{random_item[0]["_id"]}")
            return random_item[0]
        # If publicado is True, loop again to get another random item


get_one_document()
