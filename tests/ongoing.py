from __future__ import annotations

import sys
from typing import Any
from random import randint

from pytermgui import (
    InputField,
    get_widget,
    MarkupFormatter,
    MouseTarget,
    Container,
    keys,
    markup,
    Widget,
    real_length,
    Slider,
    Label,
)

from pytermgui.ansi_interface import MouseAction
from pytermgui.window_manager import WindowManager, Window
from pytermgui.cmd import MarkupApplication


def main() -> None:
    """Main method"""

    style = MarkupFormatter("[60]{item}")
    for obj in [Window, Container]:
        obj.set_style("corner", style)
        obj.set_style("border", style)

    manager = WindowManager()
    manager.bind("*", lambda *_: manager.show_targets())
    manager.bind(
        keys.CTRL_H,
        lambda *_: {
            markup.alias("wm-title", str(randint(0, 255))),
            markup.alias("wm-title", str(randint(0, 255))),
        },
    )

    app = MarkupApplication(manager)
    # manager.add(app.construct_window())

    field: InputField

    slider = Slider()

    window = (
        Window(width=50, title="root", is_modal=True)
        + f"[wm-title]This is a test window"
        ""
        + {"Button": ["label"]}
        + {"Toggle": [("one", "two")]}
        + {"Checkbox": [False]}
        + {
            "Lock slider": [
                slider.locked,
                lambda checked: setattr(slider, "locked", checked),
            ]
        }
        + {
            "Show counter": [
                slider.show_counter,
                lambda checked: setattr(slider, "show_counter", checked),
            ]
        }
        # + {"Container test": Container(["one"], ["two"])}
        + ""
        + slider
        + ""
        + (
            ["Submit", lambda *_: manager.alert(field.value)],
            ["Reset", lambda *_: setattr(field, "value", "")],
            ["Exit", lambda *_: manager.exit()],
        )
        + ["Hello", lambda *_: manager.exit()]
        + [
            ("Set Fullscreen", "Set Floating"),
            lambda value: window.set_fullscreen("Floating" in value),
        ]
        + (Container() + "test" + ["other"])
    ).center()

    manager.add(window)
    manager.add(app.construct_window())
    manager.bind(keys.CTRL_T, lambda manager, _: manager.add(window.copy()))
    manager.run()


if __name__ == "__main__":
    main()
