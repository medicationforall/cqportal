from . import Set, ArchShape, HexMesh

class ArchSet(Set):
    def __init__(self):
        super().__init__()
        
        #blueprints
        self.shape_bp = ArchShape()
        
        self.mesh_bp = HexMesh()
        self.mesh_bp.tile_length =10
        self.mesh_bp.tile_width = 10
        self.mesh_bp.tile_padding = 0.0
        self.mesh_bp.tile_chamfer = 1