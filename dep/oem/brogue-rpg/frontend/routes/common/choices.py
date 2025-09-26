from typing import Any, Generator

from frontend.platform import VirtualKey
from frontend import ui

from ..base import Page


class Option:
    def __init__(self, name: String, desc: String, enabled: bool = True):
        self.name = name
        self.desc = desc
        self.enabled = enabled


class ChoicesPage(Page[int]):
    def __init__(self, options: list[Option], title: String | None = None, cursor: int = 0):
        self.options = [o for o in options if o.enabled]
        self.title = title
        self.cursor = cursor

    def poll(self, io) -> Generator[None, Any, int]:
        while True:
            state, axis = yield from io.input.wait_for_input()
            self.cursor = (self.cursor + axis.y) % len(self.options)
            if state[VirtualKey.OK]:
                return self.cursor
            elif state[VirtualKey.ESCAPE]:
                return -1
            yield

    def __call__(self, io):
        choice_width = io.config.width // 2 - 1
        desc_width = io.config.width - choice_width - 1
        choice_height = io.config.body_height

        if self.title is not None:
            choice_height -= 1

        body = ui.HStack([
            ui.Column([
                    ui.richtext(
                        f'{i + 1}. {option.name}',
                        bg=ui.theme.selected_bg if i == self.cursor else None,
                        width=choice_width,
                    )
                    for i, option in enumerate(self.options)
                ],
                width=choice_width,
                height=choice_height,
            ),
            ui.VDivider(),
            ui.Column([
                ui.MultiLineText(
                    str(self.options[self.cursor].desc),
                    width=desc_width,
                )
            ], width=desc_width),
        ], height=choice_height)

        return ui.VStack([
            self.common_header(io),
            ui.HDivider(),
            ui.Text(
                ui.richtext(
                    str(self.title),
                    width=io.config.width,
                    bg=ui.theme.title_bg,
                )
            ) if self.title else None,
            body,
            ui.HDivider(),
            ui.Newline(height=2),
            ui.HDivider(),
            self.common_footer(io),
        ], width=io.config.width)
    
