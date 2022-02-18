from typing import Optional, Any

import pygame as pg
import pygame_gui as pg_gui
from pygame_gui import PackageResource

from .. import settings


class Window:
    def __init__(self,
                 title: str,
                 width: int,
                 height: int,
                 theme_path: Optional[PackageResource],
                 background_colour: tuple[int, int, int]) -> None:
        pg.init()
        self.background_colour = background_colour
        self.title = title
        self.height = height
        self.theme_path = theme_path
        self.width = width
        self.fps = 60
        self.clock = pg.time.Clock()
        self.screen = self._create_screen()
        self.is_running = True
        self.manager = pg_gui.UIManager(
            (self.width, self.height),
            enable_live_theme_updates=True,
            theme_path=self.theme_path
        )

    def _create_screen(self) -> pg.surface.Surface:
        pg.display.set_icon(pg.image.load(settings.APP_BMP))
        screen = pg.display.set_mode(pg.Vector2(self.width, self.height))
        pg.display.set_caption(self.title)
        return screen

    def update(self, dt: float) -> None:
        self.manager.update(dt)
        pg.display.update()

    def draw_back_ground(self) -> None:
        background = pg.Surface((self.width, self.height))
        background.fill(pg.Color(self.background_colour))
        self.screen.blit(background, (0, 0))

    def draw(self) -> None:
        self.draw_back_ground()
        self.manager.draw_ui(self.screen)

    def handle_event(self, key_event: pg.event.Event) -> None:
        if key_event.type == pg.QUIT:
            self.is_running = False
            pg.quit()
            return
        self.manager.process_events(key_event)

    def run(self) -> Any:
        while self.is_running:
            self.clock.tick(self.fps)
            dt = float(self.clock.get_time() / 1000)
            self.update(dt)
            self.draw()
            for event in pg.event.get():
                self.handle_event(event)
        pg.quit()
