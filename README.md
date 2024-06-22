# Order Service

## Description

Order Service is a microservice for managing orders within the Candy-Star application, built using FastAPI, PostgreSQL,
Redis, RabbitMQ, Alembic, and Sentry.

## Requirements

- Python 3.10
- PostgreSQL
- Redis
- RabbitMQ
- Docker (for running RabbitMQ)
- Sentry

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Eastwesser/order-service.git
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv .venv
    .venv\Scripts\activate
    ```

3. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create and configure the `.env` file based on `.env.example`:

    ```sh
    cp .env.example .env
    ```

## Starting Services

### PostgreSQL

Ensure PostgreSQL is installed and running. Configure the connection in the `.env` file.

### Redis

Install and start the Redis server:

```sh
# On Ubuntu
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

Check the status of Redis:

```sh
sudo systemctl status redis-server
```

### RabbitMQ

Start RabbitMQ using Docker:

```sh
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### Running the Application

Start the application:

```sh
uvicorn app.main:app --reload
```

The application will be available at http://127.0.0.1:8003.

API documentation will be available at http://127.0.0.1:8003/docs.

### Project Structure

```markdown
order-service/
├── app/
│ ├── __init__.py
│ ├── main.py
│ ├── crud/
│ │ ├── __init__.py
│ │ ├── crud.py
│ ├── models/
│ │ ├── __init__.py
│ │ ├── models.py
│ ├── routers/
│ │ ├── __init__.py
│ │ ├── order.py
│ ├── schemas/
│ │ ├── __init__.py
│ │ ├── order.py
│ ├── db/
│ │ ├── __init__.py
│ │ ├── session.py
├── alembic/
│ ├── versions/
│ ├── env.py
│ ├── script.py.mako
├── .env
├── .env.example
├── Dockerfile
├── requirements.txt
└── README.md
```

## API Request Examples

Get All Orders

```sh
GET /orders
```

Create a New Order

```sh
POST /orders
{
  "product_id": 1,
  "user_id": 1,
  "quantity": 2,
  "total_price": 3.98
}
```

Get an Order by ID

```sh
GET /orders/{order_id}
```

Update an Order

```sh
PUT /orders/{order_id}
{
  "product_id": 1,
  "user_id": 1,
  "quantity": 3,
  "total_price": 5.97
}
```

Delete an Order

```sh
DELETE /orders/{order_id}
```

### Contact

For questions and suggestions:

Me - eastwesser@gmail.com

GitHub - https://github.com/Eastwesser

© 2024 Candy-Star. All rights reserved.
