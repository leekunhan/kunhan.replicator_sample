import omni.replicator.core as rep
import omni.ui as ui
import omni.usd
import omni.kit.commands
import carb
from pxr import Usd, Sdf

def on_get_selection(model: ui.SimpleStringModel()) -> str:
    selected_paths = omni.usd.get_context().get_selection().get_selected_prim_paths()
    selected_string = ", ".join(selected_paths)
    model.as_string = selected_string
    print(f"{model} = Selected: {selected_string}")
    return selected_string

def get_string(stage: Usd.Stage, filed_model: ui.SimpleStringModel()) -> Sdf.Path:
    prim_path = stage.GetPrimAtPath(filed_model.as_string())
    return prim_path

# from defect generation extension

def get_current_stage():
    context = omni.usd.get_context()
    stage = context.get_stage()
    return stage

def check_path(path: str) -> bool:
    if not path:
        carb.log_error("No path was given")
        return False
    return True

def is_valid_prim(path: str):
    prim = get_prim(path)
    if not prim.IsValid():
        carb.log_warn(f"No valid prim at path given: {path}")
        return None
    return prim

def delete_prim(path: str):
    omni.kit.commands.execute('DeletePrims',
        paths=[path],
        destructive=False)

def get_prim_attr(prim_path: str, attr_name: str):
    prim = get_prim(prim_path)
    return prim.GetAttribute(attr_name).Get()

def get_textures(dir_path, png_type=".png"):
    textures = []
    dir_path += "/"
    for file in os.listdir(dir_path):
        if file.endswith(png_type):
            textures.append(dir_path + file)
    return textures

def get_prim(prim_path: str):
    stage = get_current_stage()
    prim = stage.GetPrimAtPath(prim_path)
    return prim