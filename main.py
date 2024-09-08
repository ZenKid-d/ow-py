import requests
import sys
import yaml

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
TRANSLATE_URL = "https://translate.api.cloud.yandex.net/translate/v2/translate"

def read_config_ow():
    with open("config.yml") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    return cfg["api_key_ow"]

def make_request(city):
    app_id = read_config_ow()
    city_translate = make_translate(city)
    params = "q=" + city_translate + "&appid=" + app_id + "&units=metric"
    r = requests.get(BASE_URL + params)
    print("Сейчас в городе", city, "температура", str(r.json()["main"]["temp"]), "градусов")
    

def read_config_yc():
    with open("config.yml") as x:
        cfg = yaml.load(x, Loader=yaml.FullLoader)
    return cfg["api_key_yc"] , cfg["folder_id_yc"]

def make_translate(city):
    api_key_yc, folder_id_yc = read_config_yc()
    headers = {'Content-Type': 'application/json', "Authorization": "Api-Key "+api_key_yc}
    params = {"folderId": folder_id_yc, "texts": [city], "targetLanguageCode": "en"}
    r = requests.post(TRANSLATE_URL, headers=headers, json=params)
    return r.json()['translations'][0]['text']


def main():
    city = sys.argv[1]
    make_request(city)
    
if __name__ == '__main__':
    main()