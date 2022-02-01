import datetime
import json
from typing import NamedTuple

import rumps

from . import lib, settings
from . import window

class Menus(NamedTuple):
    update_time: str = 'Update Time'
    hello_window: str = 'hello window'
    # setup_key: str = 'Set iQair Key'
    # change_area: str = 'Change Area'
    # separator: object = rumps.separator
    # show_all_area: str = 'Show all area'


class App(rumps.App):
    def __init__(self) -> None:
        super(App, self).__init__('...')
        self._menus = Menus()
        self._init_menu()
        # self._url = settings.AQI_DATA_API
        # self._site_name = settings.SITE_NAME
        # rumps.debug_mode(settings.DEBUG)

    def _init_menu(self) -> None:
        for menu in self._menus:
            if type(menu) == str:
                self.menu.add(rumps.MenuItem(menu))
            else:
                self.menu.add(menu)
        # air_data, aqi_number = self.get_air()
        # self.title = f'AQI:{aqi_number}'
        # self.menu[self._menus.air_data].title = air_data
        self.menu[self._menus.update_time].title = self._get_refresh_time()

    def _get_refresh_time(self) -> str:
        return f'Update:{datetime.datetime.now().strftime("%m-%d %H:%M:%S")}'


    @rumps.clicked("hello window")
    def click_hello_window(self, _) -> None:
        w = window.Window()
        w.run()
        print('window close')

    # def get_air(self) -> tuple[str, str]:
    #     """Query and parse AQI data."""
    #     result = f"Not found: {self._site_name}"
    #     aqi = '-1'

    #     with lib.request(self._url) as repo:
    #         if repo.status != 200:
    #             return result, aqi
    #         content_obj = repo.read().decode('utf8')
    #         obj = json.loads(content_obj)
    #         for data in obj:
    #             if data.get('SiteName', '') == self._site_name:
    #                 aqi = data['AQI']
    #                 result = (
    #                     f"{data['SiteName']}:"
    #                     f"{data['Status']}, AQI(<100): {aqi}"
    #                 )
    #                 break

    #     return result, aqi


    # def get_monitor_area(self) -> str:
    #     """Get all air monitor area."""
    #     area_list = []
    #     output = ""
    #     with lib.request(self._url) as repo:
    #         if repo.status == 200:
    #             content = repo.read().decode('utf8')
    #             obj = json.loads(content)
    #             for data in obj:
    #                 area_list.append(data.get('SiteName'))

    #         # string display format
    #         for idx, v in enumerate(area_list):
    #             output += v + " , "

                # if idx + 1 == len(area_list):
                #     output = output.rstrip(", ")

                # if (idx + 1) % 5 == 0:
                #     output += "\n"

        # return output

    # @rumps.clicked("Change Area")
    # def area_setting(self, _: rumps.MenuItem) -> None:
    #     """ clicked "Change Area button." """
    #     # print('click change area', sender)
    #     setting_window = rumps.Window(
    #         message='Set where you want to monitor air area',
    #         title='Preferences',
    #         default_text=self._site_name,
    #         ok="Submit",
    #         cancel='Cancel',
    #         dimensions=(100, 20)
    #     )

    #     resp = setting_window.run()
    #     if resp.clicked:
    #         self._site_name = resp.text
    #         self.menu[self._menus.air_data] = self.get_air()[0]

    # @rumps.timer(60)
    # def update(self, _: rumps.Timer) -> None:
    #     """ Timer """

    # @rumps.clicked("Show all area")
    # def show_area(self, _: rumps.MenuItem) -> None:
    #     """ clicked "Show all area button." """
    #     area_list = self.get_monitor_area()

    #     show_window = rumps.Window(
    #         message='All area name',
    #         title='Area List',
    #         default_text=area_list,
    #         ok=None,
    #         dimensions=(300, 300)
    #     )

    #     show_window.run()

