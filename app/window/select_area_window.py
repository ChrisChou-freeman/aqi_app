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
        super().__init__('', 550, 300, them_pack, settings.RGB_WHITE)
        countries = self.get_countries()
        self.selected_country = ''
        self.selected_state = ''
        self.selected_city = ''
        self.label_tiele = pg_gui.elements.UILabel(
            pg.Rect(0, 0, 550, 50),
            'Select Area',
            manager=self.manager,
            object_id=ObjectID(object_id='#lbt')
        )
        self.mane_panel = pg_gui.elements.UIPanel(
            pg.Rect(-3, 50, 556, 45),
            3,
            manager=self.manager,
            object_id=ObjectID(object_id='#mc')
        )
        self.contries_menu = pg_gui.elements.UIButton(
            pg.Rect(2, -1, 100, 45),
            'Contry',
            manager=self.manager,
            container=self.mane_panel,
            object_id=ObjectID(object_id='#m')
        )
        self.states_menu = pg_gui.elements.UIButton(
            pg.Rect(100, -1, 100, 45),
            'State',
            manager=self.manager,
            container=self.mane_panel,
            object_id=ObjectID(object_id='#m')
        )
        self.states_menu = pg_gui.elements.UIButton(
            pg.Rect(198, -1, 100, 45),
            'City',
            manager=self.manager,
            container=self.mane_panel,
            object_id=ObjectID(object_id='#m')
        )
        self.selection_list = pg_gui.elements.UISelectionList(
            pg.Rect(0, 95, 556, 205),
            countries,
            manager=self.manager
        )
        # self.label_countries = None
        # self.select_countries = pg_gui.elements.UIDropDownMenu(
        #     countries,
        #     countries[0],
        #     pg.Rect(100, 40, 200, 30),
        #     manager=self.manager,
        #     object_id=ObjectID(object_id='#ddm')
        # )
        # self.label_states = pg_gui.elements.UILabel(
        #     pg.Rect(170, 75, 60, 20),
        #     'State:',
        #     manager=self.manager,
        #     object_id=ObjectID(object_id='#lbt')
        # )
        # self.select_states = pg_gui.elements.UIDropDownMenu(
        #     [],
        #     '',
        #     pg.Rect(100, 100, 200, 30),
        #     manager=self.manager,
        #     object_id=ObjectID(object_id='#lbt')
        # )

    def handle_event(self, key_event: pg.event.Event) -> None:
        super().handle_event(key_event)
        if not self.is_running:
            return
        if key_event.type == pg_gui.UI_BUTTON_PRESSED:
            if key_event.ui_element == self.contries_menu:
                print('country')
        # if key_event.type == pg_gui.UI_DROP_DOWN_MENU_CHANGED:
        #     # select countries option event
        #     if key_event.ui_element == self.select_countries:
        #         country = key_event.text
        #         self.get_states(country)
        #     # select states option event
        #     if key_event.ui_element == self.select_states:
        #         state = key_event.text
        #         self.get_cities(country, state)

    def update(self, dt: float) -> None:
        super().update(dt)

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
        # for state in states_options:
        #     self.select_states.options_list.append(state)

    def get_cities(self, country: str, state: str) -> None:
        if country == '' or state == '':
            return
        citys_data = aqi.AQIapi(debug=True).request_city(country, state)
        datas: list[dict[str, str]] = citys_data.data['data']
        print(datas)

