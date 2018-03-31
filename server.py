# coding=utf-8
# @auth: applex
# @date: 2018-03-27

import socket
import time
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
        self.s.settimeout(3)  # 3s
        try:
            self.s.bind((self.host, self.port))
            self.s.listen(5)
            print_log("Server: socket bind ip:", self.s.getsockname()[0])
            self.callback("option", "show_ip", self.s.getsockname()[0])
        except Exception as e:
            print_log("Server: socket bind exception", e)
            if self.callback:
                if "ok" == self.callback("alert", "警告", "程序已在运行中！"):
                    self.callback("option", "exit")
                return None
        self.startFlag = True
        try:
            accept_td = WorkThread(thread_id=1, thread_name="server_accept", execute=self._accept)
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
                print_log("Server: first try receive len_data")
                data = self._receive_data(conn, 100, 0.5)
                print_log("Server: receive len_data:", data)
                if data:
                    print_log("Server: response len_data receive OK")
                    conn.send("SUCCEED")
                    len_data = json_decode(data)
                    length = len_data["len"]
                    # 接收到数据长度后，尝试 3 次
                    COUNT = 3
                    while COUNT > 0:
                        data = self._receive_data(conn, length, 1)
                        print_log("Server: Second try receive data")
                        if data:
                            # 反序列化数据
                            decode_data = json_decode(data)
                            self._handle_message(conn, address, decode_data)
                            print_log("Server: response data receive OK")
                            conn.send("SUCCEED")
                            break
                        COUNT = COUNT - 1
            except Exception as e:
                print_log("Server: accept", e)


    def _receive_data(self, conn, data_len, sleep_seconds):
        if conn:
            try:
                # 接收前等待一段时间
                time.sleep(sleep_seconds)
                data = conn.recv(data_len)
            except Exception as e:
                # error 10035
                print_log("receiver data:", e)
            finally:
                return data


    def _handle_message(self, conn, address, message):
        print_log("Server: socket _handle_message ", conn, address, message)
        if self.callback:
            self.callback("option", "handle_message", address, message)

