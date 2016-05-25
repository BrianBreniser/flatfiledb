#!/usr/bin/env python3
import ffdb as db
from os import remove

file = "test1.dat"
testfile = "infile.txt"
db.file = file  # make sure we test on the test file, not the real db

# create an empty db file if it does not exist
f = open(file, 'w')
f.close()

data = "STB|TITLE|PROVIDER|DATE|REV|VIEW_TIME\nstb1|the matrix|warner bros|2014-04-01|4.00|1:30\nstb1|unbreakable|buena vista|2014-04-03|6.00|2:05\nstb2|the hobbit|warner bros|2014-04-02|8.00|2:45\nstb3|the matrix|warner bros|2014-04-02|4.00|1:05\n"

f = open(testfile, 'w')
f.write(data)
f.close()

def test_prependdb():
    db.appenddb("asdf\n")
    assert(db.returndb() == ["asdf\n"])
    db.appenddb("qwer\n")
    assert(db.returndb() == ["asdf\n", "qwer\n"])
    db.prependdb("zxcv\n")
    assert(db.returndb() == ["zxcv\n", "asdf\n", "qwer\n"])
    db.prependdb("uiop\n")
    assert(db.returndb() == ["uiop\n", "zxcv\n", "asdf\n", "qwer\n"])

def test_appenddb():
    db.appenddb("asdf\n")
    assert(db.returndb() == ["asdf\n"])
    db.appenddb("qwer\n")
    assert(db.returndb() == ["asdf\n", "qwer\n"])
    db.appenddb("zxcv\n")
    assert(db.returndb() == ["asdf\n", "qwer\n", "zxcv\n"])

def test_returndb():
    assert(db.returndb() == [])
    db.appenddb("asdf\n")
    assert(db.returndb() == ["asdf\n"])
    db.appenddb("asdf\n")
    assert(db.returndb() == ["asdf\n", "asdf\n"])
    db.appenddb("asdf\n")
    assert(db.returndb() == ["asdf\n", "asdf\n", "asdf\n"])

def test_dropdb():
    assert(db.returndb() == [])
    db.appenddb("asdf\n")
    db.appenddb("asdf\n")
    db.appenddb("asdf\n")
    assert(db.returndb() == ["asdf\n", "asdf\n", "asdf\n"])
    db.dropdb()
    assert(db.returndb() == [])

def test_matchfound():
    data = [
            "stb1,the matrix,warner bros,2014-04-01,4.00,1:30\n",

            "stb2,the matrix,warner bros,2014-04-01,4.00,1:30\n",
            "stb1,not the matrix,warner bros,2014-04-01,4.00,1:30\n",
            "stb1,the matrix,not warner,2014-04-01,4.00,1:30\n",

            "stb1,the matrix,warner bros,2014-04-11,4.00,1:30\n",
            "stb1,the matrix,warner bros,2014-04-01,5.00,1:30\n",
            "stb1,the matrix,warner bros,2014-04-01,4.00,2:30\n",
            ]
    for i in data:
        db.appenddb(i)
    assert(db.matchfound("stb1", "the matrix", "warner bros") == True)
    assert(db.matchfound("stb2", "the matrix", "warner bros") == True)
    assert(db.matchfound("stb1", "matrix", "warner bros") == False)
    assert(db.matchfound("stb1", "matrix", "warner brotherererer") == False)

def test_loadfiletodb():
    db.loadfiletodb(testfile)
    assert(db.returndb() == ['stb1,the matrix,warner bros,2014-04-01,4.00,1:30\n',
           'stb1,unbreakable,buena vista,2014-04-03,6.00,2:05\n',
           'stb2,the hobbit,warner bros,2014-04-02,8.00,2:45\n',
           'stb3,the matrix,warner bros,2014-04-02,4.00,1:05\n'])

    db.loadfiletodb(testfile)
    assert(db.returndb() == ['stb1,the matrix,warner bros,2014-04-01,4.00,1:30\n',
           'stb1,unbreakable,buena vista,2014-04-03,6.00,2:05\n',
           'stb2,the hobbit,warner bros,2014-04-02,8.00,2:45\n',
           'stb3,the matrix,warner bros,2014-04-02,4.00,1:05\n'])

def main():
    # This feels like a hack and is possibly overcomplicated but for now I think it's fine
    test_list = [
        "test_returndb()",
        "test_dropdb()",
        "test_prependdb()",
        "test_matchfound()",
        "test_loadfiletodb()",
        "test_appenddb()"
    ]
    for i in test_list:
        db.dropdb()  # start with a fresh db in between tests
        exec(i)

    db.dropdb()  # clean up db one last time from last test
    print("All tests passed")  # This gives me a good feeling inside
    remove(file)  # clean files from main directory
    remove(testfile)  # clean files from main directory

if __name__ == "__main__":
    main()

