import datetime
import os
import datetime

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
        
        # create sub log directory (to save udp)
        self.udp_log_dir = os.path.join(self.log_dir, "udp")
        os.makedirs(self.udp_log_dir, exist_ok=True)
        
        # create sub log directory (to save error or exception)
        self.error_log_dir = os.path.join(self.log_dir, "error")
        os.makedirs(self.error_log_dir, exist_ok=True)
        
        # define main log file name (format: log_main.log)
        main_log_file_name = "log_main.log"
        self.main_log_file_path = os.path.join(self.log_dir, main_log_file_name)
        
    def write(self, message):
        """
        write log message to main log file
        
        Args:
            message (str): log message
        """
        with open(self.main_log_file_path, "a") as log_file:
            log_file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
    
    def write_with_can_id(self, message: str, can_id: int):
        """
        write log message to can log file
        
        Args:
            message (str): log message
            can_id (int): can id
        """
        with open(os.path.join(self.can_log_dir, str(can_id) + ".log"), "a") as log_file:
            log_file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
    
    def write_with_udp_client_name(self, message: str, client_name: str):
        """
        write log message to udp log file
        
        Args:
            message (str): log message
            client_name (str): udp client name
        """
        with open(os.path.join(self.udp_log_dir, client_name + ".log"), "a") as log_file:
            log_file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
    
    def write_error_log(self, message: str):
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
    log_system.write_with_can_id("This is a log message with can id.", 0x123)
    log_system.write_with_udp_client_name("This is a log message with udp client name.", "client1")