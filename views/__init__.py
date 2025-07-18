import hashlib
import uuid
import os
import time
import asyncio
from fastapi.responses import ORJSONResponse, JSONResponse, UJSONResponse
from config import app


def generate_single_item(i: int) -> dict:
    hex_i = hex(i).encode()
    return {
        "id": i,
        "guid": uuid.uuid4().hex,
        "md5": hashlib.md5(hex_i).hexdigest(),
        "sha1": hashlib.sha1(hex_i).hexdigest(),
        "urandom": os.urandom(25).hex(),
        "image": f"https://example.com/uploads/some_images/im{i}.jpg"
    }


def sync_generate_response():
    start_time = time.time()
    results = [generate_single_item(i) for i in range(1000)]
    end_time = time.time()
    return {
        "start_time": start_time,
        "end_time": end_time,
        "duration": end_time - start_time,
        "results": results,
    }


async def generate_response():
    return sync_generate_response()


@app.get("/orjson", response_class=ORJSONResponse)
async def orjson_result():
    return await generate_response()


@app.get("/ujson", response_class=UJSONResponse)
async def ujson_result():
    return await generate_response()


@app.get("/json", response_class=JSONResponse)
async def json_result():
    return await generate_response()
