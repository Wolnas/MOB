from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

RAW_FOLDER = Path("raw/hospitals")