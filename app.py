from flask import Flask, render_template
import requests
import time

app = Flask(__name__)


API_KEY = 'ec589e598b051f59d5a0b8a098a07b61'
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
    except Exception as e:
        print(f"Error: {e}")
    return None
#открытие страницы
@app.route('/', methods= ['GET', 'POST'])
def index():
    weather = None
    if requests.method == 'POST':
        city_raw = requests.form.get('city') #Получаем текст из инпута
        if city_raw:
            city_key = city_raw.strip().lower() #берем нижний регистр ключа
            data = get_weather_from_api(city_key) #вызываем api
            if data:
                weather = {
                    'city': data['name'],
                    'temp': round(data['main']['temp']),
                    'desc': data['weather'][0]['description']
                }

                #сохраняем в память
                current_time = time.time()
                weather_cache[city_key] = {
                    'data': weather,
                    'time': current_time
                }
                print(f"LOG: Saved {city_key} to cache")




    return render_template('index.html', weather = weather)

if __name__ == '__main__':
    app.run(debug=True)