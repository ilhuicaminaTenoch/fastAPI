from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.db.models.user import User
from app.db.client import db_client
from app.schemas.user import user_schema, users_schema

router = APIRouter(prefix="/userdb", tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


# path http://localhost:8000/user/1
@router.get("/{id}")
async def get_user(id: str):
    return await search_user('_id', ObjectId(id))


# query http://host:8000/user?id=1
@router.get("/")
async def get_user(id: str):
    return await search_user('_id', ObjectId(id))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    if type(await search_user('email', user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario ya existe"
        )
    user_dic = user.dict()
    del user_dic["id"]
    id = db_client.users.insert_one(user_dic).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id": id}))
    return User(**new_user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "No se ha eliminado al usuario"}


@router.put("/", status_code=status.HTTP_200_OK, response_model=User)
async def update_user(user: User):
    user_dic = user.dict()
    del user_dic["id"]
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dic)
    except:
        return {"error": "El usuario no se ha actualizado"}
    return await search_user('_id', ObjectId(user.id))

async def search_user(field: str, key):
    try:
        user = user_schema(db_client.users.find_one({field: key}))
        return User(**user)
    except:
        return {"error": "Email no encontrado"}
