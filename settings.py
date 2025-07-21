import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=False)
load_dotenv(dotenv_path=".env.local", override=True)


DEBUG = os.getenv("FASTAPI_DEBUG", "false").lower() in ("1", "true", "yes")

SECRET_TOKEN = os.getenv("FASTAPI_SECRET", "open")
USERS_SECRET_TOKEN = os.getenv("FASTAPI_USERS_SECRET", "open")


DATABASE_URL = os.getenv("FASTAPI_DATABASE_URL", "sqlite+aiosqlite:///database.db")
