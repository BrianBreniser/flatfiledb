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

def loadfiletodb(file):
    with open(file, 'r') as f:
        f.readline()  # ignore header
        while f.readline()  # rest of the file

def main():
    datain = "infile.txt"

    print("Before:\n\n")
    printdb()

    print("after\n\n")
    printdb()

    print("DROPPING DATABASE!!!")
    dropdb()

if __name__ == "__main__":
    main()
