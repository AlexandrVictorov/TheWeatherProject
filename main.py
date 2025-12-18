import streamlit as st
import pandas as pd

st.set_page_config(page_title="Главная", page_icon="🏠")

data = pd.DataFrame()
st.title("Заполните данные и получите аналитику по погоде 🌊")

uploaded_file = st.file_uploader("Загрузите CSV файл", type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.success(f"Файл загружен! Размер: {data.shape}")
    if st.button("Сохранить датасет"):
        st.session_state['user_data'] = data
        st.text("👈 Ваши данные сохранены...")
        st.page_link("pages/history.py", label="Смотреть исторические данные", icon="📊")
        st.page_link("pages/actual.py", label="Смотреть актуальную погоду", icon="📊")
else:
    st.error("Загрузите файл...")

town = st.selectbox('Выберите свой город:', ["New York", "London", "Paris", "Tokyo", "Moscow", "Sydney","Berlin", "Beijing",  "Rio de Janeiro", "Dubai", "Los Angeles", "Singapore", "Mumbai", "Cairo", "Mexico City"])

API = st.text_input("Введите API OpenWeatherMap")

if st.button("Сохранить API и город"):
    if API:
       st.session_state['settings'] = {
        'Town': town,
        'API': API
       }
       st.page_link("pages/actual.py", label="Смотреть погоду", icon="📊")
    else:
        st.warning('Введите API ключ и выберите город')
