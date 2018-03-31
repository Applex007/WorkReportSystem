# coding=utf-8
# @auth: applex
# @date: 2018-03-31

from fileSupport import *
from support import *

REPORT = "report"

USER = "user"
USER_NAME      = "user_name"
USER_ID        = "user_id"
USER_SERVER_IP   = "user_server_ip"

INFO = "info"
INFO_DATE    = "info_date"
INFO_PLANE   = "info_plan"
INFO_RESULT  = "info_result"


def set_report(user, info):
        return {REPORT:
                    {USER: user,
                     INFO: info
                    }
        }


def get_user_from_report(report):
    if type(report) == dict:
        report_content = report[REPORT]
        if type(report_content) == dict:
            return report_content[USER]


def get_info_from_report(report):
    if type(report) == dict:
        report_content = report[REPORT]
        if type(report_content) == dict:
            return report_content[INFO]


def set_user(user_name, user_id, user_server_ip=None):
    return {USER_NAME: user_name,
            USER_ID: user_id,
            USER_SERVER_IP: user_server_ip
           }


def get_name_from_user(user):
    if type(user) == dict:
        return user[USER_NAME]


def get_id_from_user(user):
    if type(user) == dict:
        return user[USER_ID]


def get_server_ip_from_user(user):
    if type(user) == dict:
        return user[USER_SERVER_IP]


def set_info(info_date, info_plan, info_result):
    return {INFO_DATE: info_date,
            INFO_PLANE: info_plan,
            INFO_RESULT: info_result
            }


def get_date_form_info(info):
    if type(info) == dict:
        return info[INFO_DATE]


def get_plan_from_info(info):
    if type(info) == dict:
        return info[INFO_PLANE]


def get_result_from_info(info):
    if type(info) == dict:
        return info[INFO_RESULT]


def save_user(file_path, file_name, user):
    print_log("save_user_to_file: user=", user)
    if user:
        user_content = json_encode(user)
        # print_log("save_user_to_file: user=", user)
        return save_file(file_path, file_name, user_content)


def read_user(file_path, file_name):
    user_content = read_file(file_path, file_name)
    # print_log("read_user_from_file: user_content=", user_content)
    if user_content:
        try:
            return json_decode(user_content)
        except Exception as e:
            print_log("read_user_from_file:", e)
            remove_file(file_path, file_name)


def save_report(file_path, file_name, report):
    # print_log("save_report_to_file: user=", report)
    if report:
        report_content = json_encode(report)
        return save_file(file_path, file_name, report_content)


def read_report(file_path, file_name):
    report_content = read_file(file_path, file_name)
    # print_log("read_report_from_file: report_content=", report_content)
    if report_content:
        try:
            return json_decode(report_content)
        except Exception as e:
            print_log("read_report_from_file:", e)
            remove_file(file_path, file_name)
