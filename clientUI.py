# coding=utf-8
# @auth: applex
# @date: 2018-03-28

from Tkinter import *
from tkMessageBox import *
from client import *
from ScrolledText import ScrolledText
from clientInfoDealer import *


def _submit_button_clicked():
    print_log("submit_button_clicked")
    if _check_report():
        _send_report()


def _save_user_button_clicked():
    if _check_user_name() \
            and _check_user_id() \
            and _check_user_server_ip():
        user = set_user(
            user_name=_get_user_name(),
            user_id=_get_user_id(),
            user_server_ip=_get_user_server_ip()
        )
        save_user_to_file(user)


def _load_user_form_file():
    user = read_user_from_file()
    user_name = get_name_from_user(user)
    user_id = get_id_from_user(user)
    user_server_ip = get_server_ip_from_user(user)
    if user_name:
        _infoEntry11.delete(0, END)
        _infoEntry11.insert(END, user_name)
    if user_id:
        _infoEntry12.delete(0, END)
        _infoEntry12.insert(END, user_id)
    if user_server_ip:
        _set_server_host_ip(user_server_ip)


def _load_report_form_file():
    report = read_report_from_file()
    print_log("read_report_from_file: report=", report)
    info = get_info_from_report(report)
    report_plan = get_plan_from_info(info)
    report_result = get_result_from_info(info)
    if report_plan:
        _infoText21.delete(1.0, END)
        _infoText21.insert(END, report_plan)
    if report_result:
        _infoText22.delete(1.0, END)
        _infoText22.insert(END, report_result)


def _check_report():
    return _check_user_id() \
           and _check_user_name() \
           and _check_user_server_ip() \
           and _check_info_plan() \
           and _check_info_result()


def _send_report():
    server_ip = _get_user_server_ip()
    report = set_report(
        set_user(_get_user_name(),
                 _get_user_id(),
                 server_ip
                 ),
        set_info(get_date_time()[0],
                 _get_info_plan(),
                 _get_info_result()
                 ),
    )
    save_report_to_file(report)
    global _client
    if _client.connect(server_ip):
        if _client.send_data(report):
            client.destroy()
            return True
    return False


def _check_user_name():
    if _get_user_name():
        return True
    else:
        _show_alert("提示", "请输入用户名！")
        return False


def _get_user_name():
    global _infoEntry11
    return _infoEntry11.get()


def _check_user_id():
    if _get_user_id():
        return True
    else:
        _show_alert("提示", "请输入ID！")
        return False


def _get_user_id():
    global _infoEntry12
    return _infoEntry12.get()


def _check_user_server_ip():
    if not _get_user_server_ip():
        _show_alert("提示", "服务端ip未配置，将默认使用本机ip！")
    return True


def _get_user_server_ip():
    return _get_server_host_ip()


def _check_info_plan():
    if _get_info_plan():
        return True
    else:
        _show_alert("提示", "请输入计划日报！")


def _get_info_plan():
    global _infoText21
    return _infoText21.get(0.0, END)


def _check_info_result():
    if _get_info_result():
        return True
    else:
        _show_alert("提示", "请输入结果日报！")


def _get_info_result():
    global _infoText22
    return _infoText22.get(0.0, END)


def _get_server_host_ip():
    global _infoEntry131, _infoEntry132
    global _infoEntry133, _infoEntry134
    v1 = _infoEntry131.get()
    v2 = _infoEntry132.get()
    v3 = _infoEntry133.get()
    v4 = _infoEntry134.get()
    ip = None
    if v1:
        ip = str(v1)
    else:
        return None
    if v2:
        ip = ip + "." + str(v2)
    else:
        return None
    if v3:
        ip = ip + "." + str(v3)
    else:
        return None
    if v4:
        ip = ip + "." + str(v4)
    else:
        return None
    return ip


def _set_server_host_ip(host_ip):
    if host_ip:
        ip_values_list = host_ip.split(".")
        if len(ip_values_list) == 4:
            _infoEntry131.delete(0, END)
            _infoEntry132.delete(0, END)
            _infoEntry133.delete(0, END)
            _infoEntry134.delete(0, END)
            _infoEntry131.insert(END, ip_values_list[0])
            _infoEntry132.insert(END, ip_values_list[1])
            _infoEntry133.insert(END, ip_values_list[2])
            _infoEntry134.insert(END, ip_values_list[3])


def client_callback(*args):
    if not args:
        print_log("clientUI: callback do noting", args)
        return None
    if args[0] == "message":
        return _show_message(message=args[1])
    elif args[0] == "alert":
        return _show_alert(head=args[1], meg=args[2])
    elif args[0] == "option":
        return _call_func(option=args[1], args=args[2:len(args)])
    return None


def _show_alert(head=None, meg=None):
    return showwarning(title=head, message=meg)


def _show_message(message=None):
    pass


def _call_func(option=None, args=()):
    if option == "exit":
        _exit_out()


def _exit_out():
    global _root
    _root.destroy()
    exit(0)


def _handle_input(content, reason, widget):
    global _infoEntry131, _infoEntry132
    global _infoEntry133, _infoEntry134
    print_log("_handle_input: "
              "content=%s reason=%s widget=%s"
              % (content, reason, widget))
    if str(_infoEntry11) == widget:
        return _handle_input_name(content, reason, widget)
    if str(_infoEntry12) == widget:
        return _handle_input_work_id(content, reason, widget)
    if str(_infoEntry131) == widget \
            or str(_infoEntry132) == widget \
            or str(_infoEntry133) == widget \
            or str(_infoEntry134) == widget:
        return _handle_input_ip_box(content, reason, widget)


def _handle_input_name(content, reason, widget):
    print_log("_handle_input_name: "
              "content=%s reason=%s widget=%s"
              % (content, reason, widget))
    if len(content) <= 4:
        return True
    return False


def _handle_input_work_id(content, reason, widget):
    print_log("_handle_input_work_id: "
              "content=%s reason=%s widget=%s"
              % (content, reason, widget))
    return len(content) < 10 \
           and (not check_chines(content))


def _handle_input_ip_box(content, reason, widget):
    global _infoEntry131, _infoEntry132, _infoEntry133, _infoEntry134
    print_log("_handle_input_ip_box: "
              "content=%s reason=%s widget=%s"
              % (content, reason, widget))
    if content != "" and content[-1] == ".":
        if str(_infoEntry131) == widget:
            _infoEntry132.focus_set()
            return False
        if str(_infoEntry132) == widget:
            _infoEntry133.focus_set()
            return False
        if str(_infoEntry133) == widget:
            _infoEntry134.focus_set()
            return False
        if str(_infoEntry134) == widget:
            _infoEntry131.focus_set()
            return False
        return True
    return check_ip_single_value(content)


def _handel_key_ip_box(event):
    global _infoEntry131, _infoEntry132, _infoEntry133, _infoEntry134
    var = event.widget.get()
    cursor = event.widget.index(INSERT)
    print("_handel_key_ip_box %s from %s" % (event.keysym, event.widget))
    print("handel_del_ip_box var:%s cursor:%d" % (var, cursor))
    if event.keysym == "BackSpace":
        if event.widget is _infoEntry131:
            return False
        if event.widget is _infoEntry132:
            if var == "":
                _infoEntry131.focus_set()
                return True
            return False
        if event.widget is _infoEntry133:
            if var == "":
                _infoEntry132.focus_set()
                return True
            return False
        if event.widget is _infoEntry134:
            if var == "":
                _infoEntry133.focus_set()
                return None
            return None
    elif event.keysym == "Delete":
        if event.widget is _infoEntry131:
            if var == "":
                _infoEntry132.focus_set()
                _infoEntry132.icursor(0)
                return True
            return False
        if event.widget is _infoEntry132:
            if var == "":
                _infoEntry133.focus_set()
                _infoEntry133.icursor(0)
                return True
            return False
        if event.widget is _infoEntry133:
            if var == "":
                _infoEntry134.focus_set()
                _infoEntry134.icursor(0)
                return True
            return False
        if event.widget is _infoEntry134:
            return False
    elif event.keysym == "Left":
        if event.widget is _infoEntry131:
            return False
        if event.widget is _infoEntry132:
            if cursor == 0:
                _infoEntry131.focus_set()
                _infoEntry131.icursor(END)
                return True
            return False
        if event.widget is _infoEntry133:
            if cursor == 0:
                _infoEntry132.focus_set()
                _infoEntry132.icursor(END)
                return True
            return False
        if event.widget is _infoEntry134:
            if cursor == 0:
                _infoEntry133.focus_set()
                _infoEntry133.icursor(END)
                return True
            return False
    elif event.keysym == "Right":
        if event.widget is _infoEntry131:
            if cursor == len(var):
                _infoEntry132.focus_set()
                _infoEntry132.icursor(0)
                return True
            return False
        if event.widget is _infoEntry132:
            if cursor == len(var):
                _infoEntry133.focus_set()
                _infoEntry133.icursor(0)
                return True
            return False
        if event.widget is _infoEntry133:
            if cursor == len(var):
                _infoEntry134.focus_set()
                _infoEntry134.icursor(0)
                return True
            return False
        if event.widget is _infoEntry134:
            return False
    elif event.keysym == "Home":
        _infoEntry131.focus_set()
        _infoEntry131.icursor(0)
    elif event.keysym == "End":
        _infoEntry134.focus_set()
        _infoEntry134.icursor(0)

if __name__ == '__main__':
    _root = Tk()
    _root.resizable(width='false', height='false')
    _root.title("日志系统客户端")
    _root.protocol('WM_DELETE_WINDOW', _exit_out)
    center_window(_root, 800, 800)

    _check_input = _root.register(_handle_input)  # 需要将函数包装一下，必要的

    _infoLabel1 = Label(_root, text="日期：%s" % get_date_time()[0], font=font_fs(size=12))
    _infoLabel1.pack(side=TOP, padx=10, pady=10)

    _infoFrame1 = LabelFrame(_root, height=50)
    _infoFrame1.pack(side=TOP, fill=X, padx=20)

    _infoLabel11 = Label(_infoFrame1, text="姓名：", font=font_fs(size=12))
    _infoLabel11.pack(side=LEFT, padx=10, pady=10)
    # validate选项指定为key时输入被拦截
    # 此处在Entry的get之前执行
    # 因此只能使用 % P来获得最新的输入框的内容
    v11 = StringVar()
    _infoEntry11 = Entry(_infoFrame1, width=10, font=font_yh(size=12),
                         textvariable=v11, validate="key",
                         validatecommand=(_check_input, '%P', '%v', '%W'))
    _infoEntry11.pack(side=LEFT, padx=10, pady=10)

    _infoLabel12 = Label(_infoFrame1, text="工号：", font=font_fs(size=12))
    _infoLabel12.pack(side=LEFT, padx=10, pady=10)
    v12 = StringVar()
    _infoEntry12 = Entry(_infoFrame1, width=10, font=font_yh(size=12),
                         textvariable=v12, validate="key",
                         validatecommand=(_check_input, '%P', '%v', '%W'))
    _infoEntry12.pack(side=LEFT, padx=10, pady=10)

    _infoLabel13 = Label(_infoFrame1, text="目标IP：", font=font_fs(size=12))
    _infoLabel13.pack(side=LEFT, padx=10, pady=10)
    # ---box1---
    v131 = StringVar()
    _infoEntry131 = Entry(_infoFrame1, width=4, font=font_yh(size=10),
                          textvariable=v131, validate="key",
                          validatecommand=(_check_input, '%P', '%v', '%W'))
    _infoEntry131.pack(side=LEFT, pady=10)
    _infoEntry131.bind("<Key>", _handel_key_ip_box)
    # ---point1---
    _infoLabel131 = Label(_infoFrame1, text=".", font=font_fs(size=10))
    _infoLabel131.pack(side=LEFT, pady=10)
    # ---box2---
    v132 = StringVar()
    _infoEntry132 = Entry(_infoFrame1, width=4, font=font_yh(size=10),
                          textvariable=v132, validate="key",
                          validatecommand=(_check_input, '%P', '%v', '%W'))
    _infoEntry132.pack(side=LEFT, pady=10)
    _infoEntry132.bind("<Key>", _handel_key_ip_box)
    # ---point2---
    _infoLabel131 = Label(_infoFrame1, text=".", font=font_fs(size=10))
    _infoLabel131.pack(side=LEFT, pady=10)
    # ---box3---
    v133 = StringVar()
    _infoEntry133 = Entry(_infoFrame1, width=4, font=font_yh(size=10),
                          textvariable=v133, validate="key",
                          validatecommand=(_check_input, '%P', '%v', '%W'))
    _infoEntry133.pack(side=LEFT, pady=10)
    _infoEntry133.bind("<Key>", _handel_key_ip_box)
    # ---point3---
    _infoLabel131 = Label(_infoFrame1, text=".", font=font_fs(size=10))
    _infoLabel131.pack(side=LEFT, pady=10)
    # ---box4---
    v134 = StringVar()
    _infoEntry134 = Entry(_infoFrame1, width=4, font=font_yh(size=10),
                          textvariable=v134, validate="key",
                          validatecommand=(_check_input, '%P', '%v', '%W'))
    _infoEntry134.pack(side=LEFT, pady=10)
    _infoEntry134.bind("<Key>", _handel_key_ip_box)

    _infoButton11 = Button(_infoFrame1, text="保存信息", width=10, command=_save_user_button_clicked)
    _infoButton11.pack(side=LEFT, padx=20, pady=10)

    # _infoEntry14 = Entry(_infoFrame1, width=10, font=font_yh(size=12))
    # _infoEntry14.pack(side=RIGHT, padx=10, pady=10)

    _infoFrame2 = LabelFrame(_root, height=580)
    _infoFrame2.pack(side=TOP, fill=BOTH, padx=20, pady=20)
    _infoFrame2.pack_propagate(0)

    _infoFrame21 = LabelFrame(_infoFrame2)
    _infoFrame21.pack(fill=X)

    _infoLabel211 = Label(_infoFrame21, text="计划日报：", font=font_yh(size=12))
    _infoLabel211.pack(side=LEFT, pady=10)

    _infoText21 = ScrolledText(_infoFrame2, bg="white", height=12, undo=True, font=font_fs(size=14))
    _infoText21.pack(fill=X)

    _infoFrame22 = LabelFrame(_infoFrame2)
    _infoFrame22.pack(fill=X)

    _infoLabel221 = Label(_infoFrame22, text="总结日报:", font=font_yh(size=12))
    _infoLabel221.pack(side=LEFT, pady=10)

    _infoText22 = ScrolledText(_infoFrame2, bg="white", height=12, undo=True, font=font_fs(size=14))
    _infoText22.pack(fill=X)

    _submitButton = Button(_root, text="提交到服务器", width=10, command=_submit_button_clicked)
    _submitButton.pack(side=RIGHT, padx=20)

    _load_user_form_file()
    _load_report_form_file()
    _client = Client(callback=client_callback)
    _root.mainloop()
