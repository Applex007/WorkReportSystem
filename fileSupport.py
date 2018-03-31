# coding=utf-8
# @auth: applex
# @date: 2018-03-28

import os
from threading import Lock
from support import *

_mutex = Lock()

def save_file(file_path, file_name, content):
    global _mutex
    if not os.path.isdir(file_path):
        os.makedirs(file_path, 0666)
        print_log("save_file:", "make dir file_path")
    res = False
    try:
        _mutex.acquire()
        f = open(file_path+"/"+file_name, "w")
        f.write(content)
        res = True
    except Exception as e:
        print_log("save file:", file_path+"/"+file_name, e)
    finally:
        if f:
            f.close()
        _mutex.release()
        return res


def read_file(file_path, file_name):
    res = None
    if not os.path.isdir(file_path):
        print_log("read file:", "file_path is not dir")
        return res
    try:
        f = open(file_path+"/"+file_name, "r")
        res = f.read()
        # print_log("read file:", res)
    except Exception as e:
        print_log("read file:", file_path+"/"+file_name, e)
    finally:
        if f:
            f.close()
        return res


def remove_file(file_path, file_name):
    global _mutex
    res = False
    try:
        _mutex.acquire()
        os.remove(file_path+"/"+file_name)
        res = True
    except Exception as e:
        print_log("remove_file:", e)
    finally:
        _mutex.release()
        return res


def remove_dirs(file_path):
    res = False
    try:
        _mutex.acquire()
        os.removedirs(file_path)
        res = True
    except Exception as e:
        print_log("remove_dirs:", e)
    finally:
        _mutex.release()
        return res
