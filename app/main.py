import models  # noqa: F401
import views  # noqa: F401
from config import app
from database import create_db_and_tables


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
