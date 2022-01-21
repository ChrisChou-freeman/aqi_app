import pygame
import pygame_gui
from pygame_gui.core import ObjectID


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#95a5a6'))

manager = pygame_gui.UIManager((800, 600), './test_theme.json')
drop_down_menu = pygame_gui.elements.UIDropDownMenu(
    ['a', 'b', 'c'],
    'a',
    pygame.Rect(350, 275, 200, 30),
    manager=manager,
    object_id=ObjectID(object_id='#ddm')
)

clock = pygame.time.Clock()
is_running = True

while is_running:
 time_delta = clock.tick(60)/1000.0
 for event in pygame.event.get():
     if event.type == pygame.QUIT:
         is_running = False

     manager.process_events(event)

 manager.update(time_delta)

 window_surface.blit(background, (0, 0))
 manager.draw_ui(window_surface)

 pygame.display.update()
