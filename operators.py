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

from bpy.props import (
    StringProperty
)
from bpy.types import (
    Context,
    Event,
    Operator,
    UILayout
)
from bpy_extras.io_utils import ImportHelper

from os import path as p

from .functions.blenderdefender_functions import upgrade


# -----------------------------------------------------------------
# Main Operator, opening, editing and executing the Voodoo Script
# -----------------------------------------------------------------


class IOVOODOOTRACKS_OT_import_voodoo_track(Operator, ImportHelper):
    """Import Voodoo Camera Tracker Script (for Blender 2.5, will be automaticly converted)"""
    bl_idname = "voodoo_track.import"
    bl_label = "Open Voodo Camera Track (.py)"

    def execute(self, context: 'Context'):
        """Convert the selected file from 2.5 to 2.8"""

        replace_texts = {
            "scene.objects.link(dummy)": "bpy.context.collection.objects.link(dummy)",
            "data.lens_unit = 'DEGREES'": "",
            "data.dof_distance = 0.0": "",
            "data.draw_size = 0.5": "",
            "scene.objects.link(mesh)": "bpy.context.collection.objects.link(mesh)",
            "scene.objects.link(vcam)": "bpy.context.collection.objects.link(vcam)"
        }

        with open(self.filepath, "r", encoding="utf-8") as f:
            voodoo_script = f.read()

        for source, new in replace_texts.items():
            voodoo_script = voodoo_script.replace(source, new)

        with open(self.filepath, "w+", encoding="utf-8") as f:
            f.write(voodoo_script)

        exec(voodoo_script)

        # ------ make Camera active --------------
        obj = context.window.scene.objects["voodoo_render_cam"]
        context.view_layer.objects.active = obj

        self.report(
            {'INFO'}, "Successfully imported Voodoo Tracker Script! Press CRTL + 0 to switch to camera view!")

        return {'FINISHED'}


class IOVOODOOTRACKS_OT_upgrade(Operator):
    """Upgrade from free to donation version"""
    bl_idname = "voodoo_track.upgrade"
    bl_label = "Upgrade!"

    password: StringProperty(name="")

    def execute(self, context: 'Context'):
        """Upgrade to donation version"""

        self.report({'INFO'}, upgrade(p.join(p.expanduser("~"),
                                             "Blender Addons Data",
                                             "io-voodoo-tracks",
                                             "data.blenderdefender"),
                                      self.password))
        return {'FINISHED'}

    def invoke(self, context: 'Context', event: 'Event'):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context: 'Context'):
        layout: 'UILayout' = self.layout

        layout.prop(self, "password")
        layout.label(text="Please enter your passcode. Don't have one?")
        layout.operator(
            "wm.url_open", text="Get one!").url = "https://gumroad.com/l/ImportVoodooCameraTracks"
        layout.label(text="Didn't receive Email with passcode?")
        layout.label(text="Please open an issue on GitHub.")
        layout.label(text="I will help as soon as possible!")


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
