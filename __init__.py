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


from . import operators


def menu_func(self, context: 'Context'):
    layout: 'UILayout' = self.layout
    layout.operator("voodoo_track.import", icon='CON_CAMERASOLVER')


def register():
    operators.register()

    bpy.types.TOPBAR_MT_file_import.append(menu_func)


def unregister():
    operators.unregister()
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)
