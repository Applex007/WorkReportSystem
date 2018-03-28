# coding=utf-8
# @auth: applex
# @date: 2018-03-27

from Tkinter import *
from tkMessageBox import *
from server import *
from ScrolledText import ScrolledText
from support import *

STR_SERVER_START = "点击启动服务"
STR_SERVER_STOP = "点击终止服务"
ServerState = False


def _server_button_clicked():
    global ServerState
    ServerState = ~ServerState
    print_log("ServerState", ServerState)
    if ServerState:
        _start_server_thread()
    else:
        _stop_server_thread()


def _start_server_thread():
    print_log("_start_server_thread", ServerState)
    global server
    if server.bind():
        serverButton.config(text=STR_SERVER_STOP)
        serverInfoLabel.config(text="服务创建成功...")
    else:
        serverInfoLabel.config(text="服务创建失败...")


def _stop_server_thread():
    print_log("_stop_server_thread", ServerState)
    global server
    if server.destroy():
        serverButton.config(text=STR_SERVER_START)
        serverInfoLabel.config(text="服务已终止！")


def server_callback(*args):
    print_log("serverUI: callback", args)
    if args[0] == "message":
        return _show_message(args[1])
    elif args[0] == "alert":
        return _show_alert(args[1], args[2])
    elif args[0] == "option":
        return _call_func(args[1])
    return None


def _show_message(message):
    infoText.insert(END, message)
    infoText.see(END)

def _show_alert(tl=None, meg=None):
    return showwarning(title=tl, message=meg)

def _call_func(option):
    if option == "exit":
        _exit_out()

def _exit_out():
    _stop_server_thread()
    global _root
    _root.destroy()
    exit(0)


def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def _center_window(_root, width, height):
    screenwidth = _root.winfo_screenwidth()
    screenheight = _root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    print_log(size)
    _root.geometry(size)


_root = Tk()
_root.resizable(width='false', height='false')
_root.title("日志系统服务端")
_root.protocol('WM_DELETE_WINDOW', _exit_out)
_center_window(_root, 800, 600)

infoLabel1 = Label(_root, text="消息提示：")
infoLabel1.grid(row=0, column=0, padx=10, pady=10, sticky=W)

serverButton = Button(_root, text=STR_SERVER_START, command=_server_button_clicked)
# serverButton.grid(row=0, column=1, padx=10, pady=10, sticky=E)

serverInfoLabel = Label(_root)
serverInfoLabel.grid(row=0, column=0, padx=10, pady=10, sticky=E)

infoText = ScrolledText(_root, bg='gray', width=100, height=30)
infoText.grid(row=1, columnspan=2, padx=10, pady=10)

server = Server(server_callback)
_start_server_thread()
_root.mainloop()

