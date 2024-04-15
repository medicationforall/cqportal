import cadquery as cq
from cadqueryhelper import Base
from . import ShieldShape, CapGreeble, Magnets

class CornerConnector(Base):
    def __init__(self):
        super().__init__()
        #properties
        self.length=20
        self.width=20
        self.height=25
        
        self.base_height = 5.6
        
        self.render_magnets = True
        self.magnet_padding = 1
        self.magnet_padding_x=2
        
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
        self.magnets_bp = Magnets()
        
        #shapes
        self.shape = None
        self.connector = None
        
        self.end_cap = None
        self.greeble = None
        
        
    def __make_wall_shape(self):
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
            
        )
        
        self.shape = shape.rotate((0,1,0),(0,0,0),90)
        
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
        
    def __make_corner(self):
        corner = (
            cq.Workplane("XY")
            .union(self.end_cap)
            .union(self.end_cap.rotate((0,0,1),(0,0,0),90))
        )
        self.corner = corner

        
    def __make_connector(self):
        connector = (
            cq.Workplane("XY")
            .add(self.shape)
            .add(self.shape.rotate((0,0,1),(0,0,0),90))
        )
        self.connector = connector
        
    def __make_greeble(self):
        self.greeble_bp.length = self.length - self.cut_width*2 +-1.5-2.5
        self.greeble_bp.width = self.width + self.middle_width_inset*2 - self.greeble_padding_y*2
        self.greeble_bp.height = self.height - self.base_height - self.side_height - self.top_height
        self.greeble_bp.make()
        
    def __make_magnets(self):
        self.magnets_bp.distance = self.width - self.magnets_bp.pip_radius*2 - self.magnet_padding*2 - self.magnet_padding_x
        self.magnets_bp.make()
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_wall_shape()

        self.__make_connector()
        self.__make_corner()
        self.__make_magnets()
        
        if self.render_greeble:
            self.__make_greeble()
        
    def build_connector(self):
        return self.connector
    
    def build_magnets(self):
       magnets = self.magnets_bp.build()
       magnet_x = self.length/2 - self.magnets_bp.pip_height/2
       magnet_z = -(self.height/2) + self.base_height - self.magnets_bp.pip_radius - self.magnet_padding
       scene = (
           cq.Workplane("XY")
           .union(magnets.rotate((0,0,1),(0,0,0),90).translate((0,magnet_x,magnet_z)))
           .union(magnets.translate((-magnet_x,0,magnet_z)))
       )
       return scene
        
    def build(self):
        super().build()

        scene = (
            cq.Workplane("XY")
            .add(self.corner)
        )
        
        if self.render_greeble:
            greeble = self.greeble_bp.build()
            translate_x = self.length/2 - self.greeble_bp.length/2 - self.cut_width
            translate_z = self.base_height/2+ self.side_height/2 - self.top_height/2
            scene = (
                scene
                .union(greeble.translate((-translate_x,0,translate_z)))
                .union(greeble.rotate((0,0,1),(0,0,0),90).translate((0,translate_x,translate_z)))
            )
            
        if self.render_magnets:
            magnets = self.build_magnets()
            scene = scene.cut(magnets)
        return scene
        #return cq.Workplane("XY").box(self.length,self.width,self.height)
