import os
from typing import TypedDict

PRO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False
# AQI_DATA_API = 'http://opendata2.epa.gov.tw/AQI.json'
TEST_DATA_PATH = os.path.join(PRO_PATH, 'test_aqi.data.json')
THEME_PACK_PATH = os.path.join(PRO_PATH, 'data/theme')
DATA_PATH = os.path.join(PRO_PATH, 'data/cache_data/data.pickel')
IMAGES_PATH = os.path.join(PRO_PATH, 'data/images')
APP_ICON = os.path.join(IMAGES_PATH, 'AQI.icns')
APP_BMP = os.path.join(IMAGES_PATH, 'AQI.bmp')

# iqari APIS
# https://api-docs.iqair.com/?version=latest
GET_COUNTRIES = 'http://api.airvisual.com/v2/countries'
GET_STATES = 'http://api.airvisual.com/v2/states'
GET_CITIRS_BY_STATE = 'http://api.airvisual.com/v2/cities'
GET_AQI_DATA = 'http://api.airvisual.com/v2/city'

ONE_HOUR_T0_SECONDS = 60*60
ONE_DAY_TO_SECONDS = 24*60*60
RGB_DARK = (0, 0, 0)
RGB_WHITE = (255, 255, 255)


class AqiLevel(TypedDict):
    min: int
    max: int
    point: str


AQI_LEVELS: list[AqiLevel] = [
    {
        'min': 0,
        'max': 50,
        'point': '🔵'
    },
    {
        'min': 51,
        'max': 100,
        'point': '🟢'
    },
    {
        'min': 101,
        'max': 150,
        'point': '🟡'
    },
    {
        'min': 151,
        'max': 200,
        'point': '🟠'
    },
    {
        'min': 201,
        'max': 300,
        'point': '🔴'
    },
    {
        'min': 301,
        'max': 1000,
        'point': '🟣'
    },
]
