# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import logging
import zmq
import msgpack
import time

def logger(s : str):
    logger = logging.getLogger(s)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter.converter = time.gmtime
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

ports = {
    "data" : {
    "dispatcher" : "tcp://127.0.0.1:5557",
    "broker_plivo" : "tcp://127.0.0.1:5558",
    "strategy_alert" : "tcp://127.0.0.1:5559",
    "ticker_yahoo" : "tcp://127.0.0.1:5560",
    "ticker_bitfutures" : "tcp://127.0.0.1:5561",
    "broker_bitmex" : "tcp://127.0.0.1:5562",
    "ticker_bravenewcoin" : "tcp://127.0.0.1:5563",
    },
    "control" : {
    "dispatcher" : "tcp://127.0.0.1:5577",
    "broker_plivo" : "tcp://127.0.0.1:5578",
    "strategy_alert" : "tcp://127.0.0.1:5579",
    "ticker_yahoo" : "tcp://127.0.0.1:5580",
    "ticker_bitfutures" : "tcp://127.0.0.1:5581",
    "broker_bitmex" : "tcp://127.0.0.1:5582",
    "ticker_bravenewcoin" : "tcp://127.0.0.1:5583"
    }
    }

def send(name, data):
    context = zmq.Context()
    for i in data:
        socket = context.socket(zmq.PUSH)
        socket.connect(ports[name][i['dest']])
        socket.send(msgpack.packb(i))

class AlgoObject(object):
    def __init__(self, name : str, socket_type):
        self._logger = logger(name)
        self._context = zmq.Context()
        self._poller = zmq.Poller()
        self._data_socket = self.socket(socket_type)

        self._control_socket = self.socket(zmq.PULL)
        self._control_socket.bind(ports['control'][name])
        self._poller.register(self._data_socket,
                              zmq.POLLIN)
        self._poller.register(self._control_socket,
                              zmq.POLLIN)
        self.info("starting %s" % name)
        self.timeout = None
    def socket(self, socket_type):
        return self._context.socket(socket_type)
    def send_data(self, message):
        self._data_socket.send(msgpack.packb(message))
    def recv_data(self):
        return msgpack.unpackb(self._data_socket.recv(),
                               encoding='utf-8')
    def recv_control(self):
        return msgpack.unpackb(self._control_socket.recv(),
                               encoding='utf-8')
    def debug(self, s):
        self._logger.debug(s)
    def info(self, s):
        self._logger.info(s)
    def error(self, s):
        self._logger.error(s)
    def warning(self, s):
        self._logger.warning(s)
    def process_data(self, data):
        raise NotImplementedError
    def process_control(self, data):
        pass
    def run_once(self):
        pass
    def run(self):
        while True:
            try:
                socks = dict(self._poller.poll(self.timeout))
            except KeyboardInterrupt:
                break
            if self._control_socket in socks:
                control = self.recv_control()
                self.process_control(control)
            if self._data_socket in socks:
                data = self.recv_data()
                self.process_data(data)
            self.run_once()
            

class Broker(AlgoObject):
    def __init__(self, name):
        AlgoObject.__init__(self, name, zmq.PULL)
        self._data_socket.bind(ports['data'][name])

class Ticker(AlgoObject):
    def __init__(self, name):
        AlgoObject.__init__(self, name, zmq.PUB)
        self._data_socket.bind(ports['data'][name])
        self.timeout = 30000
        self.quotes = {}
    def run_once(self):
        self.debug("running loop function")
        self.get_quotes()
        self.send_quotes()
    def send_quotes(self):
        self.debug("Sending quotes")
        self.send_data(self.quotes)
    def test(self):
        self.get_quotes()
        socket = self._context.socket(zmq.PUSH)
        socket.bind(algobroker.ports.dispatcher)
        message = { 'action' : 'log',
                    'item' : self.quotes }
        self._logger.debug("Sending data")
        socket.send(msgpack.packb(message))
