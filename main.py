from config import app
from database import create_db_and_tables
from models import *
from views import *


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
