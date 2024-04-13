import socket
import can
import time
from abc import ABCMeta, abstractmethod
from typing import Any, Type
from enum import Enum
from .log_system import LogSystem
import sys
import os

class MainController:
    def __init__(self, host_name: str = None, port: str = None, port_for_wheel_controle: str = None, is_udp=True):
        # can Listerの初期化(Noneのままだとエラー出るはず)
        self.notifier = None
        
        # ログの初期化
        self.log_system = LogSystem()
        self.log_system.write("Success : Init Log system")
        print("Success : Init Log system")
        
        # プロセスIDの取得
        pid = os.getpid()
        print(f"Process ID is {pid}")
        print(f"sudo kill -9 {pid}")
        self.log_system.write(f"Process ID is {pid}")
        self.log_system.write(f"sudo kill -9 {pid}")
        
        # UDPの初期化 (足回り以外用)
        if is_udp is True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # Check port is not None
                if port is None or host_name is None:
                    raise Exception("port or host_name is None")
                self.sock.bind((host_name, port))
            except Exception as e:
                self.log_system.update_error_log("Init UDP Error: " + e.__str__())
                self.log_system.write("Init UDP Error: " + e.__str__())
                print("Init UDP Error: " + e.__str__(), file=sys.stderr)
                sys.exit(1)

        self.log_system.write("Success : Init UDP socket")
        self.log_system.write("host_name={}, port={}".format(host_name, port))
        print("Success : Init UDP socket")
        print("host_name={}, port={}".format(host_name, port))

        # UDPの初期化 (足回り用)
        if is_udp is True:
            try:
                self.socket_for_wheel_controle = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # Check udp_port_for_other is not None
                if port_for_wheel_controle is None or host_name is None:
                    raise Exception("udp_port_for_wheel or host_name is None")
                self.socket_for_wheel_controle.bind((host_name, port_for_wheel_controle))
            except Exception as e:
                self.log_system.update_error_log("Init UDP Error: " + e.__str__())
                self.log_system.write("Init UDP Error: " + e.__str__())
                print("Init UDP Error: " + e.__str__(), file=sys.stderr)

        self.log_system.write("Success : Init UDP socket")
        self.log_system.write("host_name={}, port={}".format(host_name, port_for_wheel_controle))
        print("Success : Init UDP socket")
        print("host_name={}, port={}".format(host_name, port_for_wheel_controle))        
        
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
        msg = can.Message(timestamp=current_timestamp, arbitration_id=can_id, data=data, is_extended_id=False, is_rx=False)
        
        try:
            self.bus.send(msg, timeout=0.01)
        except can.exceptions.CanOperationError as e:
            self.log_system.write("Buffer Error: " + e.__str__())
            self.log_system.update_error_log("Buffer Error: " + e.__str__())
            print("Buffer Error: " + e.__str__(), file=sys.stderr)
            return
        except Exception as e:
            self.log_system.write("Error: " + e.__str__())
            self.log_system.update_error_log("Error: " + e.__str__())
            print("Error: " + e.__str__(), file=sys.stderr)
            return
        
        self.log_system.write(f"Send: {msg.__str__()}")
        self.log_system.update_send_can_log(msg)
        print(f"Send: {msg.__str__()}")
        #time.sleep(0.01)
        
    def read_udp(self) -> str:
        raw_data, raw_addr = self.sock.recvfrom(1024)
        data = raw_data.decode()
        addr = raw_addr[0].__str__()
        self.log_system.write("Read UDP : data={}, addr={}".format(data, addr))
        self.log_system.write_with_udp_client_name(data, addr)
        print("Read UDP : data={}, addr={}".format(data, addr))
        return data
    
    def read_udp_for_wheel_controle(self) -> str:
        raw_data, raw_addr = self.socket_for_wheel_controle.recvfrom(1024)
        data = raw_data.decode()
        addr = raw_addr[0].__str__()
        self.log_system.write("Read UDP : data={}, addr={}".format(data, addr))
        self.log_system.write_with_udp_client_name(data, addr)
        print("Read UDP : data={}, addr={}".format(data, addr))
        return data

    def __del__(self):
        # close UDP socket
        if hasattr(self, 'sock') and self.sock is not None:
            self.sock.close()
        # close CAN notifier
        if hasattr(self, 'notifier') and self.notifier is not None:
            self.notifier.stop()
        # close CAN socket
        if hasattr(self, 'bus') and self.bus is not None:
            self.bus.shutdown()
    
    @abstractmethod
    def main(self, *args: Any, **kwargs: Any) -> None:
        """
        ここにアルゴリズムを書く
        """