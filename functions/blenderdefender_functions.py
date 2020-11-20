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
        return "File is invalid"


def create_db():
    file = open("functions/IO.db", "w+")
    file.write(decode('functions/data.blenderdefender', decoding)[1])
    file.close


def update_db():
    file = open("functions/IO.db", "a")
    file.write(" dn8To&9gA")
    file.close()
    return "Update DB"


def upgrade(path, decoding, password):
    password_list = decode(path, decoding)
    try:
        file = open("functions/IO.db", "r")
        if password_list[1].split("=")[0] == file.read().split("=")[0]:
            if password in password_list:
                file.close()
                return update_db()
            else:
                file.close()
                return "Password invalid. If you think this is a misstake, please report a bug."
        else:
            file.close()
            return "Database files corrupted."
        file.close()
    except:
        return "Database file corrupted."


def f_d_version():
    file = open("functions/IO.db", "r")
    c = file.read()
    c = c.split(" ")
    if len(c) > 1:
        file.close()
        return "donation"
    else:
        file.close()
        return "free"
