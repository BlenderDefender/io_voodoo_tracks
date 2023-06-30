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

import os

from .dict.dict import decoding


def decode(path: str, decoding: dict) -> list:
    """Decode a file that holds data required for the donation system.

    Args:
        path (str): The path to the file
        decoding (dict): The mapping used for decoding.

    Returns:
        list: A list of decoded strings.
    """

    file = open(path, 'r')
    decoded = ""
    for line in file.readlines():
        line = line.split(",")
        for char in line:
            decoded += decoding[char]

    file.close()
    decoded = decoded.split(" ")
    if decoded[0] == "BlenderDefender":
        return decoded
    else:
        return "ERROR"


def setup_addons_data(data: str) -> str:
    """Setup the data required for IO Voodoo Tracks.

    Args:
        data (str): The data to save to the data dir.

    Returns:
        str: The path of the data directory.
    """

    path = os.path.join(os.path.expanduser("~"), "Blender Addons Data", "io-voodoo-tracks")
    if not os.path.isdir(path):
        os.makedirs(path)

    if "IO.db" in os.listdir(path):
        return path
    else:
        file = open(os.path.join(path, "IO.db"), "w+")
        file.write(data)
        file.close()
        return path


def update_db() -> str:
    """Update the database file.

    Returns:
        str: Status message, if the update was successful.
    """

    path = os.path.join(os.path.expanduser("~"), "Blender Addons Data", "io-voodoo-tracks", "IO.db")

    file = open(path, "a")
    file.write(" dn8To&9gA")
    file.close()
    return "Upgrade to donation version."


def upgrade(path: str, decoding: dict, password: str) -> str:
    """Function for upgrading to the donator version.

    Args:
        path (str): The path of the data directory.
        decoding (dict): The mapping used for decoding
        password (str): The passkey, that donation users get.

    Returns:
        str: Status, whether the upgrade was successful.
    """

    password_list = decode(path, decoding)
    path = os.path.join(os.path.expanduser("~"), "Blender Addons Data", "io-voodoo-tracks", "IO.db")
    try:
        file = open(path, "r")
        if password_list[1].split("=")[0] == file.read().split("=")[0]:
            if password in password_list:
                file.close()
                return update_db()
            else:
                file.close()
                return "Password invalid. If you think this is a misstake, please report a bug."
        else:
            file.close()
            return "Database file corrupted. Checkout issue #5 for help."
        file.close()
    except:
        return "Database file corrupted. Checkout issue #5 for help."


def check_free_donation_version() -> str:
    """Check, whether the user is using the free version or the donation version.

    Returns:
        str: Status in {"free", "donation", "database_file_corrupted"}
    """

    data = decode(os.path.join(os.path.expanduser("~"),
                               "Blender Addons Data",
                               "io-voodoo-tracks",
                               "data.blenderdefender"),
                  decoding)
    path = os.path.join(setup_addons_data(data[1]), "IO.db")

    file = open(path, "r")
    content = file.read()
    content = content.split(" ")
    if len(content) == 1:
        file.close()
        return "free"
    elif len(content) == 2:
        file.close()
        return "donation"
    elif len(content) > 2:
        file.close()
        return "database_file_corrupted"


def url() -> str:
    """Decode the URL that leads to the website that grants benefits to donation users.

    Returns:
        str: The decoded URL.
    """

    path = os.path.join(os.path.expanduser("~"), "Blender Addons Data", "io-voodoo-tracks", "data.blenderdefender")
    return decode(path, decoding)[2]
