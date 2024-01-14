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
        self.base_offset = 35
        self.side_inset = 8
        self.render_center = True
        
        # shapes
        self.ramp = None
        
    def _calculate_mid_offset(self):
        if self.parent:
            mid_offset = -1*(self.parent.height/2) + self.parent.base_offset
        else:
            mid_offset = -1*(self.height/2) + self.base_offset
        return mid_offset
    
    def make_center(self):
        mid_offset = self._calculate_mid_offset()
        
        if self.parent:
            side_inset = self.parent.side_inset
            frame_size = self.parent.frame_size/2
            center = shape.coffin(
                self.parent.length - side_inset - frame_size,
                self.parent.height - (side_inset/2) - frame_size,
                self.width/2,
                top_length = self.parent.top_length - side_inset - frame_size,
                base_length = self.parent.base_length - side_inset - frame_size,
                mid_offset = mid_offset + (side_inset/4) + frame_size/2
            ).rotate((1,0,0),(0,0,0),-90)
            
            center = center.translate((0,0,-1*(side_inset/4+frame_size/2)))
        else:
            mid_offset = self._calculate_mid_offset()
            center = shape.coffin(
                self.length,
                self.height,
                self.width/2,
                top_length = self.top_length,
                base_length = self.base_length,
                mid_offset = mid_offset
            ).rotate((1,0,0),(0,0,0),-90)
        
        return center
    
    def _make_ramp(self):
        if self.render_center:
            center = self.make_center()
        
        if self.parent:
            self.length = self.parent.length
            self.height = self.parent.height
            self.top_length = self.parent.top_length
            self.base_length = self.parent.base_length
            self.base_offset = self.parent.base_offset
            self.side_inset = self.parent.side_inset
        
        if self.parent:
            side = self.parent.make_side_cut(width = self.width/2, margin=0.4)
            side = side.translate((0,0,-1*(self.parent.side_inset/4)))
        else:
            mid_offset = self._calculate_mid_offset()
            side = shape.coffin(
                self.length - (self.side_inset),
                self.height - self.side_inset,
                self.width/2,
                top_length = self.top_length - self.side_inset,
                base_length = self.base_length - (self.side_inset/4),
                mid_offset = mid_offset
            ).rotate((1,0,0),(0,0,0),-90)
            
        ramp = (
            cq.Workplane("XY")
        )
        
        if self.render_center:
            ramp = ramp.add(center)
            
        
        self.ramp = (
            ramp
            .add(side.translate((0,(self.width/2),0)))
        ).translate((0,-1*(self.width/4),0))
        
    def make(self, parent=None):
        super().make(parent)
        
        if self.parent:
            self.parent.make()
        self._make_ramp()
        
    def build(self):
        super().build()
        
        scene = (
            cq.Workplane("XY")
            .union(self.ramp)
        )
        
        return scene