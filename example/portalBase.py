import cadquery as cq
from cqportal import PortalBase

bp_portal_base = PortalBase()
bp_portal_base.make()

result = bp_portal_base.build()

#show_object(result)
cq.exporters.export(result, 'stl/portalBase.stl')