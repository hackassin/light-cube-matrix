__all__ = ["LightCubeExt"]
from itertools import tee
import omni.ext
import omni.ui as ui
import omni.kit.commands as cmd
from .combo_box_model import ComboBoxModel
from .test_suite import TestSuite
from .helper import Helper as hp
from pxr import Gf, Sdf, Usd
SPACING = 4
LABEL_WIDTH = 120

class LightCubeExt(ui.Window, omni.ext.IExt):
    """
    Class that inherits Window from omni.ui and extension from omni.ext.
    This defines the member functions that are used for UI window callbacks and various
    other logical utilities to generate (n x m) lightboxes with various color patterns      
    """    

    def __init__(self,title: str = 'test', delegate=None, **kwargs):
        self.__label_width = LABEL_WIDTH
        super().__init__(title, **kwargs)
        # Models
        self._dims_model_r = ui.SimpleIntModel()
        self._dims_model_c = ui.SimpleIntModel()
        self._pattern_type_model = ComboBoxModel("Plain", "Diagonal", "Random")

    def duplicate_prim(self, prim_list, num, flag=0):
        """
        Method to duplicate the source lightcube

        Args:
            prim_list (list): list of prim names
            num (int): counter of lightcubes generated
            flag (int, optional): for rule based logics

        Returns:
            list: list of prim names
        """        
        if flag == 1:
            return prim_list
        prim_str = '/Xform/lightcube' + '_0' + str(num)
        prim_list.append(prim_str)
        # Copy LightBox
        cmd.execute('CopyPrim',
            path_from='/Xform/lightcube',
            path_to=prim_str,
            exclusive_select=False)
        return prim_list

    def translate_prim(self, tx, ty, tx0ty0tz0, prim_list):
        """
        Translation method to shift objects along x-y axis
        Args:
            tx (float): translation in x-axis
            ty (float): translation in y-axis
            tx0ty0tz0 (tuple): translation constant for source cube in (x,y,z) axis
            prim_list (list): list of prim names
        """

        cmd.execute('TransformPrimSRT',
            #path=Sdf.Path('/World/lightcube'+prim_str+'/Light_Box'),
            path=Sdf.Path(prim_list[-1]+'/Light_Box'),
            new_translation=Gf.Vec3d(tx, ty, tx0ty0tz0[2]),
            new_rotation_euler=Gf.Vec3f(0.0, 0.0, 0.0),
            new_rotation_order=Gf.Vec3i(0, 1, 2),
            new_scale=Gf.Vec3f(1.0, 1.0, 1.0),
            old_translation=Gf.Vec3d(tx0ty0tz0[0], tx0ty0tz0[1], tx0ty0tz0[2]),
            old_rotation_euler=Gf.Vec3f(0.0, 0.0, 0.0),
            old_rotation_order=Gf.Vec3i(0, 1, 2),
            old_scale=Gf.Vec3f(1.0, 1.0, 1.0))

    def update_color(self, prim_list, row_col, mode='Plain'):
        """
        _summary_

        Args:
            prim_list (list): _description_
            row_col (tuple): lightcube 2D matrix co-ordinates
            mode (str, optional): Color pattern mode. Defaults to 'Plain'.
        """        

        if mode == 'Plain':
            pass
            # cmd.execute('ChangeProperty',
            #     prop_path=Sdf.Path('/Xform/lightcube_01/Light_Box/Looks/Light_1900K/Shader.inputs:emissive_color'),
            #     value=Gf.Vec3f(0.02596861682832241, 0.4775587320327759, 0.5173745155334473),
            #     prev=Gf.Vec3f(0.7876448035240173, 0.07906857877969742, 0.07906857877969742))
        if mode == 'Diagonal' and row_col[0]!=row_col[1]:
            cmd.execute('ChangeProperty',
                prop_path=Sdf.Path(prim_list[-1] + '/Light_Box/Looks/Light_1900K/Shader.inputs:emissive_color'),
                value=Gf.Vec3f(0.02596861682832241, 0.4775587320327759, 0.5173745155334473),
                prev=Gf.Vec3f(0.89189, 0.68077, 0.07576))
            print("Color changed")
        if mode == 'Random':
            rand_vals = hp.randomize()
            cmd.execute('ChangeProperty',
                prop_path=Sdf.Path(prim_list[-1] + '/Light_Box/Looks/Light_1900K/Shader.inputs:emissive_color'),
                value=Gf.Vec3f(rand_vals[0], rand_vals[1], rand_vals[2]),
                prev=Gf.Vec3f(0.89189, 0.68077, 0.07576))            
            
    def on_click(self, n=3,m=3):
        """
        _summary_

        Args:
            n (int, optional): Number of rows. Defaults to 3.
            m (int, optional): Number of columns. Defaults to 3.
        """

        print("Lights Away!")
        stage = omni.usd.get_context().get_stage()
        prim = stage.GetPrimAtPath("/Xform/lightcube")
        matrix: Gf.Matrix4d = omni.usd.get_world_transform_matrix(prim)
        tx0ty0tz0: Gf.Vec3d = matrix.ExtractTranslation()
        prim_list = []
        # 2-D dims of lightbox
        length = 104.56476
        height = 104.13682
        # height multiple 
        h = 0
        num = 0
        flag = 0
        n = self._dims_model_r.as_int
        m = self._dims_model_c.as_int
        mode=self._pattern_type_model.get_current_item().as_string
        for r in reversed(range(n)):
            # translation variables & length multiple
            tx = ty = l = 0
            for c in reversed(range(m)):
                num+=1
                if r==n-1 and c==m-1: 
                    flag = 1
                    prim_list.append('/Xform/lightcube')
                #if r==2 and c==1: continue
                if c==m-1: l=0
                else: l+=1 
                # translation on x-axis
                tx = tx0ty0tz0[0] - l*length
                # translation on y-axis
                ty = tx0ty0tz0[1] + h*height
                prim_list = self.duplicate_prim(prim_list, num, flag)
                self.translate_prim(tx, ty, tx0ty0tz0, prim_list)
                self.update_color(prim_list, (r,c), mode)               
                flag = 0
            h+=1

    def on_startup(self, ext_id):
        """
        Method execute on startup of extension

        Args:
            ext_id (omni.ext): id of extension
        """

        print("LightCube extension startup")
        # self.models_()
        self._window = ui.Window("LightCube Generator", width=300, height=300)
        with self._window.frame:
            with ui.VStack(height=0, spacing=SPACING):
                ui.Label("Dimensions")
                # Row
                with ui.HStack():
                    ui.Label("Rows", name="attribute_name", width=LABEL_WIDTH)
                    ui.IntDrag(self._dims_model_r)
                with ui.HStack():
                    ui.Label("Columns", name="attribute_name", width=LABEL_WIDTH)
                    ui.IntDrag(self._dims_model_c)
                # Row    
                with ui.HStack():
                    ui.Label("Pattern Type", name="attribute_name", width=LABEL_WIDTH)
                    ui.ComboBox(self._pattern_type_model)
                                
                ui.Button("Create LightBox", clicked_fn=lambda: self.on_click())
                ui.Button("Test", clicked_fn=lambda: TestSuite.test())

    def on_shutdown(self):
        print("LightCube Extension shutdown")