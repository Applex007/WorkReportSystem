# coding=utf-8
# @auth: applex
# @date: 2018-03-31

import os
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Color, Font, Alignment
from openpyxl.styles.colors import *
from infoDealer import *
from support import *

_EXCEL_FILE_PATH = "./server_reports"
_EXCEL_FILE_NAME_PRE   = "日报汇总"

_EXCEL_SHEET_NAME    = "日报"
_COLUMN_USER_NAME   = "姓名"
_COLUMN_USER_ID     = "工号"
_COLUMN_INFO_DATE   = "日期"
_COLUMN_INFO_PLAN   = "计划日报"
_COLUMN_INFO_RESULT = "结果日报"

_ROW_HEAD = [_COLUMN_USER_NAME,
             _COLUMN_USER_ID,
             _COLUMN_INFO_DATE,
             _COLUMN_INFO_PLAN,
             _COLUMN_INFO_RESULT]


def handle_report_and_create_excel(server_callback):
    report_list = _read_report_form_files_in_path(server_callback)
    _write_reports_to_excel_file(report_list, server_callback)


def _read_report_form_files_in_path(server_callback):
    date = get_date_time()[0]
    file_path = _EXCEL_FILE_PATH + "/" + date
    report_list = []
    server_callback("message", "正在扫描日志文件目录：%s\n" % file_path)
    for root, sub_dirs, files in os.walk(file_path):
        for file_name in files:
            if file_name.find(date):
                # print_log(unicode("find file: %s/%s" % (root, file_name), "gbk"))
                report = read_report(root, file_name)
                report_list.append(report)
    if not report_list:
        if server_callback:
            server_callback("alert", "提示", "无日报文件！")
    return report_list


def _write_reports_to_excel_file(report_list, server_callback):
    date = get_date_time()[0]
    global _ROW_HEAD, _EXCEL_SHEET_NAME, _EXCEL_FILE_PATH
    wb = Workbook()
    excel_sheet = wb.active
    excel_sheet.title = unicode(_EXCEL_SHEET_NAME)
    excel_sheet.append(_ROW_HEAD)
    for report in report_list:
        user = get_user_from_report(report)
        user_name = get_name_from_user(user)
        user_id = get_id_from_user(user)
        info = get_info_from_report(report)
        info_plan = get_plan_from_info(info)
        info_result = get_result_from_info(info)
        row = [user_name, user_id, date, info_plan, info_result]
        excel_sheet.append(row)
    rows = len(report_list) + 1  # include head row
    columns = len(_ROW_HEAD)
    # rows height
    for row in range(1, rows + 1):  # excel rows start at 1
        if row == 1:
            continue
        print_log("row=", row)
        excel_sheet.row_dimensions[row].height = 60
    # column width
    for column in range(ord('A'), ord('A') + columns):
            column_index = chr(column)
            if (column - ord('A')) < 2:
                excel_sheet.column_dimensions[column_index].width = 15
            elif (column - ord('A')) == 2:
                excel_sheet.column_dimensions[column_index].width = 30
            elif (column - ord('A')) > 2:
                excel_sheet.column_dimensions[column_index].width = 60
    # cell style
    for row in range(1, rows + 1):
        for column in range(ord('A'), ord('A') + columns):
            column_index = chr(column)
            ft_title = Font(name=u'宋体', size=14, color=BLACK, bold=True)
            ft_content = Font(name=u'宋体', size=12, color=BLACK, bold=False)
            align = Alignment(horizontal='left', vertical='center', wrap_text=True)
            if row == 1:
                excel_sheet[str(column_index) + str(row)].font = ft_title
            else:
                excel_sheet[str(column_index) + str(row)].font = ft_content
            excel_sheet[str(column_index) + str(row)].alignment = align

    file_name = _EXCEL_FILE_NAME_PRE + "_" + date
    try:
        excel_file_path = _EXCEL_FILE_PATH + "/" + file_name + ".xlsx"
        server_callback("message", "导出日志到Excel文件：%s\n" % excel_file_path)
        wb.save(unicode(excel_file_path))
        if server_callback:
            server_callback("message", "导出Excel文件成功！%s \n\n" % excel_file_path)
            server_callback("alert", "提示", "导出Excel文件成功！\n %s" % excel_file_path)
    except Exception as e:
        print_log("save excel file exception:", e)
        if server_callback:
            server_callback("message", "Excel文件保存失败，请检查文件是否被占用！%s\n\n" % excel_file_path)
            server_callback("alert", "警告", "Excel文件保存失败，请检查文件是否被占用！\n%s" % excel_file_path)
        return False



if __name__ == '__main__':
    handle_report_and_create_excel()