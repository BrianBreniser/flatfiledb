#!/usr/bin/env python3
import os as os

# a dirty dirty global and I don't care
filedir = 'db/'

def _printdb():
    for i in os.listdir(filedir):
        with open(filedir+i, 'r') as f:
            for j in f.readlines():
                print(j, end="")

def dropdb():
    for i in os.listdir(filedir):
        os.remove(filedir+i)

def _returndb():
    x = []

    for i in os.listdir(filedir):
        with open(filedir+i, 'r') as f:
            x += f.readlines()

    return x

def _appenddb(text):
    list_of_files = os.listdir(filedir)

    if len(list_of_files) == 0:
        with open(filedir+"1.dat", 'w') as f:
            f.write(text)
    else:
        filesize = os.path.getsize(filedir+list_of_files[-1])

        if filesize > 1000000:  # consider 1 mb portions only
            # latest file is over 1mb, make a new file
            fn = "{}.dat".format(len(list_of_files) + 1)
            with open(filedir+fn, 'w') as f:
                f.write(text)
        else:
            # Just write the data to the last file, still < 1mb
            with open(filedir+list_of_files[-1], 'a') as f:
                f.write(text)

def loadfiletodb(infile):
    with open(infile, 'r') as f:
        f.readline()  # ignore header
        for i in f.readlines():  # rest of the file
            if i == "\n":
                continue
            a = i.split("|")
            stb, title, provider, date, rev, view_time = a
            if not matchfound(stb, title, provider):
                view_time = view_time.strip("\n")
                data = "{},{},{},{},{},{}\n".format(stb, title, provider, date, rev, view_time)
                _appenddb(data)

def matchfound(stb, title, provider):
    for i in os.listdir(filedir):
        with open(filedir+i, 'r') as f:
            for i in f.readlines():
                if i == "\n" or i == "":
                    continue
                i = i.split(",")
                if i[0] == stb and i[1] == title and i[2] == provider:
                    return True  # this constitutes a match
        
        return False  # no match found

def testashitload():
    for i in range(1, 100001):
        data = "stb{}|the matrix2|warner bros|2014-04-01|4.00|1:30\n".format(i)
        _appenddb(data)


def main():

    infile = "infile.txt"
    data = "STB|TITLE|PROVIDER|DATE|REV|VIEW_TIME\n\
stb1|the matrix2|warner bros|2014-04-01|4.00|1:30\n"

    f = open(infile, 'w')
    f.write(data)
    f.close()

    print("Before:\n\n")
    _printdb()

    loadfiletodb(infile)

    print("after\n\n")
    _printdb()

    os.remove(infile)

if __name__ == "__main__":
    main()
