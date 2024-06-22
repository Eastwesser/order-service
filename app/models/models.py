from sqlalchemy import Column, Integer, Float

from app.db.session import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    quantity = Column(Integer)
    total_price = Column(Float)

    # If you have relationships with other tables
    # product = relationship("Product")
    # user = relationship("User")
