from pathlib import Path
import json
import re


def ensure_folder(folder):
    """
    Crea una carpeta si no existe.
    """
    Path(folder).mkdir(parents=True, exist_ok=True)


def save_json(path, data):
    """
    Guarda un diccionario como JSON.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_markdown(path, markdown):
    """
    Guarda texto Markdown.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(markdown)


def clean_filename(text):
    """
    Convierte un título en un nombre de archivo válido.
    """
    text = text.lower()
    text = text.replace(" ", "_")
    text = text.replace("/", "_")
    text = text.replace("\\", "_")
    text = text.replace("-", "_")
    text = re.sub(r"[^\w_]", "", text)
    return text