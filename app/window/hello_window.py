import pygame as pg
import pygame_gui
from pygame_gui.core import ObjectID


SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
WINDOW_TITLE = 'Quick Start'

class Window:
    def __init__(self):
        pg.init()
        self.fps = 60
        self.clock = pg.time.Clock()
        self.screen = self._create_screen()
        self.is_running = True
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), './test_theme.json')
        self.init_ui()

    def init_ui(self) -> None:
        self.drop_down_menu = pygame_gui.elements.UIDropDownMenu(
            ['a', 'b', 'c'],
            'a',
            pg.Rect(350, 275, 200, 30),
            manager=self.manager,
            object_id=ObjectID(object_id='#ddm')
        )

    def _create_screen(self) -> pg.surface.Surface:
        screen = pg.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(WINDOW_TITLE)
        return screen

    def update(self) -> None:
        dt = float(self.clock.get_time() / 1000) 
        self.manager.update(dt)
        pg.display.update()

    def draw_back_ground(self) -> None:
        background = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(pg.Color('#95a5a6'))
        self.screen.blit(background, (0, 0))

    def draw(self) -> None:
        self.draw_back_ground()
        self.manager.draw_ui(self.screen)

    def handle_event(self, key_event: pg.event.Event) -> None:
        self.manager.process_events(key_event)
        if key_event.type == pg.QUIT:
            self.is_running = False
            pg.quit()

    def run(self) -> None:
        while self.is_running:
            self.clock.tick(self.fps)
            self.update()
            self.draw()
            for event in pg.event.get():
                self.handle_event(event)

# Window().run()
