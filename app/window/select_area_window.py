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
        self.label_countries = pg_gui.elements.UILabel(
            pg.Rect(170, 15, 60, 20),
            'Contry:',
            manager=self.manager,
            object_id=ObjectID(object_id='#lbt')
        )
        self.select_countries = pg_gui.elements.UIDropDownMenu(
            countries,
            countries[0],
            pg.Rect(100, 40, 200, 30),
            manager=self.manager,
            object_id=ObjectID(object_id='#ddm')
        )
        self.label_states = pg_gui.elements.UILabel(
            pg.Rect(170, 75, 60, 20),
            'State:',
            manager=self.manager,
            object_id=ObjectID(object_id='#lbt')
        )
        self.select_states = pg_gui.elements.UIDropDownMenu(
            [],
            '',
            pg.Rect(100, 100, 200, 30),
            manager=self.manager,
            object_id=ObjectID(object_id='#lbt')
        )

    def handle_event(self, key_event: pg.event.Event) -> None:
        super().handle_event(key_event)
        if not self.is_running:
            return
        country = ''
        state = ''
        if key_event.type == pg_gui.UI_DROP_DOWN_MENU_CHANGED:
            # select countries option event
            if key_event.ui_element == self.select_countries:
                country = key_event.text
                self.get_states(country)
            # select states option event
            if key_event.ui_element == self.select_states:
                state = key_event.text
                self.get_cities(country, state)

    def get_countries(self) -> list[str]:
        countries = aqi.AQIapi(debug=True).request_country()
        if countries.error:
            raise IOError(countries.reson)
        datas: list[dict[str, str]] = countries.data['data']
        return [ data['country'] for data in datas ]

    def get_states(self, country: str) -> None:
        if country == '':
            return
        states = aqi.AQIapi(debug=True).request_state(country)
        datas: list[dict[str, str]] = states.data['data']
        states_options = [data['state'] for data in datas]
        for state in states_options:
            self.select_states.options_list.append(state)

    def get_cities(self, country: str, state: str) -> None:
        if country == '' or state == '':
            return

