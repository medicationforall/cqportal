from . import Straight, HexMesh

class HexStraight(Straight):
    def __init__(self):
        super().__init__()
        self.mesh_width = 4

        self.mesh_bp = HexMesh() 
        self.mesh_bp.tile_length =10
        self.mesh_bp.tile_width = 10
        self.mesh_bp.tile_padding = 0.0
        self.mesh_bp.tile_chamfer = 1
        
    def make(self, parent=None):
        super().make(parent)
        
    def build(self):
        return super().build()