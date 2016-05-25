#!/usr/bin/env python3
import ffdb as db
from os import remove

file = "test1.dat"
db.file = file  # make sure we test on the test file, not the real db

# create an empty db file if it does not exist
f = open(file, 'w')
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


def main():
    test_list = [
        "test_returndb()",
        "test_dropdb()",
        "test_prependdb()",
        "test_appenddb()"
    ]
    for i in test_list:
        db.dropdb()
        exec(i)

    db.dropdb()
    print("All tests passed")
    remove(file)

if __name__ == "__main__":
    main()