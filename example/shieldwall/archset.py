import cadquery as cq
from cqportal.shieldwall import ArchSet

arch_set_bp = ArchSet()
arch_set_bp.make()
arch_set = arch_set_bp.build()

#show_object(arch_set)
cq.exporters.export(arch_set, 'stl/shieldwall_arch_set.stl')
