import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Беттің параметрлері
st.set_page_config(page_title="Higher Education Insights KZ", layout="wide")

# Modern Academic Стиль
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1e3a8a; font-family: 'Georgia', serif; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Қазақстанның жоғары білім беру жүйесі: Аналитика")
st.write("2025-2026 оқу жылына арналған стратегиялық деректер негізінде")

# --- 1-БӨЛІМ: ГРАНТТАР TREEMAP ---
st.header("1. Мамандықтар бойынша гранттар бөлінісі (2025)")

grant_data = {
    'Бағыт': ['Инженерлік, өңдеу, құрылыс', 'Педагогикалық ғылымдар', 'АКТ', 'Жаратылыстану/Математика', 'Ауыл шаруашылығы', 'Денсаулық сақтау', 'Гуманитарлық ғылымдар'],
    'Грант_саны': [18946, 13226, 11585, 9188, 5000, 2500, 1500],
    'Топ': ['Техникалық', 'Білім беру', 'Техникалық', 'Ғылым', 'Ауыл шаруашылығы', 'Медицина', 'Гуманитарлық']
}
df_grants = pd.DataFrame(grant_data)

fig_tree = px.treemap(df_grants, path=['Топ', 'Бағыт'], values='Грант_саны',
                      color='Грант_саны', color_continuous_scale='Blues',
                      title="Мемлекеттік гранттардың мамандықтар бойынша иерархиясы")
st.plotly_chart(fig_tree, use_container_width=True)

# --- 2-БӨЛІМ: 'СЕРПІН' БАҒДАРЛАМАСЫ ---
st.header("2. 'Серпін' бағдарламасының өңірлік тиімділігі")

serpin_data = {
    'Өңір': ['Түркістан', 'Қызылорда', 'Жамбыл', 'Алматы облысы', 'Маңғыстау'],
    'Гранттар_саны': [983, 750, 680, 620, 620], # Статистикалық жуықтау
    'Тиімділік_индексі': [85, 82, 78, 75, 80]
}
df_serpin = pd.DataFrame(serpin_data)

fig_bar = px.bar(df_serpin, x='Өңір', y='Гранттар_саны', 
                 color='Тиімділік_индексі', 
                 labels={'Гранттар_саны': 'Бөлінген гранттар', 'Өңір': 'Талапкерлер шыққан өңір'},
                 title="'Серпін' гранттарының өңірлер бойынша игерілуі",
                 color_continuous_scale='Viridis')
st.plotly_chart(fig_bar, use_container_width=True)

# --- 3-БӨЛІМ: ЖҰМЫС ПЕН ЖАЛАҚЫ BUBBLE CHART ---
st.header("3. Түлектердің еңбек нарығындағы көрсеткіштері")

market_data = {
    'Мамандық': ['IT мамандары', 'Инженерлер', 'Дәрігерлер', 'Мұғалімдер', 'Заңгерлер', 'Ауыл шаруашылығы'],
    'Жұмысқа_орналасу_пайызы': [89, 82, 95, 88, 65, 72],
    'Орташа_жалақы_тг': [423000, 380000, 320000, 280000, 250000, 210000],
    'Түлектер_саны': [12000, 15000, 5000, 18000, 10000, 6000]
}
df_market = pd.DataFrame(market_data)

fig_bubble = px.scatter(df_market, x='Жұмысқа_орналасу_пайызы', y='Орташа_жалақы_тг',
                        size='Түлектер_саны', color='Мамандық',
                        hover_name='Мамандық', size_max=60,
                        title="Жұмысқа орналасу деңгейі мен табыс байланысы (2024-2025)")
st.plotly_chart(fig_bubble, use_container_width=True)

# --- 4-БӨЛІМ: GRANT PREDICTOR (PANDAS FILTERING) ---
st.header("4. 'Predictor' — Грантқа түсу мүмкіндігі")

col1, col2 = st.columns(2)
with col1:
    user_score = st.number_input("ҰБТ балын енгізіңіз (50-140):", min_value=50, max_value=140, value=100)
with col2:
    category = st.selectbox("Бағытты таңдаңыз:", df_grants['Бағыт'].unique())

# Pandas фильтрі арқылы болжам жасау
thresholds = {
    'АКТ': 110, 'Инженерлік, өңдеу, құрылыс': 85, 'Педагогикалық ғылымдар': 75,
    'Жаратылыстану/Математика': 90, 'Ауыл шаруашылығы': 60, 'Денсаулық сақтау': 120,
    'Гуманитарлық ғылымдар': 115
}

target_threshold = thresholds.get(category, 50)
filtered_res = df_grants[df_grants['Бағыт'] == category]

st.subheader("Нәтиже:")
if user_score >= target_threshold:
    st.success(f"Жоғары мүмкіндік! {category} бағыты бойынша шекті балл шамамен: {target_threshold}")
    st.info(f"Бұл бағытқа биыл {filtered_res['Грант_саны'].values[0]} грант бөлінген.")
else:
    st.warning(f"Мүмкіндік төмен. {category} үшін ұсынылатын балл: {target_threshold}")
    st.write("Кеңес: Бейіндік бағыты ұқсас грант саны көп басқа мамандықтарды қарастырыңыз.")
