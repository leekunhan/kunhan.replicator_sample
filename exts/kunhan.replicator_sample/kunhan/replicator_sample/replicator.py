import omni.ui as ui
from .style import *
from .utils import *
from .rep_utils import *
from .rep_widgets import *
import omni.replicator.core as rep

class Replicator:
    def __init__(self, window):
        self.window = window
        self.max_exces = ui.SimpleIntModel(10)
        self.writer_option = ["rgb", "bounding_box_2d_tight", "semantic_segmentation", "instance_segmentation", "normals"]
        self.shape_option = ["cube", "sphere", "cylinder", "cone", "torus", "plane"]

    def _build_collapse_base(self, label: str, collapsed: bool = False):
        v_stack = None
        with ui.CollapsableFrame(label, height=0, collapsed=collapsed):
            with ui.ZStack():
                ui.Rectangle()
                v_stack = ui.VStack()
        return v_stack

    def create_shape(self, prim_type, semantic_label: str, count: int):
        with rep.new_layer("Shape"):
            if prim_type == "cube":
                rep.create.cube(semantics=[("class", semantic_label)], count= count, scale = 10)
            elif prim_type == "sphere":
                rep.create.sphere(semantics=[("class", semantic_label)], count= count, scale = 10)
            elif prim_type == "cylinder":
                rep.create.cylinder(semantics=[("class", semantic_label)], count= count, scale = 10)
            elif prim_type == "cone":
                rep.create.cone(semantics=[("class", semantic_label)], count= count, scale = 10)
            elif prim_type == "torus":
                rep.create.torus(semantics=[("class", semantic_label)], count= count, scale = 10)
            elif prim_type == "plane":
                rep.create.plane(semantics=[("class", semantic_label)], count= count, scale = 10)

    def create_prim_from_usd(self, prim_path: str, semantic_label: str, count: int):
        if not prim_path.endswith((".usd", ".usda", ".usdc")):
            carb.log_error("Invalid USD file")
            return
        with rep.new_layer("USD"):
            rep.create.from_usd(usd = prim_path, count = count, semantics = [("class", semantic_label)])

    def register_randomizer(self):
        _object = self.get_path.path_value
        position_min = self.position.min_value
        position_max = self.position.max_value
        use_position = self.position.is_checked
        rotation_min = self.rotation.min_value
        rotation_max = self.rotation.max_value
        use_rotation = self.rotation.is_checked

        path_list = [path.strip() for path in _object.split(',')]
        object_group = rep.get.prim_at_path(path = path_list)
        with rep.trigger.on_frame(rt_subframes = 32):
            with object_group:
                if use_position:
                    _position = rep.distribution.uniform(lower=position_min, upper=position_max)
                else:
                    _position = None
                    carb.log_info("No change position value")
                if use_rotation:
                    _rotation = rep.distribution.uniform(lower=rotation_min, upper=rotation_max)
                else:
                    _rotation = None
                    carb.log_info("No change rotation value")
                rep.modify.pose(position = _position, rotation = _rotation)

    def replicator_writer(self):
        annotators_kwargs = {}
        for i, _ in enumerate(self.writer_option):
            if self.annotations[i].is_checked:
                annotators_kwargs[self.writer_option[i]] = True
        _num = self.max_exces.get_value_as_int()
        render_product = self.camera.render_product
        output_dir = self.export_dir.directory

        writer = rep.writers.get("BasicWriter")
        writer.initialize(output_dir = output_dir, **annotators_kwargs)
        writer.attach(render_product)

        print(f"annotators_kwargs = {annotators_kwargs}")
        print(f"output_dir = {output_dir}")
        print(f"render_product = {render_product}")
        print(f"render_product_type = {type(render_product)}")
        print(f"num = {_num}")

        # with rep.new_layer("Randomizer"):
        #     rep_run(num=_num)


    def reset(self):
        remove_replicator_scope()
        remove_replicator_graph("Shape")
        remove_replicator_graph("USD")

    def build_replicator_controls(self):
        with self._build_collapse_base("Create"):
            with ui.VStack():
                ui.Label("Create Prim Using Replicator", height=20)
                with self._build_collapse_base("Shape", collapsed=False):
                    with ui.HStack():
                        shape = ComboboxModel(options = self.shape_option)
                        shape_semantic = SemanticModel()
                        ui.Button("Create", width = ui.Percent(15), clicked_fn = lambda: self.create_shape(prim_type=shape._get_combo_selection(),
                                                                                   semantic_label = shape_semantic._get_semantic_label(),
                                                                                   count = shape_semantic._get_count()
                                                                                   ))
                with self._build_collapse_base("From USD Path", collapsed=False):
                    with ui.VStack():
                        with ui.HStack():
                            usd_dir = CustomImportDirModel(label = "USD Directory",
                                                            file_types = [
                                                                    ("*.usd", "USD File"),
                                                                    ("*.usda", "USD ASCII File"),
                                                                    ("*.usdc", "USD Binary File")],
                                                            tooltip="Directory to import USD files")
                            usd_dir_semantic = SemanticModel(default_label = "usd_dir")
                            ui.Button("Create", width = ui.Percent(15), clicked_fn = lambda: self.create_prim_from_usd(prim_path = usd_dir.directory,
                                                                                                                       semantic_label = usd_dir_semantic._get_semantic_label(),
                                                                                                                        count = usd_dir_semantic._get_count()
                                                                                                                        ))

        with self._build_collapse_base("Randomizer"):
            with ui.VStack():
                self.get_path = PathModel(label="Get Path from Stage")
                with self._build_collapse_base("Modify"):
                    with ui.HStack():
                        with self._build_collapse_base("Position"):
                            self.position = MinMax3fModel(label="Position")
                        with self._build_collapse_base("Rotation"):
                            self.rotation = MinMax3fModel(label="Rotation")
                with ui.HStack():
                    ui.Spacer(width = ui.Percent(90))
                    ui.Button("Register", width=0, clicked_fn=lambda: self.register_randomizer())

        with self._build_collapse_base("Writer"):
            with ui.VStack():
                ui.Label("Camera", width=0)
                self.camera = CameraModel()
                with self._build_collapse_base("Pick Annotator", collapsed=False):
                    self.annotations = []
                    for i in self.writer_option:
                        checkbox = CheckboxModel(name=i)
                        self.annotations.append(checkbox)
                with ui.HStack():
                    ui.Label("trigger on Frame num   =   ", width=ui.Percent(30))
                    ui.IntField(model=self.max_exces)

                self.export_dir = CustomExportDirModel(label="Export Directory",
                                                        file_types = [
                                                                ("*.*", "All File")],
                                                        tooltip="Directory to export images")
                with ui.HStack():
                    ui.Spacer(width=ui.Percent(70))
                    ui.Button("Preview", width = ui.Percent(10), clicked_fn = rep_preview)
                    ui.Button("Stop", width = ui.Percent(10), clicked_fn = rep_stop)
                    ui.Button("Run", width = ui.Percent(10), clicked_fn = self.replicator_writer)

        with ui.HStack():
            ui.Button("Reset", width=ui.Percent(10), height=0, clicked_fn=self.reset)

# import omni.replicator.core as rep

# with rep.new_layer():
# 	camera = rep.create.camera()
# 	render_product = rep.create.render_product(camera, (1920, 1080))

# 	writer = rep.writers.get("BasicWriter")
# 	writer.initialize(output_dir = "C:/Users/ryan0511/Downloads/test_replicator/", rgb = True)
# 	writer.attach(render_product)

# 	object_group = rep.get.prim_at_path (path = "/World/Cube")

# 	with rep.trigger.on_frame(max_execs=30):
# 	   with object_group:
# 	       mod = rep.modify.pose(position=rep.distribution.uniform((-500., -500., -500.), (500., 500., 500.)))
# rep.orchestrator.run()