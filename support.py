# coding=utf-8
# @auth: applex
# @date: 2018-03-28
import sys
reload(sys)

DEBUG = True

def print_log(*args):
    global DEBUG
    if DEBUG:
       print _get_str(args)

def _get_str(arg):
    str = ""
    if type(arg) == list \
        or type(arg) == tuple \
        or type(arg) == set:
        for carg in arg:
            str = str + _get_str(carg)
    elif type(arg) == dict:
        for key in arg:
            str = "%s" %key + ":" + _get_str(arg[key])
    elif arg:
        str = str + "%s " %arg

    return str