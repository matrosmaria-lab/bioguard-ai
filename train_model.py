import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Фиксируем случайность для воспроизводимости
np.random.seed(42)
n_samples = 1200

# 1. Генерация реалистичного датасета факторов биокоррозии
bacterial_load = np.random.uniform(10, 1000, n_samples)  # кл/мл
ph_level = np.random.uniform(4.5, 8.5, n_samples)         # pH
temperature = np.random.uniform(10, 60, n_samples)       # °C
flow_rate = np.random.uniform(0.1, 3.5, n_samples)       # м/с
salinity = np.random.uniform(5, 150, n_samples)          # г/л
h2s_content = np.random.uniform(0, 50, n_samples)        # мг/л

# Формула расчета скорости коррозии с учетом физико-химических зависимостей
corrosion_rate = (
    0.15 * np.sqrt(bacterial_load) +
    0.08 * (7.5 - ph_level)**2 +
    0.03 * temperature +
    0.05 * salinity +
    0.04 * h2s_content +
    0.02 / (flow_rate + 0.1) +
    np.random.normal(0, 0.15, n_samples)
)
corrosion_rate = np.maximum(0.01, corrosion_rate)

df = pd.DataFrame({
    'bacterial_load': bacterial_load,
    'ph_level': ph_level,
    'temperature': temperature,
    'flow_rate': flow_rate,
    'salinity': salinity,
    'h2s_content': h2s_content,
    'corrosion_rate': corrosion_rate
})

X = df.drop(columns=['corrosion_rate'])
y = df['corrosion_rate']

# 2. Обучение ансамблевой модели Random Forest
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# 3. Сохранение модели и списка признаков
payload = {
    'model': model,
    'feature_names': list(X.columns)
}
joblib.dump(payload, 'model.pkl')
print("Модель успешно обучена и сохранена в model.pkl!")