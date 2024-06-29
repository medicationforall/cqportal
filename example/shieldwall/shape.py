import cadquery as cq
from cqportal.shieldwall import  ShieldShape

shape_bp = ShieldShape()
shape_bp.make()

shape_ex = shape_bp.build().extrude(2)
#show_object(shape_ex)

cq.exporters.export(shape_ex, 'stl/shieldwall_shape.stl')