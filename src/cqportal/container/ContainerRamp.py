import cadquery as cq
from . import ContainerDoor
from ..portal import RampGreebled

class ContainerRamp(RampGreebled):
    def __init__(self):
        super().__init__()
        self.bp_outside = ContainerDoor()