import datetime
import os

class LogSystem:
    def __init__(self):
        self.log_dir = "logs"
        os.makedirs("logs", exist_ok=True)
        
        self.log_file_name = "log_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
        self.log_file_path = os.path.join(self.log_dir, self.log_file_name)
        
    def write(self, message):
        with open(self.log_file_path, "a") as log_file:
            log_file.write(message + "\n")
            
if __name__ == "__main__":
    log_system = LogSystem()
    log_system.write("This is a log message.")