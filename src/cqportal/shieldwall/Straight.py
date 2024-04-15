import cadquery as cq
from . import ShieldShape, Mesh, Magnets
from cadqueryhelper import Base

class Straight(Base):
    def __init__(self):
        super().__init__()
        #properties
        self.length = 75
        self.width = 20
        self.height = 25

        self.base_height = 5.6
        
        self.render_magnets = True
        self.magnet_padding = 1
        self.magnet_padding_x=2
        
        self.cut_padding_x = 3
        self.cut_padding_z = 3
        
        self.post_length = 2
        self.post_padding_y = 1
        self.mesh_width = 3
        
        self.cut_width = .8
        self.key_margin = 0.2
        
        #blueprints
        self.shape_bp = ShieldShape()
        self.mesh_bp = Mesh()
        self.magnets_bp = Magnets()
        
        #shapes
        self.shape = None
        self.outline = None
        self.post = None
        self.key_cut = None
        self.key_template = None
        
    def __make_shape(self):
        self.shape_bp.length = self.height
        self.shape_bp.width = self.width
        self.shape_bp.base_height = self.base_height
        self.shape_bp.make()
        self.shape = self.shape_bp.build()
        
    def __make_outline(self):
        outline = (
            self.shape.extrude(self.length)
            .translate((0,0,-1*(self.length/2)))
            .rotate((0,1,0),(0,0,0),90)
        )
        self.outline = outline
        
    def _calculate_cut_height(self):
        z_diff =  self.shape_bp.base_height+4
        cut_height= self.height - z_diff
        return cut_height
        
    def __make_cut(self):
        cut_height = self._calculate_cut_height()
        cut_length = self.length - self.cut_padding_x*2
        self.cut = (
            cq.Workplane('XY')
            .box(
                cut_length,
                self.width,
                cut_height
            )
        )
        
    def __make_post(self):
        detail_height = self._calculate_cut_height()
        post_width = self.width - self.post_padding_y*2 + self.shape_bp.middle_width_inset*2 
        post = (
            cq.Workplane("XY")
            .box(
                self.post_length,
                post_width,
                detail_height
            )
        )
        self.post = post
        
    def __make_mesh(self):
        #mesh_length = self.length - 
        mesh_height = self._calculate_cut_height()
        mesh_length = self.length - self.cut_padding_x*2 - self.post_length*2
        
        self.mesh_bp.length = mesh_length
        self.mesh_bp.width = self.mesh_width
        self.mesh_bp.height = mesh_height
        self.mesh_bp.make()
        
    def __make_key_cut(self):
        key_length = self.length - self.cut_padding_x*2 - self.post_length*2 + (self.key_margin*2)
        key_height = self.height - 2  + self.key_margin
        self.key_cut = (
            cq.Workplane('XY')
            .box(
                key_length, 
                self.cut_width, 
                key_height
            )
        )

        self.key_template = (
            cq.Workplane('XY')
            .box(
                key_length, 
                key_height,
                2 
            )
        )
        
    def __make_magnets(self):
        self.magnets_bp.distance = self.width - self.magnets_bp.pip_radius*2 - self.magnet_padding*2 - self.magnet_padding_x
        self.magnets_bp.make()
        
    def make(self, parent=None):
        super().make(parent)
        self.__make_shape()
        self.__make_outline()
        self.__make_cut()
        self.__make_post()
        self.__make_mesh()
        self.__make_key_cut()
        self.__make_magnets()
        
    def build_magnets(self):
           magnets = self.magnets_bp.build()
           magnet_x = self.length/2 - self.magnets_bp.pip_height/2
           magnet_z = -(self.height/2) + self.base_height - self.magnets_bp.pip_radius - self.magnet_padding
           scene = (
               cq.Workplane("XY")
               .union(magnets.translate((magnet_x,0,magnet_z)))
               .union(magnets.translate((-magnet_x,0,magnet_z)))
           )
           return scene
        
    def build(self):
        super().build()
        interior_z_translate = 2
        post_x_translate = self.length/2-self.post_length/2 - self.cut_padding_x 
        mesh = self.mesh_bp.build()

        scene = (
            cq.Workplane('XY')
            .add(self.outline)
            .cut(self.cut.translate((
                0,
                0,
                interior_z_translate
            )))
            .add(self.post.translate((
                post_x_translate,
                0,
                interior_z_translate
            )))
            .add(self.post.translate((
                -post_x_translate,
                0,
                interior_z_translate
            )))
            .union(mesh.translate((0,0,2)))
            .cut(self.key_cut.translate((0,0,-1+self.key_margin/2)))
        )
        
        if self.render_magnets:
            magnets = self.build_magnets()
            scene = scene.cut(magnets)
 
        #return self.post
        return scene
        
    
    def build_assembly(self):
        super().build()
        interior_z_translate = 2
        post_x_translate = self.length/2-self.post_length/2 - self.cut_padding_x 
        mesh = self.mesh_bp.build()
        
        frame = (
            cq.Workplane('XY')
            .add(self.outline)
            .cut(self.cut.translate((
                0,
                0,
                interior_z_translate
            )))
            .add(self.post.translate((
                post_x_translate,
                0,
                interior_z_translate
            )))
            .add(self.post.translate((
                -post_x_translate,
                0,
                interior_z_translate
            )))
            .cut(self.key_cut.translate((0,0,-1+self.key_margin/2)))
        )
        
        if self.render_magnets:
            magnets = self.build_magnets()
            frame = frame.cut(magnets)
        
        mesh = (
            cq.Workplane('XY')
            .union(mesh.translate((0,0,2)))
            .cut(self.key_cut.translate((0,0,-1+self.key_margin/2)))
        )
        
        window = (
            cq.Workplane('XY')
            .union(self.key_cut.translate((0,0,-1+self.key_margin/2)))
        )
        
        assembly = cq.Assembly()
        assembly.add(frame, color=cq.Color(1, 0, 0), name="frame")
        assembly.add(mesh, color=cq.Color(0, 0, 1), name="mesh")
        assembly.add(window, color=cq.Color(0, 1, 0), name="window")
        
        #return self.post
        return assembly