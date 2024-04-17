import cadquery as cq
from cadqueryhelper import Base

class BaseCut(Base):
    def __init__(self):
        super().__init__()
        #properties
        self.length = 75
        self.width = 10
        self.height = 4
        self.angle = 30
        
        #shapes
        self.cut_out = None
        
    def __make_cut_out(self):
        angle = 90 - self.angle
        self.cut_out = (
            cq.Workplane("XY")
            .sketch()
            .trapezoid(self.width,self.height,angle)
            .finalize()
            .extrude(self.length)
            .translate((0,0,-1*(self.length/2)))
            .rotate((1,0,0),(0,0,0),-90)
            .rotate((0,0,1),(0,0,0),-90)
        )
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_cut_out()
        
        
    def build(self):
        super().build()
        return self.cut_out