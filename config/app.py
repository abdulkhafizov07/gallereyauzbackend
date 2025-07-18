import settings
from fastapi import FastAPI
from routers import auth_router

app = FastAPI(debug=True)

app.include_router(auth_router)
