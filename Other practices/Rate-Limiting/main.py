from fastapi import FastAPI, Depends
from fastapi_limiter.depends import RateLimiter
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis_client = redis.from_url(
        "redis://127.0.0.1:6379",
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis_client)

@app.on_event("shutdown")
async def shutdown():
    await FastAPILimiter.close()

@app.get("/", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def get_main_page():
    return {"message": "this is main page"}