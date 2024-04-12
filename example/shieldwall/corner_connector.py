import cadquery as cq
from cqportal.shieldwall import CornerConnector

corner_bp = CornerConnector()
corner_bp.height = 50
corner_bp.make()
corner_ex = corner_bp.build()

#show_object(corner_ex)
cq.exporters.export(corner_ex, 'stl/corner_connector_2.stl')