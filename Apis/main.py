from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

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


#USUARIOS
class Usuario(BaseModel):
    cedula: int = Field(..., example=1)
    nombre: str = Field(..., example="Juan Pablo")
    telefono: str = Field(None, example="4141234567")
    correo: str = Field(None, example="Juan.Pablo1234@gmail.com")

user_db: List[Usuario] = [
    Usuario(cedula=1, nombre="Juan Pablo", telefono="4141234567", correo="Juan.Pablo1234@gmail.com"),
    Usuario(cedula=2, nombre="Ana Torres", telefono="4147654321", correo="ana.torres@gmail.com")
]

@app.get("/usuarios",
         response_model=list[Usuario],
         summary="Obtener lista de usuarios",
         description="Obtiene la lista de todos los usuarios registrados en la biblioteca.",
         tags=["Usuarios"],
            responses={
                200: {"descripción": "Lista de usuarios obtenida exitosamente."},
                404: {"descriptión": "No se encontraron usuarios."}
            } 
        )


def get_usuarios() -> List[Usuario]:
    if not user_db:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios.")
    return user_db

@app.get("/usuarios/{cedula}",
         response_model=Usuario,
         summary="Obtener el usuario mediante su cédula",
         description="Obtiene la información de un usuario específico usando su cédula.",
         tags=["Usuarios"],
         responses={
             200: {"description": "Usuario encontrado exitosamente."},
             404: {"description": "Usuario no encontrado."}
         }
)
def get_usuario_por_cedula(cedula: int) -> Usuario:
    for usuario in user_db:
        if usuario.cedula == cedula:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")

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









#LIBROS
class libro:
    codigo: float = Field(..., example=1)
    titulo: str = Field(..., example="Cien años de soledad")
    categoria: str = Field(..., example="Periodica")
    sinopsis: str = Field(..., example="Novela de Gabriel García Márquez")
    precio: float = Field(..., example = 50000)

libro_db: List[libro] = []




#PRESTAMOS

class Prestamo(BaseModel):
    idPrestamo: int = Field(..., examples = [1])
    cedulaUsuario: int = Field(..., examples = [101])
    idLibro: int = Field(..., examples = [1001])
    fechaPrestamo: date = Field(..., examples = ["2024-09-05"])
    fechaDevolucion: Optional[date] = Field(None, examples = ["2025-09-05"])
    estadoPrestamo: str = Field(..., examples=["Activo", "Devuelto", "Atrasado"])

prestamos_db: List[Prestamo] = [
    Prestamo(idPrestamo=1, cedulaUsuario=1, idLibro=1001, fechaPrestamo=date(2025, 9, 5), fechaDevolucion= None, estadoPrestamo="Activo"),
    Prestamo(idPrestamo=2, cedulaUsuario=2, idLibro=1001, fechaPrestamo=date(2025, 8, 5), fechaDevolucion= date(2025, 9, 5), estadoPrestamo="Devuelto")
]

#ENDPOINTS PRESTAMOS

@app.get("/prestamos",
         response_model=list[Prestamo],
         summary="Obtener lista de todos los prestamos",
         description="Retorna todos los prestamos realizados en la biblioteca. Permite filtrar por estado del prestamos (Activo, Devuelto, Atrasado).",
         tags=["Prestamos"],
            responses={
                200: {"descripción": "Lista de prestamos obtenida exitosamente."},
                404: {"descriptión": "No se encontraron prestamos."}
            } 
        )

def obtener_trasacciones (estado_prestamo: Optional[str] =
                          Query(None, description="Filtrar por tipo de prestamo (Activo, Devuelto, Atrasado)")):
    if estado_prestamo:
        prestamos_filtrados = [p for p in prestamos_db if p.estadoPrestamo.lower() == estado_prestamo.lower()]
        if not prestamos_filtrados:
            raise HTTPException(status_code=404, detail=f"No se encontraron transacciones con tipo: {estado_prestamo}")
        return prestamos_filtrados
    return prestamos_db
#Para obtener todas las trasacciones /prestamos
#Para obtener todas las trasacciones con un estado especifico /prestamos?estado_prestamo=Activo

@app.get("/prestamos/{id_prestamo}",
         response_model=Prestamo,
         summary="Obtener los datos de un prestamo especifico",
         description="Retorna la información de un prestamo. Permite filtrar por el ID del prestamo.",
         tags=["Prestamos"],
            responses={
                200: {"descripción": "Datos de prestamo obtenido exitosamente."},
                404: {"descriptión": "No se encontraron prestamo especifico."}
            }
         )


def obtener_prestamo(id_prestamo: int):
    for prestamo in prestamos_db:
        if prestamo.idPrestamo == id_prestamo:
            print("DEBUG →", prestamo)
            return prestamo
    raise HTTPException(status_code=404, detail="Prestamo no encontrado")
#Para obtener el registro de un prestamos con un id especifico /prestamos/1






    
#Ruta raiz
@app.get("/")
def read_root():
    return {"Bienvenido": " API de Biblioteca",
            "version" : "1.0.0",
            "endpoints" : {
                "usuarios":"/usuarios",
                "libros":"/libros",
                "prestamos":"/prestamos",
                "documentacion swagger":"/docs"
            }}


#Ruta con parametro
#@app.get("/items/{item_id}")
#def read_item(libro_cod: int, q: str = None):
   # return {"item_id": libro_cod, "Titulo": q}

