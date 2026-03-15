import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from connect_DB import get_mongo_collection

collection = get_mongo_collection()
file = os.path.join(os.path.dirname(__file__), "todas_las_citas.json")

with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)


print(len(data))
