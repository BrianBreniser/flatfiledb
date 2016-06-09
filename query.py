#!/usr/bin/env python3
import os as os

# a dirty dirty global and I don't care
filedir = 'db/'

def sel(sel_list, old_list):
    """ Use ord before calling sel"""
    if not isinstance(sel_list, list):
        return "select failed, first arg must be list"
    if not isinstance(old_list, list):
        return "select fail, second arg must be list"

    new_list = []  # the new list with only the required options selected

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

def ord(ord_by, old_list):
    if not isinstance(ord_by, str):
        return "select failed, first arg must be string"
    if not isinstance(old_list, list):
        return "select fail, second arg must be list"

    new_list = []
    lol = []  # list of lists

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
        lol.append(temp)

    # lol now contains a list of lists that can be ordered using sorted
    lol = sorted(lol, key=lambda x: x[k])

    # create our new list
    for i in lol:
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

    new_list = []

    for i in filter_list:
        k = 0
        # I reeealy wish Python had case statements
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

        for j in old_list:
            li = j.split(",")
            if li[k] == i[1]:
                new_list.append(j)

    return new_list

def main():
    return True

if __name__ == "__main__":
    main()
