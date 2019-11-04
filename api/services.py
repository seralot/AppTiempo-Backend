import requests

def getapi(ubicacion):
    r = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?appid=375b5b72defecfdfccfa090d50f49db4&q={ubicacion}&units=metric&lang=es')
    return r.text