import os

bind = "0.0.0.0:9605"

workers = os.cpu_count() * 2 - 1

loglevel = "warning"

errorlog = os.path.join("logs", "error.log")

accesslog = os.path.join("logs", "access.log")
