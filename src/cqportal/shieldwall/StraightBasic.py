import cadquery as cq
from cadqueryhelper import Base
from . import ShieldShape, Magnets

class StraightBasic(Base):
    def __init__(self):
        super().__init__()

        #properties
        self.length = 75
        self.width = 20
        self.height = 20
        self.base_height = 5.6

        self.magnet_padding = 1
        self.render_magnets = True
        self.magnet_padding_x=2

        # blueprints
        self.shape_bp = ShieldShape()
        self.magnets_bp = Magnets()

        #shape
        self.wall = None
        
    def __make_shape(self, parent=None):
        self.shape_bp.length = self.height
        self.shape_bp.width = self.width
        self.shape_bp.base_height = self.base_height
        self.shape_bp.make(parent)
        

    def __make_wall_basic(self):
        shape = self.shape_bp.shape
        base_wall = (
            shape
            .extrude(self.length)
            .translate((0,0,-1*(self.length/2)))
            .rotate((0,1,0),(0,0,0),90)
        )
        self.wall = base_wall
        
    def __make_magnets(self):
        self.magnets_bp.distance = self.width - self.magnets_bp.pip_radius*2 - self.magnet_padding*2 - self.magnet_padding_x
        self.magnets_bp.make()
        
    def make(self, parent=None):
        super().make(parent)

        self.__make_shape(parent)
        self.__make_wall_basic()
        self.__make_magnets()
        
    def build(self):
        super().build()
        magnets = self.magnets_bp.build()
        magnet_x = self.length/2 - self.magnets_bp.pip_height/2
        magnet_z = -(self.height/2) + self.base_height - self.magnets_bp.pip_radius - self.magnet_padding
        scene =(
            cq.Workplane("XY")
            .union(self.wall)

        )
        
        if self.render_magnets:
            scene = (
                scene
                .cut(magnets.translate((magnet_x,0,magnet_z)))
                .cut(magnets.translate((-magnet_x,0,magnet_z)))
            )
        return scene