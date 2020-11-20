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
    "version": (1, 0, 5),
    "blender": (2, 83, 0),
    "location": "View3D > Object > Import > Open Voodo Camera Track",
    "description": "Import Voodoo Camera Tracker Scripts (for Blender 2.5) to Blender 2.8x the easy way!",
    "warning": "Checkout Gumroad for other Addons and more...",
    "wiki_url": "https://github.com/BlenderDefender/io_voodoo_tracks",
    "tracker_url": "https://github.com/BlenderDefender/io_voodoo_tracks/issues",
    "category": "Import-Export"}

import bpy
import os
import subprocess
import fileinput

from . import addon_updater_ops
from .functions.blenderdefender_functions import f_d_version

class IOVOODOOTRACKS_APT_addon_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # addon updater preferences

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context):
        layout = self.layout
        # col = layout.column() # works best if a column, or even just self.layout
        mainrow = layout.row()
        col = mainrow.column()

        layout.operator("wm.url_open", text="Checkout Gumroad for other addons and more...", icon='FUND').url = "https://gumroad.com/blenderdefender"
        if f_d_version() == "free":
            layout.label(text="IO Voodoo Tracks - You are using the free version.")
            layout.label(text="If you want to support me and get cool discount codes, please upgrade to donation version. :)")
            layout.operator("voodoo_track.upgrade")
        elif f_d_version() == "donation":
            layout.label(text="IO Voodoo Tracks - You are using the donation version. Thank you :)")
            layout.operator("wm.url_open", text="Get discount code for cool Blender Products").url="https://linktr.ee/5akW_ZE56dHsjaA"
        # could also pass in col as third arg
        addon_updater_ops.update_settings_ui(self, context)

        # Alternate draw function, which is more condensed and can be
        # placed within an existing draw function. Only contains:
        #   1) check for update/update now buttons
        #   2) toggle for auto-check (interval will be equal to what is set above)
        # addon_updater_ops.update_settings_ui_condensed(self, context, col)

        # Adding another column to help show the above condensed ui as one column
        # col = mainrow.column()
        # col.scale_y = 2
        # col.operator("wm.url_open","Open webpage ").url=addon_updater_ops.updater.website


classes = (
    IOVOODOOTRACKS_APT_addon_preferences,
)


def register():
    # addon updater code and configurations
    # in case of broken version, try to register the updater first
    # so that users can revert back to a working version
    addon_updater_ops.register(bl_info)

    # register the example panel, to show updater buttons
    for cls in classes:
        addon_updater_ops.make_annotations(cls)  # to avoid blender 2.8 warnings
        bpy.utils.register_class(cls)


def unregister():
    # addon updater unregister
    addon_updater_ops.unregister()

    # register the example panel, to show updater buttons
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
