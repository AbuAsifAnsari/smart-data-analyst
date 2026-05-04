# utils/history_manager.py
import json
import os
from datetime import datetime

HISTORY_FILE = "memory/chat_history.json"

def _load_all():
    os.makedirs("memory", exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
        return json.loads(content) if content else {}
    except:
        return {}

def _save_all(data: dict):
    os.makedirs("memory", exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_message(dataset_name: str, role: str, content: str, query: str = ""):
    """Ek message save karo — dataset ke naam se grouped."""
    data = _load_all()
    if dataset_name not in data:
        data[dataset_name] = []
    data[dataset_name].append({
        "role":      role,
        "content":   content,
        "query":     query,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    _save_all(data)

def load_history(dataset_name: str) -> list:
    """Kisi dataset ki poori chat history load karo."""
    data = _load_all()
    return data.get(dataset_name, [])

def clear_history(dataset_name: str):
    """Kisi dataset ki history clear karo."""
    data = _load_all()
    if dataset_name in data:
        del data[dataset_name]
    _save_all(data)

def get_all_sessions() -> dict:
    """Sidebar mein past sessions dikhane ke liye."""
    data = _load_all()
    sessions = {}
    for dataset, messages in data.items():
        q_count = sum(1 for m in messages if m["role"] == "user")
        last_ts = messages[-1]["timestamp"] if messages else ""
        sessions[dataset] = {
            "questions": q_count,
            "last_seen": last_ts,
            "preview":   messages[-2]["content"][:60] + "..." 
                         if len(messages) >= 2 else ""
        }
    return sessions