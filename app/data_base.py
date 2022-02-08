from typing import Optional
import pickle
import time
import os


class DataBase:
    def __init__(self, data_path: str) -> None:
        self.data_path = data_path
        self.data_obj: dict[str, dict[str, str]] = {}

    def set_data(self, key: str, value: str) -> None:
        self.data_obj[key] = {
            'update_time': str(time.time()),
            'data': value
        }

    def get_data(self, key: str) -> Optional[str]:
        data = self.data_obj.get(key, None)
        if data is None:
            return data
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
