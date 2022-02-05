import json
from typing import Any

from ..lib import net
from . import fake_data


class AQIapi:
    def __init__(self, debug=True) -> None:
        self.debug = debug
        self.key = self._load_api_key()

    def _load_api_key(self) -> str:
        return ''

    def ensure_success(self, data: Any) -> net.ReturnData:
        return_data = net.ReturnData()
        if data['status'] == 'fail':
            return_data.error = True
            return_data.reson = data['data']['message']
            return return_data
        return_data.data = data
        return return_data

    def request_country(self) -> net.ReturnData:
        return_data = net.ReturnData()
        if self.debug:
            return_data.data = json.loads(fake_data.request_country)
            return return_data
        else:
            return_data.error = True
            return_data.reson = 'Data empty error'
        return return_data

    def request_state(self, country: str) -> net.ReturnData:
        return_data = net.ReturnData()
        if self.debug:
            return_data.data = json.loads(fake_data.request_state)
            return return_data
        else:
            return_data.error = True
            return_data.reson = 'Data empty error'
        return return_data

    def request_city(self, country: str, state: str) -> net.ReturnData:
        return_data = net.ReturnData()
        if self.debug:
            return_data.data = json.loads(fake_data.request_city)
            return return_data
        else:
            return_data.error = True
            return_data.reson = 'Data empty error'
        return return_data

    def request_city_data(self,
                          country: str,
                          state: str,
                          city: str) -> net.ReturnData:
        ...
