
import os

def list_entries():
    files = os.listdir("entries")
    return sorted([file.replace(".md", "") for file in files if file.endswith(".md")])

def save_entry(title, content):
    with open(f"entries/{title}.md", "w", encoding="utf-8") as f:
        f.write(content)

def get_entry(title):
    try:
        with open(f"entries/{title}.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
