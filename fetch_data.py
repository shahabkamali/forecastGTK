
import requests


def fetch_data(url):

    try:
        response = requests.get(url)
        ret = response.json()
        response.raise_for_status()
        
        return ret
    except (ValueError, requests.exceptions.RequestException) as e:
        print({'error': e, 'url': url})


def fetch_forecast(city_id='2643743'):
    url = "http://api.openweathermap.org/data/2.5/forecast?id=%s&APPID=34892dee8e50ad1f088d6d9a6271c58b" % city_id
    ret = fetch_data(url)
    if 'cod' in ret and ret['cod'] == '200':
        return ret['list']

    return None


def get_24h_forecast_temps(city_id='2643743'):
    forecasts = fetch_forecast(city_id)

    if forecasts is None:
        return None
    # api gives us every 3 hour until 5 days
    forecasts = forecasts[:9]
    ret = {}
    for k, forecast in enumerate(forecasts):
        temp_in_cel = forecast['main']['temp'] - 273.15
        ret[k] = {'temp': "%.2f" % temp_in_cel, 'str_time': forecast['dt_txt']}
    return ret
