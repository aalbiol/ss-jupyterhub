import os
import logging
import datetime
from pathlib import Path

class UPVlog(logging.Handler): 
    def __init__(self):
        directorio="/srv/log/users/"
        self.usuario=os.getenv("USER")
        self.logger = logging.getLogger(self.usuario)
        directory_path = Path(directorio)
        directory_path.mkdir(parents=True, exist_ok=True)
        self.file_handler = logging.FileHandler(directorio+self.usuario+".log", mode="a")
        self.logger.addHandler(self.file_handler)
        self.logger.propagate = False
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        
        self.logger.info(f"User {self.usuario} Starting logging at {datetime.datetime.now()}")
        self.file_handler.flush()
    def __del__(self):
        self.logger.info(f"{self.usuario} * {datetime.datetime.now()} * {"Cerrando logger"}")
        self.file_handler.flush()
        self.logger.removeHandler(self.file_handler) 
        self.file_handler.close()
        del self.logger
        
    def log(self, mensaje):
        try:
            self.logger.info(f"{self.usuario} * {datetime.datetime.now()} * {mensaje}")
            self.file_handler.flush()
        except Exception:
            print("Could not log")