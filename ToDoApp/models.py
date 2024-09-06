from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    ward = Column(String)
    district = Column(String)
    province = Column(String)

class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    hashed_password = Column(String)
    date = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)
    fax = Column(Integer)
    address_id = Column(Integer, ForeignKey('address.id'))

class Cost(Base):
    __tablename__ = 'cost'

    id = Column(Integer, primary_key=True, index=True)
    time = Column(String)
    buy = Column(Integer)
    sell = Column(Integer)
    tax = Column(Integer)

class Flower(Base):
    __tablename__ = 'flower'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(Integer)
    cost_id = Column(Integer, ForeignKey('cost.id'))

class Rank(Base):
    __tablename__ = 'rankk'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class CustomerSpending(Base):
    __tablename__ = 'spend'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    rank_id = Column(Integer, ForeignKey('rankk.id'))
    spending = Column(Integer)

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, index=True)
    flower_id = Column(Integer, ForeignKey('flower.id'))
    quantity = Column(Integer)
    value = Column(Integer)
    status = Column(Integer)

class OrderDetail(Base):
    __tablename__ = 'order_detail'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    order_id = Column(Integer, ForeignKey('order.id'))
    date = Column(Integer)
    month = Column(Integer)
    precious = Column(Integer)
    year = Column(Integer)

class Bill(Base):
    __tablename__ = 'bill'

    id = Column(Integer, primary_key=True, index=True)
    od_id = Column(Integer, ForeignKey('order_detail.id'))
    date = Column(Integer)
    month = Column(Integer)
    precious = Column(Integer)
    year = Column(Integer)
    promotion = Column(Integer)
    total = Column(Integer)

