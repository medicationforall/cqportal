import cadquery as cq
from cqportal.shieldwall import HexSet

hex_set_bp = HexSet()
hex_set_bp.base_height = 5
hex_set_bp.make()
hex_set = hex_set_bp.build()

#show_object(hex_set)
cq.exporters.export(hex_set, 'stl/shieldwall_hex_set.stl')