from typing import List
from pydantic import BaseModel


class Item(BaseModel):
    itemId: str
    name: str
    description: str
    # img: <type unknown>
    price: float
    quantity: int  # we should create 2 item classes (Menu, Order)?


class Cart(BaseModel):
    items: List[Item]
    restaurantId: str
    subtotal: float  # should be called total?
