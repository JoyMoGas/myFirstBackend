from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(
    prefix="/userdb",
    tags=["userdb"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

def search_user(field: str, key):
    user = user_schema(db_client.users.find_one({"field": key}))
    try:
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}

# Consultar usuarios en base de datos
@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

# Consultar usuarios en base de datos por id
@router.get("/{id}")
async def getUserId(id: str):
    return search_user("_id", ObjectId(id))

# Consultar usuarios en base de datos por id con JSON
@router.get("/")
async def getUserJson(id: str):
    return search_user("_id", ObjectId(id))

# Agregar un nuevo usuario a bd
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def addUser(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe"
        )
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    return User(**new_user)

# Actualizar usuario en db
@router.put("/", response_model=User)
async def putUser(user: User):
    user_dict = dict(user)
    del user_dict["_id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict
        )
    except:
        return {"Error": "No se ha actualizado el usuario"}
    return search_user("_id", ObjectId(user.id))

# Eliminar usuario en db
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"Error": "No se ha actualizaso el usuario"}
