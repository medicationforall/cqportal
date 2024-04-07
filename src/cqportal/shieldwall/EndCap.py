import cadquery as cq
from cadqueryhelper import Base
from cqportal.shieldwall import ShieldShape

class EndCap(Base):
    def __init__(self):
        super().__init__()
        #properties
        self.length = 25
        self.width = 20
        self.height = 25
        
        self.cut_width = 16
        
        self.render_greeble = False
        
        #blueprints
        self.shape_bp =  ShieldShape()
        
        #shapes
        self.end_cap = None
        self.greeble = None
        
    def __make_end_cap(self):
        self.shape_bp.length = self.height
        self.shape_bp.width = self.width
        self.shape_bp.make()
        
        self.shape_bp.width = self.height
        
        shape = (
            self.shape_bp
            .build()
            .extrude(self.length)
            .translate((0,0,-1*self.length/2))
            #.rotate((0,1,0),(0,0,0),90)
        )
        
        self.shape_bp.width = self.width*2
        self.shape_bp.base_height += 5
        self.shape_bp.middle_width_inset = -self.cut_width 
        self.shape_bp.length += 4
        self.shape_bp.make()
        cut_shape = (
            self.shape_bp
            .build()
            .extrude(self.length)
            .translate((0,0,-1*self.length/2))
            .rotate((0,1,0),(0,0,0),90)
            .rotate((0,0,1),(0,0,0),90)
            .translate((-1*(self.length/2),0,-2))
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
            #.union(shape)
            .union(shape.rotate((0,1,0),(0,0,0),90))
            .cut(silhouette.cut(cut_shape))
        )
        
        #self.end_cap = silhouette.add(cut_shape)
        
    def __make_geeble(self):
        self.greeble = cq.Workplane("XY").box(10,10,10)
        
    def make(self, parent=None):
        super().make()
        self.__make_end_cap()
        
        if self.render_greeble:
            self.__make_geeble()
        
    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.end_cap)
        )
        
        if self.render_greeble:
            scene = scene.union(self.greeble)
        return scene