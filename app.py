import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

# 1. Конфигурация страницы
st.set_page_config(
    page_title="BioGuard AI — Мониторинг биокоррозии",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Исправление CSS-стилей (Адаптивность + Чёткие контрастные тексты)
st.markdown("""
<style>
    /* Главный фон страницы */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    
    /* Принудительный тёмный цвет для всех надписей у слайдеров и полей */
    .stSlider label, .stNumberInput label, .stSelectbox label, p, span, div {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Шапка сайта (Баннер) */
    .hero-header {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        border-radius: 16px;
        padding: 24px;
        color: white !important;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.2);
        margin-bottom: 24px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
    }
    
    .hero-header *, .hero-header p, .hero-header h1, .hero-header div {
        color: white !important;
    }
    
    .status-badge {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.3);
        white-space: nowrap;
    }

    /* Карточки для блоков */
    .custom-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    /* Адаптивность для мобильных устройств */
    @media (max-width: 768px) {
        .hero-header {
            flex-direction: column;
            align-items: flex-start;
            padding: 18px;
        }
        .block-container {
            padding-left: 12px !important;
            padding-right: 12px !important;
            padding-top: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 3. Загрузка модели
@st.cache_resource
def load_model():
    try:
        return joblib.load("model.pkl")
    except Exception as e:
        st.error(f"Ошибка загрузки модели `model.pkl`: {e}")
        return None

model = load_model()

# 4. Шапка приложения (Адаптивный баннер)
st.markdown("""
<div class="hero-header">
    <div>
        <h1 style="margin: 0; font-size: 28px; font-weight: 700;">🌿 BioGuard AI</h1>
        <p style="margin: 6px 0 0 0; opacity: 0.9; font-weight: 400 !important;">
            Интеллектуальная система управления рисками биокоррозии и мониторинга объектов
        </p>
    </div>
    <div class="status-badge">
        🟢 Система активна
    </div>
</div>
""", unsafe_allow_html=True)

# 5. Вкладки навигации
tab1, tab2, tab3 = st.tabs([
    "📊 Экспресс-прогноз", 
    "📁 Пакетный анализ (CSV/Excel)", 
    "🔍 Вклад факторов (XAI)"
])

# ==========================================
# ВКЛАДКА 1: Экспресс-прогноз
# ==========================================
with tab1:
    col_input, col_result = st.columns([1.1, 0.9], gap="large")
    
    with col_input:
        st.markdown('### ⚙️ Параметры трубопровода / среды')
        
        # Слайдеры вводных данных
        bact = st.slider("Бактериальная нагрузка (СВБ, клеток/мл)", 0, 1000, 350, step=10)
        ph = st.slider("Уровень pH среды", 4.0, 9.0, 6.8, step=0.1)
        temp = st.slider("Температура (°C)", 10, 90, 32, step=1)
        flow = st.slider("Скорость потока (м/с)", 0.1, 5.0, 1.2, step=0.1)
        salinity = st.slider("Минерализация / Соли (г/л)", 10, 300, 45, step=5)
        h2s = st.slider("Содержание H₂S (мг/л)", 0, 100, 12, step=1)

    with col_result:
        st.markdown('### 📈 Результат моделирования')
        
        if model is not None:
            # Формируем вектор фичей для модели
            features = np.array([[ph, temp, flow, salinity, h2s, bact]])
            prediction = float(model.predict(features)[0])
            
            # Определение уровня риска
            if prediction < 3.0:
                risk_label = "НИЗКИЙ РИСК"
                risk_color = "#10b981"
                bg_color = "#ecfdf5"
                recommendation = "Параметры в норме. Дополнительная обработка не требуется."
            elif prediction < 7.0:
                risk_label = "СРЕДНИЙ РИСК"
                risk_color = "#f59e0b"
                bg_color = "#fffbeb"
                recommendation = "Рекомендуется плановый контроль и профилактическая дозировка бактерицида."
            else:
                risk_label = "КРИТИЧЕСКИЙ РИСК"
                risk_color = "#ef4444"
                bg_color = "#fef2f2"
                recommendation = "Требуется немедленная подача увеличенной дозировки бактерицида и ингибитора!"

            # Карточка результатов
            st.markdown(f"""
            <div style="background-color: {bg_color}; border: 2px solid {risk_color}; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <div style="font-size: 14px; color: #64748b; font-weight: 600;">Прогнозируемая скорость износа:</div>
                <div style="font-size: 38px; font-weight: 800; color: #0f172a; margin: 4px 0;">{prediction:.2f} <span style="font-size: 20px;">мм/год</span></div>
                <div style="display: inline-block; background-color: {risk_color}; color: white !important; font-weight: 700 !important; padding: 4px 12px; border-radius: 6px; font-size: 13px;">
                    ● {risk_label}
                </div>
                <div style="margin-top: 12px; font-size: 13px; color: #334155;">{recommendation}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # График зависимости от бактерий
            st.markdown('#### 📉 Зависимость износа от роста бактерий')
            
            bact_range = np.linspace(10, 1000, 50)
            sim_features = np.array([[ph, temp, flow, salinity, h2s, b] for b in bact_range])
            preds = model.predict(sim_features)
            
            fig = px.line(
                x=bact_range, 
                y=preds, 
                labels={'x': 'Бактерии (кл/мл)', 'y': 'Износ (мм/год)'},
                color_discrete_sequence=['#10b981']
            )
            
            fig.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=260,
                font=dict(color="#1e293b", size=12),
                xaxis=dict(showgrid=True, gridcolor='#e2e8f0', tickformat='.0f'),
                yaxis=dict(showgrid=True, gridcolor='#e2e8f0', tickformat='.2f')
            )
            
            # Отрисовка графика без наезжающей панели инструментов Plotly
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ==========================================
# ВКЛАДКА 2: Пакетный анализ (CSV/Excel)
# ==========================================
with tab2:
    st.markdown('### 📁 Загрузка файла для массового расчёта')
    st.write("Загрузите CSV-файл с колонками: `ph`, `temperature`, `flow_rate`, `salinity`, `h2s`, `bacteria_count`")
    
    uploaded_file = st.file_uploader("Выберите CSV файл", type=["csv"])
    if uploaded_file is not None and model is not None:
        try:
            df = pd.read_csv(uploaded_file)
            req_cols = ['ph', 'temperature', 'flow_rate', 'salinity', 'h2s', 'bacteria_count']
            
            if all(col in df.columns for col in req_cols):
                df_features = df[req_cols]
                df['Predicted_Corrosion_mm_year'] = model.predict(df_features)
                
                st.success("Расчёт успешно выполнен!")
                st.dataframe(df, use_container_width=True)
                
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Скачать результаты (CSV)",
                    data=csv_data,
                    file_name="bioguard_predictions.csv",
                    mime="text/csv"
                )
            else:
                st.error(f"В файле отсутствуют необходимые колонки. Требуются: {', '.join(req_cols)}")
        except Exception as e:
            st.error(f"Ошибка чтения файла: {e}")

# ==========================================
# ВКЛАДКА 3: Вклад факторов (XAI)
# ==========================================
with tab3:
    st.markdown('### 🔍 Важность параметров в прогнозе модели')
    st.write("График показывает, какие показатели оказывают наибольшее влияние на итоговый расчёт скорости биокоррозии.")
    
    if model is not None and hasattr(model, 'feature_importances_'):
        feature_names = ['pH', 'Температура', 'Скорость потока', 'Соли / Минерализация', 'Сероводород (H₂S)', 'Бактерии (СВБ)']
        importances = model.feature_importances_
        
        fi_df = pd.DataFrame({'Параметр': feature_names, 'Важность': importances})
        fi_df = fi_df.sort_values(by='Важность', ascending=True)
        
        fig_imp = px.bar(
            fi_df, 
            x='Важность', 
            y='Параметр', 
            orientation='h',
            color='Важность',
            color_continuous_scale='Emrld'
        )
        fig_imp.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            font=dict(color="#1e293b", size=12),
            xaxis=dict(showgrid=True, gridcolor='#e2e8f0'),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_imp, use_container_width=True, config={'displayModeBar': False})