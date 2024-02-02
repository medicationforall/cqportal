import cadquery as cq
from cqportal import Portal, RampGreebled, FrameWindow

bp_portal = Portal()

bp_portal.bp_frame = FrameWindow()
bp_portal.bp_frame.length = 200
bp_portal.bp_frame.width = 30
bp_portal.bp_frame.height = 200
bp_portal.bp_frame.top_length = 40
bp_portal.bp_frame.base_length = 100

bp_portal.bp_ramp = RampGreebled()
bp_portal.bp_ramp.segment_count = 25

bp_portal.render_base = False
bp_portal.render_ramps = True
bp_portal.ramp_push = 0
bp_portal.bp_ramp.width = 10
bp_portal.make()

result_closed = bp_portal.build_closed()
#show_object(result_closed.translate((-1*(bp_portal.bp_frame.length+20),0,0)))
cq.exporters.export(result_closed, 'stl/portal_greebled_ramp_closed.stl')

result_open = bp_portal.build_open()
#show_object(result_open)
cq.exporters.export(result_open, 'stl/portal_greebled_ramp_open.stl')