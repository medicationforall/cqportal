import cadquery as cq
from cadqueryhelper import Base

class Magnets(Base):
    def __init__(self):
        super().__init__()
        self.distance = 12.9
        self.pip_height = 2.4
        self.pip_radius = 1.56
        
        #shapes
        self.pip = None
        self.pips = None
        
    def _make_pip(self):
        pip = (
            cq.Workplane("XY")
            .cylinder(
                self.pip_height, 
                self.pip_radius)
        )
        self.pip = pip.rotate((0,1,0),(0,0,0),90)
        
    def __make_pips(self):
        width_translate = self.distance/2
        pips = (
            cq.Workplane("XY")
            .union(self.pip.translate((0,width_translate,0)))
            .union(self.pip.translate((0,-width_translate,0)))
        )
        self.pips = pips
        
    def make(self, parent = None):
        super().make(parent)
        self._make_pip()
        self.__make_pips()
        
    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            #.union(self.pip)
            .union(self.pips)
        )
        return scene