import cadquery as cq
from cqportal.portal import CoffinTextured

bp_coffin = CoffinTextured()
bp_coffin.seed = 'rough'
bp_coffin.passes_count = 36
bp_coffin.make()

coffin = bp_coffin.build()

#show_object(coffin)

cq.exporters.export(coffin, "stl/portal_coffin_textured.stl")