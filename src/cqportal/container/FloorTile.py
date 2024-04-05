import cadquery as cq
import math
from . import Floor

def make_basic_tile(length, width, height):
    tile = cq.Workplane("XY").box(
        length, 
        width, 
        height
    )
    return tile

class FloorTile(Floor):
    def __init__(self):
        super().__init__()

        self.tile_length = 10
        self.tile_width = 10
        self.tile_padding = 1
        self.make_tile_method = make_basic_tile
        
    def _make_floor(self):
        if not self.make_tile_method:
            raise Exception("Missing make_tile_method callback")
        else:
            tile = self.make_tile_method(self.tile_length, self.tile_width, self.height)
        
        tile_length = self.tile_length + self.tile_padding * 2
        tile_width = self.tile_width + self.tile_padding * 2
        
        x_count = math.floor(self.length / tile_length)
        y_count = math.floor(self.width / tile_width)

        def add_tile(loc):
            return tile.val().located(loc)
        
        result = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = tile_length, 
                ySpacing = tile_width,
                xCount = x_count, 
                yCount= y_count, 
                center = True)
            .eachpoint(callback = add_tile)
        )
        
        floor = cq.Workplane("XY").box(self.length, self.width, self.height)
        self.floor = result

    def make(self, parent=None):
        super().make(parent)
    
    def build(self):
        return super().build()