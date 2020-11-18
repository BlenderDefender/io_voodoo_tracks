from dict.dict import decoding

def decode(path, decoding):

    f = open(path, 'r')
    a = ""
    for line in f.readlines():
        l = line.split(",")
        for c in l:
            a += decoding[c]

    f.close()
    a = a.split(" ")
    return a

print(decode('data.blenderdefender', decoding))