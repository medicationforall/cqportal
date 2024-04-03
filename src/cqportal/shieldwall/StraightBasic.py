import cadquery as cq
from cadqueryhelper import Base
from . import ShieldShape

class StraightBasic(Base):
    def __init__(self):
        super().__init__()

        #properties
        self.length = 75
        self.width = 20
        self.height = 20

        # blueprints
        self.bp_shape = ShieldShape()

        #shape
        self.wall = None

    def __make_wall_basic(self):
        shape = self.bp_shape.shape
        base_wall = (
            shape
            .extrude(self.length)
            .translate((0,0,-1*(self.length/2)))
            .rotate((0,1,0),(0,0,0),90)
        )
        self.wall = base_wall
        
    def make(self, parent=None):
        super().make(parent)
        self.bp_shape.length = self.height
        self.bp_shape.width = self.width
        self.bp_shape.make(parent)

        self.__make_wall_basic()
        
    def build(self):
        super().build()
        return self.wall