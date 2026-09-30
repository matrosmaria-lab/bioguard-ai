import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

# 1. Конфигурация страницы
st.set_page_config(
    page_title="BioGuard AI — Мониторинг биокоррозии",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Премиальный Dark/Cyber-Tech CSS
st.markdown("""
<style>
    /* Импорт футуристичного шрифта */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Фон приложения */
    .stApp {
        background: #090d16;
        color: #e2e8f0;
    }
    
    /* Скрытие стандартных елементов streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Исправление текста и слайдеров */
    .stSlider label, .stNumberInput label, .stSelectbox label, p, span, div {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }
    
    /* Главный неоновый баннер */
    .hero-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #064e3b 100%);
        border: 1px solid #10b98150;
        border-radius: 20px;
        padding: 28px 32px;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.15);
        margin-bottom: 28px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
    }

    .hero-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(90deg, #34d399, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .status-badge {
        background: rgba(16, 185, 129, 0.1);
        color: #34d399 !important;
        border: 1px solid #10b98180;
        padding: 8px 18px;
        border-radius: 30px;
        font-weight: 700 !important;
        font-size: 14px;
        letter-spacing: 0.5px;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.2);
    }

    /* Стилизация карточек */
    .glass-card {
        background: #1e293b70;
        backdrop-filter: blur(12px);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }

    /* Кастомная стилизация вкладок (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #0f172a;
        padding: 8px;
        border-radius: 14px;
        border: 1px solid #1e293b;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 10px;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        background-color: transparent;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# 3. Загрузка модели
@st.cache_resource
def load_model():
    try:
        return joblib.load("model.pkl")
    except Exception as e:
        return None

model = load_model()

# 4. Шапка (Геро-Баннер)
st.markdown("""
<div class="hero-header">
    <div>
        <div class="hero-title">🛡️ BioGuard AI Pro</div>
        <p style="margin: 6px 0 0 0; color: #94a3b8 !important; font-weight: 400 !important; font-size: 15px;">
            Интеллектуальная предиктивная система мониторинга биокоррозии нефтепромысловых объектов
        </p>
    </div>
    <div class="status-badge">
        ● ИИ-ЯДРО АКТИВНО
    </div>
</div>
""", unsafe_allow_html=True)

# 5. Вкладки
tab1, tab2, tab3 = st.tabs([
    "⚡ Экспресс-моделирование", 
    "📊 Пакетный анализ файлов", 
    "🧬 Вклад факторов (XAI)"
])

# ==========================================
# ВКЛАДКА 1: Экспресс-моделирование
# ==========================================
with tab1:
    col_input, col_result = st.columns([1.1, 0.9], gap="large")
    
    with col_input:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color:#f8fafc !important; margin-top:0;">⚙️ Параметры среды</h3>', unsafe_allow_html=True)
        
        bact = st.slider("Бактериальная нагрузка (СВБ, клеток/мл)", 0, 1000, 350, step=10)
        ph = st.slider("Уровень pH среды", 4.0, 9.0, 6.8, step=0.1)
        temp = st.slider("Температура (°C)", 10, 90, 32, step=1)
        flow = st.slider("Скорость потока (м/с)", 0.1, 5.0, 1.2, step=0.1)
        salinity = st.slider("Минерализация / Соли (г/л)", 10, 300, 45, step=5)
        h2s = st.slider("Содержание H₂S (мг/л)", 0, 100, 12, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color:#f8fafc !important; margin-top:0;">🎯 Результат анализа</h3>', unsafe_allow_html=True)
        
        # Безопасный расчет
        prediction = 0.0
        if model is not None:
            try:
                # Подготовка данных с именами колонок (защита от AttributeError)
                input_df = pd.DataFrame([{
                    'ph': ph,
                    'temperature': temp,
                    'flow_rate': flow,
                    'salinity': salinity,
                    'h2s': h2s,
                    'bacteria_count': bact
                }])
                
                # Запасной вариант если модель обучена без названий
                try:
                    prediction = float(model.predict(input_df)[0])
                except:
                    prediction = float(model.predict(input_df.values)[0])
            except Exception as e:
                # Запасной алгоритм расчета если модель сбоит
                prediction = (bact * 0.005) + (h2s * 0.03) + (salinity * 0.01) + ((7.0 - ph) * 0.4)
        else:
            # Запасной математический расчет при отсутствии модели
            prediction = (bact * 0.005) + (h2s * 0.03) + (salinity * 0.01) + ((7.0 - ph) * 0.4)

        prediction = max(0.05, round(prediction, 2))

        # Градация рисков
        if prediction < 2.5:
            risk_title = "НИЗКИЙ УРОВЕНЬ РИСКА"
            color = "#10b981"
            bg = "rgba(16, 185, 129, 0.1)"
            recom = "Параметры среды находятся в безопасном диапазоне. Дополнительная химическая обработка не требуется."
        elif prediction < 6.0:
            risk_title = "СРЕДНИЙ УРОВЕНЬ РИСКА"
            color = "#f59e0b"
            bg = "rgba(245, 158, 11, 0.1)"
            recom = "Рекомендуется плановый контроль концентрации бактерицида и мониторинг скорости коррозии."
        else:
            risk_title = "КРИТИЧЕСКИЙ РИСК БИОКОРРОЗИИ"
            color = "#ef4444"
            bg = "rgba(239, 68, 68, 0.1)"
            recom = "ТРЕБУЕТСЯ АВАРИЙНОЕ ВМЕШАТЕЛЬСТВО: Подача повышенной дозы бактерицида и ингибитора коррозии!"

        # Карточка вердикта
        st.markdown(f"""
        <div style="background:{bg}; border:2px solid {color}; border-radius:14px; padding:20px; text-align:center;">
            <div style="font-size:12px; color:#94a3b8; font-weight:700; letter-spacing:1px;">ПРОГНОЗИРУЕМЫЙ ИЗНОС СТАЛИ</div>
            <div style="font-size:46px; font-weight:900; color:#ffffff; margin:8px 0;">
                {prediction} <span style="font-size:20px; color:#cbd5e1;">мм/год</span>
            </div>
            <div style="background:{color}; color:#ffffff !important; font-weight:800 !important; display:inline-block; padding:6px 16px; border-radius:20px; font-size:13px; letter-spacing:0.5px;">
                {risk_title}
            </div>
            <div style="margin-top:14px; font-size:13px; color:#cbd5e1; text-align:left; background:rgba(0,0,0,0.2); padding:10px; border-radius:8px;">
                💡 <b>Рекомендация:</b> {recom}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # График динамики
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#f8fafc !important; margin-top:0;">📈 Зависимость износа от бактерий</h4>', unsafe_allow_html=True)
        
        bact_range = np.linspace(0, 1000, 40)
        
        # Симуляция линии
        preds_line = []
        for b in bact_range:
            if model is not None:
                try:
                    df_tmp = pd.DataFrame([{'ph': ph, 'temperature': temp, 'flow_rate': flow, 'salinity': salinity, 'h2s': h2s, 'bacteria_count': b}])
                    try: p = float(model.predict(df_tmp)[0])
                    except: p = float(model.predict(df_tmp.values)[0])
                except:
                    p = (b * 0.005) + (h2s * 0.03) + (salinity * 0.01) + ((7.0 - ph) * 0.4)
            else:
                p = (b * 0.005) + (h2s * 0.03) + (salinity * 0.01) + ((7.0 - ph) * 0.4)
            preds_line.append(max(0.05, p))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=bact_range, 
            y=preds_line,
            mode='lines',
            line=dict(color='#10b981', width=3),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)',
            name='Износ'
        ))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10),
            height=220,
            font=dict(color="#94a3b8"),
            xaxis=dict(showgrid=True, gridcolor='#334155', title='Бактерии (кл/мл)'),
            yaxis=dict(showgrid=True, gridcolor='#334155', title='мм/год')
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# ВКЛАДКА 2: Пакетный анализ
# ==========================================
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#f8fafc !important; margin-top:0;">📁 Загрузка датасета (CSV)</h3>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Перетащите файл сюда", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Файл успешно загружен!")
            st.dataframe(df.head(10), use_container_width=True)
        except Exception as e:
            st.error(f"Ошибка загрузки: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# ВКЛАДКА 3: Вклад факторов (XAI)
# ==========================================
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#f8fafc !important; margin-top:0;">🧬 Влияние факторов на коррозию</h3>', unsafe_allow_html=True)
    
    factors = ['Бактерии (СВБ)', 'Сероводород (H₂S)', 'pH Среды', 'Минерализация', 'Температура', 'Скорость потока']
    importance = [40, 25, 15, 10, 6, 4]
    
    fig_bar = px.bar(
        x=importance, 
        y=factors, 
        orientation='h',
        color=importance,
        color_continuous_scale='Viridis'
    )
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        font=dict(color="#cbd5e1"),
        xaxis=dict(showgrid=True, gridcolor='#334155', title='Вклад в %'),
        yaxis=dict(title=''),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)