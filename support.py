# coding=utf-8
# @auth: applex
# @date: 2018-03-28
import sys
import json
import time as timer

reload(sys)
sys.setdefaultencoding('utf-8')

DEBUG = True


def print_log(*args):
    global DEBUG
    if DEBUG:
        print _get_str(args)


def _get_str(arg):
    str = ""
    if type(arg) == tuple:
        str = str + "("
        for carg in arg:
            str = str + _get_str(carg)
        str = str + ")"
    elif type(arg) == list:
        str = str + "list["
        for carg in arg:
            str = str + _get_str(carg)
        str = str + "]"
    elif type(arg) == set:
        str = str + "set["
        for carg in arg:
            str = str + _get_str(carg)
        str = str + "]"
    elif type(arg) == dict:
        str = str + "{"
        for key in arg:
            str = str + "%s" % key + ":" + _get_str(arg[key]) + ","
        str = str + "}"
    elif arg:
        str = str + "%s " % arg
    return str


def json_encode(obj):
    return json.dumps(obj)


def json_decode(str):
    str = unicode(str, errors='ignore')
    return json.loads(str)


def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(_root, width, height):
    screenwidth = _root.winfo_screenwidth()
    screenheight = _root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    print_log(size)
    _root.geometry(size)


def font_yh(size=10, style="normal"):
    return "微软雅黑", size, style


def font_fs(size=10, style="normal"):
    return "仿宋", size, style


def font(typeface="宋体", size=10, style="normal"):
    return typeface, size, style


def get_date_time():
    local = timer.localtime(timer.time())
    date = timer.strftime("%Y-%m-%d", local)
    time = timer.strftime("%H:%M:%S", local)
    return date, time


def check_chines(text):
    for ch in text.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def check_ip_single_value(number):
    if number == "":
        return True
    if not number.isdigit():
        print_log("check_ip_single_value: isdigit %s" % number.isdigit())
        return False
    if len(number) > 3:
        print_log("check_ip_single_value: isdigit %s" % len(number))
        return False
    value = int(number)
    if 0 <= value <= 254:
        print_log("check_ip_single_value: %d" % value)
        return True
    return False
