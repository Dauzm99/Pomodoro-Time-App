# data/persistence.py
import json
from config import settings

def save_data(data):
    """Saves the application data (tasks, logs) to a JSON file."""
    try:
        with open(settings.DATA_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data: {e}")

def load_data():
    """Loads the application data from a JSON file."""
    try:
        with open(settings.DATA_FILE_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return a default structure if the file doesn't exist or is empty
        return {"tasks": {"Work": [], "Study": []}, "logs": {}}