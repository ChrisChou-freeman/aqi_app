from app.window import base_window
from app import settings

class SetKeyWindow(base_window.Window):
    def __init__(self) -> None:
        super().__init__('Select Area', 400, 200, None, settings.RGB_WHITE)
