import asyncio
import os

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

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


@pytest.fixture(scope="module")
async def async_client():
    """
    Create a FastAPI AsyncClient fixture to use in async tests.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="module")
async def async_session(event_loop):
    """
    Create an async session fixture for database operations.
    """
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest.fixture(scope="module", autouse=True)
async def setup_and_teardown_db():
    """
    Fixture to set up and tear down the test database.
    """
    # Setup
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    yield

    # Teardown
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


# Example test
@pytest.mark.asyncio
async def test_create_order(async_client: AsyncClient, async_session: AsyncSession):
    # Define test data
    order_data = {
        "product_id": 1,
        "user_id": 1,
        "quantity": 3,
        "total_price": 50.0
    }

    # Make POST request to create order
    response = await async_client.post("/orders/", json=order_data)

    # Assert response status code is 200
    assert response.status_code == 200

    # Assert response JSON contains expected keys
    assert "id" in response.json()
    assert response.json()["product_id"] == order_data["product_id"]
    assert response.json()["user_id"] == order_data["user_id"]
    assert response.json()["quantity"] == order_data["quantity"]
    assert response.json()["total_price"] == order_data["total_price"]

    # Optional: Verify order creation in database
    from app.crud import crud
    created_order = await crud.get_order(async_session, order_id=response.json()["id"])
    assert created_order is not None
    assert created_order.product_id == order_data["product_id"]
    assert created_order.user_id == order_data["user_id"]
    assert created_order.quantity == order_data["quantity"]
    assert created_order.total_price == order_data["total_price"]
