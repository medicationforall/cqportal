import cadquery as cq
from cqportal.shieldwall import Mesh

mesh_bp = Mesh()
mesh_bp.make()
mesh_ex = mesh_bp.build()

#show_object(mesh_ex)
cq.exporters.export(mesh_ex, 'stl/shieldwall_mesh.stl')