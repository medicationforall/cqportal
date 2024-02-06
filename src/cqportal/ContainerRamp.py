import cadquery as cq
from . import RampGreebled, ContainerDoor

class ContainerRamp(RampGreebled):
    def __init__(self):
        super().__init__()
        self.bp_outside = ContainerDoor()