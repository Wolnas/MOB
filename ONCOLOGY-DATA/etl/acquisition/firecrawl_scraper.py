import json
from pathlib import Path

from firecrawl import FirecrawlApp
from utils import clean_filename

from config import FIRECRAWL_API_KEY
from config import RAW_FOLDER

from logger import get_logger
from utils import ensure_folder
from utils import save_json
from utils import save_markdown


logger = get_logger()

ensure_folder(RAW_FOLDER)

app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)


with open("etl/acquisition/hospital_urls.txt", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]


logger.info(f"Se encontraron {len(urls)} hospitales")

folder = Path(RAW_FOLDER)

for url in urls:

    try:

        logger.info(f"Scrapeando {url}")

        result = app.scrape_url(url)

        # Convertir Document -> dict
        if hasattr(result, "model_dump"):
            result = result.model_dump()
        elif hasattr(result, "dict"):
            result = result.dict()

        metadata = result.get("metadata", {})
        markdown = result.get("markdown", "")

        title = metadata.get("title", "hospital")

        filename = clean_filename(title)

        save_json(folder / f"{filename}.json", result)
        

        if markdown:
            save_markdown(folder / f"{filename}.md", markdown)

        save_json(
            folder / f"{filename}_metadata.json",
            metadata,
        )

        logger.info(f"Guardado: {filename}")

    except Exception as e:

        logger.error(e)

print("✅ Scraping completado.")
print(f"Archivos guardados en: {folder}") 