import socket
import can
import time
from abc import ABCMeta, abstractmethod
from typing import Any
from enum import Enum
from .log_system import LogSystem

class ButtonState(Enum):
    UP_WAIT = 0
    UP_FINISH = 1
    DOWN_WAIT = 2
    DOWN_FINISH = 3

class MainController:
    def __init__(self, host_name, port):
        # ログの初期化
        self.log_system = LogSystem()
        self.log_system.write("Success : Init Log system")
        
        # UDPの初期化
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host_name, port))
        self.log_system.write("Success : Init UDP socket")
        
        # can通信の初期化
        self.bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=5000000)
        self.log_system.write("Success : Init CAN socket")
        
    def write_can_bus(self, can_id: int, data: bytearray):
        msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
        self.bus.send(msg, timeout=0.01)
        
        self.log_system.write("Write CAN Bus : id={}, msg={}".format(can_id, data.hex()))
        self.log_system.write_with_can_id(data.hex(), can_id)
        time.sleep(0.01)
        
    def read_udp(self):
        data, addr = self.sock.recvfrom(1024)
        self.log_system.write("Read UDP : data={}, addr={}".format(data, addr))
        self.log_system.write_with_udp_client_name(data, addr.__str__())
        return data
    
    @abstractmethod
    def main(self, *args: Any, **kwargs: Any) -> None:
        """
        ここにアルゴリズムを書く
        """