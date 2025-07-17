from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def index_api():
    return {"detials": "This is index page of gallereya.uz API"}

@app.get('/image')
async def image_api():
    return {"details": "This API will return some image"}

