from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.getenv('TERRAWATCH_DATA_DIR', BASE_DIR / 'data'))
DB_PATH = Path(os.getenv('TERRAWATCH_DB_PATH', DATA_DIR / 'terrawatch.sqlite3'))
