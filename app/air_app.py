import datetime
from typing import Any, NamedTuple

import rumps

from . import window, settings


class Menus(NamedTuple):
    update_time: str = 'Update Time'
    current_location: str = 'My Location: empty'
    set_key: str = 'Set Key'
    change_area: str = 'Change Area'
    separator: object = rumps.separator


MENUS = Menus()


class App(rumps.App):
    def __init__(self) -> None:
        super().__init__('AQI:32')
        rumps.debug_mode(settings.DEBUG)
        self._init_menu()

    def _init_menu(self) -> None:
        for menu in MENUS:
            if type(menu) == str:
                self.menu.add(rumps.MenuItem(menu))
            else:
                self.menu.add(menu)
        self.menu[MENUS.update_time].title = self._get_refresh_time()

    def _get_refresh_time(self) -> str:
        return f'Update:{datetime.datetime.now().strftime("%m-%d %H:%M:%S")}'

    @rumps.clicked(MENUS.change_area)
    def change_area_window(self, _) -> None:
        w = window.SelectAreaWindow()
        result = w.run()
        if not result.success:
            self.alert_window(result.reson)
        else:
            print(result)

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
        print('update....')

    def run(self) -> None:
        super().run()
