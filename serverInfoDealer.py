# coding=utf-8
# @auth: applex
# @date: 2018-03-31

from simpleThreadPool import SimpleThreadPool
from support import *
from infoDealer import *

_REPORT_FILE_PATH = "./server_reports"
_REPORT_FILE_NAME_PRE = "report_"


def handle_message(server_callback, address, message):
    print_log("handle_message", address, message)
    if message:
        report = message
        user = get_user_from_report(report)
        print_log("handle_message: user=", user)
        user_name = get_name_from_user(user)
        user_id = get_id_from_user(user)
        date, time = get_date_time()
        if server_callback:
            server_callback("message", "%s-%s 接收到客户端%s %s [%s] 的日报\n"
                            % (date, time, user_name, user_id, address))
        SimpleThreadPool.submit(execute=_save_report_to_file,
                                args=(user_name, user_id, date, server_callback, report))


def _save_report_to_file(user_name, user_id, date, server_callback, report):
    if report:
        if server_callback:
            server_callback("message", "正在存储%s %s的日报\n" % (user_name, user_id))
            report_path = _REPORT_FILE_PATH + "/" + date
            report_name = _REPORT_FILE_NAME_PRE + "_" + user_name + "_" + user_id + "_" + date
            if save_report(report_path, report_name, report):
                server_callback("message", "%s %s的日报已存储至[%s]\n\n"
                                % (user_name, user_id, report_path + "/" + report_name))
            else:
                server_callback("message", "%s %s的日报存储失败[%s]\n\n"
                                % (user_name, user_id, report_name + "/" + report_name))
