from fastapi import FastAPI

import settings  # noqa
from routers import auth_router

app = FastAPI(debug=True)

app.include_router(auth_router)
