#coding=utf-8
#@auth: applex
#@date: 2018-03-27

import socket
import thread


class Server:
    def __init__(self, message_callback):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(100)
        self.host = socket.gethostname()
        self.port = 7777
        self.startFlag = False
        self.message_callback = message_callback


    def __del__(self):
        self.startFlag = False
        self.s.close()


    def bind(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        self.startFlag = True
        try:
            thread.start_new_thread(self.accept, ("socket.accept_thread", 1))
            # self.accept("accept", 1)
            return True
        except Exception as e:
            print "Server: socket bind, start accept thread exception", e
            return False


    def destroy(self):
        self.startFlag = False
        try:
            # self.s.shutdown(2)
            self.s.close()
            return True
        except Exception as e:
            print "error", e
            return False


    def accept(self, thread_id, delay):
        print "socket: accept", thread_id, delay
        while self.startFlag:
            print "socket: accept", self.startFlag
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
                    print "recv data exception:", e
                if message:
                    self.handle_message(conn, address, message)
                    conn.send("SUCCEED")
                conn.close()
            except Exception as e:
                print "accept timeout", e
        print "socket: shutdown", self.startFlag


    def handle_message(self, conn, address, message):
        print "socket: handle_message", conn, address, message
        self.message_callback("来自客户端：%s的消息：%s" %(address, message))









