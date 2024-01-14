import cadquery as cq
from cqportal import Portal

bp_portal = Portal()
bp_portal.make()

result = bp_portal.build()
cq.exporters.export(result, 'stl/portal.stl')