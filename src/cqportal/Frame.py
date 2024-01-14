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

class Frame(Base):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.length = 150
        self.width = 15
        self.height = 150
        self.top_length = 90
        self.base_length = 100
        self.base_offset = 35
        self.side_inset = 8
        
        # shapes
        frame = None

    def _calculate_mid_offset(self):
        mid_offset = -1*(self.height/2) + self.base_offset
        return mid_offset
        
    def _make_frame(self):
        mid_offset = self._calculate_mid_offset()

        #outline = shape.coffin(
        #    self.length,
        #    self.height,
        #    self.width,
        #    top_length = self.top_length,
        #    base_length = self.base_length,
        #    mid_offset = mid_offset
        #).rotate((1,0,0),(0,0,0),-90)
        
        center = shape.coffin(
            self.length,
            self.height,
            self.width/3,
            top_length = self.top_length,
            base_length = self.base_length,
            mid_offset = mid_offset
        ).rotate((1,0,0),(0,0,0),-90)
        
        side = shape.coffin(
            self.length - self.side_inset,
            self.height - (self.side_inset/2),
            self.width/3,
            top_length = self.top_length - self.side_inset,
            base_length = self.base_length - self.side_inset,
            mid_offset = mid_offset + (self.side_inset/4)
        ).rotate((1,0,0),(0,0,0),-90)
        
        self.frame = (
            cq.Workplane("XY")
            .add(center)
            .add(side.translate((0,self.width/3,-1*(self.side_inset/4))))
            .add(side.translate((0,-1*(self.width/3),-1*(self.side_inset/4))))
        )
        
    def make(self, parent=None):
        super().make(parent)
        self._make_frame()
        
    def build(self):
        super().build()
        return self.frame
        scene = (
            cq.Workplane("XY")
            .union(self.frame)
        )
        
        return scene