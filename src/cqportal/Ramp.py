# Copyright 2024 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cadquery as cq
from cadqueryhelper import Base, shape

class Ramp(Base):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.length = 150
        self.width = 10
        self.height = 150
        self.top_length = 90
        self.base_length = 100
        self.base_offset = 35 # offset distance from the center of the ramp
        self.side_inset = 8
        self.frame_size = 10
        self.render_outside = True
        self.render_inside = True
        self.inside_margin = 0.4
        
        # shapes
        self.ramp = None
        self.inside = None
        self.outside = None
        
    def _calculate_mid_offset(self):
        mid_offset = -1*(self.height/2) + self.base_offset
        return mid_offset
    
    def _calculate_inside_length(self):
        return self.length -(self.frame_size*2) - self.side_inset - self.inside_margin*2
    
    def _calculate_inside_height(self):
        return self.height -(self.frame_size*2) - self.side_inset/2 - self.inside_margin*2
    
    def _calculate_inside_top_length(self):
        return self.top_length-self.frame_size - self.side_inset - self.inside_margin
    
    def _calculate_inside_base_length(self):
        return self.base_length-(self.frame_size/2) - self.side_inset/2 - self.inside_margin
    
    def _calculate_max_inside_length(self):
        length = self._calculate_inside_length()
        top_length = self._calculate_inside_top_length()
        base_length = self._calculate_inside_base_length()
        if top_length > length:
            length = top_length
            
        if base_length > length:
            length = base_length
        return length
        
    
    def _make_outside(self):
        mid_offset = self._calculate_mid_offset()
        
        side_inset = self.side_inset
        frame_size = self.frame_size/2
        outside = shape.coffin(
            self.length - side_inset - frame_size,
            self.height - (side_inset/2) - frame_size,
            self.width/2,
            top_length = self.top_length - side_inset - frame_size,
            base_length = self.base_length - side_inset - frame_size,
            mid_offset = mid_offset + (side_inset/4) + frame_size/2
        ).rotate((1,0,0),(0,0,0),-90)
        
        outside = outside.translate((0,0,-1*(side_inset/4+frame_size/2)))
        self.outside = outside
    
    def _make_inside(self):
        mid_offset = self._calculate_mid_offset()
        inside = shape.coffin(
            self._calculate_inside_length(),
            self._calculate_inside_height(),
            self.width/2,
            top_length = self._calculate_inside_top_length(),
            base_length = self._calculate_inside_base_length(),
            mid_offset = mid_offset  + self.side_inset /4
        ).rotate((1,0,0),(0,0,0),-90)
        inside = inside.translate((0,0,-1*(self.side_inset/4)))
        self.inside = inside
    
    def _make_ramp(self):
        
        ramp = (
            cq.Workplane("XY")
        )
        
        if self.render_outside:
            ramp = ramp.add(self.outside)
        
        if self.render_inside:
            ramp = ramp.add(self.inside.translate((0,(self.width/2),0)))
        
        self.ramp = (ramp).translate((0,-1*(self.width/4),0))
        
    def make(self, parent=None):
        super().make(parent)
        
        if self.parent:
            self.parent.make()

            self.length = self.parent.length
            self.height = self.parent.height
            self.top_length = self.parent.top_length
            self.base_length = self.parent.base_length
            self.base_offset = self.parent.base_offset
            self.frame_size = self.parent.frame_size
            self.side_inset = self.parent.side_inset
            
        if self.render_outside:
            self._make_outside()
            
        if self.render_inside:
            self._make_inside()
            
        self._make_ramp()
        
    def build(self):
        super().build()
        
        scene = (
            cq.Workplane("XY")
            .union(self.ramp)
        )
        
        return scene