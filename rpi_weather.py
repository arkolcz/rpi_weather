import json
import urllib.request
import urllib.error
import requests

# IP and location of hardware that script is running on in JSON format
IP_INFO_URL = 'http://ipinfo.io/json'

# OpenWeather API Key
API_KEY = 'Unkown' 

# Needed to access OpenWeather data and visualize on screen
USER_COUNTRY = 'Unkown'
USER_CITY = 'Uknown'
USER_IP = 'Uknown'

def update_IP_info():
    # Get IP information as JSON format
    global USER_COUNTRY, USER_CITY, USER_IP
    try:
        with urllib.request.urlopen(IP_INFO_URL) as response:
            data = json.load(response)
            USER_COUNTRY = data['country']
            USER_CITY = data['city']
            USER_IP = data['ip']
    except urllib.error.HTTPError:
        print(f'Cant access site: {IP_INFO_URL}')
        USER_COUNTRY = 'Unkown'
        USER_CITY = 'Uknown'
        USER_IP = 'Uknown'

def update_api_key():
    # Get OpenWeather API key from api_key.txt 
    global API_KEY
    try: 
        with open('api_key.txt', 'r') as f:
           API_KEY = f.read()
    except FileNotFoundError:
        print('File api_key.txt not found')
        exit() # If api_key.txt is not present, terminate program
    except:
        print('Cant read from api-key.txt')
        exit() # If we can't access api-key.txt, terminate program

def get_weather_data():
    # Fetch weather data from OpenWeather
    # requests lib used to avoid problem with unicode encoding in response
        url = f'https://api.openweathermap.org/data/2.5/weather?q={USER_CITY}&units=metric&appid={API_KEY}'
        r = requests.get(url)
        return r.json()

if  __name__ == "__main__":
    update_IP_info()
    update_api_key()
    weather = get_weather_data()
    print(weather)
