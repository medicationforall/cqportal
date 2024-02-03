import cadquery as cq
from . import Portal, RampGreebled, ContainerFrame

class Container(Portal):
    def __init__(self):
        super().__init__()
        self.render_base = False

        self.bp_frame = ContainerFrame()
        self.bp_frame.length = 75
        self.bp_frame.width = 140
        self.bp_frame.height = 75

        self.bp_frame.top_length = 50
        self.bp_frame.base_length = 50
        self.bp_frame.base_offset = 35
        self.bp_frame.side_inset = 4
        self.bp_frame.frame_size = 7

        self.bp_frame.render_sides = True

        self.bp_ramp = RampGreebled()
        self.bp_ramp.width = 8
        self.bp_ramp.segment_count = 10
        self.bp_ramp.segment_y_padding = 3
        self.bp_ramp.render_outside = True

        self.bp_hinge.rotate_deg = 0
        self.bp_hinge.ramp_bottom_margin = 0
        self.plate_spacer = .3

        self.bp_hinge.rotate_deg = 0
        
    def make(self, parent=None):
        super().make(parent)
        
    def build(self):
        container = super().build()
        scene = (
            cq.Workplane("XY")
            .add(container.translate((0,0,-self.bp_base.height - self.bp_frame.height/2)))
        )
        return scene