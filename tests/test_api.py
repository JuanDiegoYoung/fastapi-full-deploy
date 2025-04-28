import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# El mock debe aplicarse antes de importar 'app' para evitar que se cargue el modelo
with patch('src.main.joblib.load') as mock_load:
    mock_load.return_value = "mocked_model"  # O lo que sea que esperes como "modelo"

    from src.main import app  # Ahora importamos 'app' después de aplicar el mock

client = TestClient(app)

# Test para /predict
def test_predict():
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
