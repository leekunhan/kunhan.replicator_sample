# __all__ = ["ComboboxModel", "CheckboxModel", "SemanticModel", "CustomImportDirModel", "CustomExportDirModel", "PathModel"]

import omni.ui as ui
import carb
import omni.usd
from omni.kit.window.file_importer import get_file_importer
from typing import List
import omni.replicator.core as rep

class ComboboxModel():
    def __init__(self, options: list):
        self.combobox = ui.ComboBox(width = ui.Percent(15))
        self.options = options
        self._build_combobox()

    def _build_combobox(self):
        for choose in self.options:
            choose = str(choose)
            self.combobox.model.append_child_item(None, ui.SimpleStringModel(choose))

    def _get_combo_selection(self):
        current_index =  self.combobox.model.get_item_value_model().as_int
        result = self.options[current_index]
        return result

class CheckboxModel():
    def __init__(self, name: str):
        self.name = name
        self._build_checkbox()

    def _build_checkbox(self):
        with ui.HStack():
            ui.Label(self.name)
            self.use = ui.CheckBox().model
            self.use.set_value(False)

    @property
    def is_checked(self) -> bool:
        return self.use.get_value_as_bool()

class SemanticModel():
    def __init__(self, default_label: str = "Shape"):
        self._default_label = default_label
        self.semantic_label = ui.SimpleStringModel(self._default_label)
        self.count = ui.SimpleIntModel(1)
        self._build_semantic_label()

    def _build_semantic_label(self):
        with ui.HStack(height=0):
            ui.Label("Object Semantic")
            ui.StringField(model=self.semantic_label, tooltip="The label that will be associated with the shape")
            ui.Label("Count")
            ui.IntField(model=self.count, tooltip="The number of shapes to create")

    def _get_semantic_label(self):
        return self.semantic_label.as_string

    def _get_count(self):
        return self.count.as_int

class CustomImportDirModel():
    def __init__(self, label: str, tooltip: str = "", default_dir: str = "", file_types: List[str] = None) -> None:
        self._label_text = label
        self._tooltip = tooltip
        self._file_types = file_types
        self._dir = ui.SimpleStringModel(default_dir)
        self._build_directory()

    @property
    def directory(self) -> str:
        """
        Selected Directory name from file importer

        :type: str
        """
        return self._dir.get_value_as_string()

    def _build_directory(self):
        with ui.HStack(height=0, tooltip=self._tooltip):
            ui.Label(self._label_text, width=ui.Percent(30))
            ui.StringField(model=self._dir)
            ui.Button("Open", width=0, style={"padding": 5}, clicked_fn=self._pick_directory)

    def _pick_directory(self):
        file_importer = get_file_importer()
        if not file_importer:
            carb.log_warning("Unable to get file importer")
        file_importer.show_window(title="Select Folder",
                                  import_button_label="Import Directory",
                                  import_handler=self.import_handler,
                                  file_extension_types=self._file_types
                                  )


    def import_handler(self, filename: str, dirname: str, selections: List[str] = []):
        self._dir.set_value(dirname +  filename)

    def destroy(self):
        self._dir = None

class CustomExportDirModel:
    def __init__(self, label: str, tooltip: str = "", default_dir: str = "", file_types: List[str] = None) -> None:
        self._label_text = label
        self._tooltip = tooltip
        self._file_types = file_types
        self._dir = ui.SimpleStringModel(default_dir)
        self._build_directory()

    @property
    def directory(self) -> str:
        """
        Selected Directory name from file importer

        :type: str
        """
        return self._dir.get_value_as_string()

    def _build_directory(self):
        with ui.HStack(height=0, tooltip=self._tooltip):
            ui.Label(self._label_text, width=ui.Percent(30))
            ui.StringField(model=self._dir)
            ui.Button("Open", width=0, style={"padding": 5}, clicked_fn=self._pick_directory)

    def _pick_directory(self):
        file_importer = get_file_importer()
        if not file_importer:
            carb.log_warning("Unable to get file importer")
            return
        file_importer.show_window(
            title="Select Folder",
            import_button_label="Import Directory",
            import_handler=self.import_handler,
            show_only_folders=True,
            file_extension_types=self._file_types
        )

    def import_handler(self, filename: str, dirname: str, selections: List[str] = []):
        self._dir.set_value(dirname)

    def destroy(self):
        self._dir = None

class PathModel():
    def __init__(self, label: str, button_label: str = "Copy", read_only: bool = False, tooltip: str = "") -> None:
        self._label_text = label
        self._tooltip = tooltip
        self._button_label = button_label
        self._read_only = read_only
        self._path_model = ui.SimpleStringModel()
        self._top_stack = ui.HStack(height=0, tooltip=self._tooltip)
        self._button = None
        self._build()

    @property
    def path_value(self) -> str:
        return self._path_model.get_value_as_string()

    @path_value.setter
    def path_value(self, value) -> None:
        self._path_model.set_value(value)

    def _build(self):
        def copy():
            selected_paths = omni.usd.get_context().get_selection().get_selected_prim_paths()
            selected_string = ", ".join(selected_paths)
            self._path_model.set_value(selected_string)

        with self._top_stack:
            ui.Label(self._label_text, width = ui.Percent(30))
            ui.StringField(model=self._path_model, read_only=self._read_only)
            self._button = ui.Button(self._button_label, width=0,
                                     style={"padding": 5},
                                     clicked_fn=lambda: copy(),
                                     tooltip="Copies the Current Selected Path in the Stage")

    def destroy(self):
        self._path_model = None

class MinMax3fModel:
    def __init__(self, label: str, min_value: float = 0, max_value: float = 10, tooltip: str = "") -> None:
        self._min_model_x = ui.SimpleFloatModel(min_value)
        self._max_model_x = ui.SimpleFloatModel(max_value)
        self._min_model_y = ui.SimpleFloatModel(min_value)
        self._max_model_y = ui.SimpleFloatModel(max_value)
        self._min_model_z = ui.SimpleFloatModel(min_value)
        self._max_model_z = ui.SimpleFloatModel(max_value)
        self._label_text = label
        self._tooltip = tooltip
        self._build_min_max()

    @property
    def min_value(self) -> float:
        """
        Min Value of the UI
        """
        min_x = self._min_model_x.get_value_as_float()
        min_y = self._min_model_y.get_value_as_float()
        min_z = self._min_model_z.get_value_as_float()

        return (min_x, min_y, min_z)

    @property
    def max_value(self) -> float:
        """
        Max Value of the UI

        :type: int
        """
        max_x = self._max_model_x.get_value_as_float()
        max_y = self._max_model_y.get_value_as_float()
        max_z = self._max_model_z.get_value_as_float()
        return (max_x, max_y, max_z)

    @property
    def is_checked(self) -> bool:
        return self._use.get_value_as_bool()

    def _build_min_max(self):
        with ui.VStack(height=0, tooltip=self._tooltip):
            with ui.HStack():
                self._use = ui.CheckBox(width = 0).model
                ui.Label(self._label_text)
            with ui.HStack():
                ui.Label("Min X", width=0)
                ui.FloatDrag(model=self._min_model_x)
                ui.Label("Y", width=0)
                ui.FloatDrag(model=self._min_model_y)
                ui.Label("Z", width=0)
                ui.FloatDrag(model=self._min_model_z)
            with ui.HStack():
                ui.Label("Max X", width=0)
                ui.FloatDrag(model=self._max_model_x)
                ui.Label("Y", width=0)
                ui.FloatDrag(model=self._max_model_y)
                ui.Label("Z", width=0)
                ui.FloatDrag(model=self._max_model_z)

    def destroy(self):
        self._max_model_x = None
        self._min_model_x = None
        self._max_model_y = None
        self._min_model_y = None
        self._max_model_z = None
        self._min_model_z = None

class CameraModel():
    def __init__(self):
        self.camera_name = ui.SimpleStringModel("Camera")
        self.resolution_x = ui.SimpleIntModel(1920)
        self.resolution_y = ui.SimpleIntModel(1080)
        self.render_product = None
        self._build_camera()

    def _build_camera(self):
        with ui.HStack():
            ui.Label("Camera Name")
            ui.StringField(model=self.camera_name)
            ui.Label("Resolution X")
            self.res_x = ui.IntField(model=self.resolution_x)
            ui.Label("Resolution Y")
            self.res_y = ui.IntField(model=self.resolution_y)
            ui.Button("Create Camera", clicked_fn=self.create_camera)

    def create_camera(self):
        with rep.new_layer("Camera"):
            camera = rep.create.camera(
                name=self.camera_name.get_value_as_string(),)
            self.render_product = rep.create.render_product(camera, resolution=(self.res_x.model.as_int,
                                                                           self.res_y.model.as_int))
