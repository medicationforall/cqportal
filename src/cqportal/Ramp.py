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
        
    def _calculate_mid_offset(self):
        mid_offset = -1*(self.height/2) + self.base_offset
        return mid_offset
    
    def make_outside(self):
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
        
        return outside
    
    def make_inside(self):
        mid_offset = self._calculate_mid_offset()
        inside = shape.coffin(
            self.length-(self.frame_size*2) - self.side_inset - self.inside_margin*2,
            self.height-(self.frame_size*2) - self.side_inset/2 - self.inside_margin*2,
            self.width/2,
            top_length = self.top_length-self.frame_size - self.side_inset - self.inside_margin,
            base_length = self.base_length-(self.frame_size/2) - self.side_inset/2 - self.inside_margin,
            mid_offset = mid_offset  + self.side_inset /4
        ).rotate((1,0,0),(0,0,0),-90)
        inside = inside.translate((0,0,-1*(self.side_inset/4)))
            
        return inside
    
    def _make_ramp(self):
        
        ramp = (
            cq.Workplane("XY")
        )
        
        if self.render_outside:
            outside = self.make_outside()
            ramp = ramp.add(outside)
        
        if self.render_inside:
            inside = self.make_inside()
            ramp = ramp.add(inside.translate((0,(self.width/2),0)))
        
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
        self._make_ramp()
        
    def build(self):
        super().build()
        
        scene = (
            cq.Workplane("XY")
            .union(self.ramp)
        )
        
        return scene