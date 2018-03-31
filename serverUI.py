# coding=utf-8
# @auth: applex
# @date: 2018-03-27

from Tkinter import *
from ttk import *
from tkMessageBox import *
from ScrolledText import ScrolledText
from server import *
from support import *
from serverInfoDealer import *

STR_SERVER_START = "点击启动服务"
STR_SERVER_STOP = "点击终止服务"


def _server_button_clicked():
    global _buttonState
    _buttonState = ~_buttonState
    print_log("_buttonState", _buttonState)
    if _buttonState:
        _start_server_thread()
    else:
        _stop_server_thread()


def _start_server_thread():
    print_log("_start_server_thread", _buttonState)
    global _server
    global _serverButton,  _serverInfoLabel
    if _server.bind():
        _serverButton.config(text=STR_SERVER_STOP)
        _serverInfoLabel.config(text="服务创建成功...")
    else:
        _serverInfoLabel.config(text="服务创建失败...")


def _stop_server_thread():
    print_log("_stop_server_thread", _buttonState)
    global _server
    global _serverButton, _serverInfoLabel
    if _server.destroy():
        _serverButton.config(text=STR_SERVER_START)
        _serverInfoLabel.config(text="服务已终止！")


def server_callback(*args):
    if not args:
        print_log("serverUI: callback do noting", args)
        return None
    if args[0] == "message":
        return _show_message(message=args[1])
    elif args[0] == "alert":
        return _show_alert(head=args[1], meg=args[2])
    elif args[0] == "option":
        cargs = args[2:len(args)]
        print_log("args:", args, "cargs:", cargs)
        return _call_func(option=args[1], args=args[2:len(args)])
    return None


def _show_message(message=None):
    global _infoText
    if message:
        _infoText.config(state=NORMAL)
        _infoText.insert(END, message)
        _infoText.see(END)
        _infoText.config(state=DISABLED)


def _show_alert(head=None, meg=None):
    return showwarning(title=head, message=meg)


def _show_address(ip, port=None):
    address = None
    if ip:
        address = "IP: %s" % ip
        # if port:
        #     address = address + ":%s" % port
        _serverIpLabel.config(text=address)


def _call_func(option=None, args=()):
    if option == "exit":
        _exit_out()
    elif option == "show_ip":
        _show_address(*args)
    elif option == "handle_message":
        _handle_receive_message(*args)


def _handle_receive_message(address, message):
    handle_message(server_callback, address, message)

def _exit_out():
    global _root
    _stop_server_thread()
    _root.destroy()
    exit(0)


if __name__ == '__main__':
    _buttonState = False
    _root = Tk()
    _root.resizable(width='false', height='false')
    _root.title("日志系统服务端")
    _root.protocol('WM_DELETE_WINDOW', _exit_out)
    center_window(_root, 800, 600)

    _infoLabel1 = Label(_root, text="消息提示：", font=font_yh(size=12))
    _infoLabel1.grid(row=0, column=0, padx=10, pady=10, sticky=W)

    _serverButton = Button(_root, text=STR_SERVER_START, command=_server_button_clicked)
    # _serverButton.grid(row=0, column=1, padx=10, pady=10, sticky=E)

    _serverInfoLabel = Label(_root, font=font(size=11))
    _serverInfoLabel.grid(row=0, column=0, padx=10, pady=10, sticky=E)

    _serverIpLabel = Label(_root, font=font(size=11))
    _serverIpLabel.grid(row=0, column=1, padx=10, pady=10, sticky=W)

    _infoText = ScrolledText(_root, bg='white', width=100, height=30, state=DISABLED)
    _infoText.grid(row=1, columnspan=2, padx=10, pady=10)

    _server = Server(server_callback)
    _start_server_thread()
    _root.mainloop()
