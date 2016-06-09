#!/usr/bin/env python3
import store as db
import query as q
from os import remove, removedirs, makedirs, path

filedir = "testdb/"
testfile = "infile.txt"  # test input file
anothertestfile = "secondinfile.txt"  # second test input file
db.filedir = filedir

# create an empty db file directory
if path.exists(filedir):
    removedirs(filedir)
makedirs(filedir)

data = "STB|TITLE|PROVIDER|DATE|REV|VIEW_TIME\nstb1|the matrix|warner bros|2014-04-01|4.00|1:30\nstb1|unbreakable|buena vista|2014-04-03|6.00|2:05\nstb2|the hobbit|warner bros|2014-04-02|8.00|2:45\nstb3|the matrix|warner bros|2014-04-02|4.00|1:05\n"
moredata = "STB|TITLE|PROVIDER|DATE|REV|VIEW_TIME\nstb3|the matrix|warner bros|2014-04-02|4.00|1:05\nstb3|new made up movie| buena vista|2014-04-03|6.00|2:05\n"

f = open(testfile, 'w')
f.write(data)
f.close()

f = open(anothertestfile, 'w')
f.write(moredata)
f.close()

def test_appenddb():
    db._appenddb("asdf\n")
    assert(db._returndb() == ["asdf\n"])
    db._appenddb("qwer\n")
    assert(db._returndb() == ["asdf\n", "qwer\n"])
    db._appenddb("zxcv\n")
    assert(db._returndb() == ["asdf\n", "qwer\n", "zxcv\n"])

def test_returndb():
    assert(db._returndb() == [])
    db._appenddb("asdf\n")
    assert(db._returndb() == ["asdf\n"])
    db._appenddb("asdf\n")
    assert(db._returndb() == ["asdf\n", "asdf\n"])
    db._appenddb("asdf\n")
    assert(db._returndb() == ["asdf\n", "asdf\n", "asdf\n"])

def test_dropdb():
    assert(db._returndb() == [])
    db._appenddb("asdf\n")
    db._appenddb("asdf\n")
    db._appenddb("asdf\n")
    assert(db._returndb() == ["asdf\n", "asdf\n", "asdf\n"])
    db.dropdb()
    assert(db._returndb() == [])

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
        db._appenddb(i)
    assert(db.matchfound("stb1", "the matrix", "warner bros") == True)
    assert(db.matchfound("stb2", "the matrix", "warner bros") == True)
    assert(db.matchfound("stb1", "matrix", "warner bros") == False)
    assert(db.matchfound("stb1", "matrix", "warner brotherererer") == False)

def test_loadfiletodb():
    no_list_changes = ['stb1,the matrix,warner bros,2014-04-01,4.00,1:30\n',
                       'stb1,unbreakable,buena vista,2014-04-03,6.00,2:05\n',
                       'stb2,the hobbit,warner bros,2014-04-02,8.00,2:45\n',
                       'stb3,the matrix,warner bros,2014-04-02,4.00,1:05\n']

    one_change = no_list_changes + ["stb3,new made up movie, buena vista,2014-04-03,6.00,2:05\n"]

    db.loadfiletodb(testfile)
    assert(db._returndb() == no_list_changes)

    db.loadfiletodb(testfile)
    assert(db._returndb() == no_list_changes)

    db.loadfiletodb(anothertestfile)
    assert(db._returndb() == one_change)

def test_select():
    no_list_changes = ['stb1,the matrix,warner bros,2014-04-01,4.00,1:30\n',
                       'stb1,unbreakable,buena vista,2014-04-03,6.00,2:05\n',
                       'stb2,the hobbit,warner bros,2014-04-02,8.00,2:45\n',
                       'stb3,the matrix,warner bros,2014-04-02,4.00,1:05\n']

    sel_list = ['stb1,the matrix,warner bros\n',
                'stb1,unbreakable,buena vista\n',
                'stb2,the hobbit,warner bros\n',
                'stb3,the matrix,warner bros\n']

    db.loadfiletodb(testfile)
    assert(db._returndb() == no_list_changes)

    search_me = db._returndb()
    search_by = ["stb", "title", "provider"]

    assert(q.sel(search_by, search_me) == sel_list)

def test_order():
    orig_order = ['1,matrix,warner bros,2014-04-01,4.00,1:30\n',
                  '3,matrix,warner bros,2014-04-02,4.00,1:05\n',
                  '2,hobbit,warner bros,2014-04-02,8.00,2:45\n']

    new_order = ['1,matrix,warner bros,2014-04-01,4.00,1:30\n',
                 '2,hobbit,warner bros,2014-04-02,8.00,2:45\n',
                 '3,matrix,warner bros,2014-04-02,4.00,1:05\n']

    a_new_order = ['2,hobbit,warner bros,2014-04-02,8.00,2:45\n',
                   '1,matrix,warner bros,2014-04-01,4.00,1:30\n',
                   '3,matrix,warner bros,2014-04-02,4.00,1:05\n']

    assert(q.orde('stb', orig_order) == new_order)
    assert(q.orde('title', orig_order) == a_new_order)

def test_filter():
    no_filter = ['1,matrix,warner bros,2014-04-01,4.00,1:30\n',
                 '3,matrix,warner bros,2014-04-02,4.00,1:05\n',
                 '2,hobbit,warner bros,2014-04-02,8.00,2:45\n']

    yes_filter = ['1,matrix,warner bros,2014-04-01,4.00,1:30\n']

    assert(q.fil([['stb', '1']], no_filter) == yes_filter)

    other_no_filter = ['stb1,the matrix,warner bros,2014-04-01,4.00,1:30\n',
                       'stb1,unbreakable,buena vista,2014-04-03,6.00,2:05\n',
                       'stb2,the hobbit,warner bros,2014-04-02,8.00,2:45\n',
                       'stb3,the matrix,warner bros,2014-04-02,4.00,1:05\n']

    other_yes_filter= ['stb1,the matrix,warner bros,2014-04-01,4.00,1:30\n',
                       'stb1,unbreakable,buena vista,2014-04-03,6.00,2:05\n']

    assert(q.fil([['stb', 'stb1']], other_no_filter) == other_yes_filter)

def main():
    # This feels like a hack and is possibly overcomplicated but for now I think it's fine
    test_list = [
        "test_returndb()",
        "test_matchfound()",
        "test_loadfiletodb()",
        "test_appenddb()",
        "test_dropdb()",
        "test_order()",
        "test_filter()",
        "test_select()"
    ]
    for i in test_list:
        db.dropdb()  # start with a fresh db in between tests
        exec(i)

    db.dropdb()  # clean up db one last time from last test
    print("All tests passed")  # This gives me a good feeling inside
    removedirs(filedir)  # clean files from main directory
    remove(testfile)  # clean files from main directory
    remove(anothertestfile)  # clean files from main directory

if __name__ == "__main__":
    main()

