import asyncio
import os

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.crud import crud
from app.main import app
from app.models import models

# Override database URL for testing
os.environ["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL")

# Create async engine
async_engine = create_async_engine(os.getenv("TEST_DATABASE_URL"), echo=True, future=True)


@pytest.fixture(scope="module")
def event_loop():
    """
    Override the default pytest-asyncio event loop fixture to use the default asyncio loop.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="session")
async def async_session():
    db_engine = create_async_engine(async_engine)
    async_session = sessionmaker(bind=db_engine, expire_on_commit=False, class_=AsyncSession)

    yield async_session

    await async_session.close()
    await db_engine.dispose()


@pytest.fixture(scope="module", autouse=True)
async def setup_and_teardown_db():
    """
    Fixture to set up and tear down the test database.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


# Example test (removed pytest.anyio for simplicity)
async def test_create_order(async_client, async_session):
    # Define test data
    order_data = {
        "product_id": 1,
        "user_id": 1,
        "quantity": 3,
        "total_price": 50.0
    }

    # Make POST request to create order
    response = await async_client.post("/orders/", json=order_data)

    # Assert response status code is 201
    assert response.status_code == 201

    # Assert response JSON contains expected keys and values
    assert "id" in response.json()
    assert response.json()["product_id"] == order_data["product_id"]
    assert response.json()["user_id"] == order_data["user_id"]
    assert response.json()["quantity"] == order_data["quantity"]
    assert response.json()["total_price"] == order_data["total_price"]

    # Verify order creation in database
    created_order = await crud.get_order(async_session, order_id=response.json()["id"])
    assert created_order is not None
    assert created_order.product_id == order_data["product_id"]
    assert created_order.user_id == order_data["user_id"]
    assert created_order.quantity == order_data["quantity"]
    assert created_order.total_price == order_data["total_price"]
