import cadquery as cq
from cadqueryhelper import Base

class BaseMesh(Base):
    '''
    Psuedo Interface defines the minimal properties available for anything that inherits off of BaseMesh.
    '''

    def __init__(self):
        super().__init__()
        
        #properties
        self.length:float = 75
        self.width:float = 3
        self.height:float = 25
        
        #shapes
        self.tile:cq.Workplane|None = None

    def build(self) -> cq.Workplane:
        if self.tile:
            return self.tile
        else:
            raise Exception('Unable to resolve BaseMesh tile')