import os, sys
from src.logger import Logger
import dotenv
dotenv.load_dotenv()

log = Logger.get_logger()
current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)
root_directory = os.path.abspath(os.path.join(parent_directory, ".."))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
DATABASE_PATH = os.getenv('DATABASE_PATH', root_directory + "/data/app.db")

missing_vars = []
if OPENAI_API_KEY is None:
    missing_vars.append("OPENAI_API_KEY")
if SECRET_KEY is None:
    missing_vars.append("SECRET_KEY")
if AZURE_ENDPOINT is None:
    missing_vars.append("AZURE_ENDPOINT")
if AZURE_API_KEY is None:
    missing_vars.append("AZURE_API_KEY")
if AZURE_API_VERSION is None:
    missing_vars.append("AZURE_API_VERSION")

if missing_vars:
    log.debug(f"Error: Missing environment variables - {', '.join(missing_vars)}")
    sys.exit(1)

log.info("All required environment variables are set.")