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
from cadqueryhelper import shape, irregular_grid
from . import Frame
from ..shieldwall import CapGreeble

class FrameBlock(Frame):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.seed = 'test'
        
        # blueprints
        self.bp_power:CapGreeble|None = CapGreeble()
        
        # shapes
        self.i_grid:cq.Workplane|None = None
        self.power_greeble:cq.Workplane|None = None 
    
    def make_frame_power_greeble(self):
        if self.bp_power:
            bp_cap = self.bp_power
            diff = (self.length - self.base_length)/2 + self.side_inset/2

            offset = 4
            bp_cap.length = diff-offset
            bp_cap.width = 19
            bp_cap.height = 30
            bp_cap.top_fillet = 2.9
            bp_cap.side_fillet = 3
            bp_cap.operation = 'chamfer'

            bp_cap.render_grill = True
            bp_cap.grill_height = 2
            bp_cap.grill_padding_top = 1
            bp_cap.grill_padding_left = 2
            bp_cap.grill_margin = .75
            bp_cap.make()

            self.power_greeble = bp_cap.build().translate((
                self.length/2-bp_cap.length/2-offset,
                0,
                -self.height/2+bp_cap.height/2
            ))
    
    def make_greebled_panel(self):
        i_grid = irregular_grid(
            length = self.length,
            width = self.height,
            height = (self.width/3)-4,
            max_height = (self.width/3),
            max_columns = 2,
            max_rows = 3,
            col_size = 10,
            row_size = 10,
            align_z = False,
            include_outline = True,
            passes_count = 1000,
            seed = self.seed,
            make_item = None,
            union_grid = False,
        )
        self.i_grid = i_grid.rotate((1,0,0),(0,0,0),90)# = i_grid.translate((0,0,-1*(height/2)))
    
    def _make_center(self, width:float) -> cq.Workplane:
        mid_offset = self._calculate_mid_offset()
        center = shape.coffin(
            self.length,
            self.height,
            width,
            top_length = self.top_length,
            base_length = self.base_length,
            mid_offset = mid_offset
        ).rotate((1,0,0),(0,0,0),-90)
        
        center_cut = shape.coffin(
            self.length-(self.frame_size*2),
            self.height-(self.frame_size*2),
            self.width,
            top_length = self.top_length - self.frame_size,
            base_length = self.base_length - self.frame_size,
            mid_offset = mid_offset
        ).rotate((1,0,0),(0,0,0),-90)
        
        center_frame = (
            cq.Workplane("XY")
            .union(center)
            .cut(center_cut)
        )
        
        if self.i_grid:
            center_frame = (
                center_frame
                .intersect(self.i_grid)
            )

        if self.power_greeble:
            self.power_greeble = self.power_greeble.cut(center_cut)
        
        return center_frame
    
    def _make_side(self, width:float) -> cq.Workplane:
        mid_offset = self._calculate_mid_offset()
        
        side = shape.coffin(
            self.length - self.side_inset,
            self.height - (self.side_inset/2),
            width,
            top_length = self.top_length - self.side_inset,
            base_length = self.base_length - self.side_inset,
            mid_offset = mid_offset + (self.side_inset/4)
        ).rotate((1,0,0),(0,0,0),-90)
        
        side_cut = self._make_side_cut(width = width)
        
        side_frame = (
            cq.Workplane("XY")
            .union(side)
            .cut(side_cut)
        )
        
        if self.i_grid:
            greebled_side_frame = (
                side_frame
                .intersect(self.i_grid)
                .union(side_frame.translate((0,-1.5,0)))
            )
            
        return greebled_side_frame
        
    def make(self, parent=None):
        self.parent = parent
        self.make_called = True

        self.make_frame_power_greeble()
        self.make_greebled_panel()
        self.make_frame()
        
    def build(self) -> cq.Workplane:
        if self.make_called == False:
            raise Exception('Make has not been called')
        
        scene = cq.Workplane("XY")
        
        if self.frame:
            scene = scene.union(self.frame)
        else:
            raise Exception('Unable to resolve frame')
        
        if self.power_greeble:
            scene = (
                scene
                .union(self.power_greeble)
                .union(self.power_greeble.rotate((0,0,1),(0,0,0),180))
            )
        
        return scene