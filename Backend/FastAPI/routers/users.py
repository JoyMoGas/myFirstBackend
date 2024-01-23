from fastapi import FastAPI, APIRouter, status, HTTPException
from pydantic import BaseModel

router = APIRouter()
# Entidad User

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

users_list = [
            User(id=1, name="Jose", surname="Montaño", age=19),
            User(id=2, name="María", surname="Rodriguez", age=17),
            User(id=3, name="Roberto", surname="Gonzalez", age=15)
              ]
users_json = [
    {"Name": "Jose", "surname": "Montaño", "age" : 19},
    {"Name": "María", "surname": "Rodriguez", "age" : 17},
    {"Name": "Roberto", "surname": "Gonzalez", "age" : 15}
]
Founderror = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usario no encontrado"
        )
def search_user(id: int):
   
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error": "No se ha encontrado el usuario"}

@router.get("/usersjson")
async def usersjson():
    return users_json

# Buscar todos los usuarios
@router.get("/users")
async def userslist():
    return users_list

# Buscar usuario por id
@router.get("/user/{id}")
async def getUsersId(id: int):
    return search_user(id)

# Buscar usuario por ID pero /?id=1
@router.get("/users/")
async def user(id: int):
    return search_user(id)

# Agregar usuario a la lista de usuarios (Petición es con un json)
@router.post("/user/", response_model=User, status_code=201)
async def addUser(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    users_list.append(user)
    return user

# Actualizar un usuario (Recibe un json)
@router.put("/user/")
async def putUser(user: User):
    found = False
    
    for i, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[i] = user
            found = True
    if not found:
            return{"Error": "No se ha actualizado el usuario"}
    return user

@router.delete("/user/{id}")
async def deleteUser(id: int):
    found = False
    
    for i, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[i]
            found = True
            return {"Aviso": "El usuario se eliminó correctamente"}
    if not found:
        return {"Error": "No se ha eliminado al usuario"} 
    return user
