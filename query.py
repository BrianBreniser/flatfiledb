#!/usr/bin/env python3
import os as os

# a dirty dirty global and I don't care
filedir = 'db/'

def sel(sel_list, old_list):
    """ In the main program, this must be called last"""
    if not isinstance(sel_list, list):
        return "select failed, first arg must be list"
    if not isinstance(old_list, list):
        return "select fail, second arg must be list"

    new_list = []  # the new list with only the required rows selected

    # build the new_list, only included sel_list columns
    for i in old_list:
        new_line = ""
        old_line = i.split(",")
        stb, title, provider, date, rev, view_time = old_line

        # this feel super dirty, but I'm not sure of a better way yet
        if 'stb' in sel_list:
            new_line += "{},".format(stb)
        if 'title' in sel_list:
            new_line += "{},".format(title)
        if 'provider' in sel_list:
            new_line += "{},".format(provider)
        if 'date' in sel_list:
            new_line += "{},".format(date)
        if 'rev' in sel_list:
            new_line += "{},".format(rev)
        if 'view_time' in sel_list:
            new_line += "{},".format(view_time)

        new_line = new_line[:-1]  # chomp off last character, a dangling ','
        new_line= "{}\n".format(new_line)  # looking for '\n' later

        new_list.append(new_line)

    return new_list

def orde(ord_by, old_list):
    if not isinstance(ord_by, str):
        return "select failed, first arg must be string"
    if not isinstance(old_list, list):
        return "select fail, second arg must be list"

    new_list = []
    rowsAfterSplit = []

    k = 0

    # I reeealy wish Python had case statements
    if ord_by == "stb":
        k = 0
    elif ord_by == "title":
        k = 1
    elif ord_by == "provider":
        k = 2
    elif ord_by == "date":
        k = 3
    elif ord_by == "rev":
        k = 4
    elif ord_by == "view_time":
        k = 5

    for i in old_list:
        temp = i.split(",")
        rowsAfterSplit.append(temp)

    # rowsAfterSplit now contains a list of lists that can be ordered using sorted
    # This is the reason that currently I can only order by 1 item
    # I planned on using a meta function to build the lambda function below
    # That became too complicated, so I took the short cut that is there now
    rowsAfterSplit = sorted(rowsAfterSplit, key=lambda x: x[k])

    # create our new list, ordered
    for i in rowsAfterSplit:
        temp = ",".join(i)
        new_list.append(temp)
    
    return new_list


def fil(filter_list, old_list):
    if not isinstance(filter_list, list):
        return "select failed, first arg must be list"
    if not isinstance(filter_list[0], list):
        return "select failed, first arg must be list of lists"
    if not isinstance(old_list, list):
        return "select fail, second arg must be list"

    # This is very inefficient, I didn't have time to work on performance
    # this part of the algorithm got stuck in "it worked" phase, no
    # optimization was done here
    new_list = old_list[:]  # clone the list

    for i in filter_list:
        k = 0
        # I still really wish Python had case statements
        if i[0] == "stb":
            k = 0
        elif i[0] == "title":
            k = 1
        elif i[0] == "provider":
            k = 2
        elif i[0] == "date":
            k = 3
        elif i[0] == "rev":
            k = 4
        elif i[0] == "view_time":
            k = 5

        # building our new list, including filter.
        # this algorithm is very inefficient as it stands right now
        # With my time crunch I could not optimize this, so it stayed in the
        # "it worked" phase of development
        for j in old_list:
            li = j.split(",")
            if li[k] != i[1]:
                try:
                    new_list.remove(j)  # This is inefficient, should build up not break down
                except:
                    pass

    return new_list

def main():
    from sys import argv

    if len(argv) > 1:
        if argv[1] == '-h':
            print("""
Welcome to the query program

-h prints this message

-s is the select argument
use lower case column names, no spaces preferably, and include as many as you want
for example:
./query -s stb,title
will return from the database every line, but only the stb and title of each

-o is the order argument
use lower case column names, but at the moment can only accept one column
use like this:
./query -o title
will order all results by title, alphanumerically

-f is the filter argument
use it to limit the results you want to see, use it like so
./query -f stb=stb1,title="the matrix"
this will find only stb's that are equal to stb1
and only when the movie title was "the matrix"
notice: you use column=argument for each column to filter by
and separate column-arguments by comma
you can only use spaces if the space is in the name of the argument
such as in "the matrix", but you must surround the argument in quotes ""

Of course you can use these in tandem:
./query -s stb,title -o stb -f stb=stb1,title="the matrix"
will search for stb's that are stb1, with movie titles "the matrix"
will order alphabetically by stb
and will only display the stb and title columns
                  """)
            exit(0)

    select_list = []
    order = ""
    filter_list = []

    # I could have used a built in library for this, but I required some
    # specific syntax, and decided it was easier to just parse manually
    # In theory I would have done more research and found a library that
    # did exactly what I wanted. This works well for the time being though
    for i, v in enumerate(argv):
        if v == "-s":
            value = argv[i+1]
            select_list = value.split(',')

        elif v == "-o":
            order = argv[i+1]

        elif v == "-f":
            value = argv[i+1]
            outer_list = value.split(',')
            for j in outer_list:
                inner_list = j.split("=")
                filter_list.append(inner_list)

    query_list = []

    # this is also super inefficient right now, preferably I would go through
    # the db and run the filter function, so that I don't have to pull the
    # whole db into memory, which, part of the requirements state I need to
    # be able to pull in partial data, so right now this doesn't comply
    for i in os.listdir(filedir):
        with open(filedir+i, 'r') as f:
            query_list += f.readlines()

    if order:
        query_list = orde(order, query_list)
    if filter_list:
        query_list = fil(filter_list, query_list)
    if select_list:
        query_list = sel(select_list, query_list)

    # print our list we made
    for i in query_list:
        print(i, end="")

    return True

if __name__ == "__main__":
    main()
