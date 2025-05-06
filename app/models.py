# Define your SQLAlchemy models here
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app import db

# Enum for Checkout status
class CheckoutStatusEnum(PyEnum):
    pending = "Pending"
    processing = "Processing"
    completed = "Completed"

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    checkouts = relationship("Checkout", back_populates="user", cascade="all, delete-orphan")


class Item(db.Model):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    cart_items = relationship("CartItem", back_populates="item", cascade="all, delete-orphan")


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    user = relationship("User", back_populates="cart_items")
    item = relationship("Item", back_populates="cart_items")


class Checkout(db.Model):
    __tablename__ = 'checkouts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(CheckoutStatusEnum), default=CheckoutStatusEnum.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="checkouts")
