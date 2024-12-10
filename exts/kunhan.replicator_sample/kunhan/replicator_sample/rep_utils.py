import omni.replicator.core as rep
from .utils import *
import omni.kit.commands

def rep_create_camera(position, rotation, focus_distance, f_stop, resolution):
    camera = rep.create.camera(
        position=position,
        rotation=rotation,
        focus_distance=focus_distance,
        f_stop=f_stop,
        )
    render_product = rep.create.render_product(camera, resolution=resolution)
    return render_product

def rep_modify_prim():
    pass

def rep_register_randomizer():
    pass

def rep_annotation_set():
    pass

def rep_writer_set():
    pass

def execute_replicator():
    pass

def rep_preview():
    rep.orchestrator.preview()

def rep_run(num: int = 1):
    rep.orchestrator.run(num_frames=num)

def rep_stop():
    rep.orchestrator.stop()

def does_replicator_layer_exist(name: str = "replicator") -> bool:
    stage = get_current_stage()
    for layer in stage.GetLayerStack():
        if layer.GetDisplayName() == name:
            return True
    return False

def get_replicator_layer(name: str = "replicator"):
    stage = get_current_stage()
    pos = 0
    for layer in stage.GetLayerStack():
        if layer.GetDisplayName() == name:
            return layer, pos
        pos = pos + 1
    return None

def remove_replicator_scope():
    if is_valid_prim('/Replicator'):
        delete_prim('/Replicator')

def remove_replicator_graph(name: str = "replicator"):
    if get_replicator_layer(name) is not None:
        layer, pos = get_replicator_layer(name)
        omni.kit.commands.execute('RemoveSublayer',
            layer_identifier=layer.identifier,
            sublayer_position=pos)
