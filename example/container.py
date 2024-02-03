import cadquery as cq
from cqportal import Container

bp_container = Container()
bp_container.bp_hinge.rotate_deg = -90

bp_container.make()

result = bp_container.build()
#show_object(result)
cq.exporters.export(result, 'stl/container.stl')