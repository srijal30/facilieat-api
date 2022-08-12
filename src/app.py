from fastapi import FastAPI

from .routers.user_router import user_router
from .database import db

app = FastAPI()
app.include_router(user_router)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def root_page():
    return {'working': True}
