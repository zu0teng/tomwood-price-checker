import json, os, tempfile

HISTORY_FILE = "price_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(history):
    tmp_fd, tmp_path = tempfile.mkstemp(prefix="price_history_", suffix=".json", dir=".")
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, HISTORY_FILE)
    finally:
        if os.path.exists(tmp_path):
            try: os.remove(tmp_path)
            except: pass