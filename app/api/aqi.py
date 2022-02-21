import json
from typing import Any

from . import fake_data
from ..lib import net
from .. import settings
from .. import data_base


class AQIapi:
    def __init__(self, debug=True) -> None:
        self.debug = debug
        self.database = self.get_db()
        self.key = self._load_api_key(self.database)

    def _load_api_key(self, db: data_base.DataBase) -> str:
        key = db.get_data('key')
        if key is None:
            return ''
        return key

    def get_db(self) -> data_base.DataBase:
        with data_base.DataBase(settings.DATA_PATH) as db:
            return db

    def ensure_success(self, data: Any) -> net.ReturnData:
        return_data = net.ReturnData()
        if data['status'] == 'fail':
            return_data.error = True
            return_data.reson = data['data']['message']
            return return_data
        return_data.data = data
        return return_data

    def handle_response(self,
                        cache_name: str,
                        rsp_data: net.ReturnData,
                        outdate_time: int) -> net.ReturnData:
        return_data = net.ReturnData()
        if rsp_data.error:
            return rsp_data
        if rsp_data.data['status'] != 'success':
            return_data.error = True
            return_data.reson = return_data.data['data']['message']
            return return_data
        with self.database as db:
            # print('save cache')
            db.set_data(cache_name, rsp_data.data['data'], outdate_time)
        return rsp_data

    def request_countries(self) -> net.ReturnData:
        return_data = net.ReturnData()
        if self.key == '':
            return_data.error = True
            return_data.reson = 'request key is empty'
            return return_data
        if self.debug:
            return_data.data = json.loads(fake_data.request_country)
            return return_data
        cache_name = 'countries'
        contries_cache = self.database.get_data(cache_name)
        if contries_cache is not None:
            # print('cache data..')
            return_data.data = {'data': contries_cache}
            return return_data
        rsp_data = net.request(settings.GET_COUNTRIES, {'key': self.key})
        return self.handle_response(
            cache_name,
            rsp_data,
            30*settings.ONE_DAY_TO_SECONDS
        )

    def request_states(self, country: str) -> net.ReturnData:
        return_data = net.ReturnData()
        if self.key == '':
            return_data.error = True
            return_data.reson = 'request key is empty'
            return return_data
        if self.debug:
            return_data.data = json.loads(fake_data.request_state)
            return return_data
        cache_name = f'{country}_states'
        states_cache = self.database.get_data(cache_name)
        if states_cache is not None:
            return_data.data = {'data': states_cache}
            return return_data
        rsp_data = net.request(
            settings.GET_STATES,
            {'key': self.key, 'country': country}
        )
        return self.handle_response(
            cache_name,
            rsp_data,
            30*settings.ONE_DAY_TO_SECONDS
        )

    def request_cities(self, country: str, state: str) -> net.ReturnData:
        return_data = net.ReturnData()
        if self.key == '':
            return_data.error = True
            return_data.reson = 'request key is empty'
            return return_data
        if self.debug:
            return_data.data = json.loads(fake_data.request_city)
            return return_data
        cache_name = f'{country}_{state}_cities'
        cities_cache = self.database.get_data(cache_name)
        if cities_cache is not None:
            return_data.data = {'data': cities_cache}
            return return_data
        rsp_data = net.request(
            settings.GET_CITIRS_BY_STATE,
            {'key': self.key, 'country': country, 'state': state}
        )
        return self.handle_response(
            cache_name,
            rsp_data,
            30*settings.ONE_DAY_TO_SECONDS
        )

    def request_city_data(self,
                          country: str,
                          state: str,
                          city: str) -> net.ReturnData:
        return_data = net.ReturnData()
        if self.key == '':
            return_data.error = True
            return_data.reson = 'request key is empty'
            return return_data
        if self.debug:
            return_data.data = json.loads(fake_data.request_city_data)
            return return_data
        cache_name = f'{country}_{state}_{city}_datas'
        city_data_cache = self.database.get_data(cache_name)
        if city_data_cache is not None:
            return_data.data = {'data': city_data_cache}
            return return_data
        rsp_data = net.request(
            settings.GET_AQI_DATA,
            {'key': self.key, 'country': country, 'state': state, 'city': city}
        )
        return self.handle_response(
            cache_name,
            rsp_data,
            1*settings.ONE_HOUR_T0_SECONDS
        )
