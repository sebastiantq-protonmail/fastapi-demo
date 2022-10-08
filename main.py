from fastapi import FastAPI

from database import database as connection
from database import *

from v1 import v1

app = FastAPI(title="Prueba tecnica de FastAPI", 
              description="Esta es una prueba antes de la prueba tecnica",
              version="0.0.1") # Parámetros para documentación en http://localhost:8000/docs

@app.on_event("startup")
def startup():
    if connection.is_closed():
        connection.connect()

    connection.create_tables([Student, Account, Course, StudentCourse, Calification]) 
    
    # Se crean las tablas al iniciar el servidor
    # Si ya están creadas no hace nada

@app.on_event("shutdown")
def shutdown():
    if not connection.is_closed():
        connection.close()

# Esto se hace para tener un código más modular
app.include_router(v1, prefix="/api/v1", tags=["v1"])