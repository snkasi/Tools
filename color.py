#!/usr/bin/python
# -*- coding: UTF-8 -*-

def COLOR(color, text, bcolor=None, flash=False, light=True):
    flash_str = ';5' if flash else ''
    light_str = '1;' if light else ''
    color_dict = {
        'purplered': ('35', '45'),
        'blue': ('34', '44'),
        'yellow': ('33', '43'),
        'green': ('32', '42'),
        'red': ('31', '41'),
        'cyan': ('36', '46'),
        'black': ('30', '40'),
        'white': ('37', '47')
    }
    fcolor_str = color_dict.get(color, ('0', '1'))[0]
    if bcolor is not None:
        bcolor_str = color_dict.get(bcolor, ('0', '1'))[1] + ';'
    else:
        bcolor_str = ''
    return "\033[{light}{bcolor}{fcolor}{flash}m{text}\033[0m".format(light=light_str, bcolor=bcolor_str, fcolor=fcolor_str, text=text, flash=flash_str)
