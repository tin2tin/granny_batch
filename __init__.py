bl_info = {
    "name": "Batch Convert for Granny ",
    "author": "tintwotin",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "View3D > Sidebar > Granny Batch Tab",
    "description": "Batch convert a folder of fbx to a new folder of Granny friendly files",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy, os
import os.path
from mathutils import Vector

from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper
from bpy.props import (
    StringProperty,
    PointerProperty,
)
from bpy.types import (
    Panel,
    Operator,
    AddonPreferences,
    PropertyGroup,
)


class GrannyProperties(PropertyGroup):

    in_path_string: StringProperty(
        name="",
        description="Path to Input Directory",
        default="",
        maxlen=1024,
        subtype="DIR_PATH",
    )

    out_path_string: StringProperty(
        name="",
        description="Path to Output Directory",
        default="",
        maxlen=1024,
        subtype="DIR_PATH",
    )


class BatchCorrectGranny(Operator):
    """Batch correct a folder containing fbx files for Granny"""

    bl_idname = "view3d.granny_batch"
    bl_label = "Run batch"

    def execute(self, context):
        scn = bpy.context.scene
        in_path = os.path.abspath(scn.granny_input.in_path_string)
        in_path = str(in_path)  # .replace("\\", "\\\\")
        if not (os.path.isdir(in_path)):
            msg = "Please select an absolute input path: " + in_path
            self.report({"WARNING"}, msg)
            return {"CANCELLED"}
        out_path = os.path.abspath(scn.granny_input.out_path_string)
        out_path = str(out_path)  # .replace("\\", "\\\\")
        if not (os.path.isdir(out_path)):
            msg = "Please select an absolute output path: " + out_path
            self.report({"WARNING"}, msg)
            return {"CANCELLED"}
        for root, subdirectories, files in os.walk(in_path):

            for file in files:
                print(os.path.join(root, file))
                name, extention = os.path.split(file)
                if extention[-3:] == "fbx":
                    self.report({"INFO"}, "Processing: " + file)
                    home_scene = bpy.context.scene
                    new_scene = bpy.data.scenes.new(extention[1:-4])
                    bpy.context.window.scene = new_scene
                    bpy.ops.import_scene.fbx(filepath=os.path.join(root, file))

                    bpy.ops.object.select_all(action="SELECT")
                    objects = bpy.context.selected_objects

                    bpy.ops.object.empty_add(
                        type="PLAIN_AXES",
                        align="WORLD",
                        location=(0, 0, 0),
                        scale=(1, 1, 1),
                    )
                    empty = bpy.context.active_object
                    empty.name = extention[1:-4]

                    switch_mode = False
                    if bpy.context.mode != "OBJECT":
                        switch_mode = Truex
                        bpy.ops.object.mode_set(mode="OBJECT", toggle=True)
                    bpy.ops.object.select_all(action="DESELECT")
                    if objects:
                        for obj in objects:
                            obj.select_set(True)
                        points = []
                        for o in bpy.context.selected_objects:
                            for b in o.bound_box:
                                points.append(o.matrix_world @ Vector(b))
                        points.sort(key=lambda x: x[2])
                        z_altitude = points[0][2]

                        for o in bpy.context.selected_objects:
                            o.location.z -= z_altitude
                    bpy.ops.object.select_all(action="DESELECT")
                    if objects:
                        for obj in objects:
                            obj.select_set(True)
                    bpy.context.view_layer.objects.active = empty

                    bpy.ops.object.parent_set()
                    print(out_path + "\\" + name + extention)
                    bpy.ops.export_scene.fbx(
                        filepath=out_path + "\\" + name + extention,
                        use_selection=False,
                        check_existing=True,
                    )
                    bpy.ops.scene.delete()
                    bpy.context.window.scene = home_scene
            self.report({"INFO"}, "Finished")
        return {"FINISHED"}


class GrannyBatchTab:
    bl_category = "Granny Batch"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class VIEW_PT_granny_batch(GrannyBatchTab, Panel):
    bl_label = "Granny Batch"
    bl_category = "Granny Batch"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "view3d.granny_batch_panel"

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        layout.prop(scn.granny_input, "in_path_string", text="Input Folder")
        layout.prop(scn.granny_input, "out_path_string", text="Output Folder")
        layout.operator("view3d.granny_batch", text="Run Batch")


def register():
    bpy.utils.register_class(GrannyProperties)
    bpy.utils.register_class(BatchCorrectGranny)
    bpy.utils.register_class(VIEW_PT_granny_batch)
    bpy.types.Scene.granny_input = PointerProperty(type=GrannyProperties)


def unregister():
    bpy.utils.unregister_class(GrannyProperties)
    bpy.utils.unregister_class(BatchCorrectGranny)
    bpy.utils.unregister_class(VIEW_PT_granny_batch)
    del bpy.types.Scene.granny_input


if __name__ == "__main__":
    register()
