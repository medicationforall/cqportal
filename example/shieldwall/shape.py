import cadquery as cq
from cqportal import shieldwall

shape_bp = shieldwall.ShieldShape()
shape_bp.make()

shape_ex = shape_bp.build().extrude(2)
#show_object(shape_ex)

cq.exporters.export(shape_ex, 'stl/shieldwallshape.stl')