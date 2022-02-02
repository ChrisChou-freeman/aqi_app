import os

PRO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False
AQI_DATA_API = 'http://opendata2.epa.gov.tw/AQI.json'
TITLE_NAME = '基隆'   # default value
TEST_DATA_PATH = os.path.join(PRO_PATH, 'test_aqi.data.json')
THEME_PACK_PATH = os.path.join(PRO_PATH, 'data/theme')

# iqari APIS
# https://api-docs.iqair.com/?version=latest
GET_COUNTRIES = 'http://api.airvisual.com/v2/countries'
GET_STATES = 'http://api.airvisual.com/v2/states'
GET_CITIRS_BY_STATE = 'http://api.airvisual.com/v2/cities'
GET_AQI_DATA = 'http://api.airvisual.com/v2/city'

RGB_DARK = (0, 0, 0)
RGB_WHITE = (255, 255, 255)
