from fastapi import FastAPI

app = FastAPI()
#Ruta raiz
@app.get("/")
def read_root():
    return {"Mensaje": "Hola bienvenido a la API de FastAPI"}

#Ruta con parametro
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "Nombre": q}


