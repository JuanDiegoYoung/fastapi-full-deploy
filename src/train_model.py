import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

# Dataset de ejemplo
data = {
    "tamaño": [30, 40, 50, 60, 70],
    "precio": [100, 150, 200, 250, 300]
}

df = pd.DataFrame(data)

# Entrenamos modelo de regresión
X = df[["tamaño"]]
y = df["precio"]

model = LinearRegression()
model.fit(X, y)

# Guardamos el modelo
joblib.dump(model, "model/model.pkl")
print("Modelo entrenado y guardado.")
