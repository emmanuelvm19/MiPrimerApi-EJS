from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="API Biblioteca",
    version="1.0.0",
    description="API REST básica para gestión de una biblioteca académica.",
    openapi_tags=[
        {"name": "Usuarios",
            "description": "CRUD para gestionar los usuarios registrados en la biblioteca. Permite crear, consultar, actualizar y eliminar usuarios."},
        {"name": "Libros",
            "description": "CRUD para administrar los libros disponibles en la biblioteca. Permite agregar, consultar, modificar y eliminar información de libros."},
        {"name": "Prestamos",
            "description": "CRUD para gestionar los préstamos de libros. Permite registrar, consultar, actualizar y finalizar préstamos realizados por los usuarios."}
    ]
)

class Usuario(BaseModel):
    cedula: int = Field(..., example=1)
    nombre: str = Field(..., example="Juan Pablo")
    telefono: str = Field(None, example="4141234567")
    correo: str = Field(None, example="Juan.Pablo1234@gmail.com")

user_db: List[Usuario] = []

@app.get("/usuarios",
         response_model=list[Usuario],
         summary="Obtener lista de usuarios",
         description="Obtiene la lista de todos los usuarios registrados en la biblioteca.",
         tags=["Usuarios"],
            responses={
                200: {"descripción": "Lista de usuarios obtenida exitosamente."},
                404: {"description": "No se encontraron usuarios."}
            } 
        )
def get_usuarios() -> List[Usuario]:
    if not user_db:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios.")
    return user_db
    
@app.post("/usuarios", 
          status_code=201,
          summary="Crear un nuevo usuario", 
          description="Crea un nuevo usuario en la biblioteca.", 
          tags=["Usuarios"],
          responses={
              201: {"description": "Usuario creado exitosamente."},
              400: {"description": "Error en la creación del usuario, cédula ya existe en el registro."}
            }
)
def crear_usuario(usuario: Usuario) -> Usuario:
    for cada_user in user_db:
        if cada_user.cedula == usuario.cedula:
            raise HTTPException(status_code=400, detail="Cédula ya existe en el registro.")
    user_db.append(usuario)
    return usuario

@app.put("/usuarios/{cedula}", 
         response_model=Usuario,
         summary="Actualizar un usuario existente", 
         description="Actualiza la información de un usuario existente en la biblioteca.", 
         tags=["Usuarios"],
         responses={
             200: {"description": "Usuario actualizado exitosamente."},
             404: {"description": "Usuario no encontrado."}
            }
)

def actualizar_usuario(cedula: int, usuario_actualizado: Usuario) -> Usuario:
    for index, cada_user in enumerate(user_db):
        if cada_user.cedula == cedula:
            user_db[index] = usuario_actualizado
            return usuario_actualizado
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")


@app.delete("/usuarios/{cedula}", 
            summary="Eliminar un usuario",
            description="Elimina un usuario de la biblioteca.",
            tags=["Usuarios"],
            responses={
                200: {"description": "Usuario eliminado exitosamente."},
                404: {"description": "Usuario no encontrado."}
            }
)
def eliminar_usuario(cedula: int) -> dict:
    for index, cada_user in enumerate(user_db):
        if cada_user.cedula == cedula:
            del user_db[index]
            return {"detail": "Usuario eliminado exitosamente."}
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")
            

class libro:
    codigo: float = Field(..., example=1)
    titulo: str = Field(..., example="Cien años de soledad")
    categoria: str = Field(..., example="Periodica")
    sinopsis: str = Field(..., example="Novela de Gabriel García Márquez")
    precio: float = Field(..., example = 50000)

user_db: List[libro] = []
    
#Ruta raiz
@app.get("/")
def read_root():
    return {"Bienvenida": "Hola, bienvenido a la biblioteca (realizada con API rest)"}

#Ruta con parametro
@app.get("/items/{item_id}")
def read_item(libro_cod: int, q: str = None):
    return {"item_id": libro_cod, "Titulo": q}

