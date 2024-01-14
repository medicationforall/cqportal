import cadquery as cq
from cqportal import Portal

bp_portal = Portal()
bp_portal.bp_frame.length = 150
bp_portal.bp_frame.width = 30
bp_portal.bp_frame.height = 150

bp_portal.render_ramps = True
bp_portal.ramp_push = 0
bp_portal.bp_ramp.width = 10
bp_portal.make()

result_closed = bp_portal.build_closed()
#show_object(result_closed.translate((-170,0,0)))

result_open = bp_portal.build_open()
#show_object(result_open)

cq.exporters.export(result_closed, 'stl/portal_closed.stl')
cq.exporters.export(result_open, 'stl/portal_open.stl')