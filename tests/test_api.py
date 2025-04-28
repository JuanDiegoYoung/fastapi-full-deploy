import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Mockear joblib.load antes de que main.py sea importado
@pytest.fixture(scope="module", autouse=True)
def mock_model_loading():
    with patch('src.main.joblib.load') as mock_load:
        mock_load.return_value = "mocked_model"
        yield mock_load

# Importar `app` después de aplicar el mock
from src.main import app

client = TestClient(app)

# Test para /predict
def test_predict(mock_model_loading):
    # Enviar una solicitud POST con la API Key correcta y un cuerpo de ejemplo
    headers = {"X-API-Key": "wololo666"}  # Asegurarse de incluir la API Key
    response = client.post("/predict", json={"tamaño": 10}, headers=headers)
    
    # Verificar que la respuesta tenga un código de estado 200
    assert response.status_code == 200
    
    # Verificar que la respuesta tenga el tipo correcto
    response_json = response.json()
    assert "precio_estimado" in response_json
    assert isinstance(response_json["precio_estimado"], float)

# Test para /fallar
def test_fallar(mock_model_loading):
    # Enviar una solicitud GET con la API Key correcta
    headers = {"X-API-Key": "wololo666"}  # Asegurarse de incluir la API Key
    response = client.get("/fallar", headers=headers)
    
    # Verificar que la respuesta tenga un código de estado 500 (Error Interno del Servidor)
    assert response.status_code == 500
    
    # Verificar que el mensaje de error esté presente
    response_json = response.json()
    assert "detail" in response_json
