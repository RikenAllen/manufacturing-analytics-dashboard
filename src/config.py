from pathlib import Path

# Root Directory
BASE_DIRECTORY = Path(__file__).resolve().parent.parent

# Data paths

DATA_DIRECTORY = BASE_DIRECTORY / "data"
RAW_DATA_DIRECTORY = DATA_DIRECTORY / "raw"
PROCESSED_DATA_DIRECTORY = DATA_DIRECTORY / "processed"

RAW_DATA_PATH = RAW_DATA_DIRECTORY / "hot_strip_rolling_data.csv"
PROCESSED_DATA_PATH = PROCESSED_DATA_DIRECTORY / "cleaned.csv"