import cadquery as cq
from cadqueryhelper import Base

class BaseMagnets(Base):
    '''
    Psuedo Interface defines the minimal properties available for anything that inherits off of BaseMagnets.
    '''

    def __init__(self):
        super().__init__()

        #properties
        self.distance:float = 12.9
        self.pip_height:float = 2.4
        self.pip_radius:float = 1.56

        #shape
        self.pips:cq.Workplane|None = None

    def build(self) -> cq.Workplane:
        if self.pips:
            return self.pips
        else:
            raise Exception('Unable to resolve BaseMagnets pips')
