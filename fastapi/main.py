from gc import get_debug
from typing import List
from fastapi import FastAPI, Depends,HTTPException
import pydantic
from pydantic import BaseModel
from uuid import uuid4

from requests import Session

from auth import AuthHandler
from schemas import AuthDetails, CreateUserRequest
from sqlalchemy.orm import Session
from database import get_db
from models import User


app = FastAPI()

class Npc(BaseModel):
    id: str
    nombre: str 
    nivel: int
    skills: List[str] = []

""" @app.get("/")
async def root():
    return {"message": "Hello World"} """

@app.get("/npc/{npc_id}")
async def login(npc_id: int):
    return f"NPC {npc_id}"

npcs = []

@app.get("/npcs")
async def listado_npc():
    return npcs

#  
@app.post("/npc/crear")
async def crear_npc(npc:Npc):
    npc.id = str(uuid4())
    npcs.append(npc.dict())
    return " Creado!"

@app.put("/npc/modificar/{id}")
def modificar_npc(updated_npc: Npc,id:str):
    for npc in npcs:
        if npc["id"] == id:
            npc["nombre"] = updated_npc.nombre
            npc["nivel"] = updated_npc.nivel
            npc["skills"] = updated_npc.skills
            return f"npc: {updated_npc.id} modificado con éxito!"
    return f"npc: No existe!"


@app.delete("/npc/eliminar/{id}")
async def eliminar_npc(id:str):
    for npc in npcs:
        if npc["id"] == id:
            npcs.remove(npc)
            return "Npc eliminado"
    return f"npc: No existe!"



auth_handler = AuthHandler()
users = []
@app.get("/users")
async def listado_users():
    return users

@app.post("/register", status_code=201)
def register(auth_details: AuthDetails):
    if any (x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail="Username is taken")
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        "username": auth_details.username,
        "password": hashed_password
    })
    return 

@app.post("/login")
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x["username"] == auth_details.username:
            user = x
            print("usuario ya logeado")
            break
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail="Invalid Username and/or password")
    token = auth_handler.encode_token(user['username'])
    return {"token":token}




@app.get("/desprotejido")
def desprotejido():
    return "Acceso permitido"

@app.get("/protejido")
def protejido(username=Depends(auth_handler.auth_wrapper)):
    return {'name': username}

@app.post("/dbtest")
def dbtest(details: CreateUserRequest, db: Session = Depends(get_db)):
    to_create = User(
        username=details.username,
        password=details.password
    )
    db.add(to_create)
    db.commit()
    return {
        "success": True,
        "created_id": to_create.id
    }

@app.get("/get")
def get_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == id).first()

@app.delete("/delete")
def delete(id: int, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == id).delete()
    db.commit()
    return {"success": True}
    #