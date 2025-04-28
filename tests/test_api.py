import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Usamos fixture para mockear antes de la importación de main.py
@pytest.fixture(scope="module", autouse=True)
def mock_joblib_load():
    with patch('joblib.load') as mock_load:  # Asegurarnos de que el mock se aplique a la ruta correcta
        mock_load.return_value = "mocked_model"
        yield mock_load  # Aseguramos que el mock esté disponible durante todo el test

# Importar `app` después de haber mockeado `joblib.load`
from src.main import app

client = TestClient(app)

# Test para /predict
def test_predict(mock_joblib_load):
    # Enviar una solicitud POST con un cuerpo de ejemplo
    response = client.post("/predict", json={"tamaño": 10})
    
    # Verificar que la respuesta tenga un código de estado 200
    assert response.status_code == 200
    
    # Verificar que la respuesta tenga el tipo correcto
    response_json = response.json()
    assert "precio_estimado" in response_json
    assert isinstance(response_json["precio_estimado"], float)

# Test para /fallar
def test_fallar():
    # Enviar una solicitud GET al endpoint que genera un error
    response = client.get("/fallar")
    
    # Verificar que la respuesta tenga un código de estado 500 (Error Interno del Servidor)
    assert response.status_code == 500
    
    # Verificar que el mensaje de error esté presente
    response_json = response.json()
    assert "detail" in response_json
