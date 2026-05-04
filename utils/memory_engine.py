import json
import os

MEMORY_FILE = "memory/qa_log.json"

def _load_memory():
    """Safe memory loader — kabhi crash nahi karega"""
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return []
        return json.loads(content)
    except (json.JSONDecodeError, Exception):
        # File corrupt hai — reset kar do
        _reset_memory()
        return []

def _reset_memory():
    """Memory file reset karo"""
    os.makedirs("memory", exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def save_qa(question, answer, dataset_name):
    data = _load_memory()
    data.append({
        "dataset": dataset_name,
        "question": question,
        "answer": answer
    })
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_relevant_memory(question, dataset_name, top_k=3):
    data = _load_memory()
    if not data:
        return ""
    relevant = [
        qa for qa in data
        if qa["dataset"] == dataset_name or
        any(word in qa["question"].lower()
            for word in question.lower().split())
    ]
    if not relevant:
        return ""
    recent = relevant[-top_k:]
    context = "Previous relevant Q&As from memory:\n"
    for qa in recent:
        context += f"Q: {qa['question']}\nA: {qa['answer']}\n\n"
    return context