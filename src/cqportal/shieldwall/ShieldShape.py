import cadquery as cq
from cadqueryhelper import Base

def shield_shape(
    length = 20,
    width = 20,
    base_height = 4,
    middle_width_inset = -6,
    travel_distance = 2
):
    pts = [
        (0,0),
        (0,width),# base width
        (base_height,width),#base Height
        (base_height, width + middle_width_inset), # middle

        (length,width + middle_width_inset),# top
        (length,-1*(middle_width_inset)),# top

        (base_height, -1*(middle_width_inset)), # middle
        (base_height,0)
    ]
    
    base_sPnts = [
        (base_height/2+.00001, width/2),
        (base_height, width/2 - base_height/2 )
    ]
    
    mid_sPnts = [
        (base_height, width/2 + middle_width_inset+travel_distance-0.00001),
        (base_height+2, width/2 + middle_width_inset )
    ]
    
    top_sPnts = [
        (length-travel_distance+0.00001 , width/2 + middle_width_inset),
        (length, width/2 + middle_width_inset -2)
    ]

    result = (
        cq.Workplane("XY")
        .center(-1*(length/2),0)
        .lineTo(0, width/2) # base width
        .lineTo(base_height/2, width/2) #base Height
        .threePointArc(base_sPnts[0], base_sPnts[1])
        .lineTo(base_height, width/2 + middle_width_inset+travel_distance)
        .threePointArc(mid_sPnts[0], mid_sPnts[1])
        .lineTo(length-travel_distance, width/2 + middle_width_inset)
        .threePointArc(top_sPnts[0], top_sPnts[1])
        .lineTo(length, 0)
        .close()
    )
    
    ext = result.extrude(1)
    mirror = (
        cq.Workplane("XY")
        .union(ext.translate((0,0,0-.5)))
        .union(ext.translate((0,0,0-.5)).rotate((1,0,0),(0,0,0),180))
    ).translate((0,0,.5))
    
    mirrored_face_wires = mirror.faces("<Z").wires().toPending()
    return mirrored_face_wires

#-------------------------

class ShieldShape(Base):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.length = 20
        self.width = 20
        self.base_height = 4
        self.middle_width_inset = -6
        self.travel_distance =2
        self.shape_method = shield_shape
        
        # shapes
        self.shape=None
        
    def _make_shape(self):
        self.shape = self.shape_method(
            length = self.length,
            width = self.width,
            base_height = self.base_height,
            middle_width_inset = self.middle_width_inset,
            travel_distance = self.travel_distance
        )
        
    def make(self, parent=None):
        super().make(parent)
        self._make_shape()
        
    def build(self):
        super().build()
        return self.shape