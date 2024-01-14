import cadquery as cq
from cqportal import Portal

bp_portal = Portal()
bp_portal.bp_frame.length = 140
bp_portal.bp_frame.width = 30
bp_portal.bp_frame.height = 200

bp_portal.render_ramps = True
bp_portal.ramp_push = 0
bp_portal.bp_ramp.width = 10
bp_portal.make()

result = bp_portal.build_closed()
cq.exporters.export(result, 'stl/portal.stl')