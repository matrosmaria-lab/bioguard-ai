import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

st.set_page_config(page_title="BioGuard AI", page_icon="🛢️", layout="wide")

st.title("🛢️ BioGuard AI — Мониторинг и прогноз биокоррозии")
st.caption("Система интеллектуального анализа коррозионной активности на нефтепромысловых объектах")

@st.cache_resource
def load_model():
    return joblib.load('model.pkl')

model = load_model()

# Боковая панель
st.sidebar.header("🕹️ Панель управления датчиками")
val1 = st.sidebar.slider("Сулфатредуцирующие бактерии (клеток/мл)", 10.0, 100.0, 45.0)
val2 = st.sidebar.slider("Концентрация H₂S (мг/л)", 1.0, 10.0, 3.5)

input_data = pd.DataFrame([[val1, val2]], columns=['feature_1', 'feature_2'])
prediction = model.predict(input_data)[0]

# Главные колонки
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Оценка состояния")
    st.metric(label="Индекс коррозионного износа", value=f"{prediction:.1f} мм/год")
    
    if prediction > 200:
        st.error("🚨 **КРИТИЧЕСКИЙ РИСК!** Высокая скорость коррозии. Требуется непрерывная подача бактерицида.")
    elif prediction > 120:
        st.warning("⚠️ **ПОВЫШЕННЫЙ РИСК.** Превышен порог активности СРБ. Рекомендуется повторный забор проб.")
    else:
        st.success("✅ **НОРМА.** Скорость биокоррозии в пределах допустимых технологических регламентов.")

    # Выгрузка отчета
    report_data = pd.DataFrame({
        'Параметр': ['Бактерии (СРБ)', 'Сероводород H2S', 'Прогнозируемый износ'],
        'Значение': [f"{val1} кл/мл", f"{val2} мг/л", f"{prediction:.2f} мм/год"]
    })
    st.download_button(
        label="📥 Скачать отчёт (CSV)",
        data=report_data.to_csv(index=False).encode('utf-8'),
        file_name='bioguard_report.csv',
        mime='text/csv',
    )

with col2:
    st.subheader("📈 Динамика зависимости риска от бактериальной нагрузки")
    x_range = np.linspace(10, 100, 30)
    y_preds = [model.predict(pd.DataFrame([[x, val2]], columns=['feature_1', 'feature_2']))[0] for x in x_range]
    
    fig_df = pd.DataFrame({'Бактерии (клеток/мл)': x_range, 'Прогнозируемый износ': y_preds})
    fig = px.line(fig_df, x='Бактерии (клеток/мл)', y='Прогнозируемый износ', color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig, use_container_width=True)