import omni.replicator.core as rep
from .utils import *
import omni.kit.commands

def rep_preview():
    rep.orchestrator.preview()

def rep_stop():
    rep.orchestrator.stop()

def does_replicator_layer_exist(name: str) -> bool:
    stage = get_current_stage()
    for layer in stage.GetLayerStack():
        if layer.GetDisplayName() == name:
            return True
    return False

def get_replicator_layer(name: str):
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

def remove_replicator_graph(name: str):
    if get_replicator_layer(name) is not None:
        layer, pos = get_replicator_layer(name)
        omni.kit.commands.execute('RemoveSublayer',
            layer_identifier=layer.identifier,
            sublayer_position=pos)
