import cadquery as cq
from cqportal.portal import Portal, RampGreebledTwo, FrameWindowBlock, EnergyInsert

bp_portal = Portal()
bp_portal.bp_frame = FrameWindowBlock()
bp_portal.bp_frame.render_sides = True
bp_portal.bp_frame.seed = 'blocks3'#'block'
bp_portal.bp_frame.window_cut_width = 5.5

bp_portal.bp_frame.length = 150
bp_portal.bp_frame.width = 30
bp_portal.bp_frame.height = 150

bp_portal.bp_ramp = RampGreebledTwo()

bp_portal.render_base = False
bp_portal.render_hinges = True
bp_portal.bp_ramp.width = 10

if bp_portal.bp_hinge:
 bp_portal.bp_hinge.rotate_deg = -0

bp_portal.bp_iris = EnergyInsert()
bp_portal.make()

result_open = bp_portal.build()

#show_object(result_open)

cq.exporters.export(result_open,'stl/portal_frame_window_block.stl')