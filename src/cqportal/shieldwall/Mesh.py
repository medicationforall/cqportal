import cadquery as cq
from cadqueryhelper import Base
import math

class Mesh(Base):
    def __init__(self):
        super().__init__()
        #propetries
        self.length = 75
        self.width = 3
        self.height = 25
        
        self.tile_length = 5
        self.tile_width = 5
        self.tile_padding = 0.2
        self.tile_chamfer = 1.4
        
        #shapes
        self.tile=None
        self.tiles = None
        self.outline = None
        
    def __make_outline(self):
        self.outline = (
            cq.Workplane('XY')
            .box(self.length,self.height, self.width/2)
        )
        
    def _make_tile(self):
        self.tile = (
            cq.Workplane('XY')
            .box(
                self.tile_length,
                self.tile_width,
                self.width/2
            )
            .faces("-Z")
            .chamfer(self.tile_chamfer)
        )
        
    def _make_tiles(self):
        tile_length = self.tile_length + self.tile_padding * 2
        tile_width = self.tile_width + self.tile_padding * 2
        
        x_count = math.floor(self.length / tile_length)
        y_count = math.floor(self.height / tile_width)
        
        #log(f'{y_count=}')
        
        def add_star(loc):
            return self.tile.val().located(loc)
        
        self.tiles = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = tile_length, 
                ySpacing = tile_width,
                xCount = x_count, 
                yCount= y_count, 
                center = True)
            .eachpoint(callback = add_star)
        )
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_outline()
        self._make_tile()
        self._make_tiles()
        
    def build(self):
        super().build()
        mesh = (
            cq.Workplane('XY')
            .union(self.outline)
            #.cut(self.tile)
            .cut(self.tiles)
        ).rotate((1,0,0),(0,0,0),-90).translate((0,-1*(self.width/4),0))
        
        scene = (
            cq.Workplane("XY")
            .union(mesh) #front
            .union(mesh.rotate((0,0,1),(0,0,0),180)) #back
        )

        return scene