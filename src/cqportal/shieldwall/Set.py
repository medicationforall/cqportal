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
from . import ShieldShape, Mesh, Straight, EndCap, CornerConnector

class Set(Base):
    def __init__(self):
        super().__init__()
        #properties
        self.straight_count = 4
        self.padding = 5
        self.height = 25

        self.base_height = 5.6
        self.magnet_padding_x=2
        
        #self.connector_count = 2
        self.corner_count = 2
        
        #self.curve_count = 0
        self.end_cap_count = 4
        self.end_cap_length = 15
        
        #blueprints
        self.shape_bp = ShieldShape()
        self.mesh_bp = Mesh()
        self.straight_bp = Straight()
        self.end_bp = EndCap()
        self.corner_bp = CornerConnector()
        
    def __make_straight(self):
        self.straight_bp.shape_bp = self.shape_bp
        self.straight_bp.mesh_bp = self.mesh_bp
        self.straight_bp.height = self.height
        self.straight_bp.base_height = self.base_height
        self.straight_bp.magnet_padding_x = self.magnet_padding_x
        self.straight_bp.make()
        
    def __make_end_cap(self):
        self.end_bp.shape_bp = self.shape_bp
        self.end_bp.length = self.end_cap_length
        self.end_bp.height = self.height
        self.end_bp.base_height = self.base_height
        self.end_bp.magnet_padding_x = self.magnet_padding_x
        self.end_bp.make()
        
    def __make_corner(self):
        self.corner_bp.shape_bp = self.shape_bp
        self.corner_bp.height = self.height
        self.corner_bp.base_height = self.base_height
        self.corner_bp.magnet_padding_x = self.magnet_padding_x
        self.corner_bp.make()
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_straight()
        self.__make_end_cap()
        self.__make_corner()
        
    def build_repeat(self, item, width, count):
        scene = cq.Workplane("XY")
        
        for i in range(0,count):
            y_translate = (width + self.padding)*i
            scene = scene.add(item.translate((0,y_translate,0)))
        return scene
        
    def build_straight_walls(self):
        straight_wall = self.straight_bp.build()
        return self.build_repeat(
            straight_wall,
            self.straight_bp.width,
            self.straight_count
        )
    
    def build_end_caps(self):
        end_cap = self.end_bp.build()
        return self.build_repeat(
            end_cap,
            self.end_bp.width,
            self.end_cap_count
        )
    
    def build_corners(self):
        corner = self.corner_bp.build()
        return self.build_repeat(
            corner,
            self.corner_bp.width,
            self.corner_count
        )
        
    def build(self):
        super().build()
        straight_walls = self.build_straight_walls()
        end_caps = self.build_end_caps()
        corners = self.build_corners()
        
        cap_translate = (self.straight_bp.length/2 + self.end_bp.length/2 + self.padding)
        corner_translate = self.straight_bp.length/2 + self.end_bp.length + self.padding + self.corner_bp.length/2 + self.padding
        scene = (
            cq.Workplane("XY")
            .union(straight_walls)
            .union(end_caps.translate((cap_translate,0,0)))
            .add(corners.translate((corner_translate,0,0)))
        )
        return scene