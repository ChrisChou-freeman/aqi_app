from typing import Optional
import pickle
import time
from datetime import datetime
import os

ONE_HOUR_T0_SECONDS = 60*60
ONE_DAY_TO_SECONDS = 24*60*60


class DataBase:
    def __init__(self, data_path: str) -> None:
        self.data_path = data_path
        self.data_obj: dict[str, dict[str, str]] = {}

    def set_data(self, key: str, value: str, outdate_time: int) -> None:
        self.data_obj[key] = {
            'update_time': str(time.time()),
            'data': value,
            'outdate_time': str(outdate_time)
        }

    def is_outdate_data(self, key: str, data: dict[str, str]) -> bool:
        if key == 'key' or key == 'my_location':
            return False
        now_date = datetime.fromtimestamp(time.time())
        update_time = datetime.fromtimestamp(float(data['update_time']))
        past_time = now_date - update_time
        outdate_time = int(data['outdate_time'])
        if past_time.total_seconds() > outdate_time:
            return True
        return False

    def get_data(self, key: str) -> Optional[str]:
        data = self.data_obj.get(key, None)
        if data is None:
            return data
        if self.is_outdate_data(key, data):
            return None
        return data['data']

    def load_data(self) -> None:
        if not os.path.exists(self.data_path):
            return
        with open(self.data_path, 'rb') as r:
            self.data_obj = pickle.load(r)

    def dump_data(self) -> None:
        with open(self.data_path, 'wb') as w:
            pickle.dump(self.data_obj, w)

    def __enter__(self) -> 'DataBase':
        self.load_data()
        return self

    def __exit__(self, *_) -> None:
        self.dump_data()
