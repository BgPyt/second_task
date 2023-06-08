import dotenv
import os

dotenv.load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PSW = os.environ.get("DB_PSW")
DB_PORT = os.environ.get("DB_PORT")
DB_HOST = os.environ.get("DB_HOST")
PG_ADMIN_EMAIL = os.environ.get("PG_ADMIN_EMAIL")
PG_ADMIN_PASSWORD = os.environ.get("PG_ADMIN_PASSWORD")
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")