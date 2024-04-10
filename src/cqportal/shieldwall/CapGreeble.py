import cadquery as cq
from cadqueryhelper import Base
import math

class CapGreeble(Base):
    def __init__(self):
        super().__init__()
        #properties
        self.length = 20
        self.width = 8
        self.height = 30
        self.top_fillet = 2.9
        self.side_fillet = 2.5
        #self.operation = 'fillet' #chamfer
        self.operation = 'chamfer'
        
        self.render_grill = True
        self.grill_height = 2
        self.grill_padding_top = 1
        self.grill_padding_left = 2
        self.grill_margin =.5
        
        #shapes
        self.body = None
        self.grill = None
        self.grill_internal = None
        
        self.grill_set = None
        self.grill_set_internal = None
        
    def __make_body(self):
        self.body = cq.Workplane('XY').box(
            self.length,
            self.width,
            self.height
        )
        
        if self.operation == 'fillet':
            self.body = self.body.faces("X").edges("Z").fillet(self.side_fillet)
            self.body = self.body.faces("Z").edges("X").fillet(self.side_fillet)
        elif self.operation == 'chamfer':
           self.body = self.body.faces("X").edges("Z").chamfer(self.side_fillet)
           self.body = self.body.faces("Z").edges(">X").chamfer(self.top_fillet)
           self.body = self.body.faces("Z").edges("X").chamfer(self.side_fillet)

    def __make_grill_parts(self):
        grill = cq.Workplane("XY").box(
            self.length - self.grill_padding_left, 
            self.width, 
            self.grill_height
        )
        
        grill_inside = cq.Workplane("XY").box(
            self.length - self.grill_padding_left - self.grill_margin, 
            self.width - self.grill_margin*2, 
            self.grill_height
        )
        self.grill = grill
        self.grill_internal = grill_inside.faces("X").edges("Z").chamfer(1+self.grill_margin*2).translate(((self.grill_margin/2),0,0))

    def __make_grill(self, shape):
        grill_height = self.grill_height + self.grill_padding_top*2
        y_count = math.floor(self.height / grill_height) - 1
        
        def add_shape(loc):
            return shape.rotate((1,0,0),(0,0,0),90).val().located(loc)
        
        grill_set = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = 1, 
                ySpacing = grill_height,
                xCount = 1, 
                yCount= y_count, 
                center = True)
            .eachpoint(callback = add_shape)
        ).rotate((1,0,0),(0,0,0),90)
        
        return grill_set
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_body()
        
        if self.render_grill:
            self.__make_grill_parts()
            self.grill_set = self.__make_grill(self.grill)
            self.grill_set_internal = self.__make_grill(self.grill_internal)
        
    def build(self):
        scene = (
            cq.Workplane("XY")
            .union(self.body)
            #.add(self.grill_internal)
        )
        
        if self.render_grill:
            #pass
            scene = (
                scene
                #.cut(self.grill.translate((self.grill_padding_left/2,0,0)))
                #.add(self.grill_internal)
                .cut(self.grill_set.translate((self.grill_padding_left/2,0,0)))
                .add(self.grill_set_internal)
            )
        return scene