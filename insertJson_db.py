import json
import os
from connect_DB import get_mongo_collection

collection = get_mongo_collection()
file = os.path.join(os.path.dirname(__file__), "todas_las_citas.json")


def insert_json_to_mongo():
    """Insert JSON data into MongoDB collection.
    This function reads a JSON file and inserts its contents into a MongoDB collection.
    If the data is a list of documents, it checks for duplicates based on the "texto" field
    before inserting each document. If the data is not a list, it prints an error message.
    """
    # Load JSON file
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # If data is a list of documents:
    if isinstance(data, list):
        # Optionally, avoid duplicates (e.g., by "texto")
        for item in data:
            if not collection.find_one({"texto": item.get("texto")}):
                collection.insert_one(item)
                # print(f"Inserted: {item.get('texto')}")
            else:
                print(f"Already exists: {item.get('texto')}")
    else:
        print("JSON file does not contain a list of documents.")


insert_json_to_mongo()
