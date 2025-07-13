from fastapi import FastAPI


app = FastAPI()


@app.get('/')
async def index_page():
    return {"message": "This is home page"}

