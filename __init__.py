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
from bpy.types import (
    Context,
    UILayout
)
import os

import fileinput
import subprocess

from . import operators
from . import prefs

from .functions.dict.dict import decoding
from .functions.blenderdefender_functions import setup_addons_data, decode

bl_info = {
    "name": "Import Voodoo Camera Tracks",
    "author": "Blender Defender",
    "version": (1, 0, 7),
    "blender": (2, 83, 0),
    "location": "File > Import > Open Voodo Camera Track (.py)",
    "description": "Import Voodoo Camera Tracker Scripts (for Blender 2.5) to Blender 2.8x the easy way!",
    "warning": "Checkout Gumroad for other Addons and more...",
    "doc_url": "https://github.com/BlenderDefender/io_voodoo_tracks",
    "tracker_url": "https://github.com/BlenderDefender/io_voodoo_tracks/issues",
    "endpoint_url": "https://raw.githubusercontent.com/BlenderDefender/BlenderDefender/updater_endpoints/IOVOODOOTRACKS.json",
    "category": "Import-Export"}


def menu_func(self, context: 'Context'):
    layout: 'UILayout' = self.layout
    layout.operator("voodoo_track.import", icon='CON_CAMERASOLVER')


def register():
    import os
    import shutil
    path = os.path.join(os.path.expanduser(
        "~"), "Blender Addons Data", "io-voodoo-tracks")
    if not os.path.isdir(path):
        os.makedirs(path)
    shutil.copyfile(os.path.join(list(os.path.split(os.path.abspath(__file__)))[0],
                                 "functions",
                                 "data.blenderdefender"),
                    os.path.join(os.path.expanduser("~"),
                                 "Blender Addons Data",
                                 "io-voodoo-tracks",
                                 "data.blenderdefender"))

    data = decode(os.path.join(os.path.expanduser("~"),
                               "Blender Addons Data",
                               "io-voodoo-tracks",
                               "data.blenderdefender"),
                  decoding)
    setup_addons_data(data[1])

    prefs.register(bl_info)
    operators.register()

    bpy.types.TOPBAR_MT_file_import.append(menu_func)


def unregister():
    prefs.unregister()
    operators.unregister()
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)
