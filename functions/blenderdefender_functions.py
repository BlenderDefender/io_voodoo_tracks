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

from os import path as p


def decrypt(path: str, password: str) -> list:
    """Decode a file that holds data required for the donation system.

    Args:
        path (str): The path to the file
        passwort (str): The password for decrypting the file

    Returns:
        list: A list of decoded strings.
    """

    try:
        with open(path, "rb") as f:
            decoded = one_time_pad(f.read(), password).decode()
    except UnicodeDecodeError:
        return "ERROR"

    decoded = decoded.split(" ")
    if decoded[0] == "BlenderDefender":
        return decoded

    return "ERROR"


def upgrade(path: str, password: str) -> str:
    """Function for upgrading to the donator version.

    Args:
        path (str): The path of the data directory.
        password (str): The password, that donation users get.

    Returns:
        str: Status, whether the upgrade was successful.
    """

    data = decrypt(path, password)

    if data == "ERROR":
        return "Invalid password. If you think this is a mistake, please report a bug."

    path = p.join(p.expanduser(
        "~"), "Blender Addons Data", "io-voodoo-tracks", "IO.db")

    with open(path, "w+", encoding="utf-8") as f:
        f.write(password)

    return "Upgrade successfull!"


def check_free_donation_version() -> str:
    """Check, whether the user is using the free version or the donation version.

    Returns:
        str: Status in {"free", "donation"}
    """
    data_dir = p.join(p.expanduser(
        "~"), "Blender Addons Data", "io-voodoo-tracks")

    with open(p.join(data_dir, "IO.db"), "r") as f:
        password: str = f.read()

    data = decrypt(p.join(data_dir, "data.blenderdefender"), password)

    if data == "ERROR":
        return "free"

    return "donation"


def url() -> str:
    """Decode the URL that leads to the website that grants benefits to donation users.

    Returns:
        str: The decoded URL.
    """
    data_dir = p.join(p.expanduser(
        "~"), "Blender Addons Data", "io-voodoo-tracks")

    with open(p.join(data_dir, "IO.db"), "r") as f:
        password: str = f.read()

    return decrypt(p.join(data_dir, "data.blenderdefender"), password)[1]


def one_time_pad(input: bytes, password: str):
    password = password.encode()
    output_bytes = []

    for i, byte in enumerate(input):
        output_bytes.append(byte ^ password[i % len(password)])

    return bytes(output_bytes)
