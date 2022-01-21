import os

DEBUG = True
AQI_DATA_API = 'http://opendata2.epa.gov.tw/AQI.json'
SITE_NAME = '基隆'   # default value
PRO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA_PATH = os.path.join(PRO_PATH, 'test_aqi.data.json')

# iqari APIS
# https://api-docs.iqair.com/?version=latest
GET_COUNTRIES = 'http://api.airvisual.com/v2/countries'
GET_STATES = 'http://api.airvisual.com/v2/states'
GET_CITIRS_BY_STATE = 'http://api.airvisual.com/v2/cities'
GET_AQI_DATA = 'http://api.airvisual.com/v2/city'
