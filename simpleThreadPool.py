# coding=utf-8
# @auth: applex
# @date: 2018-03-28

import Queue
from threading import Thread
from support import *

class WorkThread(Thread):
    def __init__(self, thread_id=None, thread_name=None, start_call=None, end_call=None, execute=None, execute_args=()):
        super(WorkThread, self).__init__()
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.execute = execute
        self.execute_args = execute_args
        self.start_call = start_call
        self.end_call = end_call
        self.is_running = False

    def run(self):
        self.is_running = True
        if self.start_call:
            self.start_call()
        print_log("thread[%s %s] running" %(self.thread_id, self.thread_name))
        if self.execute:
            self.execute(*self.execute_args)
        self.is_running = False
        if self.end_call:
            self.end_call()

    def is_running(self):
        return self.is_running

class SimpleThreadPool:
    def __init__(self, max_size=0):
        self.max_size = max_size
        self.queue = Queue.queue()
