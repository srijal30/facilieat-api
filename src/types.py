from typing import List, Dict, Any
from pydantic import BaseModel, EmailStr

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


class User(BaseModel):
    userId: str
    email: EmailStr
    phone: str  # do we need this?
    firstName: str
    lastName: str
    status: bool  # what is this for? -- Whether user is logged in
    sendNotifications: bool
    # wallet: Wallet
    # orders: List[Order]
    # transactions: List[Order]  # whats the difference between this and orders?
    carts: List[Cart] = []

