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
    BoolProperty,
    IntProperty
)
from bpy.types import (
    AddonPreferences,
    Context,
    UILayout,
)

from . import addon_updater_ops

from .functions.blenderdefender_functions import check_free_donation_version, url


class IOVOODOOTRACKS_APT_addon_preferences(AddonPreferences):
    bl_idname = __package__

    # addon updater preferences

    auto_check_update: BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )
    updater_intrval_months: IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days: IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours: IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes: IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context: 'Context'):
        layout: 'UILayout' = self.layout
        # col = layout.column() # works best if a column, or even just self.layout
        mainrow = layout.row()
        # col = mainrow.column()

        donation_status = check_free_donation_version()

        if donation_status == "free":
            layout.operator("wm.url_open", text="Checkout Gumroad for other addons and more...",
                            icon='FUND').url = "https://gumroad.com/blenderdefender"
            layout.label(
                text="IO Voodoo Tracks - You are using the free version.")
            layout.label(
                text="If you want to support me and get cool discount codes, please upgrade to donation version. :)")
            layout.operator("voodoo_track.upgrade")
        elif donation_status == "donation":
            layout.label(
                text="IO Voodoo Tracks - You are using the donation version. Thank you :)", icon='FUND')
            layout.operator(
                "wm.url_open", text="Get discount code for cool Blender Products").url = url()
        elif donation_status == "database_file_corrupted":
            layout.operator("wm.url_open", text="Checkout Gumroad for other addons and more...",
                            icon='FUND').url = "https://gumroad.com/blenderdefender"
            layout.label(
                text="IO Voodoo Tracks - Databasefile corrupted! Please delete it.")
            layout.label(
                text="And please, stop messing around with .db files. Thanks :)")
            layout.operator("voodoo_track.upgrade",
                            text="Upgrade to donation version.")

        # could also pass in col as third arg
        if bpy.app.version < (4, 2):
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


def register_legacy(bl_info):
    # addon updater code and configurations
    # in case of broken version, try to register the updater first
    # so that users can revert back to a working version
    addon_updater_ops.register(bl_info)

    # register the example panel, to show updater buttons
    for cls in classes:
        addon_updater_ops.make_annotations(
            cls)  # to avoid blender 2.8 warnings
        bpy.utils.register_class(cls)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    # addon updater unregister
    addon_updater_ops.unregister()

    # register the example panel, to show updater buttons
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
