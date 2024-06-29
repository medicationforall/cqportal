import cadquery as cq
from cadqueryhelper import Base

class BaseShape(Base):
    '''
    Psuedo Interface defines the minimal properties available for anything that inherits off of BaseShape.
    '''

    def __init__(self):
        super().__init__()
        
        #properties
        self.length:float = 25
        self.width:float = 20
        self.base_height:float = 5
        self.middle_width_inset:float = -6
        
        #shapes
        self.shape:cq.Workplane|None = None

    def build(self) -> cq.Workplane:
        super().build()
        if self.shape:
            return self.shape
        else:
            raise Exception('unable to resolve BaseShape shape')