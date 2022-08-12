from typing import Any, Dict
from fastapi import APIRouter

from ..database import db
from ..types.user import ChangeUser, UserIn, LogIn, GetAuth, UserOut
from ..utils import response, create_token, validate_token


user_router = APIRouter(prefix="/user")


@user_router.post("/create")
async def create_account(user: UserIn) -> Dict[str, Any]:
    """Creates a new user account through client request"""
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
    await db.user.create(data=user.dict())
    return response(True, 'User successfully created!')


@user_router.post("/login")
async def login_user(login: LogIn) -> Dict[str, Any]:
    """Logs user in if information is correct"""
    # check if email exists
    requested_user = await db.user.find_unique(where={'email': login.email})
    if not requested_user:
        return response(False, 'No user with that email!')
    login.hash()  # ? maybe this can go in model
    # check for wrong password
    if requested_user.password != login.password:
        return response(False, 'Invalid email or password!')
    token = create_token(requested_user.userId)
    return response(
        success=True,
        message='Login was successful!',
        data={
            "token": token
        }
    )


# DRY this
@user_router.post("/user")
async def get_user(current_user: GetAuth) -> Dict[str, Any]:
    """Returns currently authenticated user."""
    # validate jwt
    userId = validate_token(current_user.token)
    if not userId:
        return response(False, 'Authentication details invalid!')
    # query and return
    user = await db.user.find_unique(where={'userId': userId})
    if not user:
        return response(False, 'Authentication failed!')
    return response(
        success=True,
        message='Operation was successful',
        data=UserOut(**user.dict())
    )


# DRY this
@user_router.post("/change")
async def change_info(req: ChangeUser) -> Dict[str, Any]:
    """Changes the request params"""
    # validate jwt
    userId = validate_token(req.token)
    if not userId:
        return response(False, 'Authentication details invalid!')
    # update
    keys = req.dict().items()
    await db.user.update(
        where={'userId': userId},
        data={
            key: value for key, value in keys
            if key != "token" and value is not None
        }
    )
    # return
    return response(True, 'Successfully changed user information!')
