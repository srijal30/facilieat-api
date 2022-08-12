from pydantic import BaseModel, EmailStr
from typing import Any

from uuid import uuid4
from ..utils import hash_password


class UserBase(BaseModel):
    """Base model for users"""
    userId: str
    email: EmailStr
    phone: str  # do we need this?
    firstName: str
    lastName: str
    sendNotifications: bool = True

    # status: bool = False # what is this for? -- Whether user is logged in
    # wallet: Wallet
    # orders: List[Order]  # should be named ongoing_order
    # transactions: List[Order]  # should be named past_orders
    # carts: List[Cart] = []


class UserIn(UserBase):
    """User creation request model"""
    userId: str = uuid4().hex
    password: str

    def hash(self):
        """Hash the password"""
        self.password = hash_password(self.password)

    def new_uuid(self):
        """Creates a new uuid if current one already exists in db."""
        self.userId = uuid4().hex

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)


class UserOut(UserBase):
    """User model that gets sent to the client"""
    email: str
    phone: str
    firstName: str
    lastName: str
    sendNotifications: bool

    class Config:
        orm_mode = True


class LogIn(BaseModel):
    email: EmailStr
    password: str

    def hash(self):
        """Hash the password"""
        self.password = hash_password(self.password)


class GetUser(BaseModel):
    token: str
