import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Mockear joblib.load antes de importar `app`
@pytest.fixture(scope="module", autouse=True)
def mock_model_loading():
    with patch('src.main.joblib.load') as mock_load:
        mock_load.return_value = "mocked_model"  # Simular la carga del modelo
        yield mock_load  # Nos aseguramos de que el mock esté disponible

# Importar `app` después de haber mockeado
from src.main import app

client = TestClient(app)

# Test para /predict
def test_predict(mock_model_loading):
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
    
