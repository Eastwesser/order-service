import os

import aio_pika
import aioredis
import sentry_sdk
import uvicorn
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.db.session import engine, Base
from app.routers import order

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")
if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable is not set")
if not RABBITMQ_URL:
    raise ValueError("RABBITMQ_URL environment variable is not set")

app = FastAPI()

sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"))


@app.on_event("startup")
async def startup():
    app.state.redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    app.state.rabbitmq_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()
    await app.state.rabbitmq_connection.close()
    await engine.dispose()


app.include_router(order.router)
app.add_middleware(SentryAsgiMiddleware)


@app.get("/")
async def read_root():
    return {"Hello": "Order Service"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
