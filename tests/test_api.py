import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Mockear joblib.load antes de que `main.py` sea importado
@patch('src.main.joblib.load')  # Mockear `joblib.load` en `src.main` 
def test_predict(mock_load):
    mock_load.return_value = "mocked_model"  # Simular la carga del modelo
    
    # Importar `app` después de aplicar el mock
    from src.main import app  # Importamos `app` solo después de haber mockeado

    client = TestClient(app)

    # Test para /predict
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
