from typing import Any

import pygame as pg
import pygame_gui as pg_gui
from pygame_gui.core import ObjectID
from pygame_gui import PackageResource

from app.window import base_window
from app import settings
from app.api import aqi

class SelectAreaWindow(base_window.Window):
    def __init__(self) -> None:
        them_pack = PackageResource(package='data.theme', resource='test_theme.json')
        super().__init__('Select Area', 400, 200, them_pack, settings.RGB_WHITE)
        countries = self.get_countries()
        self.select_countries = pg_gui.elements.UIDropDownMenu(
            countries,
            countries[0],
            pg.Rect(20, 20, 200, 30),
            manager=self.manager,
            object_id=ObjectID(object_id='#ddm')
        )

    def get_countries(self) -> list[str]:
        countries = aqi.AQIapi(debug=True).request_country()
        if countries.error:
            raise IOError(countries.reson)
        datas: list[dict[str, str]] = countries.data['data']
        return [ data['country'] for data in datas ]
