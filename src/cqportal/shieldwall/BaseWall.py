import cadquery as cq
from cadqueryhelper import Base
from . import BaseShape, BaseMesh, BaseMagnets, BaseCut, ShieldShape, Mesh, Magnets

class BaseWall(Base):
    '''
    Psuedo Interface defines the minimal properties available for anything that inherits off of BaseStraight.
    '''

    def __init__(self):
        super().__init__()
        #properties
        self.length:float = 75
        self.height:float = 25
        self.width:float = 20
        self.height:float = 25

        self.base_height:float = 5.6
        self.magnet_padding_x:float = 2
        self.mesh_width: float = 6
        self.render_greeble: bool = True

        #blueprints
        self.shape_bp:BaseShape = BaseShape()
        self.mesh_bp:BaseMesh = BaseMesh()
        self.magnets_bp:BaseMagnets = BaseMagnets()
        self.base_cut_bp:BaseCut = BaseCut()
        

    def build(self) -> cq.Workplane:
        super().build()
        scene = (
            cq.Workplane("XY")
        )
        return scene