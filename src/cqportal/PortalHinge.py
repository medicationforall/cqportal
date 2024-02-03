import cadquery as cq
from cadqueryhelper import Hinge

class PortalHinge(Hinge):
    def __init__(self):
        super().__init__()
        self.ramp_bottom_margin = 0
        
        #shapes
        self.ramp_hinge_cut = None
        
    def _calculate_hinge_cut_length(self):
        return self.parent.base_length - self.parent.side_inset + 10
        
    def _calculate_hinge_cut_width(self):
        return (self.radius+2) + self.plate_spacer +1
    
    def _calculate_hinge_cut_height(self):
        return self.parent.width /2
        
    def __make_ramp_hinge_cut(self):
        length = self._calculate_hinge_cut_length()
        width = self._calculate_hinge_cut_width()
        height = self._calculate_hinge_cut_height()
        cut_box = cq.Workplane("XY").box(length,width,height)
        
        ramp_z = height/2 - self.radius
        self.ramp_hinge_cut = cut_box.translate((0,0,ramp_z))
    
    def make(self, parent=None):
        super().make(parent)
        self.__make_ramp_hinge_cut()
        
    def __build_ramp(self):
        ramp_y = -(self.parent.height/2 -self.radius - self.plate_spacer)-self.ramp_bottom_margin
        ramp_z = (self.parent.width / 2) - self.radius
        
        ramp = (
            self.parent.build()
            .rotate((1,0,0),(0,0,0), -90)
            .translate((0,ramp_y,ramp_z))
        )
        
        return ramp
        
    def build(self):
        hinge = super().build()
        ramp = self.__build_ramp()
        ramp_w_cut = (
            cq.Workplane("XY")
            .add(ramp)
            .cut(self.ramp_hinge_cut)
        )
        scene = (
            cq.Workplane("XY")
            .add(ramp_w_cut.rotate((1,0,0),(0,0,0), -self.rotate_deg))
            .add(hinge.rotate((0,0,1),(0,0,0), 180))
        )
        
        return scene