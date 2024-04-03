import cadquery as cq
from cadqueryhelper import Base

class Mesh(Base):
    def __init__(self):
        super().__init__()
        
    def make(self, parent=None):
        super().make(parent)
        
    def build(self):
        super().build()
        test = cq.Workplane("XY").box(10,10,10)
        return test