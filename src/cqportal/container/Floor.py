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

class Floor(Base):
    def __init__(self):
        super().__init__()
        self.length = 75
        self.width = 75
        self.height = 4

        #shapes
        self.floor_cut = None
        self.floor = None

    def __make_floor_cut(self):
        floor_cut = cq.Workplane("XY").box(self.length, self.width, self.height)
        self.floor_cut = floor_cut

    def _make_floor(self):
        floor = cq.Workplane("XY").box(self.length, self.width, self.height)
        self.floor = floor


    def make(self, parent=None):
        super().make(parent)
        self.__make_floor_cut()
        self._make_floor()
    
    def build(self):
        super().build()
        return self.floor