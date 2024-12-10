import omni.ui as ui
from .replicator import Replicator
from .style import SPACING, default_defect_main

class MainWindow(ui.Window):
    def __init__(self, title=None, width=750, height=980):
        super().__init__(title, width=width, height=height)
        self.replicator = Replicator(self)
        self.frame.set_build_fn(self._build_fn)

    def destroy(self):
        if self:
            super().destroy()

    def _build_fn(self):
        with self.frame:
            with ui.ScrollingFrame(style = default_defect_main):
                with ui.VStack(spacing=SPACING, style={"margin": 2}):
                    self.replicator.build_replicator_controls()
                    