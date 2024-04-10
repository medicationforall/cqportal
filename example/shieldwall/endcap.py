import cadquery as cq
from cqportal.shieldwall import EndCap

cap_bp =  EndCap()
cap_bp.length = 15
cap_bp.height = 50
cap_bp.base_height = 4
cap_bp.side_height = 1
cap_bp.middle_width_inset = -6

#cap_bp.greeble_bp.operation = 'fillet'
cap_bp.greeble_bp.operation = 'chamfer'
cap_bp.greeble_bp.render_grill = True
cap_bp.make()
cap_ex = cap_bp.build()

#show_object(cap_ex)
cq.exporters.export(cap_ex, 'stl/endcap.stl')