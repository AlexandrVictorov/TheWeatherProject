import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="История", page_icon="🏠")
data = pd.DataFrame()

def scolz_mean_plot(data):
    scolz_mean = data['temperature'].rolling(window=30).mean()
    plt.hist(scolz_mean)
    plt.xlabel('Температура в градусах Цельсия')
    plt.ylabel('Количество дней')
    plt.title('Гистограмма скользящей средней температуры')
    st.pyplot(plt.gcf())

def mean_town_season_plot(data, town_to_see):
    seasons = data['season'].unique()
    st.subheader('Средняя температура по городам 🌡')
    all_cities_anomalies = {}
    for town in town_to_see:
        mean_temperatures = []
        std_temperatures = []
        season_labels = []
        anomalies = {
            'lower_levels': {},
            'upper_levels': {}
        }
        for season in seasons:
            temp_data = data.loc[(data['city'] == town) & (data['season'] == season), 'temperature']
            mean_temp = temp_data.mean()
            std_temp = temp_data.std()
            lower_level = mean_temp - 2 * std_temp
            upper_level = mean_temp + 2 * std_temp
            mean_temperatures.append(mean_temp)
            std_temperatures.append(std_temp)
            season_labels.append(season)
            anomalies['lower_levels'][season] = lower_level
            anomalies['upper_levels'][season] = upper_level
        all_cities_anomalies[town] = anomalies
        st.subheader(town)
        results_df = pd.DataFrame({
            'Сезон': season_labels,
            'Средняя температура': mean_temperatures,
            'Стандартное отклонение': std_temperatures
        })
        results_df['Средняя температура'] = results_df['Средняя температура'].round(2)
        results_df['Стандартное отклонение'] = results_df['Стандартное отклонение'].round(2)
        st.table(results_df)
    return all_cities_anomalies

def anomalies_show(data, anomalies, town_to_see):
    for town in town_to_see:
        st.subheader(f"Аномалии по сезонам в {town}")
        if town not in anomalies:
            st.warning(f"Нет данных об аномалиях для {town}")
            continue
        for season in data['season'].unique():
            if season not in anomalies[town]['lower_levels']:
                continue
            st.subheader(season)
            temp_data = data.loc[(data['city'] == town) & (data['season'] == season), 'temperature']
            lower_bound = anomalies[town]['lower_levels'][season]
            upper_bound = anomalies[town]['upper_levels'][season]
            anomalies_array = temp_data.loc[(temp_data > upper_bound) | (temp_data < lower_bound)]
            if len(anomalies_array) > 0:
                    dates = data.loc[anomalies_array.index, 'timestamp']
                    result_df = pd.DataFrame({
                        'Дата': dates.values,
                        'Температура': anomalies_array.values
                    })
                    st.table(result_df)
            else:
                st.info("Аномалий не найдено")


try:
    if 'user_data' in st.session_state and st.session_state['user_data'].shape != (0, 0):
       with st.spinner('Обрабатываю данные...'):
          data = st.session_state['user_data']
          settings = st.session_state.get('settings', {})
          st.success(f"✅ Данные загружены! Размер: {data.shape}")
          scolz_mean_plot(data) #вызываю метод построения графика скользящего среднего
          town_to_see = st.multiselect('Выберите города, по которым показать статистику:', list(data['city'].unique()), default=list(data['city'].unique())[0])
          anomalies = mean_town_season_plot(data, town_to_see)
          if st.checkbox("Показать аномалии по сезонам"):
             anomalies_show(data, anomalies, town_to_see)
    else:
        st.warning("⚠️ Данные не найдены!")
        st.info("Пожалуйста, сначала введите данные на главной странице в боковой панели.")
        st.page_link("./main.py", label="Перейти к вводу данных", icon="📝")

except KeyError as e:
    st.warning("⚠️ Данные не найдены!")
    st.info("Пожалуйста, сначала введите данные на главной странице в боковой панели.")
    st.page_link("./main.py", label="Перейти к вводу данных", icon="📝")














