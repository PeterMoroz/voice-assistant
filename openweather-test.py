import requests
import os

app_id = os.getenv('APP_ID')

while True:
    print('city ?')
    city = input()   
    url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + app_id + '&q=' + city
    response = requests.get(url)
    r = response.json()
    
    print('response:\n')
    print(str(r) + '\n')
    
    T0 = 273.15
    if r['cod'] != '404':
        m = r['main']
        t = m['temp']
        p = m['pressure']    
        h = m['humidity']
        w = r['weather']
        d = w[0]['description']
        t = t - T0
        print("Temperature: " + '{0:.2f}'.format(t) + " celsius degrees\nPressure: " + str(p) + " hPa\nHumidity: " + str(h) + "%\nDescription: " + str(d))
    else:
        print("The city not found!")