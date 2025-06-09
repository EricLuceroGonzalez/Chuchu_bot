import os
import logging
import requests

logger = logging.getLogger(__name__)


def media_upload(image_path, temp_image, twitter_api):
    """
    Uploads an image to Twitter and returns the media ID.
    """
    try:
        logging.info(f"Downloading image from Cloud..")
        image_response = requests.get(image_path)
        with open(temp_image, "wb") as img_file:
            img_file.write(image_response.content)
    except Exception as e:
        logging.error(f"On writing image file: {e}")
        return None
    try:
        # Upload the image to Twitter
        media = twitter_api.media_upload(temp_image)
        logging.info(f"Uploading image to Twitter...")
        return media.media_id
    except Exception as e:
        logging.error(f"On uploading image to Twitter: {e}")
        return None
    finally:
        # Remove the temporary image file
        if os.path.exists(temp_image):
            os.remove(temp_image)
            logging.info(f"Temporary image file removed.")
        else:
            logging.warning(f"Temporary image file does not exist.")
