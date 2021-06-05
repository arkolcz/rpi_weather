import sys
from urllib.error import HTTPError
import urllib.request
import json
import requests

# Globals
IP_INFO_URL = 'http://ipinfo.io/json'

# Keys for dict containing ip based data
COUNTRY = 'country'
CITY = 'city'
HOST_IP = 'ip'

# OpenWeather API url
OW_API_URL = 'https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}'


def get_weather_data(ip_data: dict, api_key: str) -> dict:
    """ Gets weather data from OpenWeather API
    Args:
        ip_data (dict): Dict contining location data based on IP
        api_key (str): OpenWeather API key

    """
    city = ip_data[CITY]
    url = OW_API_URL.format(city, api_key)
    r = requests.get(url)
    return r.json()


def get_ip_info() -> dict:
    """ Gets location information based on host ip

    Returns:
        ip_info (dict): Location data gathered based on IP address
    """
    try:
        with urllib.request.urlopen(IP_INFO_URL) as response:
            ip_info = json.load(response)
    except HTTPError as err:
        print(f'Can\'t access ip data from {IP_INFO_URL}. \
              (Error={err.strerror})')

    return ip_info


def get_api_key(f_path: str) -> str:
    """ Gets OpenWeather API key from file
    Args:
        f_path (str): Path to file containg API key
    Returns:
        api_key (str): Open Weather API key
    """
    try:
        with open(f_path, 'r') as f:
            api_key = f.read().rstrip()
    except FileNotFoundError as err:
        print(f'Invalid path to file: {f_path}. (Error={err.strerror})')
        sys.exit(1)
    except Exception as err:
        print(f'Could not retrieve API key. (Error={err.strerror})')
        sys.exit(1)

    return api_key


def main(f_path) -> None:
    """ Main function of the program
    Args:
        f_path (str): Path to file containg API key
    """
    api_key = get_api_key(f_path)
    ip_info = get_ip_info()
    weather = get_weather_data(ip_info, api_key)
    print(weather)


def usage() -> None:
    """ Prints scripts usage message
    """
    message = """
Usage: rpi_weather path-to-file
path-to-file: Path to file that contains your API key
--help: This help message
"""
    print(message)


if __name__ == '__main__':
    if '--help' in sys.argv:
        usage()
        sys.exit(0)

    if len(sys.argv) < 2:
        print('Error: Path to file containing OpenWeather\
               API Key must be provided')
        usage()
        sys.exit(1)

    main(sys.argv[1])