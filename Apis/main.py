from fastapi import FastAPI

app = FastAPI()
#Ruta raiz
@app.get("/")
def read_root():
    return {"Bienvenida": "Hola, bienvenido a la biblioteca (realizada con API rest)"}

#Ruta con parametro
@app.get("/items/{item_id}")
def read_item(libro_id: int, q: str = None):
    return {"item_id": libro_id, "Titulo": q}


