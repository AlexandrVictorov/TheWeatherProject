import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Графики",
    page_icon="📊",
)


def get_season_from_date(date_obj): #определяю текущую дату
    month = date_obj.month
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    elif month in [9, 10, 11]:
        return 'autumn'
    else:
        return 'unknown'


def get_current_weather(api_key, city_name, units='metric'):
    """
    Получает текущую погоду для указанного города

    Parameters:
    - api_key: ваш API ключ OpenWeatherMap
    - city_name: название города (например, "Moscow" или "Moscow,RU")
    - units: единицы измерения ('metric' - °C, 'imperial' - °F)

    Returns:
    - dict с данными о погоде или None в случае ошибки
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': units,
        'lang': 'ru'
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Проверяем на ошибки HTTP

        data = response.json()

        # Если город не найден
        if data.get('cod') != 200:
            st.error(f"Ошибка: {data.get('message', 'Неизвестная ошибка')}")
            return None
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при запросе к API: {e}")
        return None
    except ValueError as e:
        st.error(f"Ошибка при обработке ответа: {e}")
        return None


def anomalies(data, town):
    seasons = data['season'].unique()
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
            anomalies['lower_levels'][season] = lower_level
            anomalies['upper_levels'][season] = upper_level
    return anomalies


try:
   settings = st.session_state.get('settings', {})
   data = get_current_weather(settings['API'], settings['Town'], units='metric')
   dataset = st.session_state.get('user_data')
   st.success(f"Температура в {settings['Town']}: {data['main']['temp']} °C, ощущается, как: {data['main']['feels_like']} °C")
   try:
       if 'user_data' in st.session_state and st.session_state['user_data'].shape != (0, 0):
          town_anomalie = anomalies(dataset, settings['Town'])
          date_obj = datetime.fromtimestamp(data['dt'])
          season = get_season_from_date(date_obj)
          if data['main']['temp'] > town_anomalie['upper_levels'][season]:
             st.success(f"Погода сегодня аномально высокая для {season} в {settings['Town']}")
          elif data['main']['temp'] < town_anomalie['lower_levels'][season]:
             st.success(f"Погода сегодня аномально низкая для {season} в {settings['Town']}")
          else:
             st.success(f"Сегодня нормальная погода для {season} в {settings['Town']}")
       else:
           st.warning('Чтоб увидеть сравнение с историческими данными загрузите таблицу и нажмите "Сохранить датасет"')
           st.page_link("./main.py", label="Загрузить датасет", icon="📝")

   except KeyError:
       st.warning('Чтоб увидеть сравнение с историческими данными загрузите таблицу и нажмите "Сохранить датасет"')
       st.page_link("./main.py", label="Перейти к вводу данных", icon="📝")
except KeyError:
   st.warning('Заполните API ключ и Ваш город')
   st.page_link("./main.py", label="Перейти к вводу данных", icon="📝")