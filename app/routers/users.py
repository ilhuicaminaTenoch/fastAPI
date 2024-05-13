from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"])


# uvicorn users:app --reload

# Entidad Users
class User(BaseModel):
    id: int
    name: str
    first_name: str
    last_name: str
    age: int


users_list = [User(id=1, name="Tenoch", first_name="Moreno", last_name="Aguilar", age=3),
              User(id=2, name="Manuel", first_name="Moreno", last_name="Plaza", age=37),
              User(id=3, name="Acho", first_name="Moreno", last_name="Plaza", age=7)]


@router.get("/users")
async def users():
    return users_list


# path http://localhost:8000/user/1
@router.get("/user/{id}")
async def get_user(id: int):
    return search_user(id)


# query http://localhost:8000/user?id=1
@router.get("/user")
async def get_user(id: int):
    return search_user(id)


@router.post("/user", status_code=201, response_model=User)
async def create_user(user: User):
    try:
        search_user(user.id)
        raise HTTPException(status_code=409, detail="El usuario ya existe")
    except HTTPException as e:
        if e.status_code == 404:
            users_list.append(user)
            return user
        else:
            raise e


def search_user(id: int):
    user = next((user for user in users_list if user.id == id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
