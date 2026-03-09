import tweepy
import os
from dotenv import load_dotenv
import logging

import tweepy.errors

logger = logging.getLogger(__name__)

load_dotenv()


# Get credentials with error handling
def get_credential(name):
    value = os.getenv(name)
    if not value:
        logging.info(f"Missing required environment variable: {name}")
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def connect_to_twitter():
    try:
        client = tweepy.Client(
            bearer_token=get_credential("X_BEARER_TOKEN"),
            consumer_key=get_credential("X_API_KEY"),
            consumer_secret=get_credential("X_API_KEY_SECRET"),
            access_token=get_credential("X_ACCESS_TOKEN"),
            access_token_secret=get_credential("X_ACCESS_TOKEN_SECRET"),
        )

        auth = tweepy.OAuth1UserHandler(
            get_credential("X_API_KEY"),
            get_credential("X_API_KEY_SECRET"),
            get_credential("X_ACCESS_TOKEN"),
            get_credential("X_ACCESS_TOKEN_SECRET"),
        )

        # auth.set_access_token(
        #     os.getenv("X_ACCESS_TOKEN"),
        #     os.getenv("X_ACCESS_TOKEN_SECRET"),
        # )

        api = tweepy.API(auth)
        logging.info("Connected to Twitter successfully!")
        return client, api
    except tweepy.errors.TweepyException as e:
        logging.error(f"Tweepy error on: {e}")
