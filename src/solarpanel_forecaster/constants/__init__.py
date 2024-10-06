from pathlib import Path
import os

CONFIG_FILE_PATH = Path("config/config.yaml")
CONFIG_SECRET_FILE_PATH = Path("config/secret_keys.yaml")
PARAMS_FILE_PATH = Path("params.yaml")
SCHEMA_FILE_PATH = Path("schema.yaml")

# Get solis private info
SOLIS_KEYID = os.environ.get('SOLIS_KEYID', '')
SOLIS_SECRET_KEY = os.environ.get('SOLIS_SECRET_KEY', '')
SOLIS_SN = os.environ.get('SOLIS_SN', '')
CELL_LATITUDE = os.environ.get('CELL_LATITUDE', '')
CELL_LONGITUDE = os.environ.get('CELL_LONGITUDE', '')
