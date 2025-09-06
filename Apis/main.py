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

def obtener_prestamos (estado_prestamo: Optional[str] =
                          Query(None, description="Filtrar por tipo de prestamo (Activo, Devuelto, Atrasado)")):
    if estado_prestamo:
        prestamos_filtrados = [p for p in prestamos_db if p.estadoPrestamo.lower() == estado_prestamo.lower()]
        if not prestamos_filtrados:
            raise HTTPException(status_code=404, detail=f"No se encontraron transacciones con tipo: {estado_prestamo}")
        return prestamos_filtrados
    return prestamos_db
#Para obtener todas los prestamos /prestamos
#Para obtener todas los prestamos con un estado especifico /prestamos?estado_prestamo=Activo

@app.get("/prestamos/{id_Prestamo}",
         response_model=Prestamo,
         summary="Obtener los datos de un prestamo especifico",
         description="Retorna la información de un prestamo. Permite filtrar por el ID del prestamo.",
         tags=["Prestamos"],
            responses={
                200: {"descripción": "Datos de prestamo obtenido exitosamente."},
                404: {"descriptión": "No se encontraron prestamo especifico."}
            }
         )


def obtener_prestamo(idPrestamo: int):
    for prestamo in prestamos_db:
        if prestamo.idPrestamo == idPrestamo:
            print("DEBUG →", prestamo)
            return prestamo
    raise HTTPException(status_code=404, detail="Prestamo no encontrado")
#Para obtener el registro de un prestamos con un id especifico /prestamos/1


@app.post("/prestamos", 
          status_code=201,
          summary="Crear un prestamo", 
          description="Crea un nuevo prestamo de algún libro.", 
          tags=["Prestamos"],
          responses={
              201: {"description": "Prestamo creado exitosamente."},
              400: {"description": "Error en la creación del prestamo, prestamo ya existe en los registros."}
            })


def crear_prestamo(prestamo: Prestamo):
    # Verificar que no exista ya
    for p in prestamos_db:
        if p.idPrestamo == prestamo.idPrestamo:
            raise HTTPException(status_code=400, detail=f"Ya existe un prestamo con ID {prestamo.idPrestamo}")
    prestamos_db.append(prestamo)
    return prestamo


@app.put("/prestamos/{id_Prestamo}", 
         response_model=Prestamo,
         summary="Actualizar un prestamo existente", 
         description="Actualiza la información de un prestamo existente en la biblioteca. Por medio del ID", 
         tags=["Prestamos"],
         responses={
             200: {"description": "Usuario actualizado exitosamente."},
             404: {"description": "Usuario no encontrado."}
            }
)

def actualizar_prestamo(idPrestamo: int, prestamo_actualizado: Prestamo) -> Prestamo:
    for index, cada_prestamo in enumerate(prestamos_db):
        if cada_prestamo.idPrestamo == idPrestamo:
            prestamos_db[index] = prestamo_actualizado
            return prestamo_actualizado
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")

@app.delete("/prestamos/{id_Prestamo}", 
            response_model=Prestamo,
            summary="Eliminar un prestamo",
            description="Elimina un prestamo del sistema.",
            tags=["Prestamos"],
            responses={
                200: {"description": "Usuario eliminado exitosamente."},
                404: {"description": "Usuario no encontrado."}
            }
)
def eliminar_prestamo(idPrestamo: int) -> dict:
    for index, cada_prestamo in enumerate(prestamos_db):
        if cada_prestamo.idPrestamo == idPrestamo:
            del prestamos_db[index]
            return {"detail": "Usuario eliminado exitosamente."}
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")



class Libros(BaseModel):
    Titulo: str = Field(..., example="Cien años de Soledad")
    Autor: str = Field(..., example="Juan Pablo")
    Año: int = Field(None, example="2020")
    Precio: float = Field(None, example=200000)

Libros_db = [
    Libros(Titulo="Las cronicas de Dayron Moreno", Autor="Santiago Hernandez",  Año=2000,Precio=5000),
    Libros(Titulo="1984", Autor="George Orwell", Año=1949, Precio=25000),
    Libros(Titulo="Don Quijote de la Mancha", Autor="Miguel de Cervantes", Año=1605, Precio=40000),
    Libros(Titulo="La Odisea", Autor="Homero", Año=-800, Precio=45000)
]

#Obtener libro
@app.get("/Libros", tags=["Libros"], 
         summary="Obtener lista de Libros",
         response_description="Lista de Libros",
         response_model=List[Libros],
         responses={
             
                200: {"description": "Libro encontrado exitosamente."},
                404: {"description": "Libro no encontrado."}
             
})
#Imprime la lista de libros
def get_LibrosTitulo():
    return Libros_db

@app.get("/Libros/{Titulo}", tags=["Libros"], 
         response_model=Libros)

#Imprime un libro filtrado por titulo
def get_Libros(Titulo:str):
    for Libro in Libros_db:
        if Libro.Titulo == Titulo: #Esto es para que no ponga error por mayusculas
            return Libro
    raise HTTPException(status_code=404, detail="No existe el libro")

#Crea nuevo libro
@app.post("/Libros", tags=["Libros"], 
          status_code=201,
          summary="Crear un nuevo Libro", 
          description="Crea un nuevo Libro en la biblioteca.", 
          
          responses={
              201: {"description": "Libro creado exitosamente."},
              400: {"description": "Error en la creación del Libro, ya existe en el registro."}
            }
)
def crear_Libro(Libro:Libros):
    for cada_Libro in Libros_db:
        if cada_Libro.Titulo == Libro.Titulo:
            raise HTTPException(status_code=400, detail="Libro ya existe en el registro.")
    Libros_db.append(Libro)
    return Libro

#Actualizar libro
@app.put("/Libros/{Titulo}", tags=["Libros"],
         response_model=Libros,
         summary="Actualizar un Libro existente", 
         description="Actualiza la información de un Libro existente en la biblioteca.", 
         responses={
             200: {"description": "Libro actualizado exitosamente."},
             404: {"description": "Libro no encontrado."}
            }
)

def actualizar_Libro(Titulo:str, Libro_Actualizado: Libros):
    for index, Libro in enumerate(Libros_db):
        if Libro.Titulo == Titulo:
            Libros_db[index] = Libro_Actualizado.dict()
            return Libro_Actualizado
    raise HTTPException(status_code=404, detail="Libro no encontrado.")

#Eliminar libro
@app.delete("/Libros/{Titulo}", tags=["Libros"],
            summary="Eliminar un Libro",
            description="Elimina un Libro de la biblioteca.",
            responses={
                200: {"description": "Libro eliminado exitosamente."},
                404: {"description": "Libro no encontrado."}
            }
)
def eliminar_Libro(Titulo:str) -> dict:
    for index, cada_Libro in enumerate(Libros_db):
        if cada_Libro.Titulo == Titulo:
            del Libros_db[index]
            return {"detail": "Libro eliminado exitosamente."}
    raise HTTPException(status_code=404, detail="Libro no encontrado.")




#Ruta raiz
@app.get("/")
def read_root():
    return {"Bienvenido": " API de Biblioteca",
            "version" : "1.0.0",
            "endpoints" : {
                "usuarios":"/usuarios",
                "libros":"/Libros",
                "prestamos":"/prestamos",
                "documentacion swagger":"/docs"
            }}



#Ruta con parametro
#@app.get("/items/{item_id}")
#def read_item(libro_cod: int, q: str = None):
   # return {"item_id": libro_cod, "Titulo": q}

