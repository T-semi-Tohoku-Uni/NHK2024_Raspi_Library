import datetime
import os
import datetime
import csv
import can

class LogSystem:
    def __init__(self):
        # create main log directory
        main_log_dir = "logs"
        os.makedirs("logs", exist_ok=True)
        
        # create sub log directory (format: logs/YYYYMMDD_HHMMSS)
        self.log_dir = os.path.join(main_log_dir, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        os.makedirs(self.log_dir, exist_ok=True)
        
        # create sub log directory (to save can)
        self.can_log_dir = os.path.join(self.log_dir, "can")
        os.makedirs(self.can_log_dir, exist_ok=True)
        
        self.received_can_log_dir = os.path.join(self.can_log_dir, "received")
        os.makedirs(self.received_can_log_dir, exist_ok=True)
        
        self.send_can_log_dir = os.path.join(self.can_log_dir, "send")
        os.makedirs(self.send_can_log_dir, exist_ok=True)
        
        # create sub log directory (to save udp)
        self.udp_log_dir = os.path.join(self.log_dir, "udp")
        os.makedirs(self.udp_log_dir, exist_ok=True)
        
        # create sub log directory (to save error or exception)
        self.error_log_dir = os.path.join(self.log_dir, "error")
        os.makedirs(self.error_log_dir, exist_ok=True)
        
        # define main log file name (format: log_main.log)
        main_log_file_name = "log_main.log"
        self.main_log_file_path = os.path.join(self.log_dir, main_log_file_name)
    
        # define user create file
        self.user_create_file = {}

    def create_new_log(self, file_name: str):
        user_create_file_path = os.path.join(self.log_dir, file_name)
        self.user_create_file[file_name] = user_create_file_path

    def write(self, message, log_file_name = None):
        """
        write log message to main log file
        
        Args:
            message (str): log message
        """
        if log_file_name is None:
            log_file_path = self.main_log_file_path
        else:
            if not log_file_name in self.user_create_file:
                return
            log_file_path = self.user_create_file[log_file_name]

        with open(log_file_path, "a") as log_file:
            log_file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}\n")

    def update_received_can_log(self, msg: can.Message):
        arbitration_id: int = msg.arbitration_id
        data: str = msg.data.hex()
        timestamp: float = msg.timestamp
        with open(os.path.join(self.received_can_log_dir, str(hex(arbitration_id)) + ".csv"), mode="a", newline='', encoding='utf-8') as log_file:
            writer = csv.writer(log_file)
            writer.writerow([timestamp, data])
    
    def update_send_can_log(self, msg: can.Message):
        arbitration_id: int = msg.arbitration_id
        data: str = msg.data.hex()
        timestamp: float = msg.timestamp
        with open(os.path.join(self.send_can_log_dir, str(hex(arbitration_id)) + ".csv"), mode="a", newline='', encoding='utf-8') as log_file:
            writer = csv.writer(log_file)
            writer.writerow([timestamp, data])
    
    def write_with_udp_client_name(self, message: str, client_name: str):
        """
        write log message to udp log file
        
        Args:
            message (str): log message
            client_name (str): udp client name
        """
        with open(os.path.join(self.udp_log_dir, client_name + ".log"), "a") as log_file:
            log_file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
    
    def update_error_log(self, message: str):
        """
        write error log message to error log file
        
        Args:
            message (str): log message
        """
        with open(os.path.join(self.error_log_dir, "error.log"), "a") as log_file:
            log_file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
    
if __name__ == "__main__":
    log_system = LogSystem()
    log_system.write("This is a log message.")
    # log_system.write_with_can_id("This is a log message with can id.", 0x123)
    log_system.write_with_udp_client_name("This is a log message with udp client name.", "client1")
    log_system.create_new_log("new_file")
    log_system.write("sample", "new_file")
