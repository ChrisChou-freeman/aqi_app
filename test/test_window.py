#!/usr/bin/env python
from app import window


def run() -> None:
    w = window.select_area_window.SelectAreaWindow()
    # w = window.set_key_window.SetKeyWindow()
    result = w.run()
    print(result)
