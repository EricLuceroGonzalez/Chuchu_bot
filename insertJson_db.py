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


def update_text_by_id():
    """To take the json and compare with "texto" in mongo,
    and update if there is a difference
    """
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for item in data:
        doc_id = item.get("id")
        new_text = item.get("texto")
        if doc_id is not None and new_text is not None:
            mongo_doc = collection.find_one({"id": doc_id})
            if mongo_doc and mongo_doc.get("texto") != new_text:
                result = collection.update_one(
                    {"id": doc_id}, {"$set": {"texto": new_text}}
                )
                if result.modified_count:
                    print(f"Updated id {doc_id}")
                    updated += 1
    print(f"Total updated: {updated}")


update_text_by_id()
# insert_json_to_mongo()
