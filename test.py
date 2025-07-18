import asyncio
import statistics
import time
from typing import Optional

import httpx

TEST_COUNT = 1000
MAX_CONCURRENT_REQUESTS = 4  # limit to 4 at a time

ENDPOINTS = {
    "orjson": "https://api.gallereya.infinite-co.uz/orjson",
    "ujson": "https://api.gallereya.infinite-co.uz/ujson",
    "json": "https://api.gallereya.infinite-co.uz/json",
}


async def fetch(
    client: httpx.AsyncClient, name: str, url: str, semaphore: asyncio.Semaphore
) -> Optional[dict]:
    async with semaphore:
        try:
            start = time.perf_counter()
            response = await client.get(url)
            end = time.perf_counter()
            response_time = end - start

            json = response.json()
            duration = json.get("duration")

            return {
                "name": name,
                "response_time": response_time,
                "duration": duration,
            }
        except Exception as e:
            print(f"❌ Error fetching {name}: {e}")
            return None


async def benchmark(name: str, url: str) -> dict:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with httpx.AsyncClient(timeout=20.0) as client:
        tasks = [fetch(client, name, url, semaphore) for _ in range(TEST_COUNT)]
        results = await asyncio.gather(*tasks)

    results = [r for r in results if r is not None]
    durations = [r["duration"] for r in results if r["duration"] is not None]
    response_times = [r["response_time"] for r in results]

    return {
        "name": name.upper(),
        "avgfor": statistics.mean(durations),
        "avgrestime": statistics.mean(response_times),
        "min_duration": min(durations),
        "max_duration": max(durations),
        "min_response_time": min(response_times),
        "max_response_time": max(response_times),
        "count": len(results),
    }


def print_metric(metric: dict):
    print(f"{metric['name']} ({metric['count']} runs):")
    print(f"Avg execution time (duration): {metric['avgfor']:.6f}sec")
    print(f"Avg response time: {metric['avgrestime']:.6f}sec")
    print(
        f"Min/Max duration: {metric['min_duration']:.6f}/{metric['max_duration']:.6f}sec"  # noqa: E501
    )
    print(
        f"Min/Max response time: {metric['min_response_time']:.6f} / {metric['max_response_time']:.6f} sec"  # noqa: E501
    )
    print()


async def main():
    metrics = await asyncio.gather(
        *(benchmark(name, url) for name, url in ENDPOINTS.items())
    )
    for metric in metrics:
        print_metric(metric)


if __name__ == "__main__":
    asyncio.run(main())
