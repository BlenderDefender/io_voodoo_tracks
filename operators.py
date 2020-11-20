# ##### BEGIN GPL LICENSE BLOCK #####
#
# <Import Voodoo Camera Tracker Scripts for Version 2.5 the easy way>
#  Copyright (C) <2020>  <Blender Defender>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
import os
import subprocess
import fileinput

from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

# updater ops import, all setup in this file
from . import addon_updater_ops
from . import addon_updater_ops

from .functions.FileFunctions import (
    replace_wrong_lines,
    run_script
)

from .functions.blenderdefender_functions import upgrade


# -----------------------------------------------------------------
# Main Operator, opening, editing and executing the Voodoo Script
# -----------------------------------------------------------------


class IOVOODOOTRACKS_OT_import_voodoo_track(Operator, ImportHelper):
    """Import Voodoo Camera Tracker Script (for Blender 2.5, will be automaticly converted)"""
    bl_idname = "voodoo_track.import"
    bl_label = "Open Voodo Camera Track (.py)"

    def execute(self, context):
        """Convert the selected file from 2.5 to 2.8"""

        # ------call the File Browser-----------
        #   bpy.ops.text.open(filepath=self.filepath)
        filepath = self.filepath
        replace_wrong_lines(filepath)
        run_script(filepath)

        # ------make Camera active--------------
        obj = bpy.context.window.scene.objects["voodoo_render_cam"]
        bpy.context.view_layer.objects.active = obj

        self.report({'INFO'}, "Successfully imported Voodoo Tracker Script! Press CRTL + 0 to switch to camera view!")

        return {'FINISHED'}

class IOVOODOOTRACKS_OT_upgrade(Operator):
    """Upgrade from free to donation version"""
    bl_idname = "voodoo_track.upgrade"
    bl_label = "Upgrade!"

    password : StringProperty(name="Enter Password. Don't have one?")

    def execute(self, context):
        """Upgrade to donation version"""
        from .functions.dict.dict import decoding

        self.report({'INFO'}, upgrade('functions/data.blenderdefender', decoding, self.password))
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "password")
        layout.label(text="Please enter your passcode. Don't have one?")
        layout.operator("wm.url_open", text="Get one!").url="https://gumroad.com/l/ImportVoodooCameraTracks"
        # return {'FINISHED'}


classes = (
    IOVOODOOTRACKS_OT_import_voodoo_track,
    IOVOODOOTRACKS_OT_upgrade
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
