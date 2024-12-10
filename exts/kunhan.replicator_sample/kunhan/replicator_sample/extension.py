import omni.ext
import omni.kit.ui
import omni.ui as ui
from functools import partial
from .window import MainWindow
import asyncio


class MyExtension(omni.ext.IExt):
    WINDOW_NAME = "Replicator Extension"
    MENU_PATH = f"Replicator/{WINDOW_NAME}"

    def __init__(self) -> None:
        super().__init__()
        self._window_instance = None
        self._menu = None

    def on_startup(self, ext_id):
        print("[kunhan.replicator_sample] Extension started")
        ui.Workspace.set_show_window_fn(MyExtension.WINDOW_NAME, partial(self.show_window, None))

        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            self._menu = editor_menu.add_item(
                MyExtension.MENU_PATH,
                self.show_window,
                toggle=True,
                value=True
            )
        self.show_window(None, True)

    def on_shutdown(self):
        if self._menu:
            omni.kit.ui.get_editor_menu().remove_item(MyExtension.MENU_PATH)
            self._menu = None

        if self._window_instance:
            self._window_instance.destroy()
            self._window_instance = None

        ui.Workspace.set_show_window_fn(MyExtension.WINDOW_NAME, None)

        print("[kunhan.replicator_sample] Extension shutdown")

    async def _destroy_window_async(self):
        await omni.kit.app.get_app().next_update_async()
        if self._window_instance:
            self._window_instance.destroy()
            self._window_instance = None

    def _visibility_changed_fn(self, visible):
        self._set_menu(visible)
        if not visible:
            asyncio.ensure_future(self._destroy_window_async())

    def _set_menu(self, value):
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            editor_menu.set_value(MyExtension.MENU_PATH, value)

    def show_window(self, menu, value):
        if value:
            if not self._window_instance:
                self._window_instance = MainWindow(title=MyExtension.WINDOW_NAME)
                self._window_instance.set_visibility_changed_fn(self._visibility_changed_fn)
        else:
            if self._window_instance:
                self._window_instance.visible = False
