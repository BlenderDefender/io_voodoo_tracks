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


def replace_wrong_lines(python_script_filepath: str):
    """Replace the lines that lead to errors with the Voodoo Tracker script.

    Args:
        python_script_filepath (str): The path of the python script that should be updated.
    """

    replace_texts = {"scene.objects.link(dummy)": "bpy.context.collection.objects.link(dummy)",
                     "data.lens_unit = 'DEGREES'": "",
                     "data.dof_distance = 0.0": "",
                     "data.draw_size = 0.5": "",
                     "scene.objects.link(mesh)": "bpy.context.collection.objects.link(mesh)",
                     "scene.objects.link(vcam)": "bpy.context.collection.objects.link(vcam)"}

    for line in fileinput.FileInput(python_script_filepath, inplace=True):
        for s in replace_texts:
            r = replace_texts[s]
            line = line.replace(s, r)
        print(line, end='')


def run_script(python_script_filepath):
    """Run the updated IO Voodoo Tracks Python Script.

    Args:
        python_script_filepath (str): The path to the script that should be executed.
    """

    subprocess.call([
        bpy.app.binary_path,
        '--background', '-noaudio',  # '-nojoystick',
        # os.path.abspath(bpy.data.filepath), # the current .blend file
        '--python',
        os.path.abspath(python_script_filepath)
    ])

    with open(python_script_filepath, 'r') as scriptfile:
        script_text = scriptfile.read()
    exec(script_text)
