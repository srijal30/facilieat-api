from fastapi import FastAPI

app = FastAPI()

from routers.users import user_router
app.include_router(user_router)

@app.get("/")
async def root_page():
    return {'working': True}
