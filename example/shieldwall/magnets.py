import cadquery as cq
from cqportal.shieldwall import Magnets

magnet_bp = Magnets()
magnet_bp.make()
magnet_ex = magnet_bp.build()

#show_object(magnet_ex)
cq.exporters.export(magnet_ex,'stl/shieldwall_magnets.stl')