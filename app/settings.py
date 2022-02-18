import os

PRO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True
# AQI_DATA_API = 'http://opendata2.epa.gov.tw/AQI.json'
TEST_DATA_PATH = os.path.join(PRO_PATH, 'test_aqi.data.json')
THEME_PACK_PATH = os.path.join(PRO_PATH, 'data/theme')
DATA_PATH = os.path.join(PRO_PATH, 'data/cache_data/data.pickel')
CONDITION_ICON_PATH = os.path.join(PRO_PATH, 'data/images')

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
