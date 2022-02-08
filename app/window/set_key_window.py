from typing import Optional
from dataclasses import dataclass

import pygame as pg
import pygame_gui as pg_gui
from pygame_gui.core import ObjectID
from pygame_gui import PackageResource

from . import base_window
from .. import settings
from .. import data_base


@dataclass
class SKey:
    success: bool = True
    reson: str = ''
    key: Optional[str] = None


class SetKeyWindow(base_window.Window):
    def __init__(self) -> None:
        them_pack = PackageResource(
            package='data.theme',
            resource='test_theme.json'
        )
        super().__init__('Set Key', 400, 200, them_pack, settings.RGB_WHITE)
        with data_base.DataBase(settings.DATA_PATH) as db:
            self.data_base = db
        self.skey = SKey()
        self.label = pg_gui.elements.UILabel(
            pg.Rect(0, 0, 400, 50),
            'engtry iqair key',
            manager=self.manager,
            object_id=ObjectID(object_id='#lbt2')
        )
        self.text_entry = pg_gui.elements.UITextEntryLine(
            pg.Rect(0, 55, 400, 45),
            manager=self.manager,
            object_id=ObjectID(object_id='#tel')
        )
        key_str = self.data_base.get_data('key')
        if key_str is not None:
            self.text_entry.set_text(key_str)

    def handle_event(self, key_event: pg.event.Event) -> None:
        super().handle_event(key_event)
        if key_event.type == pg.KEYDOWN:
            if key_event.key == pg.K_RETURN:
                self.is_running = False

    def update(self, dt: float) -> None:
        super().update(dt)

    def run(self) -> SKey:
        super().run()
        key_str = self.text_entry.get_text()
        if key_str != '':
            with self.data_base as db:
                db.set_data('key', key_str)
        self.skey.key = key_str
        return self.skey
