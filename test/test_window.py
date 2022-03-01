#!/usr/bin/env python
from app import window


def run() -> None:
    sa = window.SelectArea()
    w = window.SetLocationWindow2(sa)
    w.run()
    print(sa)
    # w = window.set_key_window.SetKeyWindow()
