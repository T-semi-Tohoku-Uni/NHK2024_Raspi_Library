import datetime
import os

class LogSystem:
    def __init__(self):
        # create main log directory
        main_log_dir = "logs"
        os.makedirs("logs", exist_ok=True)
        
        # create sub log directory (format: logs/YYYYMMDD_HHMMSS)
        self.log_dir = os.path.join(main_log_dir, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        os.makedirs(self.log_dir, exist_ok=True)
        
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
            log_file.write(message + "\n")
    
    def write_with_file_id(self, message, file_id):
        """
        write log message to specified log file
        
        Args:
            message (str): log message
            file_id (str): log file id (can_id, udp_id, etc.)
        """
        with open(os.path.join(self.log_dir, file_id), "a") as log_file:
            log_file.write(message + "\n")
    
if __name__ == "__main__":
    log_system = LogSystem()
    log_system.write("This is a log message.")