import cadquery as cq
from cadqueryhelper import Base
from cqportal.shieldwall import ShieldShape, CapGreeble

class EndCap(Base):
    def __init__(self):
        super().__init__()
        #properties
        self.length = 25
        self.width = 20
        self.height = 25
        self.base_height = 4
        self.side_margin = -2
        self.side_height = 1
        self.top_height = 2
        
        self.cut_width = 3
        self.middle_width_inset = -6
        
        self.render_greeble = True
        self.greeble_padding_y = 1
        
        #blueprints
        self.shape_bp = ShieldShape()
        self.greeble_bp = CapGreeble()
        
        #shapes
        self.end_cap = None
        self.greeble = None
        
    def __make_end_cap(self):
        self.shape_bp.length = self.height
        self.shape_bp.width = self.width
        self.shape_bp.base_height = self.base_height
        self.shape_bp.middle_width_inset = self.middle_width_inset
        
        self.shape_bp.make()
        
        self.shape_bp.width = self.height
        
        shape = (
            self.shape_bp
            .build()
            .extrude(self.length)
            .translate((0,0,-1*self.length/2))
            #.rotate((0,1,0),(0,0,0),90)
        )
        
        self.shape_bp.width = self.length*2
        self.shape_bp.base_height += self.base_height + self.side_height
        self.shape_bp.middle_width_inset = -self.length+self.cut_width
        self.shape_bp.length += 4
        self.shape_bp.make()
        cut_shape = (
            self.shape_bp
            .build()
            .extrude(self.width)
            .translate((0,0,-1*self.width/2))
            .rotate((0,1,0),(0,0,0),90)
            .rotate((0,0,1),(0,0,0),90)
            .translate((-1*(self.length/2),0,self.side_margin))
        )
        
        silhouette = (
            cq.Workplane("XY").box(
                self.length,
                self.width,
                self.height
            )
        )
        
        self.end_cap = (
            cq.Workplane('XY')
            .union(shape.rotate((0,1,0),(0,0,0),90))
            #.add(cut_shape)
            .cut(silhouette.cut(cut_shape))#)
        )
        
    def __make_greeble(self):
        self.greeble_bp.length = self.length - self.cut_width*2 +-1.5
        self.greeble_bp.width = self.width + self.middle_width_inset*2 - self.greeble_padding_y*2
        self.greeble_bp.height = self.height - self.base_height - self.side_height - self.top_height
        self.greeble_bp.make()
        
    def make(self, parent=None):
        super().make()
        self.__make_end_cap()
        
        if self.render_greeble:
            self.__make_greeble()
        
    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.end_cap)
        )
        
        if self.render_greeble:
            greeble = self.greeble_bp.build()
            translate_x = self.length/2 - self.greeble_bp.length/2 - self.cut_width
            translate_z = self.base_height/2+ self.side_height/2 - self.top_height/2
            scene = scene.add(greeble.translate((-translate_x,0,translate_z)))
        return scene