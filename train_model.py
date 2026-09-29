import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Генерация реалистичных физических данных
np.random.seed(42)
n_samples = 1000

# Параметры: Концентрация бактерий, H2S, Температура, Минерализация
bact = np.random.uniform(10, 100, n_samples)
h2s = np.random.uniform(1, 10, n_samples)
temp = np.random.uniform(20, 80, n_samples)

# Формула реального риска с небольшим шумом
target = 15 + (bact * 2.5) + (h2s * 15) + (temp * 0.8) + np.random.normal(0, 5, n_samples)

df = pd.DataFrame({'feature_1': bact, 'feature_2': h2s, 'temp': temp, 'target': target})

X = df[['feature_1', 'feature_2']]
y = df['target']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, 'model.pkl')
print("Обновленная модель успешно сохранена!")