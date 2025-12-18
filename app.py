from flask import Flask, render_template, request
import requests
import time

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

API_KEY = 'ec589e598b051f59d5a0b8a098a07b61'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather' #запрос на сервер
#настройка кэширования
CACHE_TIMEOUT = 300
weather_cache = {}


def get_weather_from_api(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        print(f"LOG: Статус ответа API: {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"LOG: Ответ сервера не 200: {response.text}")

    except Exception as e:  # <-- Важное изменение!
        print(f"!!! ОШИБКА ВНУТРИ API ФУНКЦИИ: {e}")
        pass
    return None
#открытие страницы
@app.route('/', methods= ['GET', 'POST'])
def index():
    weather = None
    error = None
    if request.method == 'POST':
        city_raw = request.form.get('city') #Получаем текст из инпута
        if city_raw:
            city_key = city_raw.strip().lower() #берем нижний регистр ключа
            print(f"LOG: Ищем город: {city_key}")
            current_time = time.time()
            #проверяем кэш
            if city_key in weather_cache and (current_time - weather_cache[city_key]['time'] < CACHE_TIMEOUT):
                print(f"LOG: Using cached data for {city_key}")
                weather = weather_cache[city_key]['data']

            else:
                # Если в кеше нет или устарело — идем в API
                print(f"LOG: Fetching new data for {city_key}")
                data = get_weather_from_api(city_key)
                if data:
                    icon_code = data['weather'][0]['icon']
                    weather = {
                        'city': data['name'],
                        'temp': round(data['main']['temp']),
                        'desc': data['weather'][0]['description'],
                        'icon': icon_code,
                        'humidity': data['main']['humidity'],
                        'wind': data['wind']['speed'],
                        'is_night': 'n' in icon_code

                    }
                    weather_cache[city_key] = {'data': weather, 'time': current_time} #сохраняем в  кэш
                else:
                    error = "Город не найден или ошибка сервиса"






    return render_template('index.html', weather = weather, error = error)

if __name__ == '__main__':
    app.run(debug=True)