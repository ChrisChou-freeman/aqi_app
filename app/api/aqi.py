import json
from typing import Any

from ..lib import net
from .. import settings
from . import fake_data
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

    def request_countries(self) -> net.ReturnData:
        return_data = net.ReturnData()
        if self.key == '':
            return_data.error = True
            return_data.reson = 'request key is empty'
            return return_data
        if self.debug:
            return_data.data = json.loads(fake_data.request_country)
            return return_data
        contries_cache = self.database.get_data('contries')
        if contries_cache is not None:
            return_data.data = contries_cache
            return return_data
        request_data = net.request(settings.GET_COUNTRIES, {'key': self.key})
        return request_data

    def request_states(self, country: str) -> net.ReturnData:
        return_data = net.ReturnData()
        if self.debug:
            return_data.data = json.loads(fake_data.request_state)
            return return_data
        return_data.error = True
        return_data.reson = 'Data empty error'
        return return_data

    def request_cities(self, country: str, state: str) -> net.ReturnData:
        return_data = net.ReturnData()
        if self.debug:
            return_data.data = json.loads(fake_data.request_city)
            return return_data
        return_data.error = True
        return_data.reson = 'Data empty error'
        return return_data

    def request_city_data(self,
                          country: str,
                          state: str,
                          city: str) -> net.ReturnData:
        return_data = net.ReturnData()
        if self.debug:
            return_data.data = json.loads(fake_data.request_city_data)
            return return_data
        return return_data
