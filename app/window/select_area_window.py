from dataclasses import dataclass
from typing import NamedTuple, Optional

import pygame as pg
import pygame_gui as pg_gui
from pygame_gui.core import ObjectID
from pygame_gui import PackageResource

from app.window import base_window
from app.api import aqi
from app import settings


class MenuName(NamedTuple):
    Country: str = 'Country'
    State: str = 'State'
    City: str = 'City'


@dataclass
class SelectArea:
    success: bool = True
    reson: str = ''
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None

    def filled_all(self) -> bool:
        return all([self.country, self.state, self.city])


class SelectAreaWindow(base_window.Window):
    def __init__(self) -> None:
        them_pack = PackageResource(
            package='data.theme',
            resource='test_theme.json'
        )
        super().__init__('', 550, 300, them_pack, settings.RGB_WHITE)
        self.select_area = SelectArea()
        self.menu_name = MenuName()
        self.current_sleceted_menu: Optional[pg_gui.elements.UIButton] = None
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
            self.menu_name.Country,
            manager=self.manager,
            container=self.mane_panel,
            object_id=ObjectID(object_id='#m')
        )
        self.states_menu = pg_gui.elements.UIButton(
            pg.Rect(100, -1, 100, 45),
            self.menu_name.State,
            manager=self.manager,
            container=self.mane_panel,
            object_id=ObjectID(object_id='#m')
        )
        self.city_menu = pg_gui.elements.UIButton(
            pg.Rect(198, -1, 100, 45),
            self.menu_name.City,
            manager=self.manager,
            container=self.mane_panel,
            object_id=ObjectID(object_id='#m')
        )
        self.accept_menu = None
        self.selection_list = pg_gui.elements.UISelectionList(
            pg.Rect(0, 95, 556, 205),
            [],
            manager=self.manager
        )

    def selected_menu(self, key_event: pg.event.Event) -> None:
        menu_list = [self.contries_menu, self.states_menu, self.city_menu]
        if key_event.ui_element not in menu_list:
            return
        for menu in menu_list:
            if key_event.ui_element == menu:
                self.current_sleceted_menu = menu
                menu.select()
                self.change_selection_list()
            else:
                menu.unselect()

    def handle_event(self, key_event: pg.event.Event) -> None:
        super().handle_event(key_event)
        if not self.is_running:
            return
        if key_event.type == pg_gui.UI_BUTTON_PRESSED:
            self.selected_menu(key_event)
        elif key_event.type == pg_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if key_event.ui_element == self.selection_list:
                self.set_select_area()

    def update_menu_text(self) -> None:
        if self.select_area.country is not None \
                and self.contries_menu.text != self.select_area.country:
            self.contries_menu.set_text(self.select_area.country)
        if self.select_area.state is not None \
                and self.contries_menu.text != self.select_area.state:
            self.states_menu.set_text(self.select_area.state)
        if self.select_area.city is not None \
                and self.contries_menu.text != self.select_area.city:
            self.city_menu.set_text(self.select_area.city)

    def check_selected_status(self) -> None:
        '''check if area all selected'''
        if self.select_area.filled_all() or not self.select_area.success:
            self.is_running = False

    def update(self, dt: float) -> None:
        super().update(dt)
        self.update_menu_text()
        self.check_selected_status()

    def set_select_area(self) -> None:
        current_selection = self.selection_list.get_single_selection()
        if self.current_sleceted_menu == self.contries_menu:
            self.select_area.country = current_selection
        elif self.current_sleceted_menu == self.states_menu:
            self.select_area.state = current_selection
        elif self.current_sleceted_menu == self.city_menu:
            self.select_area.city = current_selection

    def change_selection_list(self) -> None:
        if self.current_sleceted_menu == self.contries_menu:
            self.selection_list.set_item_list(self.get_countries())
        elif self.current_sleceted_menu == self.states_menu:
            self.selection_list.set_item_list(self.get_states())
        elif self.current_sleceted_menu == self.city_menu:
            self.selection_list.set_item_list(self.get_cities())

    def get_countries(self) -> list[str]:
        countries = aqi.AQIapi(debug=True).request_countries()
        if countries.error:
            return []
        datas: list[dict[str, str]] = countries.data['data']
        return [data['country'] for data in datas]

    def get_states(self) -> list[str]:
        country = self.select_area.country
        if country is None:
            return []
        states = aqi.AQIapi(debug=True).request_states(country)
        if states.error:
            return []
        datas: list[dict[str, str]] = states.data['data']
        return [data['state'] for data in datas]

    def get_cities(self) -> list[str]:
        country = self.select_area.country
        state = self.select_area.state
        if country is None or state is None:
            return []
        citys_data = aqi.AQIapi(debug=True).request_cities(country, state)
        if citys_data.error:
            return []
        datas: list[dict[str, str]] = citys_data.data['data']
        return [data['city'] for data in datas]

    def run(self) -> SelectArea:
        super().run()
        return self.select_area
