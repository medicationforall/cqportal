import cadquery as cq
from cadqueryhelper import Base, shape
from cqportal.portal import RampGreebled

bp_ramp = RampGreebled()
#bp_ramp.length = 70
#bp_ramp.width = 10
#bp_ramp.height = 150
#bp_ramp.top_length = 60
bp_ramp.base_length = 80

bp_ramp.segment_padding = 0
bp_ramp.render_center = True
bp_ramp.render_inside_outline = False
bp_ramp.make()
ex_ramp = bp_ramp.build()

#show_object(ex_ramp)
cq.exporters.export(ex_ramp, 'stl/ramp_greebled.stl')