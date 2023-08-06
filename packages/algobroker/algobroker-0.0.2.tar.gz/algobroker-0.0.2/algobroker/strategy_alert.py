#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License
import my_path
import time
import zmq
import algobroker
import msgpack
from yahoo_finance import Share

class QuoteMonitor(object):
    def __init__(self):
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
        self.limits = {"3888.HK" : [ 15.0, 16.50],
                       "0700.HK" : [ 125.0, 135.0],
                       "0388.HK" : [ 175.0, 185.0]}
        self.quotes = {}
        self.sleep = 30
        self.maintainence = 60 * 30
        self._context = zmq.Context()
        self._zmq_socket = self._context.socket(zmq.PUSH)
        self._zmq_socket.bind(algobroker.ports.dispatcher)
        self._quote_source = self._context.socket(zmq.SUB)
        self._quote_source.connect(algobroker.ports.yahoo_quoter)
        self._quote_source.setsockopt(zmq.SUBSCRIBE, b'')
    def send_message(self, message):
        self._zmq_socket.send(msgpack.packb(message))
    def test_limits(self):
        for i in self.limits.keys():
            if i in self.limits and i in self.quotes:
                limits = self.limits[i]
                if limits[0] != None and self.quotes[i] <= limits[0]:
                    self.state[i] = "low"
                elif limits[1] != None and self.quotes[i] >= limits[1]:
                    self.state[i] = "high"
                else:
                    self.state[i] = "ok"
    def send_notices(self):
        msg = ""
        for k, v in self.state.items():
            if k in self.prev_state:
                prev_state = self.prev_state[k]
            else:
                prev_state = "none"
            if v == "high" or v == "low":
                if prev_state == "ok" or prev_state == "none":
                    msg += "%s - %f - %s | " % (k, self.quotes[k],
                                                v)
        if msg != "":
            self.send_message({'action' : 'alert',
                               'type' : 'sms',
                               'dst' : 'trader1',
                               'text' : msg})
        for k, v in self.state.items():
            self.prev_state[k] = v
    def test(self):
        work_message = { 'action' : 'log',
                         'item' : 'hello' }
        self.send_message(work_message)
        work_message = { 'action' : 'alert',
                         'type' : 'sms',
                         'dst'  : 'trader1',
                         'text' : 'hello and happy trading' }
        self.send_message(work_message)
    def run_once(self):
        print("running alert loop")
        data = msgpack.unpackb(self._quote_source.recv(),
                               encoding='utf-8')
        print(data)
        for k, v in data.items():
            self.quotes[k] = data[k]['last']
        self.test_limits()
        self.send_notices()
            
    def run(self):
        while True:
            self.run_once()

if __name__ == "__main__":
    qm = QuoteMonitor()
    qm.run()
