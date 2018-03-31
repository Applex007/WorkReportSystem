# coding=utf-8
# @auth: applex
# @date: 2018-03-31

from infoDealer import *

_USER_FILE_PATH = "./client_user"
_USER_FILE_NAME = "user_cfg"

_REPORT_FILE_PATH = "./client_reports"
_REPORT_FILE_NAME_PRE = "report_"


def save_user_to_file(user):
    return save_user(_USER_FILE_PATH, _USER_FILE_NAME, user)


def read_user_from_file():
    return read_user(_USER_FILE_PATH, _USER_FILE_NAME)


def save_report_to_file(report):
    return save_report(_REPORT_FILE_PATH, _REPORT_FILE_NAME_PRE + get_date_time()[0], report)


def read_report_from_file():
    return read_report(_REPORT_FILE_PATH, _REPORT_FILE_NAME_PRE + get_date_time()[0])



