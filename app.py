from flask import Flask, render_template
import requests
import time

app = Flask(__name__)


API_KEY = 'ec589e598b051f59d5a0b8a098a07b61'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather' #запрос на сервер
CACHE_TIMEOUT = 300 #5 минут

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)