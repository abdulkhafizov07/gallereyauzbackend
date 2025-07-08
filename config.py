from fastapi import FastAPI
from sqlmodel import create_engine
from settings import *
from pytz import timezone

app = FastAPI()
engine = create_engine(DATABASE_URL, connect_args=DATABASE_CONNECT_ARGS)
tzinfo = timezone(TZ_NAME)
