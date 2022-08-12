from pydantic import BaseModel, EmailStr
from typing import Any

from uuid import uuid4
from ..utils import hash_password


class UserBase(BaseModel):
    """Base model for users"""
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
    """User creation request model. Will be sent to prisma db."""
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
    class Config:
        orm_mode = True


class LogIn(BaseModel):
    """Request model for login request"""
    email: EmailStr
    password: str

    def hash(self):
        """Hash the password"""
        self.password = hash_password(self.password)


class GetAuth(BaseModel):
    """Request model for getting user"""
    token: str


class ChangeUser(GetAuth, UserBase):
    """Request model for changing user"""
    email: None = None  # my attempt at "deleting"
    phone: str | None
    firstName: str | None
    lastName: str | None
    sendNotifications: bool | None
