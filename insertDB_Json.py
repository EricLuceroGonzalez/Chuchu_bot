import json
import os
from connect_DB import get_mongo_collection
from bson import ObjectId

collection = get_mongo_collection()
file = os.path.join(os.path.dirname(__file__), "todas_las_citas.json")


def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def insertDB_to_JSON():
    print("Inserting data from JSON to MongoDB...")
    print(file)
    cursor_db = collection.find()
    json_data = list(cursor_db)
    print(f"Number of documents in DB: {len(json_data)}")
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(
                json_data, f, default=convert_objectid, ensure_ascii=False, indent=4
            )
    except Exception as e:
        print(f"Error writing to JSON file: {e}")
    print(f"Data successfully written to {file}")


insertDB_to_JSON()
