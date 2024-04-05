import cadquery as cq
from cadqueryhelper import Base, shape

class BaseCoffin(Base):
    def __init__(self):
        super().__init__()
        self.length = 150
        self.width = 5
        self.height = 150
        self.top_length = 90
        self.base_length = 100
        self.base_offset = 35 # offset distance from the base of the ramp

        # shapes
        self.coffin = None

    def _calculate_mid_offset(self):
        mid_offset = -1*(self.height/2) + self.base_offset
        return mid_offset  
    
    def make(self, parent=None):
        super().make(parent)

        mid_offset = self._calculate_mid_offset()
        coffin = shape.coffin(
            self.length,
            self.height,
            self.width,
            self.top_length,
            self.base_length,
            mid_offset = mid_offset
        ).rotate((1,0,0),(0,0,0),-90)

        self.coffin = coffin

    def build(self):
        super().build()
        return self.coffin
