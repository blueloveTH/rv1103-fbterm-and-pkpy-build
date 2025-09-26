from frontend.routes.base import Page
from frontend import ui

from .base import TabController, tab_title

class StatsPage(Page):
    def __init__(self, controller: TabController):
        self.controller = controller

    def poll(self, io):
        while True:
            state, axis = yield from io.input.wait_for_input()
            if self.controller.test(state):
                break

    def __call__(self, io):
        body = ui.Column(
            [
                tab_title("属性界面", io.input),
            ],
            height=io.config.body_height_ex
        )

        return ui.VStack([
            self.common_header(io),
            ui.HDivider(),
            body,
            ui.HDivider(),
            self.common_footer(io),
        ], width=io.config.width)