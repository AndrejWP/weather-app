from flask import Flask, render_template, request
import requests
import time

app = Flask(__name__)


API_KEY = 'bd5e378503939ddaee76f12ad7a97608'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather' #запрос на сервер
#настройка кэширования
CACHE_TIMEOUT = 300 #5 минут
weather_cache = {}   # Пустое хранилище
def get_weather_from_api(city):
    #запрос к OpenWeatherMap
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
    except Exception:
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
                    weather = {
                        'city': data['name'],
                        'temp': round(data['main']['temp']),
                        'desc': data['weather'][0]['description'],
                        'icon': data['weather'][0]['icon'],
                        'humidity': data['main']['humidity'],
                        'wind': data['wind']['speed']

                    }
                    weather_cache[city_key] = {'data': weather, 'time': current_time} #сохраняем в  кэш
                else:
                    error = "Город не найден или ошибка сервиса"






    return render_template('index.html', weather = weather, error = error)

if __name__ == '__main__':
    app.run(debug=True)