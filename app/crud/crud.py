from sqlalchemy.orm import Session

from app.models import models
from app.models.models import Order
from app.schemas.orders import OrderCreate


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders_by_user_id(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()


def create_order(db: Session, order: OrderCreate):
    db_order = Order(  # Create ORM model object
        product_id=order.product_id,
        user_id=order.user_id,
        quantity=order.quantity,
        total_price=order.total_price
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
