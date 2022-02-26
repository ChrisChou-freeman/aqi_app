import os
import datetime
from typing import Any, NamedTuple, TypedDict

import rumps

from . import window, settings, data_base
from .api import AQIapi


class AqiLevel(TypedDict):
    min: int
    max: int
    sign: str


AQI_LEVELS = [
    AqiLevel(min=0, max=50, sign='🔵'),
    AqiLevel(min=51, max=100, sign='🟢'),
    AqiLevel(min=101, max=150, sign='🟡'),
    AqiLevel(min=151, max=200, sign='🟠'),
    AqiLevel(min=201, max=300, sign='🔴'),
    AqiLevel(min=301, max=1000, sign='🟣'),
]


class Menus(NamedTuple):
    update_time: str = 'Update Time'
    current_location: str = 'Location:empty'
    seprator1: object = rumps.separator
    update: str = 'Update'
    set_key: str = 'Set Key'
    change_area: str = 'Change Area'
    separator2: object = rumps.separator


_Menus = Menus()


class App(rumps.App):
    def __init__(self) -> None:
        super().__init__('AQI:--')
        rumps.debug_mode(settings.DEBUG)
        self.data_base = self.get_db()
        self._init_menu()

    def _init_menu(self) -> None:
        for menu in _Menus:
            if type(menu) == str:
                self.menu.add(rumps.MenuItem(menu))
            else:
                self.menu.add(menu)

    def _set_update_time(self) -> None:
        self.menu[_Menus.update_time].title = self._get_refresh_time()

    def _get_refresh_time(self) -> str:
        return f'Update:{datetime.datetime.now().strftime("%m-%d %H:%M:%S")}'

    def get_db(self) -> data_base.DataBase:
        with data_base.DataBase(settings.DATA_PATH) as db:
            return db

    def _set_location(self) -> None:
        self.menu[_Menus.current_location].title = self._get_cached_location()

    def _get_aqi_level_sign(self, aqi_number: int) -> str:
        try:
            aqi_number = int(aqi_number)
        except ValueError:
            aqi_number = 0
        for aqi_level in AQI_LEVELS:
            if aqi_number >= aqi_level['min'] \
                    and aqi_number <= aqi_level['max']:
                return str(aqi_level['sign'])
        return '?'

    def set_aqi_data(self, location: str) -> None:
        '''
            set air quality index by location
        '''
        country, state, city = location.split('_')
        api = AQIapi(False)
        china_aqi_key = 'aqicn'
        usa_aqi_key = 'aqius'
        aqi_key = china_aqi_key if country == 'China' else usa_aqi_key
        result_data = api.request_city_data(
            country=country,
            state=state,
            city=city
        )
        if result_data.error:
            self.alert_window(result_data.reson)
        else:
            data = result_data.data.get('data', None)
            if data is None:
                return
            current_weather = data.get('current', None)
            if current_weather is None:
                return
            pollution_data = current_weather.get('pollution', None)
            if pollution_data is None:
                return
            Aqi_number: int = pollution_data[aqi_key]
            Aqi_level_sign = self._get_aqi_level_sign(Aqi_number)
            self.title = f'AQI:{Aqi_number}{Aqi_level_sign}'
            weather = current_weather.get('weather', None)
            if weather is None:
                return
            condition_icon = weather.get('ic', None)
            if condition_icon is None:
                return
            condition_icon_path = os.path.join(
                settings.IMAGES_PATH, f'{condition_icon}.png'
            )
            self.icon = condition_icon_path

    def _get_cached_location(self) -> str:
        with self.data_base as db:
            my_location = db.get_data('my_location')
        if my_location is None:
            my_location = 'empty'
        else:
            self.set_aqi_data(my_location)
            my_location = my_location.replace('_', '/')
        return f'Location:{my_location}'

    @rumps.clicked(_Menus.update)
    def update_click(self, _) -> None:
        self.refresh_data()

    @rumps.clicked(_Menus.set_key)
    def set_key_window(self, _) -> None:
        w = window.SetKeyWindow()
        w.run()

    @rumps.clicked(_Menus.change_area)
    def change_area_window(self, _) -> None:
        w = window.SelectAreaWindow()
        result = w.run()
        if not result.success:
            self.alert_window(result.reson)
        else:
            self._set_location()

    @rumps.notifications
    def notification_center(info: Any) -> None:
        ...

    def alert_window(self, message: str) -> None:
        rumps.alert('Message', message, icon_path=settings.APP_ICON)

    def refresh_data(self) -> None:
        self._set_update_time()
        self._set_location()

    @rumps.timer(60*30)
    def update(self, _) -> None:
        self.refresh_data()

    def run(self) -> None:
        super().run()
