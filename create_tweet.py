import random
from datetime import datetime
import os
import logging
from media_upload import media_upload

logger = logging.getLogger(__name__)


def create_tweet(text, twitter_client, twitter_api, media_ids=None):
    """
    Create a tweet with optional media attachments.

    :param text: The text content of the tweet.
    :param media_ids: A list of media IDs to attach to the tweet.
    :return: The response from the Twitter API.
    """

    # Lista de emojis relevantes para contenido histórico/archivístico
    EMOJIS = {
        "opener": [
            "🎞️",
            "👀",
            "💾",
            "🌟",
            "🎯",
            "📌",
            "🌀",
        ],
        "libro": ["📚", "🧾", "📕", "🔖", "📓", "📗", "📖", "👓", "📝"],
    }
    emoji_opener = random.choice(EMOJIS["opener"])
    emoji_book = random.choice(EMOJIS["libro"])
    # Construir texto principal
    if random.random() < 0.2:
        tweet_text = f'{emoji_opener}"{text["texto"]}"\n {emoji_book}{text["libro"]} ({text["año"]}).'
    else:
        tweet_text = f'"{text["texto"]}"\n{text["libro"]} ({text["año"]})'

    # Construir tweet completo
    if random.random() < 0.1:  # 10% chance to include image
        logging.info(f"Creating tweet with text:\n {tweet_text}")
        temp_image = f"{os.path.dirname(__file__)}/temp_image.jpg"
        mediaID = media_upload(text["portada"], temp_image, twitter_api)
        twitter_client.create_tweet(text=tweet_text, media_ids=[mediaID])
    else:  # No media, just text
        logging.info(f"Creating tweet with text:\n {tweet_text}")
        twitter_client.create_tweet(text=tweet_text)
    return "e"
