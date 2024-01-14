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
from cadqueryhelper import Base
from . import PortalBase, Frame, Ramp

class Portal(Base):
    def __init__(self):
        super().__init__()
        
        #parameters
        self.render_ramps = True
        
        # blueprints
        self.bp_base = PortalBase()
        self.bp_frame = Frame()
        self.bp_ramp = Ramp()
        self.ramp_push = 0
        self.open_angle = 94
        
    def make(self, parent=None):
        super().make(parent)
        self.bp_base.make()
        self.bp_frame.make()
        self.bp_ramp.make(self.bp_frame)
        
    def build_closed(self):
        super().build()
        portal_base  = self.bp_base.build()
        frame = self.bp_frame.build()
        
        scene = (
            cq.Workplane("XY")
            .union(portal_base.translate((0,0,self.bp_base.height/2)))
            .union(frame.translate((0,0,self.bp_frame.height/2 + self.bp_base.height)))

        )
        
        if self.render_ramps:
            ramp = self.bp_ramp.build()
            scene = (
                scene
                .add(
                    ramp
                    .translate((0,-1*(self.bp_frame.width/2+self.ramp_push),self.bp_ramp.height/2+self.bp_base.height))
                )
                .add(
                    ramp
                    .rotate((0,0,1),(0,0,0), 180)
                    .translate((0,(self.bp_frame.width/2+self.ramp_push),self.bp_ramp.height/2+self.bp_base.height))
                )
            )
        
        return scene
    
    def build_open(self):
        super().build()
        portal_base  = self.bp_base.build()
        frame = self.bp_frame.build()
        
        scene = (
            cq.Workplane("XY")
            .union(portal_base.translate((0,0,self.bp_base.height/2)))
            .union(frame.translate((0,0,self.bp_frame.height/2 + self.bp_base.height)))

        )
        
        if self.render_ramps:
            ramp = self.bp_ramp.build()
            scene = (
                scene
                .add(
                    ramp
                    .rotate((1,0,0),(0,0,0),-self.open_angle)
                    .translate((0,-1*(self.bp_ramp.height/2 + self.bp_frame.width/2),self.bp_ramp.width/2+self.bp_base.height/2))
                    #.translate((0,-1*(self.bp_frame.width/2+self.ramp_push),self.bp_ramp.height/2+self.bp_base.height))
                )
                .add(
                    ramp
                    .rotate((0,0,1),(0,0,0), 180)
                    .rotate((1,0,0),(0,0,0),self.open_angle)
                    .translate((0,(self.bp_ramp.height/2 + self.bp_frame.width/2),self.bp_ramp.width/2+self.bp_base.height/2))
                )
            )
        
        return scene