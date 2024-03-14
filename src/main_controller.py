import socket
import can
import time
from abc import ABCMeta, abstractmethod
from typing import Any, Type
from enum import Enum
from .log_system import LogSystem
import sys

class MainController:
    def __init__(self, host_name: str, port: str):
        # can Listerの初期化(Noneのままだとエラー出るはず)
        self.notifier = None
        
        # ログの初期化
        self.log_system = LogSystem()
        self.log_system.write("Success : Init Log system")
        print("Success : Init Log system")
        
        # UDPの初期化
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((host_name, port))
        except Exception as e:
            self.log_system.update_error_log("Init UDP Error: " + e.__str__())
            self.log_system.write("Init UDP Error: " + e.__str__())
            print("Init UDP Error: " + e.__str__(), file=sys.stderr)
            # sys.exit(1)

        self.log_system.write("Success : Init UDP socket")
        self.log_system.write("host_name={}, port={}".format(host_name, port))
        print("Success : Init UDP socket")
        print("host_name={}, port={}".format(host_name, port))
        
        
        # can通信の初期化
        try:
            self.bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=1000000, fd=True, data_bitrate=2000000)
        except Exception as e:
            self.log_system.update_error_log("Init CAN Error: " + e.__str__())
            self.log_system.write("Init CAN Error: " + e.__str__())
            print("Init CAN Error: " + e.__str__(), file=sys.stderr)
            sys.exit(1)
        self.log_system.write("Success : Init CAN socket")
        print("Success : Init CAN socket")
    
    def init_can_notifier(self, lister: Type[can.Listener]):
        try:
            self.notifier = can.Notifier(self.bus, [lister])
        except Exception as e:
            self.log_system.update_error_log("Init CAN Listener Error: " + e.__str__())
            self.log_system.write("Init CAN Listener Error: " + e.__str__())
            print("Init CAN Listener Error: " + e.__str__(), file=sys.stderr)
            sys.exit(1)
        self.log_system.write("Success : Init CAN Listener")
        print("Success : Init CAN Listener")
    
    def write_can_bus(self, can_id: int, data: bytearray):
        current_timestamp = time.time()
        msg = can.Message(timestamp=current_timestamp, arbitration_id=can_id, data=data, is_extended_id=False)
        
        try:
            self.bus.send(msg, timeout=0.01)
        except can.exceptions.CanOperationError as e:
            self.log_system.write("Buffer Error: " + e.__str__())
            self.log_system.update_error_log("Buffer Error: " + e.__str__())
            print("Buffer Error: " + e.__str__(), file=sys.stderr)
            return
        except Exception as e:
            self.log_system.write("Error: " + e.__str__())
            self.log_system.write_error_log("Error: " + e.__str__())
            print("Error: " + e.__str__(), file=sys.stderr)
            return
        
        self.log_system.write(f"Send: {msg.__str__()}")
        self.log_system.update_send_can_log(msg)
        print(f"Send: {msg.__str__()}")
        time.sleep(0.01)
        
    def read_udp(self) -> str:
        raw_data, raw_addr = self.sock.recvfrom(1024)
        data = raw_data.decode()
        addr = raw_addr[0].__str__()
        self.log_system.write("Read UDP : data={}, addr={}".format(data, addr))
        self.log_system.write_with_udp_client_name(data, addr)
        print("Read UDP : data={}, addr={}".format(data, addr))
        return data
    
    def __del__(self):
        # close UDP socket
        self.sock.close()
        # close CAN notifier
        self.notifier.stop()
        # close CAN socket
        self.bus.shutdown()
    
    @abstractmethod
    def main(self, *args: Any, **kwargs: Any) -> None:
        """
        ここにアルゴリズムを書く
        """