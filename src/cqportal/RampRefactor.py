import cadquery as cq
from cadqueryhelper import Base, shape
from . import BaseCoffin

class RampRefactor(Base):
    def __init__(self):
        super().__init__()
        self.length = 150
        self.width = 10
        self.height = 150
        self.top_length = 90
        self.base_length = 100
        self.base_offset = 35 # offset distance from the base of the ramp

        self.side_inset = 8
        self.frame_size = 10
        self.inside_margin = 0.4

        self.render_outside = True
        self.render_inside = True
        
        # Blueprints
        self.bp_outside = BaseCoffin()
        self.bp_inside = BaseCoffin()
        
    def __calculate_mid_offset(self):
        mid_offset = -1*(self.height/2) + self.base_offset
        return mid_offset 

    def __calculate_outside_length(self):
        return self.length - self.side_inset - (self.frame_size/2)
    
    def __calculate_outside_height(self):
        return self.height - (self.side_inset/2) - (self.frame_size/2)
    
    def __calculate_outside_top_length(self):
        return self.top_length - self.side_inset - (self.frame_size/2)
    
    def __calculate_outside_base_length(self):
        return self.base_length - self.side_inset - (self.frame_size/2)

    def __calculate_inside_length(self):
        return self.length -(self.frame_size*2) - self.side_inset - self.inside_margin*2
    
    def __calculate_inside_height(self):
        return self.height -(self.frame_size*2) - self.side_inset/2 - self.inside_margin*2
    
    def __calculate_inside_top_length(self):
        return self.top_length - self.frame_size - self.side_inset - self.inside_margin
    
    def __calculate_inside_base_length(self):
        return self.base_length - self.frame_size - self.side_inset - self.inside_margin
    
    def __make_inside(self):
        self.bp_outside.length = self.__calculate_outside_length()
        self.bp_outside.width = self.width / 2
        self.bp_outside.height = self.__calculate_outside_height()
        self.bp_outside.top_length = self.__calculate_outside_top_length()
        self.bp_outside.base_length = self.__calculate_outside_base_length()
        self.bp_outside.base_offset = self.base_offset # offset distance from the center of the ramp
        self.bp_outside.make(self)
        
    def __make_outside(self):
        self.bp_inside.length = self.__calculate_inside_length()
        self.bp_inside.width = self.width / 2
        self.bp_inside.height = self.__calculate_inside_height()
        self.bp_inside.top_length = self.__calculate_inside_top_length()
        self.bp_inside.base_length = self.__calculate_inside_base_length()
        
        height_diff = (self.height - self.__calculate_inside_height())/2
        self.bp_inside.base_offset = self.base_offset -height_diff + self.side_inset /4
        self.bp_inside.make(self)
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_inside()
        self.__make_outside()

    def build(self):
        super().build()
        outside = self.bp_outside.build()
        inside = self.bp_inside.build()
        
        side_inset = self.side_inset
        frame_size = self.frame_size/2
        out_z = -1*(side_inset/4+frame_size/2)
        in_z = -1*(self.side_inset/4)

        ramp = (
            cq.Workplane("XY")
            .add(outside.translate((0,-self.width/4,out_z)))
            .add(inside.translate((0,self.width/4,in_z)))
        )
        return ramp