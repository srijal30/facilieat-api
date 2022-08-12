from typing import Any, Dict, Union
from fastapi import APIRouter

from ..database import db
from ..types.user import UserIn, LogIn, GetUser, UserOut
from ..utils import response, create_token, validate_token


user_router = APIRouter(prefix="/user")


@user_router.post("/create")
async def create_account(user: UserIn) -> Dict[str, Any]:
    """Creates a new user account through client request"""
    # check for user with same email
    existing_user = await db.user.find_unique(where={'email': user.email})
    if existing_user:
        return response(False, 'There is already a user with that email!')

    # make sure new uuid is generated (maybe this can go in the model too?)
    existing_user = await db.user.find_unique(where={'userId': user.userId})
    while existing_user:
        user.new_uuid()
        existing_user = await db.user.find_unique(
            where={'userId': user.userId}
        )

    # hash the password (maybe this can go in the model?)
    user.hash()

    # add user to db
    await db.user.create(data=user.dict())

    # return success
    return response(True, 'User successfully created!')


@user_router.post("/login")
async def login_user(login: LogIn) -> Dict[str, Any]:
    """Logs user in if information is correct"""
    requested_user = await db.user.find_unique(where={'email': login.email})
    # check if email exists
    if not requested_user:
        return response(False, 'No user with that email!')

    # check if wrong password
    login.hash()  #? maybe this can go in model
    if requested_user.password != login.password:
        return response(False, 'Invalid email or password!')

    # create and return token
    token = create_token(requested_user.userId)
    return response(
        success=True, 
        message='Login was successful!',
        data={
            "token": token
        }
    )


@user_router.post("/user")
async def get_user(current_user: GetUser) -> Dict[str, Any]:
    """Returns currently authenticated user."""
    # validate jwt
    userId = validate_token(current_user.token)
    if not userId:
        return response(False, 'Authentication details invalid!', {})
    
    # get the user
    user = await db.user.find_unique(where={'userId': userId})

    # return the user
    return response(
        success=True,
        message='Operation was successful',
        data=UserOut(**user.dict())
    )
