import cadquery as cq
from cqportal.shieldwall import CornerConnector

corner_bp = CornerConnector()
#corner_bp.height = 50
corner_bp.make()
corner_ex = corner_bp.build()
corner_ex_assembly = corner_bp.build_assembly()

#show_object(corner_ex)
cq.exporters.export(corner_ex, 'stl/shieldwall_corner_connector.stl')
corner_ex_assembly.save("gltf/shieldwall_corner_connector.gltf")