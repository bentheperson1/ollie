from phue import Bridge
from plugins.plugin_register import register

import os

hue_ip = os.getenv("hue_ip_address")

b = Bridge(hue_ip)
b.connect()
b.get_api()

def rgb_to_xy(red, green, blue):
    # Formulas implemented from: https://gist.github.com/popcorn245/30afa0f98eea1c2fd34d

    red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if red > 0.04045 else (red / 12.92)
    green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if green > 0.04045 else (green / 12.92)
    blue =  pow((blue + 0.055) / (1.0 + 0.055), 2.4) if blue > 0.04045 else (blue / 12.92)

    x = red * 0.649926 + green * 0.103455 + blue * 0.197109
    y = red * 0.234327 + green * 0.743075 + blue * 0.022598
    z = green * 0.053077 + blue * 1.035763

    x = x / (x + y + z)
    y = y / (x + y + z)
    
    return [x, y]

def hue_set_room_on_off(room_name: str, status: bool):
    room_id = b.get_group_id_by_name(room_name.title())

    b.set_group(room_id, 'on', status)
    b.set_group(room_id, "bri", 255)

@register(plugin="hue")
def hue_turn_room_on_by_name(room_name: str):
    hue_set_room_on_off(room_name, True)

    return f"{room_name} is now on."

@register(plugin="hue")
def hue_turn_room_off_by_name(room_name: str):
    hue_set_room_on_off(room_name, False)

    return f"{room_name} is now on."

@register(plugin="hue")
def hue_set_room_color(room_name: str, color_name: str):
    color_hue = []

    match color_name.lower():
        case "red":
            color_hue = rgb_to_xy(1, 0, 0)
        case "blue":
            color_hue = rgb_to_xy(0, 0, 1)
        case "green":
            color_hue = rgb_to_xy(0, 1, 0)
        case "cyan":
            color_hue = rgb_to_xy(0, 0.75, 1)
        case "pink":
            color_hue = rgb_to_xy(1, 0, 1)
        case "white":
            color_hue = rgb_to_xy(0.5, 0.5, 0.5)
        case "off":
            color_hue = rgb_to_xy(0, 0, 0)

    room_id = b.get_group_id_by_name(room_name.title())

    if color_hue != []:
        b.set_group(room_id, 'xy', color_hue)
        b.set_group(room_id, "bri", 255)
