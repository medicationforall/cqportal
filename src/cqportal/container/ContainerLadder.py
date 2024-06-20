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

class ContainerLadder(Base):
    def __init__(self):
        super().__init__()
        self.width = (150/5)
        self.x_padding = 2
        self.ladder_depth = 6
        self.ladder_rungs = 8
        self.ladder_rung_radius = 2

        # shapes
        self.side_template = None
        self.ladder_cut = None
        self.ladder = None
        
    def _calculate_mid_offset(self):
        mid_offset = -1*(self.parent.height/2) + self.parent.base_offset
        return mid_offset
        
    def __make_side_template(self):
        mid_offset = self._calculate_mid_offset()
        
        side = shape.coffin(
            self.parent.length - self.parent.side_inset,
            self.parent.height - (self.parent.side_inset/2),
            self.width - self.x_padding*2,
            top_length = self.parent.top_length - self.parent.side_inset,
            base_length = self.parent.base_length - self.parent.side_inset,
            mid_offset = mid_offset + (self.parent.side_inset/4)
        ).rotate((1,0,0),(0,0,0),-90)
        
        side_z = -1*(self.parent.side_inset/4)
        side = side.translate((0,0,side_z))
        
        self.side_template = side

    def __make_ladder_cut(self):
        self.ladder_cut = (
            cq.Workplane("XY")
            .add(self.side_template)
            .cut(self.side_template.translate((-self.ladder_depth,0,0)))
        )
        
    def _calculate_max_inside_length(self):
        length = self.parent.length - self.parent.side_inset
        top_length = self.parent.top_length - self.parent.side_inset
        base_length = self.parent.base_length - self.parent.side_inset
        if top_length > length:
            length = top_length
            
        if base_length > length:
            length = base_length
        return length
        
    def __make_ladder(self):
        length = self._calculate_max_inside_length()
        segment_height = (self.parent.height - (self.parent.side_inset/2)) / self.ladder_rungs
        ladder_cut = (
            self.ladder_cut
            .translate((0,0,(self.parent.side_inset/4)))
            .rotate((1,0,0),(0,0,0),90)
        )
        
        def add_segment(loc):
            # weird stuff
            segment_length = length
            loc_tuple = loc.toTuple()[0]
            x = loc_tuple[0]
            y = loc_tuple[1]
            
            greeble = (
                cq.Workplane("XY")
                .center(x, y)
                .box(
                    segment_length,
                    segment_height,
                    self.width - self.x_padding*2
                )
            )
            
            greeble = greeble.intersect(ladder_cut)
            center = greeble.val().Center()
            
            rung = cq.Workplane("XY").cylinder(self.width - self.x_padding*2, self.ladder_rung_radius).translate(center)
            return rung.val()
        
        ladder_rungs = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = length/2, 
                ySpacing = segment_height,
                xCount = 1, 
                yCount= self.ladder_rungs, 
                center = True)
            .eachpoint(callback = add_segment)
            
        ).rotate((1,0,0),(0,0,0),-90).translate((0,0,-1*(self.parent.side_inset/4)))
                
        self.ladder = ladder_rungs
        
    def make(self, parent=None):
        super().make(parent)
        #log('make ladder')
        self.__make_side_template()
        self.__make_ladder_cut()
        self.__make_ladder()

    def build(self):
        super().build()
        #log('build ladder')
        return self.ladder_cut, self.ladder
    