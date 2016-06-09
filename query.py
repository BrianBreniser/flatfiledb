#!/usr/bin/env python3
import os as os

# a dirty dirty global and I don't care
filedir = 'db/'

def sel(sel_list, old_list):
    new_list = []  # the new list with only the required options selected

    if not isinstance(sel_list, list):
        return "select failed, first arg must be list"
    if not isinstance(old_list, list):
        return "select fail, second arg must be list"

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

def ord(order_list, old_list):
    new_list = []

    
    
    return new_list


def _returndb():
    x = []

    for i in os.listdir(filedir):
        with open(filedir+i, 'r') as f:
            x += f.readlines()

    return x
