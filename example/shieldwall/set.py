import cadquery as cq
from cqportal.shieldwall import Set

set_bp = Set()
set_bp.make()
set_ex = set_bp.build()

#show_object(set_ex)
cq.exporters.export(set_ex, 'stl/shieldwall_set.stl')