from fastapi import FastAPI
from fastapi import Request, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import joblib
import numpy as np
import logging
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

# Definir la cabecera de la API key
API_KEY = "wololo666"

api_key_header = APIKeyHeader(name="X-API-Key")

# Dependencia para validar el token
def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Acceso denegado. Token incorrecto o no proporcionado.",
        )
    return api_key

logging.basicConfig(
    level=logging.INFO, #No muestra DEBUG
    format="%(asctime)s [%(levelname)s] %(message)s", #hora, nivel del mensaje, contenido
    handlers=[ #Lo guarda en un archivo
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()
Instrumentator().instrument(app).expose(app)

# Cargar el modelo entrenado
model = joblib.load("model/model.pkl")

# Definir el schema del input
class Item(BaseModel):
    tamaño: float

@app.get("/")
def read_root(api_key: str = Depends(get_api_key)):
    logger.info("Se accedió al endpoint raíz")
    return {"message": "¡Hola desde FastAPI!"}

@app.post("/predict")
def predict_price(item: Item, api_key: str = Depends(get_api_key)):
    logger.info("Predicción ejecutada con éxito")
    X = np.array([[item.tamaño]])
    prediction = model.predict(X)
    return {"tamaño": item.tamaño, "precio_estimado": prediction[0]}

@app.get("/fallar")
def error_route(api_key: str = Depends(get_api_key)):
    try:
        raise Exception("Esto es un error simulado")
    except Exception as e:
        logger.exception("Error en /fallar")
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )