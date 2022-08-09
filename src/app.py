from fastapi import FastAPI

from .routers.user import user_router

app = FastAPI()
app.include_router(user_router)

@app.get("/")
async def root_page():
    return {'working':True}