__all__ = ["TestSuite"]
from itertools import tee

import omni.ext
import omni.ui as ui
import omni.kit.commands as cmd
from pxr import Gf, Sdf, Usd

class TestSuite:
    
    def test():
        stage = omni.usd.get_context().get_stage()
        prim = stage.GetPrimAtPath("/Xform/lightcube")
        matrix: Gf.Matrix4d = omni.usd.get_world_transform_matrix(prim)
        translate: Gf.Vec3d = matrix.ExtractTranslation()
        # print(matrix)
        # print(translate)
        # print(translate[0],translate[1],translate[2])
        # Copy LightBox
        cmd.execute('CopyPrim',
            path_from='/Xform/lightcube',
            path_to='/Xform/lightcube_01',
            exclusive_select=False)
        cmd.execute('ChangeProperty',
        prop_path=Sdf.Path('/Xform/lightcube/Light_Box/Looks/Light_1900K/Shader.inputs:emissive_color'),
        #value=Gf.Vec3f(0.04596861682832241, 0.9775587320327759, 0.5173745155334473),
        value=Gf.Vec3f(1, 1, 1),
        prev=Gf.Vec3f(0.89189, 0.68077, 0.07576))          
        # Translate LightCube To Left                  
        cmd.execute('TransformPrimSRT',
            path=Sdf.Path('/Xform/lightcube_01/Light_Box'),
            new_translation=Gf.Vec3d(-(translate[0]+104.56476),translate[1] , translate[2]),
            new_rotation_euler=Gf.Vec3f(0.0, 0.0, 0.0),
            new_rotation_order=Gf.Vec3i(0, 1, 2),
            new_scale=Gf.Vec3f(1.0, 1.0, 1.0),
            old_translation=Gf.Vec3d(0.0, -96.9006238326304, 0.0),
            old_rotation_euler=Gf.Vec3f(0.0, 0.0, 0.0),
            old_rotation_order=Gf.Vec3i(0, 1, 2),
            old_scale=Gf.Vec3f(1.0, 1.0, 1.0))
        # Change emissive color
        cmd.execute('ChangeProperty',
            prop_path=Sdf.Path('/Xform/lightcube_01/Light_Box/Looks/Light_1900K/Shader.inputs:emissive_color'),
            value=Gf.Vec3f(0.02596861682832241, 0.4775587320327759, 0.5173745155334473),
            prev=Gf.Vec3f(0.89189, 0.68077, 0.07576))
        # Box Above
        cmd.execute('CopyPrim',
            path_from='/Xform/lightcube',
            path_to='/Xform/lightcube_02',
            exclusive_select=False)
        cmd.execute('TransformPrimSRT',
            path=Sdf.Path('/Xform/lightcube_02/Light_Box'),
            new_translation=Gf.Vec3d(translate[0], translate[1]+104.13682, 0.0),
            new_rotation_euler=Gf.Vec3f(0.0, 0.0, 0.0),
            new_rotation_order=Gf.Vec3i(0, 1, 2),
            new_scale=Gf.Vec3f(1.0, 1.0, 1.0),
            old_translation=Gf.Vec3d(0.0, -96.9006238326304, 0.0),
            old_rotation_euler=Gf.Vec3f(0.0, 0.0, 0.0),
            old_rotation_order=Gf.Vec3i(0, 1, 2),
            old_scale=Gf.Vec3f(1.0, 1.0, 1.0))
        # Purple Box
        cmd.execute('ChangeProperty',
            prop_path=Sdf.Path('/Xform/lightcube_02/Light_Box/Looks/Light_1900K/Shader.inputs:emissive_color'),
            value=Gf.Vec3f(0.92596861682832241, 0.075587320327759, 0.9173745155334473),
            prev=Gf.Vec3f(0.89189, 0.68077, 0.07576))
        # Diagonal Box
        cmd.execute('CopyPrim',
            path_from='/Xform/lightcube',
            path_to='/Xform/lightcube_03',
            exclusive_select=False)
        cmd.execute('TransformPrimSRT',
            path=Sdf.Path('/Xform/lightcube_03/Light_Box'),
            new_translation=Gf.Vec3d(translate[0] - 104.56476, translate[1]+104.13682, 0.0),
            new_rotation_euler=Gf.Vec3f(0.0, 0.0, 0.0),
            new_rotation_order=Gf.Vec3i(0, 1, 2),
            new_scale=Gf.Vec3f(1.0, 1.0, 1.0),
            old_translation=Gf.Vec3d(0.0, -96.9006238326304, 0.0),
            old_rotation_euler=Gf.Vec3f(0.0, 0.0, 0.0),
            old_rotation_order=Gf.Vec3i(0, 1, 2),
            old_scale=Gf.Vec3f(1.0, 1.0, 1.0))  
        cmd.execute('ChangeProperty',
            prop_path=Sdf.Path('/Xform/lightcube_03/Light_Box/Looks/Light_1900K/Shader.inputs:emissive_color'),
            value=Gf.Vec3f(1, 1, 1),
            prev=Gf.Vec3f(0.89189, 0.68077, 0.07576))                       