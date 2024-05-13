from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routers import products, users, jwt_auth_users, basic_auth_users, users_db

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

