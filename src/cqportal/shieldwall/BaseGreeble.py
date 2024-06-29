import cadquery as cq
from cadqueryhelper import Base

class BaseGreeble(Base):
    '''
    Psuedo Interface defines the minimal properties available for anything that inherits off of BaseGreeble.
    '''

    def __init__(self):
        super().__init__()

        #properties
        self.length:float = 75
        self.width:float = 3
        self.height:float = 25

        self.grill_padding_left:float = 2

        #shapes
        self.body:cq.Workplane|None = None
        self.grill_set:cq.Workplane|None = None
        self.grill_set_internal:cq.Workplane|None = None

    def build(self) -> cq.Workplane:
        super().build()

        if self.body:
            return self.body
        else:
            raise Exception('Unable to resolve BaseGreeble Body')