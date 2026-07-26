import json
import re
from pathlib import Path

import pandas as pd

# ==========================
# Directorios
# ==========================

RAW_FOLDER = Path("raw/hospitals")
OUTPUT_FOLDER = Path("processed")
OUTPUT_FOLDER.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_FOLDER / "hospital_capacity.csv"

# ==========================
# Funciones auxiliares
# ==========================

def find_phone(text):
    match = re.search(r"Tel[eé]fono[:\s]*([0-9\- ]+)", text, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def find_email(text):
    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )
    return match.group(0) if match else ""


def find_address(text):
    match = re.search(
        r"Direcci[oó]n[:\s]*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).split("\n")[0].strip()

    return ""


def detect_service(text, keywords):

    text = text.lower()

    for word in keywords:
        if word.lower() in text:
            return "Sí"

    return "No"


def extract_name(metadata, markdown):

    if metadata.get("title"):

        title = metadata["title"]

        title = title.replace(
            " - Gobierno Municipal Autónomo de Santa Cruz de La Sierra",
            ""
        )

        return title.strip()

    first = markdown.split("\n")[0]

    return first.replace("#", "").strip()


def hospital_type(name):

    name = name.lower()

    if "municipal" in name:
        return "Público"

    if "hospital" in name:
        return "Público"

    if "clínica" in name:
        return "Privado"

    if "clinica" in name:
        return "Privado"

    return "Desconocido"

# ==========================
# Procesamiento
# ==========================

rows = []

for file in RAW_FOLDER.glob("*.json"):

    print("Leyendo:", file.name)

    with open(file, encoding="utf-8") as f:
        data = json.load(f)

    markdown = data.get("markdown", "")

    metadata = data.get("metadata", {})

    hospital = {}

    hospital["hospital_name"] = extract_name(metadata, markdown)

    hospital["ownership"] = hospital_type(
        hospital["hospital_name"]
    )

    hospital["department"] = "Santa Cruz"

    hospital["city"] = "Santa Cruz de la Sierra"

    hospital["address"] = find_address(markdown)

    hospital["phone"] = find_phone(markdown)

    hospital["email"] = find_email(markdown)

    hospital["website"] = metadata.get("sourceURL", "")

    hospital["emergency"] = detect_service(
        markdown,
        [
            "emergencia",
            "emergencias",
            "urgencias"
        ]
    )

    hospital["icu"] = detect_service(
        markdown,
        [
            "unidad de cuidados intensivos",
            "uci",
            "terapia intensiva"
        ]
    )

    hospital["laboratory"] = detect_service(
        markdown,
        [
            "laboratorio"
        ]
    )

    hospital["imaging"] = detect_service(
        markdown,
        [
            "imagenologia",
            "imagenología"
        ]
    )

    hospital["ct_scan"] = detect_service(
        markdown,
        [
            "tomografía",
            "tomografia"
        ]
    )

    hospital["mri"] = detect_service(
        markdown,
        [
            "resonancia",
            "mri"
        ]
    )

    hospital["neurology"] = detect_service(
        markdown,
        [
            "neurología",
            "neurologia"
        ]
    )

    hospital["neurosurgery"] = detect_service(
        markdown,
        [
            "neurocirugía",
            "neurocirugia"
        ]
    )

    hospital["oncology"] = detect_service(
        markdown,
        [
            "oncología",
            "oncologia",
            "oncólogo",
            "oncologo"
        ]
    )

    hospital["hemodialysis"] = detect_service(
        markdown,
        [
            "hemodiálisis",
            "hemodialisis"
        ]
    )

    hospital["operating_rooms"] = detect_service(
        markdown,
        [
            "quirófano",
            "quirofano"
        ]
    )

    hospital["source"] = metadata.get("sourceURL", "")

    hospital["scrape_date"] = metadata.get("cachedAt", "")

    rows.append(hospital)

# ==========================
# DataFrame
# ==========================

df = pd.DataFrame(rows)

df = df.drop_duplicates(
    subset=["hospital_name"]
)

df = df.sort_values(
    "hospital_name"
)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print()
print("===================================")
print("Hospitales encontrados:", len(df))
print("Archivo generado:")
print(OUTPUT_FILE)
print("===================================") 