#!/usr/bin/env python
from app import window


def run() -> None:
    w = window.set_location_window.SetLocationWindow()
    # w = window.set_key_window.SetKeyWindow()
    result = w.run()
    print(result)
