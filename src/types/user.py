from typing import List
from pydantic import BaseModel, EmailStr

from .utils import Cart


class User(BaseModel):
    # userId: str
    email: EmailStr
    phone: str  # do we need this?
    firstName: str
    lastName: str
    status: bool  # what is this for? -- Whether user is logged in
    sendNotifications: bool = True
    # wallet: Wallet
    # orders: List[Order]
    # transactions: List[Order]
    carts: List[Cart] = []
