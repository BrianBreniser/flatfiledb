#!/usr/bin/env python3

# a dirty dirty global and I don't care
file = 'db/db1.dat'

def printdb():
    with open(file, 'r') as f:
        for i in f.readlines():
            print(i, end="")

def dropdb():
    f = open(file, 'w')
    f.close()

def returndb():
    with open(file, 'r') as f:
        x = f.readlines()
    return x

def appenddb(text):
    with open(file, 'a') as f:
        f.write(text)

def prependdb(text):
    with open(file, 'r+') as f:
        wholedb = f.read()
        newfile = text + wholedb

    with open(file, 'w') as f:
        f.write(newfile)

def loadfiletodb(infile):
    with open(infile, 'r') as f:
        f.readline()  # ignore header
        for i in f.readlines():  # rest of the file
            if i == "\n":
                continue
            i = i.split("|")
            sbt, title, provider, date, rev, view_time = i
            if not matchfound(sbt, title, provider):
                view_time = view_time.strip("\n")
                data = "{},{},{},{},{},{}\n".format(sbt, title, provider, date, rev, view_time)
                appenddb(data)

def matchfound(sbt, title, provider):
    with open(file, 'r') as f:
        for i in f.readlines():
            if i == "\n":
                continue
            i = i.split(",")
            if i[0] == sbt and i[1] == title and i[2] == provider:
                return True  # this constitutes a match
        return False  # no match found


def main():
    datain = "infile.txt"

    print("Before:\n\n")
    printdb()

    loadfiletodb("infile.txt")

    print("after\n\n")
    printdb()

if __name__ == "__main__":
    main()
