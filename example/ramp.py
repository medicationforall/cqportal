import cadquery as cq
from cqportal import Ramp

bp_ramp = Ramp()
bp_ramp.width = 10
bp_ramp.side_inset = 10
bp_ramp.make()

result = bp_ramp.build()

#show_object(result)
cq.exporters.export(result, 'stl/ramp.stl')