# coding=utf-8
# @auth: applex
# @date: 2018-03-27

from Tkinter import *
from server import *
from ScrolledText import ScrolledText

STR_SERVER_START = "点击启动服务"
STR_SERVER_STOP = "点击终止服务"
ServerState = False


def server_button_clicked():
    global ServerState
    ServerState = ~ServerState
    print "ServerState", ServerState
    if ServerState:
        start_server_thread()
    else:
        stop_server_thread()


def start_server_thread():
    print "start_server_thread", ServerState
    if server.bind():
        serverButton.config(text=STR_SERVER_STOP)
        serverInfoLabel.config(text="服务创建成功...")
    else:
        serverInfoLabel.config(text="服务创建失败...")


def stop_server_thread():
    print "stop_server_thread", ServerState
    if server.destroy():
        serverButton.config(text=STR_SERVER_START)
        serverInfoLabel.config(text="服务已终止！")


def show_message(message):
    infoText.insert(END, message)
    infoText.see(END)


server = Server(show_message)
root = Tk()
root.geometry('800x800')
root.resizable(width='false', height='false')
root.title("日志系统服务端")

infoLabel1 = Label(root, text="消息提示：")
infoLabel1.grid(row=0, column=0, padx=10, pady=10, sticky=W)

serverButton = Button(root, text=STR_SERVER_START, command=server_button_clicked)
# serverButton.grid(row=0, column=1, padx=10, pady=10, sticky=E)

serverInfoLabel = Label(root)
serverInfoLabel.grid(row=0, column=0, padx=10, pady=10, sticky=E)

infoText = ScrolledText(root, bg='gray', width=100, height=30)
infoText.grid(row=1, columnspan=2, padx=10, pady=10)

start_server_thread()
root.mainloop()