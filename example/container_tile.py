import cadquery as cq
from cqportal import FloorTile, Container
from cqterrain import tile as terrain_tile

#----------------------

def make_custom_tile(length, width, height):
    # https://github.com/medicationforall/cqterrain/blob/main/documentation/tile.md
    return terrain_tile.carton2(
        length, 
        width, 
        height,
        x_divisor = 2,
        y_divisor = 3.58
    )

bp_container = Container()

bp_container.bp_floor = FloorTile()

bp_container.bp_floor.height=2
bp_container.bp_floor.tile_length = 17
bp_container.bp_floor.tile_width = 17
bp_container.bp_floor.tile_padding = 0
bp_container.bp_floor.make_tile_method = make_custom_tile

bp_container.bp_hinge.rotate_deg = -90
bp_container.make()

result = bp_container.build()

#show_object(result)

cq.exporters.export(result, 'stl/container_tile.stl')