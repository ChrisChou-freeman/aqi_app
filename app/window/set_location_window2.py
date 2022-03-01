from typing import Optional
from dataclasses import dataclass

import toga
from toga.style import Pack
from toga.sources.list_source import Row
from toga.widgets.optioncontainer import OptionItem

from app.api import aqi
from app import settings
from app import data_base


@dataclass
class SelectArea:
    success: bool = True
    reson: str = ''
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None

    def filled_all(self) -> bool:
        return all([self.country, self.state, self.city])


class SetLocationWindow(toga.App):
    def __init__(self, select_area: SelectArea) -> None:
        super().__init__('Set Location', 'SetLocationWindow')
        self.select_area = select_area
        self.debug = False
        self.data_base = self.get_db()
        self.box = toga.Box()
        self.oc = toga.OptionContainer()
        self.contry_table = toga.Table(
            ['Locations'],
            style=Pack(width=400),
            on_select=self.table_click,
            missing_value='None'
        )
        self.state_table = toga.Table(
            ['Locations'],
            style=Pack(width=400),
            on_select=self.table_click,
            missing_value='None'
        )
        self.city_table = toga.Table(
            ['Locations'],
            style=Pack(width=400),
            on_select=self.table_click,
            missing_value='None'
        )
        self._build()

    def get_db(self) -> data_base.DataBase:
        with data_base.DataBase(settings.DATA_PATH) as db:
            return db

    def _fill_table(self) -> None:
        ...

    def _build_table(self) -> None:
        self.oc.add('Country', self.contry_table)
        self.oc.add('State', self.state_table)
        self.oc.add('City', self.city_table)

    def _build(self) -> None:
        self._build_table()
        self.box.add(self.oc)

    def table_click(self, table: toga.Table, row: Optional[Row]) -> None:
        if row is None:
            return
        head: str = table.headings[0]
        select_item = getattr(row, head.lower())
        item: OptionItem = self.oc.content[0]
        item.label = select_item

    def startup(self) -> None:
        self.main_window = toga.MainWindow(
            title=self.formal_name,
            factory=self.factory,
            size=(400, 200)
        )
        self.main_window.content = self.box
        self.main_window.show()

    def exit(self) -> Optional[bool]:
        return super().exit()

    def get_countries(self) -> list[str]:
        countries = aqi.AQIapi(self.debug).request_countries()
        if countries.error:
            self.is_running = False
            self.select_area.success = False
            self.select_area.reson = countries.reson
            return []
        datas: list[dict[str, str]] = countries.data['data']
        return [data['country'] for data in datas]

    def get_states(self) -> list[str]:
        country = self.select_area.country
        if country is None:
            return []
        states = aqi.AQIapi(self.debug).request_states(country)
        if states.error:
            self.is_running = False
            self.select_area.success = False
            self.select_area.reson = states.reson
            return []
        datas: list[dict[str, str]] = states.data['data']
        return [data['state'] for data in datas]

    def get_cities(self) -> list[str]:
        country = self.select_area.country
        state = self.select_area.state
        if country is None or state is None:
            return []
        citys_data = aqi.AQIapi(self.debug).request_cities(country, state)
        if citys_data.error:
            self.is_running = False
            self.select_area.success = False
            self.select_area.reson = citys_data.reson
            return []
        datas: list[dict[str, str]] = citys_data.data['data']
        return [data['city'] for data in datas]

    def cache_select_area(self) -> None:
        if not self.select_area.filled_all():
            return
        selected_country = self.select_area.country
        selected_state = self.select_area.state
        selected_city = self.select_area.city
        select_area = f'{selected_country}_{selected_state}_{selected_city}'
        with self.data_base as db:
            db.set_data('my_location', select_area, 0)

    def run(self) -> None:
        self.main_loop()
