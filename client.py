#coding=utf-8
#@auth: applex
#@date: 2018-03-27

import socket
import pickle
from support import *


class Client:
    def __init__(self, host_ip=socket.gethostname(), callback=None):
        self.s = None
        self.host = host_ip
        self.port = 7777
        self.callback = callback


    def destroy(self):
        try:
            self.s.close()
            return True
        except Exception as e:
            print_log("Client: destroy exception:", e)
            return False


    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True) #允许地址重复占用
        self.s.setblocking(True)
        self.s.settimeout(10)  # 1s
        try:
            self.s.connect((self.host, self.port))
            return True
        except Exception as e:
            print_log("Client: connect exception:", e)
            if self.callback:
                if "ok" == self.callback("alert", "错误", "无法连接到服务端！"):
                    self.callback("option", "exit")
            return False


    def send_data(self, data):
        try:
            # 序列化数据
            byte_data = pickle.dumps(data)
            self.s.sendall(byte_data)
            print_log("Client: send finished!")
            # while True:
            #     message = self.s.recv(1024)
            #     return self._handle_response(message)
        except Exception as e:
            print_log("Client: _send_data exception:", e)
            if self.callback:
                self.callback("alert", "错误", "数据发送失败！")
            return False

    def _handle_response(self, message):
        print_log("Client: _handle_receive_message:", message)
        return True


if __name__ == '__main__':
    client = Client()
    if client.connect():
        # client.send_data({"title": u"哈哈哈哈哈哈", "msg": u"滚滚滚"})
        client.send_data(("哈",))
        client.destroy()

