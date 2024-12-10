import omni.ui as ui
from omni.ui import color as cl

VHEIGHT = 10
HWIDTH = 10
LABEL_WIDTH = 120
SPACING = 8

default_defect_main = {
    "Button": {
        "width": 0,
        "background_color": ui.color.black
    },
    "HStack": {
        "padding": 5
    }
}

def get_bottom_style():
    return {
        "background_color": cl("#01598c"),
        "color": cl.white,
        "border_radius": 10,
        ":hovered": {"background_color": cl("#004a75")}
    }

def get_style():
    return {
        # "background_color": cl("#f0f0f0"),
        # "color": cl.black,
        # "border_radius": 10,
        # ":hovered": {"background_color": cl("#e0e0e0")}
    }