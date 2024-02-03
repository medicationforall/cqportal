import cadquery as cq
from . import Portal, RampGreebled, ContainerFrame, Floor

class Container(Portal):
    def __init__(self):
        super().__init__()
        
        #params
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

        self.bp_hinge.rotate_deg = -90
        
        self.render_floor = True
        
        #blueprints
        self.bp_floor = Floor()
        
    def make(self, parent=None):
        super().make(parent)
        
        self.bp_floor.length = self.bp_frame.base_length - self.bp_frame.frame_size - self.bp_frame.side_inset
        self.bp_floor.width = self.bp_frame.width
        self.bp_floor.make()
        
    def build(self):
        container = super().build()
        scene = (
            cq.Workplane("XY")
            .add(container.translate((0,0,-self.bp_base.height - self.bp_frame.height/2)))
        )
        
        if self.render_floor:
            floor = self.bp_floor.build()
            floor_cut = self.bp_floor.floor_cut
            floor_z = self.bp_frame.height-(self.bp_frame.frame_size*2)+self.bp_floor.height
            
            
            scene =(
                scene
                .cut(floor_cut.translate((0,0,-floor_z/2)))
                .union(floor.translate((0,0,-floor_z/2)))
            )
        return scene