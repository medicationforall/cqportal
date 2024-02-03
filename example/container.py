import cadquery as cq
from cqportal import Container

bp_portal = Container()

bp_portal.make()

result = bp_portal.build()
#show_object(result)
cq.exporters.export(result, 'stl/container.stl')