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
from cadqueryhelper import Base, Hinge
from . import PortalBase, Frame, Ramp, PortalHinge

class Portal(Base):
    def __init__(self):
        super().__init__()
        
        #parameters
        self.render_base = True
        self.render_hinges = True
        
        self.ramp_push = 0
        self.hinge_segments = 3
        self.plate_spacer = 1
        
        # blueprints
        self.bp_base = PortalBase()
        self.bp_frame = Frame()
        self.bp_ramp = Ramp()
        self.bp_hinge = PortalHinge()
        
    def make(self, parent=None):
        super().make(parent)
        self.bp_base.make()
        self.bp_frame.make()
        self.bp_ramp.make(self.bp_frame)
        
        self.bp_hinge.length = self.bp_frame.base_length - self.bp_frame.side_inset
        self.bp_hinge.segments = self.hinge_segments
        self.bp_hinge.plate_spacer = self.plate_spacer
        self.bp_hinge.make(self.bp_ramp)
        
    def build_hinges(self):
        portal_hinge = self.bp_hinge.build()
        hinge_y = self.bp_frame.width/2 + self.bp_hinge.radius + self.bp_hinge.plate_spacer
        hinge_z = self.bp_base.height + self.bp_hinge.radius
        
        hinges = (
            cq.Workplane("XY")
            .add(
                portal_hinge
                .rotate((0,0,1),(0,0,0),180)
                .translate((0,hinge_y,hinge_z))
            )
            .add(
                portal_hinge
                .translate((0,-hinge_y,hinge_z))
            )
        )
        
        return hinges
        
        
    def build(self):
        super().build()
        
        frame = self.bp_frame.build()
        
        scene = (
            cq.Workplane("XY")
            .union(frame.translate((0,0,self.bp_frame.height/2 + self.bp_base.height)))
        )
        
        if self.render_base:
            portal_base  = self.bp_base.build()
            scene = scene.union(portal_base.translate((0,0,self.bp_base.height/2)))

        if self.render_hinges:   
            hinges = self.build_hinges()
            scene = scene.union(hinges)
        
        return scene