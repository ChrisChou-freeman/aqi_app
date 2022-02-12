import datetime
from typing import Any, NamedTuple

import rumps

from . import window, settings, data_base
from .api import AQIapi


class Menus(NamedTuple):
    update_time: str = 'Update Time'
    current_location: str = 'My Location:empty'
    set_key: str = 'Set Key'
    change_area: str = 'Change Area'
    separator: object = rumps.separator


MENUS = Menus()


class App(rumps.App):
    def __init__(self) -> None:
        super().__init__('AQI:32')
        rumps.debug_mode(settings.DEBUG)
        self.data_base = self.get_db()
        self._init_menu()

    def _init_menu(self) -> None:
        for menu in MENUS:
            if type(menu) == str:
                self.menu.add(rumps.MenuItem(menu))
            else:
                self.menu.add(menu)
        self._set_update_time()
        self._set_location()

    def _set_update_time(self) -> None:
        self.menu[MENUS.update_time].title = self._get_refresh_time()

    def _get_refresh_time(self) -> str:
        return f'Update:{datetime.datetime.now().strftime("%m-%d %H:%M:%S")}'

    def get_db(self) -> data_base.DataBase:
        with data_base.DataBase(settings.DATA_PATH) as db:
            return db

    def _set_location(self) -> None:
        self.menu[MENUS.current_location].title = self._get_cached_location()

    def set_aqi_data(self, location: str) -> None:
        country, state, city = location.split('_')
        api = AQIapi(False)
        result_data = api.request_city_data(
            country=country,
            state=state,
            city=city
        )
        if result_data.error:
            self.alert_window(result_data.reson)
        else:
            data = result_data.data['data']
            print(data)

    def _get_cached_location(self) -> str:
        with self.data_base as db:
            my_location = db.get_data('my_location')
        if my_location is None:
            my_location = 'empty'
        else:
            self.set_aqi_data(my_location)
            my_location = my_location.replace('_', '/')
        print(my_location)
        return f'My Location:{my_location}'

    @rumps.clicked(MENUS.change_area)
    def change_area_window(self, _) -> None:
        w = window.SelectAreaWindow()
        result = w.run()
        if not result.success:
            self.alert_window(result.reson)
        else:
            self._set_location()

    @rumps.notifications
    def notification_center(info: Any) -> None:
        print(info)

    def alert_window(self, message: str) -> None:
        rumps.alert('Message', message)

    @rumps.clicked(MENUS.set_key)
    def set_key_window(self, _) -> None:
        w = window.SetKeyWindow()
        result = w.run()
        print(result)

    @rumps.timer(60*60*10)
    def update(self, _) -> None:
        self._set_location()

    def run(self) -> None:
        super().run()
