import cadquery as cq
from cqportal import Frame

bp_frame = Frame()
bp_frame.top_length = 90
bp_frame.base_length = 100
bp_frame.base_offset = 35
bp_frame.make()

result = bp_frame.build()

#show_object(result)
cq.exporters.export(result, 'stl/frame.stl')