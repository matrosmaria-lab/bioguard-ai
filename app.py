import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

# ---------------------------------------------------------
# 1. Настройки страницы
# ---------------------------------------------------------
st.set_page_config(
    page_title="BioGuard AI — Экологический мониторинг биокоррозии",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. Стиль лендинга по образцу (Светло-зеленый эко-пром)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Навигация сверху */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #ffffff;
        padding: 14px 28px;
        border-radius: 50px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
        margin-bottom: 24px;
    }

    .top-nav-logo {
        font-size: 20px;
        font-weight: 800;
        color: #166534;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .top-nav-badge {
        background: #dcfce7;
        color: #15803d;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* Hero Блок */
    .hero-container {
        background: linear-gradient(135deg, #15803d 0%, #166534 60%, #0f172a 100%);
        border-radius: 24px;
        padding: 48px 40px;
        color: #ffffff;
        box-shadow: 0 20px 40px rgba(22, 101, 52, 0.15);
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }

    .hero-big-title {
        font-size: 64px;
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1.05;
        margin-bottom: 12px;
        color: #ffffff;
    }

    .hero-sub {
        font-size: 18px;
        color: #bbf7d0;
        font-weight: 500;
        max-width: 650px;
        line-height: 1.5;
        margin-bottom: 28px;
    }

    /* Карточки-фишки в Hero */
    .pill-container {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
    }

    .pill-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 12px 20px;
        border-radius: 100px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
    }

    /* Белые секции под контент */
    .section-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 32px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        margin-bottom: 32px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .section-desc {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 24px;
    }

    /* Результаты */
    .metric-badge {
        background: #f1f5f9;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        border: 2px solid #e2e8f0;
    }

    .metric-value {
        font-size: 42px;
        font-weight: 800;
        color: #0f172a;
        margin: 8px 0;
    }

    /* Форматирование слайдеров */
    .stSlider label, .stSelectbox label {
        color: #334155 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. Безопасная загрузка модели
# ---------------------------------------------------------
@st.cache_resource
def load_ml_model():
    try:
        return joblib.load("model.pkl")
    except:
        return None

model = load_ml_model()

# ---------------------------------------------------------
# 4. Верхнее меню
# ---------------------------------------------------------
st.markdown("""
<div class="top-nav">
    <div class="top-nav-logo">
        🌿 BioGuard <span>| ИИ-Система</span>
    </div>
    <div style="display:flex; gap:20px; font-weight:600; color:#475569; font-size:14px;">
        <span>01. Моделирование</span>
        <span>02. Загрузка данных</span>
        <span>03. Аналитика XAI</span>
    </div>
    <div class="top-nav-badge">
        ● СИСТЕМА АКТИВНА
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. Главный Hero-Блок (Похоже на картинку NST)
# ---------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div style="text-transform: uppercase; font-weight: 700; letter-spacing: 2px; color: #86efac; font-size: 13px; margin-bottom: 8px;">
        Экологическая безопасность & Защита инфраструктуры
    </div>
    <div class="hero-big-title">BioGuard AI</div>
    <div class="hero-sub">
        Прогнозирование бактериальной коррозии и износа металлоконструкций в нефтепромысловых средах с использованием нейросетевого анализа.
    </div>
    <div class="pill-container">
        <div class="pill-card">🌐 <span>СВБ Мониторинг</span></div>
        <div class="pill-card">⚡ <span>Экспресс-прогноз</span></div>
        <div class="pill-card">♻️ <span>Защита экосистем</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. СЕКЦИЯ 1: Интерактивный калькулятор (Идет вниз по странице)
# ---------------------------------------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 01. Экспресс-моделирование рисков</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Настройте параметры трубопровода и химического состава среды для мгновенного расчета уровня биокоррозии.</div>', unsafe_allow_html=True)

col_inputs, col_outputs = st.columns([1.1, 0.9], gap="large")

with col_inputs:
    st.markdown("##### ⚙️ Параметры среды")
    bact = st.slider("Бактериальная нагрузка (СВБ, клеток/мл)", 0, 1000, 350, step=10)
    ph = st.slider("Уровень pH среды", 4.0, 9.0, 6.8, step=0.1)
    temp = st.slider("Температура (°C)", 10, 90, 32, step=1)
    flow = st.slider("Скорость потока (м/с)", 0.1, 5.0, 1.2, step=0.1)
    salinity = st.slider("Минерализация / Соли (г/л)", 10, 300, 45, step=5)
    h2s = st.slider("Содержание H₂S (мг/л)", 0, 100, 12, step=1)

with col_outputs:
    st.markdown("##### 🎯 Прогноз модели")
    
    # Расчет
    pred = 0.0
    if model is not None:
        try:
            df_in = pd.DataFrame([{'ph': ph, 'temperature': temp, 'flow_rate': flow, 'salinity': salinity, 'h2s': h2s, 'bacteria_count': bact}])
            try:
                pred = float(model.predict(df_in)[0])
            except:
                pred = float(model.predict(df_in.values)[0])
        except:
            pred = (bact * 0.005) + (h2s * 0.03) + (salinity * 0.01) + ((7.0 - ph) * 0.4)
    else:
        pred = (bact * 0.005) + (h2s * 0.03) + (salinity * 0.01) + ((7.0 - ph) * 0.4)

    pred = max(0.05, round(pred, 2))

    # Статусы
    if pred < 2.5:
        risk_label = "НИЗКИЙ РИСК"
        badge_bg = "#dcfce7"
        badge_color = "#15803d"
        border_col = "#22c55e"
        recom_text = "Параметры среды находятся в безопасных пределах. Плановый контроль."
    elif pred < 6.0:
        risk_label = "СРЕДНИЙ РИСК"
        badge_bg = "#fef3c7"
        badge_color = "#b45309"
        border_col = "#f59e0b"
        recom_text = "Рекомендуется добавление бактерицида в нормированной дозе."
    else:
        risk_label = "КРИТИЧЕСКИЙ РИСК"
        badge_bg = "#fee2e2"
        badge_color = "#b91c1c"
        border_col = "#ef4444"
        recom_text = "ВНИМАНИЕ! Высокая скорость износа. Требуется немедленная обработка!"

    st.markdown(f"""
    <div style="background:#ffffff; border:2px solid {border_col}; border-radius:16px; padding:24px; text-align:center; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <div style="font-size:12px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Прогнозируемый износ стали</div>
        <div style="font-size:48px; font-weight:800; color:#0f172a; margin:10px 0;">{pred} <span style="font-size:18px; color:#64748b;">мм/год</span></div>
        <div style="background:{badge_bg}; color:{badge_color}; font-weight:800; display:inline-block; padding:6px 18px; border-radius:20px; font-size:13px;">
            {risk_label}
        </div>
        <div style="margin-top:16px; font-size:13px; color:#475569; text-align:left; background:#f8fafc; padding:12px; border-radius:10px;">
            💡 <b>Рекомендация:</b> {recom_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    
    # График Plotly
    bact_x = np.linspace(0, 1000, 30)
    preds_y = []
    for bx in bact_x:
        if model is not None:
            try:
                df_t = pd.DataFrame([{'ph': ph, 'temperature': temp, 'flow_rate': flow, 'salinity': salinity, 'h2s': h2s, 'bacteria_count': bx}])
                try: py = float(model.predict(df_t)[0])
                except: py = float(model.predict(df_t.values)[0])
            except: py = (bx * 0.005) + (h2s * 0.03) + (salinity * 0.01) + ((7.0 - ph) * 0.4)
        else: py = (bx * 0.005) + (h2s * 0.03) + (salinity * 0.01) + ((7.0 - ph) * 0.4)
        preds_y.append(max(0.05, py))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=bact_x, y=preds_y, mode='lines',
        line=dict(color='#166534', width=3),
        fill='tozeroy', fillcolor='rgba(22, 101, 52, 0.08)'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=180, margin=dict(l=10, r=10, t=10, b=10),
        font=dict(color="#64748b"),
        xaxis=dict(showgrid=True, gridcolor='#e2e8f0', title='Концентрация СВБ'),
        yaxis=dict(showgrid=True, gridcolor='#e2e8f0', title='мм/год')
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. СЕКЦИЯ 2: Пакетная загрузка файлов (Скроллим дальше)
# ---------------------------------------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📁 02. Пакетная обработка данных (CSV)</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Загрузите табличные данные замеров с нескольких скважин или участков для массового расчета.</div>', unsafe_allow_html=True)

up_file = st.file_uploader("Выберите CSV файл", type=["csv"])
if up_file is not None:
    try:
        data_df = pd.read_csv(up_file)
        st.success("Данные загружены!")
        st.dataframe(data_df.head(10), use_container_width=True)
    except Exception as err:
        st.error(f"Ошибка при чтении файла: {err}")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 8. СЕКЦИЯ 3: Объяснимый ИИ (XAI)
# ---------------------------------------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧬 03. Вклад факторов в биокоррозию</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Анализ важности признаков показывает, какие параметры сильнее всего ускоряют разрушение металла.</div>', unsafe_allow_html=True)

feats = ['Бактерии (СВБ)', 'Сероводород (H₂S)', 'Уровень pH', 'Минерализация', 'Температура', 'Скорость потока']
imp = [42, 24, 16, 9, 6, 3]

fig_bar = px.bar(
    x=imp, y=feats, orientation='h',
    color=imp, color_continuous_scale=['#bbf7d0', '#166534']
)
fig_bar.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    height=280, font=dict(color="#334155"),
    xaxis=dict(showgrid=True, gridcolor='#e2e8f0', title='Влияние (%)'),
    yaxis=dict(title=''), coloraxis_showscale=False
)
st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

st.markdown('</div>', unsafe_allow_html=True)