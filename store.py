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
            # bug warning: after 9 files (9mb total size) appending work improperly
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
        
        return False

def main():
    from sys import argv

    if argv[1] == '-h':
        print("""
Welcome to the storage program

-h will display this message

In order to store a file call 

$ ./store.py 'filename'

without the quotes

if the file is not in the current directory please provide the full path
in the even the file is not found, please check the spelling

-d will destroy the database
              """)
        exit(0)

    elif argv[1] == '-d':
        response = input("Are you SURE you want to drop the database?? This cannot be undone:\n(y/n)-> ")

        if response == 'y':
            dropdb()
            exit(0)
        else:
            print("Did NOT drop the db, exiting")
            exit(0)

    elif argv[1] == '-p':
        print("printing whole database\n\n")
        _printdb()
        exit(0)

    loadfiletodb(argv[1])

if __name__ == "__main__":
    main()
