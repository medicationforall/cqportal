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
from . import PortalBase, Frame, Ramp

class Portal(Base):
    def __init__(self):
        super().__init__()
        
        #parameters
        self.render_base = True
        self.render_ramps = True
        self.render_hinges = True
        
        self.ramp_push = 0
        self.open_angle = 90
        self.hinge_segments = 3
        
        # blueprints
        self.bp_base = PortalBase()
        self.bp_frame = Frame()
        self.bp_ramp = Ramp()
        self.bp_hinge = Hinge()
        
        # shapes
        self.ramp_hinge_cut = None
        
    def _calculate_hinge_cut_length(self):
        return self.bp_frame.base_length - self.bp_frame.side_inset + 10
        
    def _calculate_hinge_cut_width(self):
        return (self.bp_hinge.radius+2) + self.bp_hinge.plate_spacer +1
    
    def _calculate_hinge_cut_height(self):
        return self.bp_ramp.width /2

    def __make_ramp_hinge_cut(self):
        length = self._calculate_hinge_cut_length()
        width = self._calculate_hinge_cut_width()
        height = self._calculate_hinge_cut_height()
        cut_box = cq.Workplane("XY").box(length,width,height)
        self.ramp_hinge_cut = cut_box
        
    def make(self, parent=None):
        super().make(parent)
        self.bp_base.make()
        self.bp_frame.make()
        self.bp_ramp.make(self.bp_frame)
        
        self.bp_hinge.length = self.bp_frame.base_length - self.bp_frame.side_inset
        self.bp_hinge.segments = self.hinge_segments
        self.bp_hinge.plate_spacer = 1
        self.bp_hinge.make()
        
        self.__make_ramp_hinge_cut()
        
    def build_hinges(self):
        hinge = self.bp_hinge.build()
        hinge_y = self.bp_frame.width/2 + self.bp_hinge.radius + self.bp_hinge.plate_spacer
        hinge_z = self.bp_base.height + self.bp_hinge.radius
        
        hinges = (
            cq.Workplane("XY")
            .add(hinge.translate((0,hinge_y,hinge_z)))
            .add(hinge.rotate((0,0,1),(0,0,0),180).translate((0,-hinge_y,hinge_z)))

        )
        
        return hinges
    
    def build_hinge_cuts(self):
        
        cut_y = self.bp_frame.width/2 + self._calculate_hinge_cut_width()/2
        cut_z = self.bp_base.height + self._calculate_hinge_cut_height()/2
        
        hinge_cuts = (
            cq.Workplane("XY")
            .add(self.ramp_hinge_cut.translate((0,cut_y,cut_z)))
            .add(self.ramp_hinge_cut.translate((0,-cut_y,cut_z)))
        )
        
        return hinge_cuts
        
        
    def build_closed(self):
        super().build()
        
        frame = self.bp_frame.build()
        
        scene = (
            cq.Workplane("XY")
            .union(frame.translate((0,0,self.bp_frame.height/2 + self.bp_base.height)))

        )
        
        if self.render_base:
            portal_base  = self.bp_base.build()
            scene = scene.union(portal_base.translate((0,0,self.bp_base.height/2)))
            
        
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
            
        if self.render_hinges:
            self.bp_hinge.rotate_deg=-90
            self.bp_hinge.make()
            hinges = self.build_hinges()
            hinge_cuts = self.build_hinge_cuts()
            scene = scene.cut(hinge_cuts)
            scene = scene.union(hinges)
        
        return scene
    
    def build_open(self):
        super().build()
        portal_base  = self.bp_base.build()
        frame = self.bp_frame.build()
        
        scene = (
            cq.Workplane("XY")
            .union(frame.translate((0,0,self.bp_frame.height/2 + self.bp_base.height)))

        )
        
        if self.render_base:
            portal_base  = self.bp_base.build()
            scene = scene.union(portal_base.translate((0,0,self.bp_base.height/2)))
            
        
        if self.render_ramps:
            ramp = self.bp_ramp.build()
            ramp_y = self.bp_ramp.height/2 + self.bp_frame.width/2
            ramp_z = self.bp_ramp.width/2+self.bp_base.height
            scene = (
                scene
                .add(
                    ramp
                    .rotate((1,0,0),(0,0,0),-self.open_angle)
                    .translate((0,-ramp_y,ramp_z))
                )
                .add(
                    ramp
                    .rotate((0,0,1),(0,0,0), 180)
                    .rotate((1,0,0),(0,0,0),self.open_angle)
                    .translate((0,ramp_y,ramp_z))
                )
            )
            
        if self.render_hinges:
            self.bp_hinge.rotate_deg=0
            self.bp_hinge.make()
            hinges = self.build_hinges()
            hinge_cuts = self.build_hinge_cuts()
            scene = scene.cut(hinge_cuts)
            scene = scene.union(hinges)
        
        return scene