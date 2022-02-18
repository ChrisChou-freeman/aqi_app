from typing import Optional
from dataclasses import dataclass
import webbrowser

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
            object_id=ObjectID(object_id='#lbt2', class_id=None)
        )
        self.text_entry = pg_gui.elements.UITextEntryLine(
            pg.Rect(0, 55, 400, 45),
            manager=self.manager,
            object_id=ObjectID(object_id='#tel', class_id=None)
        )
        self.link_text = pg_gui.elements.UITextBox(
            '<a href="https://www.iqair.com/dashboard/api" >Get Key</a>',
            pg.Rect(160, 100, 80, 45),
            manager=self.manager,
            object_id=ObjectID(object_id='#tb', class_id=None)
        )
        key_str = self.data_base.get_data('key')
        if key_str is not None:
            self.text_entry.set_text(key_str)

    def handle_event(self, key_event: pg.event.Event) -> None:
        super().handle_event(key_event)
        if key_event.type == pg.KEYDOWN:
            if key_event.key == pg.K_RETURN:
                self.is_running = False
        if key_event.type == pg_gui.UI_TEXT_BOX_LINK_CLICKED:
            webbrowser.open(key_event.link_target)

    def update(self, dt: float) -> None:
        super().update(dt)

    def run(self) -> SKey:
        super().run()
        key_str = self.text_entry.get_text()
        if key_str != '':
            with self.data_base as db:
                db.set_data('key', key_str, 0)
        self.skey.key = key_str
        return self.skey
