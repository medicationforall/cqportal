import cadquery as cq
from cqportal.shieldwall import GothicMesh

gothic_bp = GothicMesh()
gothic_bp.make()
gothic_ex = gothic_bp.build()

#show_object(gothic_ex)
cq.exporters.export(gothic_ex, 'stl/shieldwall_gothicMesh.stl')