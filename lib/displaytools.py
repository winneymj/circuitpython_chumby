

import displayio
from functools import wraps
from adafruit_button import Button


def add_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)

        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func  # returning func means func can still be used normally

    return decorator


# Decorator can be written to take normal functions and make them methods

# @add_method(Button)
def set_pressed_callback(self, callback):
    print('set_pressed_callback')
    self._pressed_callback = callback


# @add_method(Button)
def set_released_callback(self, callback):
    print('set_pressed_callback')
    self._released_callback = callback


@add_method(Button)
def detect_touch(self: Button, point):
    (x_pos, y_pos) = point
    if self.contains([x_pos, y_pos]):
        if not hasattr(self, '_pressed_callback') or self.selected:
            return
        self.selected = True
        self._pressed_callback(self)
    else:
        if not hasattr(self, '_released_callback') or not self.selected:
            return
        self.selected = False
        self._released_callback(self)


def recurse_page(page, point):
    for page_item in page:
        if type(page_item) == displayio.Group:
            recurse_page(page_item, point)
        elif type(page_item) == Button:
            page_item.detect_touch(page_item, point)
