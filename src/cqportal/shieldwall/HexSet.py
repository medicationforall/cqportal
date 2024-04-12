from . import Set, HexMesh

class HexSet(Set):
    def __init__(self):
        super().__init__()
        
        self.mesh_bp = HexMesh()
        self.mesh_bp.tile_length =10
        self.mesh_bp.tile_width = 10
        self.mesh_bp.tile_padding = 0.0
        self.mesh_bp.tile_chamfer = 1