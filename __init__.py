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
    "version": (1, 0, 2),
    "blender": (2, 82, 0),
    "location": "View3D > Object > Import > Open Voodo Camera Track",
    "description": "Import Voodoo Camera Tracker Scripts (for Blender 2.5) to Blender 2.8x the easy way!",
    "warning": "",
    "wiki_url": "https://github.com/BlenderDefender/io_voodoo_tracks",
    "tracker_url": "https://github.com/BlenderDefender/io_voodoo_tracks/issues",
    "category": "Import-Export"}

import bpy
import os 

from bpy.props import StringProperty, BoolProperty 
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator 

# updater ops import, all setup in this file
from . import addon_updater_ops

#-----------------------------------------------------------------
# Main Operator, opening, editing and executing the Voodoo Script
#-----------------------------------------------------------------

class OT_IO_ImportVoodooTrack(Operator, ImportHelper):
 """Import Voodoo Camera Tracker Script (for Blender 2.5, will be automaticly converted)"""
 bl_idname = "open.voodoo_track"
 bl_label = "Open Voodo Camera Track (.py)"
 
 def execute(self, context):
  """Convert the selected file from 2.5 to 2.8"""

#------switch to Text-Editor-----------
  bpy.context.area.ui_type = 'TEXT_EDITOR'

#------call the File Browser-----------  
  bpy.ops.text.open(filepath=self.filepath)

#------edit the Script-----------------
  bpy.ops.text.jump(line=16)
  bpy.ops.text.select_line()
  
  bpy.context.space_data.find_text = "scene"
  bpy.context.space_data.replace_text = "bpy.context.collection"

  bpy.ops.text.find()
  bpy.ops.text.replace()
  bpy.ops.text.replace()
  bpy.ops.text.replace()
  
  bpy.ops.text.jump(line=19)
  bpy.ops.text.select_line()
  bpy.ops.text.delete()
  
  bpy.ops.text.jump(line=27)
  bpy.ops.text.select_line()
  bpy.ops.text.delete()
  
  bpy.ops.text.jump(line=30)
  bpy.ops.text.select_line()
  bpy.ops.text.delete()

#-------run the Script-----------------  
  bpy.ops.text.run_script()

#------return to 3D View--------------- 
  bpy.context.area.ui_type = 'VIEW_3D'

#------make Camera active--------------
  bpy.data.objects['voodoo_render_cam'].select_set(True)
  bpy.ops.view3d.object_as_camera()

  return {'FINISHED'}

#-----------------------------------------------------------------
# Import Menu
#-----------------------------------------------------------------

class Voodoo_Tracking_Menu(bpy.types.Menu):
    bl_idname = 'menu.import_voodoo'
    bl_label = 'Import'

    def draw(self, context):
        layout = self.layout
        layout.operator(OT_IO_ImportVoodooTrack.bl_idname, icon = 'CON_CAMERASOLVER')
#-----------------------------------------------------------------

def menu_func(self, context):
    self.layout.menu(Voodoo_Tracking_Menu.bl_idname)


class DemoPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	# addon updater preferences

	auto_check_update = bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False,
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

		# updater draw function
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
	DemoPreferences,
	OT_IO_ImportVoodooTrack,
	Voodoo_Tracking_Menu,
	
)


def register():
	# addon updater code and configurations
	# in case of broken version, try to register the updater first
	# so that users can revert back to a working version
	addon_updater_ops.register(bl_info)

	bpy.types.VIEW3D_MT_object.append(menu_func)

	# register the example panel, to show updater buttons
	for cls in classes:
		addon_updater_ops.make_annotations(cls) # to avoid blender 2.8 warnings
		bpy.utils.register_class(cls)


def unregister():
	# addon updater unregister
	addon_updater_ops.unregister()

	bpy.types.VIEW3D_MT_object.remove(menu_func)

	# register the example panel, to show updater buttons
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
