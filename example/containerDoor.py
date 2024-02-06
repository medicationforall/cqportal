import cadquery as cq
from cqportal import ContainerDoor

bp_door = ContainerDoor()
bp_door.cut_depth = 2
bp_door.padding = 3
bp_door.frame_width = 2
bp_door.x_translate = 0
bp_door.make()
door = bp_door.build()

#show_object(door)
cq.exporters.export(door, 'stl/container_door.stl')