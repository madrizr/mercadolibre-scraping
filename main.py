from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import json
# El módulo subprocess permite ejecutar nuevos procesos.
import subprocess

app = FastAPI()

# Definir endpoint HTTP GET en la ruta "/".
@app.get("/")
def index():
    
    # Ejecutar el comando para iniciar el spider de Scrapy llamado "mercadolibre".
    # Los resultados del scraping son guardados en el archivo data.json.
    subprocess.run(["scrapy", "crawl", "mercadolibre", "-o", "./mercadolibrescrap/data.json"])
    
    # Intentar abrir y leer el archivo data.json.
    try:
        with open('./mercadolibrescrap/data.json') as json_file:
            data = json.load(json_file)
    
    # Si el archivo no se encuentra, se maneja la excepción FileNotFoundError.
    except FileNotFoundError:
        data = {
            'message': 'Datos no encontrados',
            'status': '404'
        }        
        
    return data

