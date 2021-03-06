# SPDX-FileCopyrightText: 2021 Mark Winney for Bagaloozy
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text. All drawing is done
using the displayio module.

Pinouts are for the PiTFT and should be run in CPython.
"""
import time

import board
import terminalio
import displayio
import digitalio
import busio
import adafruit_focaltouch
import displaytools
from adafruit_display_text import label
from bagaloozy_ili9488 import ILI9488
from paralleldisplay import ParallelBus
from adafruit_button import Button


# --| Button Config |-------------------------------------------------
BUTTON_X = 110
BUTTON_Y = 95
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_STYLE = Button.ROUNDRECT
BUTTON_FILL_COLOR = 0x00FFFF
BUTTON_OUTLINE_COLOR = 0xFF00FF
BUTTON_LABEL = "HELLO WORLD"
BUTTON_LABEL_COLOR = 0x000000
# --| Button Config |-------------------------------------------------

# Release any resources currently in use for the displays
displayio.release_displays()

tft_data0 = board.IO1
tft_cs = board.IO11
tft_dc = board.IO12
tft_res = board.IO10
tft_write = board.IO14
tft_read = board.IO15

# Enable LCD backlight
tft_toggle = digitalio.DigitalInOut(board.IO13)
tft_toggle.direction = digitalio.Direction.OUTPUT
tft_toggle.value = True

# Setup the display bus
display_bus = ParallelBus(data0=tft_data0,
                          command=tft_dc,
                          chip_select=tft_cs,
                          write=tft_write,
                          read=tft_read,
                          reset=tft_res,
                          frequency=19_999_999)
# Create library object (named "ft") using a Bus I2C port
i2c = busio.I2C(board.IO17, board.IO16)

ft = adafruit_focaltouch.Adafruit_FocalTouch(i2c, debug=False)
display = ILI9488(display_bus, width=320, height=480, auto_refresh=True)

# Make the button
button = Button(
    x=BUTTON_X,
    y=BUTTON_Y,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    style=BUTTON_STYLE,
    fill_color=BUTTON_FILL_COLOR,
    outline_color=BUTTON_OUTLINE_COLOR,
    label=BUTTON_LABEL,
    label_font=terminalio.FONT,
    label_color=BUTTON_LABEL_COLOR,
)

# Make the button
button2 = Button(
    x=BUTTON_X,
    y=BUTTON_Y + 50,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    style=BUTTON_STYLE,
    fill_color=BUTTON_FILL_COLOR,
    outline_color=BUTTON_OUTLINE_COLOR,
    label='World Hello',
    label_font=terminalio.FONT,
    label_color=BUTTON_LABEL_COLOR,
)

# Make the display context
splash = displayio.Group()
display.show(splash)

# Draw a green background
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)

splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(display.width - 40, display.height - 40, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
splash.append(inner_sprite)

# Draw a label
text_group = displayio.Group(scale=3, x=57, y=120)
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

touch_bitmap = displayio.Bitmap(8, 8, 1)
touch_palette = displayio.Palette(1)
touch_palette[0] = 0x000000  # Red
touch_sprite = displayio.TileGrid(touch_bitmap, pixel_shader=touch_palette, x=0, y=0)
splash.append(touch_sprite)

# Add buttons to the display context
splash.append(button)
splash.append(button2)

print("START---")

def button2_pressed_callback(self):
    print('button2_pressed_callback - do something!')

def button2_released_callback(self):
    print('button2_released_callback - do something!')

def button_pressed_callback(self):
    print('button_pressed_callback - do something!')

def button_released_callback(self):
    print('button_released_callback - do something!')


displaytools.set_pressed_callback(button, button_pressed_callback)
displaytools.set_released_callback(button, button_released_callback)

displaytools.set_pressed_callback(button2, button2_pressed_callback)
displaytools.set_released_callback(button2, button2_released_callback)

while True:
    if ft.touched:
        ts = ft.touches
        if ts:
            touch_point = ts[0]  # the shield only supports one point!
            x = touch_point["x"]
            y = touch_point["y"]
            touch_sprite.x = x
            touch_sprite.y = y

            displaytools.recurse_page(splash, [x, y])
    else:
        displaytools.recurse_page(splash, [-1, -1])
        # print("no touched")
        time.sleep(0.10)
    # display.refresh()
