import cadquery as cq
from cadqueryhelper import Base

def arch_pointed(length=30, width=5, height=50, inner_height=25):
    m_length = length/2 #mirror length
    sPnts = [
        (inner_height+.00001, m_length+0),
        (height, 0)
    ]

    result = (
        cq.Workplane("XY")
        .center(-(height/2),0)
        .lineTo(0, m_length)
        .lineTo(inner_height, m_length)
        .spline(sPnts, includeCurrent=True)
        .close().mirrorX()
    )
    return result



#-------------------
class ArchShape(Base):
    def __init__(self):
        super().__init__()
        #properties
        self.length = 25
        self.width = 20
        self.base_height =5
        self.middle_width_inset = -6
        
        
        #shapes
        self.shape = None
        
    def make(self, parent=None):
        super().make(parent)
        self.shape = arch_pointed(
          length=self.width,
          width=0,
          height=self.length,
          inner_height=self.base_height
        )
        
    def build(self):
        super().build()
        return (
            self.shape
            #.rotate((0,0,1),(0,0,0),90)
            #.rotate((0,1,0),(0,0,0),-90)
        )