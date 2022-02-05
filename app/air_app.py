import datetime
from typing import NamedTuple

import rumps

from . import window, settings


class Menus(NamedTuple):
    update_time: str = 'Update Time'
    set_key: str = 'Set Key'
    change_area: str = 'Change Area'
    separator: object = rumps.separator


MENUS = Menus()


class App(rumps.App):
    def __init__(self) -> None:
        super().__init__('AQI:32')
        self._init_menu()
        rumps.debug_mode(settings.DEBUG)

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
        print(result)

    @rumps.clicked(MENUS.set_key)
    def set_key_window(self, _) -> None:
        w = window.SetKeyWindow()
        result = w.run()
        print(result)

    def run(self) -> None:
        super().run()
