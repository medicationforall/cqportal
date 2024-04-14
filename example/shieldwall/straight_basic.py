import cadquery as cq
from cqportal.shieldwall import StraightBasic

wall_bp = StraightBasic()
#wall_bp.length = 100
#wall_bp.width = 50
#wall_bp.height = 10
wall_bp.render_magnets = True
wall_bp.make()
wall_ex = wall_bp.build()

#show_object(wall_ex)
cq.exporters.export(wall_ex, 'stl/shieldwall_straightbasic.stl')