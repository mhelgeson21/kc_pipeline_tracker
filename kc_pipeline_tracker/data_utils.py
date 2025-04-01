import json
import os
from datetime import datetime

DATA_PATH = "pipeline_data.json"

def load_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

def add_project(project):
    data = load_data()
    project["last_updated"] = datetime.now().isoformat()
    data.append(project)
    save_data(data)