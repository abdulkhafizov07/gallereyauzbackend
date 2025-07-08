from fastapi import FastAPI
from pytz import timezone
from settings import DATABASE_CONNECT_ARGS, DATABASE_URL, TZ_NAME
from sqlmodel import create_engine

app = FastAPI()
engine = create_engine(DATABASE_URL, connect_args=DATABASE_CONNECT_ARGS)
tzinfo = timezone(TZ_NAME)
