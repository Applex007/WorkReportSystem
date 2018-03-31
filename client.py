#coding=utf-8
#@auth: applex
#@date: 2018-03-27

import socket
import time
from simpleThreadPool import *
from support import *


class Client:
    def __init__(self, callback=None):
        self.s = None
        self.port = 7777
        self.callback = callback


    def destroy(self):
        try:
            self.s.close()
            return True
        except Exception as e:
            print_log("Client: destroy exception:", e)
            return False


    def connect(self, host_ip=None):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True) #允许地址重复占用
        self.s.setblocking(True)
        self.s.settimeout(10)  # 3s
        try:
            self.s.connect((host_ip, self.port))
            return True
        except Exception as e:
            print_log("Client: connect exception:", e)
            if self.callback:
                if "ok" == self.callback("alert", "错误", "无法连接到服务端！"):
                    # self.callback("option", "exit")
                    pass
            return False


    def send_data(self, data):
        print_log("Client: send_data", data)
        # 序列化数据
        byte_data = json_encode(data)
        print_log("Client: first send_data len:", len(byte_data))
        len_byte_data = json_encode({"len": len(byte_data)})
        self._send_data_inner(len_byte_data)
        res = self._receive_data(1)
        print_log("Client: receive result:", res)
        print_log("Client: second send_data:", byte_data)
        self._send_data_inner(byte_data)
        res = self._receive_data(1)
        print_log("Client: receive result:", res)
        if self.callback:
            if res == "SUCCEED":
                self.callback("alert", "提示", "提交成功！")
            else:
                self.callback("alert", "提示", "提交失败！")


    def _send_data_inner(self, data):
        try:
            print_log("Client: do send data:", data, len(data))
            self.s.sendall(data)
            print_log("Client: send finished!")
        except Exception as e:
            print_log("Client: _send_data exception:", e)
            if self.callback:
                self.callback("alert", "错误", "数据发送失败！")
            return False

    def _receive_data(self, sleep_seconds):
        try:
            time.sleep(sleep_seconds)
            message = self.s.recv(1024)
            return message
        except Exception as e:
            print_log("Clinet: receive_data", e)

    def _handle_response(self, message):
        print_log("Client: _handle_receive_message:", message)
        return True


if __name__ == '__main__':
    client = Client()
    if client.connect():
        client.send_data({"title": u"哈哈哈哈哈哈", "msg": u"滚滚滚"})
        # client.send_data("a")
        client.destroy()

