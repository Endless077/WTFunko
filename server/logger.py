import os
import sys
import re
import string
from ast import literal_eval


from datetime import datetime as dt

def get_logger():
    if Logger._instance is None:
        filename = f"logs_{dt.now().strftime('%Y%m%d-%H%M%S%f')}.txt"
        directory = "../source/logs"
        # Singleton instantiation, first time.
        Logger(filename, directory)
    return Logger._instance

class Logger(object):
    _instance = None

    def __new__(cls, filename=None, directory=None):
        if cls._instance is None:
            if filename is None or directory is None:
                raise ValueError("Filename and directory must be provided for the first initialization.")
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(filename, directory)
        return cls._instance

    def _initialize(self, file=None, out_dir=None):
        if file is not None and out_dir is not None:
            if not isinstance(file, str) or not isinstance(out_dir, str):
                self.write("Logging", "Error: File name and directory must be strings.")
                self.log = None
            elif any(c in r'\/:*?"<>|' for c in file):
                self.write("Logging", "Error: File name contains invalid characters.")
                self.log = None
            else:
                if not os.path.exists(f"./{out_dir}"):
                    os.mkdir(f"./{out_dir}")
                curr_date = dt.now().isoformat().replace(':', '-')
                self.log = open(f"./{out_dir}/{file}_{curr_date}.txt", "x")
        else:
            self.log = None

    def write(self, tag, text):
        curr_time = dt.now().strftime("%H:%M:%S")
        log_message = f"[{tag} - {curr_time}] {text}\n"
        sys.stdout.write(log_message)
        
        if self.log:
            self.log.write(log_message)
        
    def flush(self):
        if self.log:
            self.log.flush()