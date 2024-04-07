import cadquery as cq
import math
from . import Mesh

class HexMesh(Mesh):
    def __init__(self):
        super().__init__()
        
    def _make_tile(self):
        tile = (
            cq.Workplane('XY')
            .polygon(6, self.tile_length)
        ).extrude(self.width/2).translate((0,0,-1*(self.width/4)))
        
        self.tile = tile.faces("-Z").chamfer(self.tile_chamfer)
        
    def _make_tiles(self):
        #log('_make_tiles')
        tile_length = self.tile_length - self.tile_padding
        tile_width = self.tile_length + self.tile_padding * 2
        
        x_count = math.floor(self.length / tile_length)
        y_count = math.floor(self.height / tile_width)+2
        
        #log(f'{y_count=}')
        cell_count = 0
        column_count = 0
        def add_star(loc):
            nonlocal cell_count
            nonlocal column_count
            
            location = loc.toTuple()
            new_loc = location[0]
            
            if cell_count % y_count == 0:
                column_count+=1
                
            if column_count % 2 == 0:
                # log('even column')
                pass
            else:
                # log('odd column')
                new_loc = (location[0][0], location[0][1]+self.tile_length/2, location[0][2])
                
            cell_count+=1
            
            #if cell_count >13:
            #    new_loc = (0,0,0)
            return self.tile.translate(new_loc).val()
        
        tiles = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = tile_length, 
                ySpacing = tile_width,
                xCount = x_count, 
                yCount= y_count, 
                center = True)
            .eachpoint(callback = add_star)
        )
        
        self.tiles = tiles.intersect(self.outline)
        
    def build(self):
        #super().build()
        mesh = (
            cq.Workplane('XY')
            .union(self.outline)
            #.add(self.tile)
            .cut(self.tiles)
        ).rotate((1,0,0),(0,0,0),-90).translate((0,-1*(self.width/4),0))
        
        scene = (
            cq.Workplane("XY")
            .union(mesh)
            .union(
                mesh
                .rotate((0,0,1),(0,0,0),180)
                .rotate((0,1,0),(0,0,0),180)
            )
        )

        return scene