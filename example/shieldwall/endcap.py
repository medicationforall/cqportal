import cadquery as cq
from cqportal.shieldwall import EndCap

cap_bp =  EndCap()
cap_bp.make()
cap_ex = cap_bp.build()

#show_object(cap_ex)
cq.exporters.export(cap_ex, 'stl/endcap.stl')