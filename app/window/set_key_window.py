from typing import Optional
from dataclasses import dataclass

import pygame as pg
import pygame_gui as pg_gui
from pygame_gui.core import ObjectID
from pygame_gui import PackageResource

from . import base_window
from .. import settings


@dataclass
class SKey:
    key: Optional[str] = None


class SetKeyWindow(base_window.Window):
    def __init__(self) -> None:
        them_pack = PackageResource(
            package='data.theme',
            resource='test_theme.json'
        )
        super().__init__('Set Key', 400, 200, them_pack, settings.RGB_WHITE)
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

    def update(self, dt: float) -> None:
        super().update(dt)

    def run(self) -> dict[str, Optional[str]]:
        super().run()
        return {}
