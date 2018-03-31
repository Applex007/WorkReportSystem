# coding=utf-8
# @auth: applex
# @date: 2018-03-28

import Queue
from threading import Thread
from support import *

class WorkThread(Thread):
    def __init__(self, thread_id=None, thread_name=None,
                 start_call=None, start_call_args=(),
                 end_call=None, end_call_args=(),
                 execute=None, execute_args=()):
        super(WorkThread, self).__init__()
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.execute = execute
        self.execute_args = execute_args
        self.start_call = start_call
        self.start_call_args = start_call_args
        self.end_call = end_call
        self.end_call_args = end_call_args
        self.is_running = False

    def run(self):
        self.is_running = True
        if self.start_call:
            self.start_call(*self.start_call_args)
        print_log("thread[%s %s] running" % (self.thread_id, self.thread_name))
        if self.execute:
            self.execute(*self.execute_args)
        self.is_running = False
        if self.end_call:
            self.end_call(*self.end_call_args)

    def is_running(self):
        return self.is_running

class SimpleThreadPool:
    _max_size = 3
    _queue = Queue.Queue()
    _current_size = 0

    def __init__(self):
        pass

    @staticmethod
    def _add_td_to_queue(td):
        SimpleThreadPool._queue.put(td)


    @staticmethod
    def _thread_end_callback():
        td = SimpleThreadPool._remove_td_from_queue()
        if td and type(td) == SimpleThreadPool:
            td.start()

    @staticmethod
    def _remove_td_from_queue():
        if not SimpleThreadPool._queue:
            return SimpleThreadPool._queue.get()

    @staticmethod
    def submit(execute, args=()):
        wid = SimpleThreadPool._max_size - SimpleThreadPool._current_size
        wtd = WorkThread(thread_id=wid,
                         thread_name="SimpleThreadPool_thread",
                         end_call=SimpleThreadPool._thread_end_callback,
                         execute=execute,
                         execute_args=args)
        if SimpleThreadPool._current_size < SimpleThreadPool._max_size:
            wtd.start()
        else:
            SimpleThreadPool._add_td_to_queue(wtd)
            print_log("submit: thread[%s %s] add queue" % (wid, wtd))
