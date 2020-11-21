from .dict.dict import decoding

def decode(path, decoding):

    f = open(path, 'r')
    a = ""
    for line in f.readlines():
        l = line.split(",")
        for c in l:
            a += decoding[c]

    f.close()
    a = a.split(" ")
    if a[0] == "BlenderDefender":
        return a
    else:
        return "ERROR"


def setup_addons_data(data):
    import os
    path = os.path.join(os.path.expanduser("~"), "Blender Addons Data", "io-voodoo-tracks")
    if not os.path.isdir(path):
        os.makedirs(path)

    if "IO.db" in os.listdir(path):
        return path
    else:
        file = open(os.path.join(path, "IO.db"), "w+")
        # path2 = os.path.join(path, "data.blenderdefender")
        file.write(data) #decode(path2, decoding))#[1])
        file.close()
        return path


def update_db():
    import os
    path = os.path.join(os.path.expanduser("~"), "Blender Addons Data", "io-voodoo-tracks", "IO.db")

    file = open(path, "a")
    file.write(" dn8To&9gA")
    file.close()
    return "Upgrade to donation version."


def upgrade(path, decoding, password):
    import os
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
            return "Database file corrupted. Please reinstall the addon."
        file.close()
    except:
        return "Database file corrupted. Please reinstall the addon."


def f_d_version():
    import os
    data = decode(os.path.join(os.path.expanduser("~"), "Blender Addons Data", "io-voodoo-tracks", "data.blenderdefender"), decoding)
    path = os.path.join(setup_addons_data(data[1]), "IO.db")

    file = open(path, "r")
    c = file.read()
    c = c.split(" ")
    if len(c) == 1:
        file.close()
        return "free"
    elif len(c) == 2:
        file.close()
        return "donation"
    elif len(c) > 2:
        file.close()
        return "database_file_corrupted"
