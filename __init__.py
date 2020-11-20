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

bl_info = {
    "name": "Import Voodoo Camera Tracks",
    "author": "Blender Defender",
    "version": (1, 0, 6),
    "blender": (2, 83, 0),
    "location": "File > Import > Open Voodo Camera Track (.py)",
    "description": "Import Voodoo Camera Tracker Scripts (for Blender 2.5) to Blender 2.8x the easy way!",
    "warning": "Checkout Gumroad for other Addons and more...",
    "wiki_url": "https://github.com/BlenderDefender/io_voodoo_tracks",
    "tracker_url": "https://github.com/BlenderDefender/io_voodoo_tracks/issues",
    "category": "Import-Export"}

if "bpy" in locals():
    import importlib
    # bl_class_registry.BlClassRegistry.cleanup()
    importlib.reload(prefs)
    importlib.reload(operators)

else:
    import bpy
    # from . import bl_class_registry
    from . import operators
    from . import prefs

import bpy
import os
import subprocess
import fileinput

from .functions.blenderdefender_functions import create_db

def menu_func(self, context):
    self.layout.operator("voodoo_track.import", icon='CON_CAMERASOLVER')


def register():
    import os
    if "IO.db" in os.listdir(os.path.join(os.path.split(os.path.abspath(__file__))[0], "functions")):
        pass
    else:
        create_db()

    prefs.register()
    operators.register()

    bpy.types.TOPBAR_MT_file_import.append(menu_func)


def unregister():
    prefs.unregister()
    operators.unregister()
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)
