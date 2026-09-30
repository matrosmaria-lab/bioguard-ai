import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

# --- 1. Настройки страницы ---
st.set_page_config(
    page_title="BioGuard AI — Мониторинг коррозии",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Пользовательские стили (Сбер / Чистый Изумрудный Стиль) ---
st.markdown("""
    <style>
    /* Основной фон и шрифты */
    .stApp {
        background-color: #f4f7f6;
        color: #1c2826;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Верхний навигационный банер */
    .top-navbar {
        background: linear-gradient(135deg, #0e8345 0%, #10b981 100%);
        padding: 20px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.2);
    }
    .top-navbar h1 {
        color: white !important;
        margin: 0;
        font-size: 28px;
        font-weight: 700;
    }
    .top-navbar p {
        color: #e6f4ea;
        margin: 5px 0 0 0;
        font-size: 14px;
    }

    /* Стильные карточки */
    .custom-card {
        background-color: #ffffff;
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }
    
    /* Красивые плашки статусов */
    .status-badge {
        padding: 8px 16px;
        border-radius: 30px;
        font-weight: 600;
        display: inline-block;
        font-size: 14px;
    }
    .status-low { background-color: #d1fae5; color: #065f46; }
    .status-medium { background-color: #fef3c7; color: #92400e; }
    .status-high { background-color: #fee2e2; color: #991b1b; }

    /* Кнопки в эко-стиле */
    .stButton>button {
        background-color: #10b981;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #059669;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. Загрузка модели ---
@st.cache_resource
def load_model():
    try:
        data = joblib.load('model.pkl')
        if isinstance(data, dict):
            return data['model'], data['feature_names']
        return data, ['bacterial_load', 'ph_level', 'temperature', 'flow_rate', 'salinity', 'h2s_content']
    except Exception:
        st.error("Не удалось загрузить файл model.pkl. Запустите сначала train_model.py")
        return None, []

model, feature_names = load_model()

# --- 4. Шапка сайта (Navbar) ---
st.markdown("""
    <div class="top-navbar">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1>🌿 BioGuard AI</h1>
                <p>Интеллектуальная система управления рисками биокоррозии и мониторинга объектов</p>
            </div>
            <div>
                <span style="background: rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 20px; font-size: 13px;">
                    🟢 Система активна
                </span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 5. Навигация по вкладкам ---
tab1, tab2, tab3 = st.tabs([
    "📊 Экспресс-прогноз", 
    "📁 Пакетный анализ (CSV/Excel)", 
    "🧠 Explainable AI (Анализ факторов)"
])

# ==================== ВКЛАДКА 1: ЭКСПРЕСС-ПРОГНОЗ ====================
with tab1:
    st.subheader("Введите текущие параметры трубопровода / среды")
    
    col_input, col_result = st.columns([1.1, 1])
    
    with col_input:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.write("##### ⚙️ Физико-химические показатели")
        
        bacterial_load = st.slider("Бактериальная нагрузка (СВБ, кл/мл)", 10, 1000, 350)
        ph_level = st.slider("Уровень pH среды", 4.0, 9.0, 6.8, 0.1)
        temperature = st.slider("Температура (°C)", 10, 70, 32)
        flow_rate = st.slider("Скорость потока (м/с)", 0.1, 4.0, 1.2, 0.1)
        salinity = st.slider("Минерализация / Соли (г/л)", 5, 200, 45)
        h2s_content = st.slider("Содержание H₂S (мг/л)", 0, 60, 12)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_result:
        if model:
            input_df = pd.DataFrame([[bacterial_load, ph_level, temperature, flow_rate, salinity, h2s_content]], 
                                    columns=feature_names)
            pred_rate = model.predict(input_df)[0]
            
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.write("##### 📈 Результат моделирования")
            
            st.metric("Прогнозируемая скорость износа", f"{pred_rate:.2f} мм/год")
            
            if pred_rate < 1.0:
                st.markdown('<span class="status-badge status-low">🟢 Низкий риск (Норма)</span>', unsafe_allow_html=True)
                st.info("Регулярный мониторинг. Дополнительная обработка не требуется.")
            elif pred_rate < 2.2:
                st.markdown('<span class="status-badge status-medium">🟡 Умеренный риск</span>', unsafe_allow_html=True)
                st.warning("Рекомендуется запланировать ввод бактерицида во время ТО.")
            else:
                st.markdown('<span class="status-badge status-high">🔴 КРИТИЧЕСКИЙ РИСК</span>', unsafe_allow_html=True)
                st.error("Требуется немедленная подача дозировки бактерицида и ингибитора!")
                
            st.markdown('</div>', unsafe_allow_html=True)
            
            # График зависимости от бактерий
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.write("##### 📉 Зависимость износа от роста бактерий")
            
            bact_range = np.linspace(10, 1000, 30)
            temp_df = pd.DataFrame({
                'bacterial_load': bact_range,
                'ph_level': ph_level,
                'temperature': temperature,
                'flow_rate': flow_rate,
                'salinity': salinity,
                'h2s_content': h2s_content
            })
            preds = model.predict(temp_df)
            
            fig = px.line(x=bact_range, y=preds, labels={'x': 'Бактерии (кл/мл)', 'y': 'Износ (мм/год)'},
                          color_discrete_sequence=['#10b981'])
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ==================== ВКЛАДКА 2: ПАКЕТНЫЙ АНАЛИЗ ====================
with tab2:
    st.subheader("Загрузка истории измерений для массового анализа")
    
    col_up, col_info = st.columns([2, 1])
    with col_up:
        uploaded_file = st.file_uploader("Загрузите файл CSV с параметрами объекта", type=["csv"])
    with col_info:
        st.info("Шаблон CSV должен содержать колонки: bacterial_load, ph_level, temperature, flow_rate, salinity, h2s_content.")
        
    if uploaded_file is not None and model:
        df_batch = pd.read_csv(uploaded_file)
        st.write("##### 📋 Загруженные данные (первые 5 строк):")
        st.dataframe(df_batch.head(), use_container_width=True)
        
        # Расчет прогнозов
        df_batch['Predicted_Corrosion_Rate'] = model.predict(df_batch[feature_names])
        
        st.write("##### 📊 Аналитика по всему массиву:")
        c1, c2, c3 = st.columns(3)
        c1.metric("Средний износ", f"{df_batch['Predicted_Corrosion_Rate'].mean():.2f} мм/год")
        c2.metric("Максимальный риск", f"{df_batch['Predicted_Corrosion_Rate'].max():.2f} мм/год")
        c3.metric("Всего замеров", len(df_batch))
        
        # График распределения
        fig_batch = px.histogram(df_batch, x="Predicted_Corrosion_Rate", nbins=20, 
                                 title="Распределение скоростей коррозии",
                                 color_discrete_sequence=['#059669'])
        st.plotly_chart(fig_batch, use_container_width=True)
        
        # Скачивание результата
        csv_data = df_batch.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Скачать полный отчёт с прогнозами (CSV)", data=csv_data, file_name="bioguard_report.csv", mime="text/csv")

# ==================== ВКЛАДКА 3: EXPLAINABLE AI ====================
with tab3:
    st.subheader("🧠 Объяснение решений модели (Вклад факторов)")
    st.write("Оценка того, какие именно физико-химические параметры оказывают наибольшее влияние на процесс биокоррозии.")
    
    if model and hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feature_names_ru = [
            'Бактериальная нагрузка', 'Уровень pH', 'Температура', 
            'Скорость потока', 'Минерализация (Соли)', 'Содержание H₂S'
        ]
        
        importance_df = pd.DataFrame({
            'Фактор': feature_names_ru,
            'Влияние (%)': importances * 100
        }).sort_values(by='Влияние (%)', ascending=True)
        
        fig_imp = px.bar(importance_df, x='Влияние (%)', y='Фактор', orientation='h',
                         color='Влияние (%)', color_continuous_scale='Greens',
                         title="Весомость факторов в принятии решений AI")
        fig_imp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_imp, use_container_width=True)
        
        st.success("💡 **Вывод анализа:** Основными драйверами коррозийного износа выступают бактериальная активность и кислотность среды (pH).")