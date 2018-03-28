# coding=utf-8
# @auth: applex
# @date: 2018-03-27

import socket
import pickle
# import thread
from threading import Thread
from simpleThreadPool import WorkThread
from support import *


class Server:
    def __init__(self, callback=None):
        self.s = None
        self.host = socket.gethostname()
        self.port = 7777
        self.startFlag = False
        self.callback = callback


    def destroy(self):
        try:
            self.s.close()
            self.startFlag = False
            return True
        except Exception as e:
            print "Server: destroy exception: ", e
            return False


    def bind(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True) #允许地址重复占用
        self.s.setblocking(True)
        self.s.settimeout(1)  # 1s
        try:
            self.s.bind((self.host, self.port))
            self.s.listen(5)
            print_log("Server: socket bind ip:", self.s.getsockname())
            self.callback("option", "show_ip", self.s.getsockname())
        except Exception as e:
            print_log("Server: socket bind exception", e)
            if self.callback:
                if "ok" == self.callback("alert", "警告", "程序已在运行中！"):
                    self.callback("option", "exit")
                return None
        self.startFlag = True
        try:
            accept_td = WorkThread(thread_id=1, thread_name="socket_accept", execute=self._accept)
            accept_td.start()
            # thread.start_new_thread(self._accept, ("socket.accept_thread", 1))
            # self._accept("_accept", 1)
            return True
        except Exception as e:
            print "Server: socket start _accept thread exception", e

            return False


    def _accept(self):
        while self.startFlag:
            print_log("socket: _accept", self.startFlag)
            try:
                conn, address = self.s.accept()
                message = None
                try:
                    message = conn.recv(1024)
                    data = message
                    while data:
                        data = conn.recv(1024)
                        message = message + data
                except Exception as e:
                    # error 10035
                    print_log("receiver data:", e)
                if message:
                    # 反序列化数据
                    string_message = pickle.loads(message)
                    self._handle_message(conn, address, string_message)
                    conn.send("SUCCEED")
                conn.close()
            except Exception as e:
                print_log("_accept:", e)


    def _handle_message(self, conn, address, message):
        print_log("Server: socket _handle_message ", conn, address, message)
        if self.callback:
            self.callback("message", "来自客户端：%s的消息：%s" % (address, message))

