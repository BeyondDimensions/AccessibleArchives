import os
from utils import logger
from dotenv import load_dotenv

# Construct the path to the .env file (in the current folder)

priority_path = '/opt/AccessibleArchives/Config/credentials.env'
load_dotenv(priority_path)

# Load environment variables from src/config/credentials.env (only if not already set)
project_path = os.path.join(os.path.dirname(__file__), 'credentials.env')

load_dotenv(project_path, override=False)

# Load API keys from environment variables
HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

logger.info(
    f"Loaded HUGGINGFACEHUB_API_TOKEN: {HUGGINGFACEHUB_API_TOKEN}")
logger.info(f"Loaded OPENAI_API_KEY: {OPENAI_API_KEY}")

# Handle missing API keys with a warning
if not HUGGINGFACEHUB_API_TOKEN:
    logger.warning(
        "HUGGINGFACEHUB_API_TOKEN is not set. Some features may not work.")
if not OPENAI_API_KEY:
    logger.warning(
        "OPENAI_API_KEY is not set. Some features may not work.")

SRC_PATH = os.path.abspath(os.path.join(__file__, "..", ".."))
# Path where document collections are stored
DOC_COLLECTIONS_PATH = os.path.abspath(os.path.join(
    SRC_PATH, "..", ".data"
))
