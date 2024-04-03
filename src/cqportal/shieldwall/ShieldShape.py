import cadquery as cq
from cadqueryhelper import Base

def shield_shape(
    length = 20,
    width = 20,
    base_height = 4,
    middle_width_inset = -6,

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
        (base_height, width/2 + middle_width_inset+2-0.00001),
        (base_height+2, width/2 + middle_width_inset )
    ]
    
    top_sPnts = [
        (length-2+0.00001 , width/2 + middle_width_inset),
        (length, width/2 + middle_width_inset -2)
    ]

    result = (
        cq.Workplane("XY")
        .center(-1*(length/2),0)
        .lineTo(0, width/2) # base width
        .lineTo(base_height/2, width/2) #base Height
        .threePointArc(base_sPnts[0], base_sPnts[1])
        .lineTo(base_height, width/2 + middle_width_inset+2)
        .threePointArc(mid_sPnts[0], mid_sPnts[1])
        .lineTo(length-2, width/2 + middle_width_inset)
        .threePointArc(top_sPnts[0], top_sPnts[1])
        .lineTo(length, 0)
        .close().mirrorX()
    )
    return result

#-------------------------

def shield_shape_mirror(
    length = 20,
    width = 20,
    base_height = 4,
    middle_width_inset = -6,

):
    #https://github.com/CadQuery/cadquery/issues/1072
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
        (base_height, width/2 + middle_width_inset+2-0.00001),
        (base_height+2, width/2 + middle_width_inset )
    ]
    
    top_sPnts = [
        (length-2+0.00001 , width/2 + middle_width_inset),
        (length, width/2 + middle_width_inset -2)
    ]
    
    # these are mirror inverses of the arcs....
    top_sPnts_m = [
        (length, -1*(width/2 + middle_width_inset -2)-0.00001),
        (length-2+0.1 , -1*(width/2 + middle_width_inset))
    ]
    
    mid_sPnts_m = [
        (base_height+2-0.00001, -1*(width/2 + middle_width_inset) ),
        (base_height, -1*(width/2 + middle_width_inset+2)),
    ]
    
    base_sPnts_m = [
        (base_height, -1*(width/2 -2)-0.00001),
        (base_height/2, -1*(width/2))
    ]

    result_wires = (
        cq.Workplane("XY")
        .center(-1*(length/2),0)
        .lineTo(0, width/2) # base width
        .lineTo(base_height/2, width/2) #base Height
        .threePointArc(base_sPnts[0], base_sPnts[1])
        .lineTo(base_height, width/2 + middle_width_inset+2)
        .threePointArc(mid_sPnts[0], mid_sPnts[1])
        .lineTo(length-2, width/2 + middle_width_inset)
        .threePointArc(top_sPnts[0], top_sPnts[1])
        .lineTo(length,0)
        #manual mirror, I dislike this immensely.
        .lineTo(length, -top_sPnts[1][1])
        .threePointArc(top_sPnts_m[0], top_sPnts_m[1])
        .lineTo(base_height+2, -1*(width/2 + middle_width_inset))
        .threePointArc(mid_sPnts_m[0], mid_sPnts_m[1])
        .lineTo(base_height, -1*(width/2 -2))
        .threePointArc(base_sPnts_m[0], base_sPnts_m[1])
        .lineTo(0, -1*(width/2))
        .close()
    )
    
    #result = cq.Face.makeFromWires(result_wires.val())
    #show_object(cq.Shape(sf.Shape()))
    return result_wires

#-------------------------

class ShieldShape(Base):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.length = 20
        self.width = 20
        self.base_height = 4
        self.middle_width_inset = -6
        self.shape_method = shield_shape_mirror
        
        # shapes
        self.shape=None
        
    def _make_shape(self):
        self.shape = self.shape_method(
            length = self.length,
            width = self.width,
            base_height = self.base_height,
            middle_width_inset = self.middle_width_inset,
        )
        
    def make(self, parent=None):
        super().make(parent)
        self._make_shape()
        
    def build(self):
        super().build()
        return self.shape