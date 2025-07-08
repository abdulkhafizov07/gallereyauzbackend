from config import app


@app.get("/")
def index_page():
    return {"message": "Welcome to the Index Page!"}
