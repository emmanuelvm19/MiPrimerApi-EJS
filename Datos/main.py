from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field
import json
import os

app = FastAPI(
    title="API Bibliotecaria",
    description="API para sistema Bibliotecario",
    version="1.0.0"
)

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

'''''
#Se crea Clase libro con los datos del Json
class Libros(BaseModel):
    Titulo: str
    Autor: str
    Isbn: str
    Editorial: str
    Anio: int
    Precio: float
    Idioma: str
    Categoria: str

def cargar_datos():
    global Libros_db
    try:
        # Cargar Libros
        if os.path.exists("Datos/Libros.json"):
            with open("Datos/Libros.json", 'r', encoding='utf-8') as f:
                Libros_db = json.load(f) #Esto carga todos los libros

        print(f" Libros cargados: {len(Libros_db)}")

    except Exception as e:
        print(f"No se pudo cargar los libros: {e}")

# Ejecutar la carga al iniciar
cargar_datos()
'''''

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